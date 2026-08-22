"""Stage 3 -- decide which documents may enter the evidence pool.

This is the engagement boundary, and it is a hard filter rather than a ranking
signal. A similarity score can only make another client's document unlikely; a
boundary makes it impossible. Northgate's blended USD 105/hour cannot reach
Harding's commercials section because no chunk of that document is retrievable
or citable from any section.

The failure mode is exclusion. A document whose subject cannot be established
unambiguously is excluded and reported, never admitted on the benefit of the
doubt.
"""

from __future__ import annotations

from .config import Roster
from .models import AdmissionDecision, DocProvenance, Document, Partition
from .provenance import apply_supersession, build_provenance


def build_partition(docs: list[Document], roster: Roster) -> Partition:
    """Label every document and split the corpus into admitted and excluded."""
    provs: dict[str, DocProvenance] = {doc.doc_id: build_provenance(doc, roster) for doc in docs}

    warnings: list[str] = list(apply_supersession(docs, provs))

    decisions: list[AdmissionDecision] = []
    for doc in docs:
        prov = provs[doc.doc_id]
        admitted = prov.engagement in roster.admitted_labels
        reason = _admission_reason(prov, roster, admitted)
        decisions.append(
            AdmissionDecision(
                doc_id=doc.doc_id,
                engagement=prov.engagement,
                admitted=admitted,
                reason=reason,
            )
        )

        if prov.engagement == "AMBIGUOUS":
            warnings.append(f"{doc.doc_id}: AMBIGUOUS subject, excluded -- {reason}")
        if prov.instrument == "unknown":
            warnings.append(
                f"{doc.doc_id}: instrument could not be classified; treated as internal_only"
            )
        if prov.doc_date is None:
            warnings.append(f"{doc.doc_id}: no date found; recency comparisons will skip it")

    if not any(d.admitted for d in decisions):
        raise RuntimeError(
            "no documents admitted: the engagement roster excludes the entire corpus"
        )

    return Partition(
        target=roster.target,
        decisions=decisions,
        provenance=provs,
        warnings=warnings,
    )


def _admission_reason(prov: DocProvenance, roster: Roster, admitted: bool) -> str:
    """Human-readable justification for one admission decision."""
    ev = prov.evidence_for("engagement")
    detail = ev.reason if ev else "no engagement evidence recorded"

    if admitted:
        if prov.engagement == roster.target:
            return f"target engagement '{roster.target}' -- {detail}"
        return f"company-wide material -- {detail}"

    if prov.engagement == "AMBIGUOUS":
        return f"subject ambiguous -- {detail}"
    return f"belongs to another engagement '{prov.engagement}' -- {detail}"
