"""Command-line entry point.

Stages 1-7 are inspectable without calling a model or setting an API key:

    sow partition [--verbose]   which documents are evidence, and why
    sow template                sections and required elements parsed from the template
    sow chunks [--doc X]        how documents were split into citable passages
    sow evidence --section N    the pool one section may draw on, with scores
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .admission import build_partition
from .analysis import analyse_section
from .claims import STAGE, SYSTEM_PROMPT, build_user_prompt, verify_claims
from .config import (
    DATA_DIR,
    FIXTURE_DIR,
    OUTPUT_DIR,
    ConfigError,
    load_dotenv,
    load_roster,
)
from .evidence import DEFAULT_TOP_K, assemble_pool
from .ingest import load_corpus
from .llm import LlmClient
from .models import ClaimExtraction
from .pipeline import RunContext, build_context
from .report import render_analysis, render_partition, render_pool, render_sections
from .trace import Trace


def _context(args: argparse.Namespace) -> RunContext:
    """Build the shared run context from common CLI options."""
    return build_context(
        data_dir=Path(args.data) if args.data else None,
        roster_path=Path(args.roster) if args.roster else None,
    )


def _write_json(path_arg: str, payload: str) -> None:
    """Write a JSON payload, creating parent directories."""
    out_path = Path(path_arg)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(payload, encoding="utf-8")
    print(f"written to {out_path}")


def cmd_partition(args: argparse.Namespace) -> int:
    """Run ingest -> provenance -> admission and report the partition."""
    roster = load_roster(Path(args.roster) if args.roster else None)
    docs = load_corpus(Path(args.data) if args.data else DATA_DIR)
    partition = build_partition(docs, roster)

    print(render_partition(partition, verbose=args.verbose))

    if args.json:
        _write_json(args.json, partition.model_dump_json(indent=2))

    return 0


def cmd_template(args: argparse.Namespace) -> int:
    """Show the sections and required elements parsed from the SOW template."""
    ctx = _context(args)
    print(render_sections(ctx.sections))
    if args.json:
        payload = json.dumps([s.model_dump() for s in ctx.sections], indent=2)
        _write_json(args.json, payload)
    return 0


def cmd_chunks(args: argparse.Namespace) -> int:
    """Show how documents were split into citable passages."""
    ctx = _context(args)
    chunks = ctx.chunks
    if args.doc:
        chunks = [c for c in chunks if args.doc in c.doc_id]
        if not chunks:
            raise ConfigError(f"no chunks match document filter: {args.doc}")

    print()
    for chunk in chunks:
        prov = ctx.partition.provenance[chunk.doc_id]
        mark = "PASS " if prov.engagement in ctx.roster.admitted_labels else "BLOCK"
        head = chunk.speaker or chunk.heading_path or ""
        print(f"{mark} {chunk.chunk_id}")
        if head:
            print(f"      ({head})")
        print(f"      {' '.join(chunk.text.split())[:150]}")
    print(f"\n{len(chunks)} chunks from {len({c.doc_id for c in chunks})} documents\n")
    return 0


def cmd_evidence(args: argparse.Namespace) -> int:
    """Show the evidence pool assembled for one section."""
    ctx = _context(args)
    spec = ctx.section(args.section)
    pool = assemble_pool(spec, ctx.evidence, top_k=args.top_k)

    print(render_pool(pool, ctx, show_text=not args.quiet))

    if args.tripwire:
        print(f"TRIPWIRE TERMS ({len(ctx.tripwire_terms)}) -- proper nouns only in excluded docs:")
        print("  " + ", ".join(ctx.tripwire_terms))
        print()

    if args.json:
        _write_json(args.json, pool.model_dump_json(indent=2))

    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    """Extract claims for one section, verify quotes, and analyse the result."""
    ctx = _context(args)
    spec = ctx.section(args.section)
    pool = assemble_pool(spec, ctx.evidence, top_k=args.top_k)
    llm = LlmClient(fixture_dir=FIXTURE_DIR)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with Trace(OUTPUT_DIR / "trace.jsonl") as trace:
        trace.event(
            "partition",
            admitted=[d.doc_id for d in ctx.partition.admitted],
            excluded=[d.doc_id for d in ctx.partition.excluded],
        )
        trace.event(
            "evidence_pool",
            section_id=spec.section_id,
            query=pool.query,
            selected=[
                {"chunk_id": s.chunk.chunk_id, "selector": s.selector, "score": s.score}
                for s in pool.selected
            ],
            candidate_chunks=pool.candidate_chunks,
            excluded_chunks=pool.excluded_chunks,
        )

        print(f"calling model ({llm.backend} backend, {llm.model}) for section {spec.section_id}...")
        extraction = llm.parse(STAGE, SYSTEM_PROMPT, build_user_prompt(spec, pool), ClaimExtraction)

        if args.tamper_quotes and extraction.claims:
            victim = extraction.claims[0]
            original = victim.quote
            victim.quote = victim.quote.replace(" ", " slightly ", 1) or "not in the source"
            print(
                "\n[--tamper-quotes] corrupted one quote after extraction to exercise "
                f"the verifier:\n    was: {original[:70]!r}\n    now: {victim.quote[:78]!r}\n"
            )

        trace.event(
            "claim_extraction",
            section_id=spec.section_id,
            system_prompt_chars=len(SYSTEM_PROMPT),
            user_prompt_chars=len(build_user_prompt(spec, pool)),
            raw_claims=len(extraction.claims),
        )

        verified, rejected = verify_claims(extraction, pool)
        trace.event(
            "quote_verification",
            section_id=spec.section_id,
            verified=[c.claim_id for c in verified],
            rejected=[
                {"claim_id": c.claim_id, "reason": c.reject_reason, "quote": c.quote}
                for c in rejected
            ],
        )

        analysis = analyse_section(spec, pool, verified, rejected, ctx.partition.provenance)
        trace.event(
            "analysis",
            section_id=spec.section_id,
            status=analysis.status,
            findings=[f.model_dump(mode="json") for f in analysis.findings],
            missing_elements=analysis.missing_elements,
        )
        trace.event("token_usage", **llm.usage.per_stage)

    print(render_analysis(analysis, ctx))
    print(llm.usage.summary(llm.model))
    print(f"trace written to {OUTPUT_DIR / 'trace.jsonl'}")

    if args.json:
        _write_json(args.json, analysis.model_dump_json(indent=2))

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
    p_part.set_defaults(func=cmd_partition)

    p_tpl = sub.add_parser(
        "template",
        help="Show the sections and required elements parsed from the SOW template.",
    )
    p_tpl.add_argument(
        "--json",
        nargs="?",
        const=str(OUTPUT_DIR / "template.json"),
        help="Also write the parsed sections as JSON.",
    )
    p_tpl.set_defaults(func=cmd_template)

    p_chunks = sub.add_parser("chunks", help="Show how documents were split into passages.")
    p_chunks.add_argument("--doc", help="Only show chunks whose doc_id contains this string.")
    p_chunks.set_defaults(func=cmd_chunks)

    p_ev = sub.add_parser(
        "evidence",
        help="Show the evidence pool assembled for one section.",
    )
    p_ev.add_argument("--section", type=int, required=True, help="Section number, 1-12.")
    p_ev.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=f"How many BM25 hits to select beyond the pinned set (default {DEFAULT_TOP_K}).",
    )
    p_ev.add_argument("--quiet", action="store_true", help="Omit chunk text.")
    p_ev.add_argument(
        "--tripwire",
        action="store_true",
        help="Also print the derived contamination tripwire terms.",
    )
    p_ev.add_argument(
        "--json",
        nargs="?",
        const=str(OUTPUT_DIR / "evidence.json"),
        help="Also write the pool as JSON.",
    )
    p_ev.set_defaults(func=cmd_evidence)

    p_an = sub.add_parser(
        "analyze",
        help="Extract claims for one section, verify quotes, and detect conflicts.",
    )
    p_an.add_argument("--section", type=int, required=True, help="Section number, 1-12.")
    p_an.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help="BM25 hits to select.")
    p_an.add_argument(
        "--tamper-quotes",
        action="store_true",
        help=(
            "Corrupt one returned quote before verification, to demonstrate that the "
            "verifier rejects any quote that is not a verbatim substring of its passage."
        ),
    )
    p_an.add_argument(
        "--json",
        nargs="?",
        const=str(OUTPUT_DIR / "analysis.json"),
        help="Also write the analysis as JSON.",
    )
    p_an.set_defaults(func=cmd_analyze)

    for sub_parser in (p_part, p_tpl, p_chunks, p_ev, p_an):
        sub_parser.add_argument("--data", help="Override the data directory.")
        sub_parser.add_argument("--roster", help="Override the engagement roster TOML.")

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Configuration errors fail loudly with a non-zero exit."""
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (ConfigError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
