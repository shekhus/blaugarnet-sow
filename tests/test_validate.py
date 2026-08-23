"""The deterministic drafting gates."""

from __future__ import annotations

from sow.models import Citation, DraftedSection
from sow.validate import validate_section

CIT = Citation(
    marker="C1", chunk_id="docs/harding_msa_summary.md#L6",
    doc_id="docs/harding_msa_summary.md", quote="net 45", line_start=6, line_end=6,
    instrument="executed_contract", audience="client_facing", status="executed",
)
FOREIGN = Citation(
    marker="C2", chunk_id="docs/northgate_sow_executed.md#L26",
    doc_id="docs/northgate_sow_executed.md", quote="net 30", line_start=26, line_end=26,
    instrument="executed_sow", audience="client_facing", status="executed",
)
ADMITTED = {"docs/harding_msa_summary.md"}


def _check(body, citations=(CIT,), tripwire=("StackWare",), expect_prose=True):
    return validate_section(
        DraftedSection(body_markdown=body), list(citations), ADMITTED,
        list(tripwire), expect_prose,
    )


def test_cited_prose_passes():
    assert _check("Invoices are due net 45 from receipt. [C1]") == []


def test_uncited_assertion_fails():
    issues = _check("Invoices are due net 45 from receipt.")
    assert [i.gate for i in issues] == ["uncited_assertion"]


def test_unknown_marker_fails():
    issues = _check("Something. [C9]")
    assert any(i.gate == "citation_resolves" for i in issues)


def test_out_of_scope_citation_fails():
    """The cross-engagement guarantee at the drafting gate."""
    issues = _check("Terms are net 30. [C2]", citations=(CIT, FOREIGN))
    assert any(i.gate == "citation_in_scope" for i in issues)


def test_foreign_entity_flagged():
    issues = _check("The StackWare adapter is in scope. [C1]")
    assert any(i.gate == "foreign_entity" for i in issues)


def test_headings_and_blockquotes_need_no_citation():
    body = "### Payment\n\n> NOTE: rendered by the system.\n\n| a | b |\n|---|---|\n\nNet 45. [C1]"
    assert _check(body) == []


def test_empty_body_with_claims_fails():
    issues = _check("", expect_prose=True)
    assert any(i.gate == "empty_body" for i in issues)


def test_empty_body_without_claims_is_fine():
    assert _check("", expect_prose=False) == []
