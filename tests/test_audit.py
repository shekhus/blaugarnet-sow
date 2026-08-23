"""The quality check: audit a rendered document against the corpus.

This is the check named in the README as how a draft is judged. It re-reads
data/ and re-verifies every citation from scratch, trusting nothing the run
recorded about itself.
"""

from __future__ import annotations

import pytest

from sow.assemble import render_document
from sow.audit import audit_document
from sow.models import Citation, DraftRun, SectionDraft

GOOD_QUOTE = "invoices due **net 45** from receipt"
MSA = "docs/harding_msa_summary.md"


def _citation(marker="C1", doc_id=MSA, quote=GOOD_QUOTE, start=6, end=6):
    return Citation(
        marker=marker, chunk_id=f"{doc_id}#L{start}", doc_id=doc_id, quote=quote,
        line_start=start, line_end=end, instrument="executed_contract",
        audience="client_facing", status="executed",
    )


def _run(ctx, body, citations):
    sections = [
        SectionDraft(
            section_id=s.section_id, title=s.title, status="drafted",
            body_markdown=body if s.section_id == 8 else f"Placeholder. [{citations[0].marker}]",
            citations=list(citations), findings=[], missing_elements=[],
        )
        for s in ctx.sections
    ]
    return DraftRun(sections=sections, open_questions=[], cross_section_issues=[],
                    model="test", token_usage={})


def test_well_formed_document_passes(ctx):
    run = _run(ctx, "Invoices are due net 45 from receipt. [C1]", [_citation()])
    result = audit_document(render_document(run, "harding"), ctx, run)
    assert result.passed, result.failures
    assert result.section_count == 12


def test_citation_to_excluded_document_fails(ctx):
    """The cross-engagement guarantee, checked on the finished artifact."""
    bad = _citation(doc_id="docs/northgate_sow_executed.md", quote="USD 105/hour", start=26, end=26)
    run = _run(ctx, "The blended rate is USD 105/hour. [C1]", [bad])
    result = audit_document(render_document(run, "harding"), ctx, run)
    assert not result.passed
    assert not result.checks["citation_in_scope"]


def test_non_verbatim_quote_fails(ctx):
    bad = _citation(quote="invoices due net 60 from receipt")
    run = _run(ctx, "Invoices are due net 60. [C1]", [bad])
    result = audit_document(render_document(run, "harding"), ctx, run)
    assert not result.passed
    assert not result.checks["quote_verbatim"]


def test_quote_pointing_at_the_wrong_lines_fails(ctx):
    """A real quote attached to the wrong line range is still a broken citation."""
    bad = _citation(quote=GOOD_QUOTE, start=12, end=12)
    run = _run(ctx, "Invoices are due net 45. [C1]", [bad])
    result = audit_document(render_document(run, "harding"), ctx, run)
    assert not result.checks["quote_verbatim"]


def test_foreign_entity_in_prose_fails(ctx):
    run = _run(ctx, "The StackWare adapter is delivered. [C1]", [_citation()])
    result = audit_document(render_document(run, "harding"), ctx, run)
    assert not result.checks["no_foreign_entity"]


def test_missing_section_fails(ctx):
    run = _run(ctx, "Net 45. [C1]", [_citation()])
    run.sections = [s for s in run.sections if s.section_id != 7]
    result = audit_document(render_document(run, "harding"), ctx, run)
    assert not result.checks["sections_complete"]


@pytest.mark.parametrize("check", [
    "citation_resolves", "citation_in_scope", "quote_verbatim",
    "no_foreign_entity", "sections_complete", "findings_disclosed",
])
def test_every_check_is_reported(ctx, check):
    run = _run(ctx, "Net 45. [C1]", [_citation()])
    result = audit_document(render_document(run, "harding"), ctx, run)
    assert check in result.checks
