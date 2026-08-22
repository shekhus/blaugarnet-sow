"""Paths and the engagement roster.

No secrets live here. The LLM key is read from the environment at the point of
use (see ``sow.llm``), never from a config file.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

# Repo root is three levels up from this file: src/sow/config.py -> repo root.
REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
OUTPUT_DIR = REPO_ROOT / "output"
CONFIG_DIR = REPO_ROOT / "config"
ROSTER_PATH = CONFIG_DIR / "engagements.toml"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "golden_run"

# The SOW template is a source document, but it defines the target structure
# rather than supplying engagement facts. Stages that assemble evidence skip it.
TEMPLATE_DOC_ID = "sow_template.md"


class ConfigError(RuntimeError):
    """Raised when configuration is missing or malformed. Never swallowed."""


@dataclass(frozen=True)
class Roster:
    """The engagement roster loaded from ``config/engagements.toml``.

    Declares who the clients are. Declares nothing about scope, rates, dates or
    conflicts.
    """

    target: str
    clients: dict[str, tuple[str, ...]]
    company_markers: tuple[str, ...]

    @property
    def admitted_labels(self) -> frozenset[str]:
        """Engagement labels whose documents may enter the evidence pool.

        Derived, not configured: the target engagement plus company-wide
        material. Everything else is excluded.
        """
        return frozenset({self.target, "company"})

    def other_clients(self) -> tuple[str, ...]:
        """Client labels that are hard-excluded from evidence."""
        return tuple(sorted(k for k in self.clients if k != self.target))


@lru_cache(maxsize=1)
def load_roster(path: Path | None = None) -> Roster:
    """Load and validate the engagement roster.

    Fails loudly on a missing file, a missing target, or a target that has no
    entry in the client table -- a silently empty roster would admit every
    document in the corpus.
    """
    roster_path = path or ROSTER_PATH
    if not roster_path.is_file():
        raise ConfigError(f"engagement roster not found: {roster_path}")

    with roster_path.open("rb") as fh:
        raw = tomllib.load(fh)

    target = raw.get("target")
    if not isinstance(target, str) or not target.strip():
        raise ConfigError(f"{roster_path}: 'target' must be a non-empty string")

    clients_raw = raw.get("clients")
    if not isinstance(clients_raw, dict) or not clients_raw:
        raise ConfigError(f"{roster_path}: 'clients' table is missing or empty")

    clients: dict[str, tuple[str, ...]] = {}
    for name, aliases in clients_raw.items():
        if not isinstance(aliases, list) or not all(isinstance(a, str) for a in aliases):
            raise ConfigError(f"{roster_path}: clients.{name} must be a list of strings")
        if not aliases:
            raise ConfigError(f"{roster_path}: clients.{name} has no aliases")
        clients[name] = tuple(a.lower() for a in aliases)

    if target not in clients:
        raise ConfigError(
            f"{roster_path}: target '{target}' has no entry in the [clients] table"
        )

    markers = raw.get("company_markers")
    if not isinstance(markers, list) or not markers:
        raise ConfigError(f"{roster_path}: 'company_markers' must be a non-empty list")

    return Roster(
        target=target,
        clients=clients,
        company_markers=tuple(str(m).lower() for m in markers),
    )
