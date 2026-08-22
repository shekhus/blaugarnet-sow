"""Human-readable rendering of the corpus partition.

Printed on every run so the reviewer sees the engagement boundary before reading
a single drafted word.
"""

from __future__ import annotations

from .models import EvidencePool, Partition, SectionSpec
from .pipeline import RunContext

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


def _one_line(text: str, width: int) -> str:
    """Collapse a chunk to a single line for tabular display."""
    flat = " ".join(text.split())
    return flat if len(flat) <= width else flat[: width - 1] + "…"


def render_sections(sections: list[SectionSpec]) -> str:
    """Render the parsed template: sections and their required elements."""
    lines: list[str] = ["", "SOW TEMPLATE -- parsed sections and required elements", _RULE]
    for spec in sections:
        lines.append(f"section {spec.section_id:>2}. {spec.title}")
        if spec.subsections:
            lines.append(f"        subsections: {', '.join(spec.subsections)}")
        lines.append(f"        guidance:    {spec.guidance or '(none)'}")
        for element in spec.required_elements:
            lines.append(f"          required: {element}")
        lines.append("")
    lines.append(_RULE)
    total = sum(len(s.required_elements) for s in sections)
    lines.append(f"{len(sections)} sections  {total} required elements")
    lines.append("")
    return "\n".join(lines)


def render_pool(pool: EvidencePool, ctx: RunContext, show_text: bool = True) -> str:
    """Render one section's evidence pool with selectors, scores and provenance."""
    lines: list[str] = []
    add = lines.append
    spec = ctx.section(pool.section_id)

    add("")
    add(f"EVIDENCE POOL -- section {pool.section_id}. {pool.title}")
    add(_RULE)
    add(f"required elements : {' | '.join(spec.required_elements)}")
    add(f"retrieval query   : {_one_line(pool.query, 150)}")
    add(
        f"candidate chunks  : {pool.candidate_chunks} admitted"
        f"    ({pool.excluded_chunks} chunks from {len(pool.excluded_docs)} "
        f"excluded documents were never candidates)"
    )
    add(f"selected          : {len(pool.selected)}")
    add(_RULE)
    add(
        f"{'SEL':<10} {'SCORE':>7}  {'AUDIENCE':<14} {'STATUS':<18} CHUNK"
    )
    add(_RULE)

    for scored in pool.selected:
        chunk = scored.chunk
        prov = ctx.partition.provenance[chunk.doc_id]
        selector = f"bm25 #{scored.rank}" if scored.selector == "retrieved" else scored.selector
        score = f"{scored.score:7.3f}" if scored.selector == "retrieved" else "-"
        add(f"{selector:<10} {score:>7}  {prov.audience:<14} {prov.status:<18} {chunk.chunk_id}")
        if show_text:
            flag = (
                f"  [names other engagement: {', '.join(chunk.foreign_mentions)}]"
                if chunk.foreign_mentions
                else ""
            )
            add(f"{'':<10} {'':>7}  {_one_line(chunk.text, 96)}{flag}")

    add(_RULE)
    add("")
    return "\n".join(lines)
