"""Stage 1 -- read the source corpus.

``data/`` is read-only. Documents are loaded verbatim, including line structure,
because citations are line-anchored and must be checkable against the file by
hand.
"""

from __future__ import annotations

from pathlib import Path

from .config import DATA_DIR, ConfigError
from .models import Document


def load_corpus(data_dir: Path | None = None) -> list[Document]:
    """Read every markdown file under ``data/``, sorted by doc_id.

    Raises:
        ConfigError: if the data directory is missing or contains no markdown.
    """
    root = data_dir or DATA_DIR
    if not root.is_dir():
        raise ConfigError(f"data directory not found: {root}")

    paths = sorted(root.rglob("*.md"))
    if not paths:
        raise ConfigError(f"no markdown documents found under {root}")

    docs = [load_document(p, root) for p in paths]

    empty = [d.doc_id for d in docs if not d.text.strip()]
    if empty:
        raise ConfigError(f"empty source documents: {', '.join(empty)}")

    return docs


def load_document(path: Path, root: Path | None = None) -> Document:
    """Read one source file into a Document with its line structure preserved."""
    base = root or DATA_DIR
    text = path.read_text(encoding="utf-8")
    return Document(
        doc_id=path.relative_to(base).as_posix(),
        path=path,
        text=text,
        lines=tuple(text.splitlines()),
    )
