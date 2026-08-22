# Blaugarnet SOW Drafter

## What this is
Engineering exercise for Blaugarnet Inc. Build a system that drafts a Statement of
Work for the **Harding Outfitters** engagement from the company documents in `data/`,
following the SOW template in that folder, with a human approval step.

## Non-negotiable constraints (from the brief — these are what's graded)

1. **Every substantive claim in the draft cites the specific source passage it came
   from.** Not "per the discovery notes" — a resolvable pointer: document name +
   location/chunk id.
2. **Where sources are inconsistent or insufficient for a section, the system makes
   that visible rather than guessing.** This must be detected by code at run time.
   A conflict caught only because a human noticed it in the output does not count.
3. **A trace is logged showing how each section was assembled** — what was retrieved,
   what was sent to the model, what came back, what was flagged.
4. **A CLI review step**: reviewer approves or rejects each section with a comment;
   rejected sections are redrafted using that comment.
5. **The reviewers will clone this repo and run it themselves against the same
   `data/` folder.** It must work end-to-end, unassisted, from a cold clone with
   only an environment variable set. No manual steps, no hand-fixing output.
6. Approximate **token usage per draft run** is reported.
7. At least one **automated quality check**, implemented as a test.

## How I want you to work
- Read the files in `data/` yourself with your tools. Do not ask me to paste contents.
- Propose a plan before writing code for anything non-trivial. I will approve or push back.
- Small, verifiable steps. I read every diff before it lands.
- Prefer boring and dependency-light over clever — the reviewers must run this on a
  clean machine with no help from me.
- Deterministic checks in code beat asking the model to behave. If a rule can be
  enforced outside the model, enforce it outside the model.
- No silent fallbacks. If something cannot be done, fail loudly or flag it — never
  fill a gap with a plausible guess.
- Structured, validated output for anything the pipeline consumes downstream.
- If an assumption is needed, state it and keep moving. Assumptions get recorded in
  the README; do not stall to ask me.

## Layout
```
data/             source documents, unmodified, incl. the SOW template — READ ONLY
src/              the system
tests/            automated checks
output/           generated draft, trace, review log
ai_transcripts/   exported AI conversations (submission requirement)
README.md         assumptions, design choices, quality measures, next steps
```

## Environment
- Python 3.11+
- LLM API key read from the environment variable `ANTHROPIC_API_KEY` — never
  hardcoded, never committed. `.env.example` is committed; `.env` is gitignored.
- Pinned versions in `requirements.txt`.

## Conventions
- Type hints; docstrings on public functions.
- No secrets, no absolute paths from my machine.
- Commit messages say why, not what.

## Source notes
*Compiled by reading all 26 files in `data/` on 2026-08-23. This section is a **recall
fixture**: it records what one careful human pass found, so the detector's output can be
measured against it. It is **not** detector input — nothing here is to be hardcoded. How
each conflict resolves is deliberately omitted; the system must derive that from the
sources at run time.*

### Documents by category

**Harding Outfitters — the engagement being scoped (9)**

| File | Covers | Date |
|---|---|---|
| `transcripts/2026-07-10_harding_discovery_call.md` | Problem framing, initial scope, first go-live date, CTO security constraints | 2026-07-10 |
| `transcripts/2026-08-05_harding_scoping_call.md` | Effort estimates, commercials, governance, staffing shape, acceptance discussion | 2026-08-05 |
| `transcripts/2026-08-19_harding_kickoff_prep_internal.md` | Staffing allocations, risk list, drafting instructions. Marked *"not for client distribution"* | 2026-08-19 |
| `emails/harding_timeline_thread.md` | 4 messages: scope descope, timeline change, sandbox confirmation | 2026-08-12 → 08-15 |
| `chat/blaugarnet_harding_channel_export.md` | `#harding-delivery` export; corrections, verbal commitments, status | Jul–Aug, exported 08-21 |
| `notes/harding_scope_addendum_v1.md` | Scope, timeline, effort. Marked superseded by v2 | 2026-08-07 |
| `notes/harding_scope_addendum_v2.md` | Scope in/out, timeline, freezes, effort. Marked *"out for signature"* (unsigned) | 2026-08-18 |
| `notes/harding_requirements_draft.md` | Modules, roles, NFRs, security detail, open items. Marked *"incomplete, do not circulate"* | touched 2026-08-16 |
| `docs/harding_msa_summary.md` | Payment terms, IP, liability, compliance, change-control mechanism | MSA executed 2026-08-10 |

**Company reference — applies to Harding (8)**

| File | Covers | Date |
|---|---|---|
| `sow_template.md` | The 12-section target structure | undated |
| `docs/blaugarnet_rate_card_2026.md` | Current card; exception rule | eff. 2026-01-01 |
| `docs/blaugarnet_rate_card_2025.md` | Prior card; condition for honoring it past 2025 | eff. 2025-01-01 |
| `internal/blaugarnet_sales_playbook_extract.md` | §4 commercial guardrails: pricing, rates, terms, acceptance authority | v2026-04 |
| `internal/helios_bank_postmortem.md` | Three lessons: vendor sandbox timing, acceptance-as-TBD, unwritten verbal splits | closed 2025-11 |
| `internal/blaugarnet_infosec_policy.md` | SOC 2 Type II, least privilege, regulated-data addendum rule | v3.2, 2026-03 |
| `internal/blaugarnet_qa_checklist_template.md` | Release checklist; sign-off and waiver mechanics | v1.4, undated |
| `internal/blaugarnet_marketing_onepager.md` | Firm description usable for §1 framing | undated |

**Other clients — precedent, and the main contamination hazard (5)**

| File | Client | Date |
|---|---|---|
| `docs/northgate_sow_executed.md` | Northgate Logistics — an executed SOW in this exact template | 2026-05-02 |
| `transcripts/2026-05-19_northgate_kickoff.md` | Northgate Logistics | 2026-05-19 |
| `emails/northgate_cutover_email.md` | Northgate Logistics | 2026-08-04 |
| `notes/atlas_retail_discovery_notes.md` | Atlas Retail, pursuit stage, marked "no commitment" | 2026-07-03 |
| `notes/atlas_retail_status.md` | Atlas Retail, pursuit status | 2026-07-28 |

**Internal, largely unrelated (4)** — retrieval noise
`internal/blaugarnet_allhands_2026-07.md` (2026-07-25) · `internal/blaugarnet_engineering_onboarding.md` (undated) · `internal/blaugarnet_leave_policy.md` (2026-01) · `internal/blaugarnet_travel_expense_policy.md` (2025-09).
Thin genuine hooks: the all-hands and a `finance.bot` chat message both reference a rate-card
compliance review due 2026-08-31; the T&E policy bears on expense handling under §8.

Only 9 of 26 documents concern Harding.

### SOW template structure (`data/sow_template.md`)
Twelve required sections: 1 Engagement Overview & Objectives · 2 Scope of Work (2.1 In / 2.2 Out) ·
3 Deliverables & Milestones · 4 Timeline · 5 Team & Roles · 6 Governance & Change Management ·
7 Client Responsibilities & Dependencies · 8 Commercials · 9 Security & Compliance ·
10 Assumptions & Open Questions · 11 Risks · 12 Acceptance Criteria.

### Conflict recall fixture

Each entry states the disputed fact and the files carrying differing accounts of it.
Resolution is intentionally not recorded.

**C1 — Production go-live date.** `2026-12-11` in `transcripts/2026-07-10_harding_discovery_call.md`,
`transcripts/2026-08-05_harding_scoping_call.md`, `notes/harding_scope_addendum_v1.md`;
`2027-01-15` in `emails/harding_timeline_thread.md`, `notes/harding_scope_addendum_v2.md`,
`chat/blaugarnet_harding_channel_export.md`.

**C2 — Instant exchanges in or out of phase one.** In scope in
`transcripts/2026-07-10_harding_discovery_call.md`, `transcripts/2026-08-05_harding_scoping_call.md`,
`notes/harding_scope_addendum_v1.md` (item 5); out of scope in `emails/harding_timeline_thread.md`,
`notes/harding_scope_addendum_v2.md`, `chat/blaugarnet_harding_channel_export.md`.

**C3 — Rate structure: blended vs role-based.** `transcripts/2026-08-05_harding_scoping_call.md`
states "blended it comes out around a hundred and five" and retracts it within the same turn;
`chat/blaugarnet_harding_channel_export.md` (08-06) disputes the figure; the same
`USD 105/hour` blended figure appears as settled fact in `docs/northgate_sow_executed.md` §8.

**C4 — Which rate card applies.** `docs/blaugarnet_rate_card_2026.md` states it is for SOW use
absent a written exception; `chat/blaugarnet_harding_channel_export.md` (08-08) and
`transcripts/2026-08-19_harding_kickoff_prep_internal.md` assert a client commitment to 2025
rates; `docs/blaugarnet_rate_card_2025.md` conditions that on a finance-approved deal note;
`internal/blaugarnet_sales_playbook_extract.md` §2 requires the note be referenced in the SOW.
No deal-note document exists in `data/`, and no identifier for one appears in any source.

**C5 — Payment terms.** Net 30 in `transcripts/2026-08-05_harding_scoping_call.md`,
`internal/blaugarnet_sales_playbook_extract.md` §4, and `docs/northgate_sow_executed.md`;
net 45 in `docs/harding_msa_summary.md`.

**C6 — Change-request approval authority.** Steering-committee-only in
`transcripts/2026-08-05_harding_scoping_call.md`; a 40-hour threshold with joint
delivery-lead/IT-director approval in `transcripts/2026-08-19_harding_kickoff_prep_internal.md`
and `chat/blaugarnet_harding_channel_export.md` (08-20). `docs/harding_msa_summary.md` requires
a written change order but states the MSA is silent on approval bodies. Both internal sources
also carry an instruction to record this as an open negotiation point.

**C7 — Acceptance criteria: deferred vs required in the SOW.** Deferral to a UAT planning sprint
in `transcripts/2026-08-05_harding_scoping_call.md`, with a client objection in the same turn;
`notes/harding_requirements_draft.md` still lists them undefined; a mandatory-section rule in
`internal/blaugarnet_sales_playbook_extract.md` §5 and `internal/helios_bank_postmortem.md`
lesson 2; `sow_template.md` §12 requires the section.

**C8 — Effort against calendar.** `transcripts/2026-08-05_harding_scoping_call.md` pairs
~2,400 hours with a ~3-month schedule; `notes/harding_scope_addendum_v2.md` carries the same
~2,400 hours across a schedule extended to 2027-01-15 with an added regression window, while
`emails/harding_timeline_thread.md` records a client instruction that the extra runway be used
for UAT rather than absorbed as slack. `notes/harding_scope_addendum_v1.md` carries ~2,900 hours.

**C9 — Payment milestone schedule.** 20/30/30/20 with named triggers appears only in
`transcripts/2026-08-05_harding_scoping_call.md` — the same passage containing the retracted
figure in C3; 25/25/25/25 appears in `docs/northgate_sow_executed.md`. The "UAT entry" trigger
resolves to one date under `notes/harding_scope_addendum_v1.md` and to a split window under
`notes/harding_scope_addendum_v2.md`.

**C10 — Data migration responsibility split.** Deferred in
`transcripts/2026-07-10_harding_discovery_call.md`; agreed verbally per
`chat/blaugarnet_harding_channel_export.md` (07-18) and queried again in
`transcripts/2026-08-19_harding_kickoff_prep_internal.md`; written into
`notes/harding_scope_addendum_v2.md` item 5, which is unsigned.
`internal/helios_bank_postmortem.md` lesson 3 concerns the same pattern.

**C11 — Staffing allocations.** Roles without allocations in
`transcripts/2026-08-05_harding_scoping_call.md`; percentages only in
`transcripts/2026-08-19_harding_kickoff_prep_internal.md`, which is marked not for client
distribution. Cross-engagement load: the delivery lead is also allocated in
`docs/northgate_sow_executed.md` §5, and `notes/atlas_retail_status.md` flags an architect
availability collision with a Harding design week.

**C12 — Named-entity traps (break retrieval rather than the facts).** The Helios vendor and its
provisioning duration are conflated and then corrected in-line in
`transcripts/2026-08-19_harding_kickoff_prep_internal.md` and
`chat/blaugarnet_harding_channel_export.md` (07-11); the actual figures live in
`internal/helios_bank_postmortem.md` and `transcripts/2026-07-10_harding_discovery_call.md`
and differ from each other. `docs/northgate_sow_executed.md` supplies a named acceptance
authority and a 10-business-day acceptance window — the shape of the fact Harding lacks (G12),
in another client's document. The delivery lead's name appears in both engagements.
Positive control: the OrderHub sandbox filing date is consistent across
`chat/blaugarnet_harding_channel_export.md` (07-30),
`transcripts/2026-08-05_harding_scoping_call.md`, and
`transcripts/2026-08-19_harding_kickoff_prep_internal.md`.

### Coverage gaps by template section

| § | State | Missing |
|---|---|---|
| 1 Overview | covered | — |
| 2 Scope | covered | — |
| 3 Deliverables & Milestones | partial | **G3** No deliverable-level milestone table: no deliverable descriptions, no milestone exit criteria. Only payment triggers exist. |
| 4 Timeline | covered | Sprint structure stated only loosely. |
| 5 Team & Roles | partial | **G5** Client counterparts named, but no SOW obligations assigned to them. |
| 6 Governance | partial | **G6a** No delivery-level meeting cadence stated for Harding. **G6b** Escalation path never discussed in any source. (Approval authority is C6.) |
| 7 Client Responsibilities | partial | **G7** No turnaround SLA on environment or access provisioning. |
| 8 Commercials | partial | **G8a** No total contract value, and not derivable — allocations are percentages, never hours per role. **G8b** No statement on travel or expenses for this engagement. |
| 9 Security & Compliance | partial | **G9a** No regulation ever named, though `sow_template.md` §9 asks for applicable regulatory requirements. **G9b** Pen-test vendor ownership marked TBD. **G9c** Client infosec questionnaire not yet received. **G9d** PCI scope-out and DPA both marked "confirm with legal", never confirmed. **G9e** Unclear whether the regulated-data addendum and named security reviewer in `internal/blaugarnet_infosec_policy.md` are triggered. |
| 10 Assumptions & Open Questions | covered | — |
| 11 Risks | covered | — |
| 12 Acceptance Criteria | **absent** | **G12** No mechanism, no acceptance window, and no named client-side acceptance authority anywhere in the corpus. |

**Absent from every source (G13):** total price or fee · escalation path · warranty, hypercare or
post-go-live support · quantified availability/performance target (marked "TBD, quantify" in
`notes/harding_requirements_draft.md`) · agent-queue reporting requirements ("nobody has
specified any") · deal-note identifier for the rate exception (C4) · accessibility requirements
for the customer-facing portal, though `internal/blaugarnet_qa_checklist_template.md` mandates a
scan. Two scope items appear in neither the in-scope nor the out-of-scope list of
`notes/harding_scope_addendum_v2.md`: duplicate return detection (marked "nice-to-have?") and
carrier return-label generation (marked parked).

---
*Deliberately not in this file: the architecture. Retrieval strategy, the section
pipeline and the conflict-detection approach are decided in session.*
