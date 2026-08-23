"""Chunking and retrieval: the contamination guarantee, and recall it must keep."""

from __future__ import annotations

import pytest

from sow.evidence import assemble_pool
from sow.index import stem


def test_chunk_text_is_verbatim_source(ctx):
    """Quote verification is exact substring matching, so text must not be rewritten."""
    for chunk in ctx.chunks[:200]:
        doc = ctx.document(chunk.doc_id)
        assert chunk.text == "\n".join(doc.lines[chunk.line_start - 1 : chunk.line_end])


def test_retraction_stays_with_its_claim(ctx):
    """The scoping call states a blended rate and withdraws it in the same turn."""
    chunk = next(
        c for c in ctx.chunks
        if c.chunk_id == "transcripts/2026-08-05_harding_scoping_call.md#L23"
    )
    assert "hundred and five" in chunk.text
    assert "ignore that" in chunk.text


@pytest.mark.parametrize("section_id", list(range(1, 13)))
def test_no_out_of_scope_chunk_in_any_pool(ctx, section_id):
    """The structural guarantee: excluded documents are absent, not down-ranked."""
    pool = assemble_pool(ctx.section(section_id), ctx.evidence)
    excluded = {d.doc_id for d in ctx.partition.excluded}
    assert not [s for s in pool.selected if s.chunk.doc_id in excluded]


def test_commercials_pool_contains_the_rate_tables(ctx):
    """Without plural stemming, "rates" never matches "Hourly rate" and the
    section is assembled with the deal-note rules but no actual rates."""
    ids = assemble_pool(ctx.section(8), ctx.evidence).chunk_ids()
    assert "docs/blaugarnet_rate_card_2026.md#L4-12" in ids
    assert "docs/blaugarnet_rate_card_2025.md#L4-12" in ids


def test_commercials_pool_contains_both_corrections(ctx):
    ids = assemble_pool(ctx.section(8), ctx.evidence).chunk_ids()
    assert "transcripts/2026-08-05_harding_scoping_call.md#L23" in ids
    assert "chat/blaugarnet_harding_channel_export.md#L14" in ids
    assert "docs/harding_msa_summary.md#L6" in ids


def test_governance_pool_contains_both_positions(ctx):
    ids = assemble_pool(ctx.section(6), ctx.evidence).chunk_ids()
    assert "transcripts/2026-08-05_harding_scoping_call.md#L17" in ids
    assert "transcripts/2026-08-19_harding_kickoff_prep_internal.md#L17" in ids
    assert "docs/harding_msa_summary.md#L13" in ids


def test_adjacent_turn_pulled_in(ctx):
    """A short reply carries the correction but scores nothing on its own."""
    ids = assemble_pool(ctx.section(6), ctx.evidence).chunk_ids()
    assert "chat/blaugarnet_harding_channel_export.md#L21" in ids


def test_superseded_is_retrievable_but_marked(ctx):
    """The draft must be able to report what v1 said; the policy stops it supporting."""
    ids = assemble_pool(ctx.section(8), ctx.evidence).chunk_ids()
    assert any(c.startswith("notes/harding_scope_addendum_v1.md") for c in ids)
    assert ctx.partition.provenance["notes/harding_scope_addendum_v1.md"].status == "superseded"


def test_tripwire_excludes_shared_vocabulary(ctx):
    """"Northgate" and "105" appear in admitted documents too, so the textual
    tripwire cannot catch them. That is a conflict, not contamination."""
    assert "Northgate" not in ctx.tripwire_terms
    assert "105" not in ctx.tripwire_terms
    assert "StackWare" in ctx.tripwire_terms


def test_tripwire_excludes_template_vocabulary(ctx):
    """Section headings the template itself mandates must never be tripwire terms."""
    assert "Milestones" not in ctx.tripwire_terms
    assert "Objectives" not in ctx.tripwire_terms


def test_plural_stemming_is_conservative():
    assert stem("rates") == "rate"
    assert stem("terms") == "term"
    assert stem("business") == "business"
    assert stem("status") == "status"
    assert stem("analysis") == "analysis"
