"""Stage 12 -- deterministic gates on a drafted section.

No model is consulted. Each gate either passes or names exactly what failed, so
a redraft can be given the specific complaint rather than "try again".

The gates:

* **citation_resolves**  -- every marker in the prose exists in the section's
  citation table.
* **citation_in_scope**  -- every cited passage belongs to an admitted document.
  This is the structural guarantee against cross-engagement contamination:
  another client's blended rate cannot appear under a citation because no chunk
  of that document is citable from any section.
* **uncited_assertion**  -- every assertive line carries at least one marker.
* **foreign_entity**     -- advisory scan for proper nouns that occur only in
  excluded documents.
* **empty_body**         -- a section with claims produced no prose.

A failure sends the section back for a bounded number of redrafts. If it still
fails, the section is marked ``unsupported`` and written anyway with its issues
attached. Nothing is dropped silently.
"""

from __future__ import annotations

import re

from .draft import markers_used
from .models import Citation, DraftedSection, ValidationIssue

MAX_REVISIONS = 2

# Lines that assert nothing on their own and so need no citation.
_HEADING = re.compile(r"^\s*#{1,6}\s")
_QUOTE = re.compile(r"^\s*>")
_TABLE = re.compile(r"^\s*\|")
_RULE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
_BULLET_ONLY = re.compile(r"^\s*(?:[-*+]|\d+\.)\s*$")
_WORD = re.compile(r"[A-Za-z]{2,}")


def validate_section(
    draft: DraftedSection,
    citations: list[Citation],
    admitted_doc_ids: set[str],
    tripwire_terms: list[str],
    expect_prose: bool,
) -> list[ValidationIssue]:
    """Run every gate against one drafted section."""
    issues: list[ValidationIssue] = []
    body = draft.body_markdown
    table = {c.marker: c for c in citations}

    if expect_prose and not body.strip():
        issues.append(
            ValidationIssue(gate="empty_body", detail="section has claims but produced no prose")
        )

    for marker in markers_used(body):
        if marker not in table:
            issues.append(
                ValidationIssue(
                    gate="citation_resolves",
                    detail=f"marker [{marker}] does not exist in this section's citation table",
                )
            )

    for citation in citations:
        if citation.doc_id not in admitted_doc_ids:
            issues.append(
                ValidationIssue(
                    gate="citation_in_scope",
                    detail=(
                        f"[{citation.marker}] cites {citation.doc_id}, which is not an "
                        f"admitted document for this engagement"
                    ),
                )
            )

    issues.extend(_uncited_assertions(body))
    issues.extend(_foreign_entities(body, tripwire_terms))
    return issues


def _uncited_assertions(body: str) -> list[ValidationIssue]:
    """Find assertive lines with no citation marker.

    Headings, blockquotes, tables, rules and bare list bullets assert nothing on
    their own. Everything else that contains words is treated as an assertion
    and must carry a marker.
    """
    issues: list[ValidationIssue] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue
        if (
            _HEADING.match(raw)
            or _QUOTE.match(raw)
            or _TABLE.match(raw)
            or _RULE.match(raw)
            or _BULLET_ONLY.match(raw)
        ):
            continue
        if not _WORD.search(line):
            continue
        if not markers_used(line):
            issues.append(
                ValidationIssue(
                    gate="uncited_assertion",
                    detail="assertive line carries no citation marker",
                    excerpt=line[:160],
                )
            )
    return issues


def _foreign_entities(body: str, tripwire_terms: list[str]) -> list[ValidationIssue]:
    """Advisory scan for entities that exist only in excluded documents.

    Secondary to ``citation_in_scope``, which is exact. This catches an
    unattributed mention rather than a wrong citation, and cannot catch a value
    that also appears in an admitted document -- "105" being the example this
    corpus is built around.
    """
    issues: list[ValidationIssue] = []
    for term in tripwire_terms:
        if re.search(rf"\b{re.escape(term)}\b", body):
            issues.append(
                ValidationIssue(
                    gate="foreign_entity",
                    detail=(
                        f"'{term}' appears only in documents excluded from this engagement"
                    ),
                    excerpt=term,
                )
            )
    return issues


def redraft_instruction(issues: list[ValidationIssue]) -> str:
    """Turn gate failures into a specific complaint for the next attempt."""
    lines = ["The previous draft failed automated validation. Fix exactly these problems:"]
    for issue in issues:
        lines.append(f"  - [{issue.gate}] {issue.detail}")
        if issue.excerpt:
            lines.append(f"      offending text: {issue.excerpt!r}")
    lines.append(
        "Do not add new facts while fixing these. If a sentence cannot be supported by a "
        "claim in the table, delete it rather than finding a marker to attach."
    )
    return "\n".join(lines)
