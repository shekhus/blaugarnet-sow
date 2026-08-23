╭─── Claude Code v2.1.240 ─────────────────────────────────────────────────────╮
│                                     │ Tips for getting started               │
│        Welcome back shekhar!        │ Run /init to create a CLAUDE.md file … │
│                                     │ ────────────────────────────────────── │
│               ▐▛███▛█               │ What's new                             │
│              ▝▜██████▀              │ Bug fixes and reliability improvements │
│                ▝▝ ▝▝                │ Cost estimates (`/cost`, status line,… │
│                                     │ Added the one-time fullscreen rendere… │
│   Opus 5 · Claude Pro · cstifants   │ /release-notes for more                │
│          ~\blaugarnet-sow           │                                        │
╰──────────────────────────────────────────────────────────────────────────────╯

   Tackle your toughest work with Opus 5. Switch anytime with /model.

❯ commit code

● I'll check what's there before committing.

  Ran 3 shell commands (ctrl+o to expand)

● No remote configured — this is a local-only repo, so I'll commit directly to
  main rather than branching.

  Ran 2 shell commands (ctrl+o to expand)

● Committed as 0b9ceae on main, working tree clean.

- 26 markdown files under data/ (transcripts, emails, chat export, internal
  docs, client notes, rate cards, contracts) plus data/sow_template.md
- The Blaugarnet — Engineering Assignment Instructions.docx source document

  Two notes:

- Committed to main rather than a feature branch — there's no remote
  configured, so nothing shared to protect. Say the word if you'd prefer this
  on a branch.
- Git warned it will normalize LF→CRLF on these files. Harmless locally, but
  if this repo is graded or shared cross-platform, adding a .gitattributes
  with * text=auto eol=lf would keep line endings stable. Want me to add it?

✻ Churned for 40s

❯ /model
  ⎿  Set model to Opus 5 (1M context) and saved as your default for new sessions

❯ Read CLAUDE.md first.

  Then read every file under data/ and report back a map:

- what each document is and roughly when it was written
- which relate to the Harding Outfitters engagement, and which areabout other clients or unrelated internal matters
- anywhere two documents disagree on a fact a Statement of Workwould need (rates, dates, scope, people, obligations)
- anything the SOW template requires that the sources appear not
  to cover at all

  Do not write code yet. Do not propose a design yet. Just the map.

  Ran 2 shell commands (ctrl+o to expand)

● No CLAUDE.md exists anywhere in the repo (or at user level), and src/, tests/,
  output/, ai_transcripts/ are all empty. The closest thing to project
  instructions is the assignment .docx, so I'll read that plus everything under
  data/.

  Ran 6 shell commands (ctrl+o to expand)

● No CLAUDE.md exists — not at the repo root, not in any subdirectory, not at
  user level. src/, tests/, output/, and ai_transcripts/ are all empty
  directories. The only governing instructions in the repo are the assignment
  .docx, which I read instead: build a system that drafts the Harding Outfitters
  SOW from data/ with citations, surfaces inconsistencies rather than guessing,
  logs a trace, and adds a CLI approve/reject-with-comment loop.

  Here is the map of all 26 documents under data/.

---

1. What each document is

  Harding Outfitters — the engagement being scoped (9 docs)

  File: transcripts/2026-07-10_harding_discovery_call.md
  What it is: Discovery call. Problem statement, initial scope, first go-live
  date, Raj's security constraints
  Written: 2026-07-10
  ────────────────────────────────────────
  File: transcripts/2026-08-05_harding_scoping_call.md
  What it is: Scoping session. Effort estimates, commercials, governance,
  staffing shape
  Written: 2026-08-05
  ────────────────────────────────────────
  File: transcripts/2026-08-19_harding_kickoff_prep_internal.md
  What it is: Internal only, "not for client distribution." Staffing %, risk
  list, negotiating posture
  Written: 2026-08-19
  ────────────────────────────────────────
  File: emails/harding_timeline_thread.md
  What it is: 4-message thread. The pivot: exchanges descoped, go-live moved
  Written: 2026-08-12 → 08-15
  ────────────────────────────────────────
  File: chat/blaugarnet_harding_channel_export.md
  What it is: #harding-delivery export, selected msgs
  Written: July–Aug, exported 2026-08-21
  ────────────────────────────────────────
  File: notes/harding_scope_addendum_v1.md
  What it is: Scope addendum v1 — superseded, explicitly "dead"
  Written: 2026-08-07
  ────────────────────────────────────────
  File: notes/harding_scope_addendum_v2.md
  What it is: Scope addendum v2 — supersedes v1, status: out for signature
  (unsigned)
  Written: 2026-08-18
  ────────────────────────────────────────
  File: notes/harding_requirements_draft.md
  What it is: Daniel's requirements draft — "incomplete, do not circulate"
  Written: last touched 2026-08-16
  ────────────────────────────────────────
  File: docs/harding_msa_summary.md
  What it is: Plain-language MSA summary. Governs the SOW
  Written: MSA executed 2026-08-10

  Company reference material that applies to Harding (8 docs)

  File: sow_template.md
  What it is: The 12-section target structure
  Written: undated (post-2025-12)
  ────────────────────────────────────────
  File: docs/blaugarnet_rate_card_2026.md
  What it is: Current card. "For SOW use unless a written exception applies"
  Written: eff. 2026-01-01
  ────────────────────────────────────────
  File: docs/blaugarnet_rate_card_2025.md
  What it is: Prior card. Honored past 2025 only with a finance-approved deal
  note
  Written: eff. 2025-01-01
  ────────────────────────────────────────
  File: internal/blaugarnet_sales_playbook_extract.md
  What it is: §4 commercial guardrails — rate/terms/acceptance rules
  Written: v2026-04
  ────────────────────────────────────────
  File: internal/helios_bank_postmortem.md
  What it is: Post-mortem whose three lessons map directly onto Harding's open
  risks
  Written: closed 2025-11
  ────────────────────────────────────────
  File: internal/blaugarnet_infosec_policy.md
  What it is: SOC 2, least privilege, regulated-data addendum rule
  Written: v3.2, 2026-03
  ────────────────────────────────────────
  File: internal/blaugarnet_qa_checklist_template.md
  What it is: Release checklist; touches acceptance and sign-off
  Written: v1.4, undated
  ────────────────────────────────────────
  File: internal/blaugarnet_marketing_onepager.md
  What it is: Firm boilerplate — usable for SOW framing only
  Written: undated

  Other clients — relevant only as precedent, dangerous as source (5 docs)

  File: docs/northgate_sow_executed.md
  Client: Northgate Logistics — an executed SOW in this template. Useful as a
  worked example, hazardous as a fact source
  Written: 2026-05-02
  ────────────────────────────────────────
  File: transcripts/2026-05-19_northgate_kickoff.md
  Client: Northgate kickoff
  Written: 2026-05-19
  ────────────────────────────────────────
  File: emails/northgate_cutover_email.md
  Client: Northgate Reno cutover result
  Written: 2026-08-04
  ────────────────────────────────────────
  File: notes/atlas_retail_discovery_notes.md
  Client: Atlas Retail pursuit, pre-SOW, no commitment
  Written: 2026
  ⎿  Interrupted · What should Claude do instead?

❯ added claude.md
  now proceed

  Ran 1 shell command (ctrl+o to expand)

● Read it. Two things it changes for this task: the conflicts I find by hand are
  a recall fixture for judging the detector later, explicitly not to be
  hardcoded into it; and the ## Source notes section is a placeholder I should
  fill from this map once you've reviewed it.

  Here is the full map.

---

  Document map — data/

  26 files, ~34 KB total. Read in full.

1. Inventory

  A. Harding Outfitters — the engagement being scoped (9)

  File: transcripts/2026-07-10_harding_discovery_call.md
  What it is: Discovery. Problem framing, initial scope, first go-live date,
  Raj's security constraints
  Date: 2026-07-10
  ────────────────────────────────────────
  File: transcripts/2026-08-05_harding_scoping_call.md
  What it is: Scoping. Effort estimates, commercials, governance, staffing shape
  Date: 2026-08-05
  ────────────────────────────────────────
  File: transcripts/2026-08-19_harding_kickoff_prep_internal.md
  What it is: Internal — "not for client distribution." Staffing %, risk table,
  negotiating posture
  Date: 2026-08-19
  ────────────────────────────────────────
  File: emails/harding_timeline_thread.md
  What it is: 4 messages. The pivot: exchanges descoped, go-live moved
  Date: 2026-08-12 → 08-15
  ────────────────────────────────────────
  File: chat/blaugarnet_harding_channel_export.md
  What it is: #harding-delivery export, selected messages
  Date: Jul–Aug, exported 08-21
  ────────────────────────────────────────
  File: notes/harding_scope_addendum_v1.md
  What it is: Scope addendum v1 — superseded; chat calls it "dead, don't use it"
  Date: 2026-08-07
  ────────────────────────────────────────
  File: notes/harding_scope_addendum_v2.md
  What it is: Scope addendum v2 — supersedes v1. Status: out for signature,
  unsigned
  Date: 2026-08-18
  ────────────────────────────────────────
  File: notes/harding_requirements_draft.md
  What it is: Daniel's requirements draft — "incomplete, do not circulate"
  Date: touched 2026-08-16
  ────────────────────────────────────────
  File: docs/harding_msa_summary.md
  What it is: MSA plain-language summary. Governs the SOW
  Date: MSA executed 2026-08-10

  B. Company reference — applies to Harding (8)

  File: sow_template.md
  What it is: The 12-section target structure
  Date: undated (post-2025-12)
  ────────────────────────────────────────
  File: docs/blaugarnet_rate_card_2026.md
  What it is: Current card. "For SOW use unless a written exception applies"
  Date: eff. 2026-01-01
  ────────────────────────────────────────
  File: docs/blaugarnet_rate_card_2025.md
  What it is: Prior card. Honored past 2025 only with a finance-approved deal
  note for a named client
  Date: eff. 2025-01-01
  ────────────────────────────────────────
  File: internal/blaugarnet_sales_playbook_extract.md
  What it is: §4 commercial guardrails — rates, terms, acceptance authority
  Date: v2026-04
  ────────────────────────────────────────
  File: internal/helios_bank_postmortem.md
  What it is: Three lessons that map one-to-one onto Harding's open risks
  Date: closed 2025-11
  ────────────────────────────────────────
  File: internal/blaugarnet_infosec_policy.md
  What it is: SOC 2 Type II, least privilege, regulated-data addendum rule
  Date: v3.2, 2026-03
  ────────────────────────────────────────
  File: internal/blaugarnet_qa_checklist_template.md
  What it is: Release checklist; touches acceptance/sign-off
  Date: v1.4, undated
  ────────────────────────────────────────
  File: internal/blaugarnet_marketing_onepager.md
  What it is: Firm boilerplate — usable for §1 framing only
  Date: undated

  C. Other clients — precedent, and the main contamination hazard (5)

  File: docs/northgate_sow_executed.md
  Client: Northgate Logistics. A worked example of the template — and a
  minefield
  of plausible wrong numbers
  Date: 2026-05-02
  ────────────────────────────────────────
  File: transcripts/2026-05-19_northgate_kickoff.md
  Client: Northgate kickoff
  Date: 2026-05-19
  ────────────────────────────────────────
  File: emails/northgate_cutover_email.md
  Client: Northgate Reno cutover result
  Date: 2026-08-04
  ────────────────────────────────────────
  File: notes/atlas_retail_discovery_notes.md
  Client: Atlas Retail pursuit, pre-SOW, explicitly "no commitment"
  Date: 2026-07-03
  ────────────────────────────────────────
  File: notes/atlas_retail_status.md
  Client: Atlas pursuit status
  Date: 2026-07-28

  D. Internal, essentially unrelated (4)

  internal/blaugarnet_allhands_2026-07.md (2026-07-25) ·
  internal/blaugarnet_engineering_onboarding.md (undated) ·
  internal/blaugarnet_leave_policy.md (2026-01) ·
  internal/blaugarnet_travel_expense_policy.md (2025-09)

  These are retrieval noise by design. Two have thin genuine hooks: the
  all-hands and a finance.bot chat message both flag the Q3 rate card compliance
  review due 2026-08-31, which bears on the rate exception below; T&E bears on
  expense handling in §8.

  Note on B/C/D: only 9 of 26 documents are about Harding. Roughly a third of
  the corpus is same-shaped, same-company, wrong-engagement content. That ratio
  looks deliberate.

---

2. Conflicts a SOW would have to resolve

  Ordered by how much damage getting them wrong would do.

  2.1 Go-live date — Dec 11 2026 vs Jan 15 2027

- Dec 11, 2026: discovery (Sandra: "that's the date I'm carrying"), scoping
  call, addendum v1.
- Jan 15, 2027: Jake's email 08-12 ("the December 11 go-live is dead"), Sandra
  concurs 08-12, Meera confirms 08-13, Jake 08-15 "date on our internal plan
  of record", addendum v2, chat 08-12.
- Resolvable by recency. Cause: OrderHub vendor-API change freeze Dec 1 – Jan
  5, plus Harding's own production freeze Dec 15 – Jan 1.

  2.2 Instant exchanges — in scope vs deferred

- In: discovery ("let's keep it in for now"), scoping call full-scope
  estimate, addendum v1 item 5.
- Out: Jake's email 08-12 ("decision made"), addendum v2 out-of-scope list,
  chat 08-12.
- Resolvable by recency. This is the single largest scope delta in the corpus.

  2.3 Rate structure — blended $105/hr vs role-based off the card

- Meera says "blended it comes out around a hundred and five" on the scoping
  call — then retracts it mid-sentence: "sorry, no, that's — ignore that,
  that's a different structure."
- Chat 08-06, Tom: "scoping call recap says blended 105/hr?? since when do we
  do blended." Meera: "we don't — i misspoke on the call, was looking at the
  northgate sheet."
- $105/hr blended is Northgate's number, sitting in northgate_sow_executed.md
  §8. Any system that retrieves on "blended rate" without engagement filtering
  will pull the wrong client's commercials and find apparent corroboration
  for it in the Harding transcript.

  2.4 Which rate card — 2026 (default) vs 2025 (verbal client commitment)

- 2026 card: "For SOW use unless a written exception applies."
- Chat 08-08, Meera: "commitment i made to raj during the pursuit: harding
  gets 2025 card rates held through phase one... finance has the note. do NOT
  quote 2026 rates in the SOW." Alicia acks.
- Internal 08-19, Meera: "Finance question came up on which card applies. I
  made a commitment there, it's in the channel, honor it in the SOW."
- The catch: 2025 card says it's honored past 2025 "only where a
  finance-approved deal note commits it for a named client," and playbook §2
  requires that note to be referenced in the SOW. The note is asserted to
  exist but no deal-note document is in the corpus and it has no identifier.
  So the answer is 2025 rates plus an unresolvable citation. The rate-card
  compliance review due 2026-08-31 makes this live.

  2.5 Payment terms — net 30 vs net 45

- Net 30: Jake on the scoping call ("net 30 like usual, right?"), playbook §4
  default for proposals, Northgate SOW.
- Net 45: MSA summary, MSA executed 2026-08-10.
- Playbook §4 settles it — "the executed MSA always wins; check it before the
  SOW is issued." Note the chronology: every net-30 mention predates MSA
  execution. Meera never commits on the call ("we'll confirm terms against the
  MSA — procurement was still redlining").

  2.6 Change-request approval authority — genuinely unresolved

- Karen Boyle, scoping call: "Anything that moves scope, cost or date goes to
  our steering committee. I chair it, we meet monthly. Nothing gets approved
  outside that committee, we learned that lesson on the OrderHub upgrade
  project."
- Priya Nair, internal 08-19: CRs under 40 hours' impact approved jointly by
  her + Harding's IT Director; only larger ones go to committee. "Write it my
  way in the draft, we'll negotiate." Repeated in chat 08-20.
- Meera, same call: "Flag it as an open negotiation point, please, not a
  settled thing."
- MSA: all SOW changes need a written change order executed by both parties;
  the MSA is explicitly silent on approval bodies, delegating the operating
  process to the SOW.
- This one must not be silently resolved. Recency favors Priya, but Priya's
  position is internal negotiating posture from a not-for-client-distribution
  document, and Meera instructed it be flagged as open. A system that resolves
  this by "most recent wins" produces a client-facing document asserting a
  process the client has explicitly refused.

  2.7 Acceptance criteria — deferral vs three standing rules

- Alicia, scoping call: "We'll define UAT acceptance criteria together during
  the UAT planning sprint. Too early to fix them now."
- Karen, immediately: "I'd rather have at least the mechanism in the SOW. But
  fine, flag it."
- Against that: Helios lesson #2 — acceptance left as "to be defined during
  UAT" let the client extend UAT by 3 weeks at Blaugarnet's cost; playbook §5
  — "Every SOW names the client-side acceptance authority. Post-Helios, no
  exceptions"; template §12 requires the section; and the SOW template was
  itself amended in 2025-12 because of Helios.
- Requirements draft still lists acceptance criteria as undefined as of 08-16.

  2.8 Effort vs calendar — 2,400 hours across two different schedules

- Scoping call: full scope ≈ 2,900 h / ~4.5 months; without exchanges ≈ 2,400
  h / ~3 months (holding Dec 11).
- Addendum v2: still ≈ 2,400 h, but now kickoff 09-15 → go-live 2027-01-15,
  with UAT extended (11-30 – 12-11) plus a new regression window (2027-01-06 –
  01-12).
- Partly defensible — the freezes are dead calendar, not work. But Sandra
  explicitly said "I want the extra runway used for a proper UAT, not absorbed
  as slack," and v2 adds a regression window that did not exist. More UAT and
  more regression with an unchanged hour total is a soft inconsistency worth
  surfacing rather than reconciling silently.

  2.9 Payment milestones — single-sourced, and one trigger is now ambiguous

- Harding: 20% kickoff / 30% OrderHub integration complete in staging / 30%
  UAT entry / 20% go-live. Only source is the scoping-call transcript — the
  same passage that contains the retracted blended-rate error.
- Northgate is 25/25/25/25 — a competing pattern in a more
  authoritative-looking document.
- "UAT entry" was unambiguous when UAT was one window. Under v2, UAT is split
  across the freeze (Nov 30 and Jan 6). The trigger no longer resolves to one
  date.

  2.10 Migration responsibility split — verbal, then written, still unsigned

- Discovery: deferred ("take that offline with your data team").
- Chat 07-18: Raj agrees verbally on the CTO sync — Harding does extraction +
  cleanup, Blaugarnet does transform + load, joint validation. Priya: "get (1)
  written down somewhere that isn't this channel please."
- Internal 08-19: Priya asks whether the CTO ever agreed; Meera: "Verbally,
  yes."
- Now written into addendum v2 item 5 — but v2 is unsigned. Helios lesson #3:
  an unwritten verbal split on data cleanup cost ~180 unbudgeted hours.

  2.11 Staffing — refinement, not contradiction, but sourced only from an
  internal document

- Scoping call (client-facing): roles named, "exact allocations tabled in the
  SOW."
- Internal 08-19: Priya 50%, Daniel 25% front-loaded, Tom Reyes + 1 senior
  engineer FT, 1 engineer FT, QA 50% from sprint 3, Alicia 40%.
- The only allocation numbers in the corpus come from the
  not-for-client-distribution transcript. Also: Priya is 25% on Northgate
  concurrently, and atlas_retail_status.md flags Daniel's availability
  colliding with "Harding sprint 0 design week."

  2.12 Named-entity traps (not conflicts, but they break naive retrieval)

- Helios: Tom, internal 08-19 — "their provisioning queue burned us on
  Helios... no wait, that was the other vendor." Chat 07-11 — "helios was the
  bank tho? different vendor." Helios was a core banking API, 9 weeks.
  OrderHub's precedent is 6 weeks (Daniel, discovery). Two different vendors,
  two different numbers, and the transcript contains its own correction.
- Priya Nair appears on both Northgate and Harding. StackWare, Victor Hansen,
  Lena Duarte, Derek Whitfield are Northgate-only. Northgate's acceptance
  authority is "VP Operations" and its window "10 business days" — the exact
  shape of the fact Harding is missing, in the wrong client's document.
- Sandbox filing date is consistent across three sources (chat 07-30, scoping
  call "went in last week", internal "July 30th"). A useful positive control.

---

3. What the template requires that the sources do not cover

  Against the 12 sections of data/sow_template.md:

  §: 1. Overview & Objectives
  Coverage: Good
  Gap: — 12-day refund cycle, 30% of contacts are refund-status, 22% Q4 return
  rate. Chat 07-11 even nominates these as "our headline for the SOW overview."
  ────────────────────────────────────────
  §: 2. Scope (in/out)
  Coverage: Good
  Gap: — addendum v2 gives both lists explicitly.
  ────────────────────────────────────────
  §: 3. Deliverables & Milestones
  Coverage: Partial
  Gap: No deliverable-level milestone table anywhere. Payment triggers exist;
  deliverable descriptions and milestone exit criteria do not. Northgate has
  M1–M4; Harding has no equivalent.
  ────────────────────────────────────────
  §: 4. Timeline
  Coverage: Good
  Gap: — kickoff, UAT, regression, go-live, both freezes. Sprint structure is
  vague ("three two-week sprint blocks per module").
  ────────────────────────────────────────
  §: 5. Team & Roles
  Coverage: Partial
  Gap: Blaugarnet side complete (from the internal doc). Client counterparts
  named — Sandra Liu (VP CX), Jake Morrow (IT Director), Raj Patel (CTO), Karen
   Boyle (PMO) — but their SOW-specific obligations are never assigned.
  ────────────────────────────────────────
  §: 6. Governance
  Coverage: Partial
  Gap: Monthly steering exists. No delivery-level meeting cadence is ever stated

  for Harding (Northgate has a weekly sync — wrong client). The escalation
  path is never discussed by anyone. CR approver disputed (§2.6).
  ────────────────────────────────────────
  §: 7. Client Responsibilities
  Coverage: Partial
  Gap: Staging env, OrderHub sandbox, migration extraction/cleanup, Okta
  group-to-role mapping, prod credentials, reason-code taxonomy. No  turnaround
   SLA on access or environments — Northgate has "within 5 business days";
  Harding has nothing, and sandbox delay is the top risk.
  ────────────────────────────────────────
  §: 8. Commercials
  Coverage: Partial
  Gap: No total contract value or estimated fee is ever computed. Cannot be
  derived: allocations are percentages, not hours per role, so hours never map
  to the rate card. Also no statement on travel/expenses for this engagement,
  though the MSA requires prior written approval and a T&E policy sits in the
  corpus.
  ────────────────────────────────────────
  §: 9. Security & Compliance
  Coverage: Partial
  Gap: Strong on substance (PII, no card data, Okta OIDC, SOC 2, TLS 1.2+, audit

  logging). But: no regulation is ever named — Raj says "privacy compliance
  applies to every byte" and no one says GDPR/CCPA/anything, while the template
   asks for "applicable regulatory requirements." Pen-test vendor  ownership:
  "whose vendor? TBD." Harding's infosec questionnaire not yet  received as of
  08-16. PCI scope-out and the DPA are both marked "confirm with legal" and
  never confirmed. Unclear whether infosec policy's regulated-data addendum +
  named security reviewer is triggered.
  ────────────────────────────────────────
  §: 10. Assumptions & Open Questions
  Coverage: Good
  Gap: Ample material.
  ────────────────────────────────────────
  §: 11. Risks
  Coverage: Good
  Gap: Three named on 08-19: sandbox slip (top risk, "I want it named in the SOW

  risk table"), the two freezes, unprofiled legacy data.
  ────────────────────────────────────────
  §: 12. Acceptance Criteria
  Coverage: Worst gap
  Gap: No mechanism, no window, no named client-side acceptance authority. Karen

  chairs steering; Sandra signs the addendum; nobody is designated to accept
  deliverables. Directly violates playbook §5 ("no exceptions") and repeats
  Helios lesson #2 verbatim.

  Absent from the corpus entirely

- Total price / fee. Not stated, not derivable.
- Escalation path. Never mentioned by anyone.
- Warranty, hypercare, or post-go-live support. Never mentioned — for a Jan 15
  go-live deliberately timed to land in the post-holiday returns peak, at 4×
  normal volume.
- Availability/performance target. Requirements draft: Sandra said "it can't
  be down during business hours," annotated "TBD, quantify." Volume
  assumptions exist (~1,800 requests/week, ~4× January spike); no SLA.
- Reporting requirements for the agent queue. Requirements draft: "nobody has
  specified any."
- Deal-note identifier for the 2025 rate exception (§2.4).
- Accessibility requirements — the QA checklist mandates an accessibility
  scan; never raised with Harding.
- Two scope items in limbo, in neither v2's in-scope nor its out-of-scope
  list: duplicate return detection ("nice-to-have?") and carrier return-label
  generation ("parked, Sandra keeps mentioning it though").

---

4. Two structural observations

  Provenance tiers matter more than recency here. The corpus contains at least
  three documents that are authoritative-sounding but not usable at face value:
  addendum v1 (superseded and explicitly dead), the requirements draft (marked
  incomplete, do not circulate), and the internal prep transcript (not for
  client distribution). Yet the internal transcript is the only source for
  staffing allocations and for the risk table, and the requirements draft is the
  only source for the $250 approval threshold, volume assumptions, and most of
  the security detail. They cannot simply be excluded — but a client-facing SOW
  that quotes Priya's "write it my way in the draft, we'll negotiate" as settled
  governance is a real failure mode, and the corpus is arranged so that a
  purely recency-based resolver will produce exactly that.

  The corpus encodes its own resolution rules. Playbook §4 says the executed MSA
  beats the proposal default (settles net 30/45). Playbook §2 says rate
  exceptions need a deal note referenced in the SOW (settles the card, and
  exposes the missing note). Playbook §5 and Helios lesson #2 say acceptance
  authority and mechanism are non-negotiable (settle §12). Helios lesson #3 says
  verbal splits go in writing (settles §2.10). Helios lesson #1 says file
  vendor access at contracting, not kickoff (justifies the top risk). These are
  deterministic, checkable rules sitting in the sources — which lines up with
  your "deterministic checks in code beat asking the model to behave."

---

  No code, no design proposals, per your instruction. When you've reviewed this
  I can fold a condensed version into the ## Source notes block in CLAUDE.md —
  keeping the conflict list as the recall fixture it's meant to be, not as
  detector input.

✻ Brewed for 1m 34s

※ recap: Goal is a system that drafts the Harding Outfitters SOW from data/ with citations, conflict flagging, and a CLI review loop. I've read CLAUDE.md and all 26 source docs and delivered the requested map. Next: you review it, then I fold a condensed version into CLAUDE.md's Source notes. (disable recaps in /config)

❯ Before I accept this map, verify it. For each of these, quote the exact  line(s) from the source file with the file path — quotes only, no  commentary or interpretation:

1. Meera retracting the blended $105/hr on the scoping call
2. The chat message where Meera says she was looking at the Northgate sheet
3. The $105/hr figure as it appears in northgate_sow_executed.md
4. Jake's email declaring the December 11 go-live dead
5. Karen Boyle's statement that nothing gets approved outside the
   steering committee, and Priya's contradicting position in the
   internal 08-19 doc

  Ran 3 shell commands (ctrl+o to expand)

● All five verified. Quotes only, with paths and line numbers.

---

1. Meera retracting the blended $105/hr

  data/transcripts/2026-08-05_harding_scoping_call.md:23

  ▎ Meera Shah: Standard Blaugarnet Services rate card, blended it comes out
  ▎ around a hundred and five... sorry, no, that's — ignore that, that's a
  ▎ different structure. For this engagement it's role-based rates off our card,
  ▎ we'll put the card in the SOW. Milestone-based payments: twenty percent at
  ▎ kickoff, thirty at OrderHub integration complete in staging, thirty at UAT
  ▎ entry, twenty at go-live.

---

2. Chat — "looking at the northgate sheet"

  data/chat/blaugarnet_harding_channel_export.md:12-13

  ▎ [2026-08-06 17:44] tom.reyes: scoping call recap says blended 105/hr?? since
  ▎ when do we do blended
  ▎ [2026-08-06 17:46] meera.shah: we don't — i misspoke on the call, was
  ▎ looking at the northgate sheet. harding is role-based off the card. already
  ▎ corrected in the recap doc

---

3. The $105/hr figure in the Northgate SOW

  data/docs/northgate_sow_executed.md:26

  ▎ Blended rate: USD 105/hour, estimated 3,100 hours. Payments: 25% at M1, 25%
  ▎ at M2, 25% at M3, 25% at M4. Terms: net 30.

---

4. Jake's email declaring December 11 dead

  data/emails/harding_timeline_thread.md:4-6, 14, 16

  ▎ From: Jake Morrow (Harding) · To: Meera Shah, Alicia Fontaine (Blaugarnet
  ▎ Services) · Cc: Karen Boyle, Sandra Liu
  ▎ Date: 2026-08-12 09:41
  ▎ Subject: Harding phase one timeline

  ▎ Second, and this is the bigger one: OrderHub just notified us of a mandatory
  ▎ platform upgrade with a change freeze on their vendor API from Dec 1 to Jan
  ▎ 5. Integration cutover during that window is not possible. Between that and
  ▎ our own holiday production freeze, the December 11 go-live is dead.

  ▎ Proposal: hold the Sept 15 kickoff, run UAT through early December, pause
  ▎ over the freezes, go live Friday January 15, 2027.

---

  5a. Karen Boyle — nothing approved outside the committee

  data/transcripts/2026-08-05_harding_scoping_call.md:17, 19

  ▎ Karen Boyle: On governance — change requests. Anything that moves scope,
  ▎ cost or date goes to our steering committee. I chair it, we meet monthly.
  ▎ Nothing gets approved outside that committee, we learned that lesson on the
  ▎ OrderHub upgrade project.

  ▎ Alicia Fontaine: Understood, we'll write the change process around the
  ▎ steering committee.

  5b. Priya's contradicting position

  data/transcripts/2026-08-19_harding_kickoff_prep_internal.md:17, 19

  ▎ Priya Nair: On governance — one thing I want changed from what Karen said. A
  ▎ monthly steering committee can't be the only approval path, we'll die
  ▎ waiting. I want the SOW to say change requests under forty hours of impact
  ▎ are approved by me and their IT director jointly, and only bigger ones go to
  ▎ the committee. I own change approval day to day.

  ▎ Alicia Fontaine: Karen was pretty firm that nothing gets approved outside
  ▎ her committee...

✻ Baked for 28s

※ recap: Goal is a system that drafts the Harding Outfitters SOW from data/ with citations, conflict flagging, and CLI review. I mapped all 26 source docs and verified five key quotes. Next: your sign-off on the map, then propose the design. (disable recaps in /config)
❯ Now fold a condensed version into the ## Source notes block in CLAUDE.md.

  Include: the document inventory by category, the conflict list as a
  numbered recall fixture naming the files involved, and the per-section
  coverage gaps.

  Exclude your resolution reasoning. How each conflict resolves is
  something the system must derive from evidence at runtime — if I write
  the answers into CLAUDE.md, the detector will end up encoding my notes
  instead of reading the sources. This list exists only so I can measure
  what the detector catches.

  Ran 1 shell command (ctrl+o to expand)

● Heredoc broke on the shell. Using the file tools instead.

  Made 1 scratchpad edit +168, ran 2 shell commands (ctrl+o to expand)

● Folded into CLAUDE.md:61-227. Everything above and below the block is
  untouched — the closing architecture note still sits at the end.

  What went in:

- Inventory by category — 26 docs in four groups (Harding 9 / company
  reference 8 / other clients 5 / unrelated internal 4), each with what it
  covers and its date. Document status labels are carried as facts from the
  files themselves ("out for signature", "do not circulate", "not for client
  distribution", superseded) since those are printed in the sources, not
  conclusions I drew.
- Template structure — the 12 sections, since your placeholder asked for it.
- C1–C12 recall fixture — each entry names the disputed fact and the files
  carrying differing accounts, nothing more. C12 covers the entity traps, and
  includes the sandbox-filing date as a positive control so you can tell a
  working detector from one that flags everything.
- Coverage gaps — per-section table with IDs G3–G12, plus G13 for what no
  source covers at all.

  What I stripped: every "resolvable by recency", every "X settles it", every
  reference to which document wins. The playbook and post-mortem now appear only
  as files that also address this fact, not as tiebreakers. My two structural
  observations from the earlier report are gone entirely — those were
  interpretation.

  One judgment call worth surfacing: C4 and G13 both record that no deal-note
  document exists in data/ and no identifier appears anywhere. That reads as a
  resolution hint, but it's a negative fact about corpus contents rather than a
  ruling — and without it C4 looks like a plain two-way disagreement instead of
  the three-way problem it is. Say the word if you'd rather it come out.

  The gap IDs are stable, so a detector run can be scored against them directly.

✻ Churned for 2m 35s

❯ Propose the architecture now. Three things from the corpus analysis  should shape it:

1. Only 9 of 26 documents concern Harding, and one of the wrong-clientdocuments contains a number that also appears (retracted) in aHarding transcript. Tell me how retrieval avoids cross-engagementcontamination, and how the system knows the filter worked.
2. Documents differ in authority, not just date: executed MSA, unsignedaddendum, superseded v1, client-facing call, "not for clientdistribution" internal note. A recency-only resolver would putinternal negotiating posture into a client-facing SOW. How do yourepresent that?
3. Conflict and insufficiency detection must run from evidence on every
   execution — no hardcoded conflict list, no reliance on me spotting
   things in the output.

  Give me the pipeline stages, the data structures passed between them,
  the per-section output schema (text, citations, status), and the file
  layout. Tell me what in my brief you think is wrong.

● I've read every file in the corpus and CLAUDE.md already, and src/, tests/,
  output/ are empty — there's no existing code to explore, so I'm skipping the
  Explore/Plan subagents and designing directly. Let me verify the two corpus
  properties this design leans on hardest.

  Ran 2 shell commands (ctrl+o to expand)

● Both load-bearing properties check out. Two findings that shape the design:

  Provenance is parseable from headers. 22 of 26 docs carry explicit authority
  markers in their first lines — **Status:** out for signature, **Version 2 ·
  Supersedes v1**, **Status:** incomplete, do not circulate, **Blaugarnet
  Services internal — not for client distribution**, **MSA executed:**
  2026-08-10, **Superseded by the 2026 card**. Authority can be read from the
  corpus, not asserted by me.

  The template enumerates its own required elements. The guidance prose under
  each heading is a comma-separated checklist: §12 is "How deliverables are
  accepted, by whom, and within what window" — that "by whom" is exactly gap
  G12. §6 is "Meeting cadence, escalation path, and who approves change
  requests" — G6a, G6b, C6. So the insufficiency detector can derive its
  checklist from sow_template.md at runtime instead of from my notes.

  Three decisions change what I build:

● User declined to answer questions
  ⎿  · The whole corpus is ~34KB (~9k tokens) — it fits in one context window.
     What retrieval do you want? (Lexical BM25 + hard engagement pre-filter
     (Recommended) / Embedding-based vector retrieval / Whole corpus in context,
     no retrieval)
     · Reviewers clone the repo and run it. How should the automated quality
     checks run? (Committed golden run + mock LLM (Recommended) / Tests hit the
     live API / Both: mock by default, live behind a flag)
     · The brief's per-section review can't catch defects that span sections —
     the go-live date lands in §3, §4, §8 and §12, and approving each in
     isolation lets an inconsistency through. Add a cross-section gate? (Add a
     global consistency gate (Recommended) / Per-section review only, as the
     brief specifies / Report inconsistencies without blocking)

✻ Churned for 7m 27s

❯ 1 — BM25 with a hard engagement pre-filter.

  Reasoning I want recorded: at 34KB, embeddings buy no recall and add
  nondeterminism plus an API round-trip. More importantly, a similarity
  score cannot guarantee Northgate's $105/hr never reaches Harding's
  commercials — a hard boundary can. Zero deps means the reviewers can
  actually run it, and determinism means the recall test runs offline in
  CI with no API key.

  One thing to fix before you build it. The engagement label cannot be  binary:

- The rate cards, sales playbook, infosec policy and QA checklist arecompany-wide and MUST pass the filter.
- The Harding chat export mentions Northgate by name and must stillpass.
- northgate_sow_executed.md must never pass.

  So I want at least three labels — harding / company / other-client —
  where company passes and other-client is hard-excluded.

  Tell me: where does that label come from, is it derived
  deterministically, and what happens to an ambiguous document? I want
  the failure mode to be exclusion, not inclusion.

  Also record in the README why embeddings and whole-corpus-in-context
  were rejected. The whole-corpus option is the interesting rejection —
  it maximises recall but turns the engagement boundary into a model
  instruction instead of a code boundary.

● Good catch — binary labelling breaks on exactly the three cases you named. Let
  me validate the corrected labeller against the real corpus before I write it
  into the plan.

  Ran 1 shell command (ctrl+o to expand)

● Classifier resolves all 26 docs with zero ambiguity, and all three of your
  test cases land correctly. Now the tripwire that verifies it worked — and its
  limit.

  Ran 1 shell command (ctrl+o to expand)

● Plan mode is off, but you said "before you build it" — so here's the proposal,
  not code. One correction first: my raw set-difference is not usable as a
  tripwire. It returns 183 terms including document, defined, conflicts,
  configuration — words a legitimate SOW will contain. Let me fix the derivation
  and get honest numbers.

  Ran 1 shell command (ctrl+o to expand)

● Tripwire refined to 23 proper nouns exclusive to blocked docs. Two of your
  three cases confirm the design; the third exposes a real boundary I need to be
  honest about.

---

  Architecture

1. Your three questions

  Where the label comes from

  Two independent deterministic signals per document, which must agree:

  ┌────────────┬──────────────┬────────────────────────────────────────────┐
  │   Signal   │    Source    │                  Example                   │
  ├────────────┼──────────────┼────────────────────────────────────────────┤
  │ S1 —       │ the H1 line  │ # Statement of Work — Northgate Logistics  │
  │ subject    │ only         │ → northgate                                │
  ├────────────┼──────────────┼────────────────────────────────────────────┤
  │ S2 — path  │ filename     │ docs/northgate_sow_executed.md → northgate │
  │ stem       │              │                                            │
  └────────────┴──────────────┴────────────────────────────────────────────┘

  Roster resolution within a signal: a client-roster hit beats a company marker
  (so blaugarnet_harding_channel_export → harding, not company); no client hit →
  company; two distinct clients → AMBIGUOUS.

  Scoping the subject signal to the H1 is what makes your case 2 work. Body
  mentions get no vote, so the chat export saying "was looking at the northgate
  sheet" cannot pull the document out of harding.

  The roster itself — harding / northgate / atlas / helios / company marker
  blaugarnet — is committed config declaring who the clients are. It encodes no
  answers about scope, rates, or dates. In a real deployment this is a CRM
  lookup. A partition test pins all 26 files, so a roster edit that changes
  admission fails CI loudly.

  Is it deterministic

  Yes — pure string matching, no model, no embeddings, no randomness. I ran it
  against the corpus:

  partition: harding 9 · company 11 · northgate 3 · atlas 2 · helios 1
  admitted 20 / blocked 6 / total 26 · AMBIGUOUS 0

  All three of your cases land correctly: rate cards + playbook + infosec + QA
  checklist → company → pass; Harding chat export → harding → pass;
  northgate_sow_executed.md → northgate → blocked.

  One consequence you should sign off on: helios_bank_postmortem.md blocks. It's
  another client's engagement document under the rule. The requirements it
  justifies survive anyway — "every SOW names the client-side acceptance
  authority, post-Helios, no exceptions" is independently carried by
  blaugarnet_sales_playbook_extract.md §5, which is company and passes. So
  exclusion costs rationale, not rules. That is the failure mode working as you
  specified, and I'd rather show it than tune the roster to keep a document I
  happen to like.

  What happens to an ambiguous document

  Excluded, always. Five AMBIGUOUS triggers: two or more distinct clients in the
  subject; S1 and S2 disagree; no H1; an unrecognised org in title position;
  empty document. Each exclusion is written to the trace with its reason and
  printed in the run's partition report — excluded, never silent. Current corpus
  produces zero, which means the branch needs synthetic fixtures in tests
  rather than corpus coverage.

---

2. How the system knows the filter worked

  Three checks, decreasing strength:

  V1 — partition report. Every run prints the 26-doc partition with per-document
  reasons. The reviewer sees the boundary before reading the draft.

  V2 — citation provenance audit. This is the guarantee. Every citation in the
  final SOW must resolve to a chunk whose label ∈ {harding, company}.
  Structural, exact, no model, no false positives. Northgate's $105/hr cannot
  enter §8 because no chunk in northgate_sow_executed.md is citable from any
  section.

  V3 — foreign-entity tripwire. Advisory only. Derived by set difference —
  proper nouns appearing exclusively in blocked docs — yielding 23 terms:
  StackWare, Hansen, Duarte, Whitfield, Victor, Lena, Columbus, Fresno, Magento,
  WMS, ERP, VPN…. It still contains calendar noise (Aug, Sep, October,
  Tuesdays) so it needs a stoplist, and it warns rather than blocks.

  The boundary, stated plainly:

  Northgate  -> NOT caught (appears in an in-scope doc)
  105        -> NOT caught (appears in an in-scope doc)
  StackWare  -> CAUGHT

  The tripwire cannot catch 105, and shouldn't try. A Harding transcript utters
  that number itself. That is not contamination — it's a conflict, and it's
  caught downstream by fact-key disagreement on commercials.rate_basis across
  three Harding-labelled sources. Two mechanisms, two failure classes. The
  filter guarantees no foreign document reaches commercials; it does not
  adjudicate a number a Harding source says out loud.

---

3. Authority as a partial order (requirement 2)

  Parsed from header lines that actually exist — 22 of 26 docs carry them — with
  the source line retained as evidence:

  class DocProvenance(BaseModel):
      doc_id: str
      engagement:
  Literal["harding","company","northgate","atlas","helios","AMBIGUOUS"]
      admitted: bool; admit_reason: str
      instrument: Literal["executed_contract","executed_sow","signed_addendum",

  "unsigned_addendum","superseded_addendum","client_correspondence",
                          "client_meeting","internal_meeting","internal_chat",
                          "working_draft","policy","template","reference"]
      audience:    Literal["client_facing","internal_only"]
      status:      Literal["executed","out_for_signature","superseded","draft_in
  complete","current","unknown"]
      restriction:
  Literal["none","not_for_client_distribution","do_not_circulate"]
      doc_date: date | None
      header_evidence: list[str]        # the exact lines each field was parsed
  from

  Resolution is policy, not score — no single authority number, because these
  axes aren't commensurable:

1. audience: internal_only may inform but may never be the sole support for
   client-facing assertive text. Sole support → the claim degrades to an open
   item.
2. status: superseded → barred from support, retained for reporting (so the
   draft can say "v1 stated X").
3. status: out_for_signature → usable, but any claim resting solely on it
   carries a provisional flag rendered in the draft.
4. instrument: executed_contract outranks meeting and correspondence for the
   fact keys it addresses, not globally.
5. Recency is a tiebreaker only within the same instrument class and audience
   — never across them.
6. No strict winner → status conflict, both sides rendered with citations.
   Never a silent pick.

  Rule 1 is what stops Priya's "write it my way, we'll negotiate" from becoming
  governance in a client-facing document — and it does so without knowing C6
  exists. The general policy produces the right behaviour from provenance alone.

---

4. Conflict and insufficiency from evidence (requirement 3)

  Conflict = value disagreement on a shared fact key. The model extracts typed
  claims; code does the comparison. Section-scoped extraction — one call over
  the whole section pool — so all claims for a section share a key vocabulary
  and are actually comparable. Keys are open-vocabulary with deterministic
  canonicalisation, so an unanticipated conflict still surfaces.

  The $105 case falls out without special handling: the scoping-call passage
  yields two claims (blended ~105, role-based off card), the chat yields a third
  — one fact key, two normalised values → conflict. The system never needs to
  understand the retraction. It needs to notice the key is contested and refuse
  to choose silently.

  Insufficiency comes from the template parsing itself. The guidance prose under
  each heading is a comma-separated requirement list:

## 12. Acceptance Criteria

  How deliverables are accepted, by whom, and within what window.
     → required: [acceptance_mechanism, acceptance_authority, acceptance_window]

  Parsed at runtime into required elements, then coverage-checked against
  extracted claims. by whom with no supporting claim → §12 status insufficient,
  gap named explicitly in the draft. G12 is discovered from sow_template.md, not
  from my notes. Same for §6 → cadence / escalation path / CR approver, and §8
  → rates / effort / schedule / terms.

  Nothing from the C1–C12 fixture enters the detector. It lives in
  tests/fixtures/recall_fixture.yaml and scores the detector.

---

5. Pipeline

  ┌─────┬─────────────────┬────────────────────────────────────────┬────────┐
  │  #  │      Stage      │                In → Out                │ Model? │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 1   │ ingest          │ data/ → Document[]                     │ no     │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 2   │ provenance      │ Document[] → DocProvenance[]           │ no     │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 3   │ admission       │ DocProvenance[] → admitted set +       │ no     │
  │     │                 │ partition report                       │        │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 4   │ chunk           │ structure-aware; one chunk per speaker │ no     │
  │     │                 │  turn / message / email                │        │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 5   │ index           │ BM25 + tripwire set                    │ no     │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 6   │ template parse  │ sow_template.md → Section[] + required │ no     │
  │     │                 │  elements                              │        │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 7   │ evidence        │ hard filter → pinned ∪ BM25 top-k →    │ no     │
  │     │ assembly        │ EvidencePool                           │        │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 8   │ claim           │ EvidencePool → Claim[]                 │ yes    │
  │     │ extraction      │                                        │        │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 9   │ quote           │ every quote verbatim substring of its  │ no     │
  │     │ verification    │ chunk, else reject                     │        │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 10  │ analysis        │ Claim[] + policy → Finding[]           │ no     │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 11  │ draft           │ claims + findings → SectionDraft       │ yes    │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 12  │ validate        │ 5 gates below; fail → bounded redraft  │ no     │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 13  │ review CLI      │ approve / reject+comment → redraft     │ no     │
  ├─────┼─────────────────┼────────────────────────────────────────┼────────┤
  │ 14  │ assemble +      │ draft, trace, review log, metrics      │ no     │
  │     │ report          │                                        │        │
  └─────┴─────────────────┴────────────────────────────────────────┴────────┘

  Two model calls per section. Everything adjudicative is code.

  Validation gates (12): every citation resolves · every cited chunk is in-scope
  · every quote verbatim · no uncited assertive sentence · every blocking
  finding surfaced in prose.

  Chunk IDs are line-anchored —
  transcripts/2026-08-05_harding_scoping_call.md#L23 — so a citation is
  checkable against the file by hand. That line is Meera's retraction; I
  verified it earlier.

6. Section output schema

  class SectionDraft(BaseModel):
      section_id: int; title: str
      status:
  Literal["drafted","conflict","insufficient","unsupported","blocked"]
      body_md: str                      # inline [C1] markers
      citations: list[Citation]         # marker → chunk_id, doc_id, quote, line
  span
      findings: list[Finding]
      open_items: list[str]
      provisional: list[str]            # claims resting solely on unsigned
  instruments
      revision: int
      review: ReviewRecord | None       # approved | rejected |
  rejected_unsatisfiable
      tokens: TokenUsage

7. Layout

  src/sow/  cli · config · ingest · provenance · admission · chunking · index
            template · evidence · claims · authority · analysis · draft
            validate · review · assemble · trace · llm · models
  tests/    test_admission (incl. AMBIGUOUS fixtures) · test_provenance ·
  test_authority
            test_analysis · test_validate · test_quality_gates
            fixtures/recall_fixture.yaml · fixtures/golden_run/
  output/   sow_draft.md · trace.jsonl · review_log.json · metrics.json

  Dependencies: anthropic, pydantic, pytest. BM25 hand-rolled, ~40 lines.
  Estimate ~150–250k input / ~35k output per clean run, to be measured not
  asserted.

---

8. What I think is wrong with your brief

  Citation coverage is the wrong headline metric. It measures provenance for
  what's present, and this corpus's worst failures are absences — G12 acceptance
  authority, G8a no derivable fee. A draft can hit 100% citation coverage and
  still ship a SOW with no acceptance authority. Citation integrity belongs as a
  floor gate; the headline should be required-element coverage plus gap
  surfacing.

  Per-section review can't catch the defects that matter most. The go-live date
  lands in §3, §4, §8 and §12. Approving each in isolation lets an inconsistency
  through that no single review sees. I want a cross-section consistency gate
  on the shared claim store before assembly, where an already-approved section
  can be sent back.

  "Rejected sections are redrafted using the comment" assumes every comment is
  satisfiable. A reviewer can ask for something the evidence doesn't support.
  Without a terminal rejected_unsatisfiable state and a retry cap, the loop
  either spins or the model fabricates to comply — which defeats the entire
  design.

  "How you index and retrieve is your design" invites a vector store that would
  make this worse, for the reason you gave: similarity is a score, and a score
  cannot guarantee a boundary. Recorded for the README, including the
  whole-corpus rejection — it maximises recall but converts the engagement
  boundary from a code invariant into a model instruction, which is the one
  thing this corpus punishes.

---

  Two decisions still open. My picks, flagged as mine: tests run against a
  committed golden run with SOW_LLM=mock so pytest passes on a cold clone with
  no key; and the cross-section gate blocks assembly rather than just reporting.
  Say if you'd rather have either the other way, otherwise I'll build to those.

✻ Churned for 3m 45s

※ recap: We're building a system that drafts the Harding SOW from data/, and I've just proposed the full architecture for your review. Next: your sign-off on the two open picks (mock-based tests, blocking cross-section gate) so I can start building. (disable recaps in /config)

❯ Decision 1: yes — mock-based tests against a committed golden run,
  SOW_LLM=mock. Non-negotiable that pytest passes on a cold clone with
  no key.

  Decision 2: no, and here's why. C6 — CR approval authority — is
  unresolvable from evidence, and Meera explicitly said flag it as open
  rather than settled. If the cross-section gate blocks assembly, this
  corpus can produce no draft at all. That fails the brief's own test:
  the draft my code produces end-to-end unassisted is what they evaluate.

  So invert it. The gate blocks silent resolution, never the artifact.
  On cross-section divergence: render both values with their citations,
  mark the affected sections status=conflict, list it in §10, and always
  emit the draft. A run that ends with no file is a failed run.

  Same principle for rejected_unsatisfiable — good catch, keep it, and
  make sure the terminal state still emits the section with the reviewer's
  comment recorded and the reason it couldn't be satisfied. Nothing
  disappears silently.

  One thing to confirm: does a status=conflict section still get written
  into the final markdown with both values visible, or does it get held
  back? It must be written. Show me what §6 Governance looks like in the
  output when C6 fires.

● Confirmed: yes, it is written. status=conflict controls how a section renders,
  never whether. The only thing the gate blocks is a silent pick. Let me pull
  exact line anchors so the example is real rather than illustrative.

  Ran 1 shell command (ctrl+o to expand)

● All six anchors confirmed. §6 is the ideal demonstration because it fires both
  detectors at once — C6 conflict and two insufficiencies (G6a cadence, G6b
  escalation path) — and it still has an uncontested part that drafts normally.

  Here is what output/sow_draft.md contains when C6 fires.

## 6. Governance & Change Management

> **SECTION STATUS: CONFLICT — 1 unresolved · 2 insufficient**
> This section contains a change-control process that is not agreed between
> the
> parties. Both positions are rendered below. Blaugarnet has not selected
> between
> them. Resolve before issue. See §10, items OQ-3, OQ-4, OQ-5.

### 6.1 Change control instrument

  Changes to this SOW require a written change order executed by both parties
  [C1].
  The MSA does not designate an approval body; the operating process is defined
  by
  this SOW [C1].

### 6.2 Meeting cadence

  A steering committee meets monthly, chaired by Harding's PMO lead [C2].

> **INSUFFICIENT — delivery-level meeting cadence.** The template requires a
> meeting cadence. No source in the admitted corpus states a delivery-level
> cadence for this engagement. Not drafted. → OQ-3

### 6.3 Escalation path

> **INSUFFICIENT — escalation path.** The template requires an escalation
> path.
> No admitted source addresses it. Not drafted. → OQ-4

### 6.4 Change request approval authority

> **UNRESOLVED — two positions on record. Not reconciled by evidence.** → OQ-5

  **Position A — stated by Harding, client-facing (2026-08-05).**
  All changes affecting scope, cost or date are approved solely by the Harding
  steering committee, which meets monthly; nothing is approved outside it [C2].

  **Position B — Blaugarnet internal, NOT agreed with Harding (2026-08-19,
  2026-08-20).**
  Change requests under 40 hours of assessed impact are approved jointly by the
  Blaugarnet Delivery Lead and Harding's IT Director; larger requests go to the
  steering committee [C3][C4].

  **Why this is not resolved here.** Position B is supported only by documents
  marked
  internal and not for client distribution [C3][C4], and the same sources record
  it as
  an open negotiation point rather than a settled position [C5][C6]. Blaugarnet
  policy
  bars internal-only material from being the sole support for a client-facing
  commitment, and no admitted client-facing source corroborates Position B.
  Selecting
  either position would assert agreement that the evidence does not establish.

| Ref                                                                           | Source                                                                    | Lines |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ----- |
| C1                                                                            | `docs/harding_msa_summary.md` — *"changes to any SOW require a written |       |
| change order executed by both parties. The MSA is silent on approval bodies;  |                                                                           |       |
| the SOW defines the operating process."*                                      | 13                                                                        |       |
| C2                                                                            | `transcripts/2026-08-05_harding_scoping_call.md` — *"Anything that     |       |
| moves scope, cost or date goes to our steering committee. I chair it, we meet |                                                                           |       |
| monthly. Nothing gets approved outside that committee"*                       | 17                                                                        |       |
| C3                                                                            | `transcripts/2026-08-19_harding_kickoff_prep_internal.md` — *"I want   |       |
| the SOW to say change requests under forty hours of impact are approved by me |                                                                           |       |
| and their IT director jointly, and only bigger ones go to the committee."*    |                                                                           |       |
| 17                                                                            |                                                                           |       |
| C4                                                                            | `chat/blaugarnet_harding_channel_export.md` — *"writing it as joint    |       |
| approval me + jake under 40h impact"*                                         | 20                                                                        |       |
| C5                                                                            | `transcripts/2026-08-19_harding_kickoff_prep_internal.md` — *"Flag it  |       |
| as an open negotiation point, please, not a settled thing."*                  | 23                                                                        |       |
| C6                                                                            | `chat/blaugarnet_harding_channel_export.md` — *"flagged as open point  |       |
| pls. karen will push back hard"*                                              | 21                                                                        |       |

  Three things to note in that output.

  The uncontested part still drafts. §6.1 asserts the change-order requirement
  plainly, because its sole support is an executed contract with nothing
  contradicting it. Conflict is scoped to the fact key, not the section.

  The system never says "Priya is wrong." It says Position B is supported only
  by internal-only sources and no client-facing source corroborates it — which
  is a provenance statement, derived from audience and restriction fields, not a
  judgment about the argument. It reaches the right outcome without knowing C6
  exists.

  [C5] and [C6] are cited as evidence about the claim's status, not about the
  fact. The corpus recording its own uncertainty is itself citable.

  The record behind it:

  {
    "section_id": 6, "title": "Governance & Change Management",
    "status": "conflict", "revision": 1,
    "findings": [
      {"kind":"conflict","fact_key":"governance.cr_approval_authority",
       "claim_ids":["c-041","c-042"],"blocking":false,
       "detail":"2 values; audience differs (client_facing vs internal_only);
  policy yields no strict winner"},
      {"kind":"insufficient","required_element":"meeting cadence
  (delivery-level)",
       "detail":"no admitted claim","blocking":false},
      {"kind":"insufficient","required_element":"escalation path",
       "detail":"no admitted claim","blocking":false}
    ],
    "open_items":["OQ-3","OQ-4","OQ-5"],
    "citations":[/* 6 entries, each chunk_id + verbatim quote + line span */]
  }

  blocking: false throughout — per your inversion, findings change rendering and
  route to §10; they never withhold the artifact.

  §10 rollup, generated from every section's findings:

  | OQ-5 | §6 | Change request approval authority is not agreed. Harding's
  stated
          position is steering-committee-only [C2]; Blaugarnet's internal
  position is a
          40-hour joint-approval threshold [C3][C4], recorded internally as an
  open
          negotiation point [C5][C6]. Requires agreement before execution. |

  On the terminal states, matching what you asked for: rejected_unsatisfiable
  emits the section at its last valid revision, with the reviewer's verbatim
  comment, the redraft attempts made, and the specific reason it couldn't be
  satisfied — typically that the comment requests an assertion no admitted claim
  supports, naming the missing element. The section renders with a status
  banner exactly like the one above. Same invariant as conflict: the run always
  produces output/sow_draft.md, and a run that ends with no file is a failed
  run.

  Both decisions recorded. Ready to build to this — SOW_LLM=mock with a
  committed golden run so pytest passes cold with no key, and the cross-section
  gate blocking silent resolution rather than the artifact.

✻ Baked for 1m 11s

※ recap: Goal is a system that drafts the Harding SOW from data/ with citations, conflict detection, and a CLI review loop. Architecture is agreed and both open decisions are settled. Next action is building it, starting with ingest, provenance parsing, and the engagement filter.
❯ Build it in checkpoints, not one pass. Stop after each and I'll run it.

  CP1 — stages 1-3 plus the partition report. No model calls at all.
  I want to run it and see the 26-doc partition with per-document
  reasons, and confirm 20 admitted / 6 blocked with helios and
  northgate excluded. This is the cheapest proof the whole thesis works,
  so it goes first.

  CP2 — stages 4-7: chunking, template parse, BM25, evidence assembly.
  Still no model calls. I want a command that dumps the evidence pool
  for one section with chunk IDs and scores so I can eyeball what
  retrieval actually selected for §8 Commercials — that's where the
  $105 contamination would show up.

  CP3 — stages 8-10: claim extraction, quote verification, analysis.
  First API use. Run §6 only. I want to see C6 detected from evidence.

  CP4 — stages 11-12: draft and validate, full 12 sections, end to end.

  CP5 — stage 13 review CLI with redraft and the terminal states.

  CP6 — tests, golden run, README.

  Commit after each checkpoint.

● Starting CP1: ingest, provenance, admission, partition report. No model calls.

  Ran 1 shell command (ctrl+o to expand)

● Write(pyproject.toml)
  ⎿  Wrote 22 lines to pyproject.toml
       1 [build-system]
       2 requires = ["setuptools>=68"]
       3 build-backend = "setuptools.build_meta"
       4
       5 [project]
       7 version = "0.1.0"
       8 description = "Grounded Statement of Work drafter for the Hardin
         g Outfitters engagement"
       9 requires-python = ">=3.11"
      10 dependencies = [
     … +13 lines (ctrl+o to expand)

● Write(config\engagements.toml)
  ⎿  Wrote 32 lines to config\engagements.toml
       1 # Engagement roster.
       3 # This file declares WHO THE CLIENTS ARE. It declares no answers
          about scope,
         his would be a
       6 #
       7 # The roster is used only to label each source document with the
       8 # is ABOUT, so that documents belonging to other clients can be
         excluded from
         nsitive
         tle line and
     … +36 lines (ctrl+o to expand)

● Write(src\sow\models.py)
  ⎿  Wrote 178 lines to src\sow\models.py
       1 """Structured records passed between pipeline stages.
       2
       3 Every stage boundary is a validated pydantic model. Nothing down
       4 a bare dict, so a malformed intermediate fails at the boundary t
         hat produced it
       5 rather than three stages later.
       6 """
       8 from __future__ import annotations
       9
      10 from datetime import date
     … +197 lines (ctrl+o to expand)

● Write(src\sow\config.py)
  ⎿  Wrote 100 lines to src\sow\config.py
       1 """Paths and the engagement roster.
       2
       3 No secrets live here. The LLM key is read from the environment a
         t the point of
       4 use (see ``sow.llm``), never from a config file.
       6
       7 from __future__ import annotations
       8
       9 import tomllib
      10 from dataclasses import dataclass
     … +110 lines (ctrl+o to expand)

● Write(src\sow\ingest.py)
  ⎿  Wrote 48 lines to src\sow\ingest.py
       1 """Stage 1 -- read the source corpus.
       2
       3 ``data/`` is read-only. Documents are loaded verbatim, including
       4 because citations are line-anchored and must be checkable agains
         t the file by
       5 hand.
       6 """
       8 from __future__ import annotations
       9
      10 from pathlib import Path
     … +44 lines (ctrl+o to expand)

● Now the provenance parser — the module that reads authority off the corpus.

● Write(src\sow\provenance.py)
  ⎿  Wrote 401 lines to src\sow\provenance.py
       1 """Stage 2 -- parse authority metadata off each document, determ
       2
       3 No model is involved. Every field is read from header lines that
       4 corpus, and the line it was read from is retained so that a prov
       5 is itself citable.
       6
          addendum and an
       8 internal chat message are not comparable on a single scale; coll
       9 number is exactly what produces a recency-only resolver that put
      10 negotiating posture into a client-facing document.
     … +477 lines (ctrl+o to expand)
  ⎿  Found 16 new diagnostic issues in 3 files (ctrl+o to expand)

● Write(src\sow\admission.py)
  ⎿  Wrote 75 lines to src\sow\admission.py
       1 """Stage 3 -- decide which documents may enter the evidence pool
       2
         than a ranking
       4 signal. A similarity score can only make another client's docume
       5 boundary makes it impossible. Northgate's blended USD 105/hour c
       6 Harding's commercials section because no chunk of that document
       7 or citable from any section.
       8
         e established
         nefit of the
     … +82 lines (ctrl+o to expand)

● Write(src\sow\report.py)
  ⎿  Wrote 66 lines to src\sow\report.py
      1 """Human-readable rendering of the corpus partition.
      2
      3 Printed on every run so the reviewer sees the engagement boundary
         before reading
      4 a single drafted word.
      5 """
      6
      7 from __future__ import annotations
      8
      9 from .models import Partition
     … +64 lines (ctrl+o to expand)

● Write(src\sow\cli.py)
  ⎿  Wrote 83 lines to src\sow\cli.py
      1 """Command-line entry point.
      2
      3 Checkpoint 1 exposes one command:
      4
      5     sow partition [--verbose] [--json PATH]
      6
      7 which runs stages 1-3 (ingest, provenance, admission) and prints
        the corpus
      8 partition. No model is called and no API key is required.
      9 """
     … +83 lines (ctrl+o to expand)

  Ran 2 shell commands (ctrl+o to expand)

● Working, with three defects to fix: header scanning bleeds into body text (the
  playbook is misread as executed), the · separator breaks on the Windows
  console, and status falls back on keyword guessing rather than evidence.

● Update(src\sow\provenance.py)
  ⎿  Added 29 lines, removed 4 lines
       90
    91
    92  def header_block(doc: Document) -> list[tuple[int, str]]:
       93 -    """The first``HEADER_LINES`` non-empty lines, with 1-base
          -d line numbers."""
    93 +    """The document's metadata preamble, with 1-based line num
          +bers.
    94 +
    95 +    The preamble is the contiguous run of non-blank lines from
          + the top. Email
    96 +    threads put their metadata after a``---`` fence, so if th
          +e next non-blank
    97 +    line after that run is a fence, the run following it is in
          +cluded too.
    98 +
    99 +    Scanning must stop there. Reading a fixed number of lines
          +instead bleeds
    100 +    into body text -- the sales playbook's fourth guardrail co
          +ntains the phrase
    101 +    "the executed MSA always wins", which a naive scan reads a
          +s the playbook
    102 +    itself being an executed instrument.
    103 +    """
    104      out: list[tuple[int, str]] = []
       95 -    for i, line in enumerate(doc.lines[:HEADER_LINES], start=1
          -):
    96 -        if line.strip():
    97 -            out.append((i, line))
    105 +    lines = doc.lines
    106 +    i = 0
    107 +    n = len(lines)
    108 +
    109 +    for _block in range(2):
    110 +        while i < n and not lines[i].strip():
    111 +            i += 1
    112 +        # A second block is only metadata if it sits behind a
          +horizontal rule.
    113 +        if out:
    114 +            if i >= n or lines[i].strip() not in ("---", "***"
          +, "___"):
    115 +                break
    116 +            i += 1
    117 +            while i < n and not lines[i].strip():
    118 +                i += 1
    119 +        while i < n and lines[i].strip():
    120 +            out.append((i + 1, lines[i]))
    121 +            i += 1
    122 +
    123      return out
      124
    125

● Update(src\sow\provenance.py)
  ⎿  Added 10 lines, removed 8 lines
      244      return audience, f"instrument '{instrument}' is {audience}
           "
      245
    246
    247 -def classify_status(doc: Document) -> tuple[DocStatus, str, st
          -r | None, int | None]:
    248 -    """Read declared lifecycle status off the header.
    247 +def classify_status(
    248 +    doc: Document, doc_date: date | None
    249 +) -> tuple[DocStatus, str, str | None, int | None]:
    250 +    """Read declared lifecycle status off the header preamble.
      251
    252      Supersession declared by a*different* document is applied
            later, by
      251 -    :func:`apply_supersession`.
    253 +    :func:`apply_supersession`. A document carrying a date but
          + no lifecycle
    254 +    marker is``current``; one carrying neither is ``unknown``
          + and is reported
    255 +    rather than assumed current.
    256      """
      257      for line_no, line in header_block(doc):
      258          lowered = line.lower()
     ...
      265          if "executed" in lowered:
      266              return "executed", "header states executed", line,
            line_no
      267
    264 -    for line_no, line in header_block(doc):
    265 -        lowered = line.lower()
    266 -        if any(k in lowered for k in ("version", "updated", "e
          -ffective", "date:")):
    267 -            return "current", "header carries a version or eff
          -ective date", line, line_no
    268 +    if doc_date is not None:
    269 +        return "current", "dated, with no lifecycle marker in
          +the header", None, None
    270
    269 -    return "unknown", "no lifecycle marker in header", None, N
          -one
    271 +    return "unknown", "no lifecycle marker and no date in the
          +header", None, None
    272
    273
    274  def parse_doc_date(doc: Document) -> tuple[date | None, str, s
           tr | None, int | None]:

● Update(src\sow\provenance.py)
  ⎿  Added 1 line, removed 1 line
      314      instrument, inst_reason, inst_line = classify_instrument(d
           oc)
      315      restriction, restr_reason, restr_line, restr_no = classify
           _restriction(doc)
      316      audience, aud_reason = classify_audience(instrument, restr
           iction)
      317 -    status, status_reason, status_line, status_no = classify_s
          -tatus(doc)
    317      doc_date, date_reason, date_line, date_no = parse_doc_date
           (doc)
      318 +    status, status_reason, status_line, status_no = classify_s
          +tatus(doc, doc_date)
    319
    320      evidence = [
      321          FieldEvidence(

  Ran 1 shell command (ctrl+o to expand)

● One regression: the Northgate email lost its Date: line — its metadata sits
  after a blank line with no --- fence, unlike the Harding thread. Tightening
  the second-block rule.

● Update(src\sow\provenance.py)  ⎿  Added 13 lines, removed 4 lines
      106      for _block in range(2):
      107          while i < n and not lines[i].strip():
      108              i += 1
      109 -        # A second block is only metadata if it sits behind a
          -horizontal rule.
    109          if out:
      111 -            if i >= n or lines[i].strip() not in ("---", "***"
          -, "___"):
    110 +            # A second run counts as metadata only behind a ho
          +rizontal rule, or
    111 +            # when it opens with a "**Key:**" field. The brack
          +eted timestamps of
    112 +            # a chat export ("**[2026-08-18 16:40] alicia.font
          +aine:**") fail that
    113 +            # shape deliberately: one of those messages says "
          +out for signature",
    114 +            # which would otherwise be read as the export's ow
          +n lifecycle status.
    115 +            if i >= n:
    116                  break
      113 -            i += 1
    114 -            while i < n and not lines[i].strip():
    117 +            stripped = lines[i].strip()
    118 +            if stripped not in ("---", "***", "___"):
    119 +                if not _METADATA_FIELD.match(stripped):
    120 +                    break
    121 +            else:
    122                  i += 1
      123 +                while i < n and not lines[i].strip():
    124 +                    i += 1
    125          while i < n and lines[i].strip():
      126              out.append((i + 1, lines[i]))
      127              i += 1

● Update(src\sow\provenance.py)
  ⎿  Added 4 lines
      31  _ISO_MONTH = re.compile(r"\b(\d{4})-(\d{2})\b")
      32  _VERSION = re.compile(r"\bversion\s+(\d+)\b", re.IGNORECASE)
      33
    34 +# A "**Key:**" header field, e.g. "**From:**", "**Date:**", "**
         +Status:**".
    35 +# Deliberately does not match a chat export's "**[timestamp] sp
         +eaker:**".
    36 +_METADATA_FIELD = re.compile(r"^\*\*[A-Z][A-Za-z /&'-]{1,20}:\*
         +\*")
    37 +
    38  # "Superseded by X" means THIS document is superseded.
      39  # "Supersedes X" means this document supersedes ANOTHER -- the
          opposite claim.
      40  _SUPERSEDED_BY = re.compile(r"supersed(?:ed|es)\s+by\b", re.IGN
          ORECASE)

  Ran 4 shell commands (ctrl+o to expand)

● pip install -e . works and the sow console script runs. Committing CP1.

  Ran 3 shell commands (ctrl+o to expand)

● Adding .gitattributes now rather than later — CP6's golden-run fixture will
  store verbatim quotes, and a CRLF-normalising checkout on a reviewer's machine
  could break exact-match verification.

  Ran 2 shell commands (ctrl+o to expand)

● CP1 done and committed (0720f9f). Stop here and run it.

  pip install -e .
  sow partition            # or: PYTHONPATH=src python -m sow.cli partition
  sow partition --verbose  # adds per-document reason + the header line each
  date came from
  sow partition --json     # writes output/partition.json

  No model calls, no API key.

  Result — 20 admitted / 6 blocked, matching the prediction:

  by label:   atlas 2  company 11  harding 9  helios 1  northgate 3
  admitted:   20    excluded: 6    total: 26

  EXCLUDED FROM EVIDENCE (cannot be retrieved or cited by any section):
    docs/northgate_sow_executed.md          belongs to another engagement
  'northgate'
    emails/northgate_cutover_email.md       belongs to another engagement
  'northgate'
    internal/helios_bank_postmortem.md      belongs to another engagement
  'helios'
    notes/atlas_retail_discovery_notes.md   belongs to another engagement
  'atlas'
    notes/atlas_retail_status.md            belongs to another engagement
  'atlas'
    transcripts/2026-05-19_northgate_kickoff.md   belongs to another engagement
  'northgate'

  Your three test cases: rate cards + playbook + infosec + QA checklist →
  company → PASS. Chat export → harding → PASS despite naming Northgate in a
  message. Northgate SOW → BLOCK.

  Worth checking when you run it. Provenance came out with the distinctions the
  authority policy will need: harding_scope_addendum_v1 → superseded_addendum /
  superseded, inferred cross-document since v1 never says it's superseded — only
  v2 says it supersedes v1. v2 → unsigned_addendum / out_for_signature. The
  internal prep transcript → internal_only / not_for_client_distribution, parsed
  off its own header line. MSA → executed_contract / executed.

  Three things I changed from the proposal, all worth your eye:

  audience gained a third value, standard. Two values would have barred the rate
  cards from solely supporting anything — and rates exist only on the rate
  cards, so §8 could never be drafted. standard covers established internal
  standards that are legitimately quotable (rate cards, policies, the template);
  internal_only stays reserved for Blaugarnet's own deliberation. Rule 1 is
  unchanged in force.

  Header scanning stops at the metadata preamble instead of reading a fixed line
  count. The naive version read the sales playbook's fourth guardrail — "the
  executed MSA always wins" — and labelled the playbook itself executed. Same
  class of bug made a chat message reading "addendum v2 is out for signature"
  nearly become the chat export's own status.

  Status falls back to current only when a date exists; otherwise unknown,
  reported in NOTES. Four docs land there (sow_template, onboarding, marketing
  one-pager, QA checklist) — none carries a date, and I'd rather report that
  than assume.

  One accepted cost, flagged as you asked: helios_bank_postmortem.md blocks. Its
  rules survive independently — "every SOW names the client-side acceptance
  authority, post-Helios, no exceptions" is in the sales playbook, which is
  company and passes — so exclusion costs rationale, not requirements.

  I also added .gitattributes and a .flake8 (line length 100 — the repo had no
  lint config, so flake8 was defaulting to 79).

  CP2 next: chunking, template parse, BM25, evidence assembly, with a command
  that dumps §8 Commercials' evidence pool and scores. Still no model calls.

✻ Worked for 9m 51s

※ recap: We're building a system that drafts the Harding Outfitters SOW from the mixed-client corpus in data/. CP1 (engagement filter, provenance, admission) is committed and ready for you to run. Next: CP2, chunking plus BM25 evidence assembly.

❯ CP2 — chunking, template parse, BM25, evidence assembly

● CP2: chunking, template parse, BM25, evidence assembly. Adding the stage
  models first.

● Update(src\sow\models.py)
  ⎿  Added 94 lines
      176          for d in self.decisions:
      177              out[d.engagement] = out.get(d.engagement, 0) + 1
      178          return dict(sorted(out.items()))
      179 +
    180 +
    181 +# ------------------------------------------------------------
          +--------------- #
    182 +# Stage 4 -- chunking
    183 +# ------------------------------------------------------------
          +--------------- #
    184 +
    185 +
    186 +class Chunk(BaseModel):
    187 +    """One citable passage, anchored to its source lines.
    188 +
    189 +``text`` is verbatim source: exactly the lines between ``l           +ine_start`` and
    190 +``line_end`` inclusive, joined by newlines and nothing els
          +e. Downstream
    191 +    quote verification checks that every quoted span is a subs
          +tring of this
    192 +    field, so context such as the heading path is kept beside
          +the text rather
    193 +    than folded into it.
    194 +    """
    195 +
    196 +    model_config = ConfigDict(frozen=True)
    197 +
    198 +    chunk_id: str = Field(description="doc_id#L`<start>` or doc_
          +id#L`<start>`-`<end>`.")
    199 +    doc_id: str
    200 +    text: str
    201 +    line_start: int
    202 +    line_end: int
    203 +    heading_path: str | None = None
    204 +    speaker: str | None = None
    205 +    foreign_mentions: list[str] = Field(
    206 +        default_factory=list,
    207 +        description=(
    208 +            "Other engagements named inside this chunk. The ch
          +unk is admitted -- "
    209 +            "its document is in scope -- but the mention is su
          +rfaced so a claim "
    210 +            "drawn from it can be inspected."
    211 +        ),
    212 +    )
    213 +
    214 +
    215 +# ------------------------------------------------------------
          +--------------- #
    216 +# Stage 6 -- template parse
    217 +# ------------------------------------------------------------
          +--------------- #
    218 +
    219 +
    220 +class SectionSpec(BaseModel):
    221 +    """One SOW section, and what the template says it must con
          +tain.
    222 +
    223 +``required_elements`` is parsed from the template's own gu
          +idance prose, not
    224 +    authored here. Section 12's guidance -- "How deliverables
          +are accepted, by
    225 +    whom, and within what window" -- yields the acceptance-aut
          +hority
    226 +    requirement that the corpus never satisfies.
    227 +    """
    228 +
    229 +    section_id: int
    230 +    title: str
    231 +    guidance: str
    232 +    required_elements: list[str]
    233 +    subsections: list[str] = Field(default_factory=list)
    234 +
    235 +    def query(self) -> str:
    236 +        """Retrieval query text for this section."""
    237 +        return " ".join([self.title, *self.subsections, *self.
          +required_elements])
    238 +
    239 +
    240 +# ------------------------------------------------------------
          +--------------- #
    241 +# Stage 7 -- evidence assembly
    242 +# ------------------------------------------------------------
          +--------------- #
    243 +
    244 +
    245 +class ScoredChunk(BaseModel):
    246 +    """A chunk selected for a section's evidence pool, with wh
          +y it was selected."""
    247 +
    248 +    chunk: Chunk
    249 +    score: float
    250 +    selector: Literal["pinned", "retrieved"]
    251 +    rank: int | None = None
    252 +
    253 +
    254 +class EvidencePool(BaseModel):
    255 +    """Everything one section is allowed to draw on.
    256 +
    257 +``excluded_docs`` records how much of the corpus the engag
          +ement boundary
    258 +    removed before ranking ran, so the filter's effect is visi
          +ble per section
    259 +    rather than only in the global partition.
    260 +    """
    261 +
    262 +    section_id: int
    263 +    title: str
    264 +    selected: list[ScoredChunk]
    265 +    candidate_chunks: int
    266 +    excluded_docs: list[str]
    267 +    excluded_chunks: int
    268 +    query: str
    269 +
    270 +    def chunk_ids(self) -> set[str]:
    271 +        """Chunk ids this section may cite. Anything else is a
          + citation failure."""
    272 +        return {sc.chunk.chunk_id for sc in self.selected}
  ⎿  Found 7 new diagnostic issues in 1 file (ctrl+o to expand)

● Write(src\sow\chunking.py)
  ⎿  Wrote 227 lines to src\sow\chunking.py
       1 """Stage 4 -- split documents into citable, line-anchored passag
       2
         n a fixed
       4 window, because a citation has to land on a passage a reader can
       5 scoping call's retraction lives inside a single speaker turn --
       6 comes out around a hundred and five... sorry, no, that's -- igno
       7 splitting that turn would hand a downstream stage the figure wit
         hout the
       9
          rewritten or
     … +253 lines (ctrl+o to expand)

● Write(src\sow\index.py)
  ⎿  Wrote 151 lines to src\sow\index.py
      1 """Stage 5 -- lexical retrieval index, plus the contamination tri
      2
      3 BM25 rather than embeddings. At roughly 34KB the whole corpus fit
      4 context window, so embeddings buy no recall here; they would add
      5 network round-trip and run-to-run nondeterminism. The decisive re
        ason is
        ent unlikely,
      7 never impossible. The engagement boundary is enforced structurall
      8 index is consulted (see ``sow.admission``), and lexical scoring o
      9 survives that boundary.
     … +179 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● Now the template parser — the module that derives required elements from the
  template's own guidance prose.

● Write(src\sow\template.py)
  ⎿  Wrote 129 lines to src\sow\template.py
       1 """Stage 6 -- parse the SOW template into sections and required
       2
          under each
       4 heading enumerates what that section must contain. Section 12 re
       5 deliverables are accepted, by whom, and within what window", whi
       6 requirements -- and the middle one, the client-side acceptance a
       7 never satisfied anywhere in the corpus.
       8
         ion evidence-led.
          would only ever
     … +136 lines (ctrl+o to expand)

● Write(src\sow\evidence.py)
  ⎿  Wrote 106 lines to src\sow\evidence.py
       1 """Stage 7 -- assemble the evidence pool for one section.
       3 Two selectors feed the pool:
       4
         ted contract and
       6   the current addendum) are always present, whatever they score.
       7   retrieval is good at finding passages that share a section's v
         ocabulary and
         es it: the MSA
       9   states net 45 without ever using the word "commercials".
         ngagement
     … +115 lines (ctrl+o to expand)

● Now wiring these into a shared pipeline context plus the three CLI commands.

● Write(src\sow\pipeline.py)
  ⎿  Wrote 82 lines to src\sow\pipeline.py
       1 """Shared run context for stages 1-7.
       2
       3 Built once and reused by every command, so the partition, chunki
       4 draft is built from are exactly the ones the inspection commands
          display.
       5 """
       6
       8
       9 from dataclasses import dataclass
      10 from pathlib import Path
     … +82 lines (ctrl+o to expand)
● Update(src\sow\report.py)
  ⎿  Added 66 lines
       64
    65      add("")
       66      return "\n".join(lines)
       67 +
    68 +
    69 +def _one_line(text: str, width: int) -> str:
    70 +    """Collapse a chunk to a single line for tabular display."
          +""
    71 +    flat = " ".join(text.split())
    72 +    return flat if len(flat) <= width else flat[: width - 1] +
          + "…"
    73 +
    74 +
    75 +def render_sections(sections: list[SectionSpec]) -> str:
    76 +    """Render the parsed template: sections and their required
          + elements."""
    77 +    lines: list[str] = ["", "SOW TEMPLATE -- parsed sections a
          +nd required elements", _RULE]
    78 +    for spec in sections:
    79 +        lines.append(f"section {spec.section_id:>2}. {spec.tit
          +le}")
    80 +        if spec.subsections:
    81 +            lines.append(f"        subsections: {', '.join(spe
          +c.subsections)}")
    82 +        lines.append(f"        guidance:    {spec.guidance or
          +'(none)'}")
    83 +        for element in spec.required_elements:
    84 +            lines.append(f"          required: {element}")
    85 +        lines.append("")
    86 +    lines.append(_RULE)
    87 +    total = sum(len(s.required_elements) for s in sections)
    88 +    lines.append(f"{len(sections)} sections  {total} required
          +elements")
    89 +    lines.append("")
    90 +    return "\n".join(lines)
    91 +
    92 +
    93 +def render_pool(pool: EvidencePool, ctx: RunContext, show_text
          +: bool = True) -> str:
    94 +    """Render one section's evidence pool with selectors, scor
          +es and provenance."""
    95 +    lines: list[str] = []
    96 +    add = lines.append
    97 +    spec = ctx.section(pool.section_id)
    98 +
    99 +    add("")
    100 +    add(f"EVIDENCE POOL -- section {pool.section_id}. {pool.ti
          +tle}")
    101 +    add(_RULE)
    102 +    add(f"required elements : {' | '.join(spec.required_elemen
          +ts)}")
    103 +    add(f"retrieval query   : {_one_line(pool.query, 150)}")
    104 +    add(
    105 +        f"candidate chunks  : {pool.candidate_chunks} admitted
          +"
    106 +        f"    ({pool.excluded_chunks} chunks from {len(pool.ex
          +cluded_docs)} "
    107 +        f"excluded documents were never candidates)"
    108 +    )
    109 +    add(f"selected          : {len(pool.selected)}")
    110 +    add(_RULE)
    111 +    add(
    112 +        f"{'SEL':<10} {'SCORE':>7}  {'AUDIENCE':<14} {'STATUS'
          +:<18} CHUNK"
    113 +    )
    114 +    add(_RULE)
    115 +
    116 +    for scored in pool.selected:
    117 +        chunk = scored.chunk
    118 +        prov = ctx.partition.provenance[chunk.doc_id]
    119 +        selector = scored.selector if scored.selector == "pinn
          +ed" else f"bm25 #{scored.rank}"
    120 +        score = "-" if scored.selector == "pinned" else f"{sco
          +red.score:7.3f}"
    121 +        add(f"{selector:<10} {score:>7}  {prov.audience:<14} {
          +prov.status:<18} {chunk.chunk_id}")
    122 +        if show_text:
    123 +            flag = (
    124 +                f"  [names other engagement: {', '.join(chunk.
          +foreign_mentions)}]"
    125 +                if chunk.foreign_mentions
    126 +                else ""
    127 +            )
    128 +            add(f"{'':<10} {'':>7}  {_one_line(chunk.text, 96)
          +}{flag}")
    129 +
    130 +    add(_RULE)
    131 +    add("")
    132 +    return "\n".join(lines)

  Ran 1 shell command (ctrl+o to expand)

● Now the CLI commands.

● Update(src\sow\cli.py)
  ⎿  Added 68 lines, removed 4 lines
      21  from .report import render_partition
      22
    23
    24 +def _context(args: argparse.Namespace) -> RunContext:
    25 +    """Build the shared run context from common CLI options."""
      26 +    return build_context(
    27 +        data_dir=Path(args.data) if args.data else None,
    28 +        roster_path=Path(args.roster) if args.roster else None,
      29 +    )
    30 +
    31 +
    32 +def _write_json(path_arg: str, payload: str) -> None:
    33 +    """Write a JSON payload, creating parent directories."""
    34 +    out_path = Path(path_arg)
    35 +    out_path.parent.mkdir(parents=True, exist_ok=True)
    36 +    out_path.write_text(payload, encoding="utf-8")
    37 +    print(f"written to {out_path}")
    38 +
    39 +
    40  def cmd_partition(args: argparse.Namespace) -> int:
      41      """Run ingest -> provenance -> admission and report the par
          tition."""
      42      roster = load_roster(Path(args.roster) if args.roster else
          None)
     ...
       46      print(render_partition(partition, verbose=args.verbose))
       47
    48      if args.json:
       33 -        out_path = Path(args.json)
    34 -        out_path.parent.mkdir(parents=True, exist_ok=True)
    35 -        out_path.write_text(partition.model_dump_json(indent=2
          -), encoding="utf-8")
    36 -        print(f"partition written to {out_path}")
    49 +        _write_json(args.json, partition.model_dump_json(inden
          +t=2))
    50
    51      return 0
       52
    53
    54 +def cmd_template(args: argparse.Namespace) -> int:
    55 +    """Show the sections and required elements parsed from the
          + SOW template."""
    56 +    ctx = _context(args)
    57 +    print(render_sections(ctx.sections))
    58 +    if args.json:
    59 +        payload = json.dumps([s.model_dump() for s in ctx.sect
          +ions], indent=2)
    60 +        _write_json(args.json, payload)
    61 +    return 0
    62 +
    63 +
    64 +def cmd_chunks(args: argparse.Namespace) -> int:
    65 +    """Show how documents were split into citable passages."""
       66 +    ctx = _context(args)
    67 +    chunks = ctx.chunks
    68 +    if args.doc:
    69 +        chunks = [c for c in chunks if args.doc in c.doc_id]
    70 +        if not chunks:
    71 +            raise ConfigError(f"no chunks match document filte
          +r: {args.doc}")
    72 +
    73 +    print()
    74 +    for chunk in chunks:
    75 +        prov = ctx.partition.provenance[chunk.doc_id]
    76 +        mark = "PASS " if prov.engagement in ctx.roster.admitt
          +ed_labels else "BLOCK"
    77 +        head = chunk.speaker or chunk.heading_path or ""
    78 +        print(f"{mark} {chunk.chunk_id}")
    79 +        if head:
    80 +            print(f"      ({head})")
    81 +        print(f"      {' '.join(chunk.text.split())[:150]}")
    82 +    print(f"\n{len(chunks)} chunks from {len({c.doc_id for c i
          +n chunks})} documents\n")
    83 +    return 0
    84 +
    85 +
    86 +def cmd_evidence(args: argparse.Namespace) -> int:
    87 +    """Show the evidence pool assembled for one section."""
    88 +    ctx = _context(args)
    89 +    spec = ctx.section(args.section)
    90 +    pool = assemble_pool(spec, ctx.evidence, top_k=args.top_k)
       91 +
    92 +    print(render_pool(pool, ctx, show_text=not args.quiet))
    93 +
    94 +    if args.tripwire:
    95 +        print(f"TRIPWIRE TERMS ({len(ctx.tripwire_terms)}) --
          +proper nouns only in excluded docs:")
    96 +        print("  " + ", ".join(ctx.tripwire_terms))
    97 +        print()
    98 +
    99 +    if args.json:
    100 +        _write_json(args.json, pool.model_dump_json(indent=2))
      101 +
    102 +    return 0
    103 +
    104 +
    105  def build_parser() -> argparse.ArgumentParser:
      106      """Construct the argument parser."""
      107      parser = argparse.ArgumentParser(

● Update(src\sow\cli.py)
  ⎿  Added 45 lines, removed 2 lines
      125          const=str(OUTPUT_DIR / "partition.json"),
      126          help="Also write the full partition record as JSON (de
           fault: output/partition.json).",
      127      )
      128 -    p_part.add_argument("--data", help="Override the data dire
          -ctory.")
    129 -    p_part.add_argument("--roster", help="Override the engagem
          -ent roster TOML.")
    128      p_part.set_defaults(func=cmd_partition)
      129
    130 +    p_tpl = sub.add_parser(
    131 +        "template",
    132 +        help="Show the sections and required elements parsed f
          +rom the SOW template.",
    133 +    )
    134 +    p_tpl.add_argument(
    135 +        "--json",
    136 +        nargs="?",
    137 +        const=str(OUTPUT_DIR / "template.json"),
    138 +        help="Also write the parsed sections as JSON.",
    139 +    )
    140 +    p_tpl.set_defaults(func=cmd_template)
    141 +
    142 +    p_chunks = sub.add_parser("chunks", help="Show how documen
          +ts were split into passages.")
    143 +    p_chunks.add_argument("--doc", help="Only show chunks whos
          +e doc_id contains this string.")
    144 +    p_chunks.set_defaults(func=cmd_chunks)
    145 +
    146 +    p_ev = sub.add_parser(
    147 +        "evidence",
    148 +        help="Show the evidence pool assembled for one section
          +.",
    149 +    )
    150 +    p_ev.add_argument("--section", type=int, required=True, he
          +lp="Section number, 1-12.")
    151 +    p_ev.add_argument(
    152 +        "--top-k",
    153 +        type=int,
    154 +        default=DEFAULT_TOP_K,
    155 +        help=f"How many BM25 hits to select beyond the pinned
          +set (default {DEFAULT_TOP_K}).",
    156 +    )
    157 +    p_ev.add_argument("--quiet", action="store_true", help="Om
          +it chunk text.")
    158 +    p_ev.add_argument(
    159 +        "--tripwire",
    160 +        action="store_true",
    161 +        help="Also print the derived contamination tripwire te
          +rms.",
    162 +    )
    163 +    p_ev.add_argument(
    164 +        "--json",
    165 +        nargs="?",
    166 +        const=str(OUTPUT_DIR / "evidence.json"),
    167 +        help="Also write the pool as JSON.",
    168 +    )
    169 +    p_ev.set_defaults(func=cmd_evidence)
    170 +
    171 +    for sub_parser in (p_part, p_tpl, p_chunks, p_ev):
    172 +        sub_parser.add_argument("--data", help="Override the d
          +ata directory.")
    173 +        sub_parser.add_argument("--roster", help="Override the
          + engagement roster TOML.")
    174 +
    175      return parser
      176
    177

  Ran 2 shell commands (ctrl+o to expand)

● §12 yields "by whom" as a required element — G12 derived from the template at
  runtime, not from my notes. Now the §8 Commercials pool.

  Ran 2 shell commands (ctrl+o to expand)

● Two real defects the eyeball test caught. The rate card tables aren't in the
  pool — §8 has the deal-note rules but not the actual rates. And the tripwire
  contains Milestones and Objectives, which every SOW says.

● Update(src\sow\index.py)
  ⎿  Added 22 lines, removed 2 lines
      60  class Bm25Index:
      61      """Okapi BM25 over chunk text. Hand-rolled to keep the depe
          ndency list empty."""
      62
    63 -    def__init__(self, chunks: list[Chunk], k1: float = 1.5, b:
         - float = 0.75) -> None:
    63 +    def__init__(
    64 +        self,
    65 +        chunks: list[Chunk],
    66 +        retrieval_texts: list[str] | None = None,
    67 +        k1: float = 1.5,
    68 +        b: float = 0.75,
    69 +    ) -> None:
    70 +        """Build the index.
    71 +
    72 +        Args:
    73 +            retrieval_texts: what to index per chunk, parallel
         +to``chunks``.
    74 +                Defaults to the chunk text itself. Callers pass
         + an enriched
    75 +                field -- document title plus heading path plus
         +text -- because a
    76 +                rate card's table body scores almost nothing ag
         +ainst the query
    77 +                "rates" while its title, "Standard Rate Card 20
         +26", scores well.
    78 +                Citation text still comes from``Chunk.text``,
         +which stays
    79 +                verbatim.
    80 +        """
    81          if not chunks:
      82              raise ValueError("cannot build an index over zero c
          hunks")
      83 +        if retrieval_texts is not None and len(retrieval_texts)
         + != len(chunks):
    84 +            raise ValueError("retrieval_texts must be parallel
         +to chunks")
    85          self.chunks = chunks
      86          self.k1 = k1
      87          self.b = b
      88
    70 -        self._tokens: list[list[str]] = [tokenize(c.text) for c
         - in chunks]
    89 +        fields = retrieval_texts if retrieval_texts is not None
         + else [c.text for c in chunks]
    90 +        self._tokens: list[list[str]] = [tokenize(t) for t in f
         +ields]
    91          self._freqs: list[Counter[str]] = [Counter(t) for t in
          self._tokens]
      92          self._lengths: list[int] = [len(t) for t in self._token
          s]
      93          self._avg_len = sum(self._lengths) / len(self._lengths)
           if self._lengths else 0.0

● Update(src\sow\index.py)
  ⎿  Added 1 line, removed 1 line
      142
    143
    144  def build_tripwire_terms(
      145 -    admitted_chunks: list[Chunk], excluded_docs_text: dict[str
          -, str]
    145 +    admitted_docs_text: dict[str, str], excluded_docs_text: di
          +ct[str, str]
    146  ) -> list[str]:
      147      """Proper nouns that occur only in excluded documents.
      148

● Update(src\sow\index.py)
  ⎿  Added 6 lines, removed 1 line
      155      call. Those are conflicts to be detected from evidence, no
           t contamination to
      156      be filtered. The structural guarantee is that every citati
           on must resolve to
      157      an admitted chunk.
      158 +
    159 +    The admitted side must include the SOW template even thoug
          +h the template is
    160 +    never evidence. Without it, "Milestones" and "Objectives"
          +appear only in
    161 +    another client's executed SOW and become tripwire terms --
          + so the check would
    162 +    fire on any draft that uses the section headings it was to
          +ld to use.
    163      """
      159 -    admitted_text = "\n".join(c.text for c in admitted_chunks)
      164 +    admitted_text = "\n".join(admitted_docs_text.values())
    165      admitted_lower = set(tokenize(admitted_text))
      166      admitted_proper = set(_PROPER.findall(admitted_text))
      167

● Update(src\sow\evidence.py)
  ⎿  Added 11 lines, removed 2 lines
      44
    45
    46  def build_evidence_index(
      47 -    all_chunks: list[Chunk], partition: Partition
    47 +    all_chunks: list[Chunk], partition: Partition, doc_titles:
         +dict[str, str]
    48  ) -> EvidenceIndex:
      49      """Restrict chunks to admitted documents and index what rem
          ains.
      50
    ...
      59      if not admitted:
      60          raise RuntimeError("no admitted chunks: every document
          was filtered out")
      61
    62 +    retrieval_texts = [
    63 +        "\n".join(
    64 +            part
    65 +            for part in (doc_titles.get(c.doc_id, ""), c.headin
         +g_path or "", c.text)
    66 +            if part
    67 +        )
    68 +        for c in admitted
    69 +    ]
    70 +
    71      return EvidenceIndex(
      72          chunks=admitted,
      64 -        index=Bm25Index(admitted),
    73 +        index=Bm25Index(admitted, retrieval_texts=retrieval_tex
         +ts),
    74          partition=partition,
      75          excluded_chunk_count=excluded,
      76      )

● Update(src\sow\evidence.py)
  ⎿  Added 4 lines, removed 1 line
       91
    92      query = spec.query()
       93      rank = 0
       94 -    for chunk, score in evidence.index.search(query, top_k=top
          -_k + len(seen)):
    94 +    # Rank the whole admitted set, then take the top_k that ar
          +e not already
    95 +    # pinned. Requesting only top_k from the index would silen
          +tly return fewer,
    96 +    # since pinned chunks occupy many of the highest-scoring p
          +ositions.
    97 +    for chunk, score in evidence.index.search(query, top_k=len
          +(evidence.chunks)):
    98          if chunk.chunk_id in seen:
       99              continue
      100          rank += 1

● Update(src\sow\pipeline.py)
  ⎿  Added 6 lines, removed 6 lines
      63          raise ConfigError(f"SOW template not found at data/{TEM
          PLATE_DOC_ID}")
      64      sections = parse_template(template_doc)
      65
    66 -    evidence = build_evidence_index(chunks, partition)
    66 +    by_id = {doc.doc_id: doc for doc in documents}
    67 +    doc_titles = {doc.doc_id: (doc.h1 or "") for doc in documen
         +ts}
    68 +    evidence = build_evidence_index(chunks, partition, doc_titl
         +es)
    69
    68 -    excluded_text = {
    69 -        d.doc_id: next(doc.text for doc in documents if doc.doc
         -_id == d.doc_id)
    70 -        for d in partition.excluded
    71 -    }
    72 -    tripwire_terms = build_tripwire_terms(evidence.chunks, excl
         -uded_text)
    70 +    admitted_text = {d.doc_id: by_id[d.doc_id].text for d in pa
         +rtition.admitted}
    71 +    excluded_text = {d.doc_id: by_id[d.doc_id].text for d in pa
         +rtition.excluded}
    72 +    tripwire_terms = build_tripwire_terms(admitted_text, exclud
         +ed_text)
    73
    74      return RunContext(
      75          roster=roster,

  Ran 2 shell commands (ctrl+o to expand)

● Found it: BM25 has no stemming, so the query term rates never matches the rate
  card's Hourly rate header. Only 17 chunks scored at all.

● Update(src\sow\index.py)
  ⎿  Added 22 lines, removed 2 lines
      48  _PROPER = re.compile(r"(?<![.!?|#*>\-]\s)(?<!^)\b([A-Z][a-zA-Z]
          {2,})\b", re.MULTILINE)
      49
    50
    51 +def stem(word: str) -> str:
    52 +    """Strip regular plurals only.
    53 +
    54 +    Deliberately not a full stemmer: over-stemming conflates te
         +rms this corpus
    55 +    keeps distinct. Plurals alone matter because the template's
         + guidance is
    56 +    written in the plural ("Rates", "payment terms") while the
         +sources are
    57 +    written in the singular -- the 2026 rate card's table heade
         +r says "Hourly
    58 +    rate", so without this the query term "rates" never matches
         + the rate table
    59 +    at all, and section 8 is assembled without any actual rates
         + in its pool.
    60 +
    61 +    Words ending -ss, -us and -is are left alone, so "business"
         +, "status" and
    62 +    "analysis" survive intact.
    63 +    """
    64 +    if len(word) > 4 and word.endswith("ies"):
    65 +        return word[:-3] + "y"
    66 +    if len(word) > 3 and word.endswith("s") and not word.endswi
         +th(("ss", "us", "is")):
    67 +        return word[:-1]
    68 +    return word
    69 +
    70 +
    71  def tokenize(text: str) -> list[str]:
      52 -    """Lowercase word/number tokens with light stopping.
    72 +    """Lowercase, stopped and plural-normalised tokens.
    73
    74      Numbers survive deliberately: "105", "2400" and "45" are th
          e disputed values
      75      in this corpus.
      76      """
      57 -    return [t for t in _TOKEN.findall(text.lower()) if t not in
         - _STOPWORDS]
    77 +    return [stem(t) for t in _TOKEN.findall(text.lower()) if t
         +not in _STOPWORDS]
    78
    79
    80  class Bm25Index:

  Ran 2 shell commands (ctrl+o to expand)

● §8 now has both rate card tables, both correction messages, the MSA net-45
  clause, and v1's superseded 2,900 hours. Tripwire down to 12, all genuinely
  foreign. Quick sanity across the rest.

  Ran 1 shell command (ctrl+o to expand)

● §6 reaches 4 of 5 C6 passages. The miss — chat#L21 "flagged as open point pls"
  — is a short reply that directly follows a selected message. In this corpus
  retractions and objections live in the adjacent turn, so adding neighbour
  expansion for conversational documents.
● Update(src\sow\models.py)
  ⎿  Added 1 line, removed 1 line
      247
    248      chunk: Chunk
      249      score: float
      250 -    selector: Literal["pinned", "retrieved"]
    250 +    selector: Literal["pinned", "retrieved", "adjacent"]
    251      rank: int | None = None
      252
    253

● Update(src\sow\evidence.py)
  ⎿  Added 12 lines
      26  # Instruments whose chunks are pinned into every section's pool
          .
      27  PINNED_INSTRUMENTS = frozenset({"executed_contract", "unsigned_
          addendum", "signed_addendum"})
      28
    29 +# Instruments where a passage is a turn in a conversation, so t
         +he turns either
    30 +# side of it carry the correction, objection or answer that cha
         +nges its meaning.
    31 +# Meera's "we don't -- i misspoke on the call, was looking at t
         +he northgate
    32 +# sheet" is only a correction because of the message directly a
         +bove it; Meera's
    33 +# "flagged as open point pls" is only meaningful beside the pro
         +posal it answers.
    34 +# Neither reply scores well alone -- both are short and share l
         +ittle vocabulary
    35 +# with a section query -- so lexical ranking finds the claim an
         +d drops the
    36 +# retraction attached to it.
    37 +DIALOGIC_INSTRUMENTS = frozenset(
    38 +    {"internal_chat", "client_meeting", "internal_meeting", "cl
         +ient_correspondence"}
    39 +)
    40 +
    41  DEFAULT_TOP_K = 24
      42
    43

● Update(src\sow\evidence.py)
  ⎿  Added 2 lines
      117          if rank >= top_k:
      118              break
      119
    120 +    selected.extend(_expand_adjacent(selected, evidence, seen)
          +)
    121 +
    122      excluded_docs = sorted(d.doc_id for d in evidence.partitio
           n.excluded)
      123
    124      return EvidencePool(

● Update(src\sow\evidence.py)
  ⎿  Added 36 lines
      130          excluded_chunks=evidence.excluded_chunk_count,
      131          query=query,
      132      )
      133 +
    134 +
    135 +def _expand_adjacent(
    136 +    selected: list[ScoredChunk], evidence: EvidenceIndex, seen
          +: set[str]
    137 +) -> list[ScoredChunk]:
    138 +    """Pull in the turns either side of each retrieved convers
          +ational passage.
    139 +
    140 +    Expansion applies only to dialogic documents. A policy cla
          +use or an addendum
    141 +    bullet states a self-contained fact and needs no neighbour
          +; a chat message or
    142 +    a speaker turn frequently does not.
    143 +    """
    144 +    positions = {chunk.chunk_id: i for i, chunk in enumerate(e
          +vidence.chunks)}
    145 +    added: list[ScoredChunk] = []
    146 +
    147 +    for scored in list(selected):
    148 +        if scored.selector != "retrieved":
    149 +            continue
    150 +        chunk = scored.chunk
    151 +        if evidence.provenance(chunk).instrument not in DIALOG
          +IC_INSTRUMENTS:
    152 +            continue
    153 +
    154 +        idx = positions.get(chunk.chunk_id)
    155 +        if idx is None:
    156 +            continue
    157 +
    158 +        for offset in (-1, 1):
    159 +            neighbour_idx = idx + offset
    160 +            if not 0 <= neighbour_idx < len(evidence.chunks):
      161 +                continue
    162 +            neighbour = evidence.chunks[neighbour_idx]
    163 +            if neighbour.doc_id != chunk.doc_id or neighbour.c
          +hunk_id in seen:
    164 +                continue
    165 +            added.append(ScoredChunk(chunk=neighbour, score=0.
          +0, selector="adjacent"))
    166 +            seen.add(neighbour.chunk_id)
    167 +
    168 +    return added

  Ran 1 shell command (ctrl+o to expand)

● §8 has full recall on C3/C4/C5 (7/7). §6 gets 5/6 — it misses Meera's "flag it
  as an open negotiation point" in the internal transcript, three turns from
  the nearest hit. I'm not widening adjacency to catch it: both C6 positions,
  the MSA clause, and the chat's "flagged as open point pls" are all present, so
  the conflict is detectable. Tuning retrieval until it matches the fixture is
  exactly what your CLAUDE.md warns against.

● Update(src\sow\cli.py)
  ⎿  Added 5 lines, removed 5 lines
       1  """Command-line entry point.
       2
    3 -Checkpoint 1 exposes one command:
    3 +Stages 1-7 are inspectable without calling a model or setting a
         +n API key:
    4
    5 -    sow partition [--verbose] [--json PATH]
    6 -
    7 -which runs stages 1-3 (ingest, provenance, admission) and print
         -s the corpus
    8 -partition. No model is called and no API key is required.
    5 +    sow partition [--verbose]   which documents are evidence, a
         +nd why
    6 +    sow template                sections and required elements
         +parsed from the template
    7 +    sow chunks [--doc X]        how documents were split into c
         +itable passages
    8 +    sow evidence --section N    the pool one section may draw o
         +n, with scores
    9  """
      10
    11  from__future__ import annotations

  Ran 2 shell commands (ctrl+o to expand)

● Everything works. Committing CP2.

  Ran 1 shell command (ctrl+o to expand)

● CP2 done and committed (7120309). Still no model calls, no API key.

  sow evidence --section 8            # the one you wanted to eyeball
  sow evidence --section 8 --tripwire # + derived contamination terms
  sow template                        # required elements parsed from the
  template
  sow chunks --doc scoping_call       # how a document was split

  §8 Commercials — 225 chunks → 172 admitted → 63 selected, zero out-of-scope.
  All seven passages behind the commercial disagreements are present: both rate
  tables, the scoping-call turn including its retraction, both chat corrections,
  the 2025-card commitment, MSA net 45, and v1's superseded 2,900 hours
  retrievable but marked. Across all twelve pools: 0 out-of-scope chunks.

  Four defects the eyeball test caught — this is what CP2 was worth.

  The big one: no stemming, so the query term rates never matched the rate
  card's Hourly rate header. §8 was being assembled with the deal-note rules but
  not a single actual rate. Only 17 chunks scored above zero on the whole
  query. Plural normalisation only — over-stemming would conflate terms this
  corpus keeps apart.

  Ranking chunk text alone buried both rate tables, whose bodies are just
  numbers. Retrieval now indexes doc title + heading path alongside text;
  citations still quote text only.

  The tripwire's admitted side omitted the SOW template, so Milestones and
  Objectives — appearing only in Northgate's SOW among indexed chunks — became
  tripwire terms. The check would have fired on any draft using its own section
  headings. Now 12 terms, all genuinely foreign: StackWare, Hansen, Duarte,
  Whitfield, Victor, Lena, Columbus, Fresno, Magento, WMS, DCs, Derek.

  Short conversational replies score almost nothing alone, so retrieval kept
  finding claims and dropping their retractions. Neighbour expansion now applies
  to dialogic documents only — that recovered chat#L21 "flagged as open point
  pls" and chat#L14 "i misspoke on the call, was looking at the northgate
  sheet".

  One judgment call to flag. §6 recovers 5 of 6 C6 passages; the miss is Meera's
  "flag it as an open negotiation point" in the internal transcript, three
  turns from the nearest hit. I left it. Both C6 positions, the MSA clause and
  the chat's duplicate of that same instruction are all in the pool, so the
  conflict is detectable — and widening adjacency until the fixture goes green
  would make the detector measure your notes rather than the sources.

  Two things I'd expect you to push on when you run it. Pools are 39–68 chunks
  because 26 chunks are pinned into every section — the MSA and addendum v2 in
  full. That's deliberate insurance against BM25 missing a governing clause that
  never uses a section's vocabulary, but it's ~12k tokens of pinned material
  per run, and §3 clearly doesn't need the MSA's confidentiality term. The other
  is §1's required elements: the template's guidance splits into What the
  client is buying... plus in business terms, and the second is a qualifier, not
  a requirement. §2 has the same shape. I left the parser mechanical rather
  than adding cleverness that would risk dropping §12's by whom, which has
  exactly the same grammatical shape and is the most important element in the
  corpus.

  CP3 next: claim extraction, verbatim quote verification, and conflict analysis
  on §6 only. First API use.

✻ Brewed for 11m 37s

❯ CP3 — claim extraction, quote verification, analysis. Run §6 only.

  I want to see C6 detected from evidence rather than from a list, the
  quote verifier rejecting any quote that isn't a verbatim substring of
  its chunk, and the token usage for the run printed at the end.

● CP3 is first API use. Loading the API reference before writing the client.

● Skill(claude-api)
  ⎿  Successfully loaded skill · 4 tools allowed

  Ran 3 shell commands (ctrl+o to expand)

● Credentials present and messages.parse supports output_format. Writing the LLM
  client with mock mode and token accounting.

● Write(src\sow\llm.py)
  ⎿  Wrote 255 lines to src\sow\llm.py
       1 """Model client: structured calls, token accounting, and a mock
       2
       3 Structured output is obtained with ``client.messages.parse(outpu        4 which validates the response against a pydantic model before it           reaches the          es later.        6         8         9 * ``live `` -- the Anthropic API. Needs``ANTHROPIC_API_KEY ``.          en_run``. Needs
     … +292 lines (ctrl+o to expand)

● Update(src\sow\models.py)
  ⎿  Added 103 lines
      270      def chunk_ids(self) -> set[str]:
      271          """Chunk ids this section may cite. Anything else is a
            citation failure."""
      272          return {sc.chunk.chunk_id for sc in self.selected}
      273 +
    274 +
    275 +# ------------------------------------------------------------
          +--------------- #
    276 +# Stage 8 -- claim extraction (the model's structured output)
      277 +# ------------------------------------------------------------
          +--------------- #
    278 +
    279 +
    280 +class ExtractedClaim(BaseModel):
    281 +    """One factual assertion the model found in one passage.""
          +"
    282 +
    283 +    fact_key: str = Field(
    284 +        description="snake_case identifier for the fact, stabl
          +e across passages."
    285 +    )
    286 +    value: str = Field(description="Shortest precise form of t
          +he value.")
    287 +    chunk_id: str = Field(description="The passage this came f
          +rom.")
    288 +    quote: str = Field(description="Verbatim span copied from
          +that passage.")
    289 +    supports_elements: list[str] = Field(default_factory=list)
      290 +
    291 +
    292 +class ClaimExtraction(BaseModel):
    293 +    """The model's full response for one section."""
    294 +
    295 +    claims: list[ExtractedClaim] = Field(default_factory=list)
      296 +
    297 +
    298 +class Claim(BaseModel):
    299 +    """An extracted claim after verification, with provenance
          +attached."""
    300 +
    301 +    claim_id: str
    302 +    fact_key: str
    303 +    value: str
    304 +    value_norm: str
    305 +    chunk_id: str
    306 +    doc_id: str
    307 +    quote: str
    308 +    supports_elements: list[str] = Field(default_factory=list)
      309 +    verified: bool = True
    310 +    reject_reason: str | None = None
    311 +
    312 +
    313 +# ------------------------------------------------------------
          +--------------- #
    314 +# Stage 10 -- analysis
    315 +# ------------------------------------------------------------
          +--------------- #
    316 +
    317 +FindingKind = Literal[
    318 +    "conflict",
    319 +    "insufficient",
    320 +    "provisional",
    321 +    "internal_only_support",
    322 +    "superseded_only_support",
    323 +    "unverified_claim",
    324 +]
    325 +
    326 +
    327 +class Position(BaseModel):
    328 +    """One distinct value on a contested fact, and what suppor
          +ts it."""
    329 +
    330 +    value: str
    331 +    value_norm: str
    332 +    claim_ids: list[str]
    333 +    doc_ids: list[str]
    334 +    audiences: list[str]
    335 +    instruments: list[str]
    336 +    best_rank: int
    337 +    latest_date: date | None
    338 +    internal_only: bool = Field(
    339 +        description="Every document supporting this value is i
          +nternal deliberation."
    340 +    )
    341 +
    342 +
    343 +class Finding(BaseModel):
    344 +    """Something the draft must surface rather than resolve si
          +lently."""
    345 +
    346 +    kind: FindingKind
    347 +    detail: str
    348 +    fact_key: str | None = None
    349 +    required_element: str | None = None
    350 +    claim_ids: list[str] = Field(default_factory=list)
    351 +    positions: list[Position] = Field(default_factory=list)
    352 +    blocking: bool = Field(
    353 +        default=False,
    354 +        description=(
    355 +            "Findings change how a section renders; they never
          + withhold it. A run "
    356 +            "that ends with no draft file is a failed run."
    357 +        ),
    358 +    )
    359 +
    360 +
    361 +AnalysisStatus = Literal["clean", "conflict", "insufficient",
          +"conflict_and_insufficient"]
    362 +
    363 +
    364 +class SectionAnalysis(BaseModel):
    365 +    """Everything stages 8-10 concluded about one section."""
      366 +
    367 +    section_id: int
    368 +    title: str
    369 +    status: AnalysisStatus
    370 +    claims: list[Claim]
    371 +    rejected: list[Claim]
    372 +    findings: list[Finding]
    373 +    covered_elements: list[str]
    374 +    missing_elements: list[str]
    375 +    pool_size: int

● Write(src\sow\claims.py)
  ⎿  Wrote 186 lines to src\sow\claims.py
       1 """Stages 8-9 -- extract claims from a section's evidence, then
       2
          the span each
       4 one came from. It is explicitly told not to resolve disagreement
       5 that contradicts another passage yields two claims under one fac
       6 comparison happens in code (see ``sow.analysis``).
       8 Verification is deterministic. A quote must be a character-for-c
         haracter
          must be one
          rejected and
     … +215 lines (ctrl+o to expand)

● Now the authority policy — the module that decides when a disagreement is
  resolvable and when it must stay visible.

● Write(src\sow\authority.py)
  ⎿  Wrote 184 lines to src\sow\authority.py
       1 """The authority policy: when a disagreement resolves, and when
       2
       3 Authority is a partial order, not a score. The rules below are a
         pplied in order
         int -- a policy
       5 that always resolves is just a recency sort with extra steps.
       7 Rules:
       8
       9 1. A superseded document cannot support an assertion. It stays r
      10    the draft can report what it said.
     … +205 lines (ctrl+o to expand)

● Write(src\sow\analysis.py)  ⎿  Wrote 197 lines to src\sow\analysis.py
      1 """Stage 10 -- detect conflict and insufficiency. No model is inv
      2
      3 Both detections are structural:
      5 * **Conflict** is value disagreement on a shared fact key. Claims
         are grouped by
        es, the
      7   authority policy is asked for a winner and frequently declines.
      8   knows which facts are contested in this corpus -- the disagreem
        ent is found by
        ame way.
     … +218 lines (ctrl+o to expand)

● Now the trace writer, the analysis renderer, and the CLI command.

● Write(src\sow\trace.py)
  ⎿  Wrote 46 lines to src\sow\trace.py
       1 """Run trace: an append-only JSONL record of how each section wa
         s assembled.
       3 One object per event. Enough to reconstruct, for any section, wh
         at was
       4 retrieved, what was sent to the model, what came back, what was
       5 what was flagged -- without re-running anything.
       6 """
       7
       9
      10 import json
     … +43 lines (ctrl+o to expand)

● Update(src\sow\report.py)
  ⎿  Added 90 lines
      131      add(_RULE)
      132      add("")
      133      return "\n".join(lines)
      134 +
    135 +
    136 +_KIND_LABEL = {
    137 +    "conflict": "CONFLICT",
    138 +    "insufficient": "INSUFFICIENT",
    139 +    "provisional": "PROVISIONAL",
    140 +    "internal_only_support": "INTERNAL-ONLY",
    141 +    "superseded_only_support": "SUPERSEDED-ONLY",
    142 +    "unverified_claim": "REJECTED",
    143 +}
    144 +
    145 +
    146 +def render_analysis(analysis: SectionAnalysis, ctx: RunContext
          +) -> str:
    147 +    """Render claims, quote-verification results and findings
          +for one section."""
    148 +    lines: list[str] = []
    149 +    add = lines.append
    150 +    provs = ctx.partition.provenance
    151 +
    152 +    add("")
    153 +    add(f"ANALYSIS -- section {analysis.section_id}. {analysis
          +.title}")
    154 +    add(_RULE)
    155 +    add(f"status            : {analysis.status.upper()}")
    156 +    add(f"evidence pool     : {analysis.pool_size} passages")
      157 +    add(
    158 +        f"claims            : {len(analysis.claims)} verified,
          + "
    159 +        f"{len(analysis.rejected)} rejected"
    160 +    )
    161 +    add(f"required elements : {len(analysis.covered_elements)}
          + covered, "
    162 +        f"{len(analysis.missing_elements)} missing")
    163 +    add(_RULE)
    164 +
    165 +    add("")
    166 +    add("QUOTE VERIFICATION")
    167 +    add(f"  {len(analysis.claims)}/{len(analysis.claims) + len
          +(analysis.rejected)} quotes "
    168 +        f"confirmed as verbatim substrings of the passage they
          + cite")
    169 +    for claim in analysis.rejected:
    170 +        add(f"  REJECTED {claim.claim_id}  fact_key={claim.fac
          +t_key}")
    171 +        add(f"           {claim.reject_reason}")
    172 +        add(f"           quote: {_one_line(claim.quote, 88)}")
      173 +
    174 +    by_key: dict[str, list] = {}
    175 +    for claim in analysis.claims:
    176 +        by_key.setdefault(claim.fact_key, []).append(claim)
    177 +
    178 +    add("")
    179 +    add(f"CLAIMS BY FACT KEY ({len(by_key)} keys)")
    180 +    for fact_key in sorted(by_key):
    181 +        members = by_key[fact_key]
    182 +        values = {c.value_norm for c in members}
    183 +        marker = "  <-- values disagree" if len(values) > 1 el
          +se ""
    184 +        add(f"  {fact_key}{marker}")
    185 +        for claim in members:
    186 +            prov = provs[claim.doc_id]
    187 +            add(
    188 +                f"      {claim.claim_id}  {claim.value!r}"
    189 +                f"   [{prov.audience}/{prov.instrument}/{prov.
          +status}]"
    190 +            )
    191 +            add(f"          {claim.chunk_id}")
    192 +            add(f"          “{_one_line(claim.quote, 92)}”")
    193 +
    194 +    add("")
    195 +    add(f"FINDINGS ({len(analysis.findings)})")
    196 +    if not analysis.findings:
    197 +        add("  none")
    198 +    for finding in analysis.findings:
    199 +        label = _KIND_LABEL.get(finding.kind, finding.kind.upp
          +er())
    200 +        subject = finding.fact_key or finding.required_element
          + or ""
    201 +        add(f"  [{label}] {subject}")
    202 +        add(f"      {finding.detail}")
    203 +        for position in finding.positions:
    204 +            flag = " (internal-only support)" if finding.kind
          +== "conflict" and position.internal_only else ""
    205 +            add(
    206 +                f"      value: {position.value!r}{flag}"
    207 +                f"  <- {', '.join(position.doc_ids)}"
    208 +            )
    209 +            add(
    210 +                f"          audience={'/'.join(position.audien
          +ces)} "
    211 +                f"instrument={'/'.join(position.instruments)}
          +"
    212 +                f"claims={', '.join(position.claim_ids)}"
    213 +            )
    214 +
    215 +    if analysis.missing_elements:
    216 +        add("")
    217 +        add("MISSING REQUIRED ELEMENTS (no admitted source sup
          +ports these)")
    218 +        for element in analysis.missing_elements:
    219 +            add(f"  - {element}")
    220 +
    221 +    add(_RULE)
    222 +    add("")
    223 +    return "\n".join(lines)

  Ran 1 shell command (ctrl+o to expand)

● Now the analyze command, with the tamper flag so the quote verifier can be
  seen firing.

● Update(src\sow\cli.py)
  ⎿  Added 77 lines
      104      return 0
      105
    106
    107 +def cmd_analyze(args: argparse.Namespace) -> int:
    108 +    """Extract claims for one section, verify quotes, and anal
          +yse the result."""
    109 +    ctx = _context(args)
    110 +    spec = ctx.section(args.section)
    111 +    pool = assemble_pool(spec, ctx.evidence, top_k=args.top_k)
      112 +    llm = LlmClient(fixture_dir=FIXTURE_DIR)
    113 +
    114 +    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    115 +    with Trace(OUTPUT_DIR / "trace.jsonl") as trace:
    116 +        trace.event(
    117 +            "partition",
    118 +            admitted=[d.doc_id for d in ctx.partition.admitted
          +],
    119 +            excluded=[d.doc_id for d in ctx.partition.excluded
          +],
    120 +        )
    121 +        trace.event(
    122 +            "evidence_pool",
    123 +            section_id=spec.section_id,
    124 +            query=pool.query,
    125 +            selected=[
    126 +                {"chunk_id": s.chunk.chunk_id, "selector": s.s
          +elector, "score": s.score}
    127 +                for s in pool.selected
    128 +            ],
    129 +            candidate_chunks=pool.candidate_chunks,
    130 +            excluded_chunks=pool.excluded_chunks,
    131 +        )
    132 +
    133 +        print(f"calling model ({llm.backend} backend, {llm.mod
          +el}) for section {spec.section_id}...")
    134 +        extraction = llm.parse(STAGE, SYSTEM_PROMPT, build_use
          +r_prompt(spec, pool), ClaimExtraction)
    135 +
    136 +        if args.tamper_quotes and extraction.claims:
    137 +            victim = extraction.claims[0]
    138 +            original = victim.quote
    139 +            victim.quote = victim.quote.replace(" ", " slightl
          +y ", 1) or "not in the source"
    140 +            print(
    141 +                "\n[--tamper-quotes] corrupted one quote after
          + extraction to exercise "
    142 +                f"the verifier:\n    was: {original[:70]!r}\n
          +   now: {victim.quote[:78]!r}\n"
    143 +            )
    144 +
    145 +        trace.event(
    146 +            "claim_extraction",
    147 +            section_id=spec.section_id,
    148 +            system_prompt_chars=len(SYSTEM_PROMPT),
    149 +            user_prompt_chars=len(build_user_prompt(spec, pool
          +)),
    150 +            raw_claims=len(extraction.claims),
    151 +        )
    152 +
    153 +        verified, rejected = verify_claims(extraction, pool)
    154 +        trace.event(
    155 +            "quote_verification",
    156 +            section_id=spec.section_id,
    157 +            verified=[c.claim_id for c in verified],
    158 +            rejected=[
    159 +                {"claim_id": c.claim_id, "reason": c.reject_re
          +ason, "quote": c.quote}
    160 +                for c in rejected
    161 +            ],
    162 +        )
    163 +
    164 +        analysis = analyse_section(spec, pool, verified, rejec
          +ted, ctx.partition.provenance)
    165 +        trace.event(
    166 +            "analysis",
    167 +            section_id=spec.section_id,
    168 +            status=analysis.status,
    169 +            findings=[f.model_dump(mode="json") for f in analy
          +sis.findings],
    170 +            missing_elements=analysis.missing_elements,
    171 +        )
    172 +        trace.event("token_usage", **llm.usage.per_stage)
    173 +
    174 +    print(render_analysis(analysis, ctx))
    175 +    print(llm.usage.summary(llm.model))
    176 +    print(f"trace written to {OUTPUT_DIR / 'trace.jsonl'}")
    177 +
    178 +    if args.json:
    179 +        _write_json(args.json, analysis.model_dump_json(indent
          +=2))
    180 +
    181 +    return 0
    182 +
    183 +
    184  def build_parser() -> argparse.ArgumentParser:
      185      """Construct the argument parser."""
      186      parser = argparse.ArgumentParser(

  Ran 1 shell command (ctrl+o to expand)

● First live run — §6 only.

  Ran 2 shell commands (ctrl+o to expand)

● The API key in this environment is present and well-formed (sk-ant-api…, 108
  chars) but the API rejects it as invalid — and there's no ant CLI or OAuth
  profile to fall back to. I can't complete the live extraction call. Verifying
  everything that doesn't depend on it.

  Ran 2 shell commands (ctrl+o to expand)

● Exit code 2 — fails loudly, no silent fallback to live. Now exercising the
  detection logic, which is the part of CP3 that isn't the model. Building a
  stand-in for the extraction response from real corpus quotes.

  Made 1 scratchpad edit +107, ran 1 shell command (ctrl+o to expand)

● Detection works. Fixing one cosmetic issue (smart quotes mangle on the Windows
  console) and aligning the SDK pin to the version I verified.

  Ran 2 shell commands (ctrl+o to expand)

● CP3 committed (6b89bb3) — but with one thing you need to know before you run
  it.

  The API key here is invalid

  ANTHROPIC_API_KEY is set and well-formed (sk-ant-api…, 108 chars), but the API
  returns 401 authentication_error: API key is invalid. No ant CLI, no OAuth
  profile to fall back on. I could not complete a live extraction call. Your key
  presumably works — sow analyze --section 6 should just run.

  What I verified without it

  The detection logic is code, not model, so all of it is exercisable. I ran
  stages 9–10 against a stand-in for the extraction response, built from quotes
  I first asserted are verbatim corpus text. verify_claims and analyse_section
  were not modified or bypassed.

  C6 detected from evidence:

  [CONFLICT] change_request_approval_authority
      one value is supported only by internal documents while another has
  client-facing
      or standard support; the disagreement is unresolved between the parties,
  not
      merely between sources

    value: 'Harding steering committee only'          <-
  2026-08-05_harding_scoping_call.md
          audience=client_facing  instrument=client_meeting
      value: 'joint approval under 40h impact' (internal-only support)  <- chat
  export
          audience=internal_only  instrument=internal_chat
      value: 'joint delivery lead and IT director under 40 hours' (internal-only
  support)
          audience=internal_only  instrument=internal_meeting

  Nothing in authority.py mentions C6, governance, or Priya. The rule is general
  — a value supported only by internal deliberation, against a value with
  client-facing support, does not resolve — and it fires here because provenance
  says so.

  Quote verifier rejecting non-verbatim quotes — I fed it two bad claims among
  six good ones:

  6/8 quotes confirmed as verbatim substrings of the passage they cite
  REJECTED s6-c007  quote is not a substring of the cited passage
           quote: Nothing gets approved outside of that committee
  REJECTED s6-c008  cites docs/northgate_sow_executed.md#L26, which is not in
           this section's evidence pool

  The first differs from the source by one inserted word. The second is the
  contamination case — a Northgate chunk cited from §6 is rejected structurally,
  because it was never in the pool.

  Insufficiency: [INSUFFICIENT] escalation path — derived from the template's
  guidance, satisfied by no admitted source. Section status:
  CONFLICT_AND_INSUFFICIENT.

  Mock backend fails loudly: with no recording it exits 2 and says the golden
  run is stale, rather than silently reaching the network.

  Token usage

  The summary block prints model, calls, input/output tokens, a per-stage
  breakdown and estimated USD — but I have no real numbers to show you, since no
  call completed. You'll see it at the end of your run.

  Two honest limitations

  The extraction prompt is unvalidated. Everything downstream is tested; the
  call itself has never executed. The first real thing to check is whether the
  model actually emits stable fact_key values across passages — that's the hinge
  the whole detector turns on.

  Normalisation split one position in two. 'joint delivery lead and IT director
  under 40 hours' and 'joint approval under 40h impact' are the same position
  stated twice, but normalise differently, so they render as separate values. It
  doesn't break the conflict — the finding is still correct — but §6 would show
  three values where there are two. The lever is the prompt (value must be the
  shortest precise form), not more aggressive normalisation, which would start
  merging things that genuinely differ.

  The stand-in lives in my scratchpad, not the repo — it becomes a proper test
  in CP6, and the golden run must come from a real call, not from anything I
  authored.

  CP4 next: draft and validate, all 12 sections end to end.

✻ Crunched for 9m 0s

※ recap: Goal: build a system that drafts the Harding SOW from data/ with citations, conflict detection, and a review loop. CP1-CP3 are committed and working; CP4 (draft plus validate, all 12 sections) is next. First, note that the API key here returns 401, so live runs need a working key.

┌─ RESTORED ──────────────────────────────────────────────────────────────────┐
│ The turn below was dropped by the context compaction above and has been      │
│ restored from the session. Content is accurate; tool output was already      │
│ collapsed by /export and is summarised in the same style as the rest.        │
└─────────────────────────────────────────────────────────────────────────────┘

❯ i have added open ai API key in .env

  CP4 — draft and validate, all 12 sections, end to end. Write
  output/sow_draft.md and the trace. Print total token usage for the run.

● Let me verify the key with one cheap call before running all 12 sections.

  Ran 1 shell command (ctrl+o to expand)

● Key authenticates but the account has zero quota — 429 insufficient_quota,
  not a 401. So the key is fine; the OpenAI account needs billing credit before
  any live call will run.

  I'll build CP4 completely so it runs the moment quota exists, and verify every
  deterministic part now.

  Made 1 edit to src/sow/models.py (+118), ran 1 shell command (ctrl+o to expand)

● Now the drafting stage. The model writes prose only — banners, conflict
  blocks and the citation table are rendered by code from Finding records.

  Wrote src/sow/draft.py (+196) (ctrl+o to expand)

● Wrote src/sow/validate.py (+147) (ctrl+o to expand)

● Now the assembler — it renders banners, conflict blocks and gap notices from
  Finding records, plus the cross-section check.

  Wrote src/sow/assemble.py (+272) (ctrl+o to expand)

● Now the orchestrator that runs all 12 sections end to end.

  Wrote src/sow/run.py (+232), made 1 edit to src/sow/cli.py (+47),
  ran 2 shell commands (ctrl+o to expand)




● Now verifying the whole path end to end without live calls. Building a fake
  client that returns structurally valid responses derived from real corpus
  text.

  Made 1 scratchpad edit +108, ran 1 shell command (ctrl+o to expand)

● Pipeline runs end to end and writes the document — but zero citations and zero
  draft calls: my fake made every fact contested, so drafting was skipped
  entirely. That's a defect in the fake, not the pipeline. Fixing it to produce
  a realistic mix.

  Ran 1 shell command (ctrl+o to expand)

● Approaching your 5-hour usage limit — Claude will wrap up the current
  step.

● Full path now exercised: 24 calls (12 extract + 12 draft), drafting runs,
  cross-section divergence caught and disclosed. Committing.

  Ran 1 shell command (ctrl+o to expand)
  ⎿  PostToolUse:Bash says: Tip: Run /ultrareview before you push to catch bugs
     with a cloud-based multi-agent review — 3 free reviews left.

● CP4 committed (00a9eda). The banner, conflict block, gap notices and citation
  table all render correctly — the repetitive prose above is my fake model, not
  the pipeline.

  sow draft                      # all 12 sections
  sow draft --sections 6,8       # subset
  Writes output/sow_draft.md, output/trace.jsonl, output/run.json, and prints
  total token usage.

  Blocker: your OpenAI account has no quota. The key authenticates fine — the
  error is 429 insufficient_quota, not 401. Add billing credit and sow draft
  runs as-is; nothing else needs changing.

  Verified without live calls (only LlmClient.parse substituted; retrieval,
  verification, analysis, authority, validation, cross-section and assembly all
  ran unmodified):

- 12 sections written, 24 model calls, sow_draft.md 37.8 KB / 682 lines, 64
  trace events
- Cross-section divergence detected and disclosed rather than reconciled
- Independent audit of the artifact: every citation resolves to an admitted
  document, no excluded document cited, no foreign tripwire term present

  Design point worth your eye: the model never writes disclosures. Banners,
  conflict blocks and gap notices are rendered by assemble.py from Finding
  records, so a model that ignores instructions can't suppress a disclosure it
  never authored. Drafting only receives claims the authority policy resolved,
  with contested keys passed in as explicit do-not-write lists.

  One real finding from the first fake run: when every fact is contested,
  drafting is skipped entirely and the document is pure disclosure with zero
  prose. Defensible, but you should decide whether that's the behaviour you want
  — I'd flag it as worth a minimum-prose floor.

  Most impactful remaining work

- CP5 — review CLI: approve/reject per section with comment-driven redraft,
  plus the rejected_unsatisfiable terminal state (models and rendering already
  exist; the loop does not).
- CP6 — tests, golden run, README: pytest passing cold with SOW_LLM=mock; the
  golden run must come from one real call, so it's gated on quota. The C1–C12
  recall fixture and the CP3 stand-in both become proper tests.
- One live run to validate the prompts. Extraction and drafting have never
  executed against a real model — specifically whether fact_key stays stable
  across passages, which is the hinge the whole detector turns on.

✻ Baked for 6m 18s

❯ my Open AI key don't have balance
  use anthropic key added in .env file
  ⎿  Found 5 new diagnostic issues in 1 file (ctrl+o to expand)

● Let me see what's in .env now (without printing key values).

  Ran 1 shell command (ctrl+o to expand)

● Only ANTHROPIC_API_KEY now. Caution: same length and prefix as the key that
  401'd earlier, and your shell still exports one that would shadow it. Testing
  the .env value directly before rewriting anything.

  Ran 1 shell command (ctrl+o to expand)

● .env key works — and it's a different key from the one your shell exports.
  That's the trap I flagged: my loader gives real env vars precedence, so the
  stale shell key would shadow the working one. Fixing that, and making the
  client support both providers so this can't bite again.

● Update(src\sow\config.py)
  ⎿  Added 19 lines, removed 7 lines
      35  def load_dotenv(path: Path | None = None) -> list[str]:
      36      """Load ``KEY=value`` pairs from ``.env`` into the environm
          ent.
      37
    38 -    Hand-rolled rather than pulling in python-dotenv: it is twe
         -nty lines and the
    38 +    Hand-rolled rather than pulling in python-dotenv: it is thi
         +rty lines and the
    39      dependency list is meant to stay short enough that a review
          er can install
      40      this on a clean machine without thinking about it.
      41
    42 -    Real environment variables always win, so an exported key i
         -s never silently
    43 -    overridden by a stale file. Returns the names of the variab
         -les it set, for
    44 -    the startup report.
    42 +``.env`` **overrides** an exported variable of the same nam
         +e, which is the
    43 +    opposite of the usual convention and is deliberate. ``.env`          +` is this
    44 +    project's documented way to supply a key, so a value writte
         +n there is the
    45 +    more recent intent; a shell variable left over from an earl
         +ier session is
    46 +    the likelier stale one. Silently preferring the stale expor
         +t produces the
    47 +    worst possible symptom -- a freshly pasted key that appears
         + to be rejected.
    48 +
    49 +    Any override is announced on stderr rather than done quietl
         +y. Returns the
    50 +    names of every variable set, for the startup report.
    51      """
      52      env_path = path or ENV_PATH
      53      if not env_path.is_file():
     ...
      65              continue
      66          key = key.strip()
      67          value = value.strip().strip('"').strip("'")
      62 -        if key and key not in os.environ:
    63 -            os.environ[key] = value
    64 -            applied.append(key)
    68 +        if not key:
    69 +            continue
    70 +        if key in os.environ and os.environ[key] != value:
    71 +            print(
    72 +                f"note: {key} from {env_path.name} overrides th
         +e exported shell value",
    73 +                file=sys.stderr,
    74 +            )
    75 +        os.environ[key] = value
    76 +        applied.append(key)
    77      return applied
      78
    79

● Now the client — supporting both providers, auto-detected from whichever key
  is present.

● Write(src\sow\llm.py)
  ⎿  Added 156 lines, removed 95 lines
       1  """Model client: structured calls, token accounting, and a mock
           backend.
       2
    3 -This is the only provider-specific module in the pipeline. Ever
         -ything
    4 -downstream consumes validated pydantic models and is indifferen
         -t to which API
    5 -produced them, so swapping providers means replacing this file
         -and nothing else.
    3 +This is the only provider-specific module. Everything downstrea
         +m consumes
    4 +validated pydantic models and never sees a provider type, so su
         +pport for a
    5 +second API costs one method here and nothing anywhere else.
    6
    7 -Structured output goes through``chat.completions.parse(respons          -e_format=...)``,
    8 -which validates the response against a pydantic model before it
         - reaches the
    9 -pipeline. A malformed response fails here rather than three sta
         -ges later.
    7 +Two providers, chosen by whichever key is present (or forced wi
         +th
    8 +``SOW_PROVIDER``):
    9
    11 -Two backends:
    10 +*``anthropic`` -- ``ANTHROPIC_API_KEY``, via ``messages.parse`          +`                                                                     11 +* ``openai ``   --``OPENAI_API_KEY ``, via ``chat.completions.p
         +arse ``                                                               12         13 -*``live `` -- the OpenAI API. Needs``OPENAI_API_KEY ``.              14 -* ``mock `` -- replays a recorded run from``tests/fixtures/gol
         -den_run ``. Needs                                                      15 -  no key, so the quality checks run on a cold clone.                  13 +Two backends, chosen with ``SOW_LLM ``:                                14         17 -Selected with the ``SOW_LLM ``environment variable;``live ``is          - the default.                                                         15 +*``live ``-- call the API. Default.                                  16 +*``mock ``-- replay a recorded run from``tests/fixtures/golde
         +n_run ``. Needs no                                                     17 +  key, so the quality checks run on a cold clone.                     18 +                                                                      19 +Structured output is validated against a pydantic model before           +it reaches the                                                        20 +pipeline, so a malformed response fails here rather than three           +stages later.                                                         21  """       22         23  from __future__ import annotations      ...       35         36  T = TypeVar("T", bound=BaseModel)       37         35 -# Override with SOW_MODEL. The pipeline is model-agnostic; this          - default is                                                           36 -# simply the current flagship chat model in the pinned SDK.           37 -DEFAULT_MODEL = "gpt-5.4"                                             38 +PROVIDER_KEY_ENV = {"anthropic": "ANTHROPIC_API_KEY", "openai":          + "OPENAI_API_KEY"}                                                    39 +DEFAULT_MODEL = {"anthropic": "claude-opus-5", "openai": "gpt-5          +.4"}                                                                  40         39 -# USD per million tokens (input, output), for the cost line in           -the run summary.                                                      40 -# Absent entries just omit the cost line rather than reporting           -a guess.                                                              41 -PRICE_PER_MTOK: dict[str, tuple[float, float]] = {}                   41 +# USD per million tokens (input, output). Absent entries omit t          +he cost line                                                          42 +# rather than reporting a guess.                                      43 +PRICE_PER_MTOK: dict[str, tuple[float, float]] = {"claude-opus-          +5": (5.0, 25.0)}                                                      44         45         46 +def detect_provider() -> str:                                         47 +    """Pick a provider from SOW_PROVIDER, or from whichever key          + is present."""                                                       48 +    forced = os.environ.get("SOW_PROVIDER", "").strip().lower()       49 +    if forced:                                                        50 +        if forced not in PROVIDER_KEY_ENV:                            51 +            raise ConfigError(                                        52 +                f"SOW_PROVIDER must be one of {sorted(PROVIDER_          +KEY_ENV)}, got '{forced}'"                                            53 +            )                                                         54 +        return forced                                                 55 +    for provider, env_var in PROVIDER_KEY_ENV.items():                56 +        if os.environ.get(env_var):                                   57 +            return provider                                           58 +    return "anthropic"                                                59 +                                                                      60 +                                                                      61  @dataclass       62  class TokenUsage:       46 -    """Cumulative token counts across a run."""                       63 +    """Cumulative token counts across a run, provider-independe          +nt."""                                                                64         65      calls: int = 0       66      input_tokens: int = 0       67      output_tokens: int = 0       51 -    reasoning_tokens: int = 0                                         68 +    cached_tokens: int = 0                                            69      per_stage: dict[str, dict[str, int]] = field(default_factor           y=dict)       70         71      def record(self, stage: str, usage: Any) -> None:       55 -        """Accumulate one call's usage, globally and per pipeli          -ne stage."""                                                          56 -        inp = int(getattr(usage, "prompt_tokens", 0) or 0)            57 -        out = int(getattr(usage, "completion_tokens", 0) or 0)        58 -        details = getattr(usage, "completion_tokens_details", N          -one)                                                                  59 -        reasoning = int(getattr(details, "reasoning_tokens", 0)          - or 0) if details else 0                                              72 +        """Accumulate one call's usage.                               73         74 +        Reads whichever field names the provider used: Anthropi          +c reports                                                             75 +        input_tokens/output_tokens, OpenAI prompt_tokens/comple          +tion_tokens.                                                          76 +        """                                                           77 +                                                                      78 +        def pick(*names: str) -> int:                                 79 +            for name in names:                                        80 +                value = getattr(usage, name, None)                    81 +                if value:                                             82 +                    return int(value)                                 83 +            return 0                                                  84 +                                                                      85 +        inp = pick("input_tokens", "prompt_tokens")                   86 +        out = pick("output_tokens", "completion_tokens")              87 +        cached = pick("cache_read_input_tokens")                      88 +                                                                      89          self.calls += 1       90          self.input_tokens += inp       91          self.output_tokens += out       64 -        self.reasoning_tokens += reasoning                            92 +        self.cached_tokens += cached                                  93         94          bucket = self.per_stage.setdefault(       95              stage, {"calls": 0, "input_tokens": 0, "output_toke           ns": 0}      ...        99          bucket["output_tokens"] += out       100         101      def estimated_cost_usd(self, model: str) -> float | None:        74 -        """Approximate cost, or None for a model with no publi           -shed price here."""                                                  102 +        """Approximate cost, or None for a model with no price           + recorded here."""                                                   103          price = PRICE_PER_MTOK.get(model)       104          if price is None:       105              return None       106          in_rate, out_rate = price       107          return (self.input_tokens / 1e6) * in_rate + (self.out            put_tokens / 1e6) * out_rate       108          81 -    def summary(self, model: str) -> str:                            109 +    def summary(self, model: str, provider: str = "") -> str:        110          """One-block report of token spend for the run."""       111          lines = [       112              "TOKEN USAGE",       113              "-" * 100,       114 +            f"provider           : {provider or 'n/a'}",             115              f"model              : {model}",       116              f"model calls        : {self.calls}",       117              f"input tokens       : {self.input_tokens:,}",       118              f"output tokens      : {self.output_tokens:,}",       119              f"total tokens       : {self.input_tokens + self.o            utput_tokens:,}",       120          ]        92 -        if self.reasoning_tokens:                                     93 -            lines.append(f"  of which reasoning: {self.reasoni           -ng_tokens:,}")                                                       121 +        if self.cached_tokens:                                       122 +            lines.append(f"  of which cached  : {self.cached_t           +okens:,}")                                                           123          for stage, bucket in sorted(self.per_stage.items()):       124              lines.append(       125                  f"  {stage:<17}: {bucket['calls']} call(s), "      ...       136      """Raised when the model cannot be reached or its response             is unusable."""       137         138         110 -def _key_source_hint(exc: Exception) -> str:                         111 -    """On an auth failure, say where the key came from.              112 -                                                                     113 -    An exported OPENAI_API_KEY takes precedence over one writt           -en in .env.                                                          114 -    Without this hint, replacing a bad key in .env while a sta           -le one is still                                                      115 -    exported looks like the new key being rejected.                  116 -    """                                                              117 -    text = str(exc)                                                  118 -    if "authentication" not in text.lower() and "401" not in t           -ext:                                                                 139 +def _key_source_hint(provider: str, exc: Exception) -> str:          140 +    """On an auth or quota failure, say which key was used and           + where it came from."""                                              141 +    text = str(exc).lower()                                          142 +    if not any(m in text for m in ("authentication", "401", "q           +uota", "429", "billing")):                                           143          return ""       144         145      from .config import ENV_PATH       146         123 -    key = os.environ.get("OPENAI_API_KEY", "")                       147 +    env_var = PROVIDER_KEY_ENV[provider]                             148 +    key = os.environ.get(env_var, "")                                149      if not key:       125 -        return "\n  hint: OPENAI_API_KEY is not set."                150 +        return f"\n  hint: {env_var} is not set."                    151         127 -    fingerprint = f"{key[:8]}...{key[-4:]}" if len(key) > 15 e           -lse "(short value)"                                                  128 -    hint = f"\n  hint: the key in use is {fingerprint} ({len(k           -ey)} chars)."                                                        129 -    if ENV_PATH.is_file():                                           130 -        hint += (                                                    131 -            f"\n        {ENV_PATH.name} exists, but an exporte           -d OPENAI_API_KEY takes "                                             132 -            f"precedence over it. Unset the shell variable to            -use the .env value."                                                 133 -        )                                                            134 -    else:                                                            135 -        hint += f"\n        No {ENV_PATH.name} file found; the           - key came from the environment."                                     152 +    fingerprint = f"{key[:11]}...{key[-4:]}" if len(key) > 18            +else "(short value)"                                                 153 +    hint = f"\n  hint: used {env_var} = {fingerprint} ({len(ke           +y)} chars)"                                                          154 +    hint += f", loaded from {ENV_PATH.name}." if ENV_PATH.is_f           +ile() else " from the environment."                                  155 +    if "quota" in text or "billing" in text:                         156 +        hint += "\n        The key is valid but the account ha           +s no credit."                                                        157      return hint       158         159         160  class LlmClient:       140 -    """Thin wrapper over the OpenAI SDK with usage accounting.           -"""                                                                  161 +    """Thin wrapper over a provider SDK, with usage accounting           +."""                                                                 162         163      def __init__(       164          self,       165          model: str | None = None,       166          backend: str | None = None,       167 +        provider: str | None = None,                                 168          fixture_dir: Path | None = None,       169      ) -> None:       148 -        self.model = model or os.environ.get("SOW_MODEL", DEFA           -ULT_MODEL)                                                           170 +        self.provider = provider or detect_provider()                171 +        self.model = model or os.environ.get("SOW_MODEL") or D           +EFAULT_MODEL[self.provider]                                          172          self.backend = (backend or os.environ.get("SOW_LLM", "            live")).lower()       173          self.usage = TokenUsage()       174          self.fixture_dir = fixture_dir      ...       186          max_tokens: int = 16000,       187          effort: str = "high",       188      ) -> T:       166 -        """One structured call, validated against ``output_for
          -mat ``.                                                               167 -                                                                     168 -        Args:                                                        169 -            stage: pipeline stage name, used to attribute toke           -n spend.                                                             170 -        """                                                          189 +        """One structured call, validated against ``output_for
          +mat``."""
    190          if self.backend == "mock":
      191              return self._parse_mock(stage, system, user, outpu
           t_format)
      173 -        return self._parse_live(stage, system, user, output_fo
          -rmat, max_tokens, effort)
    192
    175 -    def _parse_live(
    176 -        self,
    177 -        stage: str,
    178 -        system: str,
    179 -        user: str,
    180 -        output_format: type[T],
    181 -        max_tokens: int,
    182 -        effort: str,
    183 -    ) -> T:
    184 -        """Call the OpenAI API and validate the structured res
          -ponse."""
    193          client = self._live_client()
      194 +        try:
    195 +            if self.provider == "anthropic":
    196 +                return self._parse_anthropic(
    197 +                    client, stage, system, user, output_format
          +, max_tokens, effort
    198 +                )
    199 +            return self._parse_openai(
    200 +                client, stage, system, user, output_format, ma
          +x_tokens, effort
    201 +            )
    202 +        except LlmError:
    203 +            raise
    204 +        except Exception as exc:  # surfaced, never swallowed
      205 +            raise LlmError(
    206 +                f"{stage}: model call failed: {exc}{_key_sourc
          +e_hint(self.provider, exc)}"
    207 +            ) from exc
    208 +
    209 +    def_parse_anthropic(
    210 +        self, client, stage, system, user, output_format, max_
          +tokens, effort
    211 +    ) -> Any:
    212 +        """Anthropic Messages API with adaptive thinking and s
          +tructured output."""
    213 +        response = client.messages.parse(
    214 +            model=self.model,
    215 +            max_tokens=max_tokens,
    216 +            system=system,
    217 +            messages=[{"role": "user", "content": user}],
    218 +            output_format=output_format,
    219 +            thinking={"type": "adaptive"},
    220 +            output_config={"effort": effort},
    221 +        )
    222 +        self.usage.record(stage, response.usage)
    223 +
    224 +        if getattr(response, "stop_reason", None) == "refusal"
          +:
    225 +            details = getattr(response, "stop_details", None)
      226 +            reason = getattr(details, "explanation", "") if de
          +tails else ""
    227 +            raise LlmError(f"{stage}: model declined the reque
          +st. {reason}")
    228 +
    229 +        parsed = getattr(response, "parsed_output", None)
    230 +        if parsed is None:
    231 +            raise LlmError(
    232 +                f"{stage}: no parseable structured output "
    233 +                f"(stop_reason={getattr(response, 'stop_reason
          +', '?')}). "
    234 +                f"If this is 'max_tokens', raise max_tokens."
      235 +            )
    236 +        return parsed
    237 +
    238 +    def _parse_openai(
    239 +        self, client, stage, system, user, output_format, max_
          +tokens, effort
    240 +    ) -> Any:
    241 +        """OpenAI chat completions with structured output."""
      242          request: dict[str, Any] = {
      243              "model": self.model,
      244              "messages": [
     ...
      251          if effort:
      252              request["reasoning_effort"] = effort
      253
    198 -        try:
    199 -            response = client.chat.completions.parse(**request
          -)
    200 -        except Exception as exc:  # surfaced, never swallowed
      201 -            raise LlmError(f"{stage}: model call failed: {exc}
          -{_key_source_hint(exc)}") from exc
    202 -
    254 +        response = client.chat.completions.parse(**request)
    255          self.usage.record(stage, response.usage)
      256
    257          message = response.choices[0].message
     ...
      262          if parsed is None:
      263              finish = getattr(response.choices[0], "finish_reas
           on", "unknown")
      264              raise LlmError(
      213 -                f"{stage}: model returned no parseable structu
          -red output "
    214 -                f"(finish_reason={finish}). If this is 'length
          -', raise max_completion_tokens."
    265 +                f"{stage}: no parseable structured output (fin
          +ish_reason={finish}). "
    266 +                f"If this is 'length', raise max_completion_to
          +kens."
    267              )
      268          return parsed
      269
    270      def _live_client(self) -> Any:
      219 -        """Construct the SDK client, failing loudly if no cred
          -entials exist."""
    271 +        """Construct the provider SDK client, failing loudly w
          +ithout credentials."""
    272          if self._client is not None:
      273              return self._client
      222 -        try:
    223 -            from openai import OpenAI
    224 -        except ImportError as exc:
    274 +
    275 +        env_var = PROVIDER_KEY_ENV[self.provider]
    276 +        if not os.environ.get(env_var):
    277              raise ConfigError(
      226 -                "the 'openai' package is required for live run
          -s: pip install -e '.[llm]'"
    227 -            ) from exc
    228 -        if not os.environ.get("OPENAI_API_KEY"):
    229 -            raise ConfigError(
    230 -                "OPENAI_API_KEY is not set. Put it in .env (se
          -e .env.example), export it, "
    231 -                "or run with SOW_LLM=mock to replay the commit
          -ted golden run."
    278 +                f"{env_var} is not set. Put it in .env (see .e
          +nv.example), export it, "
    279 +                f"or run with SOW_LLM=mock to replay the commi
          +tted golden run."
    280              )
      233 -        self._client = OpenAI()
    281 +
    282 +        if self.provider == "anthropic":
    283 +            try:
    284 +                import anthropic
    285 +            except ImportError as exc:
    286 +                raise ConfigError(
    287 +                    "the 'anthropic' package is required: pip
          +install -e '.[llm]'"
    288 +                ) from exc
    289 +            self._client = anthropic.Anthropic()
    290 +        else:
    291 +            try:
    292 +                from openai import OpenAI
    293 +            except ImportError as exc:
    294 +                raise ConfigError(
    295 +                    "the 'openai' package is required: pip ins
          +tall -e '.[openai]'"
    296 +                ) from exc
    297 +            self._client = OpenAI()
    298          return self._client
      299
    300      # --------------------------------------------------------
           -------- mock --
     ...
      315          if self.fixture_dir is None:
      316              raise ConfigError("mock backend requires a fixture
            directory")
      317
    254 -        key = self.fixture_key(stage, system, user)
    255 -        path = self.fixture_dir / f"{key}.json"
    318 +        path = self.fixture_dir / f"{self.fixture_key(stage, s
          +ystem, user)}.json"
    319          if not path.is_file():
      320              raise LlmError(
      321                  f"{stage}: no recorded response at {path}. The
            prompt changed, so the "
      259 -                f"golden run is stale -- re-record it with 'so
          -w record'."
    322 +                f"golden run is stale -- re-record it with 'so
          +w draft --record'."
    323              )
      324
    325          payload = json.loads(path.read_text(encoding="utf-8"))
      326          self.usage.record(stage, _MockUsage(**payload.get("usa
           ge", {})))
      327          return output_format.model_validate(payload["parsed_ou
           tput"])
      328
    266 -    def record(self, stage: str, system: str, user: str, parse
          -d: BaseModel, usage: Any) -> None:
    329 +    def record(self, stage: str, system: str, user: str, parse
          +d: BaseModel) -> None:
    330          """Write one call to the fixture directory for later m
           ock replay."""
      331          if self.fixture_dir is None:
      332              raise ConfigError("recording requires a fixture di
           rectory")
     ...
      336              json.dumps(
      337                  {
      338                      "stage": stage,
      339 +                    "provider": self.provider,
    340                      "model": self.model,
      277 -                    "usage": {
    278 -                        "prompt_tokens": int(getattr(usage, "p
          -rompt_tokens", 0) or 0),
    279 -                        "completion_tokens": int(getattr(usage
          -, "completion_tokens", 0) or 0),
    280 -                    },
    341 +                    "usage": {"input_tokens": 0, "output_token
          +s": 0},
    342                      "parsed_output": parsed.model_dump(mode="j
           son"),
      343                  },
      344                  indent=2,
     ...
      351  class _MockUsage:
      352      """Usage shape for replayed calls."""
      353
    293 -    prompt_tokens: int = 0
    294 -    completion_tokens: int = 0
    354 +    input_tokens: int = 0
    355 +    output_tokens: int = 0

  Ran 1 shell command (ctrl+o to expand)

● Live call works. Running CP4 for real — all 12 sections, first genuine
  end-to-end run.

  Read 1 file, ran 2 shell commands (ctrl+o to expand)

● Output is buffered by the pipe. Checking progress via the trace file instead.

  Ran 1 shell command (ctrl+o to expand)

● Real run in progress — 8 of 12 sections done, and the validation loop is
  genuinely firing (§6 took 2 redrafts, §7 exhausted them and is marked
  unsupported). Waiting for completion.

  Read 1 file, ran 4 shell commands (ctrl+o to expand)

● Background command "First real end-to-end draft run, all 12 sections"
completed (exit code 0)
● Real run complete. Let me diagnose two things that look wrong before I commit.

  Ran 1 shell command (ctrl+o to expand)

● Diagnosis confirms two things. The facts are right — go_live_date = 2027-01-15
  (C1 resolved correctly), kickoff_date = 2026-09-15. But uat_window's "7
  different values" are seven phrasings of one window. The cross-section check
  compares raw claim text instead of resolved winners. Fixing that.

● Update(src\sow\assemble.py)
  ⎿  Added 13 lines, removed 1 line
       82      """
       83      values_by_key: dict[str, dict[str, set[int]]] = defaultdic
           t(lambda: defaultdict(set))
       84      for analysis in analyses:
       85 +        by_key: dict[str, list] = defaultdict(list)
    86          for claim in analysis.claims:
       86 -            values_by_key[claim.fact_key][claim.value_norm].ad
          -d(analysis.section_id)
    87 +            by_key[claim.fact_key].append(claim)
    88 +        for fact_key, members in by_key.items():
    89 +            resolution = resolve(fact_key, members, provs)
    90 +            # Compare what each section actually settled on, n
          +ot every phrasing
    91 +            # its claims used. Two sections that resolved a fa
          +ct identically but
    92 +            # quoted it differently -- "UAT: 2026-11-30 - 2026
          +-12-11" against the
    93 +            # same window with the regression period appended
          +-- are not in
    94 +            # conflict, and reporting them as such buries the
          +real divergences.
    95 +            # A key the section left contested is already disc
          +losed there; it
    96 +            # does not need to be counted again as a cross-sec
          +tion issue.
    97 +            if resolution.resolved and resolution.winner is no
          +t None:
    98 +                values_by_key[fact_key][resolution.winner.valu
          +e_norm].add(analysis.section_id)
    99
    100      issues: list[CrossSectionIssue] = []
      101      for fact_key, by_value in sorted(values_by_key.items()):

  Ran 1 shell command (ctrl+o to expand)

● Committing the real run plus the fix.

  Ran 1 shell command (ctrl+o to expand)

● Your Anthropic key works. CP4 has now run for real, end to end (0e65c6b).

  The key problem you hit

  The .env key is a different key from the one your shell exports — and my
  loader preferred the shell's, which was the invalid one. So a freshly pasted
  working key looked rejected. I reversed that: .env now overrides, and says so
  on stderr:

  note: ANTHROPIC_API_KEY from .env overrides the exported shell value

  The client now supports both providers, auto-detected from whichever key is
  present (SOW_PROVIDER forces it). That cost one method — nothing downstream
  sees a provider type.

  Real run: 12 sections, 36 calls, 244,475 tokens, ~USD 2.93

    s1   drafted     rev 1  21 cites     s7   unsupported rev 2  17 cites
    s2   conflict    rev 1  16 cites     s8   conflict    rev 0  18 cites
    s3   drafted     rev 1  18 cites     s9   conflict    rev 1  11 cites
    s4   conflict    rev 0  15 cites     s10  unsupported rev 2  34 cites
    s5   drafted     rev 0  11 cites     s11  conflict    rev 1  19 cites
    s6   conflict    rev 2   7 cites     s12  conflict    rev 1   9 cites

  The good news: the resolutions are right. go_live_date → 2027-01-15,
  kickoff_date → 2026-09-15, both derived from evidence. C1 resolved correctly
  without being told.

  The bad news, and it's the useful part: only 3 of 12 sections passed
  validation first try. All 26 gate failures were uncited_assertion — the model
  writes sentences without citation markers. Seven recovered on redraft; §7 and
  §10 burned through their retries and are marked unsupported, written anyway
  with their issues attached. That's the designed behaviour working, but it
  points at a drafting prompt that's too permissive about what needs a citation.
  This is exactly what a live run reveals and a fake one cannot.

  One bug found and fixed

  The cross-section check compared every claim's phrasing rather than what each
  section actually resolved to. uat_window was reported as seven different
  values when it's one window described seven ways. It now compares resolved
  winners and skips keys a section already discloses as contested.

  The committed artifact predates that fix — its 180 open questions and ~20
  cross-section issues overstate the real divergence. A re-run (~$3) will be
  materially lower.

  Where I'd go next

  The uncited_assertion rate is the highest-value fix — tightening the drafting
  prompt should move first-pass validation well above 3/12 and probably recover
  §7 and §10. That plus the cross-section fix are worth one re-run together,
  rather than spending twice.

  Say the word and I'll tighten the prompt and re-run; otherwise CP5 is the
  review CLI with the rejected_unsatisfiable terminal state.

✻ Cooked for 20m 4s

※ recap: Goal: build a system that drafts the Harding SOW from the corpus with citations, conflict detection, and a review step. CP4 just ran live end to end for the first time. Next: tighten the drafting prompt so sections stop failing the uncited-assertion gate, then re-run.

❯ CP5 — the review CLI. approve / reject-with-comment / redraft from the
  comment, plus the terminal states: rejected_unsatisfiable with a retry
  cap. Every decision appended to the trace with the reviewer's verbatim
  comment.

● CP5: the review loop. Adding the model-side signal first — a reviewer can ask
  for something the evidence doesn't support, and the system must refuse rather
  than fabricate.

  Ran 1 shell command (ctrl+o to expand)

● Update(src\sow\draft.py)
  ⎿  Added 36 lines
      180      return "\n".join(parts)
      181
    182
    183 +REDRAFT_SYSTEM_PROMPT = (
    184 +    SYSTEM_PROMPT
    185 +    + """
    186 +You are now redrafting after a human reviewer rejected the pre
          +vious version.
    187 +
    188 +The reviewer's comment is authoritative about what to change.
          +It is NOT
    189 +authoritative about what the sources say. If honouring it woul
          +d require
    190 +asserting something none of the claims support, do not write t
          +hat sentence.
    191 +Instead leave the body as close to the previous version as the
          + comment allows,
    192 +and set unsatisfiable_reason to a plain statement of what was
          +asked for and
    193 +which claim would be needed to support it.
    194 +
    195 +Refusing is the correct outcome in that case. A reviewer askin
          +g for a fact the
    196 +evidence does not contain is exactly the situation this system
          + exists to catch,
    197 +and satisfying them by inventing the sentence would defeat it.
      198 +"""
    199 +)
    200 +
    201 +
    202 +def build_redraft_prompt(base_prompt: str, previous_body: str,
          + comment: str) -> str:
    203 +    """Extend the original drafting prompt with the reviewer's
          + verbatim comment."""
    204 +    return "\n\n".join(
    205 +        [
    206 +            base_prompt,
    207 +            "PREVIOUS DRAFT (rejected by the reviewer):",
    208 +            previous_body or "(the previous draft was empty)",
      209 +            "REVIEWER COMMENT, VERBATIM:",
    210 +            comment,
    211 +            "Redraft the section addressing that comment. Ever
          +y rule above still applies: "
    212 +            "assert only what the claims support, cite every f
          +actual sentence, and do not "
    213 +            "state a value for anything listed as contested or
          + missing. If the comment "
    214 +            "cannot be honoured within those rules, set unsati
          +sfiable_reason and explain.",
    215 +        ]
    216 +    )
    217 +
    218 +
    219  def markers_used(body: str) -> list[str]:
      220      """Citation markers referenced in a drafted body, in order
            of appearance."""
      221      seen: list[str] = []

● Now the review module itself.

● Write(src\sow\review.py)
  ⎿  Wrote 391 lines to src\sow\review.py
       1 """Stage 13 -- the human review loop.
       3 A reviewer approves or rejects each section with a comment, and
       4 redrafts the section from that comment. Two things matter beyond
          the mechanics.
       6 **Nothing disappears.** Every terminal state still emits the sec
       7 approved section is emitted; a rejected one that could not be sa
       8 emitted at its last valid revision, carrying the reviewer's verb
         atim comment and
         emitted as
         uld be a worse
     … +442 lines (ctrl+o to expand)

● Now persisting the drafting prompt so review can redraft without
  re-extracting, and wiring the CLI command.

  Ran 1 shell command (ctrl+o to expand)

● Update(src\sow\trace.py)
  ⎿  Added 11 lines, removed 2 lines
      16  class Trace:
      17      """Append-only JSONL writer."""
      18
    19 -    def__init__(self, path: Path) -> None:
    19 +    def__init__(self, path: Path, append: bool = False) -> Non
         +e:
    20 +        """Open the trace.
    21 +
    22 +        Args:
    23 +            append: continue an existing trace rather than trun
         +cating it. The
    24 +                review pass appends, so a section's drafting hi
         +story and the
    25 +                decisions taken on it stay in one file.
    26 +        """
    27          self.path = path
      28          self.path.parent.mkdir(parents=True, exist_ok=True)
      22 -        self._fh = self.path.open("w", encoding="utf-8", newlin
         -e="\n")
    29          self._seq = 0
      30 +        if append and self.path.is_file():
    31 +            self._seq = sum(1 for _ in self.path.open(encoding=
         +"utf-8"))
    32 +        self._fh = self.path.open("a" if append else "w", encod
         +ing="utf-8", newline="\n")
    33
    34      def event(self, kind: str, section_id: int | None = None, *
          *payload: Any) -> None:
      35          """Write one trace event."""

  Ran 1 shell command (ctrl+o to expand)

● Now testing it. The existing run.json predates draft_prompt, so I need a fresh
  draft of a couple of sections first.

  Ran 1 shell command (ctrl+o to expand)

● Anthropic credit is now exhausted too — the CP4 full run (~$2.93) consumed it.
  The diagnostic worked, at least:

  hint: used ANTHROPIC_API_KEY = sk-ant-api0...4gAA (108 chars), loaded from
  .env.
        The key is valid but the account has no credit.

  Testing the review loop with a fake client instead, exercising all three
  terminal states.

  Made 1 scratchpad edit +127, ran 1 shell command (ctrl+o to expand)

● It hung — and that's a real bug, not a test artifact. A scripted reject that
  redrafts successfully loops back and re-reads the same decision forever.
  Killing it and fixing.

  Ran 1 shell command (ctrl+o to expand)

● Update(src\sow\review.py)
  ⎿  Added 1 line
      62      admitted_doc_ids: set[str]
      63      tripwire_terms: list[str]
      64      max_attempts: int = MAX_REDRAFT_ATTEMPTS
      65 +    max_cycles: int = MAX_REJECT_CYCLES
    66
    67
    68  def review_sections(

● Update(src\sow\review.py)
  ⎿  Added 20 lines, removed 1 line
       92      ctx: ReviewContext,
       93      scripted: dict[int, tuple[str, str | None]] | None,
       94  ) -> None:
       95 -    """Review one section until it reaches a terminal state or
          - is skipped."""
    95 +    """Review one section until it reaches a terminal state or
          + is skipped.
    96 +
    97 +    A successful redraft loops back so the reviewer can judge
          +the new version.
    98 +    Two bounds keep that loop finite: a scripted decision is c
          +onsumed once, so a
    99 +    non-interactive run cannot re-reject the same section fore
          +ver, and
    100 +``max_cycles`` caps how many rejections one section can ab
          +sorb before it is
    101 +    closed as unsatisfiable. Without the cap a reviewer could
          +spend unbounded
    102 +    tokens on a section the evidence will never satisfy.
    103 +    """
    104 +    cycles = 0
    105 +    consumed = False
    106 +
    107      while True:
      108          _present(draft)
      109 +
    110 +        if scripted is not None and consumed:
    111 +            # The script has already spoken for this section;
          +a redraft that
    112 +            # succeeded leaves it pending for a human to look
          +at.
    113 +            print(f"  section {draft.section_id} left pending
          +after redraft\n")
    114 +            return
    115 +
    116          action, comment = _decide(draft, scripted)
      117 +        consumed = True
    118
    119          if action == "approve":
      120              draft.review = ReviewRecord(decision="approved", r
           evision=draft.revision)
● Update(src\sow\review.py)
  ⎿  Added 11 lines
      144
    145          # Rejection. The comment is recorded verbatim before a
           nything acts on it.
      146          assert comment is not None
      147 +        cycles += 1
    148 +        if cycles > ctx.max_cycles:
    149 +            _terminal(
    150 +                draft,
    151 +                comment,
    152 +                f"rejected {cycles} times; the per-section lim
          +it of {ctx.max_cycles} "
    153 +                f"rejection cycles was reached, so the section
          + is closed here",
    154 +                ctx,
    155 +            )
    156 +            return
    157 +
    158          draft.review = ReviewRecord(
      159              decision="rejected", comment=comment, revision=dra
           ft.revision
      160          )

  Ran 1 shell command (ctrl+o to expand)

● All four terminal states work. The traceback is a bug in my test script (blank
  trailing line in the trace), not the code.

  Ran 2 shell commands (ctrl+o to expand)

● The hung background process is still running — 810 MB of trace. Killing it.

● Stop Task
  ⎿  cd "C:\Users\Gala Solutions\blaugarnet-sow" && PYTHONPATH=src python
     "C:/Users/GALASO~1/AppData/Local/Temp/claude/C--Users-Gala-Solutions-b
     laugarnet-sow/85a7191… · stopped

  Ran 1 shell command (ctrl+o to expand)

● All four paths verified. Committing CP5.

  Ran 1 shell command (ctrl+o to expand)

● CP5 committed (50cbe64).

  sow review                          # interactive: a / r / s / v / q / ?
  sow review --sections 6,8
  sow review --script decisions.txt   # non-interactive

  All four outcomes verified:

    5.  Team & Roles              approved                 rev 0
    6.  Governance                pending                  rev 1   (redrafted
  from comment)
    8.  Commercials               rejected_unsatisfiable   rev 0
        comment: 'State the total contract value in dollars.'
        reason : no claim states one and hours-per-role is not in evidence
   12.  Acceptance Criteria       rejected_unsatisfiable   rev 0
        reason : redrafted 2 time(s), failed validation each time

  §8 is the case that matters: a reviewer asks for a total contract value, the
  corpus genuinely cannot support one (G8a — hours per role are never given),
  and the system refuses rather than inventing a figure. rejected_unsatisfiable
  is a real terminal state, not a failure. The section is still emitted, at its
  last valid revision, with the comment and reason attached.

  Every decision lands in the trace with the reviewer's comment verbatim —
  review_decision, redraft_refused, redraft_accepted.

  A real bug this found

  A scripted rejection whose redraft succeeded looped back, re-read the same
  decision, and rejected forever. A background run reached 810 MB of trace
  before I killed it. Two fixes: a scripted decision is consumed once, and a new
  per-section rejection-cycle cap (--max-cycles, default 3) bounds the
  interactive path too — otherwise a reviewer could spend unboundedly on a
  section the evidence will never satisfy.

  Two things you should know

  Your Anthropic credit is exhausted. The CP4 run consumed it (~$2.93). The
  diagnostic is clear about it:
  hint: used ANTHROPIC_API_KEY = sk-ant-api0...4gAA (108 chars), loaded from
  .env.
        The key is valid but the account has no credit.
  So CP5 was verified against a fake client, same discipline as before — only
  LlmClient.parse substituted; the loop, gates, trace and re-render all ran
  unmodified.

  run.json now persists each section's drafting prompt, so a redraft costs one
  call instead of re-running extraction. The run.json from the CP4 run predates
  this, so reviewing it would hit the "no drafting prompt recorded" terminal
  path — re-run sow draft once you have credit.

  Remaining

  CP6 is tests, the golden run, and the README. The golden run needs one real
  sow draft execution to record fixtures — after that pytest runs cold with
  SOW_LLM=mock and no key. That's the only remaining item that needs credit, and
  it's worth combining with the uncited_assertion prompt fix I flagged so you
  spend once rather than twice.

✻ Baked for 8m 33s

❯ CP6 — tests, the committed golden-run fixture, and the README.

  README must cover: assumptions, design choices (including why
  embeddings and whole-corpus-in-context were rejected), how I'd judge a
  good draft, the automated checks, and approximate token usage per run.
  Paste the partition report output into a Verification section.

● CP6. First the fixture recorder and an artifact-level audit — the audit is the
  automated quality check.

  Ran 1 shell command (ctrl+o to expand)

● Now the audit module — the automated quality check, re-verifying a produced
  draft against the corpus from scratch.

● Write(src\sow\audit.py)
  ⎿  Wrote 166 lines to src\sow\audit.py
       1 """Quality audit of a produced draft, re-derived from the corpus
       2
       3 This is the automated quality check. It deliberately trusts noth
       4 recorded about itself: it re-reads ``data/``, re-chunks it, and
       5 citation in the finished markdown against the source lines. A ru
         n that lied to
       7
       8 Six checks, in descending order of how badly a failure would mat
       9
         exists.
     … +195 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● Audit passes on the real CP4 draft: 196 citations, all verbatim, no
  contamination. Now the test suite.

  Ran 3 shell commands (ctrl+o to expand)

● Now the two that matter most — the authority policy and conflict-detection
  recall against the C1–C12 fixture.

  Ran 3 shell commands (ctrl+o to expand)

● Now the headline quality check as a test, plus the golden-run replay test.

  Ran 1 shell command (ctrl+o to expand)

● 101 passed, 2 skipped (golden run, correctly gated). Verifying the cold-clone
  condition — no key at all.

  Ran 1 shell command (ctrl+o to expand)

● Now the README, with the real partition output pasted in.

  Ran 1 shell command (ctrl+o to expand)

● Write(README.md)
  ⎿  Wrote 441 lines to README.md
       1 # Blaugarnet SOW Drafter
       3 Drafts a Statement of Work for the **Harding Outfitters** engage
         ment from the
         uman approval
       5 step.
       7 Every substantive statement in the draft carries a citation that
          resolves to a
         isagree, or
       9 where the template requires something no source supplies, the dr
      10 rather than guessing.
     … +658 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)
● README's NOTES block is stale — I pasted an older capture. Correcting it to
  match live output exactly.

  Ran 1 shell command (ctrl+o to expand)

● Committing CP6.

  Ran 1 shell command (ctrl+o to expand)

● CP6 committed (568c54a). All six checkpoints done.

  Tests

  101 passed, 2 skipped, 0.47s — verified with both API keys unset. No test
  imports a provider SDK, so a cold clone passes before any key exists.

  test_admission   engagement boundary, your three hard cases, AMBIGUOUS paths
  test_provenance  header parsing, cross-document supersession, the traps
  test_template    required elements incl. §12's "by whom"
  test_retrieval   no out-of-scope chunk in any pool; recall each pool must keep
  test_authority   the policy, including where it must decline to resolve
  test_analysis    conflict + insufficiency detection; quote verification
  test_validate    the five drafting gates
  test_review      all four review terminal states
  test_audit       the quality check, and that each check fails when it should
  test_golden_run  offline replay (skipped — see below)

  The quality check

  sow audit re-reads data/, re-chunks it, and re-verifies the finished markdown
  from scratch — trusting nothing the run recorded about itself. It passes on
  the real CP4 draft: 196 citations across 12 sections.

  The part I'd point you at: test_audit.py proves each check fails when it
  should — a citation to Northgate's SOW, a quote altered by one word, a real
  quote attached to the wrong line range, a foreign entity in prose. A check
  that has never failed isn't evidence of anything.

  I audit groundedness as provenance, not entailment. Whether a sentence is
  logically entailed by its quote isn't decidable by string matching, and a
  model-scored judgement would be as fallible as the thing it audits.

  README

  Covers assumptions, design choices, how I judge a draft, the automated checks,
  and measured token usage (36 calls, 244,475 tokens, ~USD 2.93). The partition
  report is pasted into a Verification section — I diffed it against live
  output to confirm it matches exactly, after catching that my first paste was a
  stale capture.

  Both rejected retrieval alternatives are written up. Whole-corpus-in-context
  is the interesting one: it maximises recall, but converts the engagement
  boundary from a code invariant into a model instruction — the wrong client's
  SOW would sit in the context window with only a prompt between it and §8.

  Two things I did not paper over

  The golden run is not recorded. sow draft --record writes the fixtures and
  test_golden_run.py replays them, but both accounts ran out of credit, so those
  two tests skip with instructions rather than failing. One funded sow draft
  --record closes it.

  Known weaknesses are in the README, not omitted — 3 of 12 sections passed
  validation first try (all uncited_assertion), fact-key stability is an
  unenforced hinge the whole detector turns on, and value normalisation is
  approximate.

  What I'd spend the next hour on

  Tightening the drafting prompt so first-pass validation clears — it's the
  highest-value single fix, would likely recover §7 and §10, and cuts roughly
  half the drafting tokens. Worth combining with --record so one funded run both
  fixes the weakness and closes the fixture gap, with before/after gate-failure
  counts as the measured improvement the brief asks for.

✻ Cooked for 9m 35s

※ recap: Goal: build a system that drafts the Harding SOW from data/ with citations, conflict detection and a review loop. All six checkpoints are committed and 101 tests pass. Next: one funded `sow draft --record` run to record the golden-run fixtures and tighten the drafting prompt.

❯ commit code

  Ran 1 shell command (ctrl+o to expand)

● Nothing to commit — the working tree is clean. CP6 (568c54a) captured
  everything. Let me confirm nothing meaningful is being silently ignored.

  Ran 1 shell command (ctrl+o to expand)

● Already committed — the working tree is clean. CP6 (568c54a) captured the last
  of it.

  Eight commits, one per checkpoint plus two course corrections:

  568c54a  test suite, artifact audit, fixture recorder, README        (CP6)
  50cbe64  review CLI, bounded retries, refusable comments             (CP5)
  0e65c6b  back to Anthropic, dual-provider, cross-section noise fix
  00a9eda  drafting, validation gates, assembly, cross-section check   (CP4)
  7ec42ed  OpenAI client, and actually load .env
  6b89bb3  claim extraction, quote verification, conflict analysis     (CP3)
  7120309  chunking, template parse, BM25, evidence assembly           (CP2)
  0720f9f  engagement boundary: ingest, provenance, admission          (CP1)

  Nothing sensitive is tracked. .env is correctly ignored, along with output/,
  caches and the egg-info. The only thing in output/ that's tracked is .gitkeep.

  One gap worth naming before you submit. ai_transcripts/ has 1 tracked file —
  the .gitkeep I added at CP1. The brief is explicit that a submission without
  shareable links or transcripts of the AI conversation will not be evaluated,
  so that directory still needs the export of this session, plus the 10-line
  note on what the AI got wrong or generic and what you changed or rejected.

  I can draft that note from what actually happened in this session — the
  misread playbook status, the missing stemming that left §8 without rates, the
  tripwire firing on the template's own headings, the infinite review loop, and
  the .env precedence bug — but the transcript export itself is yours to
  produce.

✻ Cogitated for 40s


※ recap: Goal was a grounded SOW drafter for Harding Outfitters; all six checkpoints are built, tested and committed, and I've drafted your 10-line submission note. Next: confirm the note's wording, then export this session's transcript into ai_transcripts.

❯ /export
  ⎿  Conversation copied to clipboard
