"""Required elements come from the template's own guidance prose."""

from __future__ import annotations

from sow.template import split_requirements


def test_all_twelve_sections(ctx):
    assert [s.section_id for s in ctx.sections] == list(range(1, 13))


def test_acceptance_authority_is_a_required_element(ctx):
    """Section 12's "by whom" is the gap nothing in the corpus fills.

    It is derived here, at run time, from the template -- not from a list of
    things somebody thought to look for.
    """
    spec = ctx.section(12)
    assert "by whom" in [e.lower() for e in spec.required_elements]
    assert len(spec.required_elements) == 3


def test_governance_elements(ctx):
    elements = [e.lower() for e in ctx.section(6).required_elements]
    assert "meeting cadence" in elements
    assert "escalation path" in elements
    assert "who approves change requests" in elements


def test_commercials_elements(ctx):
    elements = [e.lower() for e in ctx.section(8).required_elements]
    assert {"rates", "estimated effort", "payment schedule", "payment terms"} <= set(elements)


def test_parenthetical_enumeration_is_not_split():
    """"staffing (role, allocation)" is one requirement, not two."""
    parts = split_requirements("Blaugarnet staffing (role, allocation) and named counterparts.")
    assert parts == ["Blaugarnet staffing (role, allocation)", "named counterparts"]


def test_table_prefix_is_stripped():
    assert split_requirements("Table: deliverable, description, target milestone.") == [
        "deliverable", "description", "target milestone"
    ]
