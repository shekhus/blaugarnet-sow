"""End-to-end run: stages 7-12 across every section.

Section order is the template's own. Each section is retrieved, extracted,
verified, analysed, drafted and validated independently; the cross-section
check runs once at the end, over the claims all sections produced.

A run always writes ``output/sow_draft.md``. Findings change how a section
renders, never whether it renders, and a validation failure that survives its
redrafts marks the section unsupported and writes it with its issues attached.
A run that ends without a draft file is a failed run.
"""

from __future__ import annotations

from pathlib import Path

from .analysis import analyse_section
from .assemble import (
    build_open_questions,
    cross_section_check,
    render_document,
    section_status,
)
from .claims import STAGE as EXTRACT_STAGE
from .claims import SYSTEM_PROMPT as EXTRACT_SYSTEM
from .claims import build_user_prompt as build_extract_prompt
from .claims import verify_claims
from .draft import STAGE as DRAFT_STAGE
from .draft import SYSTEM_PROMPT as DRAFT_SYSTEM
from .draft import assertable_claims, build_citations
from .draft import build_user_prompt as build_draft_prompt
from .draft import used_citations
from .evidence import DEFAULT_TOP_K, assemble_pool
from .llm import LlmClient
from .models import (
    ClaimExtraction,
    DraftedSection,
    DraftRun,
    SectionAnalysis,
    SectionDraft,
    SectionSpec,
)
from .pipeline import RunContext
from .trace import Trace
from .validate import MAX_REVISIONS, redraft_instruction, validate_section


def run_draft(
    ctx: RunContext,
    llm: LlmClient,
    output_dir: Path,
    section_ids: list[int] | None = None,
    top_k: int = DEFAULT_TOP_K,
    max_revisions: int = MAX_REVISIONS,
    verbose: bool = True,
) -> DraftRun:
    """Draft every requested section and write the document, trace and records."""
    specs = [s for s in ctx.sections if section_ids is None or s.section_id in section_ids]
    if not specs:
        raise ValueError(f"no template sections matched {section_ids}")

    output_dir.mkdir(parents=True, exist_ok=True)
    admitted_doc_ids = {d.doc_id for d in ctx.partition.admitted}
    drafts: list[SectionDraft] = []
    analyses: list[SectionAnalysis] = []

    with Trace(output_dir / "trace.jsonl") as trace:
        trace.event(
            "run_start",
            model=llm.model,
            backend=llm.backend,
            sections=[s.section_id for s in specs],
        )
        trace.event(
            "partition",
            admitted=sorted(admitted_doc_ids),
            excluded=[d.doc_id for d in ctx.partition.excluded],
            tripwire_terms=ctx.tripwire_terms,
        )

        for spec in specs:
            if verbose:
                print(f"  section {spec.section_id:>2}. {spec.title} ...", flush=True)
            draft, analysis = _run_section(
                spec, ctx, llm, trace, admitted_doc_ids, top_k, max_revisions, verbose
            )
            drafts.append(draft)
            analyses.append(analysis)

        cross_issues = cross_section_check(analyses, ctx.partition.provenance)
        for issue in cross_issues:
            for draft in drafts:
                if draft.section_id in issue.section_ids and draft.status == "drafted":
                    draft.status = "conflict"
        trace.event(
            "cross_section_check",
            issues=[i.model_dump(mode="json") for i in cross_issues],
        )

        open_questions = build_open_questions(drafts)
        run = DraftRun(
            sections=drafts,
            open_questions=open_questions,
            cross_section_issues=cross_issues,
            model=llm.model,
            token_usage={
                "calls": llm.usage.calls,
                "input_tokens": llm.usage.input_tokens,
                "output_tokens": llm.usage.output_tokens,
                "per_stage": llm.usage.per_stage,
            },
        )

        document = render_document(run, ctx.roster.target)
        (output_dir / "sow_draft.md").write_text(document, encoding="utf-8")
        (output_dir / "run.json").write_text(run.model_dump_json(indent=2), encoding="utf-8")

        trace.event(
            "run_end",
            sections=len(drafts),
            open_questions=len(open_questions),
            token_usage=run.token_usage,
            draft_bytes=len(document),
        )

    return run


def _run_section(
    spec: SectionSpec,
    ctx: RunContext,
    llm: LlmClient,
    trace: Trace,
    admitted_doc_ids: set[str],
    top_k: int,
    max_revisions: int,
    verbose: bool,
) -> tuple[SectionDraft, SectionAnalysis]:
    """Retrieve, extract, verify, analyse, draft and validate one section."""
    provs = ctx.partition.provenance
    pool = assemble_pool(spec, ctx.evidence, top_k=top_k)
    trace.event(
        "evidence_pool",
        section_id=spec.section_id,
        query=pool.query,
        selected=[
            {"chunk_id": s.chunk.chunk_id, "selector": s.selector, "score": s.score}
            for s in pool.selected
        ],
        excluded_chunks=pool.excluded_chunks,
    )

    extract_user = build_extract_prompt(spec, pool)
    extraction = llm.parse(EXTRACT_STAGE, EXTRACT_SYSTEM, extract_user, ClaimExtraction)
    verified, rejected = verify_claims(extraction, pool)
    trace.event(
        "claim_extraction",
        section_id=spec.section_id,
        prompt_chars=len(extract_user),
        raw_claims=len(extraction.claims),
        verified=len(verified),
        rejected=[
            {"claim_id": c.claim_id, "reason": c.reject_reason, "quote": c.quote}
            for c in rejected
        ],
    )

    analysis = analyse_section(spec, pool, verified, rejected, provs)
    trace.event(
        "analysis",
        section_id=spec.section_id,
        status=analysis.status,
        findings=[f.model_dump(mode="json") for f in analysis.findings],
        missing_elements=analysis.missing_elements,
    )

    allowed, contested = assertable_claims(verified, provs)
    citations, by_chunk = build_citations(allowed, pool, provs)
    draft_user = build_draft_prompt(
        spec, allowed, by_chunk, contested, analysis.missing_elements, analysis.findings
    )

    drafted = DraftedSection(body_markdown="", drafting_notes=[])
    issues = []
    revision = 0

    if allowed:
        for attempt in range(max_revisions + 1):
            revision = attempt
            prompt = draft_user if attempt == 0 else f"{draft_user}\n\n{redraft_instruction(issues)}"
            drafted = llm.parse(DRAFT_STAGE, DRAFT_SYSTEM, prompt, DraftedSection)
            issues = validate_section(
                drafted, citations, admitted_doc_ids, ctx.tripwire_terms, expect_prose=True
            )
            trace.event(
                "validation",
                section_id=spec.section_id,
                revision=attempt,
                passed=not issues,
                issues=[i.model_dump(mode="json") for i in issues],
            )
            if not issues:
                break
            if verbose:
                print(
                    f"      revision {attempt + 1}: {len(issues)} gate failure(s), redrafting",
                    flush=True,
                )

    status = section_status(analysis, unsupported=bool(issues))
    draft = SectionDraft(
        section_id=spec.section_id,
        title=spec.title,
        status=status,
        body_markdown=drafted.body_markdown,
        citations=used_citations(drafted, citations),
        findings=analysis.findings,
        missing_elements=analysis.missing_elements,
        issues=issues,
        revision=revision,
    )
    trace.event(
        "section_drafted",
        section_id=spec.section_id,
        status=status,
        revision=revision,
        citations=[c.marker for c in draft.citations],
        body_chars=len(draft.body_markdown),
        drafting_notes=drafted.drafting_notes,
    )
    return draft, analysis
