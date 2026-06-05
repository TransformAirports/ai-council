# Red Team Critique v1
## Of: Strategist Draft v1 — "The Cheapest Lever"
*Indoor Signage Best Practices Run | June 3, 2026*

This draft is more disciplined than the average first pass. The opening scene works. The Frankfurt-as-governance-proof move is genuinely smart. The MWAA-specific section is grounded in real numbers and reasonable structuring. But the draft has thirty-three distinct problems, several of which are load-bearing. The most serious are the math error on cost ratios, the under-engagement with the Contrarian's strongest point about Zurich/Google, the misrepresentation of the Munich eye-tracking finding, and the consultant-report cadence of the executive summary and the implications section. Address these or the report is vulnerable to a hostile reader.

---

## A. Invented or Mis-stated Numbers

**1. The "0.1 to 0.2 percent of the capital program" claim is mathematically wrong.**
- *Location:* Section V, "The cheapest-lever claim, rigorously," paragraph 2.
- *Issue:* "$5 to $10 million one-time wayfinding investment at MWAA... is on the order of 0.1 to 0.2 percent of the 2025–2039 capital program." The arithmetic: $5M / $9,000M = 0.056%; $10M / $9,000M = 0.111%. The actual range is 0.06%–0.11%, not 0.1–0.2%. The Executive Summary point 1 correctly says "under 0.2 percent" for an $8M program (also imprecise but defensible). Section V doubles the percentage. A skeptical reader runs this math in their head and the credibility of the whole cost-asymmetry argument leaks.
- *Recommendation:* Either say "under 0.15 percent" (true) or recalculate against MWAA's per-year CapEx ($600M/yr per the Infrastructure Economist brief), in which case $5–10M is 0.8–1.7% of an annual program. Pick the framing and get the arithmetic right.

**2. The "$1 to $5 million per year" incremental concession revenue range is an analyst construction presented as derivative of brief evidence.**
- *Location:* Section V, "The cheapest-lever claim, rigorously," paragraph 2.
- *Issue:* The Infrastructure Economist brief calibrates the elasticity precisely: a 1% dwell-time improvement yields $660K–$880K annually at MWAA. The strategist's "$1 to $5 million per year" implies a 1.5–7.5% dwell-time gain, which is not supported anywhere. The range floor ($1M) is above the brief's actual single-percentage-point upper bound ($880K).
- *Recommendation:* Either cite the brief's range ($660K–$880K per percentage point) and let the reader multiply, or explicitly state "if a 2–6% dwell-time gain is achieved" and own that the multiplier is the analyst's, not the brief's.

**3. The "100:1 or better" cost-to-value ratio is rhetoric, not arithmetic.**
- *Location:* Section V, "The cheapest-lever claim, rigorously," paragraph 1.
- *Issue:* "The order-of-magnitude ratio between cost and value can be reasonably argued at 100:1 or better." No brief supports a 100:1 claim. The brief math: $5M cost, $660K–$880K per year per percent dwell improvement. Even at a generous 5% sustained gain, value is $3.3–4.4M/yr; over a 10-year horizon, that's roughly 6–9:1, not 100:1. To hit 100:1 the strategist needs to either capitalize a perpetuity at very low discount rates or include unverified maintenance savings and revenue-loss recovery vendor figures.
- *Recommendation:* Drop "100:1 or better." Replace with the actual multiple the brief math supports, or cite the IRR framing the Infrastructure Economist brief uses verbatim ("an IRR that most capital programs cannot match").

**4. The "eighty percent of customer service agent time" figure is leaned on as load-bearing four separate times despite the brief flagging it as Mappedin-sourced industry estimate.**
- *Location:* Executive Summary point 6, Section III "Decision Point Is the Unit of Analysis" paragraph 3, Section III "Contradiction Debt" paragraph 5, Section V "cheapest-lever" paragraph 3.
- *Issue:* The Operations Analyst brief sources this to Mappedin (a wayfinding-software vendor), with no Ponemon or BLS or ACI primary source. The strategist treats it as established. The Contrarian or a hostile reader will flag this.
- *Recommendation:* Either drop two of the four uses and caveat the remaining as "industry estimates suggest" or replace with the FAA-cited ACI ASQ data on wayfinding as a top-six satisfaction driver (Operations brief, evidence section), which is methodologically stronger.

**5. The "$740,000 annually" sign maintenance figure is double-counted and over-trusted.**
- *Location:* Executive Summary point 6 (implicit), Section III "Contradiction Debt" paragraph 5, Section V "cheapest-lever" paragraph 2.
- *Issue:* The Infrastructure Economist brief explicitly notes: "Traditional airport sign maintenance: over $740,000 annually — Ponemon Institute 2023 study, cited in display vendor literature." That is a vendor-cited Ponemon claim — uncorroborated by any primary source the brief was able to locate. The strategist uses it in load-bearing math ("plus reductions in maintenance-line spending currently running at $740,000 annually on the legacy system") without flagging the provenance.
- *Recommendation:* Caveat once when introduced, then either build the argument without it or replace with the Denver SignAgent work-order-time reduction (4–5 days to minutes) as a more concrete, defensible cost story.

**6. The "$15 to $25 million for a phased rationalization" is presented as if calibrated to brief evidence; it is not.**
- *Location:* Section VI "Implications," observation Two.
- *Issue:* The strategist writes "calibrated against the Heathrow framework and against the Ontario International experience." Heathrow was £10M (~$12.5M) for five years across an 80M-passenger airport. The Ontario data point ($485K → $1.3M, 168% overrun) is a single project at a small hub. Neither produces a $15–25M MWAA estimate without additional assumptions the strategist doesn't show. The number reads as an analyst's instinct dressed as derivation.
- *Recommendation:* Show the work — "Heathrow scaled by passenger volume yields ~$8M; apply the Ontario overrun multiplier (2.7x) and the Chief Engineer's 40–50% live-terminal premium to get $X." Or state explicitly: "an order-of-magnitude estimate; precise scoping is downstream of the masterplan studies already budgeted."

**7. The "two-thirds including United Express" figure for IAD enplanements is stated as "roughly two-thirds" and as "66 percent affiliated-carrier share" in different places — inconsistency.**
- *Location:* Executive Summary point 8 ("two-thirds"); Section V "lease-structure argument," last paragraph ("66% affiliated-carrier share" implied).
- *Issue:* The Airline Commercial Strategist brief gives "approximately two-thirds" for enplanements and 56–59.6% for landed weight. The draft moves between figures without specifying which metric. A reader will notice.
- *Recommendation:* Pick enplanements (the metric the brief actually anchors at "two-thirds") and use it consistently.

**8. The "Concourse B" reference for MWAA Design Manual volumes drops Concourse Z.**
- *Location:* Section VI, observation One.
- *Issue:* "MWAA's Design Manual currently runs to seven volumes, with separate tenant design standards for IAD's Main Terminal and Concourse B — two parts of the same airport." The Regulatory/Political brief is explicit: "IAD Vol. 2 (Main Terminal/Concourse Z Tenant Design Standards), IAD Vol. 3 (Concourse B Tenant Design Standards)." Concourse Z is the *international arrivals* level — meaningfully relevant to the CBP FIS argument the strategist makes elsewhere. Dropping it makes the example weaker than it should be.
- *Recommendation:* Add Concourse Z. The fragmentation argument is stronger when the reader sees three named volumes for one airport, not two.

**9. "Heathrow's £10 million five-year framework" cited without 2013-dollar caveat the brief flagged.**
- *Location:* Executive Summary point 1, Section V paragraph 2.
- *Issue:* The Infrastructure Economist brief explicitly cautions: "Heathrow's £10M framework is a 2013 figure. Construction cost inflation since then... means a comparable program today would cost materially more." The strategist scales the Heathrow figure to MWAA passenger volume but does not adjust for thirteen years of cost escalation.
- *Recommendation:* Inflation-adjust to 2026 dollars (UK construction inflation ~50–60% over the period, depending on index) — that bumps the implied MWAA scale to ~$12–13M, which actually *strengthens* the case once you also factor in the live-terminal premium.

---

## B. Misrepresented or Cherry-Picked Evidence

**10. The Munich eye-tracking finding is restated as a different finding.**
- *Location:* Executive Summary point 3; Section III "Why Digital Is Not the Answer the Vendors Sell," paragraph 3; Section V "digital-investment argument" last paragraph.
- *Issue:* The actual Munich finding (Operations Analyst brief, Technology Scout brief): "passengers largely ignored information on navigation signage that wasn't relevant to their journey." The strategist reframes this multiple times as: passengers "stop reading digital displays mid-corridor when the content rotates between navigation and advertising" and "learn to filter content that changes unpredictably." The Munich study did *not* find that passengers filter rotating/dynamic content because it rotates. It found they filter content irrelevant to their journey. The strategist is conflating relevance-filtering with variability-filtering. The Munich data does not support the strategist's claim about digital displays specifically.
- *Recommendation:* Either restate the Munich finding accurately (passengers ignore irrelevant content) and let the implication for digital displays be inferred separately, or cite a different study that actually measures the variability-filtering effect.

**11. The opening Concourse C → Concourse D scenario is overdetermined.**
- *Location:* Section I "The Decision Point," paragraphs 1–3.
- *Issue:* United's actual MCT is 35 minutes (Airline Commercial Strategist brief, quote 4); Mobile Lounge runs every 5 min, direct trip up to 15 min. The strategist's narrative — twenty-minute buffer collapses if she takes the wrong mode — assumes a worst-case path (AeroTrain to C, return, walk, wait) that the brief does not establish as typical. The brief's framing is that the MCT figure is "constructed for the best-case connection." The strategist's claim that she is "with high probability, on a later flight" is rhetorical, not evidenced.
- *Recommendation:* Either soften ("the buffer can collapse to negative") or add a specific source for misconnect probability at IAD D-gate connections. The scene is the report's hook — it should not collapse to anecdote under scrutiny.

**12. The Frankfurt 1972 analogy understates that Aicher worked on a new terminal, not a retrofit.**
- *Location:* Section III "Wayshowing Distinction and the Committee Problem," paragraph 3; Section V "What the capital-base argument gets right," paragraph 2.
- *Issue:* The strategist uses Aicher's Frankfurt as proof that "governance discipline was present without the matching capital event." But Aicher built the standard at the design stage of a new terminal — the Aviation Historian brief makes clear his "contract included spatial separation of commercial advertising from the wayfinding system" and the rules were "embedded in the airport's operating architecture." This is the *opposite* of imposing governance on an existing fragmented terminal. The Contrarian's capital-base argument is therefore not fully refuted; Frankfurt is also a capital-event story, just an earlier one.
- *Recommendation:* Engage the limitation honestly. The argument the strategist actually has is that PANYNJ (a retrofit case) is succeeding, not that Frankfurt proves retrofits work. Drop Frankfurt as the refutation; use PANYNJ's *actual* progress (manual published 2020, prototype rollout active) as the harder evidence.

**13. The "$700 million annually" lost-concession figure is included three times despite the strategist flagging it once as vendor-sourced.**
- *Location:* Section III "Contradiction Debt" paragraph 5, Section V "What the digital-investment argument gets right" paragraph 2.
- *Issue:* Both the Infrastructure Economist and Technology Scout briefs explicitly disown this number. The Tech Scout brief calls it "not an audited number" and untraceable. Including it three times — even with caveats — repeats the vendor's claim into the reader's memory. The brief evidence the strategist actually has (the 89-airport 2024 study with the 6%/8% elasticity) is stronger, peer-reviewed, and sufficient.
- *Recommendation:* Cite the $700M figure once at most, immediately disowning it, then build the entire revenue case off the 89-airport elasticity. Strike the other two mentions.

**14. The "37% / 40% / 25%" LED vendor numbers are recapitulated in the counter-case section even after the strategist correctly disowns them.**
- *Location:* Section IV "The Counter-Case" bullet 4; Section V "digital-investment argument" paragraph 2.
- *Issue:* The strategist steelmans the Contrarian's reliance on these numbers by reciting them, then in V notes they "have not been independently audited." The recitation in IV serves a rhetorical purpose (presenting the strongest counter) but the numbers themselves are not load-bearing for the Contrarian's actual argument and citing them gives them more rhetorical weight than they deserve.
- *Recommendation:* In IV, replace the LED vendor figures with the Contrarian brief's actual stronger argument: that Apple/Google indoor mapping is rapidly substituting and that airline app usage is up 7 points in five years. The vendor LED claim is the weakest part of the Contrarian case; steelmanning it strengthens the strategist's own rebuttal but at the cost of imprecision.

**15. The "0.2 percent of the capital plan" claim in Executive Summary point 1 trips over the same problem as critique #1, plus understates the Heathrow inflation issue from #9.**
- *Location:* Executive Summary point 1.
- *Issue:* "Heathrow's five-year wayfinding consultancy framework, scaled to MWAA's traffic, suggests an eight-million-dollar comprehensive program — under 0.2 percent of the capital plan." $8M / $9B = 0.089%, which is "under 0.1%," not "under 0.2%." The strategist is rounding generously upward to make the asymmetry sound less dramatic than the math actually supports — which is the opposite of what they should be doing.
- *Recommendation:* "Under 0.1 percent of the capital plan." Or, better, "less than one part in a thousand." This makes the cost-asymmetry argument more powerful, not less.

---

## C. Logical Gaps and Non-Sequiturs

**16. The MII workaround claim in Section VI observation Two doesn't survive the Airline Commercial Strategist brief's own threshold.**
- *Location:* Section VI, observation Two; also Executive Summary point 8.
- *Issue:* The strategist writes that a $15–25M program "treated as an operating standard with capital classification reserved for infrastructure-grade elements... need not trigger formal MII review at affirmative-MII thresholds." But the Airline Commercial Strategist brief is explicit: "A capital program under the threshold for MII review (typically $5-10 million, varying by agreement) avoids the formal process. A comprehensive, terminal-wide overhaul will cross that threshold." A $15–25M program will cross the threshold by any reasonable accounting. The strategist's "need not trigger" depends entirely on classifying most of the spend as operating expense — which is plausible but is not a free pass on MII review, and the brief does not say it is.
- *Recommendation:* State the strategy honestly: "structured to minimize the capital-classified component below MII thresholds, recognizing this requires aggressive classification that airlines may challenge." Don't claim it sidesteps MII automatically.

**17. The "second-best at one percent of the cost" claim for the IAD AeroTrain/Mobile Lounge decision-point fix doesn't engage the brief's actual finding.**
- *Location:* Section VI, observation Three.
- *Issue:* The Airline Commercial Strategist brief is explicit: "This is a decision chain, not a single decision point. Each link is a wayfinding problem." The strategist's recommendation — "the sign must answer the question *which mode do I take?* by pointing to the FIDS first, and only then routing the passenger" — restates this as a single decision point ("solvable inside MWAA's authority"). It papers over the brief's finding that this is a chain that signage alone cannot fully resolve.
- *Recommendation:* Concede the chain problem. The signage argument is that it *improves* the chain (by ordering it correctly), not that it resolves the underlying transport-mode mismatch. The strategist's existing prose acknowledges "second-best at best" but then claims solvability — pick one.

**18. The "the dwell-time elasticity from the 2024 89-airport study" is applied to wayfinding without the brief's caveat that the study does not isolate wayfinding as the driver.**
- *Location:* Section III "Contradiction Debt" final paragraph, Section V "cheapest-lever" paragraph 2.
- *Issue:* The Infrastructure Economist brief flags this directly: "Dwell time improvements are not solely attributable to wayfinding... The revenue impact of wayfinding improvements should be modeled as a share of the total dwell time effect, not the entirety of it." The strategist applies the full elasticity to wayfinding-driven dwell-time gains in the MWAA payback math.
- *Recommendation:* Discount the elasticity. If wayfinding is one of, say, five drivers of dwell time (security throughput, lounge access, retail mix, scheduling, wayfinding), allocate proportionally. Even at 20% allocation the case still holds and the payback math becomes credibly defensible instead of optimistically constructed.

**19. The "lifecycle math is more sobering than capital programs typically recognize" paragraph is about digital displays but is used to argue against digital investment broadly.**
- *Location:* Section III "Why Digital Is Not the Answer the Vendors Sell," paragraph 4.
- *Issue:* The Chief Engineer's lifecycle data (5–7 years for panels, 3–5 for media players, 35–40% of FIDS units operating beyond lifecycle) supports a claim that digital displays are *under-refreshed*, not that they shouldn't be deployed. The strategist's framing — "Airports are now carrying digital signage fleets installed in the early 2010s that have never been refreshed" — is a maintenance failure, not a digital-vs-static failure.
- *Recommendation:* Re-frame this paragraph as: the lifecycle data argues for *funded refresh discipline*, not for less digital. Otherwise it reads as motivated reasoning.

**20. The "wayfinding is the cheapest lever that the airport can pull without negotiating with someone who can say no" closing line of Section V doesn't survive Section IV's own concessions.**
- *Location:* Section V, last paragraph.
- *Issue:* The strategist has just spent six pages conceding that the lease structure, TSA, CBP, fire marshal, advertising concession, MII clause, and ADA all constrain wayfinding decisions. The "without negotiating with someone who can say no" claim refers only to common areas. Stating it as a flat summary undercuts the strategist's own careful concessions. A skeptical reader notices the rhetorical bait-and-switch.
- *Recommendation:* "...the cheapest lever the airport can pull *in its common-use areas* without external negotiation." The qualifier is already in the argument; put it in the slogan.

**21. The "Airport apps are not the substitute" claim slips between two different counter-arguments.**
- *Location:* Executive Summary point 4; Section III "Why Digital Is Not the Answer," last paragraph; Section V "smartphone substitution argument," paragraphs 1–3.
- *Issue:* The 7% adoption rate is for the airport's own app (which no one disputes is small). The Contrarian's argument is that third-party tools (Apple Maps, Google Maps Live View) are filling the gap — *not* the airport apps. The strategist's response — "the passenger who most needs wayfinding help... is, by definition, the passenger least likely to have installed a third-party indoor navigation tool" — is plausible but unsourced. Apple Maps and Google Maps are *installed by default* on the relevant phones. The strategist conflates "third-party indoor navigation tool" with "specialized navigation app."
- *Recommendation:* Source the claim about whose-phone-has-what or restate it more carefully: the passenger under stress doesn't *consult* the navigation tool, regardless of whether it is installed. The Heathrow eye-tracking finding about decision points actually supports this framing better than the strategist uses it.

---

## D. Weak Rhetoric and Consultant-Report Prose

**22. The Executive Summary is eight bold-led numbered paragraphs — the literal definition of a consultant deck slide.**
- *Location:* Section II.
- *Issue:* The run prompt asked for prose "in the tradition of Matt Levine on aviation, not a consultant thought-leadership piece." This is the most consultant-deck section of the draft. Each paragraph opens with a bold thesis sentence followed by bracketed brief citations. The reader gets eight versions of the same rhetorical move. By point 6 the reader is skimming.
- *Recommendation:* Rewrite as 4–5 paragraphs of running prose with the same content. The bold lead is fine for one or two; eight in a row is decking. Or cut to three or four high-leverage points and let the body do the rest.

**23. Section V's parallel headers ("What X gets right and what it misses") read as a template.**
- *Location:* Section V, all five subsection headers.
- *Issue:* Four identically structured subsection openers in a row is a tic. McPhee would not write this.
- *Recommendation:* Vary the openers. The structure (concede then refute) can persist; the rhetorical shape doesn't have to. Or replace the parallel headers with subtle scene-setting transitions and let the structure emerge.

**24. "The arithmetic is not subtle" appears once but the same rhetorical move (let the math speak for itself) appears five times in different phrasings.**
- *Location:* Section III "Contradiction Debt" final paragraph; Section V "cheapest-lever"; Section VI observation Two.
- *Issue:* It's a tic. Each occurrence weakens the move.
- *Recommendation:* Keep one. Show the math the other times instead of asserting that the math is obvious.

**25. "Per Mollerup, the Danish designer..." is grammatically ambiguous.**
- *Location:* Section III "The Decision Point Is the Unit of Analysis," paragraph 2.
- *Issue:* Per is his first name. The sentence reads at first scan as "According to Mollerup..." Casual readers will need to re-parse. McPhee would put "the Danish designer Per Mollerup" or "Per Mollerup, the Dane who..." — anything to disambiguate.
- *Recommendation:* "The Danish designer Per Mollerup" or restructure the sentence.

**26. "Buzzword" hedges: "structural," "structurally," "structurally identical" appear 11+ times.**
- *Location:* Throughout. Especially Section III "Decision Point" paragraph 1, Section III "Wayshowing Distinction" paragraphs 2–3, Section V "lease-structure argument," Section V "cheapest-lever."
- *Issue:* "Structural" is doing too much work in this draft. It is the strategist's hedge of choice when a sharper word would commit the argument. "Structurally identical" — meaning what? Twin? Analogous? Same problem?
- *Recommendation:* Strike half the uses. Replace with specifics.

**27. Section VI's "One. Two. Three. Four. Five." opens with the most consultant-deck cadence in the draft.**
- *Location:* Section VI "Implications for MWAA."
- *Issue:* "Five observations follow from this position, in the order they would have to be addressed. **One.** ... **Two.** ..." The run prompt asked for narrative prose. This is recipe.
- *Recommendation:* Restructure as 5 short prose sections with substantive headers (the way Section III handles its subsections). Or compress to three observations and write them out.

**28. The opening scene is good but the "Multiply that decision point by every connecting passenger" line is the kind of motivational-speaker move the prompt explicitly bars.**
- *Location:* Section I, paragraph 3.
- *Issue:* "Multiply that decision point by every connecting passenger, every day, at every American hub. That is the cost of bad airport wayfinding." It is the most Tom-Peters sentence in the draft. The scene before it was specific; this sentence is hand-waved aggregation.
- *Recommendation:* Either replace with a specific figure (X% of US enplanements are connecting; Y% of those route through airports with documented wayfinding failure modes), or strike the line entirely and let the scene do the work.

**29. The closing scene returns to the passenger — good — but the final sentence borders on aphorism.**
- *Location:* Last two paragraphs.
- *Issue:* "If MWAA does not do the work, she will be on a later flight, and we will continue to call it a carrier delay." This lands, but barely. The "we will continue to call it" formulation is the kind of writerly tag that risks reading as op-ed rather than analysis.
- *Recommendation:* Test the line against the Matt Levine standard. If it sounds like something Levine would write, keep it. If it sounds like an editorial sign-off, sharpen.

---

## E. Missed Counter-Arguments

**30. The Contrarian's sharpest data point — Zurich's wayfinding reputation may owe to Google Live View, not signage — is unaddressed.**
- *Location:* Not addressed.
- *Issue:* Contrarian brief paragraph: "Zurich's celebrated wayfinding may owe part of its reputation to Google Maps indoor navigation, not to its sign hierarchy." This is the single most damaging contrarian claim because Zurich is one of the four named exemplars the thesis depends on. The strategist mentions Google Live View at Zurich in passing but never confronts the claim that the wayfinding reputation may be partly the digital overlay.
- *Recommendation:* Address it directly. Either acknowledge the digital overlay is part of Zurich's success (which strengthens the broader "match medium to information-change rate" argument) or cite evidence that Zurich's pre-Google reputation was already strong. The Aviation Historian brief gives you the latter — Zurich's standards manual and tenant-enforcement structure predate Google Live View by years.

**31. The Contrarian's depreciation argument (existing signage is aging; capital renewal is unavoidable) is not addressed.**
- *Location:* Not addressed.
- *Issue:* Contrarian Bullet 7: "Replacing aging sign infrastructure is not optional any more than replacing aging HVAC is optional. The question is not whether capital will be spent — it is whether it will be spent reactively or strategically." The strategist's argument that wayfinding is the "cheapest lever" implicitly assumes the alternative is no spending. But the Contrarian's depreciation point is that spending will happen regardless; governance determines whether it accumulates as patchwork or as a system.
- *Recommendation:* This is actually a friendly fact for the thesis if the strategist names it. The depreciation argument strengthens "governance is the binding constraint" rather than undermining it. Add a paragraph that absorbs it.

**32. The Contrarian's "staff-based interventions can be deployed in weeks without airline consent" point is brushed past.**
- *Location:* Section V "cheapest-lever" paragraph 3.
- *Issue:* The strategist says these interventions are "valuable" and "complementary." That's not a refutation. The Contrarian's actual claim is that they offer faster, cheaper, lower-MII-exposure paths to similar passenger experience improvements. The strategist needs to either price them against signage rationalization or concede they should be funded in parallel.
- *Recommendation:* Concede explicitly: "These should be funded; they are not substitutes for the structural fix." Then explain why both are needed.

---

## F. Under-Used Lenses

**33. The Aviation Historian's Pittsburgh three-chapter case is used for one quote about "expansive natural flow" but the full lesson is the load-bearing one — and it goes unused.**
- *Location:* Section VI, observation Four (one passing reference).
- *Issue:* The Pittsburgh case is the cleanest empirical demonstration that wayfinding must be calibrated to operational era, not just construction era. Chapter 2 (the post-hub mismatch from 2004–2025) is exactly the MWAA situation: a wayfinding system that was correct for one operational model and is now wrong for a different one. The historian gives the strategist a 20-year empirical case study; the strategist takes one sentence from chapter 3.
- *Recommendation:* Use Pittsburgh in the contradiction-debt argument. Two decades of operating with a connection-optimized wayfinding system after the hub collapsed is the clearest analog to IAD operating with mode-mismatch signage. The case is sitting in the historian's brief unspent.

**34. The Chief Engineer's ADA Title II April 2027 deadline is a forcing function the implications section ignores.**
- *Location:* Not in Section VI.
- *Issue:* The Chief Engineer brief flags ADA Title II digital accessibility compliance as a "hard deadline (extended to April 26, 2027 for larger entities)" creating a second forcing function on the refresh cycle. For MWAA, this is approximately ten months out from the draft date. A wayfinding masterplan that doesn't account for this deadline is missing a key contingency.
- *Recommendation:* Add to Section VI as a sixth observation or fold into observation Five. The 2027 deadline turns "wayfinding is overdue" into "wayfinding is timed against an external compliance forcing event" — a much sharper argument for board approval.

**35. The Architectural Historian brief is not cited even once.**
- *Location:* Not used.
- *Issue:* The run includes the architectural historian on the council (only emergency-management-consultant is excluded). The strategist references Saarinen and Pelli through the Aviation Historian and Chief Engineer briefs but never engages an architectural-historical argument about how terminal design intent interacts with wayfinding. This is a missed lens.
- *Recommendation:* Verify the brief exists in stage1 (it does) and either incorporate or explicitly state why it was set aside. Saarinen's National Hall and Pelli's DCA design intent are referenced in the draft — the architectural historian likely has more to say about design intent vs. operational reality that would strengthen the contradiction-debt argument.

**36. The Chief Engineer's distinction between AC 150/5360-12F (terminal) and AC 150/5340-18H (airfield only) is a precision the draft could use.**
- *Location:* Not used.
- *Issue:* The Chief Engineer brief specifically notes this confusion is "common in scope documents." Naming it would strengthen the strategist's credibility with the engineering reader. It is also a small but pointed indicator that the strategist has done the work.
- *Recommendation:* One footnote-style aside in Section III's "Decision Point" subsection where the federal standard is introduced.

**37. The Regulatory/Political brief's PFC cap erosion (40–50% of 2001 purchasing power) is mentioned only by the Aviation Historian and not connected to the MWAA-specific argument.**
- *Location:* Not in Section VI.
- *Issue:* The PFC cap erosion is the structural reason wayfinding doesn't get funded as capital. It is also the reason the operating-standard classification (the strategist's recommendation) is forced rather than chosen. Naming this strengthens the recommendation by showing the strategist understands the funding mechanics, not just the legal mechanics.
- *Recommendation:* Add a sentence in observation Two of Section VI: "the PFC cap, unchanged since 2001 and now at roughly half its real 2001 purchasing power, is the structural reason discretionary funding will not appear for a wayfinding capital program."

---

## G. Structural Issues

**38. Sections II (Executive Summary) and III (The Argument) have substantial content overlap and the reader gets the argument twice.**
- *Location:* Section II vs. Section III.
- *Issue:* Each of the eight Executive Summary points has a corresponding section in III. The reader processes the argument once in compressed form, then again at full length. The Levine model is to lead with a strong opening, get to the argument fast, and not summarize before delivering. An executive summary makes sense in a board memo; in a Council essay aimed at "sophisticated, skeptical peer readers... tired of [McKinsey decks]," it actively works against the tone.
- *Recommendation:* Either drop the executive summary entirely (the run prompt allows ~1,100 words for it but does not require it) or compress to one paragraph of three or four sentences. If kept, restructure as prose, not as a numbered list.

**39. Section IV (counter-case) and Section V (refutation) together run roughly the same length as Section III (the argument).**
- *Location:* Sections IV–V relative to Section III.
- *Issue:* The strategist is right to steelman; the prompt requires it. But spending equal time on the counter-case and the refutation can leave a reader who skims feeling that the case is at best 50/50. The refutation is convincing enough — but it doesn't need to be six points to the counter-case's six.
- *Recommendation:* Compress V to three or four refutations rather than five. Take the strongest counter-points and address them sharply; drop the weaker ones (the digital-investment refutation in particular is repetitive with Section III).

**40. The closing scene (post-Section VI) is the strongest writing in the draft, and it's set up by the weakest structural section.**
- *Location:* Section VI to closing.
- *Issue:* Section VI's "One, Two, Three, Four, Five" cadence sets up the closing scene by exhausting the reader on bulleted prescriptions. The closing scene then has to do extra work to recover the narrative voice the opening established.
- *Recommendation:* Reshape Section VI as prose. The five observations can become three or four sub-sections with substantive headers. This lets the closing scene land with momentum rather than recovery.

---

## Summary

The draft is in solid shape for v1. The MWAA-specific economics, the governance-as-binding-constraint argument, and the Frankfurt-as-historical-proof move are strong. But:

- **Fix the cost-ratio math** (#1, #15, #3) — this is the single most embarrassing class of error if a reader catches it.
- **Stop misrepresenting Munich** (#10) — the brief does not say what the strategist is claiming three separate times.
- **Address Zurich/Google explicitly** (#30) — this is the Contrarian's hardest punch, and the draft doesn't engage it.
- **Decking the executive summary** (#22) and the consultant-cadence of Section VI (#27) — the prompt was explicit about tone, and these sections are the most off-tone.
- **Pittsburgh chapter 2** (#33) is sitting in the historian's brief and would strengthen the contradiction-debt argument materially.

The thesis holds. The argument needs precision in the math and economy in the prose.

*— Red Team v1*
