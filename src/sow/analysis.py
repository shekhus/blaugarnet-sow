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

    covered, missing = _coverage(spec, claims)
    for element in missing:
        findings.append(
            Finding(
                kind="insufficient",
                detail=(
                    f"the template requires '{element}' and no admitted source supports it"
                ),
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


def _coverage(spec: SectionSpec, claims: list[Claim]) -> tuple[list[str], list[str]]:
    """Split the template's required elements into covered and missing."""
    supported = {
        element.strip().lower()
        for claim in claims
        for element in claim.supports_elements
    }
    covered = [e for e in spec.required_elements if e.strip().lower() in supported]
    missing = [e for e in spec.required_elements if e.strip().lower() not in supported]
    return covered, missing
