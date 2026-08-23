"""Stage 11 -- draft one section's prose from its verified claims.

The model writes prose and nothing else. Status banners, conflict blocks, gap
notices and the citation table are rendered from ``Finding`` records by
``sow.assemble``. That split is deliberate: "every finding is surfaced" becomes
a structural property of the assembler rather than an instruction the model is
asked to follow, and a model that ignores an instruction cannot suppress a
disclosure.

The model is therefore given only the material it may assert -- claims whose
fact key the authority policy actually resolved -- and is told explicitly that
contested and missing facts are handled elsewhere and must not be guessed at.
"""

from __future__ import annotations

import re

from .authority import resolve
from .models import (
    Citation,
    Claim,
    DocProvenance,
    DraftedSection,
    EvidencePool,
    Finding,
    SectionSpec,
)

STAGE = "draft_section"

MARKER = re.compile(r"\[(C\d+)\]")

SYSTEM_PROMPT = """\
You draft one section of a client-facing Statement of Work from verified claims.

You are given claims that have already been checked against their sources, each
with a citation marker. You are also told which facts are contested and which
required elements have no source at all. Those are rendered elsewhere in the
document by the system. Your job is only the settled prose.

Rules:

1. Every sentence that asserts a fact must carry at least one citation marker in
   square brackets, exactly as given, for example [C3]. A sentence with no
   marker will be rejected by an automated check and the section redrafted.
2. Assert only what the claims state. Do not add background, do not infer
   consequences, do not smooth over a gap with a plausible sentence. If the
   claims do not cover something the section would normally say, leave it out
   and note it in drafting_notes.
3. Never state a value for a fact listed as contested. Do not pick one, do not
   average them, do not hint at a preference. The system renders both positions
   with their citations after your prose.
4. Never write a value for a required element listed as missing. The system
   renders that gap explicitly.
5. Do not invent citation markers. Use only the markers in the table given.
6. Write in the register of a professional services contract: plain, specific,
   present tense. No marketing language, no filler, no restating the brief.
7. Do not write a section heading. The system supplies it.

Output markdown prose. Short paragraphs, or a short list where the source
material is genuinely a list.
"""


def build_citations(
    claims: list[Claim], pool: EvidencePool, provs: dict[str, DocProvenance]
) -> tuple[list[Citation], dict[str, str]]:
    """Assign a stable marker to every distinct passage the claims rest on.

    Returns the citation table and a map from chunk id to marker.
    """
    chunks = {sc.chunk.chunk_id: sc.chunk for sc in pool.selected}
    citations: list[Citation] = []
    by_chunk: dict[str, str] = {}

    for claim in claims:
        if claim.chunk_id in by_chunk:
            continue
        chunk = chunks[claim.chunk_id]
        prov = provs[chunk.doc_id]
        marker = f"C{len(citations) + 1}"
        by_chunk[claim.chunk_id] = marker
        citations.append(
            Citation(
                marker=marker,
                chunk_id=chunk.chunk_id,
                doc_id=chunk.doc_id,
                quote=claim.quote,
                line_start=chunk.line_start,
                line_end=chunk.line_end,
                instrument=prov.instrument,
                audience=prov.audience,
                status=prov.status,
            )
        )
    return citations, by_chunk


def assertable_claims(
    claims: list[Claim], provs: dict[str, DocProvenance]
) -> tuple[list[Claim], set[str]]:
    """Split claims into those the section may assert and the contested fact keys.

    A fact key is assertable when the authority policy produced a winner and
    that winner is not supported only by internal deliberation. Everything else
    is left to the conflict and disclosure blocks.
    """
    by_key: dict[str, list[Claim]] = {}
    for claim in claims:
        by_key.setdefault(claim.fact_key, []).append(claim)

    allowed: list[Claim] = []
    contested: set[str] = set()

    for fact_key, members in by_key.items():
        resolution = resolve(fact_key, members, provs)
        if not resolution.resolved or resolution.winner is None:
            contested.add(fact_key)
            continue
        if resolution.winner.internal_only:
            contested.add(fact_key)
            continue
        winning = set(resolution.winner.claim_ids)
        allowed.extend(c for c in members if c.claim_id in winning)

    return allowed, contested


def build_user_prompt(
    spec: SectionSpec,
    claims: list[Claim],
    by_chunk: dict[str, str],
    contested: set[str],
    missing: list[str],
    findings: list[Finding],
) -> str:
    """Render the drafting prompt for one section."""
    parts = [
        f"SOW SECTION {spec.section_id}: {spec.title}",
        f"Template guidance: {spec.guidance}",
        "",
        "REQUIRED ELEMENTS:",
    ]
    for element in spec.required_elements:
        state = "NO SOURCE - do not write anything for this" if element in missing else "covered"
        parts.append(f"  - {element}  [{state}]")

    parts += ["", "VERIFIED CLAIMS YOU MAY ASSERT:"]
    if not claims:
        parts.append("  (none)")
    for claim in claims:
        marker = by_chunk[claim.chunk_id]
        parts.append(f"  [{marker}] {claim.fact_key}: {claim.value}")
        parts.append(f"        source quote: \"{claim.quote}\"")

    if contested:
        parts += ["", "CONTESTED - DO NOT STATE A VALUE FOR THESE:"]
        for fact_key in sorted(contested):
            detail = next(
                (f.detail for f in findings if f.kind == "conflict" and f.fact_key == fact_key),
                "sources disagree",
            )
            parts.append(f"  - {fact_key}: {detail}")
        parts.append(
            "  The system renders each of these below your prose, with both values and "
            "their citations. Do not mention, summarise or resolve them."
        )

    if missing:
        parts += ["", "MISSING - NO SOURCE EXISTS, DO NOT INVENT:"]
        parts.extend(f"  - {element}" for element in missing)
        parts.append("  The system renders these gaps explicitly. Leave them out of your prose.")

    parts += [
        "",
        "Draft the prose for the settled material only. Every factual sentence carries "
        "at least one marker from the table above.",
    ]
    return "\n".join(parts)


REDRAFT_SYSTEM_PROMPT = (
    SYSTEM_PROMPT
    + """
You are now redrafting after a human reviewer rejected the previous version.

The reviewer's comment is authoritative about what to change. It is NOT
authoritative about what the sources say. If honouring it would require
asserting something none of the claims support, do not write that sentence.
Instead leave the body as close to the previous version as the comment allows,
and set unsatisfiable_reason to a plain statement of what was asked for and
which claim would be needed to support it.

Refusing is the correct outcome in that case. A reviewer asking for a fact the
evidence does not contain is exactly the situation this system exists to catch,
and satisfying them by inventing the sentence would defeat it.
"""
)


def build_redraft_prompt(base_prompt: str, previous_body: str, comment: str) -> str:
    """Extend the original drafting prompt with the reviewer's verbatim comment."""
    return "\n\n".join(
        [
            base_prompt,
            "PREVIOUS DRAFT (rejected by the reviewer):",
            previous_body or "(the previous draft was empty)",
            "REVIEWER COMMENT, VERBATIM:",
            comment,
            "Redraft the section addressing that comment. Every rule above still applies: "
            "assert only what the claims support, cite every factual sentence, and do not "
            "state a value for anything listed as contested or missing. If the comment "
            "cannot be honoured within those rules, set unsatisfiable_reason and explain.",
        ]
    )


def markers_used(body: str) -> list[str]:
    """Citation markers referenced in a drafted body, in order of appearance."""
    seen: list[str] = []
    for match in MARKER.finditer(body):
        if match.group(1) not in seen:
            seen.append(match.group(1))
    return seen


def used_citations(draft: DraftedSection, citations: list[Citation]) -> list[Citation]:
    """Narrow the citation table to markers the prose actually used."""
    used = set(markers_used(draft.body_markdown))
    return [c for c in citations if c.marker in used]
