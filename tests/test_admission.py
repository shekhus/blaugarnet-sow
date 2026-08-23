"""The engagement boundary. These pin the partition of data/.

If a roster edit changes which documents count as evidence, this fails loudly
rather than quietly widening what the draft may cite.
"""

from __future__ import annotations

import pytest

from sow.models import Document
from sow.provenance import classify_engagement

ADMITTED = 20
EXCLUDED = 6


def test_partition_is_pinned(ctx):
    assert len(ctx.partition.admitted) == ADMITTED
    assert len(ctx.partition.excluded) == EXCLUDED
    assert len(ctx.partition.decisions) == ADMITTED + EXCLUDED


def test_no_document_is_ambiguous(ctx):
    assert [d.doc_id for d in ctx.partition.decisions if d.engagement == "AMBIGUOUS"] == []


@pytest.mark.parametrize(
    "doc_id",
    [
        "docs/blaugarnet_rate_card_2025.md",
        "docs/blaugarnet_rate_card_2026.md",
        "internal/blaugarnet_sales_playbook_extract.md",
        "internal/blaugarnet_infosec_policy.md",
        "internal/blaugarnet_qa_checklist_template.md",
    ],
)
def test_company_wide_material_is_admitted(ctx, doc_id):
    """Rates exist only on the cards; barring them would make section 8 undraftable."""
    assert ctx.partition.provenance[doc_id].engagement == "company"


def test_chat_export_admitted_despite_naming_another_client(ctx):
    """The subject signal is the title, so a body mention cannot reclassify a document."""
    doc_id = "chat/blaugarnet_harding_channel_export.md"
    assert ctx.partition.provenance[doc_id].engagement == "harding"
    body = ctx.document(doc_id).text.lower()
    assert "northgate" in body


@pytest.mark.parametrize(
    "doc_id,engagement",
    [
        ("docs/northgate_sow_executed.md", "northgate"),
        ("emails/northgate_cutover_email.md", "northgate"),
        ("transcripts/2026-05-19_northgate_kickoff.md", "northgate"),
        ("internal/helios_bank_postmortem.md", "helios"),
        ("notes/atlas_retail_discovery_notes.md", "atlas"),
        ("notes/atlas_retail_status.md", "atlas"),
    ],
)
def test_other_client_documents_are_blocked(ctx, doc_id, engagement):
    assert ctx.partition.provenance[doc_id].engagement == engagement
    assert doc_id not in {d.doc_id for d in ctx.partition.admitted}


def _doc(name: str, h1: str) -> Document:
    text = f"# {h1}\n\nbody\n"
    return Document(
        doc_id=name, path=__import__("pathlib").Path(name), text=text,
        lines=tuple(text.splitlines()),
    )


def test_multi_client_subject_is_ambiguous(ctx):
    """No document in the corpus triggers this, so it needs a synthetic case."""
    label, reason, _ = classify_engagement(
        _doc("harding_northgate_joint.md", "Harding and Northgate joint review"), ctx.roster
    )
    assert label == "AMBIGUOUS"
    assert "multiple clients" in reason


def test_signal_disagreement_is_ambiguous(ctx):
    label, reason, _ = classify_engagement(
        _doc("northgate_notes.md", "Harding Outfitters discovery"), ctx.roster
    )
    assert label == "AMBIGUOUS"
    assert "disagree" in reason


def test_missing_title_is_ambiguous(ctx):
    text = "no heading here\n"
    doc = Document(
        doc_id="x.md", path=__import__("pathlib").Path("x.md"), text=text,
        lines=tuple(text.splitlines()),
    )
    label, reason, _ = classify_engagement(doc, ctx.roster)
    assert label == "AMBIGUOUS"
    assert "no H1" in reason


def test_ambiguous_is_excluded_not_admitted(ctx):
    """The failure mode is exclusion, never admission on the benefit of the doubt."""
    assert "AMBIGUOUS" not in ctx.roster.admitted_labels
