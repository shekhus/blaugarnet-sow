# The SOW Drafter, explained

A walkthrough of what this project was asked to do, why it was harder than it
looks, how it works, and where it still falls short.

---

## 1. The problem

Blaugarnet is a software services firm. Before starting work for a client they
write a **Statement of Work** — the contract-like document that says what will be
built, by when, for how much, who does what, and how the client signs it off.

Writing one is slow and mostly clerical. All the facts already exist, but they
are scattered across call transcripts, emails, chat logs, scribbled notes and
signed contracts. Someone has to read all of it and assemble the document.

The task: **build a system that drafts the Statement of Work for one client —
Harding Outfitters — automatically, from a folder of 26 company documents.**

But with five conditions attached, and these are the real assignment:

| # | Condition | In plain words |
|---|---|---|
| 1 | Every claim cites its source | Not "per the notes" — a real pointer: which file, which lines, and the exact sentence it came from. |
| 2 | Conflicts must be caught **by code** | Where documents disagree, the system must notice *by itself, while running*. A human spotting it afterwards doesn't count. |
| 3 | A trace is logged | For each section: what was retrieved, what was sent to the AI, what came back, what was flagged. |
| 4 | A human approves each section | Approve, or reject with a comment — and a rejected section is rewritten using that comment. |
| 5 | It must run from a cold clone | Someone else downloads it, sets one API key, and it works. No manual fixing. |

Plus: report roughly how many tokens a draft costs, and include at least one
automated quality check written as a test.

**The thing to notice about condition 2.** The obvious way to build this is
"stuff the documents into an AI and ask for a SOW." That would produce something
that *looks* right. The conditions are designed to make that fail — because a
plausible-looking contract with a silently invented delivery date is worse than
no contract at all.

---

## 2. Why this is harder than it looks

The 26 documents in `data/` are a trap, deliberately built. Three things make
the naive approach dangerous.

### Only 9 of the 26 documents are about Harding

The rest are company policies, an *executed SOW for a different client*
(Northgate Logistics), a third client's sales notes (Atlas Retail), and internal
noise like the leave policy.

### The wrong client's numbers look exactly like the right client's numbers

Northgate's signed SOW contains **"blended USD 105/hour"** — stated as settled
fact, in a real signed contract, in the same document template.

The same figure appears in a Harding call, where someone says it and then
**takes it back in the same breath** — the correction sits a few words after the
number.

An AI searching for "what rate do we charge Harding?" finds both. One is a
confident number in a signed contract; the other is a retracted slip. Simple
text-similarity search cannot tell them apart — and picking the wrong one puts
another client's pricing into Harding's contract.

### The documents disagree with each other, and not all documents are equal

The go-live date is `2026-12-11` in three documents and `2027-01-15` in three
others. Payment terms are net 30 in one place and net 45 in the signed MSA.

You cannot just take the most recent answer. The newest document might be an
internal note marked **"not for client distribution"** where the team is
discussing what they'd *like* to negotiate. Sorting by date would take the
company's private negotiating position and print it in a document sent to the
client.

**So the real problem is not "write a document." It is: keep the wrong facts
out, and be honest about the ones that are genuinely unknown.**

---

## 3. The core idea

One sentence:

> **The AI is allowed to write sentences. It is never allowed to decide what is
> true.**

Everything that involves judgement — which documents count, which source wins
when two disagree, whether something is missing, whether a citation is real — is
done by ordinary code with fixed rules. The AI does two narrow jobs: pull facts
out of a passage, and turn approved facts into readable prose.

This matters because of an asymmetry: if you *ask* a model to behave, it usually
does, and occasionally it doesn't, and you find out later. If the code makes a
mistake impossible, it is impossible every time.

---

## 4. How it works, step by step

Thirteen stages. **Only two of them call the AI.**

### Stages 1–3: decide which documents are even allowed to be used

Each document is labelled with the client it is *about*, before anything else
happens. Documents belonging to another client are **removed from the search
index entirely** — not ranked lower, not discouraged. Absent.

Northgate's $105/hour cannot end up in Harding's pricing section, because no
part of that file can be found or quoted by any section. It's not unlikely.
It's impossible.

**How does it label them?** Two independent, dumb signals: the document's title
and its filename. **They must agree.** If they disagree, or a document mentions
two clients, or has no title, it is marked `AMBIGUOUS` — and ambiguous
documents are **excluded**. When unsure, the system locks the door.

There's a nice detail here. The Harding chat log *mentions Northgate by name* in
one message. Anything that classified documents by scanning their body text
would misfile it and throw away a genuine Harding source. Because only the title
and filename get a vote, the chat log stays.

The result is printed on every run:

```text
by label:   atlas 2  company 11  harding 9  helios 1  northgate 3
admitted:   20    excluded: 6    total: 26

EXCLUDED FROM EVIDENCE (cannot be retrieved or cited by any section):
  docs/northgate_sow_executed.md
      belongs to another engagement 'northgate' -- title and filename agree
  ...
```

### Stages 4–5: cut documents into quotable pieces

Documents are split along their natural seams — one piece per speaker turn, chat
message, email, bullet or table row.

Why not fixed-size chunks? Because the retraction lives *inside* a single
speaker turn. Cut it in the middle and you hand the $105 figure downstream with
its correction detached. **The correction must travel with the claim.**

### Stage 6: read the template as a checklist

The blank SOW template has guidance under each heading. Section 12 says:

> *"How deliverables are accepted, **by whom**, and within what window."*

The system parses that sentence into three things it must find: a mechanism, a
person, and a window. It doesn't work from a hand-written list of what to look
for, because a hand-written list only ever finds the gaps someone anticipated.

### Stage 7: gather evidence for each section

For each of the 12 sections, collect the relevant passages using keyword search
(BM25 — a standard, boring ranking formula, hand-written in about 40 lines with
no external libraries).

Two additions, both found by looking at what went wrong:

- **Always include the governing contracts**, whether or not keywords match. The
  MSA sets payment at net 45 without ever using the word "commercials" — keyword
  search would never find it, and it's the clause that overrides everything.
- **Always pull in neighbouring messages** in conversations. A short reply like
  *"we don't — i misspoke on the call"* scores almost nothing on its own, so
  ranking kept finding claims and dropping their retractions.

### Stage 8 — *AI* — pull facts out

The AI reads the passages and extracts individual facts, each with the exact
quote it came from and a label like `go_live_date`.

It is explicitly told **never to resolve a disagreement.** If one passage says
December and another says January, it returns *both*. If a passage states a
number and then withdraws it, it returns *both*.

### Stage 9: verify every quote

Code checks each quote is a **character-for-character match** of the source
lines. Anything else is thrown away. A quote the AI reworded is not a quote.

### Stage 10: decide who wins — the part that does the real work

Documents are ranked on **four separate scales**, not one score: what kind of
instrument it is, who it was written for, its status, and its date. An unsigned
addendum and an internal chat message aren't comparable on one number, and
squashing them into one is exactly what produces a naive "newest wins" system.

The rules, in order:

1. A **superseded** document can't support a claim. (It's still readable, so the
   draft can report what it used to say.)
2. **If one answer is supported only by internal chatter, and a competing answer
   has client-facing support, the disagreement does not resolve.** These aren't
   two readings of one body of evidence — one is what the client said, the other
   is what the company would like to negotiate.
3. Otherwise, the **strongest instrument** wins (a signed contract beats a chat
   message).
4. **Recency** only breaks ties between equals.
5. Anything left over is a conflict — rendered with *both* answers and both
   citations.

**Rule 2 is the one that earns its keep.** Buried in an internal file is an
instruction amounting to *"write it our way in the draft, we'll negotiate it
later."* Rule 2 keeps that out of a client-facing contract — and it was written
without knowing that sentence existed.

### Stage 11 — *AI* — write the prose

The AI receives **only the facts the rules resolved**, plus explicit
do-not-write lists of the contested and missing ones. It writes plain
paragraphs.

**The warnings are written by code, not the AI.** Conflict blocks, gap notices,
status banners and citation tables are generated from records. This means "every
problem is disclosed" is a property of the machinery, not an instruction the
model was asked to follow — *a model that ignores instructions still cannot
suppress a warning it never wrote.*

### Stage 12: five automatic gates

Every line of prose must carry a citation marker, no foreign client names, no
facts that weren't handed over, and so on. Failures trigger a rewrite, up to a
limit. A section that still fails is marked `unsupported` and **published
anyway, with its problems attached.**

That last point is deliberate: a run **always** produces a document. Problems
change how a section looks, never whether it exists. A corpus with something
genuinely unresolvable in it — as this one has — must still produce something a
human can work with.

### Stage 13: the human review step

```bash
sow review
```

Each section, one at a time: **approve**, or **reject with a comment**. A
rejection sends the section back to be rewritten *using your comment*. Every
decision, including your exact words, is appended to the log.

---

## 5. What you actually get

Four files. Here is real output.

**A cited paragraph** — every claim tagged, every tag resolving to a table with
the file, the line numbers and the verbatim quote:

> Production go-live is 2027-01-15 [C2], with the engagement beginning at
> kickoff on 2026-09-15 [C3].

| Ref | Source | Lines | Quote |
|---|---|---|---|
| C2 | `notes/harding_scope_addendum_v2.md` | 22 | *Production go-live: **2027-01-15*** |
| C3 | `notes/harding_scope_addendum_v2.md` | 20 | *Kickoff: 2026-09-15* |

**A conflict the system refused to settle** — from the pricing section:

> **UNRESOLVED — applicable_rate_card.** one value is supported only by internal
> documents while another has client-facing or standard support; the
> disagreement is unresolved between the parties, not merely between sources
>
> **Position A.** 2026 card for SOW use unless written exception
> Sources: `docs/blaugarnet_rate_card_2026.md` (policy; standard).
>
> **Position B — supported only by internal documents, not agreed with the
> client.** 2025 card, phase one only
> Sources: `chat/blaugarnet_harding_channel_export.md` (internal_chat).
>
> *Blaugarnet has not selected between these. Selecting either would assert an
> agreement the evidence does not establish.*

That last line is the whole project in one sentence.

**A caution about a fact that rests on an unsigned document:**

> **NOTE — go_live_date.** rests only on an instrument that is out for
> signature, not executed

**The other outputs:** `trace.jsonl` (one entry per event — what was retrieved,
sent, returned, rejected, flagged), `run.json` (the full structured run), and
`review_log.json` (the approve/reject decisions).

---

## 6. How we know it works

### The test suite — 105 tests, half a second, no API key

Because everything adjudicative is plain code, almost all of it can be tested
offline. A reviewer cloning the repo can run `pytest` before they have a key.

The tests cover the client boundary and its hard cases, document authority
including *where the rules must refuse to decide*, that no out-of-scope passage
reaches any section, quote verification, the five gates, and all four review
outcomes.

### The independent audit

```bash
sow audit
```

This re-reads `data/` from scratch, re-cuts it, and re-checks the finished
document — **trusting nothing the run recorded about itself.** A run that lied
to its own log would still be caught.

```text
DRAFT AUDIT
  PASS  citation_resolves      PASS  no_foreign_entity
  PASS  citation_in_scope      PASS  sections_complete
  PASS  quote_verbatim         PASS  findings_disclosed
  196 citations across 12 sections
  RESULT: PASS
```

And — this is the part worth pointing at — `test_audit.py` **proves each check
fails when it should**, by feeding the auditor a citation to Northgate's SOW, a
quote altered by a single word, a real quote attached to the wrong lines, and a
foreign client name in the prose. *A check that has never failed is not evidence
of anything.*

### What it costs

Measured on a real 12-section run:

| | |
|---|---|
| Model calls | 36 (12 extraction + 24 drafting, including 12 rewrites) |
| Total tokens | 244,475 |
| Estimated cost | ~USD 2.93 |

Two calls per section is the floor. Budget 150k–250k tokens for a clean run.

---

## 7. Where it falls short

Stated plainly, because a system like this is only worth what its known limits
are worth.

### It checks that citations are *real*, not that they're *right*

The audit proves every quote genuinely exists in the source. It does **not**
prove the sentence is a fair reading of that quote — that isn't decidable by
text matching, and asking a model to judge it would be as fallible as the thing
it's auditing.

**There is a live example of this in the current draft.** Section 12 says:

> This SOW names the client-side acceptance authority [C4].

C4 is a real, verbatim quote — from the internal sales playbook:

> *"5. Every SOW names the client-side acceptance authority. Post-Helios, no
> exceptions."*

But that's a **rule saying every SOW must name one**. It has been read as a
statement that this SOW *does* name one. **No name appears anywhere in the
corpus** — this is the single biggest genuine gap in the source documents, and
the draft currently states the opposite of the truth. Every automated check
passes, because the citation is real and the section is present.

### Relatedly, the gap detector reported nothing on the recorded run

All twelve sections recorded **zero** missing elements. The machinery works —
the template parser does extract *"by whom"* as a required element for section
12 — but on this run something was accepted as satisfying it. The most important
absence in the corpus was not flagged. **This is the first thing to fix.**

### Most sections needed a second attempt

Only **3 of 12** sections passed the gates first time. All 26 failures were the
same thing: an uncited line. The gate was right; the instructions to the model
were too vague about which lines need a marker. Rewrites cost roughly half the
drafting budget. *(The fix is now committed but not yet measured on a paid run —
see below.)*

### The offline replay isn't recorded yet

There's a mechanism to record a real run and replay it offline for free, so the
full pipeline can be tested without a key. It's built and proven end-to-end, but
the API accounts ran out of credit before it could be recorded, so two tests
skip. The other 105 are unaffected.

### Two smaller ones

**Fact labels aren't enforced.** Conflict detection relies on the AI using the
same label for the same fact across passages. It held on the real run, but
nothing forces it.

**Comparison is approximate.** The same date window written two ways can read as
two different positions and show up as a phantom disagreement.

---

## 8. If you only remember three things

1. **The AI writes; code decides.** Every judgement — which documents count, who
   wins a disagreement, whether a citation is real — is fixed code with fixed
   rules, testable offline without an API key.

2. **The client boundary is a locked door, not a preference.** Another client's
   signed contract isn't ranked lower, it's absent. That converts "should be
   fine" into "cannot happen."

3. **Refusing to answer is a feature.** Where the sources genuinely disagree,
   the draft shows both positions and says the company hasn't chosen. The
   failure mode of every naive version of this system is a confident, tidy,
   wrong document.

---

## 9. Where things live

| Path | What's there |
|---|---|
| `data/` | The 26 source documents and the blank template. Read-only. |
| `src/sow/` | The system. One file per stage — `admission.py` is the client boundary, `authority.py` the tie-break rules, `assemble.py` the disclosure rendering. |
| `tests/` | 105 offline tests. |
| `output/` | The draft, the trace, the run record, the review log. |
| `README.md` | The full technical version of this document. |
| `CLAUDE.md` | Notes on the source corpus, and a by-hand list of the conflicts to measure the detector against. |

```bash
pytest                    # 105 tests, no key needed
sow partition --verbose   # which documents count, and why — no key needed
sow draft                 # write the draft
sow audit                 # independently re-verify it
sow review                # approve / reject each section
```
