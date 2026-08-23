# Transcript index

Topic index for [`session-01.md`](session-01.md) — 4,332 lines, one Claude Code
session covering the whole build, from first commit to final test run.

Kept as a separate file on purpose: every reference below is a line number into
the transcript, and prepending an index would shift all of them.

**How to jump.** `sed -n '760,812p' ai_transcripts/session-01.md`, or `:760` in
an editor.

---

## 1. Session at a glance

| Phase | Lines | What happens |
| --- | --- | --- |
| Corpus analysis | 15–759 | Read all 26 documents, map them, verify the map against sources |
| Architecture | 760–1345 | Design proposed, two decisions challenged and changed |
| Build CP1–CP6 | 1346–4287 | Six checkpoints, each run and reviewed before the next |
| Wrap-up | 4288–4332 | Final commit, submission note |

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
| 3260 | **CP4** — draft and validate, all 12 sections, end to end *(restored)* |
| 3367 | OpenAI account unfunded → switch back to Anthropic |
| 3833 | CP5 — review CLI and terminal states |
| 4140 | CP6 — tests, golden run, README |
| 4288 | `commit code` — final |

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
| 3727 | Cross-section check compared raw phrasings, not resolved winners — one UAT window read as seven values |
| 3801 | Only **3 of 12** sections passed validation first try; all failures `uncited_assertion` |
| 4066 | Scripted rejection looped forever — **810 MB of trace** before it was killed |

---

## 6. Infrastructure and credentials

| Line | Event |
| --- | --- |
| 3267 | OpenAI `insufficient_quota` |
| 3367 | Switch back to Anthropic; dual-provider client |
| 3969 | Anthropic credit exhausted mid-build |
| — | `.env` was never loaded at all; then a stale exported key shadowed the working one in `.env` |

---

## 7. Results

| Line | Result |
| --- | --- |
| 895, 1350, 1715 | Corpus partition: **20 admitted / 6 blocked**, zero ambiguous |
| 1111 | `rejected_unsatisfiable` introduced as a real terminal state |
| 3787 | Real run: **36 calls, 244,475 tokens, ~USD 2.93** |
| 4171 | Draft audit passes: **196 citations** across 12 sections |
| 4185 | **101 tests pass**, no API key, no network |

---

## 8. Known gaps in this transcript

Stated because the export is evidence, and an incomplete one should not look
complete.

- **One turn was restored.** The CP4 request and the first part of its response
  were dropped by the context compaction at line 3250 and have been restored
  from the session, marked with a `RESTORED` banner at line 3252. Content is
  accurate; the banner is there so the file does not present reconstructed text
  as raw export output.
- **One turn is still missing, deliberately.** A short exchange about whether to
  use an OpenAI key was also lost to that compaction and has been left out. Its
  outcome — the switch to OpenAI and back again — is visible from line 3267.
- **The export is compacted throughout.** Nine `※ recap:` markers appear where
  context was summarised, and tool output is collapsed to
  `Ran N shell commands (ctrl+o to expand)`, so command output and file diffs
  are largely absent.
- **The session continues past the export.** The submission note was drafted
  after `/export` at line 4331 and is not in the file.

A second `/export` after the final turn would close the last gap.
