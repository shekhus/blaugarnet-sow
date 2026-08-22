"""Shared run context for stages 1-7.

Built once and reused by every command, so the partition, chunking and index a
draft is built from are exactly the ones the inspection commands display.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .admission import build_partition
from .chunking import chunk_corpus
from .config import TEMPLATE_DOC_ID, ConfigError, Roster, load_roster
from .evidence import EvidenceIndex, build_evidence_index
from .index import build_tripwire_terms
from .ingest import load_corpus
from .models import Chunk, Document, Partition, SectionSpec
from .template import parse_template


@dataclass(frozen=True)
class RunContext:
    """Everything stages 1-7 produce, assembled once."""

    roster: Roster
    documents: list[Document]
    partition: Partition
    chunks: list[Chunk]
    sections: list[SectionSpec]
    evidence: EvidenceIndex
    tripwire_terms: list[str]

    def document(self, doc_id: str) -> Document:
        """Look up a source document by id."""
        for doc in self.documents:
            if doc.doc_id == doc_id:
                return doc
        raise KeyError(doc_id)

    def section(self, section_id: int) -> SectionSpec:
        """Look up a parsed template section by number."""
        for spec in self.sections:
            if spec.section_id == section_id:
                return spec
        available = ", ".join(str(s.section_id) for s in self.sections)
        raise ConfigError(f"no section {section_id} in the template (have: {available})")


def build_context(
    data_dir: Path | None = None, roster_path: Path | None = None
) -> RunContext:
    """Run stages 1-7. No model is called and no API key is required."""
    roster = load_roster(roster_path)
    documents = load_corpus(data_dir)
    partition = build_partition(documents, roster)

    provs = partition.provenance
    chunks = chunk_corpus(documents, provs, roster)

    template_doc = next((d for d in documents if d.doc_id == TEMPLATE_DOC_ID), None)
    if template_doc is None:
        raise ConfigError(f"SOW template not found at data/{TEMPLATE_DOC_ID}")
    sections = parse_template(template_doc)

    by_id = {doc.doc_id: doc for doc in documents}
    doc_titles = {doc.doc_id: (doc.h1 or "") for doc in documents}
    evidence = build_evidence_index(chunks, partition, doc_titles)

    admitted_text = {d.doc_id: by_id[d.doc_id].text for d in partition.admitted}
    excluded_text = {d.doc_id: by_id[d.doc_id].text for d in partition.excluded}
    tripwire_terms = build_tripwire_terms(admitted_text, excluded_text)

    return RunContext(
        roster=roster,
        documents=documents,
        partition=partition,
        chunks=chunks,
        sections=sections,
        evidence=evidence,
        tripwire_terms=tripwire_terms,
    )
