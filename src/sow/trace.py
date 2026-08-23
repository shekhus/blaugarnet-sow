"""Run trace: an append-only JSONL record of how each section was assembled.

One object per event. Enough to reconstruct, for any section, what was
retrieved, what was sent to the model, what came back, what was rejected and
what was flagged -- without re-running anything.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class Trace:
    """Append-only JSONL writer."""

    def __init__(self, path: Path, append: bool = False) -> None:
        """Open the trace.

        Args:
            append: continue an existing trace rather than truncating it. The
                review pass appends, so a section's drafting history and the
                decisions taken on it stay in one file.
        """
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._seq = 0
        if append and self.path.is_file():
            self._seq = sum(1 for _ in self.path.open(encoding="utf-8"))
        self._fh = self.path.open("a" if append else "w", encoding="utf-8", newline="\n")

    def event(self, kind: str, section_id: int | None = None, **payload: Any) -> None:
        """Write one trace event."""
        self._seq += 1
        record = {
            "seq": self._seq,
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "kind": kind,
            "section_id": section_id,
            **payload,
        }
        self._fh.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        self._fh.flush()

    def close(self) -> None:
        """Close the underlying file."""
        self._fh.close()

    def __enter__(self) -> "Trace":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
