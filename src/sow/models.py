"""Structured records passed between pipeline stages.

Every stage boundary is a validated pydantic model. Nothing downstream consumes
a bare dict, so a malformed intermediate fails at the boundary that produced it
rather than three stages later.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Literal

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


# --------------------------------------------------------------------------- #
# Stage 4 -- chunking
# --------------------------------------------------------------------------- #


class Chunk(BaseModel):
    """One citable passage, anchored to its source lines.

    ``text`` is verbatim source: exactly the lines between ``line_start`` and
    ``line_end`` inclusive, joined by newlines and nothing else. Downstream
    quote verification checks that every quoted span is a substring of this
    field, so context such as the heading path is kept beside the text rather
    than folded into it.
    """

    model_config = ConfigDict(frozen=True)

    chunk_id: str = Field(description="doc_id#L<start> or doc_id#L<start>-<end>.")
    doc_id: str
    text: str
    line_start: int
    line_end: int
    heading_path: str | None = None
    speaker: str | None = None
    foreign_mentions: list[str] = Field(
        default_factory=list,
        description=(
            "Other engagements named inside this chunk. The chunk is admitted -- "
            "its document is in scope -- but the mention is surfaced so a claim "
            "drawn from it can be inspected."
        ),
    )


# --------------------------------------------------------------------------- #
# Stage 6 -- template parse
# --------------------------------------------------------------------------- #


class SectionSpec(BaseModel):
    """One SOW section, and what the template says it must contain.

    ``required_elements`` is parsed from the template's own guidance prose, not
    authored here. Section 12's guidance -- "How deliverables are accepted, by
    whom, and within what window" -- yields the acceptance-authority
    requirement that the corpus never satisfies.
    """

    section_id: int
    title: str
    guidance: str
    required_elements: list[str]
    subsections: list[str] = Field(default_factory=list)

    def query(self) -> str:
        """Retrieval query text for this section."""
        return " ".join([self.title, *self.subsections, *self.required_elements])


# --------------------------------------------------------------------------- #
# Stage 7 -- evidence assembly
# --------------------------------------------------------------------------- #


class ScoredChunk(BaseModel):
    """A chunk selected for a section's evidence pool, with why it was selected."""

    chunk: Chunk
    score: float
    selector: Literal["pinned", "retrieved", "adjacent"]
    rank: int | None = None


class EvidencePool(BaseModel):
    """Everything one section is allowed to draw on.

    ``excluded_docs`` records how much of the corpus the engagement boundary
    removed before ranking ran, so the filter's effect is visible per section
    rather than only in the global partition.
    """

    section_id: int
    title: str
    selected: list[ScoredChunk]
    candidate_chunks: int
    excluded_docs: list[str]
    excluded_chunks: int
    query: str

    def chunk_ids(self) -> set[str]:
        """Chunk ids this section may cite. Anything else is a citation failure."""
        return {sc.chunk.chunk_id for sc in self.selected}


# --------------------------------------------------------------------------- #
# Stage 8 -- claim extraction (the model's structured output)
# --------------------------------------------------------------------------- #


class ExtractedClaim(BaseModel):
    """One factual assertion the model found in one passage."""

    fact_key: str = Field(
        description="snake_case identifier for the fact, stable across passages."
    )
    value: str = Field(description="Shortest precise form of the value.")
    chunk_id: str = Field(description="The passage this came from.")
    quote: str = Field(description="Verbatim span copied from that passage.")
    supports_elements: list[str] = Field(default_factory=list)


class ClaimExtraction(BaseModel):
    """The model's full response for one section."""

    claims: list[ExtractedClaim] = Field(default_factory=list)


class Claim(BaseModel):
    """An extracted claim after verification, with provenance attached."""

    claim_id: str
    fact_key: str
    value: str
    value_norm: str
    chunk_id: str
    doc_id: str
    quote: str
    supports_elements: list[str] = Field(default_factory=list)
    verified: bool = True
    reject_reason: str | None = None


# --------------------------------------------------------------------------- #
# Stage 10 -- analysis
# --------------------------------------------------------------------------- #

FindingKind = Literal[
    "conflict",
    "insufficient",
    "provisional",
    "internal_only_support",
    "superseded_only_support",
    "unverified_claim",
]


class Position(BaseModel):
    """One distinct value on a contested fact, and what supports it."""

    value: str
    value_norm: str
    claim_ids: list[str]
    doc_ids: list[str]
    audiences: list[str]
    instruments: list[str]
    best_rank: int
    latest_date: date | None
    internal_only: bool = Field(
        description="Every document supporting this value is internal deliberation."
    )


class Finding(BaseModel):
    """Something the draft must surface rather than resolve silently."""

    kind: FindingKind
    detail: str
    fact_key: str | None = None
    required_element: str | None = None
    claim_ids: list[str] = Field(default_factory=list)
    positions: list[Position] = Field(default_factory=list)
    blocking: bool = Field(
        default=False,
        description=(
            "Findings change how a section renders; they never withhold it. A run "
            "that ends with no draft file is a failed run."
        ),
    )


AnalysisStatus = Literal["clean", "conflict", "insufficient", "conflict_and_insufficient"]


class SectionAnalysis(BaseModel):
    """Everything stages 8-10 concluded about one section."""

    section_id: int
    title: str
    status: AnalysisStatus
    claims: list[Claim]
    rejected: list[Claim]
    findings: list[Finding]
    covered_elements: list[str]
    missing_elements: list[str]
    pool_size: int


# --------------------------------------------------------------------------- #
# Stage 11 -- drafting
# --------------------------------------------------------------------------- #


class DraftedSection(BaseModel):
    """The model's contribution to a section: prose only.

    The model never writes status banners, conflict blocks, gap notices or the
    citation table. Those are rendered from ``Finding`` records by code, so
    "every finding is surfaced" is guaranteed structurally rather than
    requested in a prompt.
    """

    body_markdown: str = Field(
        description="Prose for the settled material only, every assertion carrying a [Cn] marker."
    )
    drafting_notes: list[str] = Field(
        default_factory=list,
        description="Anything the model could not state from the claims it was given.",
    )


class Citation(BaseModel):
    """A resolvable pointer from a marker in the draft to a source passage."""

    marker: str
    chunk_id: str
    doc_id: str
    quote: str
    line_start: int
    line_end: int
    instrument: str
    audience: str
    status: str


class ValidationIssue(BaseModel):
    """One deterministic gate failure against a drafted section."""

    gate: Literal[
        "citation_resolves",
        "citation_in_scope",
        "uncited_assertion",
        "foreign_entity",
        "empty_body",
    ]
    detail: str
    excerpt: str | None = None


ReviewDecision = Literal["pending", "approved", "rejected", "rejected_unsatisfiable"]


class ReviewRecord(BaseModel):
    """What a reviewer did with a section, and what came of it."""

    decision: ReviewDecision = "pending"
    comment: str | None = None
    revision: int = 0
    unsatisfiable_reason: str | None = None


SectionStatus = Literal[
    "drafted",
    "conflict",
    "insufficient",
    "conflict_and_insufficient",
    "unsupported",
]


class SectionDraft(BaseModel):
    """One finished section: prose, citations, findings and review state.

    ``status`` controls how a section renders, never whether it renders. A run
    that ends without a draft file is a failed run.
    """

    section_id: int
    title: str
    status: SectionStatus
    body_markdown: str
    citations: list[Citation]
    findings: list[Finding]
    missing_elements: list[str]
    open_item_ids: list[str] = Field(default_factory=list)
    issues: list[ValidationIssue] = Field(default_factory=list)
    revision: int = 0
    review: ReviewRecord = Field(default_factory=ReviewRecord)


class OpenQuestion(BaseModel):
    """A numbered entry in the assembled Assumptions & Open Questions section."""

    ref: str
    section_id: int
    kind: FindingKind
    detail: str
    positions: list[Position] = Field(default_factory=list)


class CrossSectionIssue(BaseModel):
    """One fact resolved differently in two or more sections.

    Reported and rendered; never allowed to block the artifact. A corpus where
    something is genuinely unresolvable would otherwise produce no draft at all.
    """

    fact_key: str
    section_ids: list[int]
    values: list[str]
    detail: str


class DraftRun(BaseModel):
    """The whole run: every section, the open-question rollup, and spend."""

    sections: list[SectionDraft]
    open_questions: list[OpenQuestion]
    cross_section_issues: list[CrossSectionIssue]
    model: str
    token_usage: dict[str, Any] = Field(default_factory=dict)
