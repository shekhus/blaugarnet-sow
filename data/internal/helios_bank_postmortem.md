# Project post-mortem — Helios Bank statement portal (closed 2025-11)
**Facilitator:** Priya Nair · **Distribution:** delivery org

## What we shipped
Customer statement portal + document vault, 14-month engagement, went live 2025-10-20, 4 weeks late.

## What went well
- Milestone-based commercial structure kept scope honest.
- Weekly client demo cadence caught UX misses early.

## What hurt
1. **Vendor sandbox provisioning (core banking API) took 9 weeks** against a plan of 3. We started the request only at kickoff. LESSON: file vendor access requests during contracting, not at kickoff.
2. Acceptance criteria were left as "to be defined during UAT." Client used the ambiguity to extend UAT by 3 weeks at our cost. LESSON: put the acceptance mechanism and window in the SOW even if detailed criteria come later.
3. A verbal agreement on data cleanup ownership was never written down; we absorbed ~180 unbudgeted hours. LESSON: verbal responsibility splits go into the SOW under client responsibilities, every time.

## Actions
- SOW template updated to require Acceptance Criteria section (done, 2025-12).
- Pre-kickoff checklist now includes vendor access requests (done).
