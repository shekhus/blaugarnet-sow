"""Structured records passed between pipeline stages.

Every stage boundary is a validated pydantic model. Nothing downstream consumes
a bare dict, so a malformed intermediate fails at the boundary that produced it
rather than three stages later.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# --------------------------------------------------------------------------- #
# Vocabularies
# --------------------------------------------------------------------------- #

EngagementLabel = Literal[
    "harding",
    "company",
    "northgate",
    "atlas",
    "helios",
    "AMBIGUOUS",
]

Instrument = Literal[
    "executed_contract",
    "executed_sow",
    "signed_addendum",
    "unsigned_addendum",
    "superseded_addendum",
    "client_correspondence",
    "client_meeting",
    "internal_meeting",
    "internal_chat",
    "working_draft",
    "policy",
    "template",
    "reference",
    "unknown",
]

# How a document may be used as support for client-facing assertive text.
#
#   client_facing    -- a bilateral record: executed contracts, client meetings,
#                       correspondence with the client. May solely support an
#                       assertion.
#   standard         -- an established internal standard that is legitimately
#                       quotable to a client: rate cards, policies, the SOW
#                       template. May solely support an assertion. (Without this
#                       class, rates -- which exist only on the rate cards --
#                       could never be asserted.)
#   internal_only    -- a record of Blaugarnet's own deliberation or an
#                       unreviewed draft. May INFORM a section but may never be
#                       the SOLE support for a client-facing assertion.
Audience = Literal["client_facing", "standard", "internal_only"]

DocStatus = Literal[
    "executed",
    "out_for_signature",
    "superseded",
    "draft_incomplete",
    "current",
    "unknown",
]

Restriction = Literal["none", "not_for_client_distribution", "do_not_circulate"]


# --------------------------------------------------------------------------- #
# Stage 1 -- ingest
# --------------------------------------------------------------------------- #


class Document(BaseModel):
    """A source file read verbatim from ``data/``. Never mutated."""

    model_config = ConfigDict(frozen=True)

    doc_id: str = Field(description="Path relative to data/, POSIX separators.")
    path: Path
    text: str
    lines: tuple[str, ...]

    @property
    def h1(self) -> str | None:
        """The first level-1 markdown heading, or None if the file has none."""
        for line in self.lines:
            if line.startswith("# "):
                return line[2:].strip()
        return None


# --------------------------------------------------------------------------- #
# Stage 2 -- provenance
# --------------------------------------------------------------------------- #


class FieldEvidence(BaseModel):
    """Why a provenance field holds the value it holds.

    ``source_line`` is the verbatim line the value was parsed from, so every
    provenance decision is itself citable back to the corpus.
    """

    field: str
    value: str
    reason: str
    source_line: str | None = None
    line_no: int | None = None


class DocProvenance(BaseModel):
    """Authority metadata for one document, parsed deterministically.

    Authority is deliberately several orthogonal axes rather than one score:
    an unsigned addendum and an internal chat message are not comparable on a
    single scale, and collapsing them to a number is what produces a
    recency-only resolver.
    """

    doc_id: str
    engagement: EngagementLabel
    instrument: Instrument
    audience: Audience
    status: DocStatus
    restriction: Restriction
    doc_date: date | None
    evidence: list[FieldEvidence] = Field(default_factory=list)

    def evidence_for(self, field: str) -> FieldEvidence | None:
        """Return the recorded evidence for one provenance field."""
        return next((e for e in self.evidence if e.field == field), None)


# --------------------------------------------------------------------------- #
# Stage 3 -- admission
# --------------------------------------------------------------------------- #


class AdmissionDecision(BaseModel):
    """Whether one document may enter the evidence pool, and why."""

    doc_id: str
    engagement: EngagementLabel
    admitted: bool
    reason: str


class Partition(BaseModel):
    """The corpus split into admitted and excluded sets.

    Written to the trace and printed on every run: the reviewer sees the
    engagement boundary before reading a single drafted word.
    """

    target: str
    decisions: list[AdmissionDecision]
    provenance: dict[str, DocProvenance]
    warnings: list[str] = Field(default_factory=list)

    @property
    def admitted(self) -> list[AdmissionDecision]:
        return [d for d in self.decisions if d.admitted]

    @property
    def excluded(self) -> list[AdmissionDecision]:
        return [d for d in self.decisions if not d.admitted]

    def counts(self) -> dict[str, int]:
        """Document count per engagement label."""
        out: dict[str, int] = {}
        for d in self.decisions:
            out[d.engagement] = out.get(d.engagement, 0) + 1
        return dict(sorted(out.items()))
