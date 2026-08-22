# Harding Outfitters — Phase One Requirements (WORKING DRAFT)
**Author:** Daniel Okafor · **Last touched:** 2026-08-16 · **Status:** incomplete, do not circulate

## Users & roles
- Customer (order lookup via order number + email OTP; no persistent account required)
- Returns Agent (Harding staff, ~14 users)
- Refund Approver (Harding staff, ~6 users; approvals above USD 250)
- Admin (Harding IT, 2–3 users)
Staff roles authenticate via Okta (OIDC). Customer verification is portal-local — order number + email OTP.

## Modules
### Returns portal
- Order lookup, item-level selection, quantity, reason codes (config list, Harding owns taxonomy)
- Photo upload for damaged/defective claims (PDF/JPEG, 20MB cap), virus scanning
- Status page: submitted → under review → approved → refund issued (or: denied, with reason)
### Agent queue
- Unified queue, filter by status/date/value/reason; assignment; duplicate return detection (order + SKU match) — nice-to-have?
- Refund or exchange proposal → refund executed in OrderHub on approval
### OrderHub integration
- Order lookup (vendor API v3, OAuth2 client credentials)
- Refund execution and write-back; nightly reconciliation job
- Sandbox first, prod credentials via Harding IT
### SSO
- Okta OIDC for the three staff roles; group-to-role mapping owned by Harding IT

## Non-functional
- Availability target: TBD (Sandra said "it can't be down during business hours", quantify)
- Volume assumption: ~1,800 return requests/week baseline; plan for ~4x spike in January
- Audit: every state change on a return logged with actor + timestamp

## Security & compliance
- Customer PII (names, addresses, order history). No card data in the portal — refunds execute inside OrderHub; keeps the portal out of PCI scope (confirm with legal).
- DPA executed under MSA (confirm with legal).
- Harding infosec questionnaire: NOT YET RECEIVED as of 2026-08-16
- Pen test before go-live — whose vendor? TBD
- Data at rest encryption, TLS 1.2+ — standard

## Out / later
- Instant exchanges + credit-risk rules (descoped from phase one per J. Morrow email 2026-08-12; addendum being revised)
- Analytics dashboard (phase two)
- Auto-approved refunds for low-value items (explicitly not wanted yet)
- Carrier return-label generation and pickup scheduling — parked, Sandra keeps mentioning it though

## Open
- Migration: legacy RMA export + returns spreadsheet profiling not started. Effort unknown.
- Acceptance criteria per deliverable — still undefined, Karen wants mechanism in SOW
- Reporting requirements for the agent queue — nobody has specified any
