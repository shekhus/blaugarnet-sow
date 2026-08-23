"""Assembly -- compose the final markdown, and check consistency across sections.

Everything that discloses a problem is written here, from ``Finding`` records,
not by the model. A conflict block is a rendering of the positions the authority
policy declined to choose between; a gap notice is a rendering of a required
element with no source. The model cannot omit either, because it never wrote
them.

The cross-section check compares facts that appear in more than one section. It
gates silent resolution, never the artifact: where two sections landed on
different values for one fact, both are disclosed and both sections are marked
contested, and the draft is still written. A corpus containing something
genuinely unresolvable -- as this one does -- must still produce a document.
"""

from __future__ import annotations

from collections import defaultdict

from .authority import resolve
from .models import (
    CrossSectionIssue,
    DocProvenance,
    DraftRun,
    Finding,
    OpenQuestion,
    Position,
    SectionAnalysis,
    SectionDraft,
    SectionStatus,
)

DISCLOSED_KINDS = {
    "conflict",
    "insufficient",
    "internal_only_support",
    "superseded_only_support",
    "provisional",
}


def section_status(analysis: SectionAnalysis, unsupported: bool) -> SectionStatus:
    """Map analysis outcome plus validation result onto a section status."""
    if unsupported:
        return "unsupported"
    has_conflict = any(f.kind == "conflict" for f in analysis.findings)
    if has_conflict and analysis.missing_elements:
        return "conflict_and_insufficient"
    if has_conflict:
        return "conflict"
    if analysis.missing_elements:
        return "insufficient"
    return "drafted"


def build_open_questions(drafts: list[SectionDraft]) -> list[OpenQuestion]:
    """Number every disclosed finding across the document, for section 10."""
    questions: list[OpenQuestion] = []
    for draft in sorted(drafts, key=lambda d: d.section_id):
        for finding in draft.findings:
            if finding.kind not in DISCLOSED_KINDS:
                continue
            ref = f"OQ-{len(questions) + 1}"
            subject = finding.fact_key or finding.required_element or ""
            questions.append(
                OpenQuestion(
                    ref=ref,
                    section_id=draft.section_id,
                    kind=finding.kind,
                    detail=f"{subject}: {finding.detail}" if subject else finding.detail,
                    positions=finding.positions,
                )
            )
            draft.open_item_ids.append(ref)
    return questions


def cross_section_check(
    analyses: list[SectionAnalysis], provs: dict[str, DocProvenance]
) -> list[CrossSectionIssue]:
    """Find facts that two sections settled differently.

    Per-section review cannot catch this: the go-live date is drafted in the
    timeline, the milestones and the payment triggers, and approving each in
    isolation lets an inconsistency through that no single review sees.
    """
    values_by_key: dict[str, dict[str, set[int]]] = defaultdict(lambda: defaultdict(set))
    for analysis in analyses:
        by_key: dict[str, list] = defaultdict(list)
        for claim in analysis.claims:
            by_key[claim.fact_key].append(claim)
        for fact_key, members in by_key.items():
            resolution = resolve(fact_key, members, provs)
            # Compare what each section actually settled on, not every phrasing
            # its claims used. Two sections that resolved a fact identically but
            # quoted it differently -- "UAT: 2026-11-30 - 2026-12-11" against the
            # same window with the regression period appended -- are not in
            # conflict, and reporting them as such buries the real divergences.
            # A key the section left contested is already disclosed there; it
            # does not need to be counted again as a cross-section issue.
            if resolution.resolved and resolution.winner is not None:
                values_by_key[fact_key][resolution.winner.value_norm].add(analysis.section_id)

    issues: list[CrossSectionIssue] = []
    for fact_key, by_value in sorted(values_by_key.items()):
        sections_using = {s for sections in by_value.values() for s in sections}
        if len(by_value) < 2 or len(sections_using) < 2:
            continue
        # Only a divergence: one section using a value another section does not.
        if all(sections_using == sections for sections in by_value.values()):
            continue
        issues.append(
            CrossSectionIssue(
                fact_key=fact_key,
                section_ids=sorted(sections_using),
                values=sorted(by_value),
                detail=(
                    f"'{fact_key}' appears in sections "
                    f"{', '.join(str(s) for s in sorted(sections_using))} with "
                    f"{len(by_value)} different values; disclosed rather than reconciled"
                ),
            )
        )
    return issues


# --------------------------------------------------------------------------- #
# Markdown rendering
# --------------------------------------------------------------------------- #

_BANNER = {
    "conflict": "SECTION STATUS: CONFLICT",
    "insufficient": "SECTION STATUS: INSUFFICIENT",
    "conflict_and_insufficient": "SECTION STATUS: CONFLICT AND INSUFFICIENT",
    "unsupported": "SECTION STATUS: UNSUPPORTED",
}


def render_document(run: DraftRun, target: str) -> str:
    """Render the whole SOW draft as markdown."""
    out: list[str] = [
        f"# Statement of Work — {target.title()} (DRAFT)",
        "",
        "> Machine-drafted from the source corpus. Every substantive statement carries a",
        "> citation resolving to a document, line range and verbatim quote. Sections whose",
        "> sources disagree, or whose required elements have no source, are marked and",
        "> rendered with the disagreement or the gap visible. Nothing was resolved silently.",
        "",
    ]

    if run.cross_section_issues:
        out += [
            "> **CROSS-SECTION INCONSISTENCY.** One or more facts were settled differently",
            "> in different sections. They are listed in section 10 and marked where they",
            "> occur. The draft is issued regardless; reconcile before use.",
            "",
        ]

    for draft in sorted(run.sections, key=lambda d: d.section_id):
        out.extend(render_section(draft))

    out.extend(_render_open_questions(run))
    return "\n".join(out).rstrip() + "\n"


def render_section(draft: SectionDraft) -> list[str]:
    """Render one section: banner, prose, disclosures, citation table."""
    out: list[str] = [f"## {draft.section_id}. {draft.title}", ""]

    banner = _BANNER.get(draft.status)
    if banner:
        counts = []
        conflicts = [f for f in draft.findings if f.kind == "conflict"]
        if conflicts:
            counts.append(f"{len(conflicts)} unresolved")
        if draft.missing_elements:
            counts.append(f"{len(draft.missing_elements)} insufficient")
        suffix = f" — {' · '.join(counts)}" if counts else ""
        out += [f"> **{banner}{suffix}**"]
        if draft.open_item_ids:
            out.append(f"> See section 10: {', '.join(draft.open_item_ids)}.")
        out.append("")

    if draft.body_markdown.strip():
        out += [draft.body_markdown.strip(), ""]

    for finding in draft.findings:
        if finding.kind == "conflict":
            out.extend(_render_conflict(finding))
        elif finding.kind == "insufficient":
            out.extend(_render_gap(finding))
        elif finding.kind in ("provisional", "internal_only_support", "superseded_only_support"):
            out += [f"> **NOTE — {finding.fact_key or ''}.** {finding.detail}", ""]

    if draft.issues:
        out += ["> **VALIDATION FAILED — this section is unsupported.**"]
        for issue in draft.issues:
            out.append(f"> - [{issue.gate}] {issue.detail}")
        out.append("")

    if draft.review.decision == "rejected_unsatisfiable":
        out += [
            "> **REVIEWER REJECTION NOT SATISFIABLE.**",
            f"> Comment: {draft.review.comment!r}",
            f"> Reason: {draft.review.unsatisfiable_reason}",
            "> The section is issued at its last valid revision.",
            "",
        ]

    if draft.citations:
        out += ["| Ref | Source | Lines | Quote |", "|---|---|---|---|"]
        for citation in draft.citations:
            lines = (
                str(citation.line_start)
                if citation.line_start == citation.line_end
                else f"{citation.line_start}-{citation.line_end}"
            )
            quote = citation.quote.replace("|", "\\|").replace("\n", " ")
            out.append(f"| {citation.marker} | `{citation.doc_id}` | {lines} | *{quote}* |")
        out.append("")

    return out


def _render_conflict(finding: Finding) -> list[str]:
    """Render an unresolved disagreement with every position and its provenance."""
    out = [
        f"> **UNRESOLVED — {finding.fact_key}.** {finding.detail}",
        "",
    ]
    for index, position in enumerate(finding.positions, start=1):
        label = chr(ord("A") + index - 1)
        qualifier = (
            " — supported only by internal documents, not agreed with the client"
            if position.internal_only
            else ""
        )
        out.append(f"**Position {label}{qualifier}.** {position.value}")
        out.append(
            f"Sources: {', '.join(f'`{d}`' for d in position.doc_ids)} "
            f"({'/'.join(position.instruments)}; {'/'.join(position.audiences)})."
        )
        out.append("")
    out.append(
        "Blaugarnet has not selected between these. Selecting either would assert an "
        "agreement the evidence does not establish."
    )
    out.append("")
    return out


def _render_gap(finding: Finding) -> list[str]:
    """Render a required element that no admitted source supports."""
    return [
        f"> **INSUFFICIENT — {finding.required_element}.** {finding.detail} "
        f"Not drafted; no value has been invented for it.",
        "",
    ]


def _render_open_questions(run: DraftRun) -> list[str]:
    """Render the document-wide rollup appended to section 10."""
    if not run.open_questions and not run.cross_section_issues:
        return []

    out = ["", "---", "", "## Open questions and disclosures (rollup)", ""]
    if run.open_questions:
        out += ["| Ref | Section | Kind | Detail |", "|---|---|---|---|"]
        for question in run.open_questions:
            detail = question.detail.replace("|", "\\|")
            out.append(
                f"| {question.ref} | §{question.section_id} | {question.kind} | {detail} |"
            )
        out.append("")

    if run.cross_section_issues:
        out += ["### Cross-section inconsistencies", ""]
        for issue in run.cross_section_issues:
            out.append(
                f"- **{issue.fact_key}** — sections "
                f"{', '.join(f'§{s}' for s in issue.section_ids)}; values: "
                + "; ".join(f"*{v}*" for v in issue.values)
            )
        out.append("")
    return out


def position_summary(position: Position) -> str:
    """One-line description of a position, for logs and the trace."""
    return f"{position.value} <- {', '.join(position.doc_ids)}"
