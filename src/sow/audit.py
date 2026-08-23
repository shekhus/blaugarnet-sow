"""Quality audit of a produced draft, re-derived from the corpus.

This is the automated quality check. It deliberately trusts nothing the run
recorded about itself: it re-reads ``data/``, re-chunks it, and re-verifies every
citation in the finished markdown against the source lines. A run that lied to
its own trace would still fail here.

Six checks, in descending order of how badly a failure would matter:

1. **citation_resolves**   every citation names a document that exists.
2. **citation_in_scope**   every cited document is admitted for this engagement.
                           This is the cross-engagement guarantee: another
                           client's blended rate cannot appear under a citation.
3. **quote_verbatim**      every quoted span is still a character-for-character
                           substring of the lines it points at.
4. **no_foreign_entity**   no proper noun unique to an excluded document appears.
5. **sections_complete**   every template section is present in the document.
6. **findings_disclosed**  every conflict and gap recorded in the run appears in
                           the rendered text.

Groundedness is checked as provenance, not as plausibility. Whether a sentence
is *entailed* by its quote is not decidable by string matching, and asking a
model to score it would make the check as fallible as the thing it audits.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .models import DraftRun
from .pipeline import RunContext

# "| C1 | `docs/harding_msa_summary.md` | 6 | *quoted text* |"
_CITATION_ROW = re.compile(
    r"^\|\s*(C\d+)\s*\|\s*`([^`]+)`\s*\|\s*([\d-]+)\s*\|\s*\*(.*?)\*\s*\|\s*$", re.M
)
_SECTION_HEAD = re.compile(r"^## (\d+)\.\s", re.M)


@dataclass
class AuditResult:
    """Outcome of auditing one rendered document."""

    checks: dict[str, bool] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)
    citation_count: int = 0
    section_count: int = 0

    @property
    def passed(self) -> bool:
        return all(self.checks.values())

    def render(self) -> str:
        """Human-readable audit report."""
        rule = "-" * 100
        lines = ["", "DRAFT AUDIT", rule]
        for name, ok in self.checks.items():
            lines.append(f"  {'PASS' if ok else 'FAIL'}  {name}")
        lines.append(rule)
        lines.append(f"  {self.citation_count} citations across {self.section_count} sections")
        if self.failures:
            lines.append("")
            lines.append(f"  {len(self.failures)} failure(s):")
            lines.extend(f"    - {f}" for f in self.failures)
        lines.append(rule)
        lines.append(f"  RESULT: {'PASS' if self.passed else 'FAIL'}")
        lines.append("")
        return "\n".join(lines)


def audit_document(document: str, ctx: RunContext, run: DraftRun | None = None) -> AuditResult:
    """Audit a rendered SOW draft against the corpus it claims to come from."""
    result = AuditResult()
    docs_by_id = {d.doc_id: d for d in ctx.documents}
    admitted = {d.doc_id for d in ctx.partition.admitted}
    excluded = {d.doc_id for d in ctx.partition.excluded}

    rows = _CITATION_ROW.findall(document)
    result.citation_count = len(rows)
    result.section_count = len(set(_SECTION_HEAD.findall(document)))

    resolves, in_scope, verbatim = [], [], []
    for marker, doc_id, line_range, quote in rows:
        if doc_id not in docs_by_id:
            resolves.append(f"[{marker}] names {doc_id}, which is not in the corpus")
            continue
        if doc_id not in admitted:
            in_scope.append(
                f"[{marker}] cites {doc_id}, excluded from this engagement"
            )
            continue
        if not _quote_matches(docs_by_id[doc_id].lines, line_range, quote):
            verbatim.append(
                f"[{marker}] quote is not a verbatim substring of {doc_id}:{line_range}"
            )

    foreign = [
        term for term in ctx.tripwire_terms if re.search(rf"\b{re.escape(term)}\b", document)
    ]
    named_excluded = sorted(d for d in excluded if d in document)
    expected_sections = {s.section_id for s in ctx.sections}
    present_sections = {int(n) for n in _SECTION_HEAD.findall(document)}
    missing_sections = sorted(expected_sections - present_sections)

    undisclosed: list[str] = []
    if run is not None:
        for draft in run.sections:
            for finding in draft.findings:
                if finding.kind == "conflict" and finding.fact_key:
                    if finding.fact_key not in document:
                        undisclosed.append(
                            f"section {draft.section_id}: conflict on "
                            f"'{finding.fact_key}' is not disclosed in the document"
                        )
                elif finding.kind == "insufficient" and finding.required_element:
                    if finding.required_element not in document:
                        undisclosed.append(
                            f"section {draft.section_id}: gap '{finding.required_element}' "
                            f"is not disclosed in the document"
                        )

    result.checks = {
        "citation_resolves": not resolves,
        "citation_in_scope": not in_scope and not named_excluded,
        "quote_verbatim": not verbatim,
        "no_foreign_entity": not foreign,
        "sections_complete": not missing_sections,
        "findings_disclosed": not undisclosed,
    }
    result.failures = (
        resolves
        + in_scope
        + [f"document names excluded source {d}" for d in named_excluded]
        + verbatim
        + [f"foreign entity '{t}' appears in the document" for t in foreign]
        + [f"template section {n} is missing from the document" for n in missing_sections]
        + undisclosed
    )
    return result


def _quote_matches(lines: tuple[str, ...], line_range: str, quote: str) -> bool:
    """Check a quote against the exact source lines the citation points at."""
    parts = line_range.split("-")
    try:
        start = int(parts[0])
        end = int(parts[-1])
    except ValueError:
        return False
    if start < 1 or end > len(lines) or start > end:
        return False
    span = "\n".join(lines[start - 1 : end])
    # The renderer escapes pipes and flattens newlines for the markdown table.
    return quote.replace("\\|", "|") in " ".join(span.split()) or quote.replace(
        "\\|", "|"
    ) in span


def audit_paths(draft_path: Path, ctx: RunContext, run_path: Path | None = None) -> AuditResult:
    """Audit a draft on disk."""
    run = None
    if run_path and run_path.is_file():
        run = DraftRun.model_validate_json(run_path.read_text(encoding="utf-8"))
    return audit_document(draft_path.read_text(encoding="utf-8"), ctx, run)
