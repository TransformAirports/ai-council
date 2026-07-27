# Red Team Critique — Strategist Draft v1
**Run:** visitor-access-at-houston-airports-2
**Target:** `outputs/stage2/strategist-draft-v1.md` ("The Velvet Rope at the Oversubscribed Door")
**Verified against:** all eight Stage 1 briefs (infrastructure-economist, operations-analyst, contrarian, airline-commercial-strategist, regulatory-political-analyst, airport-ceo, airport-coo, director-of-public-safety)

**Overall verdict before the itemized list:** This is a good draft with a serious spine — the "narrow yes at Hobby" architecture is defensible and the counter-case section is honest. But the draft has one load-bearing sentence that is false as written (the "convergence" claim, item 1), one internal contradiction it never notices (Hobby is also under construction, item 2), one framing device that its own recommendation refutes (the $39-ticket man, item 3), and it systematically suppresses the single strongest piece of counter-evidence in the COO brief (item 6). Fix those four and the report is strong. Ship it as-is and a skeptical Director's staff will find at least two of them.

---

## A. Unsupported claims

**1. The "convergence" claim is inflated, and it is the finding the whole recommendation rests on.**
- **Location:** "Why the counter-case is insufficient," final paragraph: *"The contrarian, the operator, the CEO, the regulatory analyst, and the public-safety chair converged independently on the same site. That convergence is the finding."*
- **Issue:** Five agents are claimed; only three delivered. The contrarian ("pilot at HOU, not IAH"), the operations analyst ("Pilot at HOU first"), and the regulatory analyst ("HOU is the lower-risk pilot site") named Hobby. The CEO brief never names a site — its verdict is "small, non-airline-funded, revocable pilot," site-agnostic. The public-safety chair says "capped, single-location, vetted pilot" — location unspecified. Worse, the COO — presumably "the operator" — leans the *other way*: the COO's case-FOR item 4 argues IAH's new ICP checkpoints make this "no better moment in a decade," and Example 3 says "For IAH, pick one checkpoint in one terminal for the pilot." If "the operator" means the ops-analyst, then the COO's dissent is simply missing from the count. Either way, the sentence "that convergence is the finding" is built on a manufactured 5-of-5 when the honest tally is 3 named, 2 silent, 1 arguably contrary.
- **Recommendation:** Restate honestly: three lenses independently named Hobby; two prescribed the same *shape* (capped, revocable, non-airline-funded) without naming a site; the COO saw a case for IAH's fresh checkpoint capacity that the strategist overrules for stated reasons. An honest 3-plus-2-with-one-dissent is still persuasive. A false 5-of-5 is a fact-checker veto waiting to happen.

**2. "No Bush-scale construction footprint" hand-waves past the draft's own evidence that Hobby is under construction.**
- **Location:** Exec summary #4 and the pitch section, "Site: Hobby" bullet.
- **Issue:** The draft's central structural argument is that active terminal construction is "the documented cause of death for these programs" (Pittsburgh), and exec summary #4 explicitly lists "a $470 million concourse expansion at Hobby" as part of Houston's capital-disruption exposure. Then the recommendation sends the pilot to Hobby with the phrase "no Bush-scale construction footprint" and never reconciles the two. The COO brief says the West Concourse expansion completes in 2027 — i.e., the pilot would launch into an active construction site at the recommended airport. The draft kills Bush with the construction argument and then exempts Hobby from the same argument by adjective ("Bush-scale").
- **Recommendation:** Address it head-on: state where the West Concourse work physically sits relative to the existing checkpoint and concourses, whether it compresses circulation the way Pittsburgh's did, and whether launch should be sequenced after 2027 completion. If the answer is "the expansion doesn't touch the checkpoint or existing sterile circulation," say so and source it. If the Council doesn't know, the recommendation must say "pending confirmation of construction phasing at HOU" — that is a real go/no-go condition, not a detail.

**3. The bookend character is refuted by the draft's own eligibility recommendation — and by the evidence on how visitors actually use these programs.**
- **Location:** Opening paragraph and closing paragraph (the man with the $39 ticket).
- **Issue:** Three problems. (a) He is fabricated and presented as fact: "Somewhere in that line stood a man..." and the closer asserts he "got his coffee and watched his airplane." No source. A hypothetical must be marked as one. (b) He is internally implausible: nobody buys a throwaway ticket to stand in a four-hour shutdown line for coffee. The scene undermines itself. (c) Most damning: the draft calls him "the customer a visitor pass program is designed to serve," then recommends eligibility limited to "military and USO send-offs, credentialed elder- and first-time-traveler assistance, sanctioned events and tours" — a program that would *exclude him*. Meanwhile the contrarian brief's DTW survey data says the dominant real use is meeting an arriving or departing traveler, not plane-watching. The framing device contradicts both the evidence and the recommendation.
- **Recommendation:** Either mark him as hypothetical and make him a greeter (the modal user per DTW's surveys), or keep the plane-watcher and confront the fact that the recommended narrow eligibility turns him away — which is actually an interesting, honest beat: the program the evidence supports does not serve the person the romance of the idea evokes. Use that or cut him.

**4. "The most oversubscribed checkpoint in Texas" — unsupported superlative.**
- **Location:** Second paragraph of the lede.
- **Issue:** No brief compares Houston's checkpoints to DFW, DAL, AUS, or SAT. The briefs support "among the worst TSA wait times in the country during the 2026 shutdown" — a stronger and *sourced* claim.
- **Recommendation:** Replace with the sourced national claim. Never trade a documented superlative for an undocumented one.

**5. Fabricated scene specificity in the lede.**
- **Location:** Opening sentence: "At 5:40 on a March morning... the queue at Terminal E... doubled back on itself twice and spilled toward the international arrivals hall."
- **Issue:** The sources say IAH waits exceeded four hours and roughly half of lanes were closed systemwide. No source puts the four-hour wait at Terminal E, at 5:40 a.m., doubling back twice. The Click2Houston figure for Terminal E is 45 minutes on a normal bad day — a different datum. Narrative license is fine; invented reportage detail attached to real citations is not, and footnote [^1] currently implies these specifics are sourced.
- **Recommendation:** Soften to what the record supports ("On the March 2026 mornings when...") or explicitly generalize. Do not let a footnote launder invented detail.

---

## B. Cherry-picked evidence

**6. The COO's "fresh checkpoint capacity" argument — the strongest single piece of counter-evidence to the draft's timing thesis — is suppressed entirely.**
- **Location:** "The dead pioneer is the most important benchmark" section; also exec summary #4.
- **Issue:** The COO brief states, in bold terms: "Houston has fresh checkpoint capacity, right now, uniquely. The ICP just added screening capacity at IAH. There is no better moment in a decade to absorb a modest, capped, off-peak visitor load than the year the new checkpoints come online," and explicitly frames Houston's timing as cutting "both ways." The draft presents timing as one-way fatal ("Houston is doing to itself, on purpose, the thing that killed the Pittsburgh program") and never acknowledges the ICP-capacity counter-argument exists. This is the exact behavior the run prompt bans: using a brief's data while ignoring counter-evidence in the same brief. The draft even cites the same COO/Community Impact material for the construction risk while skipping the capacity upside two paragraphs away.
- **Recommendation:** Present the COO's argument and beat it on the merits (e.g., ICP capacity serves Terminal E international flows where waits still hit 45 minutes; the Domestic Terminal Program will consume the slack; new capacity during a construction program is not durable slack). The rebuttal is available. Omission is not.

**7. Both sides of the concession-revenue question are asserted confidently, in opposite directions, to serve different arguments — and the airline strategist's caveat is dropped.**
- **Location:** Pitch section, "strongest case for" ("the concession spend it generates is yours under the hybrid-compensatory structure") vs. the airlines section ("Southwest... would also capture most of any concession upside, which is one more reason Hobby is the cleaner pilot site").
- **Issue:** The airline strategist's brief flags this precise question as *unresolved*: "The Council must confirm how Houston's agreement treats concession revenue before assuming any carrier will support the program on economic grounds," and the Southwest-capture scenario carries two explicit conditionals ("if the program lifts spend and if it is walled off from the gates") that the draft strips. As written, the draft tells the Director the airport keeps the upside at Bush and Southwest captures it at Hobby — under the same use agreement. Both cannot be casually true, and the brief says neither is confirmed.
- **Recommendation:** Pick one consistent treatment, restore the "confirm the revenue-sharing mechanics" caveat as a 90-day action item, and stop using the concession flow as a directional argument in two directions.

**8. The 300-passengers-per-hour design target is used where the ops analyst's real-world figure would cut against the draft.**
- **Location:** "The scarce thing is a lane at 6:10 a.m.," first paragraph ("about six percent of a single lane").
- **Issue:** The ops-analyst brief warns that 300/hr is a DHS *design* target and that actual planning throughput is 150–250 passengers/hour/lane — and adds that any Houston cap-setting "should use the airport's own checkpoint throughput data by hour and checkpoint," a caveat the draft never carries into its recommendation. At 150/hr, 18 visitors/hour is 12 percent of a lane, double the draft's figure. The draft picked the denominator that flatters its argument.
- **Recommendation:** Show the range (6–12 percent depending on realized lane throughput) and add the ops analyst's instruction — set the cap from IAH/HOU's own hourly checkpoint data — to the 90-day list.

**9. "Industry-standard 300-per-day cap" misdescribes the benchmark set.**
- **Location:** Exec summary #2.
- **Issue:** 300/day is Seattle's cap — the *largest* in the country. The distribution is DTW 75, PHL 100, MSY 50/100, TPA six per two-hour block. Calling the maximum "industry-standard" inflates the norm by 3–6x and softens the later pivot to a 50/day recommendation.
- **Recommendation:** "At the largest operating cap in the country — Seattle's 300 a day —..." The sentence gets stronger, not weaker.

**10. Hobby had the *worse* shutdown numbers, and the draft never metabolizes that.**
- **Location:** Throughout — 47.4 percent callout at HOU is cited in the lede and counter-case, then Hobby is recommended as the safer site without comment.
- **Issue:** The saturation argument the draft deploys against Bush applies at least as hard to Hobby on a shutdown morning: higher callout rate, single terminal, less checkpoint redundancy. The Hobby case rests on geometry, governance, and construction scale — none of which cures federal staffing collapse. A hostile reader will ask why the airport with the nation's *worst* callout rate is the "cleaner" site.
- **Recommendation:** One paragraph: the shutdown risk is site-independent and is answered by the throttle/blackout architecture, not by site selection; Hobby wins on the variables site selection *can* control. Say it before someone asks it.

---

## C. Logical gaps

**11. The 42.4 percent callout figure and the "6 percent absence from a 2 percent baseline" figure sit side-by-side, unreconciled.**
- **Location:** Lede + exec summary #2.
- **Issue:** These are different metrics from different sources at different scopes — local peak callout rates at Houston's two airports (KHOU) vs. national frontline absence (CNN) — juxtaposed in a single sentence as if commensurable. Same problem with "more than 300 officers resigned inside a month," a national figure that in context reads Houston-specific. A numerate reader hits 42.4 vs. 6 and stops trusting the paragraph.
- **Recommendation:** Label scopes explicitly: "nationally, absence rose to ~6 percent; at Houston's two airports, callout rates peaked at 42.4 and 47.4 percent, the worst in the country; more than 300 officers resigned nationwide within a month."

**12. "Five different operators independently concluding" — the paragraph names three.**
- **Location:** "The scarce thing is a lane at 6:10 a.m.," second paragraph (Seattle, Tampa, New Orleans).
- **Issue:** Arithmetic borrowed from the COO brief's five-program set (SEA, DTW, PHL, MSY, PIT) without carrying the programs over. Small, but it is exactly the kind of slip that invites an audit of every other number.
- **Recommendation:** Either add DTW's hours-cap and PHL's advance-window to the list or say "three."

**13. The "two-hour line versus two-hour-and-ten-minute line" is pseudo-quantification.**
- **Location:** End of the "scarce thing" section.
- **Issue:** No arithmetic supports ten minutes. Eighteen visitors an hour into a multi-lane checkpoint does not produce a derivable delay figure from anything in the briefs — and on a throttle-equipped program, the visitors are *paused* on that morning anyway, which is the draft's own design. The sentence concedes an effect the recommended design eliminates, using a number pulled from the air.
- **Recommendation:** Cut the fake precision. The honest version: "on the mornings that make the news, any discretionary load is indefensible — which is why the throttle exists."

**14. "None has produced a mass-casualty event or a catastrophic breach" states an absence-of-evidence as a verified fact.**
- **Location:** "The counter-case, honestly presented," first paragraph.
- **Issue:** The contrarian's actual claim is "I found no evidence of a resulting catastrophic breach" — a search result, not a certification. The run prompt demands verified incident histories; the draft hardens a non-finding into a finding.
- **Recommendation:** "no *reported* incident in the public record" — three words, defensible forever.

---

## D. Weak rhetoric and flat prose

**15. The report cites its own commissioning instructions as an authority.**
- **Location:** End of "Start with the number" section: "The run that produced this report ruled the 'pays for itself' argument out of bounds, and it was right to."
- **Issue:** Process exhaust. The Director does not know or care what "the run" ruled; a report that appeals to its own terms of reference for analytical cover is begging the question in public.
- **Recommendation:** Delete. The Seattle evidence in the same paragraph already does the work.

**16. Internal Council agents appear as on-stage characters in a report addressed to the Director of Aviation.**
- **Location:** "Why the counter-case is insufficient" ("The contrarian who built the strongest case against conceded this directly: '...'"; "the contrarian's bottom line is fair"; "the public-safety chair concedes...").
- **Issue:** Quoting the Council's own internal briefs as if they were external authorities is the "As the X brief notes..." disease wearing a costume. To the reader, "the contrarian" is nobody. The concessions are real analysis; the attribution wrapper is machinery showing.
- **Recommendation:** Keep the concessions, absorb the attributions: "the strongest version of the case against concedes that a well-bounded trough program adds little load." If the Council's method must be visible, put it in a scope note, not the argument.

**17. "Perhaps 80 percent of the goodwill" is a spitballed number wearing a percent sign, uncited in the pitch.**
- **Location:** Pitch section, "Eligibility" bullet; also exec-adjacent counter-case ("capture perhaps 80 percent of the goodwill").
- **Issue:** This is the contrarian's illustrative guess ("perhaps 80% of the goodwill at 5% of the volume"), presented in the decision section with no footnote and no flag. Every other derived number in the draft is honestly bracketed; this one isn't.
- **Recommendation:** Either strip the number ("most of the goodwill at a fraction of the volume") or footnote it as an illustrative ratio, not an estimate.

**18. "The revenue thesis has historically lost to the experience thesis" generalizes from one airport.**
- **Location:** Exec summary #8 and the money section.
- **Issue:** "Historically" is one data point — Seattle. The infra-economist's phrasing had the same flaw; the draft inherited it uncritically. One program's self-description is an anecdote, not a history.
- **Recommendation:** "At the one airport that launched on a revenue rationale — Seattle — the revenue thesis lost to the experience thesis within a few years." Specific beats sweeping, per the house tone rules.

---

## E. Missed counter-arguments

**19. The airline strategist's landside alternative — the highest-confidence version of the whole concept — is never evaluated.**
- **Location:** Absent; belongs in or after "The airlines are the real board of directors."
- **Issue:** The airline strategist's bottom section is explicit: confine the visitor concept to public, pre-security space (greeting areas, landside events, observation) and "most of this carrier risk evaporates... That is the version of a 'visitor program' a strategist can recommend at a constrained dual-hub system like Houston's with the highest confidence." The run prompt's use cases explicitly include "publicly accessible or post-security non-SIDA areas." The draft argues sterile-side-or-nothing and never explains why the cheaper, veto-proof landside version — alone or as Phase 0 — loses to a sterile-side pilot. A Director's cheapest question ("why not do the landside version first?") currently has no answer in the report.
- **Recommendation:** Add the comparison and beat it honestly (the sterile-side access *is* the product; landside amenities don't deliver the gate moment) or fold landside programming in as the Phase 0 the phasing logic naturally wants.

**20. Reconnaissance, sterile-side hand-offs, and insider-assistance surface are raised in the counter-case and never rebutted.**
- **Location:** "The counter-case" (raised) vs. "Why the counter-case is insufficient" (absent).
- **Issue:** The rebuttal section answers saturation, suspension, density/accountability, and staffing — and silently drops the contrarian's residual-risk trio (long-dwell reconnaissance population, hand-off/staging risk, insider surface). The run prompt lists insider assistance and reconnaissance as required security-case elements. An unanswered objection the draft itself printed is worse than one it never mentioned.
- **Recommendation:** Two sentences in the security rebuttal: advance application with named identity and TSA adjudication makes a pass-holder the *most* attributable person in the terminal; the cap and single-location design bound the dwell population; and the unvetted way to conduct reconnaissance — a refundable ticket — remains strictly easier. The material is in the public-safety brief's logic; use it.

**21. Organized-labor opposition is documented in two briefs and appears nowhere in the draft.**
- **Location:** Absent; belongs in the political-risk discussion.
- **Issue:** Both the regulatory analyst and the COO flag the APFA's on-record reaction to myPITpass ("bad idea," "clog already frustratingly long TSA security lines") and the reg analyst explicitly instructs: expect the same framing in Houston and pre-position the "identical screening, watch-list vetted" rebuttal. A council-visible city department launching this program will face that soundbite in week one, and the draft's political section — otherwise strong — never arms the Director for it.
- **Recommendation:** One paragraph in the political discussion or a 90-day communications line item.

**22. Cybersecurity and privacy — a named success criterion — are absent, despite an on-point incident in the briefs.**
- **Location:** Absent; the run prompt's security criterion names "cybersecurity and privacy" and the recommendation spec names "privacy controls."
- **Issue:** The program collects Secure Flight Passenger Data on members of the public and runs on a registration platform — and the ops-analyst brief records that SEA's program was knocked offline by the Port of Seattle's 2024 cyberattack. The draft recommends a "live registry of who is inside the sterile area" without a word on data handling, retention, or the demonstrated cyber failure mode of the reference program.
- **Recommendation:** Add a short privacy/cyber paragraph: what data is collected, who holds it, retention limits, TPIA/open-records exposure for a city department, and the SEA outage as the precedent for platform fragility.

---

## F. Missed lenses / scope gaps against the run prompt

**23. The definitional success criterion — visitor pass vs. gate pass vs. badging vs. escorted vs. SIDA/CIDA vs. FIS — is never delivered.**
- **Location:** Absent; the run prompt lists it first under both "What this IS" and "Success criteria."
- **Issue:** The draft gestures at the taxonomy once (the escort-labor paragraph) but never defines what the pass *is*: who may enter, which areas (domestic sterile, non-SIDA), and — critically — the regulatory analyst's hard exclusion: CBP-controlled FIS space and international corridors are never available to a visitor pass. At an international gateway like IAH that exclusion is a design boundary, and it is nowhere in the draft. The run prompt's "What this is NOT" expressly bans conflating these space types; the draft avoids conflation mostly by avoiding the topic.
- **Recommendation:** A tight definitional passage (150–250 words) early in "The argument," including the FIS/CBP exclusion and the distinction from airline gate passes and badged access. This is a checklist item the fact-checker and the client will both look for.

**24. Pilot duration and utilization stop-criteria are specified by the run prompt and only half-delivered.**
- **Location:** Pitch section, "First 90 days" and stop-criteria sentence.
- **Issue:** The run prompt requires "pilot duration, success and stop criteria." The draft gives stop criteria in kind (wait threshold, incident threshold, utilization floor) but no values and no pilot duration — six months? A year? Renewed how? The insurance and legal-review cost elements from the success criteria are likewise absent (legal review appears once, in a cost list).
- **Recommendation:** Name a duration (12 months captures a full seasonal cycle including one peak-blackout period) and commit to publishing threshold values at launch even if the report only frames them.

---

## G. Structural issues

**25. The shutdown statistics and the Pittsburgh story are each told four times.**
- **Location:** 42.4/47.4 percent + four-hour waits: lede, exec summary #2, "scarce thing" section, counter-case, concessions list. Pittsburgh: exec summary #4, its own section, counter-case, pitch "Do not" bullet.
- **Issue:** Repetition an exec summary licenses once becomes padding by the third body appearance. The counter-case restatement of the callout figures is a full re-litigation of material the reader has now seen twice; the momentum sag in the middle third of the report is mostly this.
- **Recommendation:** Full treatment once in the body; thereafter, reference ("the March numbers," "the Pittsburgh precedent"). Recovers 300–400 words and the pace.

**26. The executive summary runs ~850 words against a ~1,100-word spec, while carrying eight numbered findings that the body then re-argues nearly verbatim.**
- **Location:** Executive summary.
- **Issue:** Mild spec shortfall, but the real problem is allocation: the summary spends its words repeating the body's statistics instead of doing the one thing only a summary can — the decision, conditions, cost, and first steps in the Director's language. Items #2–#4 are compressed body sections; the recommendation paragraph, the best part, is one paragraph.
- **Recommendation:** Rebalance toward the decision: expand the recommendation, conditions, and stop-criteria treatment; compress the evidence recaps to clauses. That also closes the word gap honestly.

---

*Items 1, 2, 3, 6, and 19 are the ones that change the report's defensibility rather than its polish. The Strategist should address every item but must not ship v2 without those five.*
