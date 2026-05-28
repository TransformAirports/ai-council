# Red Team Critique — Strategist Draft v1
**Run:** sterile-corridor-resilience | **Stage:** 2 | **Date:** 2026-05-27

The draft is sophisticated, the architecture is right, and the load-bearing claims mostly trace to the briefs. But it cheats in specific places, sharpens numbers past what the underlying briefs support, dresses analyst constructions as cited findings, and lapses into consultant-deck rhythm in several sections that the run prompt explicitly told the Strategist not to write. Below, in priority order.

---

## A. The numbers that don't add up or are sharper than the briefs

### 1. The pulse arithmetic in II.2 and the "exactly matches" formulation
- **Location:** Executive Summary item 2; Section III "The Pulse Problem"; reprised in III "Bidirectional Flow."
- **Issue:** The Strategist writes that "the train discharge volume approximately equals the corridor's degraded capacity, with effectively zero buffer." The operations-analyst brief computes essentially the same arithmetic — but the brief flags it explicitly as "[from training-data, calculation requires field verification against measured dwell data]." The Strategist preserves "analyst calculation flagged for field verification" in II.2 but then drops the caveat in III, where the prose hardens to "the corridor's effective capacity, in the regime the train actually creates, exactly matches the load the train actually delivers." That is over-spin. The brief never says "exactly matches" — it says "precisely matches" in a flagged hypothetical. More importantly, the brief computes 200 passengers per 2-minute headway (one train per two minutes), while the draft has the train delivering "approximately 200 passengers in roughly 90 seconds of platform discharge." Where does the 90-second figure come from? Not from the operations-analyst brief, which says nothing about discharge duration — only headway and travel time. The slacker brief speculates "90-second dwell" at Find 1 in section 3 but flags it as a question for the Strategist, not an answer. The Strategist invented a sharper number than the briefs support and presented it as fact.
- **Recommendation:** Either source the 90-second discharge time to a specific reference (MWAA dwell-time documentation, AeroTrain operations data) or strip it. Reinstate the "calculation requires field verification" flag everywhere the calculation appears, not just on first use. Replace "exactly matches" with "is at or near" — the brief does not support equality.

### 2. The 280-passenger figure for the AeroTrain in III "Vertical Circulation"
- **Location:** Section III "Vertical Circulation: Where the Engineering Is Hardest," paragraph that begins "When that happens, the AeroTrain arrives with 280 passengers..."
- **Issue:** The operations-analyst brief sets train capacity at 216 passengers (72 per car × 3 cars). The COO brief uses 280. The Strategist uses 280 here but 216 elsewhere ("Three-car trains carrying up to 216 passengers by design capacity" in II.2 and III "The Pulse Problem"). Which is it? The Strategist is silently switching numbers depending on which paragraph he is writing. The COO's 280 was operator-voice memory, not engineering data; the operations-analyst's 216 is design-capacity-derived. Pick one, cite it, and reconcile.
- **Recommendation:** Standardize on 216 (the cited engineering figure) and note that operational loads vary. Or explicitly acknowledge that observed loads have run to 280 in practice (citing COO brief) and that the divergence between nameplate and observed itself supports the thesis.

### 3. "8 to 12 days per month" escalator outages — sourcing
- **Location:** Section III "Vertical Circulation," "based on MWAA maintenance data disclosed in CIP budget justifications, one of the two escalators serving the AeroTrain platform is out of service for scheduled or unscheduled maintenance on average 8 to 12 days per month. [Airport COO Brief]"
- **Issue:** The COO brief does say this. But the COO brief itself is operator-voice memory — written from the chair — and cites "MWAA maintenance data disclosed in CIP budget justifications" without naming a specific CIP year or document. The Strategist has laundered an operator's recollection into a citation that reads as if a primary document was reviewed. The brief flags itself: "Web access was unavailable during research; all sources are cited by canonical reference identifier and last-known URL. Sources should be verified by downstream fact-checking agents." The Strategist did not preserve that flag.
- **Recommendation:** Either cite the specific CIP year and section, or downgrade the framing to "MWAA operational reports indicate" with a Fact-checker flag.

### 4. The $22 billion / $3.75 billion central spine number
- **Location:** Opening thesis sentence (I), II.7 reference, V "On the political moment," and VI "On the $22 billion proposal." The most specific instance: VI's "the underground subterranean central spine reported as a $3.75 billion element should include not just additional AeroTrain capacity but expanded vertical circulation at all handoff points and parallel sterile-side pedestrian paths between concourses as DEN is now building."
- **Issue:** The regulatory-political brief sources the $22 billion figure to ffxnow.com, May 2026, characterizing it as "approximately $22 billion, including a $3.75 billion underground subterranean central spine that would expand AeroTrain connectivity and render the mobile lounges obsolete." That matches. But the Strategist's prescriptive language — that the $3.75 billion element "should include … expanded vertical circulation at all handoff points and parallel sterile-side pedestrian paths between concourses" — is the Strategist's recommendation, not a feature of the reported program. The political brief never says the $3.75 billion element is currently scoped to include corridor resilience or that it should be. The Strategist is layering his preferred scope onto the reported number in a way that a careful reader might mistake for an existing program element.
- **Recommendation:** Rewrite to make the "should include" clearly the Strategist's recommendation, not a description: "MWAA should advocate that the $3.75 billion central-spine element be scoped to include..." The current phrasing reads as if the spine is already that scope.

### 5. The "$8 to $12 million" Concourse C escalator fix
- **Location:** Section III "Vertical Circulation"; VI "On the Concourse C escalator gap."
- **Issue:** The COO brief states "The design fix — a third escalator or a second elevator bank at the Concourse C AeroTrain connection — has been estimated at $8–12 million. It has not been funded." The Strategist uses the figure twice as if it were a published estimate. The COO brief offers no source for that range, and the COO brief's own framing is operator's memory. The chief-engineer brief offers a different parametric: "$3 to $6 million per shaft pair in construction cost, exclusive of soft costs, before occupied-building premiums are applied" — though the engineer is estimating shaft widening, not a third escalator bay, so it is not the same scope. Still, the Strategist treats the $8–12M figure as authoritative without disclosing it is an operator's recollection.
- **Recommendation:** Acknowledge the estimate is from an operator's chair, flag for Fact-checker verification against MWAA capital documents, or supplement with the chief-engineer's parametric to bracket the range.

### 6. PFC purchasing power: 40% vs. 55% — pick one
- **Location:** II.7, III "The Historical Arc."
- **Issue:** The Strategist uses "roughly 40 percent of its purchasing power in real terms" in two places. The regulatory-political brief says "approximately 40 percent below its 2000 value" — consistent. But the aviation-historian brief says "the PFC buys roughly 40-45 percent of what it bought in 2001" and in its Quotable Data Points: "the purchasing power of the PFC has declined by approximately 55 percent relative to 2001 construction costs." These are different baselines (CPI vs. ENR construction index) producing different numbers, and the historian brief explicitly flags the 55% figure as "Analyst construction from primary data — flag for fact-checker verification." The Strategist picked the friendlier-to-cite figure without acknowledging the construction-cost inflation baseline that the historian brief specifically warned was more relevant for capital-program discussions. This matters: a 40% erosion against CPI versus a 55% erosion against ENR is the difference between a moderate constraint and a severe one. For a sterile corridor capital piece, the construction-cost baseline is the right one.
- **Recommendation:** Choose the ENR baseline (it is the right one for construction discussion) or present both. Acknowledge the analyst-construction caveat.

### 7. "60-65%" United enplanement share — internal inconsistency in the briefs the Strategist did not resolve
- **Location:** II.7, III "Why the Capital Decision Loses," and elsewhere.
- **Issue:** The airline-commercial-strategist brief uses "roughly 60-65%." The CEO brief uses "roughly 50-55% of seats and a substantially higher share of connecting traffic." These are different metrics (enplanements vs. seats) and the briefs disagree. The Strategist picked 60-65% and stuck with it without acknowledging the disagreement or distinguishing seat share from enplanement share. United's posture on MII review depends on enplanement share specifically (the regulatory mechanism); using a higher share than the CEO brief documented may overstate United's leverage.
- **Recommendation:** Reconcile. Cite enplanement share specifically (which is what triggers MII). If 60-65% is the correct figure, flag for Fact-checker against current MWAA / DOT T-100 data.

### 8. LaGuardia "175 percent of design capacity" — verify the framing
- **Location:** III "The Historical Arc."
- **Issue:** The operations-analyst brief says "Central Terminal B was designed in 1964 for 8 million annual passengers and was processing approximately 14 million annually... 175% of design capacity." The aviation-historian brief says "designed for roughly 8 million annual passengers. By the 2010s, LGA was handling 14-15 million." The Strategist uses "175 percent" — fine if 14M, less precise if 15M (which would be 187%). More important: the Strategist writes "Cleaning crews pulling equipment across the bidirectional corridor at LGA peak reduced effective width from roughly 16 feet to 10." That specific number does not appear in either the operations-analyst brief or the aviation-historian brief as a measured value. The aviation-historian brief says "Cleaning crews pulling equipment across the bidirectional corridor at peak reduced effective width from roughly 16 feet to 10 feet" — so it does appear there, but the brief gives no source for it. The Strategist has picked up an analyst assertion and presented it as historical fact.
- **Recommendation:** Flag the 16-to-10-feet figure for Fact-checker. Either source it to a specific PANYNJ or post-occupancy reference or reframe as illustrative.

### 9. The "70 percent staffing" TSA characterization
- **Location:** III "The Pulse Problem" (the dependent claim is implicit); VI "On the 6:45 a.m. mental model"; the framing comes from the COO brief.
- **Issue:** Less serious than the others, but the Strategist embraces the COO's "3 of 4 lanes / one officer called out / 70% staffing on a Tuesday" as scene-setting and uses it as factual texture. This is operator-voice color, not measured data. The opener is the right place for that texture; the analytical sections should not treat it as established baseline. The Strategist mostly handles this well but should re-check that he is not quietly converting evocation into evidence anywhere.

---

## B. The Contrarian and the DCA Project Journey answer

### 10. Did the Strategist actually answer DCA Project Journey, or just acknowledge it?
- **Location:** V "On path dependence and the renovation window."
- **Issue:** The Contrarian's strongest point — counter-claim #5 — is that DCA Project Journey demonstrates in-place renovation is possible, reconfigured sterile corridor geometry, replaced vertical circulation, widened circulation paths, all in an occupied operating concourse without a single day of full-concourse closure. The Strategist's response is to concede this and then say "DCA Project Journey also demonstrated what in-place renovation costs and how it constrains design." That is not a rebuttal. The Contrarian's point is not that in-place renovation is cheap or easy; the Contrarian explicitly says it is "operationally complex and expensive, but it was done." The Contrarian's claim is that the path-dependence framing is wrong: the corridors are not locked, MWAA is actively rebuilding them right now. The Strategist concedes the rebuild is possible and then redirects to cost — "3 to 5x" — and the renovation window. But the cost argument only matters if you accept the original framing that the design decisions are locked in. The Contrarian has already conceded they are not. The Strategist has not actually engaged the structural claim — that the path-dependence framing is overstated because the window is open continuously, not narrowly. Saying "the window is not closed forever. It is closed for thirty years" begs the question. Why? Because the briefs say so? No — because the Strategist asserts it.
- **Recommendation:** Either accept the path-dependence weakening (and re-frame the thesis around "the renovation window is now and the next one is far enough away to matter") or build the case for why mid-renovation cost premiums are large enough to compress the practical reopen window to once per generation. The 3-to-5x premium is from the infrastructure-economist brief; tie it to MWAA-specific bond-issuance economics rather than asserting "thirty years" as a brute fact. Concede more, then build the structural argument back up with specifics.

### 11. The checkpoint exclusion answer is rhetorical, not analytical
- **Location:** V "On the checkpoint exclusion."
- **Issue:** The Strategist concedes the Contrarian's checkpoint argument is "analytically convenient" and then argues that sterile circulation has a "specific property the other two do not: it has no operational substitute when it fails." That is a real distinction but the Strategist does not quantify it against the Contrarian's expected-throughput-gain-per-dollar comparison. The Contrarian says: "$50M deployed at checkpoints (additional lane capacity, CT scanner throughput, staffing) almost certainly exceeds the gain from wider post-checkpoint corridors." The Strategist replies that catastrophic-failure-mode resilience is in a "different category." But the Contrarian is not arguing about catastrophic failure — he is arguing about the throughput gain at the median, where most disruption hours actually live. The Strategist needs to either accept the median-vs-tail framing (and concede that the case is about tail compression, not throughput) — which he attempts in the COO-mental-model section but does not connect to the checkpoint-vs-corridor capital comparison — or provide a quantified counterargument showing that the tail-compression benefit per dollar at the corridor exceeds the median-throughput benefit per dollar at the checkpoint. He does neither. The argument is asserted, not made.
- **Recommendation:** Connect the COO's tail-distribution framing directly to the checkpoint trade-off. Specifically argue that checkpoint investment moves the median while corridor/vertical-circulation investment compresses the tail, and that these are not substitutes. If the case is "do both in different parts of the capital stack," say so explicitly.

### 12. Cleaning timing — Contrarian conceded too easily
- **Location:** V "On operations versus capital"; VI "On the operations-capital seam."
- **Issue:** The Contrarian argued: "The actual solution to that problem is a cleaning schedule that avoids peak periods — not a wider corridor." The Strategist concedes in VI: "This is a contract problem, not a capital problem." That is correct and intellectually honest. But it weakens the opening scene. The opening scene's load-bearing detail is the cleaning crew at the south end of the corridor. The Strategist uses that detail to dramatize a capital case and then later concedes it is a contract case. The scene needs to land different work, or it has been deployed in service of an argument that the Strategist himself then deflates.
- **Recommendation:** Either: (a) reframe the opening scene so the cleaning crew is one of several marginal failures that compound (which the COO's "marginal-times-five" language explicitly supports) and is not itself the capital case; or (b) acknowledge in the opening scene that some of these failures are contractual and the capital case is specifically about the binary-failure ones (escalator, vertical circulation). The current sequencing — opens on cleaning crew as the dramatic example, later concedes cleaning crew is not capital — undermines its own opener.

### 13. The "operations underspending prior question" was raised by the Contrarian and not addressed
- **Location:** Contrarian #3 closing: "The thesis should be asking why MWAA's operating budget for sterile-side corridor operations is what it is before it argues for more capital." V "On operations versus capital."
- **Issue:** The Strategist concedes "MWAA almost certainly has not optimized cleaning schedules, maintenance SLAs, incident response staffing, and AeroTrain headway management to the extent the contrarian case implicitly assumes" and then immediately pivots to "the failure mode in which the asset itself is gone." That pivot is fine for the tail-compression argument, but the Contrarian's prior question — has MWAA optimized operations first — is left answered with a shrug. For a piece pitched at MWAA leadership, this is an audience-credibility issue. The Strategist owes a paragraph on what operational optimization MWAA should be doing in parallel, and where the seam is.
- **Recommendation:** Add a paragraph in V or VI: what is the operational optimization stack that should be funded alongside capital — and explicitly state that resisting that work makes the capital case weaker, not stronger.

### 14. The Sixth Counter-Claim (empirical foundation cuts both ways)
- **Location:** Contrarian counter-claim #6; the Strategist's V response does not address it explicitly.
- **Issue:** The Contrarian's point is sharp: if the Fruin data is unreliable, the Strategist cannot cite it to support specific corridor-widening targets any more than he can cite it to defend current standards. The Strategist's V "First, on the LOS framework" addresses the framework's validity, not the Contrarian's specific point that empirical uncertainty cuts both ways. The Strategist's response is essentially "ACRP itself says the data needs updating, so we should update it" — but that is not a response to "you cannot cite unreliable data to make a recommendation." The Strategist's recommendation in VI to instrument Tier 2 East is precisely the right answer to this objection but it is not explicitly tied back to the Contrarian's #6.
- **Recommendation:** In V, explicitly engage the "cuts both ways" point. The instrumentation recommendation in VI is the answer; tie it back.

---

## C. Missed lenses and underused briefs

### 15. The Chief Engineer's column-grid argument is structurally underused
- **Location:** III "The Column Grid and the Inheritance Problem" — present but thin.
- **Issue:** The chief-engineer brief makes the column grid the single most consequential constraint on corridor width. The Strategist gives it one paragraph in III and then moves on. This should be a load-bearing section, because it is the constructability fact that makes the path-dependence argument structural rather than rhetorical. The brief offers specific physical detail — "Widening requires either relocating columns (structurally prohibitive without temporary shoring of the floors above) or cantilevering into the existing bay — which in turn eats into the MEP chase space that runs along the corridor ceiling" — that the Strategist compresses to one sentence. The chief-engineer's brief also raises moving-walkway pallet-width and exit-throat geometry as design-fixed elements that cannot be corrected operationally; the Strategist does not use this at all. The exit-throat backflow problem is exactly the kind of vivid constructability detail that would harden the argument.
- **Recommendation:** Expand the column-grid section. Add a paragraph on moving-walkway exit-throat geometry. The chief engineer is the second-most-load-bearing brief after operations-analyst; treat it accordingly.

### 16. The Airline Commercial Strategist's connect-time framing is mentioned but not deployed in the recommendations
- **Location:** III "Why the Capital Decision Loses"; V "On the political moment"; VI.
- **Issue:** The airline-commercial-strategist brief argues that MWAA's strongest negotiating posture with United is to demonstrate corridor degradation in connect-bank reliability terms — a metric United's network planning team can price. The Strategist references this twice but never operationalizes it. The VI "Implications for MWAA" is the place to make the specific recommendation: deploy Tier 2 East instrumentation to measure connect-bank reliability impact, then take the results to United's network planning team (not airline relations) with a connect-time-reduction case. That specific tactical recommendation is the natural climax of the airline brief's argument. The draft hints at it but never lands it.
- **Recommendation:** In VI, add a specific tactical recommendation about how MWAA presents the corridor case to United — to which United team, with what metric, on what timeline. Tie this to the Tier 2 East instrumentation recommendation. The airline brief is doing more work than the draft credits it for.

### 17. The Aviation Historian's "three structural breaks" frame is the second-best section of the draft and could anchor more
- **Location:** III "The Historical Arc: Three Times Before."
- **Issue:** This is actually well-used. But the historian's specific framing — "This debate has occurred three times in the last 50 years, each time triggered by a structural break" — is buried inside an argument section rather than used as a structural device for the whole piece. Consider whether opening Movement III with the historian frame (rather than starting with Pulse Problem) might give the piece more momentum. The historian's third break — post-pandemic recovery + aging vertical circulation + capital constraint — is essentially the Strategist's whole thesis condensed. Letting the historian carry the opening of the analytical movement might give it more force.
- **Recommendation:** Consider re-ordering III to lead with the historical arc. The PuIse Problem becomes the present-day expression of the third structural break. This may or may not work — depends on whether the Strategist wants the analytical force up front or the historical inevitability — but it is worth a draft.

### 18. The slacker brief's Hillsborough/Taylor framing is present but underplayed
- **Location:** III "The Pulse Problem" (Taylor Report referenced).
- **Issue:** The slacker brief offered the Hillsborough framing as load-bearing: "Airports have not had their Hillsborough. The question buried in this thesis is: does MWAA want to have it proactively, or reactively?" The Strategist uses the Green Guide stat (82 persons per meter per minute) and the Taylor Report reference but does not let the framing land. The "stadium concourse problem wearing an airport coat" formulation is the Strategist's own (good) phrase but the surrounding paragraph treats it almost as a parenthetical. The slacker is offering a rhetorical hammer the Strategist barely picks up.
- **Recommendation:** Either commit to the Hillsborough framing as a structural argument (which would require sharper rhetoric about consequence asymmetry) or drop the Taylor Report reference entirely. Half-using it is the worst of both worlds.

### 19. Virtual Christian's "what happens when AeroTrain goes down for four hours" is missing
- **Location:** Should appear in Section V or VI but does not.
- **Issue:** The virtual-christian brief raises a specific scenario — AeroTrain down for four hours, not four minutes — and argues "the real resilience question at IAD is not 'can the corridors handle peak flow' but 'what does the system look like when AeroTrain is not running and we need to move 8,000 passengers across the airfield by bus and still maintain sterile integrity.'" This scenario is the strongest version of the resilience argument and the Strategist does not address it. It connects directly to the DEN $300-700M parallel: building sterile-side pedestrian alternatives to APMs. The Strategist mentions DEN repeatedly but does not connect the dots to the IAD-specific "what happens at hour four" scenario.
- **Recommendation:** Add a paragraph in V (probably under "On operations versus capital") explicitly addressing the four-hour AeroTrain failure scenario and the bus-as-substitute math. This is where the DEN parallel becomes most pointed for IAD.

### 20. The international-to-international flow is added at the end of VI without setup
- **Location:** VI "On the international-to-international flow."
- **Issue:** This is the virtual-christian's "one thing the Strategist should not miss." The Strategist does include it — credit for that — but as the seventh bullet in VI, with no prior setup in the analytical sections. The argument is genuinely important (the corridor optimized for the 7 a.m. domestic bank may be wrong for the noon international connection complex) but appears without warning. The reader has not been prepared to evaluate it.
- **Recommendation:** Either thread the international flow concern through Section III (probably under Pulse Problem or Column Grid) or remove it from VI. As written, it appears as an afterthought when the brief flagged it as primary.

---

## D. Prose, rhythm, structure

### 21. Section III "The Pulse Problem" opens with a definitional sentence
- **Location:** III "The Pulse Problem," first sentence: "The single most consequential thing about an automated people mover at a midfield airport is that it does not deliver a flow. It delivers a pulse."
- **Issue:** This is a consultant-deck opener — superlative claim, then definitional reveal. The McPhee/Lewis/Gawande tradition the run prompt invokes opens with a specific scene or concrete detail. The Strategist's actual opener (Section I) does this well. Section III throws away that earned rhythm and reverts to "the single most consequential thing about X" — which is exactly the language the tone rules forbid. The reader has just absorbed a beautifully-rendered scene in Section I and is now reading a McKinsey thesis statement.
- **Recommendation:** Rewrite the opener of III as a scene — the AeroTrain platform at the moment of arrival, the bunching at the escalator, the next train two minutes out. The pulse argument should land through observation, not assertion.

### 22. "As the X brief notes" / "the X Brief argues" patterning
- **Location:** Throughout, but conspicuous in V and VI.
- **Issue:** The brief-citation pattern — "[Operations Analyst Brief]," "[Airport COO Brief]" — appears in the prose constantly. This is appropriate for traceability inside the Council process but reads as memo-citation when transposed into long-form narrative. McPhee never says "according to the geologist I interviewed." He names the geologist, sketches the conversation, and quotes the sentence. The Strategist should be doing more of this — naming the disciplines and letting their arguments come through as voices rather than as bracketed citations. The current pattern reads as defensive: "this is what the brief said, please do not blame me." A confident long-form writer would absorb the citation into the prose ("the operations analyst found that…" or simply "the empirical record shows…") and reserve brackets for surprising or contested claims.
- **Recommendation:** Audit every bracketed citation. Keep them on the load-bearing empirical claims (the PLOS One 25%, the ACRP Problem Statement, the 49 CFR sections). Remove them from the connective tissue where they are not doing work.

### 23. Executive Summary item lengths are uniform — the rhythm flattens
- **Location:** II.
- **Issue:** Each of the eight items is roughly the same length (4-7 lines), built on the same syntactic frame (bold lead claim, supporting evidence sentence, supporting evidence sentence, citation). This is the LinkedIn-thought-leadership rhythm. A McPhee equivalent would vary item length dramatically — some items two sentences, others a small paragraph. The current rhythm signals "consultant memo" to the reader and the run prompt explicitly excludes that signal.
- **Recommendation:** Cut at least two of the executive-summary items to two sentences. Let one expand to a short paragraph that lingers on the specific MWAA implication. The variability matters.

### 24. Section V structure: "Five specific grounds" / "First, on… Second, on… Third, on…"
- **Location:** V opening.
- **Issue:** The "let me concede and rebut in numbered order" structure is the structure of an MBA case-memo response. It is also the safest structure, which is why everyone in consulting writes it. The run prompt asked for Matt-Levine-on-aviation. Levine never writes "Five specific grounds. First. Second. Third." He writes through the objections in the order they cause him the most trouble, gives the hardest ones more space, dismisses the weak ones in a clause. The current Section V gives every counter-argument exactly equal weight and exactly equal treatment, which signals to the reader that the writer has not actually weighed them.
- **Recommendation:** Restructure V so that the hardest objection (probably DCA Project Journey + path dependence) gets the most space and the weakest (probably checkpoint exclusion, which is genuinely a scope issue) gets dispatched quickly. Let some objections leave a mark; let others be cleanly answered. The current "each gets a numbered paragraph" structure flattens the analysis.

### 25. Section VI is a memo
- **Location:** VI "Implications for MWAA."
- **Issue:** "On the Tier 2 East opening. On the Concourse C escalator gap. On the use-and-lease window. On the $22 billion proposal. On the federal funding stack. On the international-to-international flow. On the operations-capital seam. On the 6:45 a.m. mental model." This is the structure of a board-action-memo. It is not the structure of long-form narrative. The COO-brief's framing (the 6:45 a.m. mental model) is sufficient to carry a full closing section as narrative — the operator at the chair, the calls he is making, the capital decisions he wishes someone had made in 1997. The Strategist has the material to write that section. Instead he has written a series of "On X" subheads strung together by recommendations.
- **Recommendation:** Rewrite VI as a single sustained narrative — probably anchored to the 6:45 a.m. scene from the opener — that incorporates the specific recommendations as they arise. Eight bullet subheads is a board memo; one rendered argument with embedded specifics is the McPhee model. This is the section that most needs the prose rewrite.

### 26. The closing
- **Location:** Final two paragraphs.
- **Issue:** "A corridor is a piece of floor between two ceilings. It is the cheapest element to draw and the most expensive to fix." This is good — earned, specific, with a useful structural metaphor. Then: "At 6:45 a.m. on a Tuesday in February, with one escalator running rough and a cleaning crew fifteen minutes past their window, the corridor at Concourse C will clear or it will not. The question for MWAA is not whether to know in advance. The question is whether to measure." The last sentence is a kicker, which is fine, but "whether to know in advance" is a slightly awkward construction. And the close as a whole returns to the opener cleanly but does not quite land the "what now" the piece has been building toward.
- **Recommendation:** Tighten the last sentence. Consider whether the close should name the specific decision the Tier 2 East opening forces (instrument or don't, before September 2026) rather than the more abstract "whether to measure." The piece has earned a sharper, more specific kicker.

---

## E. Cherry-picked from briefs / counter-evidence ignored

### 27. The Contrarian's "200 hours per year" speculation
- **Location:** Contrarian #2 made an explicit empirical claim the Strategist did not engage: "If [the number of hours per year corridors operate above LOS D] is, say, 200 hours per year (less than 2.5% of operating hours), the capital case for widening is substantially weaker."
- **Issue:** The Strategist's V "On the cost-benefit arithmetic" addresses the lifecycle math but never engages the specific empirical question the Contrarian raised: how many hours per year does the IAD corridor operate above LOS D? The Strategist's instrumentation recommendation in VI is the right answer to this question (we should measure it), but the Strategist does not explicitly say "the Contrarian's 200-hour speculation could be true, could be false, we don't know, and the absence of measurement is itself the problem." That is the honest version. The Strategist instead pivots to lifecycle math, which is a different argument.
- **Recommendation:** Address the 200-hour speculation directly. Connect it to the instrumentation recommendation. The honest answer is: we don't know, we should, and the cost of measuring is tiny relative to the cost of being wrong in either direction.

### 28. The operations-analyst brief's ORD T2 counterexample was ignored
- **Location:** The operations-analyst brief offered a useful counter-example: "O'Hare Terminal 2's underground pedestrian tunnel network connecting T1, T2, and T3 represents a case where adequate horizontal circulation capacity exists but the routing (below grade, through parking infrastructure, with non-intuitive wayfinding) degrades its operational utility. This is a counterexample to infrastructure determinism: you can build adequate physical capacity and still generate bottleneck behavior through poor configuration."
- **Issue:** This is the operations-analyst voluntarily flagging the limits of the infrastructure-determinism argument. The Strategist ignored it entirely. This is cherry-picking — the Strategist used the brief's pro-thesis findings and skipped the within-brief counter-evidence.
- **Recommendation:** Add a sentence in IV or V acknowledging the ORD T2 counterexample. The honest version: width alone does not solve corridor problems if routing and wayfinding fail. This actually strengthens the thesis (the framework must include both dimensional and configurational variables) but the Strategist has to do the work.

### 29. The infrastructure-economist brief's BER cautionary tale was used selectively
- **Location:** The infrastructure-economist brief uses Berlin Brandenburg as the cautionary tale for commissioning cost escalation. The chief-engineer brief uses it similarly.
- **Issue:** Neither use the Strategist preserved. The BER lesson — that infrastructure that must be proved compliant before passengers can flow through it is subject to commissioning-cost escalation — is directly relevant to the in-place sterile renovation argument. The Strategist drops it entirely. The Strategist also drops the JFK Terminal 1 cost-comparison ($800M partial remediation vs. $9B+ greenfield replacement) from the chief-engineer brief, which is a precedent for the cost trajectory at LGA-style end-state cases.
- **Recommendation:** In V "On the cost-benefit arithmetic," add the BER commissioning-cost dynamic as the European analog to the in-place renovation cost premium. The JFK T1 figure should appear at least once as another data point for the "deferred enough, you face the full replacement decision" trajectory.

### 30. The operations-analyst's "induced demand at bottlenecks" finding
- **Location:** Operations-analyst brief: "A 2019 experimental study in Physica A found that crowd density near corridor bottlenecks increases with corridor width upstream of the bottleneck — a counterintuitive result that matters for AeroTrain station design: wider approach corridors can funnel higher-density crowds into bottleneck transitions."
- **Issue:** This is a counterintuitive finding that complicates the "wider is better" implicit argument. The Strategist does not engage with it. It cuts against parts of his thesis (wider may not always be better) but supports other parts (the bottleneck — vertical circulation — is the critical sizing decision, not just corridor width). Either way, it is in the brief and the Strategist did not address it.
- **Recommendation:** Engage. This finding actually supports the Strategist's emphasis on vertical circulation as the critical chokepoint — the upstream corridor matters less than the vertical handoff. Use the finding to sharpen the vertical-circulation focus.

---

## F. Invented or analyst-constructed numbers presented as cited

### 31. "approximately 1 a.m. to 3:30 a.m. — roughly 2.5 hours per night"
- **Location:** III "The Column Grid"; II.6.
- **Issue:** This figure comes from the chief-engineer brief and is presented there as practitioner observation: "the effective construction window at AeroTrain station locations is approximately 1 a.m. to 3:30 a.m. — roughly 2.5 hours per night." The brief does not source it. The Strategist preserves the number but not the "practitioner observation" caveat.
- **Recommendation:** Preserve the practitioner-observation caveat. The number is plausible and useful as illustration, but the brief explicitly says it is not citable.

### 32. "35 to 45 percent of greenfield construction productivity"
- **Location:** II.6, III "The Column Grid."
- **Issue:** Chief-engineer brief explicitly flags this: "Source: practitioner observation, not a citable public source." The brief also explicitly says: "Strategist should not present this as a published figure, but it is the right order of magnitude." The Strategist presents it as fact in II.6 and in III, including the bracketed citation "[Chief Engineer Brief]" which makes it look more authoritative than it is.
- **Recommendation:** Either preserve the "practitioner observation" caveat or paraphrase to "industry estimates put the productivity gap in the range of half to two-thirds." The current presentation imports a flagged-uncitable figure as if it were a TRB published finding.

### 33. "$5 to $20 million per intervention" for right-sizing at construction
- **Location:** V "On the cost-benefit arithmetic."
- **Issue:** Infrastructure-economist brief: "the marginal cost of adding, for example, one additional escalator bank at each AeroTrain station concourse handoff, or widening a critical sterile connector segment by 20%, is likely in the range of $5–$20 million per intervention." Brief flags caveats throughout. The Strategist uses the figure cleanly.
- **Recommendation:** Acceptable but note this is analyst construction, not a published estimate.

### 34. "3 to 5x cost premium"
- **Location:** III "Vertical Circulation"; V "On the cost-benefit arithmetic."
- **Issue:** Infrastructure-economist brief: "this multiplier is derived from contractor cost indexes and pattern evidence from analogous projects... must be treated as an informed estimate, not a verified figure." The Strategist treats it as established. Note this conflicts with the Contrarian's citation of ACRP Report 25's "1.5-2.5 times the equivalent greenfield" figure. The Strategist uses both numbers without acknowledging the conflict.
- **Recommendation:** Reconcile. Either the multiplier is 1.5-2.5x (ACRP-published) or 3-5x (industry estimate). The Strategist cannot use both without explanation. Probably the right answer is: ACRP's 1.5-2.5x is for in-place renovation generally; the 3-5x is for mid-life vertical circulation replacement at sterile-side handoffs specifically. If so, say that.

### 35. "MEP coordination premiums of 30 to 40 percent"
- **Location:** V "On path dependence and the renovation window."
- **Issue:** Chief-engineer brief: "MEP coordination... added 30 to 40% to the MEP contractor's scope and schedule relative to greenfield." Properly cited; the Strategist preserves it. Acceptable.

### 36. "the IATA Baggage Report 2023" figures on carry-on counts
- **Location:** III "The 1970s Dataset That ACRP Has Disavowed."
- **Issue:** Contrarian brief cited this: "IATA's 2023 Baggage Report documents that carry-on rates have increased substantially over the past decade, with passengers on North American routes averaging 1.3 carry-on items per person in 2022 versus estimates of 0.7-0.8 in earlier periods." The Strategist preserves the citation. Fact-checker should verify the IATA Baggage Report 2023 exists and contains these specific numbers — the Contrarian's citation is somewhat informal.
- **Recommendation:** Flag for Fact-checker. If the IATA Baggage Report 2023 does not contain those exact numbers, the Strategist needs a different empirical anchor.

---

## G. Structural issues

### 37. Six movements is one too many
- **Location:** Overall structure.
- **Issue:** The piece has six movements (or seven, counting the closing): Cleaning Crew opener; Executive Summary; The Argument (which is itself seven sub-sections); Counter-Case; Why Counter-Case Insufficient; Implications for MWAA; closing. The Argument section alone is 4,500+ words across seven subsections. This is too many sections for a 9,800-word piece that the run prompt explicitly compared to Matt Levine. Levine writes in numbered chunks within a single sustained argument. The current structure asks the reader to track too many transitions.
- **Recommendation:** Consider collapsing The Argument from seven subsections to four or five. The "Industry Designs to a Model It Has Never Validated" and "The Denver Confession" sections could merge (both are about the simulation/measurement gap producing capital consequences). The "Lifecycle Accountability Gap" could fold into "Why the Capital Decision Loses Every Internal Competition" since they are arguing the same thing from different lenses.

### 38. The Executive Summary is too long for what it does
- **Location:** II. Eight items, each 4-7 lines.
- **Issue:** ~1,100 words is the target from the run prompt. The current eight-item structure consumes that budget without leaving room for the kind of single-paragraph synthesis a Matt-Levine reader would expect (the "here is the punch line" paragraph that the eight items would then unpack). The eight items are also internally redundant in places — item 4 (no post-occupancy validation) and item 8 (inflection point timing) could compress to one item each rather than two.
- **Recommendation:** Either cut to 5-6 items or add a one-paragraph synthesis at the top of II that compresses the whole argument to four sentences. The current structure is all unpacking and no synthesis.

### 39. The thesis sentence is too long
- **Location:** I, the three-sentence thesis: "Sterile corridor design at major US hub airports is governed by code minimums and a fifty-year-old pedestrian flow framework that was never built for what these corridors are now asked to do — absorb pulsed APM discharges into bidirectional flow paths whose single-point vertical circulation is at the end of its first service life."
- **Issue:** That sentence is 49 words. It is doing a lot of work. It is also the kind of sentence the run prompt explicitly warned against ("intellectually honest about the counter-argument. Slightly provocative but not polemical"). The current sentence is provocative but also vague at the load-bearing points: "code minimums" is fine, "fifty-year-old pedestrian flow framework" is fine, but "single-point vertical circulation" front-loads a specific technical claim that the reader has not yet been prepared for. The thesis should land more cleanly.
- **Recommendation:** Break it into two sentences. Put the technical detail (vertical circulation, single-point failure) in the second sentence so the first sentence carries the framing claim cleanly.

### 40. The "Implications for MWAA" section opens redundantly
- **Location:** VI first paragraph: "The Tier 2 program is in active construction. The Tier 2 East concourse opens September 2026 with no publicly documented corridor-level sensing deployment and no published post-occupancy validation plan. The $22 billion IAD revitalization concept is under DOT review with no confirmed funding mechanism. The midfield escalators installed between 1997 and 2004 are at or past their practical service life."
- **Issue:** All four sentences have already appeared in the executive summary and in III. This is the stacked-summary opening that the system-prompt critique-rules specifically flagged. The reader has just read these facts. Restating them as a four-sentence opener is consultant-deck rhythm.
- **Recommendation:** Open VI with a specific decision MWAA is making in the next eighteen months and the consequence of getting it wrong. Drop the restated facts.

---

## H. Things the draft gets right (so the Strategist does not over-correct)

- The opening scene is genuinely good. The detail of "fifteen minutes past their scheduled clearance, because somebody spilled coffee at 5:15 and the second pass took longer than the contract assumes" is the kind of specific that the run prompt asked for.
- The ACRP Problem Statement 24-1058 quotation is accurately rendered against the regulatory-political brief.
- The bidirectional 25% finding is accurately attributed to the PLOS One 2018 paper and the Strategist did not over-spin the magnitude.
- The DEN $300-700M framing is faithful to both the operations-analyst and technology-scout briefs.
- The Counter-Case section (IV) is genuinely strong — the run prompt asked for the counter-case to feel its full force and it does. Do not weaken IV in revision.
- The decision to treat the COO's "tail compression" framing as the load-bearing capital argument is correct and well-executed (in V at least). The work in VI to make it operational needs to come through.
- The historian's "three structural breaks" frame is intact and well-used.

---

## Priority for v2

If the Strategist addresses only five items, the priorities are:

1. **Item 10** — actually answer the DCA Project Journey path-dependence argument, not just acknowledge it.
2. **Item 25** — rewrite VI as narrative, not memo.
3. **Item 15** — expand the column-grid / chief-engineer section to load-bearing weight.
4. **Items 1 and 2** — fix the pulse arithmetic over-spin and reconcile the 216/280 passenger conflict.
5. **Item 11** — answer the checkpoint trade-off in expected-throughput-gain-per-dollar terms, not in rhetorical "different category" terms.

Everything else is improvement work; these five are correctness work.

---

*Critique v1 — submitted to the Strategist for v2. Saved at `/Users/cgkiv/Documents/GitHub/ai-council/outputs/stage2/red-team-critique-v1.md`.*
