"""The authority policy, including the cases where it must decline to resolve."""

from __future__ import annotations

from sow.analysis import normalise_value
from sow.authority import resolve
from sow.models import Claim


def claim(cid, key, value, doc_id):
    return Claim(
        claim_id=cid, fact_key=key, value=value, value_norm=normalise_value(value),
        chunk_id=f"{doc_id}#L1", doc_id=doc_id, quote="q", supports_elements=[],
    )


MSA = "docs/harding_msa_summary.md"
SCOPING = "transcripts/2026-08-05_harding_scoping_call.md"
INTERNAL = "transcripts/2026-08-19_harding_kickoff_prep_internal.md"
CHAT = "chat/blaugarnet_harding_channel_export.md"
CARD26 = "docs/blaugarnet_rate_card_2026.md"
V1 = "notes/harding_scope_addendum_v1.md"
V2 = "notes/harding_scope_addendum_v2.md"
EMAIL = "emails/harding_timeline_thread.md"


def test_executed_contract_outranks_a_meeting(provs):
    """net 45 in the MSA against net 30 said on a call."""
    r = resolve("payment_terms", [
        claim("a", "payment_terms", "net 45", MSA),
        claim("b", "payment_terms", "net 30", SCOPING),
    ], provs)
    assert r.resolved
    assert r.winner.value == "net 45"
    assert "instrument" in r.reason


def test_internal_only_against_client_facing_does_not_resolve(provs):
    """The disagreement is between the parties, not between sources.

    Asserting either would claim an agreement the evidence does not establish.
    """
    r = resolve("change_request_approval_authority", [
        claim("a", "k", "steering committee only", SCOPING),
        claim("b", "k", "joint approval under 40h", INTERNAL),
        claim("c", "k", "joint approval under 40h", CHAT),
    ], provs)
    assert not r.resolved
    assert r.winner is None
    assert "only by internal documents" in r.reason
    assert len(r.positions) == 2
    assert [p.internal_only for p in r.positions].count(True) == 1


def test_internal_only_cannot_be_sole_support(provs):
    """A 2025-rate commitment that exists only in internal chat is not assertable."""
    r = resolve("rate_card", [
        claim("a", "rate_card", "2026 card", CARD26),
        claim("b", "rate_card", "2025 card", CHAT),
    ], provs)
    assert not r.resolved


def test_superseded_cannot_support_but_is_reported(provs):
    """v1's 2,900 hours must not win, and must still be visible."""
    r = resolve("effort_hours", [
        claim("a", "effort_hours", "2900 hours", V1),
        claim("b", "effort_hours", "2400 hours", V2),
    ], provs)
    assert r.resolved
    assert "2400" in r.winner.value


def test_only_superseded_support_does_not_resolve(provs):
    r = resolve("effort_hours", [claim("a", "effort_hours", "2900 hours", V1)], provs)
    assert not r.resolved
    assert "superseded" in r.reason


def test_unanimous_value_resolves(provs):
    r = resolve("go_live_date", [
        claim("a", "go_live_date", "2027-01-15", EMAIL),
        claim("b", "go_live_date", "2027-01-15", V2),
    ], provs)
    assert r.resolved
    assert not r.contested


def test_date_phrasings_are_one_value(provs):
    """The same date written three ways must not read as three positions."""
    r = resolve("go_live_date", [
        claim("a", "go_live_date", "2027-01-15", EMAIL),
        claim("b", "go_live_date", "January 15, 2027", V2),
    ], provs)
    assert len(r.positions) == 1


def test_hedges_do_not_create_a_conflict(provs):
    r = resolve("effort_hours", [
        claim("a", "effort_hours", "2,400 hours", V2),
        claim("b", "effort_hours", "approximately 2400 hours", EMAIL),
    ], provs)
    assert len(r.positions) == 1
