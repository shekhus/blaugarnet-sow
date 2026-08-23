# Blaugarnet SOW Drafter

Drafts a Statement of Work for the **Harding Outfitters** engagement from the
documents in `data/`, following `data/sow_template.md`, with a human approval
step.

Every substantive statement in the draft carries a citation that resolves to a
document, a line range and a verbatim quote. Where the sources disagree, or
where the template requires something no source supplies, the draft says so
rather than guessing.

---

## Quick start

```bash
python -m venv .venv && . .venv/Scripts/activate    # or bin/activate
pip install -e ".[llm,dev]"

pytest                                   # 101 tests, no API key needed

cp .env.example .env                     # add ANTHROPIC_API_KEY (or OPENAI_API_KEY)
sow draft                                # writes output/sow_draft.md
sow audit                                # re-verifies it; exits non-zero on failure
sow review                               # approve / reject each section
```

Stages 1–7 need no key at all:

```bash
sow partition --verbose     # which documents are evidence, and why
sow template                # sections and required elements parsed from the template
sow chunks --doc scoping    # how a document was split into citable passages
sow evidence --section 8    # the pool section 8 may draw on, with BM25 scores
```

**Key handling.** `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`, read from the
environment; `.env` is gitignored and `.env.example` is committed. Values in
`.env` **override** an exported shell variable of the same name — the reverse of
the usual convention, and deliberate, because a stale exported key silently
shadowing a freshly pasted one produces the worst possible symptom. The override
is announced on stderr.

---

## The problem this corpus actually poses

Only **9 of 26 documents concern Harding**. The rest are company policy, another
client's executed SOW, a third client's pursuit notes, and internal material
with no bearing on the engagement. Three properties make naive retrieval unsafe:

- Northgate's executed SOW states a **blended USD 105/hour**. The same figure
  appears in a Harding transcript — spoken, then retracted in the same sentence.
  A similarity score cannot tell those apart.
- The Harding chat export **names Northgate** in a message, so anything that
  classifies documents by their body text will misfile it.
- The facts a SOW needs are spread across instruments of very different
  authority: an executed MSA, an unsigned addendum, a superseded addendum, a
  client meeting, and an internal note marked *not for client distribution*.
  Sorting by recency puts the internal note's negotiating posture into a
  client-facing contract.

---

## Design choices

### The engagement boundary is a hard filter, not a ranking signal

Each document is labelled with the engagement it is *about*, before retrieval
runs. Documents belonging to another client are **absent from the index**, not
down-weighted. Northgate's blended rate cannot reach section 8 because no chunk
of that document is retrievable or citable from any section.

The label comes from two independent deterministic signals — the **H1 title**
and the **filename stem** — which must agree. Scoping the subject signal to the
title is what lets the chat export stay admitted despite naming Northgate: body
text gets no vote. Disagreement, a multi-client subject, or a missing title
yields `AMBIGUOUS`, and **`AMBIGUOUS` is excluded**. The failure mode is
exclusion, never admission on the benefit of the doubt.

`config/engagements.toml` declares only *who the clients are*. It declares
nothing about scope, rates, dates or conflicts. `tests/test_admission.py` pins
the resulting partition, so a roster edit that widens what the draft may cite
fails the suite.

### Retrieval: BM25, and why not the alternatives

**Embeddings were rejected.** At ~34 KB the whole corpus fits in a single
context window, so embeddings buy no recall here, while adding a dependency, a
network round-trip and run-to-run nondeterminism. The decisive reason is
narrower: a similarity score can only make another client's document *unlikely*.
A boundary makes it *impossible*. Determinism also means the recall tests run
offline in CI with no key.

**Whole-corpus-in-context was rejected** — and it is the more interesting
rejection, because it maximises recall. Passing every admitted document to every
section would guarantee nothing is missed. But it converts the engagement
boundary from a **code invariant** into a **model instruction**: the wrong
client's SOW would be in the context window, and only a prompt would stand
between it and section 8. This corpus is built to punish exactly that. It also
costs roughly 4× the tokens per run and leaves no retrieval story to evaluate.

BM25 is hand-rolled (~40 lines, zero dependencies). Two selectors feed each
section's pool: **pinned** chunks from the governing instruments (the executed
MSA and the current addendum) are always present, because lexical retrieval is
good at finding passages sharing a section's vocabulary and bad at finding the
one contractual clause that silently overrides it — the MSA states net 45
without ever using the word "commercials". **Retrieved** chunks come from BM25
over what survived the boundary.

Two refinements came from inspecting the section 8 pool, which is where
contamination would surface:

- Retrieval indexes **document title and heading path alongside chunk text**.
  Ranking body text alone buried both rate tables, whose contents are numbers.
- **Plural stemming only.** Without it the query term `rates` never matched the
  card's `Hourly rate` header, and section 8 was assembled with the deal-note
  rules but no actual rates. A fuller stemmer would conflate terms this corpus
  keeps distinct.
- **Neighbouring turns** are pulled in for conversational documents. A short
  reply carries the correction — *"we don't — i misspoke on the call, was
  looking at the northgate sheet"* — but scores almost nothing alone, so lexical
  ranking kept finding claims and dropping their retractions.

### Chunking follows document structure

One chunk per speaker turn, chat message, email, list item or table. A citation
must land on a passage a reader can check, and the scoping call's retraction
lives *inside* one turn — splitting it would hand the figure downstream with the
correction detached. `Chunk.text` is verbatim source, so quote verification is
exact substring matching.

### Authority is a partial order that is allowed to decline

Provenance is parsed from header lines that already exist in the corpus
(`**Status:** out for signature`, `**Version 2 · Supersedes v1**`, `**not for
client distribution**`), and each field retains the line it came from, so a
provenance decision is itself citable. Authority is kept as **orthogonal axes** —
instrument, audience, status, date — because an unsigned addendum and an
internal chat message are not comparable on a single scale, and collapsing them
to a number is precisely what produces a recency-only resolver.

The resolution rules, in order:

1. A **superseded** document cannot support an assertion. It stays retrievable
   so the draft can report what it said.
2. If one value is supported **only by internal deliberation** and a competing
   value has client-facing or standard support, the disagreement **does not
   resolve**. Those are not rival readings of one body of evidence — one is what
   the client stated, the other is what Blaugarnet would like to negotiate.
3. Otherwise the **strongest instrument** wins.
4. **Recency** breaks ties only among equals.
5. Anything else is a conflict, rendered with both values and their citations.

Rule 2 is what keeps *"write it my way in the draft, we'll negotiate"* out of a
client-facing SOW — and it is written without knowing that sentence exists.

A third audience class, `standard`, exists because two would have barred the
rate cards from solely supporting anything, and rates exist *only* on the cards.

### Conflict detection is comparison, not recognition

The model extracts claims and is told explicitly **never to resolve a
disagreement**: two passages with different values yield two claims under one
`fact_key`; a passage that states a value then withdraws it yields both. Code
groups by key, normalises, and compares. Nothing in the detector knows which
facts are contested in this corpus, so an unanticipated disagreement surfaces
the same way as an anticipated one.

Normalisation is deliberately conservative — dates unified, thousands
separators dropped, hedges removed. Over-normalising merges values that
genuinely differ; under-normalising invents conflicts out of phrasing.

### Insufficiency comes from the template

The guidance prose under each template heading is a checklist. Section 12 reads
*"How deliverables are accepted, by whom, and within what window"* and yields
three required elements — and **"by whom"** is the one nothing in the corpus
satisfies. Parsing that at run time is what makes the check evidence-led; a
hand-written list of things to look for would only ever find anticipated gaps.

### The model writes prose; code writes the disclosures

Status banners, conflict blocks, gap notices and citation tables are rendered
from `Finding` records by `assemble.py`. The model receives only claims the
authority policy **resolved**, with contested keys and missing elements passed
in as explicit do-not-write lists. "Every finding is surfaced" is therefore a
structural property of the assembler, not an instruction the model is asked to
follow — a model that ignores instructions cannot suppress a disclosure it never
wrote.

### Findings never withhold the artifact

A run **always** writes `output/sow_draft.md`. Findings change how a section
renders, never whether it renders. A section that fails validation after its
redrafts is marked `unsupported` and written anyway with its issues attached.
The cross-section consistency check gates **silent resolution**, not the
document: where two sections settled one fact differently, both readings are
disclosed and both sections marked contested. A corpus containing something
genuinely unresolvable — as this one does — must still produce a document.

---

## Assumptions

1. **The engagement roster is configuration.** `config/engagements.toml` lists
   the clients; a real deployment would read a CRM. It encodes no answers.
2. **`data/` is read-only** and its markdown conventions are stable — an H1 per
   document, `**Key:** value` header fields, speaker turns as `**Name:**`.
3. **Addendum v2 is unsigned** and treated as such: claims resting solely on it
   are marked provisional rather than asserted flatly.
4. **The Helios post-mortem is another client's engagement document** and is
   excluded. This is an accepted cost, stated because it is a real loss: the
   rules it justifies survive independently in the sales playbook, which is
   company-wide and admitted. Exclusion costs rationale, not requirements.
5. **Groundedness is checked as provenance, not entailment.** Whether a sentence
   is logically entailed by its quote is not decidable by string matching, and a
   model-scored judgement would be as fallible as the thing it audits.
6. **Section 10 is a rollup.** Disclosed findings from every section are
   numbered `OQ-n` there and referenced from the sections they came from.
7. **One draft per run.** No incremental re-drafting of a subset except through
   `--sections` or the review loop.

---

## How I judge whether a draft is good

In descending order of what a failure would cost:

| # | Property | How it is checked |
|---|---|---|
| 1 | **No cross-engagement contamination** | Every citation resolves to an admitted document. Structural and exact. |
| 2 | **Citations are real** | Every quote is still a verbatim substring of the lines it points at, re-read from `data/`. |
| 3 | **Nothing asserted without support** | Every assertive line carries a citation marker. |
| 4 | **Disagreements are visible, not resolved** | Every recorded conflict appears in the rendered text with both positions. |
| 5 | **Gaps are visible, not filled** | Every required element with no source is named as missing. |
| 6 | **Completeness** | All twelve template sections present. |

**What I deliberately do not measure.** Citation *coverage* as a headline number
is misleading here: it rewards sections that were easy and says nothing about
the ones that matter. A draft can hit 100% citation coverage and still ship a
SOW with no acceptance authority. Coverage is a floor gate; required-element
coverage and gap disclosure are the real signal.

### The automated check

`sow audit` (and `tests/test_audit.py`) re-reads `data/`, re-chunks it, and
re-verifies the finished markdown from scratch — trusting nothing the run
recorded about itself. A run that lied to its own trace would still fail.

```
DRAFT AUDIT
  PASS  citation_resolves      PASS  no_foreign_entity
  PASS  citation_in_scope      PASS  sections_complete
  PASS  quote_verbatim         PASS  findings_disclosed
  196 citations across 12 sections
  RESULT: PASS
```

`tests/test_audit.py` proves each check *fails* when it should, by feeding the
auditor a citation to Northgate's SOW, a quote altered by one word, a quote
attached to the wrong line range, and a foreign entity in prose.

### Test suite

**101 tests, ~0.5s, no API key.** Every test is deterministic; none imports a
provider SDK.

```
tests/test_admission.py   engagement boundary, the three hard cases, AMBIGUOUS paths
tests/test_provenance.py  header parsing, cross-document supersession, the traps
tests/test_template.py    required elements incl. section 12's "by whom"
tests/test_retrieval.py   no out-of-scope chunk in any pool; recall the pools must keep
tests/test_authority.py   the policy, including where it must decline to resolve
tests/test_analysis.py    conflict + insufficiency detection; quote verification
tests/test_validate.py    the five drafting gates
tests/test_review.py      all four review terminal states
tests/test_audit.py       the quality check, and that each check fails when it should
tests/test_golden_run.py  offline replay (skipped until fixtures are recorded)
```

The C-numbers in `test_analysis.py` reference the recall fixture in `CLAUDE.md`.
That list is a yardstick for what a careful human found by hand; **it is never
consulted by the detector.**

---

## Token usage

Measured on a real 12-section run, `claude-opus-5`:

| | |
|---|---|
| Model calls | **36** (12 extraction + 24 drafting, incl. 12 redrafts) |
| Input tokens | **158,864** |
| Output tokens | **85,611** |
| **Total** | **244,475** |
| Estimated cost | **~USD 2.93** |

Two calls per section is the floor: one extraction, one draft. Each validation
failure adds one more. On this run only 3 of 12 sections passed validation
first time, so redrafts account for roughly half the drafting spend — see
*Known weaknesses*. Budget **~150k–250k tokens** for a clean run and more if the
reviewer rejects sections.

---

## Verification

The corpus partition, printed on every run. This is the cheapest proof that the
engagement boundary works.

```
CORPUS PARTITION -- target engagement: harding
----------------------------------------------------------------------------------------------------
       ENGAGEMENT  INSTRUMENT             AUDIENCE       STATUS             DOCUMENT
----------------------------------------------------------------------------------------------------
PASS   harding     internal_chat          internal_only  current            chat/blaugarnet_harding_channel_export.md
PASS   company     policy                 standard       superseded         docs/blaugarnet_rate_card_2025.md
PASS   company     policy                 standard       current            docs/blaugarnet_rate_card_2026.md
PASS   harding     executed_contract      client_facing  executed           docs/harding_msa_summary.md
BLOCK  northgate   executed_sow           client_facing  executed           docs/northgate_sow_executed.md
PASS   harding     client_correspondence  client_facing  current            emails/harding_timeline_thread.md
BLOCK  northgate   client_correspondence  client_facing  current            emails/northgate_cutover_email.md
PASS   company     internal_meeting       internal_only  current            internal/blaugarnet_allhands_2026-07.md
PASS   company     policy                 standard       unknown            internal/blaugarnet_engineering_onboarding.md
PASS   company     policy                 standard       current            internal/blaugarnet_infosec_policy.md
PASS   company     policy                 standard       current            internal/blaugarnet_leave_policy.md
PASS   company     reference              standard       unknown            internal/blaugarnet_marketing_onepager.md
PASS   company     policy                 standard       unknown            internal/blaugarnet_qa_checklist_template.md
PASS   company     policy                 standard       current            internal/blaugarnet_sales_playbook_extract.md
PASS   company     policy                 standard       current            internal/blaugarnet_travel_expense_policy.md
BLOCK  helios      reference              standard       current            internal/helios_bank_postmortem.md
BLOCK  atlas       working_draft          internal_only  current            notes/atlas_retail_discovery_notes.md
BLOCK  atlas       reference              standard       current            notes/atlas_retail_status.md
PASS   harding     working_draft          internal_only  draft_incomplete   notes/harding_requirements_draft.md
PASS   harding     superseded_addendum    client_facing  superseded         notes/harding_scope_addendum_v1.md
PASS   harding     unsigned_addendum      client_facing  out_for_signature  notes/harding_scope_addendum_v2.md
PASS   company     template               standard       unknown            sow_template.md
BLOCK  northgate   client_meeting         client_facing  current            transcripts/2026-05-19_northgate_kickoff.md
PASS   harding     client_meeting         client_facing  current            transcripts/2026-07-10_harding_discovery_call.md
PASS   harding     client_meeting         client_facing  current            transcripts/2026-08-05_harding_scoping_call.md
PASS   harding     internal_meeting       internal_only  current            transcripts/2026-08-19_harding_kickoff_prep_internal.md
----------------------------------------------------------------------------------------------------
by label:   atlas 2  company 11  harding 9  helios 1  northgate 3
admitted:   20    excluded: 6    total: 26

EXCLUDED FROM EVIDENCE (cannot be retrieved or cited by any section):
  docs/northgate_sow_executed.md
      belongs to another engagement 'northgate' -- title and filename agree: names client 'northgate'
  emails/northgate_cutover_email.md
      belongs to another engagement 'northgate' -- title and filename agree: names client 'northgate'
  internal/helios_bank_postmortem.md
      belongs to another engagement 'helios' -- title and filename agree: names client 'helios'
  notes/atlas_retail_discovery_notes.md
      belongs to another engagement 'atlas' -- title and filename agree: names client 'atlas'
  notes/atlas_retail_status.md
      belongs to another engagement 'atlas' -- title and filename agree: names client 'atlas'
  transcripts/2026-05-19_northgate_kickoff.md
      belongs to another engagement 'northgate' -- title and filename agree: names client 'northgate'

NOTES (5):
  - notes/harding_scope_addendum_v1.md: marked superseded by notes/harding_scope_addendum_v2.md (v1 < v2)
  - internal/blaugarnet_engineering_onboarding.md: no date found; recency comparisons will skip it
  - internal/blaugarnet_marketing_onepager.md: no date found; recency comparisons will skip it
  - internal/blaugarnet_qa_checklist_template.md: no date found; recency comparisons will skip it
  - sow_template.md: no date found; recency comparisons will skip it
```

Note `harding_scope_addendum_v1.md` → `superseded`. v1 never says it is
superseded; only v2 says it supersedes v1. That is inferred across documents by
grouping on title and version number.

On the real run, the detector resolved `go_live_date` to **2027-01-15** and
`kickoff_date` to **2026-09-15** from evidence, and left change-request approval
authority unresolved with both positions rendered — which is correct: the
corpus records it as an open negotiation point.

---

## AI transcripts

`ai_transcripts/` holds the session this was built in.

- [`ai_transcripts/README.md`](ai_transcripts/README.md) — topic index: turn
  boundaries, where each design decision was argued, the bugs live runs found,
  and the measured results. Every entry is a line number into the transcript.
- [`ai_transcripts/session-01.md`](ai_transcripts/session-01.md) — the export,
  4,332 lines.

The index's final section records what the export is missing: one turn restored
after a context compaction dropped it (marked in place), one deliberately
omitted, and tool output collapsed throughout by the export itself.

---

## Pipeline

| # | Stage | Model? |
|---|---|---|
| 1–3 | ingest → provenance → **admission** (the engagement boundary) | no |
| 4–5 | structure-aware chunking → BM25 index + tripwire set | no |
| 6 | parse template into sections and required elements | no |
| 7 | per-section evidence pool: hard filter → pinned ∪ BM25 ∪ adjacent | no |
| 8 | claim extraction | **yes** |
| 9 | quote verification | no |
| 10 | authority policy → conflict + insufficiency findings | no |
| 11 | draft prose from resolved claims | **yes** |
| 12 | five validation gates → bounded redraft | no |
| 13 | review CLI: approve / reject-with-comment / redraft | no |
| — | assembly, cross-section check, audit | no |

Two model calls per section; everything adjudicative is code.

**Outputs.** `output/sow_draft.md`, `output/trace.jsonl` (one JSON object per
event: what was retrieved, what was sent, what came back, what was rejected,
what was flagged), `output/run.json`, `output/review_log.json`.

---

## Known weaknesses

**Uncited assertions on first draft.** On the real run only **3 of 12** sections
passed validation first time; all 26 gate failures were `uncited_assertion`.
Seven recovered on redraft, two exhausted their retries and shipped as
`unsupported`. The gate is doing its job, but the drafting prompt is too
permissive about what needs a marker. This is the highest-value single fix and
would cut roughly half the drafting tokens.

**The golden run is not recorded.** `sow draft --record` writes the fixtures and
`tests/test_golden_run.py` replays them offline, but the API accounts available
during development ran out of credit, so the fixtures are absent and those two
tests skip. The other 101 tests are deterministic and unaffected.

**Fact-key stability is the hinge.** Conflict detection depends on the model
using the same `fact_key` for the same fact across passages. It held on the real
run, but nothing enforces it; a canonicalisation pass over proposed keys would
make it robust.

**Value normalisation is approximate.** The same window written two ways can
read as two positions. The cross-section check now compares *resolved winners*
rather than raw claim text, which removed most of the noise, but within-section
phrasing variation can still split one position in two.

---

## Next steps with more time

1. Tighten the drafting prompt so first-pass validation clears; re-run and
   report before/after gate-failure counts.
2. Record the golden run and add a token-budget regression test.
3. Canonicalise `fact_key` values across sections before comparison.
4. Score conflict-detection recall against the C1–C12 fixture in `CLAUDE.md` as
   a reported metric.
5. A minimum-prose floor: when every fact in a section is contested, the section
   currently renders as pure disclosure with no prose at all.
