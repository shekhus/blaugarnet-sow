"""Conflict and insufficiency detection, plus quote verification.

The C-numbers reference the recall fixture recorded in CLAUDE.md's Source notes.
That list is a yardstick for what a careful human found; it is never consulted by
the detector, which finds disagreement by comparing values under a shared fact
key.
"""

from __future__ import annotations

from sow.analysis import analyse_section
from sow.claims import verify_claims
from sow.evidence import assemble_pool
from sow.models import ClaimExtraction, ExtractedClaim

SCOPING = "transcripts/2026-08-05_harding_scoping_call.md"
INTERNAL = "transcripts/2026-08-19_harding_kickoff_prep_internal.md"
CHAT = "chat/blaugarnet_harding_channel_export.md"
MSA = "docs/harding_msa_summary.md"


def _extraction(*rows):
    return ClaimExtraction(claims=[
        ExtractedClaim(fact_key=k, value=v, chunk_id=c, quote=q, supports_elements=list(e))
        for k, v, c, q, e in rows
    ])


def _run(ctx, section_id, extraction):
    spec = ctx.section(section_id)
    pool = assemble_pool(spec, ctx.evidence)
    verified, rejected = verify_claims(extraction, pool)
    return analyse_section(spec, pool, verified, rejected, ctx.partition.provenance), pool


def test_c6_change_approval_conflict_detected_from_evidence(ctx):
    """C6: the corpus's genuinely unresolved fact."""
    analysis, _ = _run(ctx, 6, _extraction(
        ("change_request_approval_authority", "steering committee only",
         f"{SCOPING}#L17", "Nothing gets approved outside that committee",
         ["who approves change requests"]),
        ("change_request_approval_authority", "joint approval under 40h",
         f"{INTERNAL}#L17",
         "change requests under forty hours of impact are approved by me and their "
         "IT director jointly", ["who approves change requests"]),
        ("change_control_instrument", "written change order",
         f"{MSA}#L13",
         "changes to any SOW require a written change order executed by both parties",
         ["who approves change requests"]),
    ))
    conflicts = [f for f in analysis.findings if f.kind == "conflict"]
    assert len(conflicts) == 1
    assert conflicts[0].fact_key == "change_request_approval_authority"
    assert len(conflicts[0].positions) == 2
    assert any(p.internal_only for p in conflicts[0].positions)
    assert analysis.status in ("conflict", "conflict_and_insufficient")


def test_g6b_escalation_path_reported_missing(ctx):
    """G6b: the template requires it and no source addresses it."""
    analysis, _ = _run(ctx, 6, _extraction(
        ("steering_cadence", "monthly", f"{SCOPING}#L17", "we meet monthly",
         ["Meeting cadence"]),
    ))
    assert "escalation path" in analysis.missing_elements
    assert any(
        f.kind == "insufficient" and f.required_element == "escalation path"
        for f in analysis.findings
    )


def test_g12_acceptance_authority_reported_missing(ctx):
    """G12: nothing in the corpus names who accepts deliverables."""
    analysis, _ = _run(ctx, 12, _extraction())
    assert "by whom" in [m.lower() for m in analysis.missing_elements]


def test_findings_never_block_the_artifact(ctx):
    """Findings change how a section renders, never whether it renders."""
    analysis, _ = _run(ctx, 6, _extraction(
        ("k", "a", f"{SCOPING}#L17", "Nothing gets approved outside that committee", []),
        ("k", "b", f"{INTERNAL}#L17", "I own change approval day to day", []),
    ))
    assert analysis.findings
    assert not any(f.blocking for f in analysis.findings)


def test_non_verbatim_quote_is_rejected(ctx):
    """One word inserted. The requirement is a verbatim span."""
    analysis, _ = _run(ctx, 6, _extraction(
        ("k", "v", f"{SCOPING}#L17", "Nothing gets approved outside of that committee", []),
    ))
    assert len(analysis.claims) == 0
    assert len(analysis.rejected) == 1
    assert "not a substring" in analysis.rejected[0].reject_reason


def test_quote_from_outside_the_pool_is_rejected(ctx):
    """A citation to an excluded document cannot survive verification."""
    analysis, _ = _run(ctx, 6, _extraction(
        ("payment_terms", "net 30", "docs/northgate_sow_executed.md#L26", "Terms: net 30", []),
    ))
    assert len(analysis.claims) == 0
    assert "not in this section's evidence pool" in analysis.rejected[0].reject_reason


def test_reproduced_quote_is_distinguished_from_absent_one(ctx):
    """Whitespace-folded matches are still rejected, but say why."""
    analysis, _ = _run(ctx, 6, _extraction(
        ("k", "v", f"{SCOPING}#L17", "Nothing   gets approved outside that committee", []),
    ))
    assert "reproduced, not copied" in analysis.rejected[0].reject_reason


def test_clean_section_has_no_findings(ctx):
    analysis, _ = _run(ctx, 6, _extraction(
        ("cadence", "monthly", f"{SCOPING}#L17", "we meet monthly", ["Meeting cadence"]),
        ("escalation", "x", f"{SCOPING}#L17", "I chair it", ["escalation path"]),
        ("approver", "y", f"{SCOPING}#L17", "goes to our steering committee",
         ["who approves change requests"]),
    ))
    assert analysis.missing_elements == []
    assert [f for f in analysis.findings if f.kind == "conflict"] == []
    assert analysis.status == "clean"


# --------------------------------------------------------------------------- #
# G12 -- the acceptance authority the corpus never names.
#
# Coverage used to be whatever the model said it was. Section 12 asks "by whom",
# the model offered the playbook rule requiring that every SOW name an acceptance
# authority, and the gap went unreported while the draft asserted the opposite.
# These pin the verification that now stands between the two.
# --------------------------------------------------------------------------- #

PLAYBOOK = "internal/blaugarnet_sales_playbook_extract.md"
PLAYBOOK_RULE = (
    "5. Every SOW names the client-side acceptance authority. Post-Helios, no exceptions."
)


def test_policy_demanding_a_party_does_not_supply_one(ctx):
    """G12, exactly as it occurred: the real quote, the real element."""
    analysis, _ = _run(ctx, 12, _extraction(
        ("acceptance_authority", "SOW names the client-side acceptance authority",
         f"{PLAYBOOK}#L8", PLAYBOOK_RULE, ["by whom"]),
    ))

    assert "by whom" in analysis.missing_elements
    gap = next(f for f in analysis.findings if f.required_element == "by whom")
    assert gap.kind == "insufficient"
    assert "company-wide policy" in gap.detail
    assert analysis.status in ("insufficient", "conflict_and_insufficient")


def test_an_engagement_source_can_supply_a_party(ctx):
    """The rule must not simply refuse every party element."""
    analysis, _ = _run(ctx, 12, _extraction(
        ("acceptance_authority", "Karen Boyle",
         f"{SCOPING}#L33", "Acceptance — how do we formally accept deliverables?",
         ["by whom"]),
    ))
    assert "by whom" not in analysis.missing_elements


def test_a_recorded_absence_is_not_an_answer(ctx):
    """A source saying the authority is TBD has not named one."""
    analysis, _ = _run(ctx, 12, _extraction(
        ("acceptance_authority", "TBD",
         f"{SCOPING}#L33", "Acceptance — how do we formally accept deliverables?",
         ["by whom"]),
    ))
    assert "by whom" in analysis.missing_elements


def test_company_policy_still_covers_a_non_party_element(ctx):
    """The narrowing is confined to elements asking *who*.

    Rates live only on the company-wide cards; requiring engagement-specific
    support everywhere would invent gaps the corpus does not have.
    """
    analysis, _ = _run(ctx, 12, _extraction(
        ("acceptance_mechanism", "release checklist sign-off",
         f"{PLAYBOOK}#L8", PLAYBOOK_RULE, ["How deliverables are accepted"]),
    ))
    assert "How deliverables are accepted" not in analysis.missing_elements
