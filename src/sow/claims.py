"""Stages 8-9 -- extract claims from a section's evidence, then verify the quotes.

The model's only job here is to find factual assertions and copy the span each
one came from. It is explicitly told not to resolve disagreements: a passage
that contradicts another passage yields two claims under one fact key, and the
comparison happens in code (see ``sow.analysis``).

Verification is deterministic. A quote must be a character-for-character
substring of the passage it claims to come from, and the passage must be one
this section was actually given. A claim failing either check is rejected and
reported -- never repaired, never quietly kept.
"""

from __future__ import annotations

import re
import unicodedata

from .llm import LlmClient
from .models import Chunk, Claim, ClaimExtraction, EvidencePool, SectionSpec

STAGE = "extract_claims"

SYSTEM_PROMPT = """\
You extract factual claims from source passages for a Statement of Work.

Rules, in order of importance:

1. Every claim must come from one passage, and `quote` must be copied from that
   passage character for character. Do not paraphrase, tidy punctuation, fix
   spelling, expand abbreviations or join text across passages. A quote that is
   not an exact substring of its passage is discarded.
2. Extract only what a passage states. Never infer, combine or calculate.
3. NEVER resolve disagreements. If two passages state different values for the
   same fact, emit both as separate claims sharing one `fact_key`. If a single
   passage states a value and then corrects or withdraws it, emit both the
   original and the correction as separate claims sharing one `fact_key`. It is
   not your job to decide which is right.
4. `fact_key` is a short snake_case identifier for the fact itself, not for the
   passage: `go_live_date`, `payment_terms`, `change_request_approval_authority`.
   Use the same key for every claim about the same fact, whichever passage it
   came from. This is what lets the disagreement be detected.
5. `value` is the shortest precise form of the fact: a date as YYYY-MM-DD, an
   amount with its unit, otherwise a short noun phrase. Never a sentence.
6. `supports_elements` lists which of the section's required elements this claim
   helps satisfy, copied exactly from the list given. Use an empty list if none.

Extract every claim relevant to this section, including ones that appear
outdated, informal, internal, or contradicted. Filtering is done downstream and
depends on seeing everything.
"""


def build_user_prompt(spec: SectionSpec, pool: EvidencePool) -> str:
    """Render the extraction prompt for one section."""
    parts = [
        f"SOW SECTION {spec.section_id}: {spec.title}",
        f"Template guidance: {spec.guidance}",
        "",
        "REQUIRED ELEMENTS (copy these strings exactly into supports_elements):",
    ]
    parts.extend(f"  - {element}" for element in spec.required_elements)
    parts.append("")
    parts.append("PASSAGES:")

    for scored in pool.selected:
        chunk = scored.chunk
        header = f"[{chunk.chunk_id}]"
        if chunk.speaker:
            header += f" speaker: {chunk.speaker}"
        if chunk.heading_path:
            header += f" section: {chunk.heading_path}"
        parts.append("")
        parts.append(header)
        parts.append(chunk.text)

    return "\n".join(parts)


def extract_claims(
    spec: SectionSpec, pool: EvidencePool, llm: LlmClient
) -> tuple[list[Claim], list[Claim], str, str]:
    """Extract and verify claims for one section.

    Returns:
        (verified, rejected, system_prompt, user_prompt)
    """
    system = SYSTEM_PROMPT
    user = build_user_prompt(spec, pool)
    extraction = llm.parse(STAGE, system, user, ClaimExtraction)
    verified, rejected = verify_claims(extraction, pool)
    return verified, rejected, system, user


def verify_claims(
    extraction: ClaimExtraction, pool: EvidencePool
) -> tuple[list[Claim], list[Claim]]:
    """Check every extracted claim against the passage it cites.

    Two deterministic gates, no model involved:

    * the cited chunk must be in this section's pool;
    * the quote must be an exact substring of that chunk's text.

    Returns ``(verified, rejected)``. Rejected claims keep their reason so the
    trace and the run summary can report exactly what failed.
    """
    by_id: dict[str, Chunk] = {sc.chunk.chunk_id: sc.chunk for sc in pool.selected}
    verified: list[Claim] = []
    rejected: list[Claim] = []

    for index, raw in enumerate(extraction.claims, start=1):
        claim_id = f"s{pool.section_id}-c{index:03d}"
        chunk = by_id.get(raw.chunk_id)

        if chunk is None:
            rejected.append(
                _claim(
                    claim_id,
                    raw,
                    doc_id=raw.chunk_id.split("#")[0],
                    verified=False,
                    reason=(
                        f"cites {raw.chunk_id}, which is not in this section's evidence pool"
                    ),
                )
            )
            continue

        if raw.quote not in chunk.text:
            rejected.append(
                _claim(
                    claim_id,
                    raw,
                    doc_id=chunk.doc_id,
                    verified=False,
                    reason=_mismatch_reason(raw.quote, chunk.text),
                )
            )
            continue

        verified.append(_claim(claim_id, raw, doc_id=chunk.doc_id, verified=True, reason=None))

    return verified, rejected


def _mismatch_reason(quote: str, text: str) -> str:
    """Explain why a quote failed verification, distinguishing near misses.

    A quote that matches only after whitespace and unicode normalisation was
    reproduced rather than copied. It is still rejected -- the requirement is a
    verbatim span -- but saying so is more useful than "not found".
    """
    if _loose(quote) in _loose(text):
        return (
            "quote is not a verbatim substring of the cited passage; it matches only "
            "after whitespace/unicode normalisation, so it was reproduced, not copied"
        )
    return "quote is not a substring of the cited passage"


def _loose(text: str) -> str:
    """Whitespace- and unicode-normalised form, used only to classify failures."""
    folded = unicodedata.normalize("NFKD", text)
    folded = folded.replace("—", "-").replace("–", "-")
    folded = folded.replace("‘", "'").replace("’", "'")
    folded = folded.replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", folded).strip().lower()


def _claim(claim_id: str, raw, doc_id: str, verified: bool, reason: str | None) -> Claim:
    """Build a Claim record from the model's raw output."""
    from .analysis import normalise_value

    return Claim(
        claim_id=claim_id,
        fact_key=raw.fact_key.strip().lower(),
        value=raw.value.strip(),
        value_norm=normalise_value(raw.value),
        chunk_id=raw.chunk_id,
        doc_id=doc_id,
        quote=raw.quote,
        supports_elements=list(raw.supports_elements),
        verified=verified,
        reject_reason=reason,
    )
