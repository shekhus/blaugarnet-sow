"""Command-line entry point.

Checkpoint 1 exposes one command:

    sow partition [--verbose] [--json PATH]

which runs stages 1-3 (ingest, provenance, admission) and prints the corpus
partition. No model is called and no API key is required.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .admission import build_partition
from .config import DATA_DIR, OUTPUT_DIR, ConfigError, load_roster
from .ingest import load_corpus
from .report import render_partition


def cmd_partition(args: argparse.Namespace) -> int:
    """Run ingest -> provenance -> admission and report the partition."""
    roster = load_roster(Path(args.roster) if args.roster else None)
    docs = load_corpus(Path(args.data) if args.data else DATA_DIR)
    partition = build_partition(docs, roster)

    print(render_partition(partition, verbose=args.verbose))

    if args.json:
        out_path = Path(args.json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(partition.model_dump_json(indent=2), encoding="utf-8")
        print(f"partition written to {out_path}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser."""
    parser = argparse.ArgumentParser(
        prog="sow",
        description="Grounded Statement of Work drafter (Harding Outfitters engagement).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_part = sub.add_parser(
        "partition",
        help="Show which source documents are admitted as evidence, and why.",
    )
    p_part.add_argument(
        "--verbose",
        action="store_true",
        help="Show the parsed reason and date evidence for every document.",
    )
    p_part.add_argument(
        "--json",
        nargs="?",
        const=str(OUTPUT_DIR / "partition.json"),
        help="Also write the full partition record as JSON (default: output/partition.json).",
    )
    p_part.add_argument("--data", help="Override the data directory.")
    p_part.add_argument("--roster", help="Override the engagement roster TOML.")
    p_part.set_defaults(func=cmd_partition)

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Configuration errors fail loudly with a non-zero exit."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (ConfigError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
