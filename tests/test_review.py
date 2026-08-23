"""The review loop's terminal states. Nothing disappears from the document."""

from __future__ import annotations

from pathlib import Path

from sow.llm import LlmClient, TokenUsage
from sow.models import Citation, DraftedSection, SectionDraft
from sow.review import ReviewContext, parse_script, review_sections
from sow.trace import Trace

CIT = Citation(
    marker="C1", chunk_id="docs/harding_msa_summary.md#L6",
    doc_id="docs/harding_msa_summary.md", quote="net 45", line_start=6, line_end=6,
    instrument="executed_contract", audience="client_facing", status="executed",
)


class _Usage:
    input_tokens = 100
    output_tokens = 50


class _Llm(LlmClient):
    """Behaviour keyed by section: 2 refuses, 3 never cites, others redraft cleanly."""

    def __init__(self):
        super().__init__(backend="mock", fixture_dir=Path("/nonexistent"))
        self.usage = TokenUsage()
        self.calls = 0

    def parse(self, stage, system, user, output_format, max_tokens=16000, effort="high"):
        self.usage.record(stage, _Usage())
        self.calls += 1
        if "SECTION 2" in user:
            return DraftedSection(
                body_markdown="",
                unsatisfiable_reason="no claim states a total contract value",
            )
        if "SECTION 3" in user:
            return DraftedSection(body_markdown="Uncited sentence.")
        return DraftedSection(body_markdown="Redrafted prose. [C1]")


def _draft(sid):
    return SectionDraft(
        section_id=sid, title=f"S{sid}", status="drafted",
        body_markdown="Original prose. [C1]", citations=[CIT], findings=[],
        missing_elements=[], revision=0,
        draft_prompt=f"SOW SECTION {sid}: S{sid}\n  [C1] fact: value",
    )


def _review(script, tmp_path, drafts=None, **kw):
    drafts = drafts or [_draft(1), _draft(2), _draft(3)]
    llm = _Llm()
    with Trace(tmp_path / "t.jsonl") as trace:
        ctx = ReviewContext(
            llm=llm, trace=trace, admitted_doc_ids={CIT.doc_id},
            tripwire_terms=[], max_attempts=2, **kw,
        )
        review_sections(drafts, ctx, scripted=parse_script(script))
    events = [
        __import__("json").loads(line)
        for line in (tmp_path / "t.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    return drafts, events, llm


def test_approve(tmp_path):
    drafts, events, _ = _review("1 approve\n2 skip\n3 skip", tmp_path)
    assert drafts[0].review.decision == "approved"
    assert any(e["kind"] == "review_decision" and e["decision"] == "approved" for e in events)


def test_reject_then_successful_redraft(tmp_path):
    drafts, events, _ = _review("1 reject Tighten this up.\n2 skip\n3 skip", tmp_path)
    assert "Redrafted prose" in drafts[0].body_markdown
    assert drafts[0].revision == 1
    assert any(e["kind"] == "redraft_accepted" for e in events)


def test_comment_recorded_verbatim(tmp_path):
    comment = "Tighten this up."
    _, events, _ = _review(f"1 reject {comment}\n2 skip\n3 skip", tmp_path)
    rejected = [e for e in events if e.get("decision") == "rejected"]
    assert rejected and rejected[0]["comment"] == comment


def test_model_refusal_is_a_terminal_state(tmp_path):
    """A reviewer can ask for something the evidence does not support."""
    drafts, events, _ = _review("2 reject State the total contract value.", tmp_path)
    section = next(d for d in drafts if d.section_id == 2)
    assert section.review.decision == "rejected_unsatisfiable"
    assert "no claim states" in section.review.unsatisfiable_reason
    assert any(e["kind"] == "redraft_refused" for e in events)


def test_refused_section_keeps_its_last_valid_revision(tmp_path):
    drafts, _, _ = _review("2 reject State the total contract value.", tmp_path)
    section = next(d for d in drafts if d.section_id == 2)
    assert section.body_markdown == "Original prose. [C1]"


def test_retry_cap_exhausted_is_terminal(tmp_path):
    drafts, _, llm = _review("3 reject Add a sentence.", tmp_path)
    section = next(d for d in drafts if d.section_id == 3)
    assert section.review.decision == "rejected_unsatisfiable"
    assert "failed automated validation" in section.review.unsatisfiable_reason
    assert llm.calls == 2


def test_every_section_survives_review(tmp_path):
    """A review pass must never remove content from the document."""
    drafts, _, _ = _review(
        "1 approve\n2 reject State the total contract value.\n3 reject Add a sentence.",
        tmp_path,
    )
    assert len(drafts) == 3
    assert all(d.body_markdown for d in drafts)


def test_scripted_rejection_is_consumed_once(tmp_path):
    """A successful redraft must not re-read the same decision forever."""
    drafts, _, llm = _review("1 reject Tighten this up.\n2 skip\n3 skip", tmp_path)
    assert drafts[0].review.decision == "pending"
    assert llm.calls == 1
