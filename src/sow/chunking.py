"""Stage 4 -- split documents into citable, line-anchored passages.

Chunk boundaries follow each document's own structure rather than a fixed
window, because a citation has to land on a passage a reader can check. The
scoping call's retraction lives inside a single speaker turn -- "blended it
comes out around a hundred and five... sorry, no, that's -- ignore that" -- so
splitting that turn would hand a downstream stage the figure without the
correction attached to it.

``Chunk.text`` is always verbatim source. Nothing is normalised, rewritten or
prefixed, so quote verification later can be exact substring matching.
"""

from __future__ import annotations

import re

from .config import Roster
from .models import Chunk, DocProvenance, Document

# "**Priya Nair:**" at the start of a transcript turn.
_SPEAKER = re.compile(r"^\*\*([A-Z][^*:]{1,48}):\*\*")
# "**[2026-08-20 11:08] priya.nair:**" at the start of a chat message.
_CHAT = re.compile(r"^\*\*\[([^\]]+)\]\s*([^*:]+):\*\*")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_LIST_ITEM = re.compile(r"^\s{0,3}(?:[-*+]|\d+\.)\s+")
_FENCE = re.compile(r"^(?:---|\*\*\*|___)\s*$")

Block = tuple[int, int, str | None, str | None]
"""(start_line, end_line, heading_path, speaker), all 1-based inclusive."""


def chunk_corpus(
    docs: list[Document],
    provs: dict[str, DocProvenance],
    roster: Roster,
    skip_doc_ids: frozenset[str] = frozenset(),
) -> list[Chunk]:
    """Chunk every document, in corpus order."""
    out: list[Chunk] = []
    for doc in docs:
        if doc.doc_id in skip_doc_ids:
            continue
        out.extend(chunk_document(doc, provs[doc.doc_id], roster))
    return out


def chunk_document(doc: Document, prov: DocProvenance, roster: Roster) -> list[Chunk]:
    """Split one document according to its instrument class."""
    if prov.instrument in ("client_meeting", "internal_meeting"):
        blocks = _split_speaker_turns(doc)
    elif prov.instrument == "internal_chat":
        blocks = _split_chat_messages(doc)
    elif prov.instrument == "client_correspondence":
        blocks = _split_email_messages(doc)
    else:
        blocks = _split_structured(doc)

    others = {
        name: aliases
        for name, aliases in roster.clients.items()
        if name != roster.target
    }

    chunks: list[Chunk] = []
    for start, end, heading, speaker in blocks:
        text = "\n".join(doc.lines[start - 1 : end])
        if not text.strip():
            continue
        lowered = text.lower()
        foreign = sorted(
            name for name, aliases in others.items() if any(a in lowered for a in aliases)
        )
        anchor = f"L{start}" if start == end else f"L{start}-{end}"
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}#{anchor}",
                doc_id=doc.doc_id,
                text=text,
                line_start=start,
                line_end=end,
                heading_path=heading,
                speaker=speaker,
                foreign_mentions=foreign,
            )
        )
    return chunks


def _trim(lines: tuple[str, ...], start: int, end: int) -> tuple[int, int]:
    """Shrink a 1-based inclusive span to drop leading and trailing blank lines."""
    while start <= end and not lines[start - 1].strip():
        start += 1
    while end >= start and not lines[end - 1].strip():
        end -= 1
    return start, end


def _emit(lines: tuple[str, ...], start: int, end: int, heading: str | None,
          speaker: str | None, out: list[Block]) -> None:
    """Append a trimmed, non-empty block."""
    start, end = _trim(lines, start, end)
    if start <= end:
        out.append((start, end, heading, speaker))


def _split_speaker_turns(doc: Document) -> list[Block]:
    """One chunk per speaker turn; the metadata preamble is its own chunk."""
    lines = doc.lines
    starts = [i + 1 for i, line in enumerate(lines) if _SPEAKER.match(line)]
    out: list[Block] = []

    preamble_end = (starts[0] - 1) if starts else len(lines)
    _emit(lines, 1, preamble_end, None, None, out)

    for idx, start in enumerate(starts):
        end = (starts[idx + 1] - 1) if idx + 1 < len(starts) else len(lines)
        match = _SPEAKER.match(lines[start - 1])
        _emit(lines, start, end, None, match.group(1) if match else None, out)
    return out


def _split_chat_messages(doc: Document) -> list[Block]:
    """One chunk per chat message; the export header is its own chunk."""
    lines = doc.lines
    starts = [i + 1 for i, line in enumerate(lines) if _CHAT.match(line)]
    out: list[Block] = []

    preamble_end = (starts[0] - 1) if starts else len(lines)
    _emit(lines, 1, preamble_end, None, None, out)

    for idx, start in enumerate(starts):
        end = (starts[idx + 1] - 1) if idx + 1 < len(starts) else len(lines)
        match = _CHAT.match(lines[start - 1])
        _emit(lines, start, end, None, match.group(2).strip() if match else None, out)
    return out


def _split_email_messages(doc: Document) -> list[Block]:
    """One chunk per message in a thread, split on horizontal rules.

    A single-message email has no rules, so the whole body becomes one chunk
    after the title.
    """
    lines = doc.lines
    out: list[Block] = []

    fences = [i + 1 for i, line in enumerate(lines) if _FENCE.match(line)]
    if not fences:
        _emit(lines, 1, 1, None, None, out)
        _emit(lines, 2, len(lines), None, None, out)
        return out

    _emit(lines, 1, fences[0] - 1, None, None, out)
    for idx, fence in enumerate(fences):
        start = fence + 1
        end = (fences[idx + 1] - 1) if idx + 1 < len(fences) else len(lines)
        sender = None
        for line in lines[start - 1 : min(end, start + 3)]:
            if line.startswith("**From:**"):
                sender = line[len("**From:**") :].split("·")[0].strip()
                break
        _emit(lines, start, end, None, sender, out)
    return out


def _split_structured(doc: Document) -> list[Block]:
    """Split prose documents on headings, then on blocks within each heading.

    A run of list items becomes one chunk per top-level item, so an individually
    citable fact -- an MSA term, a playbook guardrail, a numbered scope item --
    is not buried inside a larger passage. Tables stay whole: a rate card row
    without its header row states nothing.
    """
    lines = doc.lines
    out: list[Block] = []
    heading_stack: list[tuple[int, str]] = []
    i = 0
    n = len(lines)

    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        if not stripped:
            i += 1
            continue

        heading_match = _HEADING.match(raw)
        if heading_match:
            level = len(heading_match.group(1))
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, heading_match.group(2).strip()))
            i += 1
            continue

        block_start = i + 1
        while i < n and lines[i].strip():
            i += 1
        block_end = i

        path = " > ".join(title for _, title in heading_stack) or None
        _emit_block(lines, block_start, block_end, path, out)

    return out


def _emit_block(lines: tuple[str, ...], start: int, end: int, heading: str | None,
                out: list[Block]) -> None:
    """Emit one contiguous block, exploding lists into their items."""
    span = lines[start - 1 : end]

    if any(line.lstrip().startswith("|") for line in span):
        _emit(lines, start, end, heading, None, out)
        return

    item_starts = [start + offset for offset, line in enumerate(span) if _LIST_ITEM.match(line)]
    if len(item_starts) < 2:
        _emit(lines, start, end, heading, None, out)
        return

    if item_starts[0] > start:
        _emit(lines, start, item_starts[0] - 1, heading, None, out)
    for idx, item_start in enumerate(item_starts):
        item_end = (item_starts[idx + 1] - 1) if idx + 1 < len(item_starts) else end
        _emit(lines, item_start, item_end, heading, None, out)
