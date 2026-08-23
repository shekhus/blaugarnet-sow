"""Authority parsed off header lines, and the traps in doing so."""

from __future__ import annotations

import pytest


def test_playbook_is_not_executed(ctx):
    """Its fourth guardrail says "the executed MSA always wins".

    Scanning a fixed number of lines reads that as the playbook itself being an
    executed instrument, which would let it outrank a client meeting.
    """
    prov = ctx.partition.provenance["internal/blaugarnet_sales_playbook_extract.md"]
    assert prov.status == "current"
    assert prov.instrument == "policy"


def test_chat_export_status_not_taken_from_a_message(ctx):
    """One chat message reads "addendum v2 is out for signature"."""
    prov = ctx.partition.provenance["chat/blaugarnet_harding_channel_export.md"]
    assert prov.status != "out_for_signature"


def test_supersession_is_inferred_across_documents(ctx):
    """v1 never says it is superseded; only v2 says it supersedes v1."""
    v1 = ctx.partition.provenance["notes/harding_scope_addendum_v1.md"]
    v2 = ctx.partition.provenance["notes/harding_scope_addendum_v2.md"]
    assert v1.status == "superseded"
    assert v1.instrument == "superseded_addendum"
    assert v2.status == "out_for_signature"
    assert v2.instrument == "unsigned_addendum"
    assert "supersede" in " ".join(e.reason for e in v1.evidence).lower()


def test_distribution_restriction_is_read_from_the_header(ctx):
    prov = ctx.partition.provenance["transcripts/2026-08-19_harding_kickoff_prep_internal.md"]
    assert prov.restriction == "not_for_client_distribution"
    assert prov.audience == "internal_only"


def test_msa_is_an_executed_contract(ctx):
    prov = ctx.partition.provenance["docs/harding_msa_summary.md"]
    assert prov.instrument == "executed_contract"
    assert prov.status == "executed"
    assert prov.audience == "client_facing"


@pytest.mark.parametrize(
    "doc_id,audience",
    [
        ("docs/blaugarnet_rate_card_2026.md", "standard"),
        ("transcripts/2026-08-05_harding_scoping_call.md", "client_facing"),
        ("chat/blaugarnet_harding_channel_export.md", "internal_only"),
        ("notes/harding_requirements_draft.md", "internal_only"),
    ],
)
def test_audience_classes(ctx, doc_id, audience):
    assert ctx.partition.provenance[doc_id].audience == audience


def test_every_field_records_why(ctx):
    """A provenance decision is itself citable."""
    prov = ctx.partition.provenance["notes/harding_scope_addendum_v2.md"]
    for field in ("engagement", "instrument", "audience", "status", "doc_date"):
        assert prov.evidence_for(field) is not None


def test_missing_date_is_reported_not_invented(ctx):
    prov = ctx.partition.provenance["sow_template.md"]
    assert prov.doc_date is None
    assert any("no date" in w for w in ctx.partition.warnings)
