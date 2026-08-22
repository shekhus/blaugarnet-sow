"""Stage 7 -- assemble the evidence pool for one section.

Two selectors feed the pool:

* **pinned** -- chunks from the governing instruments (the executed contract and
  the current addendum) are always present, whatever they score. Lexical
  retrieval is good at finding passages that share a section's vocabulary and
  bad at finding the one contractual clause that quietly overrides it: the MSA
  states net 45 without ever using the word "commercials".
* **retrieved** -- BM25 over everything else that survived the engagement
  boundary.

Superseded documents stay retrievable on purpose. The draft has to be able to
report that addendum v1 said something different; what the authority policy bars
is letting a superseded document *support* an assertion.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import TEMPLATE_DOC_ID
from .index import Bm25Index
from .models import Chunk, DocProvenance, EvidencePool, Partition, ScoredChunk, SectionSpec

# Instruments whose chunks are pinned into every section's pool.
PINNED_INSTRUMENTS = frozenset({"executed_contract", "unsigned_addendum", "signed_addendum"})

# Instruments where a passage is a turn in a conversation, so the turns either
# side of it carry the correction, objection or answer that changes its meaning.
# Meera's "we don't -- i misspoke on the call, was looking at the northgate
# sheet" is only a correction because of the message directly above it; Meera's
# "flagged as open point pls" is only meaningful beside the proposal it answers.
# Neither reply scores well alone -- both are short and share little vocabulary
# with a section query -- so lexical ranking finds the claim and drops the
# retraction attached to it.
DIALOGIC_INSTRUMENTS = frozenset(
    {"internal_chat", "client_meeting", "internal_meeting", "client_correspondence"}
)

DEFAULT_TOP_K = 24


@dataclass(frozen=True)
class EvidenceIndex:
    """Everything needed to assemble pools, built once per run."""

    chunks: list[Chunk]
    index: Bm25Index
    partition: Partition
    excluded_chunk_count: int

    def provenance(self, chunk: Chunk) -> DocProvenance:
        """Provenance of the document a chunk came from."""
        return self.partition.provenance[chunk.doc_id]


def build_evidence_index(
    all_chunks: list[Chunk], partition: Partition, doc_titles: dict[str, str]
) -> EvidenceIndex:
    """Restrict chunks to admitted documents and index what remains.

    The engagement boundary is applied here, before ranking. Chunks from another
    client's documents are not down-weighted -- they are absent, so no section
    can retrieve or cite them.
    """
    admitted_docs = {d.doc_id for d in partition.admitted} - {TEMPLATE_DOC_ID}
    admitted = [c for c in all_chunks if c.doc_id in admitted_docs]
    excluded = len(all_chunks) - len(admitted)

    if not admitted:
        raise RuntimeError("no admitted chunks: every document was filtered out")

    retrieval_texts = [
        "\n".join(
            part
            for part in (doc_titles.get(c.doc_id, ""), c.heading_path or "", c.text)
            if part
        )
        for c in admitted
    ]

    return EvidenceIndex(
        chunks=admitted,
        index=Bm25Index(admitted, retrieval_texts=retrieval_texts),
        partition=partition,
        excluded_chunk_count=excluded,
    )


def assemble_pool(
    spec: SectionSpec, evidence: EvidenceIndex, top_k: int = DEFAULT_TOP_K
) -> EvidencePool:
    """Select the chunks one section may draw on."""
    selected: list[ScoredChunk] = []
    seen: set[str] = set()

    for chunk in evidence.chunks:
        prov = evidence.provenance(chunk)
        if prov.instrument in PINNED_INSTRUMENTS and prov.status != "superseded":
            selected.append(ScoredChunk(chunk=chunk, score=0.0, selector="pinned"))
            seen.add(chunk.chunk_id)

    query = spec.query()
    rank = 0
    # Rank the whole admitted set, then take the top_k that are not already
    # pinned. Requesting only top_k from the index would silently return fewer,
    # since pinned chunks occupy many of the highest-scoring positions.
    for chunk, score in evidence.index.search(query, top_k=len(evidence.chunks)):
        if chunk.chunk_id in seen:
            continue
        rank += 1
        selected.append(
            ScoredChunk(chunk=chunk, score=round(score, 4), selector="retrieved", rank=rank)
        )
        seen.add(chunk.chunk_id)
        if rank >= top_k:
            break

    selected.extend(_expand_adjacent(selected, evidence, seen))

    excluded_docs = sorted(d.doc_id for d in evidence.partition.excluded)

    return EvidencePool(
        section_id=spec.section_id,
        title=spec.title,
        selected=selected,
        candidate_chunks=len(evidence.chunks),
        excluded_docs=excluded_docs,
        excluded_chunks=evidence.excluded_chunk_count,
        query=query,
    )


def _expand_adjacent(
    selected: list[ScoredChunk], evidence: EvidenceIndex, seen: set[str]
) -> list[ScoredChunk]:
    """Pull in the turns either side of each retrieved conversational passage.

    Expansion applies only to dialogic documents. A policy clause or an addendum
    bullet states a self-contained fact and needs no neighbour; a chat message or
    a speaker turn frequently does not.
    """
    positions = {chunk.chunk_id: i for i, chunk in enumerate(evidence.chunks)}
    added: list[ScoredChunk] = []

    for scored in list(selected):
        if scored.selector != "retrieved":
            continue
        chunk = scored.chunk
        if evidence.provenance(chunk).instrument not in DIALOGIC_INSTRUMENTS:
            continue

        idx = positions.get(chunk.chunk_id)
        if idx is None:
            continue

        for offset in (-1, 1):
            neighbour_idx = idx + offset
            if not 0 <= neighbour_idx < len(evidence.chunks):
                continue
            neighbour = evidence.chunks[neighbour_idx]
            if neighbour.doc_id != chunk.doc_id or neighbour.chunk_id in seen:
                continue
            added.append(ScoredChunk(chunk=neighbour, score=0.0, selector="adjacent"))
            seen.add(neighbour.chunk_id)

    return added
