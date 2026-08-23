"""Replay the committed golden run offline.

Skipped when no fixtures are present, so a cold clone still passes; recorded
with `sow draft --record`. The rest of the suite is deterministic and needs
neither fixtures nor a key.
"""

from __future__ import annotations

import pytest

from sow.audit import audit_document
from sow.config import FIXTURE_DIR, OUTPUT_DIR
from sow.llm import LlmClient
from sow.run import run_draft

pytestmark = pytest.mark.skipif(
    not FIXTURE_DIR.is_dir() or not any(FIXTURE_DIR.glob("*.json")),
    reason=(
        "no golden run recorded; run 'sow draft --record' once with a funded key "
        "to populate tests/fixtures/golden_run"
    ),
)


def test_replay_produces_an_auditable_draft(ctx, tmp_path):
    llm = LlmClient(backend="mock", fixture_dir=FIXTURE_DIR)
    run = run_draft(ctx, llm, tmp_path, verbose=False)
    document = (tmp_path / "sow_draft.md").read_text(encoding="utf-8")

    assert document, "a run must always produce a draft"
    result = audit_document(document, ctx, run)
    assert result.passed, result.failures


def test_replay_is_deterministic(ctx, tmp_path):
    """Same fixtures, same document. Retrieval and analysis carry no randomness."""
    first = run_draft(ctx, LlmClient(backend="mock", fixture_dir=FIXTURE_DIR),
                      tmp_path / "a", verbose=False)
    second = run_draft(ctx, LlmClient(backend="mock", fixture_dir=FIXTURE_DIR),
                       tmp_path / "b", verbose=False)
    assert (tmp_path / "a" / "sow_draft.md").read_text(encoding="utf-8") == (
        tmp_path / "b" / "sow_draft.md"
    ).read_text(encoding="utf-8")
    assert len(first.sections) == len(second.sections) == 12
