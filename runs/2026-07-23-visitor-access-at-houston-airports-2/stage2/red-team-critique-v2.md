# Red Team Critique — Strategist Draft v2
**Run:** visitor-access-at-houston-airports-2
**Target:** `outputs/stage2/strategist-draft-v2.md` ("The Velvet Rope at the Oversubscribed Door")
**Verified against:** all eight Stage 1 briefs (infrastructure-economist, operations-analyst, contrarian, airline-commercial-strategist, regulatory-political-analyst, airport-ceo, airport-coo, director-of-public-safety) and the v1 critique.

**Overall verdict before the itemized list.** The v2 revision is real work. The convergence tally is now honest, the COO's fresh-capacity argument is presented and beaten on the merits, the Hobby-construction contradiction became a launch condition, the composite plane-watcher now earns his place, and the concession-revenue question is handled with one consistent treatment. Of the five items v1 flagged as ship-blockers, four are genuinely fixed and one (item 2) is fixed in the only honest form available.

But the revision has a signature failure mode: **it fixed the v1 items by talking about fixing them.** The draft now opens with two pages of revision notes addressed to me, not the Director; it references "the first draft" twice inside the argument; and it converted the manufactured-consensus problem into a paragraph of visible Council machinery. Meanwhile the single largest analytical gap survived both drafts untouched: **the report recommends Hobby and never models Southwest's response or runs a single Hobby-denominated number.** Every quantitative claim in the draft is sized against Bush, and the carrier-response section litigates United at the airport the report rejects while giving one non-sequitur sentence to the 93-percent carrier at the airport it selects. A skeptical Director's staff will find that in one read.

Ship-blockers this round: items 1, 2, 3, 5, and 6.

---

## A. New weaknesses the revision introduced

**1. Process exhaust is now the first thing the Director reads.**
- **Location:** "Revision notes (v1 → v2)," lines 7–18 — two pages of itemized responses to the Red Team, at the top of the deliverable.
- **Issue:** v1 items 15 and 16 attacked process leakage — the report citing its own run instructions and staging internal agents as characters. v2 deleted those sentences and then installed a far larger version of the same disease as front matter: a numbered ledger of critique items, push-backs, and drafting decisions ("Item 13 (the ten-minute line). Cut the fake number..."). The Director has never seen the v1 critique. To her, this section is twenty-four references to documents that don't exist in her world. If this block is meant as a memo to the Red Team, it belongs in a separate file or a transmittal note — not inside the report.
- **Recommendation:** Strip the entire revision-notes section from the deliverable. If the push-backs need a record, put them in `outputs/stage2/strategist-response-v2.md`. The report must open cold, on the shutdown line.

**2. "The first draft" appears twice inside the argument, and the confidence paragraph is Council machinery on stage.**
- **Location:** "Why the counter-case is insufficient" — "the residual-risk trio the counter-case raised and the first draft left hanging" and "A word about how confident to be in that site choice, because the first draft overclaimed it. Three lenses independently named Hobby: the strongest case against, the operational-throughput analysis, and the regulatory read... the executive-finance view and the public-safety view... A manufactured consensus would have been a liability the first skeptical staffer could puncture."
- **Issue:** The Director has read no first draft and knows no "lenses." This paragraph is the v1 item-16 disease — internal agents as on-stage characters — wearing the costume v1 predicted it would wear ("the attribution wrapper is machinery showing"). Worse, "a manufactured consensus would have been a liability" confesses, in the deliverable, that an earlier version manufactured a consensus. The *substance* of the paragraph is excellent: the site choice rests on three independent analyses, two shape-only prescriptions, and one overruled dissent. That can be said without drafting history.
- **Recommendation:** Rewrite the paragraph in the world's terms, not the Council's: "Three independent analyses — the strongest case against the program, the checkpoint-throughput arithmetic, and the regulatory read — each landed on Hobby..." Delete both "first draft" references. Cut the manufactured-consensus sentence entirely.

**3. The report recommends Hobby and never once runs the numbers at Hobby — a gap two briefs explicitly warned about.**
- **Location:** Systemic. "The scarce thing is a lane at 6:10 a.m." (all arithmetic is Bush: 48.45M passengers, 64,000 daily enplanements, seventeen operating hours, 300/day cap); exec summary #2 (Bush denominators); the recommendation (50/day, midday-to-evening, one Hobby checkpoint).
- **Issue:** The infrastructure-economist's caveat 6 is explicit: "I did not model HOU separately in detail... the per-airport revenue and capacity math should be re-run for HOU specifically." The ops analyst gives the Hobby inputs (14.6M passengers, single 24-hour terminal, two concourses) and the draft never touches them. So the essay's showcase arithmetic — 18 visitors an hour, 6–12 percent of a lane, 0.075 percent of throughput — describes a 300/day program at the airport the report *rejects*, while the 50/day, ~8-operating-hour program at the airport it *recommends* goes unsized. The irony: the Hobby math would *strengthen* the case. Fifty passes over an eight-hour midday-evening window is roughly six visitors an hour — 2–4 percent of a single real-world lane — trivial even against Hobby's smaller checkpoint plant. The draft leaves its best number on the table and lets a hostile reader notice that every figure describes the wrong airport.
- **Recommendation:** Add three sentences of Hobby-denominated arithmetic in either the "scarce thing" section or the rebuttal: the recommended configuration's hourly load, against Hobby's throughput, with the honest caveat (carried from [^8]) that Hobby's per-checkpoint hourly data must set the final cap. Note the one true gap — no brief documents Hobby's checkpoint count — as exactly that.

**4. "A fraction of a million dollars a year" contradicts the sentence it lives in.**
- **Location:** "Start with the number that ends the money conversation," second paragraph: "worth about ten dollars in concessions and parking... and at even 300 visitors a day that is a fraction of a million dollars a year of gross upside before any cost."
- **Issue:** Run the stated arithmetic: $10.16 × 300 × 365 ≈ $1.1 million — not a fraction of a million. The economist's own range is $0.5M–$1.1M gross per airport (at a *discounted* $5–$10 per visitor). The draft takes the top-of-range per-head figure, the top-of-range volume, and then reports a total below the bottom of the range. Any staffer with a calculator catches this, and it sits in the section whose entire job is to be arithmetically bulletproof.
- **Recommendation:** Either say "$0.5 to $1.1 million a year of gross upside — before any cost, and most of it fictional because greeters get dropped off and buy nothing" (the brief's actual range, and the "fictional" beat survives), or keep "fraction of a million" and honestly derive it from the discounted per-visitor figure at realized (not capped) volumes. Not both halves of two different calculations.

**5. "A refundable ticket bought under any name" is factually wrong, and the public-safety brief says so.**
- **Location:** Security rebuttal in "Why the counter-case is insufficient": "the genuinely unvetted way to run reconnaissance — a refundable ticket bought under any name — remains strictly easier than applying for a pass days ahead."
- **Issue:** Ticketed passengers are not unvetted and cannot fly "under any name" — Secure Flight watch-list vetting of ticketed passengers is the entire subject of 49 CFR Part 1560, which this draft cites eight paragraphs earlier as the program's own vetting mechanism. The public-safety brief drew the distinction precisely: a ticketed passenger "gets the same screening with *less advance vetting*" — a lead-time difference, not a vetting-versus-no-vetting difference. The v1 recommendation (item 20) supplied the correct form of this argument; the revision overshot it into a claim that is false on the draft's own regulatory citations. This is the sentence a TSA reviewer or the public-safety chair strikes first.
- **Recommendation:** "the lower-friction way to run reconnaissance — a same-day refundable ticket, vetted only at booking — remains strictly easier than applying days ahead and submitting to adjudication." The argument survives intact; the falsehood does not.

**6. The blackout calendar is tied to a World Cup the program cannot exist for.**
- **Location:** Recommendation, "Hours" bullet: "blackout every peak date on a calendar published before launch, tied to demand forecasts and the 2026 World Cup"; also the rebuttal: "Houston, a 2026 World Cup host city closing out its own checkpoints in the same year, must publish the blackout logic before launch."
- **Issue:** Timeline incoherence the draft creates itself. The report is dated to a July 2026 decision; its own critical path says the ASP amendment takes "six to twelve months on TSA's calendar" — so the earliest launch is roughly mid-2027. The 2026 World Cup will have ended a year before the first pass is issued. A blackout calendar "tied to the 2026 World Cup" is a plan to suspend a program that does not yet exist for an event that will be over. (Separately: "closing out its own checkpoints" is garbled — presumably "closing out its checkpoint construction.") Seattle's World Cup suspensions remain a valid *precedent* for pre-published blackout logic; they are not a valid *input* to Houston's calendar.
- **Recommendation:** Keep SEA as precedent. Re-anchor Houston's blackout calendar to events the pilot will actually live through: holiday peaks, spring break, hurricane-season IROPS, and any 2027–2028 special events. Fix the garbled phrase.

**7. The revision notes overclaim what item 24 fixed: stop-criteria *values* are still not named.**
- **Location:** Revision notes ("named pilot duration and stop-criteria values (24)") vs. the recommendation ("a checkpoint-wait threshold that auto-pauses issuance, an incident threshold, and a utilization floor").
- **Issue:** Duration (12 months) and cap (50/day) are named. The stop criteria are still categories, not values — no wait-minute threshold, no incident definition, no utilization percentage. That is exactly the v1 finding, restated. The draft may legitimately hold that final values must come from Hobby's own data — but then it must say that, and it must stop claiming the item was incorporated in full.
- **Recommendation:** Name provisional values with the honest bracket — e.g., "pause issuance when the pilot checkpoint's standard-lane wait exceeds 20 minutes [provisional; set final threshold from Hobby hourly data]; non-renewal below 40 percent average cap utilization" — or state explicitly that values are a launch-condition deliverable, and correct the revision-notes claim.

---

## B. Unsupported and unstable claims

**8. "About two dozen airports" vs. "about 20... to 28" vs. "~20" — three counts of the same population in one document.**
- **Location:** Counter-case ("About two dozen airports run these programs and none has produced a reported mass-casualty event"), federal-frame section ("from about 20 in mid-2025 to 28 by January 2026"), footnote 37 ("~20 operating programs").
- **Issue:** The contrarian's no-reported-breach finding was made against ~20 programs; the reg analyst's count is 28 as of January 2026. The draft cites all three numbers without reconciling which population the safety claim covers. Small, but v1 item 12 established that count-slips invite an audit of every other number — and this one sits inside the load-bearing safety sentence.
- **Recommendation:** One consistent formulation: "the roughly two dozen programs operating over the past decade — about 20 in mid-2025, 28 by January 2026 — have produced no reported catastrophic breach in the public record." Align footnote 37.

**9. "The observation area that Houston has not yet built" — an asserted fact about Houston's landside plant with no source.**
- **Location:** Closing paragraph; echoed in the velvet-rope section ("A landside observation deck is a genuine good and Houston should build toward one").
- **Issue:** No brief documents whether IAH or HOU currently has a public observation area. It is a small claim, but it is a *checkable* claim about the client's own property in the final sentence of the report — the worst possible place to be wrong. If Houston has any landside viewing amenity, the closing beat collapses.
- **Recommendation:** Verify or soften: "back to the landside, outside the rope" carries the same emotional payload without asserting an inventory fact nobody sourced.

**10. "The public-safety literature notes drily that a bad actor can already buy a $39 fare."**
- **Location:** Lede, second paragraph.
- **Issue:** Vague attribution laundering an internal source. The "$39 ticket" line is from the Council's own public-safety brief (which said "$39 Spirit tickets"), not from any external literature. This is the v1 item-16 problem inverted: instead of naming the internal agent, the draft dresses the internal agent as a body of published work. Under the house tone rules, that's a vague attribution where a plain statement exists.
- **Recommendation:** State it as fact, unattributed: "a bad actor can already buy a $39 fare." The observation is self-evidently true and needs no invented provenance.

**11. "A marginal population that small... does not move the staffing requirement in the first place" — asserted, not supported.**
- **Location:** Staffing-lag rebuttal, "Why the counter-case is insufficient."
- **Issue:** No brief says a 50/day pilot leaves 1542.217 adequacy unmoved — that is an analyst judgment presented as settled. The public-safety brief's position is stricter: the staffing MOU is a *precondition* regardless of size ("any visitor pass business case that doesn't include a signed staffing/cost MOU... is booking a benefit while externalizing the cost"). The draft keeps the MOU in the 90-day list — good — but the rebuttal sentence dismisses the same constraint the action item exists to answer. Adequacy under 1542.217 is the Federal Security Director's call, not the Strategist's.
- **Recommendation:** Soften to a claim the record supports: "a population that small and that concentrated is the version of the program *least likely* to move the adequacy determination — and the written HPD/HFD understanding, negotiated before launch, is what proves it rather than assumes it."

---

## C. Cherry-picked evidence

**12. Southwest's response to the Hobby pilot is never modeled — the airline lens is applied only to the airport the report rejects.**
- **Location:** "The airlines are the real board of directors" — five paragraphs on United's MII lever, the 2030 lease, the rate-base rule, all at Bush; one sentence on Southwest at Hobby.
- **Issue:** The airline strategist's opening rule is unambiguous: "A visitor-pass strategy that does not model carrier response is not a strategy — it is a wish," and the brief names Southwest's specific exposure — 30–40-minute point-to-point turns for which "gate-area dwell and holdroom crowding are the enemy," making a program that adds bodies to Southwest's holdrooms "a direct operational threat." The report sends the pilot into that carrier's building at 93 percent concentration and never asks the brief's governing question of it: what will Southwest do? Does Hobby's use agreement carry its own MII exposure? Does Southwest object, acquiesce, or (per the brief's flagged conditionals) support? The United analysis is thorough; the Southwest analysis consists of a single sentence — and that sentence is item 13.
- **Recommendation:** Add a Southwest-at-Hobby passage doing for the recommended site what the United passage does for the rejected one: Southwest's turn-time intolerance, the holdroom question (a 50/day midday trickle vs. Southwest's departure pushes), the funding rule's application to Hobby's cost centers, and the honest unknown carried from [^23]. The design answer exists — off-peak hours and a checkpoint away from the departure banks keep visitors out of Southwest's turns — but it must be argued, not assumed.

**13. "Southwest is even more congestion-intolerant — one more reason Hobby is the better place" is a non-sequitur as written.**
- **Location:** Last sentence of the airlines section.
- **Issue:** Read it cold: the dominant carrier at the recommended site is *more* intolerant of exactly the load the program adds, *therefore* pilot there. The intended logic — a single-signatory environment is a cleaner negotiation, and a carrier that punishes congestion instantly enforces design discipline — is never stated. As printed, the sentence hands a hostile reader the report's own recommendation as a contradiction.
- **Recommendation:** Supply the missing middle: "Southwest's fast turns are even less tolerant of congestion than United's banks — which is precisely why the Hobby pilot must run midday-to-evening, away from the pushes. What Hobby offers in exchange is a single counterparty and a clean accountability boundary: one carrier to brief, one agreement to check, one checkpoint to protect."

**14. The convergence tally counts one dissent and quietly reclassifies the other.**
- **Location:** The confidence paragraph ("three named, two silent on location, and one honest dissent").
- **Issue:** The airline strategist's bottom line was that the *landside* version is the one recommendable "with the highest confidence" at a constrained dual-hub — i.e., the sterile-side pilot itself, at either airport, goes against that brief's first preference. The draft handles the landside argument well in the velvet-rope section and converts it into Phase 0 — a legitimate move — but the honesty tally then counts only the COO as a dissent. Two of eight analyses declined to endorse the recommended product; the paragraph reports one. Having built its credibility on an honest count, the draft cannot afford a second thumb on the scale.
- **Recommendation:** Extend the tally by one clause: "...one honest dissent on site, engaged and overruled above — and one dissent on product, the landside-first view, which the phasing absorbs as Phase 0 rather than overrules."

**15. "Feasibility is inversely correlated with the health of the hub" repeats the aphorism the same brief corrects.**
- **Location:** "The dead pioneer" section: "The feasibility of these programs is inversely correlated with the health of the hub. The airports that can run them easily are the ones the airlines abandoned."
- **Issue:** The airline strategist's own Detroit case study warns against exactly this generalization: DTW is a Delta hub with a durable program, and "the relevant variable is not 'hub vs. non-hub' but 'does the carrier's peak throughput have slack.'" The draft knows this — it cites Detroit's "circulation headroom" two sections later — but states the clean aphorism at the point of maximum rhetorical effect and saves the correction for a subordinate clause forty paragraphs away. That is the v1 item-18 pattern (a sweeping law from thin data) in new clothes.
- **Recommendation:** Correct it at the point of statement: "The feasibility of these programs tracks slack, not sentiment. The airports that run them easily either lost their hub — Pittsburgh — or, like Detroit, kept checkpoint headroom a peak-banked hub lacks."

---

## D. Logical gaps

**16. Exec summary #2 argues with the numbers of a program the report doesn't recommend.**
- **Location:** Executive summary, finding 2: "A 300-per-day cap is well under one percent of Bush's daily enplaned passengers... concentrated at specific lanes and hours."
- **Issue:** The recommendation is 50/day at Hobby. The summary's only sizing arithmetic describes 300/day at Bush — six times the cap, at the other airport. A Director reading only the summary (which is what executive summaries are for) never sees the recommended program sized at all. This is the summary-level face of item 3.
- **Recommendation:** One added clause: "the recommended pilot — 50 a day at Hobby, midday to evening — runs at roughly a sixth of that load through a single checkpoint at the smaller airport."

**17. The Pittsburgh causal phrasing invites a misreading the footnote contradicts.**
- **Location:** "The dead pioneer": "It ended in 2020, and the part that matters for Houston is that it never came back, and the reason was not COVID and not a security incident. It was construction."
- **Issue:** The record (reg brief, and the draft's own [^17]) is: COVID ended it; construction kept it dark. The sentence's grammar lets "the reason" attach to "it ended" as easily as to "it never came back" — and on the first reading, the draft appears to deny the documented cause of the 2020 shutdown. Precision matters here because Pittsburgh is the report's most-leaned-on precedent.
- **Recommendation:** "COVID ended it in 2020. What matters for Houston is why it never came back: not a security incident, not budget — construction."

---

## E. Weak rhetoric and flat prose

**18. Sentence three of the "argument in three sentences" is an 85-word freight train.**
- **Location:** Lede, "Here is the argument in three sentences."
- **Issue:** The device promises compression and delivers a sentence with nine commas, two em-dash asides, and a colon-delimited design spec. The three-sentence frame is good; the third sentence is a paragraph wearing a belt. It also buries the single most quotable formulation in the report ("it deserves to fail") at the end of a clause pile-up.
- **Recommendation:** Split it. "The right decision is a narrow yes: a hard-capped, off-peak, advance-vetted, twelve-month pilot at Hobby, funded outside the airline rate base and sold as community relations. Anything larger — at Bush, at scale, justified by revenue, layered onto construction — will be switched off in front of angry families on the days they most want it, and it deserves to fail." Four sentences that read like three.

**19. The concede-litany restates the shutdown statistics a fifth time.**
- **Location:** "Why the counter-case is insufficient," first two paragraphs — seven consecutive sentences opening "Concede that...", the first of which re-cites the 2026 checkpoint collapse already told in the lede, exec #2, the "scarce thing" section, and the counter-case.
- **Issue:** The Strategist's push-back on v1 item 25 defended the counter-case's re-use of the shutdown numbers, and that defense is accepted — the counter-case needs them. But the concede-litany is a *fifth* appearance, two paragraphs after the fourth, and the anaphora ("Concede... Concede... Concede...") is a consultant's drum where one beat would land harder. The section the reader most needs to trust opens with the report's most-repeated material.
- **Recommendation:** Keep the concessions; cut them to one tight paragraph that references rather than restates: "Concede all of it — the worst checkpoints in the country in early 2026, the fictional escort savings, the small demand, the peak-day suspensions, the residual risk, the staffing lag Houston cannot compress. Every concession is true." Then proceed to the turn, which is the section's real work.

---

## F. Structural issues

**20. The report's front-to-back architecture is now: memo to the Red Team → essay → memo to the Director. Pick one reader.**
- **Location:** Whole document.
- **Issue:** With the revision notes at top (item 1) and the drafting-history asides in the middle (item 2), the v2 draft addresses three audiences in sequence. Everything between — the lede, the argument, the counter-case, the pitch — is genuinely strong and reads as the long-form essay the spec demands. The frame around it does not.
- **Recommendation:** One reader: the Director. Revision notes out (separate file), drafting-history references out, convergence paragraph rewritten in-world (item 2). No other structural surgery is needed this round — the section order, the counter-case placement, and the rebalanced executive summary all work.

---

## Scorecard on the v1 ledger

Fixed and verified: items 1 (tally now honest in substance — see item 2 above for its packaging, and item 14 for the missing second dissent), 2 (launch condition is the right form), 3 (composite marked, confronted, and the closing beat is the best new writing in the draft), 4, 5, 6 (the COO rebuttal-and-banking move is genuinely good), 7, 8, 9, 10 (the site-independence paragraph is exactly what was asked), 11, 12, 13, 14, 15, 16 (in letter — see item 2), 17, 18, 19 (Phase 0/Phase 1 sequencing is the right answer), 20 (but see item 5 — the fix overshot into error), 21, 22, 23, 26.

Partially fixed: 24 (duration and cap named; threshold values still absent — item 7), 25 (reduced; one cut remains — item 19).

**Do not ship v3 without items 1, 2, 3, 5, and 6. Items 4, 12, and 13 are one working session; the rest are line edits.**
