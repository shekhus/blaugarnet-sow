# Call transcript — Harding Outfitters discovery
**Date:** 2026-07-10 · **Recorded via:** Blaugarnet Services meeting bot
**Attendees:** Sandra Liu (Harding, VP Customer Experience), Jake Morrow (Harding, IT Director), Raj Patel (Harding, CTO), Meera Shah (Blaugarnet Services, Account Director), Daniel Okafor (Blaugarnet Services, Solutions Architect)

**Meera Shah:** Thanks everyone for making time. Goal today is to understand the returns problem end to end, and, um, start shaping what a first phase could look like.

**Sandra Liu:** So the short version — our returns process is email and a shared inbox. Customers email photos of a jacket with a failed zipper to support, someone copies it into a spreadsheet, someone else keys the refund into OrderHub. Average refund cycle is twelve days. Thirty percent of our support contacts are literally "where is my refund." In Q4, returns hit twenty-two percent of orders and the whole thing melts. What we want is a portal — customer looks up their order, picks the items, tells us why, uploads photos if it's damaged, and watches the status. And our agents work one queue instead of three inboxes and a spreadsheet.

**Daniel Okafor:** When you say the refund happens — you want the portal issuing refunds directly, or an agent approves first?

**Sandra Liu:** Agent approves. We're not ready for auto-approved refunds. Maybe someday, for low-value items.

**Jake Morrow:** From my side — whatever gets built has to talk to OrderHub. That's our order management system, it owns orders, payments, refunds. OrderHub has a vendor API program, we're already enrolled.

**Daniel Okafor:** Good. We've integrated OrderHub twice before, their sandbox provisioning is the slow part — took six weeks once. Worth starting that paperwork immediately.

**Raj Patel:** Two hard requirements from me. One, single sign-on for staff — we're an Okta shop, everything goes through Okta or it doesn't ship. Two, this is customer data — names, addresses, order history — so privacy compliance applies to every byte, and I want zero card data in this thing. Refunds execute inside OrderHub, the portal never touches a card number. Your infosec people will get our questionnaire.

**Meera Shah:** Understood on both. Sandra, you mentioned exchanges earlier — instant exchanges, where the replacement ships before the return even arrives — is that phase one?

**Sandra Liu:** I'd love it to be. Returns without instant exchange is half the story for us — that's the feature that turns a refund into a save.

**Jake Morrow:** Let's keep it in for now and see what the estimate says.

**Meera Shah:** Okay, so working scope for phase one: customer returns portal, agent queue, OrderHub integration for order lookup and refund execution, Okta SSO, and instant exchanges. We'll size that.

**Raj Patel:** Timeline expectations — Sandra has a board commitment. Sandra?

**Sandra Liu:** I told the board live before the January returns wave. So go-live December 11th, 2026, at the latest. That's the date I'm carrying.

**Meera Shah:** Noted — December 11 go-live is the working target. Aggressive but let's see the plan. On commercials, we'll bring a rate and effort estimate to the scoping session. Payment terms and contracting run under the MSA your procurement team is finalizing with us.

**Jake Morrow:** One more thing — historical data. Six years of orders live in OrderHub already, that's fine. But the last four years of returns are split between a retired RMA tool export and the spreadsheet situation I mentioned, which I'm not proud of. What's your assumption on who moves that?

**Daniel Okafor:** Let's take that offline with your data team — it depends heavily on quality. We'll come back with a split of responsibilities.

**Meera Shah:** Great session. Next step is a scoping call in early August, we'll bring the phase plan.
