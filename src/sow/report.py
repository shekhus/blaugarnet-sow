"""Human-readable rendering of the corpus partition.

Printed on every run so the reviewer sees the engagement boundary before reading
a single drafted word.
"""

from __future__ import annotations

from .models import Partition

_RULE = "-" * 100


def render_partition(partition: Partition, verbose: bool = False) -> str:
    """Render the partition as a table with a per-document reason."""
    lines: list[str] = []
    add = lines.append

    add("")
    add(f"CORPUS PARTITION -- target engagement: {partition.target}")
    add(_RULE)
    add(f"{'':<6} {'ENGAGEMENT':<11} {'INSTRUMENT':<22} {'AUDIENCE':<14} {'STATUS':<18} DOCUMENT")
    add(_RULE)

    for decision in partition.decisions:
        prov = partition.provenance[decision.doc_id]
        add(
            f"{'PASS' if decision.admitted else 'BLOCK':<6} "
            f"{decision.engagement:<11} "
            f"{prov.instrument:<22} "
            f"{prov.audience:<14} "
            f"{prov.status:<18} "
            f"{decision.doc_id}"
        )
        if verbose:
            add(f"{'':<6} reason: {decision.reason}")
            date_ev = prov.evidence_for("doc_date")
            if date_ev and date_ev.source_line:
                add(f"{'':<6} dated:  {prov.doc_date} <- {date_ev.source_line.strip()}")

    add(_RULE)

    counts = partition.counts()
    add("by label:   " + "  ".join(f"{k} {v}" for k, v in counts.items()))
    add(
        f"admitted:   {len(partition.admitted)}"
        f"    excluded: {len(partition.excluded)}"
        f"    total: {len(partition.decisions)}"
    )

    excluded = partition.excluded
    if excluded:
        add("")
        add("EXCLUDED FROM EVIDENCE (cannot be retrieved or cited by any section):")
        for decision in excluded:
            add(f"  {decision.doc_id}")
            add(f"      {decision.reason}")

    if partition.warnings:
        add("")
        add(f"NOTES ({len(partition.warnings)}):")
        for warning in partition.warnings:
            add(f"  - {warning}")

    add("")
    return "\n".join(lines)
