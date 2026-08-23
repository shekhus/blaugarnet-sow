# Transcript index

Topic index for [`ai_transcripts.md`](ai_transcripts.md) — 4,290 lines, one
Claude Code session covering the whole build.

Kept as a separate file on purpose: every reference below is a line number into
the transcript, and prepending an index would shift all of them.

**How to jump.** `sed -n '760,812p' ai_transcripts.md`, or `:760` in an editor.

---

## 1. Session at a glance

| Phase | Lines | What happens |
| --- | --- | --- |
| Corpus analysis | 15–759 | Read all 26 documents, map them, verify the map against sources |
| Architecture | 760–1345 | Design proposed, two decisions challenged and changed |
| Build CP1–CP6 | 1346–4245 | Six checkpoints, each run and reviewed before the next |
| Wrap-up | 4246–4290 | Final commit, submission note |

Six checkpoint commits plus two course corrections; `git log --oneline` in the
repo lines up with the phases above.

---

## 2. Turn-by-turn

| Line | Turn |
| --- | --- |
| 15 | `commit code` — initial corpus commit |
| 46 | Read CLAUDE.md, map every document under `data/` |
| 178 | CLAUDE.md added; full 26-document map delivered |
| 610 | **Verify the map** — exact quotes demanded before acceptance |
| 707 | Fold a condensed map into CLAUDE.md `## Source notes` |
| 760 | **Propose the architecture** |
| 813 | BM25 chosen; three-label correction issued |
| 1170 | Two decisions: mock-based tests; **invert the cross-section gate** |
| 1346 | Build in six checkpoints — CP1 delivered |
| 1777 | CP2 — chunking, template parse, BM25, evidence assembly |
| 2711 | CP3 — claim extraction, quote verification, analysis |
| 3325 | OpenAI account unfunded → switch back to Anthropic |
| 3791 | CP5 — review CLI and terminal states |
| 4098 | CP6 — tests, golden run, README |
| 4246 | `commit code` — final |

---

## 3. Design decisions and where they were argued

| Line | Decision |
| --- | --- |
| 760 | Architecture proposal: pipeline stages, data structures, section schema |
| 813 | **Embeddings rejected.** A similarity score can only make another client's rate *unlikely*; a boundary makes it impossible |
| 813 | **Whole-corpus-in-context rejected.** Maximises recall but turns the engagement boundary from a code invariant into a model instruction |
| 813 | **Binary engagement label rejected** — would have excluded the rate cards the SOW needs. Three labels required, subject decided by title not body |
| 886 | Ambiguity must resolve to exclusion, never admission |
| 1170 | **Cross-section gate inverted** — gate silent resolution, never the artifact, or this corpus yields no draft at all |
| 1170 | Tests run offline against a committed golden run |
| 1207 | Worked example: what §6 Governance looks like when the conflict fires |
| 1242 | Both positions rendered with provenance; neither selected |

---

## 4. Corpus analysis

| Line | Topic |
| --- | --- |
| 910 | Helios post-mortem excluded — the accepted cost, flagged for sign-off |
| 184 | The C1–C12 conflict list kept as a **recall fixture**, never detector input |
| 340 | The retracted blended rate, inside a single speaker turn |
| 345 | Chat correction: "was looking at the northgate sheet" |
| 371 | Sales playbook: "the executed MSA always wins" |
| 790 | Section 12's "by whom" derived from the template at run time |
| 548 | Acceptance authority: the gap nothing in the corpus fills |
| 854 | Tripwire's own limit: it cannot catch "Northgate" or "105" |
| 610–706 | Verification pass: every claim quoted with file and line |

---

## 5. Bugs found, and how

Live runs and inspection found things reading the code did not.

| Line | Bug |
| --- | --- |
| 371 | Header scanning read the playbook's own text and labelled it `executed` |
| 2258 | Contamination tripwire fired on `Milestones` / `Objectives` — the template's own section headings |
| 2439 | **No stemming**: query `rates` never matched `Hourly rate`, so §8 was assembled with the deal-note rules but no actual rates |
| 2502 | Short replies carry corrections but score nothing alone — adjacent turns pulled in |
| 3685 | Cross-section check compared raw phrasings, not resolved winners — one UAT window read as seven values |
| 3759 | Only **3 of 12** sections passed validation first try; all failures `uncited_assertion` |
| 4024 | Scripted rejection looped forever — **810 MB of trace** before it was killed |

---

## 6. Infrastructure and credentials

| Line | Event |
| --- | --- |
| 3287 | OpenAI `insufficient_quota` |
| 3325 | Switch back to Anthropic; dual-provider client |
| 3927 | Anthropic credit exhausted mid-build |
| — | `.env` was never loaded at all; then a stale exported key shadowed the working one in `.env` |

---

## 7. Results

| Line | Result |
| --- | --- |
| 895, 1350, 1715 | Corpus partition: **20 admitted / 6 blocked**, zero ambiguous |
| 1111 | `rejected_unsatisfiable` introduced as a real terminal state |
| 3745 | Real run: **36 calls, 244,475 tokens, ~USD 2.93** |
| 4129 | Draft audit passes: **196 citations** across 12 sections |
| 4143 | **101 tests pass**, no API key, no network |

---

## 8. Known gaps in this transcript

Stated because the export is evidence, and an incomplete one should not look
complete.

- **Two turns are missing.** The question about whether to use an OpenAI key,
  and the CP4 request (draft and validate, all 12 sections). The work they
  produced is present; the prompts are not.
- **The export is compacted.** It ends with a `※ recap:` line, and tool output
  is collapsed to `Ran N shell commands (ctrl+o to expand)` rather than shown in
  full, so command output and file diffs are largely absent.
- **The session continues past the export.** The submission note was drafted
  after `/export` at line 4289 and is not in the file.

A second `/export` after the final turn would close the last gap; recovering the
two missing prompts would need the raw session log rather than the rendered
export.
