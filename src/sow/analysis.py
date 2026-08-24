"""Stage 10 -- detect conflict and insufficiency. No model is involved.

Both detections are structural:

* **Conflict** is value disagreement on a shared fact key. Claims are grouped by
  key, normalised, and compared; where more than one value survives, the
  authority policy is asked for a winner and frequently declines. Nothing here
  knows which facts are contested in this corpus -- the disagreement is found by
  comparison, so a disagreement nobody anticipated is found the same way.

* **Insufficiency** is a required element with no verified claim behind it. The
  element list comes from the template's own guidance prose, so the check is
  driven by what the document must contain rather than by a list of things
  somebody thought to look for.

Coverage is the one place the model used to be believed. It reports which
elements each claim supports, and that report was taken at face value -- which
made "is this requirement met?" a model judgement in a pipeline that keeps every
other judgement in code. It failed exactly where it mattered: section 12 asks for
the acceptance authority "by whom", the model offered the sales playbook rule
*"Every SOW names the client-side acceptance authority"*, and coverage accepted a
policy demanding a name as though it supplied one.

So a coverage report is now a proposal that code verifies. For elements asking
*who*, the verification is structural: only a document about this engagement can
name this engagement's people, and the claim's value must actually contain a
name. See ``_coverage``.
"""

from __future__ import annotations

import re

from .authority import is_provisional, resolve
from .models import (
    AnalysisStatus,
    Claim,
    DocProvenance,
    EvidencePool,
    Finding,
    SectionAnalysis,
    SectionSpec,
)

# Hedges that should not make two statements of the same value look different.
_HEDGES = re.compile(
    r"\b(approximately|approx|about|roughly|around|circa|c\.|~|at least|no later than|"
    r"target|targeted|proposed|working)\b",
    re.IGNORECASE,
)
_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}
_LONG_DATE = re.compile(
    r"\b(" + "|".join(_MONTHS) + r")\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b",
    re.IGNORECASE,
)
_DAY_FIRST = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(" + "|".join(_MONTHS) + r")\s+(\d{4})\b",
    re.IGNORECASE,
)

# Required elements that ask *who* rather than *what*. Derived from the
# template's own wording, so a template that stops asking for a party stops
# triggering this: "by whom", "who approves change requests", "named client
# counterparts".
_PARTY_ELEMENT = re.compile(
    r"\b(whom|who|authority|signator(?:y|ies)|counterparts?|approver)\b",
    re.IGNORECASE,
)

# Values that record the absence of an answer rather than an answer. A source
# that says the authority is "TBD" is not a source that names one.
_PLACEHOLDER_VALUE = re.compile(
    r"^(tbd|tba|n/?a|none|unknown|open|pending|"
    r"to be (confirmed|determined|decided|agreed|named)|"
    r"not (yet )?(confirmed|determined|decided|agreed|named|defined))\b",
    re.IGNORECASE,
)


def normalise_value(value: str) -> str:
    """Canonical form used only for equality comparison.

    Deliberately conservative. Over-normalising merges values that genuinely
    differ; under-normalising invents conflicts out of phrasing. Dates are
    unified because the same date is written three ways across this corpus, and
    thousands separators are dropped because "2,400" and "2400" are one number.
    """
    text = value.strip().lower()
    text = _LONG_DATE.sub(lambda m: _iso(m.group(3), _MONTHS[m.group(1).lower()], m.group(2)), text)
    text = _DAY_FIRST.sub(lambda m: _iso(m.group(3), _MONTHS[m.group(2).lower()], m.group(1)), text)
    text = _HEDGES.sub(" ", text)
    text = re.sub(r"(\d),(\d{3})\b", r"\1\2", text)
    text = re.sub(r"[^\w\s./-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" .,-")
    return text


def _iso(year: str, month: int, day: str) -> str:
    """Format a parsed date as YYYY-MM-DD."""
    return f"{int(year):04d}-{month:02d}-{int(day):02d}"


def analyse_section(
    spec: SectionSpec,
    pool: EvidencePool,
    claims: list[Claim],
    rejected: list[Claim],
    provs: dict[str, DocProvenance],
) -> SectionAnalysis:
    """Group claims, compare values, and check element coverage."""
    findings: list[Finding] = []

    for claim in rejected:
        findings.append(
            Finding(
                kind="unverified_claim",
                detail=f"claim discarded: {claim.reject_reason}",
                fact_key=claim.fact_key,
                claim_ids=[claim.claim_id],
            )
        )

    by_key: dict[str, list[Claim]] = {}
    for claim in claims:
        by_key.setdefault(claim.fact_key, []).append(claim)

    for fact_key in sorted(by_key):
        resolution = resolve(fact_key, by_key[fact_key], provs)

        if not resolution.resolved and resolution.contested:
            findings.append(
                Finding(
                    kind="conflict",
                    detail=resolution.reason,
                    fact_key=fact_key,
                    claim_ids=[cid for p in resolution.positions for cid in p.claim_ids],
                    positions=resolution.positions,
                )
            )
            continue

        if not resolution.resolved:
            findings.append(
                Finding(
                    kind="superseded_only_support",
                    detail=resolution.reason,
                    fact_key=fact_key,
                    claim_ids=[cid for p in resolution.positions for cid in p.claim_ids],
                    positions=resolution.positions,
                )
            )
            continue

        winner = resolution.winner
        assert winner is not None
        if winner.internal_only:
            findings.append(
                Finding(
                    kind="internal_only_support",
                    detail=(
                        "supported only by internal documents; may inform the section "
                        "but cannot be asserted to the client on its own"
                    ),
                    fact_key=fact_key,
                    claim_ids=winner.claim_ids,
                    positions=[winner],
                )
            )
        elif is_provisional(winner, provs):
            findings.append(
                Finding(
                    kind="provisional",
                    detail="rests only on an instrument that is out for signature, not executed",
                    fact_key=fact_key,
                    claim_ids=winner.claim_ids,
                    positions=[winner],
                )
            )

    covered, missing, reasons = _coverage(spec, claims, provs)
    for element in missing:
        findings.append(
            Finding(
                kind="insufficient",
                detail=f"the template requires '{element}' {reasons[element]}",
                required_element=element,
            )
        )

    has_conflict = any(f.kind == "conflict" for f in findings)
    status: AnalysisStatus = (
        "conflict_and_insufficient"
        if has_conflict and missing
        else "conflict"
        if has_conflict
        else "insufficient"
        if missing
        else "clean"
    )

    return SectionAnalysis(
        section_id=spec.section_id,
        title=spec.title,
        status=status,
        claims=claims,
        rejected=rejected,
        findings=findings,
        covered_elements=covered,
        missing_elements=missing,
        pool_size=len(pool.selected),
    )


def supplies_a_party(claim: Claim, provs: dict[str, DocProvenance]) -> bool:
    """True when this claim could name a party for *this* engagement.

    Two structural conditions, neither of which needs to understand the sentence.

    The document must be about the engagement rather than company-wide. A policy
    that applies to every SOW cannot know who signs this one off; it is the source
    of the requirement, not of an answer. This is what the section 12 gap turned
    on -- the only support for "by whom" was the playbook rule demanding a name.

    And the value must not be a recorded absence. "TBD" is a source telling you
    it has no answer.
    """
    prov = provs.get(claim.doc_id)
    if prov is None or prov.engagement == "company":
        return False
    return not _PLACEHOLDER_VALUE.match(claim.value.strip())


def _coverage(
    spec: SectionSpec, claims: list[Claim], provs: dict[str, DocProvenance]
) -> tuple[list[str], list[str], dict[str, str]]:
    """Split required elements into covered and missing, and say why for missing.

    The model proposes which elements each claim supports; this verifies the
    proposal rather than accepting it. An element asking for a party is covered
    only when some claim actually supplies one -- see ``_supplies_a_party``. For
    every other element the model's report still stands, which is a narrower
    trust than before but not yet none: see the README's known weaknesses.
    """
    proposed: dict[str, list[Claim]] = {}
    for claim in claims:
        for element in claim.supports_elements:
            proposed.setdefault(element.strip().lower(), []).append(claim)

    covered: list[str] = []
    missing: list[str] = []
    reasons: dict[str, str] = {}

    for element in spec.required_elements:
        backing = proposed.get(element.strip().lower(), [])

        if not backing:
            missing.append(element)
            reasons[element] = "and no admitted source supports it"
            continue

        if _PARTY_ELEMENT.search(element) and not any(
            supplies_a_party(claim, provs) for claim in backing
        ):
            missing.append(element)
            reasons[element] = (
                "which asks for a party; the only support is company-wide policy "
                "requiring that such a party be named, or a source recording that "
                "none has been named yet"
            )
            continue

        covered.append(element)

    return covered, missing, reasons
