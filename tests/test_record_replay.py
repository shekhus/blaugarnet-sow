"""The golden-run mechanism: record, replay, and fail loudly when stale.

These run against a stand-in provider, so they verify the recording path itself
without a key. A bug here would only surface after a paid run, which is exactly
the wrong time to find it.
"""

from __future__ import annotations

import json

import pytest

from sow.llm import LlmClient, LlmError, TokenUsage
from sow.models import ClaimExtraction, DraftedSection


class _Usage:
    input_tokens = 1234
    output_tokens = 567


class _Recorder(LlmClient):
    """Writes fixtures through the real record() path."""

    def __init__(self, fixture_dir):
        super().__init__(backend="live", fixture_dir=fixture_dir, record_fixtures=True)
        self.usage = TokenUsage()

    def parse(self, stage, system, user, output_format, max_tokens=16000, effort="high"):
        self.usage.record(stage, _Usage())
        parsed = (
            ClaimExtraction(claims=[])
            if output_format is ClaimExtraction
            else DraftedSection(body_markdown="Recorded. [C1]")
        )
        self.record(stage, system, user, parsed)
        return parsed


def test_record_then_replay_returns_the_same_object(tmp_path):
    rec = _Recorder(tmp_path)
    rec.parse("draft_section", "SYS", "USER", DraftedSection)

    mock = LlmClient(backend="mock", fixture_dir=tmp_path)
    replayed = mock.parse("draft_section", "SYS", "USER", DraftedSection)
    assert replayed.body_markdown == "Recorded. [C1]"


def test_fixture_key_is_prompt_specific(tmp_path):
    """A changed prompt must miss its fixture rather than replay a stale one."""
    rec = _Recorder(tmp_path)
    rec.parse("draft_section", "SYS", "USER", DraftedSection)

    mock = LlmClient(backend="mock", fixture_dir=tmp_path)
    with pytest.raises(LlmError, match="no recorded response"):
        mock.parse("draft_section", "SYS", "USER CHANGED", DraftedSection)


def test_missing_fixture_never_falls_through_to_a_live_call(tmp_path):
    """Silently reaching the network would void every offline guarantee."""
    mock = LlmClient(backend="mock", fixture_dir=tmp_path)
    with pytest.raises(LlmError, match="golden run is stale"):
        mock.parse("draft_section", "SYS", "USER", DraftedSection)


def test_recorded_fixture_keeps_real_token_counts(tmp_path):
    """A replayed golden run should report what the recorded run cost."""
    rec = _Recorder(tmp_path)
    rec.parse("draft_section", "SYS", "USER", DraftedSection)

    payload = json.loads(next(tmp_path.glob("*.json")).read_text(encoding="utf-8"))
    assert payload["usage"] == {"input_tokens": 1234, "output_tokens": 567}
    assert payload["provider"] in ("anthropic", "openai")

    mock = LlmClient(backend="mock", fixture_dir=tmp_path)
    mock.parse("draft_section", "SYS", "USER", DraftedSection)
    assert mock.usage.input_tokens == 1234
    assert mock.usage.output_tokens == 567
