"""Stage 13 -- the human review loop.

A reviewer approves or rejects each section with a comment, and a rejection
redrafts the section from that comment. Two things matter beyond the mechanics.

**Nothing disappears.** Every terminal state still emits the section. An
approved section is emitted; a rejected one that could not be satisfied is
emitted at its last valid revision, carrying the reviewer's verbatim comment and
the reason it could not be honoured; a section never reached is emitted as
pending. A review pass that removes content from the document would be a worse
outcome than one that ships a marked-up section.

**A comment can be refused.** A reviewer may ask for something the sources do
not support. The redraft is told, explicitly, that the comment is authoritative
about what to change but not about what the evidence says, and that naming the
obstacle beats inventing a sentence. That path ends in
``rejected_unsatisfiable`` -- a real terminal state, not a failure.

Retries are capped so a rejection cannot spend unbounded tokens. Exhausting the
cap is itself an unsatisfiable outcome, recorded with the validation failures
that caused it.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

from .draft import REDRAFT_SYSTEM_PROMPT, STAGE, build_redraft_prompt, used_citations
from .llm import LlmClient
from .models import (
    Citation,
    DraftedSection,
    ReviewRecord,
    SectionDraft,
    ValidationIssue,
)
from .trace import Trace
from .validate import redraft_instruction, validate_section

MAX_REDRAFT_ATTEMPTS = 2

# How many times one section may be rejected before it is closed as
# unsatisfiable. Bounds token spend on a section the evidence will never satisfy.
MAX_REJECT_CYCLES = 3

_HELP = """\
  a  approve this section
  r  reject and give a comment (the section is redrafted from it)
  s  skip -- leave pending, section still appears in the document
  v  view the full section text again
  q  quit review (remaining sections stay pending)
  ?  this help"""


class QuitReview(Exception):
    """Raised when the reviewer ends the pass early."""


@dataclass
class ReviewContext:
    """Everything the loop needs to redraft and revalidate a section."""

    llm: LlmClient
    trace: Trace
    admitted_doc_ids: set[str]
    tripwire_terms: list[str]
    max_attempts: int = MAX_REDRAFT_ATTEMPTS
    max_cycles: int = MAX_REJECT_CYCLES


def review_sections(
    drafts: list[SectionDraft],
    ctx: ReviewContext,
    section_ids: list[int] | None = None,
    scripted: dict[int, tuple[str, str | None]] | None = None,
) -> list[SectionDraft]:
    """Walk the sections, collecting decisions.

    Args:
        scripted: non-interactive decisions keyed by section id, as
            ``{section_id: (action, comment)}``. Used by the tests so the loop
            runs without a terminal.
    """
    targets = [d for d in drafts if section_ids is None or d.section_id in section_ids]
    try:
        for draft in sorted(targets, key=lambda d: d.section_id):
            _review_one(draft, ctx, scripted)
    except QuitReview:
        print("\nreview ended early; remaining sections stay pending\n")
    return drafts


def _review_one(
    draft: SectionDraft,
    ctx: ReviewContext,
    scripted: dict[int, tuple[str, str | None]] | None,
) -> None:
    """Review one section until it reaches a terminal state or is skipped.

    A successful redraft loops back so the reviewer can judge the new version.
    Two bounds keep that loop finite: a scripted decision is consumed once, so a
    non-interactive run cannot re-reject the same section forever, and
    ``max_cycles`` caps how many rejections one section can absorb before it is
    closed as unsatisfiable. Without the cap a reviewer could spend unbounded
    tokens on a section the evidence will never satisfy.
    """
    cycles = 0
    consumed = False

    while True:
        _present(draft)

        if scripted is not None and consumed:
            # The script has already spoken for this section; a redraft that
            # succeeded leaves it pending for a human to look at.
            print(f"  section {draft.section_id} left pending after redraft\n")
            return

        action, comment = _decide(draft, scripted)
        consumed = True

        if action == "approve":
            draft.review = ReviewRecord(decision="approved", revision=draft.revision)
            ctx.trace.event(
                "review_decision",
                section_id=draft.section_id,
                decision="approved",
                revision=draft.revision,
                comment=None,
            )
            print(f"  section {draft.section_id} approved\n")
            return

        if action == "skip":
            ctx.trace.event(
                "review_decision",
                section_id=draft.section_id,
                decision="skipped",
                revision=draft.revision,
                comment=None,
            )
            print(f"  section {draft.section_id} left pending\n")
            return

        if action == "quit":
            raise QuitReview

        # Rejection. The comment is recorded verbatim before anything acts on it.
        assert comment is not None
        cycles += 1
        if cycles > ctx.max_cycles:
            _terminal(
                draft,
                comment,
                f"rejected {cycles} times; the per-section limit of {ctx.max_cycles} "
                f"rejection cycles was reached, so the section is closed here",
                ctx,
            )
            return

        draft.review = ReviewRecord(
            decision="rejected", comment=comment, revision=draft.revision
        )
        ctx.trace.event(
            "review_decision",
            section_id=draft.section_id,
            decision="rejected",
            revision=draft.revision,
            comment=comment,
        )

        satisfied = _redraft_from_comment(draft, comment, ctx)
        if not satisfied:
            return
        # Redraft succeeded: present it and ask again.


def _redraft_from_comment(draft: SectionDraft, comment: str, ctx: ReviewContext) -> bool:
    """Redraft a rejected section. Returns False if it reached a terminal state."""
    base = draft.draft_prompt
    if not base:
        _terminal(
            draft,
            comment,
            "no drafting prompt was recorded for this section, so it cannot be redrafted",
            ctx,
        )
        return False

    citations = _citation_pool(draft)
    issues: list[ValidationIssue] = []

    for attempt in range(1, ctx.max_attempts + 1):
        prompt = build_redraft_prompt(base, draft.body_markdown, comment)
        if issues:
            prompt = f"{prompt}\n\n{redraft_instruction(issues)}"

        print(f"  redrafting (attempt {attempt}/{ctx.max_attempts}) ...", flush=True)
        drafted: DraftedSection = ctx.llm.parse(
            STAGE, REDRAFT_SYSTEM_PROMPT, prompt, DraftedSection
        )

        if drafted.unsatisfiable_reason:
            ctx.trace.event(
                "redraft_refused",
                section_id=draft.section_id,
                attempt=attempt,
                comment=comment,
                reason=drafted.unsatisfiable_reason,
            )
            _terminal(draft, comment, drafted.unsatisfiable_reason, ctx)
            return False

        issues = validate_section(
            drafted, citations, ctx.admitted_doc_ids, ctx.tripwire_terms, expect_prose=True
        )
        ctx.trace.event(
            "validation",
            section_id=draft.section_id,
            revision=draft.revision + attempt,
            source="review_redraft",
            passed=not issues,
            issues=[i.model_dump(mode="json") for i in issues],
        )

        if not issues:
            draft.body_markdown = drafted.body_markdown
            draft.citations = used_citations(drafted, citations)
            draft.issues = []
            draft.revision += attempt
            draft.review = ReviewRecord(
                decision="pending", comment=comment, revision=draft.revision
            )
            ctx.trace.event(
                "redraft_accepted",
                section_id=draft.section_id,
                revision=draft.revision,
                comment=comment,
            )
            print(f"  redrafted and revalidated (revision {draft.revision})\n")
            return True

        print(f"    {len(issues)} gate failure(s)", flush=True)

    _terminal(
        draft,
        comment,
        (
            f"redrafted {ctx.max_attempts} time(s) and the result failed automated "
            f"validation each time ({'; '.join(i.detail for i in issues)})"
        ),
        ctx,
    )
    return False


def _terminal(draft: SectionDraft, comment: str, reason: str, ctx: ReviewContext) -> None:
    """Record an unsatisfiable rejection. The section is still emitted."""
    draft.review = ReviewRecord(
        decision="rejected_unsatisfiable",
        comment=comment,
        revision=draft.revision,
        unsatisfiable_reason=reason,
    )
    ctx.trace.event(
        "review_decision",
        section_id=draft.section_id,
        decision="rejected_unsatisfiable",
        revision=draft.revision,
        comment=comment,
        unsatisfiable_reason=reason,
    )
    print(f"  section {draft.section_id}: rejection could not be satisfied")
    print(f"    {reason}")
    print("    section is emitted at its last valid revision with the comment recorded\n")


def _citation_pool(draft: SectionDraft) -> list[Citation]:
    """Citations a redraft may use: the ones the section already resolved."""
    return list(draft.citations)


# --------------------------------------------------------------------------- #
# Presentation and input
# --------------------------------------------------------------------------- #


def _present(draft: SectionDraft) -> None:
    """Show a section and everything a reviewer needs to judge it."""
    rule = "=" * 100
    print(rule)
    print(f"SECTION {draft.section_id}. {draft.title}")
    print(f"status: {draft.status}    revision: {draft.revision}    "
          f"citations: {len(draft.citations)}")
    print(rule)

    if draft.body_markdown.strip():
        print(draft.body_markdown.strip())
    else:
        print("(no prose -- every fact in this section is contested or unsupported)")

    conflicts = [f for f in draft.findings if f.kind == "conflict"]
    if conflicts:
        print(f"\n-- {len(conflicts)} unresolved conflict(s), rendered in the document --")
        for finding in conflicts:
            print(f"   {finding.fact_key}: {finding.detail}")
            for position in finding.positions:
                flag = " [internal-only]" if position.internal_only else ""
                print(f"     - {position.value}{flag}  <- {', '.join(position.doc_ids)}")

    if draft.missing_elements:
        print(f"\n-- {len(draft.missing_elements)} required element(s) with no source --")
        for element in draft.missing_elements:
            print(f"   {element}")

    if draft.issues:
        print(f"\n-- {len(draft.issues)} validation issue(s) --")
        for issue in draft.issues:
            print(f"   [{issue.gate}] {issue.detail}")

    if draft.citations:
        print("\n-- citations --")
        for citation in draft.citations:
            print(f"   [{citation.marker}] {citation.doc_id}:"
                  f"{citation.line_start}-{citation.line_end}")
    print()


def _decide(
    draft: SectionDraft, scripted: dict[int, tuple[str, str | None]] | None
) -> tuple[str, str | None]:
    """Get one decision, from the script in non-interactive mode or from stdin."""
    if scripted is not None:
        action, comment = scripted.get(draft.section_id, ("skip", None))
        print(f"[scripted] {action}" + (f": {comment}" if comment else ""))
        return action, comment

    while True:
        try:
            raw = input(f"section {draft.section_id} [a/r/s/v/q/?] > ").strip().lower()
        except EOFError:
            print("\nno input available; leaving remaining sections pending")
            raise QuitReview from None

        if raw in ("a", "approve"):
            return "approve", None
        if raw in ("s", "skip", ""):
            return "skip", None
        if raw in ("q", "quit"):
            return "quit", None
        if raw in ("v", "view"):
            _present(draft)
            continue
        if raw in ("?", "h", "help"):
            print(_HELP)
            continue
        if raw in ("r", "reject"):
            comment = _read_comment()
            if not comment:
                print("  a rejection needs a comment; nothing recorded")
                continue
            return "reject", comment
        print("  unrecognised. '?' for help")


def _read_comment() -> str:
    """Read a possibly multi-line comment, terminated by a blank line."""
    print("  comment (end with an empty line):")
    lines: list[str] = []
    while True:
        try:
            line = input("  > ")
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines).strip()


def review_summary(drafts: list[SectionDraft]) -> str:
    """Tabular summary of the review pass."""
    rule = "-" * 100
    lines = ["", "REVIEW SUMMARY", rule]
    counts: dict[str, int] = {}
    for draft in sorted(drafts, key=lambda d: d.section_id):
        decision = draft.review.decision
        counts[decision] = counts.get(decision, 0) + 1
        lines.append(
            f"  {draft.section_id:>2}. {draft.title:<38} {decision:<24} rev {draft.revision}"
        )
        if draft.review.comment:
            lines.append(f"      comment: {draft.review.comment[:88]}")
        if draft.review.unsatisfiable_reason:
            lines.append(f"      reason : {draft.review.unsatisfiable_reason[:88]}")
    lines.append(rule)
    lines.append("  " + "   ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    lines.append("")
    return "\n".join(lines)


def parse_script(text: str) -> dict[int, tuple[str, str | None]]:
    """Parse a non-interactive decision script.

    One decision per line: ``<section> <approve|reject|skip> [comment]``.
    """
    decisions: dict[int, tuple[str, str | None]] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 2)
        if len(parts) < 2 or not parts[0].isdigit():
            print(f"warning: ignoring unparseable script line: {raw!r}", file=sys.stderr)
            continue
        section_id = int(parts[0])
        action = parts[1].lower()
        comment = parts[2] if len(parts) > 2 else None
        if action.startswith("a"):
            decisions[section_id] = ("approve", None)
        elif action.startswith("r"):
            decisions[section_id] = ("reject", comment or "rejected without detail")
        else:
            decisions[section_id] = ("skip", None)
    return decisions
