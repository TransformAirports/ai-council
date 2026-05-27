# Red Team Critique v1
## Attack on Strategist Draft v1 — "The Architecture of Silence"

**Date:** 2026-05-21
**Critique target:** `outputs/stage2/strategist-draft-v1.md`
**Posture:** Adversarial. The draft is good in places, structurally over-engineered in others, and contains at least three importations from outside the brief base that must be either sourced or removed.

The thesis is salvageable. The execution is not yet long-form essay; it is consultant-memo with literary flourish bolted on the edges. Specific items below.

---

## A. Unsupported / invented claims

**1. The Kansas City International "success case" is not in any Stage 1 brief.**
- **Location:** "What the Successful Cases Share" (paragraph 3); also referenced in Executive Summary #7.
- **Issue:** The draft asserts, with specificity, that KCI's new terminal "built its budget from gate count and functional requirements rather than from drawings; airline sign-off on functional requirements before design began; early contractor involvement; and a hard external deadline tied to the 2023 NFL Draft." None of these four claims appear in any of the twelve Stage 1 briefs. KCI is not discussed by infrastructure-economist, operations-analyst, technology-scout, chief-engineer, airline-commercial-strategist, regulatory-political-analyst, aviation-historian, airport-ceo, airport-coo, contrarian, slacker, or virtual-christian. This is a load-bearing third case in the successful-counter-case argument and it has been imported from the Strategist's general knowledge.
- **Recommendation:** Either drop KCI and rely on Istanbul + Changi T4 as the success duo, or commission a specific source (and run it past fact-checker before final). As written, this paragraph will fail Stage 4 verification.

**2. "Year 1 demand realization averaging 70% of forecast" is invented.**
- **Location:** Implications section, recommendation 7 ("Reference-class forecasting against the actual base rate").
- **Issue:** The 80% cost-overrun figure traces to Flyvbjerg via chief-engineer and infrastructure-economist briefs. The "schedule slips averaging 25%" and "Year 1 demand realization averaging 70%" figures do not. Operations-analyst gives the closest comparable: rail passenger traffic averages 51.4% below forecast — which is not 70% realization, it is closer to 49% realization. The number was constructed.
- **Recommendation:** Either replace with the actual Flyvbjerg figure (51% shortfall for the worst-forecasting categories) with the rail caveat, or strike the specific percentages and rephrase as "substantially below the feasibility study forecasts the briefs document."

**3. "Schedule slips averaging 25%" is unsupported.**
- **Location:** Implications, recommendation 7.
- **Issue:** No Stage 1 brief cites this number. Infrastructure-economist gives the 86% overrun / 28% mean from Flyvbjerg's transport database — that is cost, not schedule. Aviation-historian gives 34–45% for fixed-link transport cost overruns. Neither is "25% schedule slip."
- **Recommendation:** Source or remove.

**4. "OECD and the World Bank for how to make construction work" — World Bank citation is invented.**
- **Location:** "Six Months Was What Was Agreed," paragraph 1.
- **Issue:** Regulatory-political brief cites "OECD IOC Toolkit case study on Heathrow T5." No Stage 1 brief mentions the World Bank citing T5. The Strategist appears to have pluralized OECD into "OECD and the World Bank" for rhetorical weight.
- **Recommendation:** Cut "and the World Bank." If the goal is institutional weight, OECD alone is sufficient.

**5. NPIAS framing contradicts the underlying brief.**
- **Location:** Executive Summary #4.
- **Issue:** Draft asserts: "NPIAS-identified investment needs rose from $43.5 billion … to $62.4 billion … a 43% increase **without a single additional gate scoped**, driven by construction inflation…" Infrastructure-economist brief is explicit that the increase was "driven by **both** construction cost inflation **and expanded project scope**." The Strategist removed half the causal explanation to make the inflation point sharper. This is cherry-picking against the source.
- **Recommendation:** Rewrite to match the brief: "driven by construction inflation **and expanded project scope**." Or, if you want the cleaner version, attribute it to the inflation portion only and disclose that scope also expanded.

**6. "Denver's 16-month delay generated $360 million in operating deficits" mis-categorizes the $360M figure.**
- **Location:** Executive Summary #3.
- **Issue:** Chief-engineer brief decomposes the $360M as: $230M operating deficits, $37M lost income, $86M alternative baggage system, $8M additional bond issuance. The full $360M is total delay cost, not operating deficits alone. The Strategist conflates the two. The Munich Warning section gets this right ("$33 million per month and $360 million cumulative"), but the executive summary is wrong.
- **Recommendation:** "$360 million in cumulative delay costs" or "$230 million in operating deficits within a $360 million total delay cost."

**7. Munich engineers "sat down to write a letter" — the letter is the Strategist's literary invention.**
- **Location:** Opening paragraph.
- **Issue:** Tech-scout brief documents that "Munich airport confirmed the project 'was set up to fail'" and that Munich "sent a similar warning based on direct operational experience" (contrarian). None of the briefs describe the medium as a letter. The opening narrative ("engineers at Munich Airport sat down to write a letter… The Munich engineers' letter, in essence, said: this is set up to fail") is dramatized.
- **Recommendation:** This is the opener of the essay and the scene that anchors the title metaphor. Either find a primary source that establishes "letter" as the form (a real document, not a brief paraphrase), or rewrite the scene around what the briefs actually describe — a formal written warning, a consultation, or a documented communication. Do not let the scene rest on a fabricated medium.

**8. "Istanbul opened on October 29, 2018" — date too specific to be in any brief.**
- **Location:** "What the Successful Cases Share."
- **Issue:** Operations-analyst, tech-scout, and chief-engineer all say "October 2018." None give October 29. The date is correct (it was the 95th anniversary of the Turkish Republic) but the Strategist sourced it from outside the brief base.
- **Recommendation:** Either soften to "October 2018" or cite an explicit source. Fact-checker will catch this.

---

## B. Cherry-picked evidence

**9. The T5 recovery story is too clean.**
- **Location:** "Six Months Was What Was Agreed," final two paragraphs.
- **Issue:** The Strategist concedes T5 recovered but frames recovery as "not absolution" because two executives were fired and brand damage persisted. Contrarian brief is stronger: by February 2009 (under eleven months), BA's mishandling rate at T5 was five bags in 1,000 — the brief notes T5 is "now widely regarded as one of Heathrow's best-performing terminals." The Strategist quietly drops the contrarian's structural point that T5 was a *recoverable* failure of a different category than BER. The counter-case section concedes this later, but the T5 narrative paragraph itself is selectively pessimistic to keep T5 inside the "failure" set.
- **Recommendation:** Tighten the T5 section to acknowledge recovery time explicitly (eleven months, not "eventually") before the executive-firing penalty is invoked. The honest reading: T5 is the case where the recovery proves the failure was operational not structural. That distinction needs to live in the T5 section, not be deferred to the counter-case.

**10. BER fire-system-as-"thermodynamically incoherent" overstates the design verdict.**
- **Location:** Executive Summary #2; Berlin's Draughtsman section.
- **Issue:** Multiple briefs (chief-engineer, regulatory-political, tech-scout) describe the smoke-extraction design as "physically possible but requires exceptional engineering rigor" or "a unique undertaking … not worked as planned." The chief-engineer brief explicitly notes "This is physically possible but requires exceptional engineering rigor." The Strategist's "thermodynamically incoherent before a single duct was installed" overstates the physics — it was buildable in principle and failed in practice, not impossible by physics. This matters because the Strategist's framing makes the failure look stupid; the reality is subtler and indicts the governance more, not less.
- **Recommendation:** Replace "thermodynamically incoherent" with the brief's actual framing — "required reversing the natural buoyancy of heated air at a scale that had never been demonstrated." That language is in the brief, it is more accurate, and it is more damning of the supervisory board.

**11. The Aerotrain framing in the Implications section silently drops the COO brief's caveat.**
- **Location:** Implications, paragraph 2.
- **Issue:** The Strategist frames Aerotrain as "scope-and-design failure mode that LGA Terminal B exhibited in a different form." Infrastructure-economist brief notes the four-month delay was for reliability testing — testing actually held the line. That is a competing read: Aerotrain may have been a case of *appropriate* ORAT discipline (delayed opening to complete testing) rather than scope failure. The Strategist picks the worst available reading without engaging the alternative.
- **Recommendation:** Either acknowledge the reliability-testing framing or argue against it. As written, the Aerotrain paragraph reads as if the case has been settled when the briefs are agnostic.

**12. The BER passenger comparison hides what year it's measuring.**
- **Location:** Executive Summary #1 says "BER's pre-construction projection of 34 million passengers against a Year 1 actual of 9 million."
- **Issue:** The 9M figure in airline-commercial-strategist is for 2020 (partial year, opened in November, mid-pandemic). The full first-year 2021 figure is 9.95M. The Strategist picks the lower partial-year number while calling it "Year 1." Operations-analyst is explicit that 2020 was "deeply distorted by COVID-19" and notes the 700,000 figure for the first 100 days. The Strategist quietly uses the pandemic-distorted figure to maximize the failure ratio.
- **Recommendation:** Pick one consistently and disclose. Honest version: "BER's first full year of operations (2021) saw 9.95 million passengers against a 34-million design calibration — and 2020 was worse, distorted by the pandemic the airport had no resilience to absorb." That is in the Berlin's Draughtsman section already. Make the executive summary match.

---

## C. Logical gaps

**13. The thesis silently mutates between Executive Summary and Counter-Case.**
- **Location:** Whole essay.
- **Issue:** Executive Summary asserts "four leading indicators recur" and treats them as diagnostic. The Counter-Case section then concedes the Contrarian's point that the four signals appear in ~91.5% of all megaprojects and so are *not* diagnostic. The reformulation ("the signals are universal; what predicts outcome is institutional standing to act on them") is sound, but the Executive Summary is still pitched as if the four signals were the framework. A reader reading top-to-bottom encounters two different theses.
- **Recommendation:** Rewrite the Executive Summary after the Counter-Case is resolved. The executive summary should lead with the sharper formulation (institutional standing) and treat the four signals as the screening test, not the predictor. As written, the essay argues its own thesis into a different shape and leaves the front matter intact.

**14. "We will know in eight months" — what is the inference rule?**
- **Location:** Phasing, P3s, and the New Failure Mode section, closing line.
- **Issue:** This is a rhetorical flourish that promises a falsification window without specifying what would falsify the thesis. If JFK NTO opens in November 2026 with no operational incident, does that disconfirm the thesis? If it slips again, does that confirm it? The Strategist has not committed to a test.
- **Recommendation:** Either commit to the test (e.g., "If NTO opens in November with baggage mishandling below the T5 day-one rate and CBP processing within design tolerance, the institutional check held. If not, the case proves") or strike the line. The cleverness is unearned without it.

**15. The Implications section assumes MWAA without arguing for it.**
- **Location:** Implications.
- **Issue:** The run prompt asks for a piece that applies "to a forthcoming massive capital project." The Strategist names MWAA-Dulles specifically and pivots into seven prescriptive recommendations. The pivot is unearned — the essay never argues that Dulles is the analogous case rather than, say, O'Hare's $11.5B program or DFW Terminal F. O'Hare in particular is conspicuously absent from the body of the essay despite being the largest active US program at the time of writing.
- **Recommendation:** Either argue for why Dulles is the canonical applied case (likely the right move given the audience), or broaden the prescription to apply across the wave. As written, the leap from BER/T5/Denver to MWAA is rhetorically efficient but logically loose.

**16. The "designated pessimist" recommendation is asserted, not justified.**
- **Location:** Implications, recommendation 5.
- **Issue:** The Strategist proposes a "named executive, insulated from the political opening-date commitment, whose performance review depends on surfacing what will break before opening." None of the success cases (Istanbul, Changi T4, KCI) are documented in the briefs as having such a role. This is the Strategist's invention. It may be a good idea, but it is presented as if the success cases prove it.
- **Recommendation:** Frame as the Strategist's synthesis, not as a pattern lifted from successful cases. Or find evidence that Istanbul, Changi, or Kansas City actually had a designated pessimist by another name. Without that, the recommendation is opinion in the dress of evidence.

---

## D. Weak rhetoric and flat prose

**17. The Executive Summary is too long and pre-empts the essay.**
- **Location:** Lines 22–38.
- **Issue:** Eight numbered points totaling roughly 800 words. The run prompt specifies a ~1,100-word executive summary, so the length is in band, but the Executive Summary in its current form effectively delivers the entire argument before the essay begins. A reader who reads the summary has no incentive to read the essay. McPhee, Lewis, Kidder do not write this way. They open with a scene and let the argument accumulate.
- **Recommendation:** Cut the Executive Summary to four sharper points OR convert it into a 3-paragraph prose preface rather than a numbered list. Right now it reads as a deck.

**18. Consultant-style definitional subsection openers.**
- **Location:** Multiple section headers.
- **Issue:** "Berlin Brandenburg Airport is the complete specimen." "Denver's Great Hall is the case where the contracting structure itself produced the institutional gap." "Istanbul opened on October 29, 2018." These are all variations of a board-deck opener — definitional, declarative, identical in rhythm. None of them lands a reader inside a scene. Compare to the Munich Warning opener, which actually works because it puts the reader in a room with engineers writing a letter.
- **Recommendation:** Open at least three subsections with a scene, a specific moment, or a sentence that does not start with the case name. Examples that would land harder: "Klaus Wowereit acknowledged in 2015 that no one on the supervisory board had been selected for construction competency. He was the supervisory board chairman." Or: "On the morning the Great Hall contract was terminated, the contractor's projected overrun had grown to $311 million." The case-name opener is a tell that the section was structured before it was written.

**19. "This is the architecture of silence" is good. Most of the other metaphors are not.**
- **Location:** Various.
- **Issue:** "The Munich Warning, and What It Tells Us About Visibility" — academic title. "When the Design Is the Failure" — accurate but flat. "Six Months Was What Was Agreed" — good (it's Booker's line, doing work). "Berlin's Draughtsman" — good. Subsection titles are inconsistent in voice. Half of them sound like a McKinsey deck section header ("Why the Counter-Case Is Insufficient," "What the Successful Cases Share"), and the other half sound like an essay.
- **Recommendation:** Either commit to essay-style titles (concrete, particular, scene-anchored) across all subsections, or commit to deck-style (declarative, framework-naming) across all. The hybrid is worse than either.

**20. Banned-word check: "leverage" appears twice.**
- **Location:** "Phasing, P3s..." paragraph 3 (LAX grand jury quote uses "leveraged" — acceptable as a direct quote) and Berlin's Draughtsman ("the credit structure embeds material demand risk… debt service coverage compresses with no public buffer").
- **Issue:** "Leverage" used twice. Once in a direct quote (defensible). Once it's near-miss. Also check for: "many," "often," "increasingly." Quick scan turns up: "many post-mortems describe" (early); "many programs"; "most have only program management firms." "Most" used as filler several places where a specific number would land.
- **Recommendation:** Run a pass replacing "many," "most," "often" with either specific numbers from the briefs or stronger active phrasing. The briefs have the numbers.

**21. "The architecture of silence" is named but never delivered as scene.**
- **Location:** Title, opening, and throughout.
- **Issue:** The phrase appears in the title and is invoked at three points. It is asserted as a concept ("the systematic suppression of bad news by an organizational structure that rewards optimism at every reporting layer") but never staged. A McPhee piece would put us inside one of those reporting layers — at a specific BER staff meeting, at a specific Denver project review, at a specific BAA-BA handoff meeting. We get the abstraction; we don't get the scene.
- **Recommendation:** Find one scene in the brief evidence that physically depicts a signal being received and softened. Schwarz's January 2013 firing is one candidate (he reported 90% completion against 56% actual). Stage it. That is the scene the title promises.

**22. Stacked summary paragraphs.**
- **Location:** "Why the Counter-Case Is Insufficient" — six paragraphs each opening with "Concede the [N]th objection…" and ending with a reformulated thesis. By paragraph four the rhythm is sermonic.
- **Issue:** The structure is rhetorically clean and prose-flat. Six conceded-then-rebutted paragraphs in a row will lose any reader who is not already convinced.
- **Recommendation:** Compress to three. The first and fourth objections (universality of signals; structural optimism bias) are the load-bearing ones; the others can be addressed in one combined paragraph. Reader gets the move once; doesn't need it six times.

---

## E. Missed counter-arguments

**23. The contrarian's "false positive paralysis" scenario is not fully engaged.**
- **Location:** Counter-Case.
- **Issue:** Contrarian Scenario A: if the four signals are present in 91.5% of all megaprojects, a CEO who acts on them risks paralysis, cost-reductive intervention, or political damage. The Strategist concedes the diagnostic point but does not address the action problem — what does a CEO who sees the signals *actually do* without causing the cure-worse-than-disease problem? The seven recommendations in the Implications section are activities, not decision triggers. A reader looking for "when do I pull the cord" doesn't get an answer.
- **Recommendation:** Add a paragraph in the Counter-Case section or Implications that specifies the decision rule: when do you stop the program vs. surface the risk vs. let it run? Without this, the framework is "be vigilant," which is not a framework.

**24. The Regulatory-Political brief's "things that cannot be moved" point is acknowledged but under-used.**
- **Location:** Counter-Case fifth objection.
- **Issue:** Regulatory-political brief makes the case that PFC, CBP staffing, TSA design changes, and slot caps are immovable on any project timeline. The Strategist concedes this in a paragraph and pivots to "airports can choose their own governance architecture." That is a fair pivot but it obscures the brief's deeper point: the immovable federal constraints are what *produce* the financing structures (P3s, SFRBs, demand-risk debt) that produce the governance fragmentation in the first place. The chain — federal politics → financing structure → governance fragmentation → opening-day failure — is in the regulatory brief and is the most useful causal arc available. The Strategist treats it as a peripheral objection.
- **Recommendation:** Promote the regulatory chain to a load-bearing position. Right now the essay reads as if governance failure is sui generis. The brief argues it is downstream of federal funding politics. That is a stronger thesis. Use it.

**25. Pittsburgh / Memphis / CVG dehubbing pattern goes unused.**
- **Location:** Should appear in the LGA / business-case discussion; does not.
- **Issue:** Airline-commercial-strategist brief documents five US airports (PIT, MEM, CVG, STL, CLE) where the carrier dehubbed and the airport was left holding terminal capacity for traffic that no longer existed. This is the BER failure mode (demand assumption collapse) at US airports, in identifiable cases, with specific carriers. The Strategist mentions Pittsburgh in passing in the historian-style summary but never engages the dehubbing pattern as a US-applicable warning. The MWAA Dulles audience would care about this — IAD has competing-hub risk and a carrier-specific exposure that the Strategist could draw on. Instead the Strategist writes about Air Berlin.
- **Recommendation:** Add a short section or paragraph on the US dehub pattern. It strengthens the applicability claim in the Implications section and gives the airline-commercial lens real estate it has earned.

---

## F. Missed lenses

**26. Chief Engineer lens on constructability and lifecycle cost is underused.**
- **Location:** Throughout.
- **Issue:** Chief-engineer brief offers two load-bearing insights the essay doesn't use:
  - Lifecycle cost structure: terminal capex is 15–20% of 30-year lifetime cost; BHS capex is 30–40%; OPEX consumes 60–70%. Sponsors who optimize ribbon-cutting price defer maintenance pain to year 10–15.
  - CSPP / Part 139: the regulatory machinery that converts a schedule "optimization" into a federally-non-executable plan. This is a forcing function that bounds what owners can do under schedule pressure.
- **Recommendation:** Either add a short section on lifecycle cost as the "fifth warning sign" (the one that doesn't show up in year 1–3 but cripples year 10–15) or use it as part of the prescription set in the Implications. The essay currently treats year 1–3 as the full failure horizon. Chief-engineer brief argues the failure clock keeps running.

**27. Aviation Historian's "current wave is the largest since 1989-1998" framing is buried.**
- **Location:** Executive Summary #4 mentions it.
- **Issue:** Aviation historian's most useful contribution is the framing that the post-deregulation hub-building wave produced Pittsburgh, Mirabel, and Denver, and the current wave (JFK NTO, JFK T6, O'Hare, LAX APM, LGA, Delta LGA, DFW F) is the first comparable concentration of programs. That historical arc — "we have been here before, this is what it broke before, and the scale is bigger now" — should be doing more work in the essay. Currently it appears as a single bullet point and gets dropped.
- **Recommendation:** Open or close the essay with the historical-arc point. Aviation historian's framing is the strongest "stakes" argument available and the Strategist uses it only as a fact.

**28. Airport CEO / COO lenses on bond covenants and operator-inherits framing are absent.**
- **Location:** Implications discusses use-and-lease and CPE, but no covenant mechanics; COO insight on "operator inherits what the project team couldn't close" doesn't appear.
- **Issue:** Airport-CEO brief offers specific covenant arithmetic (1.25x–1.50x DSCR for A-rated airports; covenant breach triggers; 30–60 bps spread widening). Airport-COO brief gives the line "the operator inherits what the project team couldn't close" and walks through specific Day-1 work-order types. Both lenses give the essay concrete operational stakes. Neither is used. The Implications section recommendations are framed at the institutional/governance level, not at the financial-covenant level (CEO's domain) or the punch-list-becomes-work-order level (COO's domain).
- **Recommendation:** Either fold the covenant math into a paragraph in the Implications (the bond market is reading the same news the airport is) or fold the COO's "operator inherits" line into the LGA section, which is exactly that case. Right now these two lenses paid for nothing.

---

## G. Structural issues

**29. The "What the Successful Cases Share" section is too short and too tidy.**
- **Location:** Subsection of The Argument.
- **Issue:** Three paragraphs cover Istanbul, Changi T4, and Kansas City and then close with a one-line aphorism ("These are not warning sign detectors. They are warning sign actors."). After 2,000 words of detailed failure narrative, the successful cases get clipped, summary treatment. This unbalances the essay: the failures get cinema, the successes get a paragraph each. McPhee would not write this way.
- **Recommendation:** Either expand one success case to scene-level depth (Changi T4's 7,500 volunteers running 100+ trials with 2,500 staff is a film waiting to be made) or accept that the successes are framework-points, not scenes, and admit it. The current half-measure is the weakest section in the essay.

**30. The Implications section has seven sequenced recommendations.**
- **Location:** Implications.
- **Issue:** First, second, third, fourth, fifth, sixth, seventh. Each paragraph opens with the ordinal. This is a deliverable structure, not an essay structure. McPhee, Lewis, Gawande do not write seven-point recommendation sections. They embed implications in narrative or land on two or three central directives.
- **Recommendation:** Consolidate to three or four directives, each with more weight and a real-world example or analogue. Or, if seven recommendations are needed, format them as an addendum at the end ("For the operator: a checklist") and let the body of the implications section be prose.

**31. The closing photograph image is good but underdeveloped.**
- **Location:** Final two paragraphs.
- **Issue:** "There is a photograph from BER's October 2020 opening day. The terminal is largely empty…" The image lands. The follow-up paragraph — "A capital planner looking at the next decade should ask…" — collapses back into rhetorical question mode. The photograph deserves more than a quick beat.
- **Recommendation:** Either let the photograph end the piece (cut the explanatory paragraph) or give the photograph one more beat of description before the closing question. The current version reads as if the writer noticed they needed to land the thesis and ran out the door.

**32. The essay does not show its sources.**
- **Location:** Throughout.
- **Issue:** This is a Stage 2 strategist draft, not the final, so attribution will tighten in editing. But the draft as written makes specific factual claims with no in-line citations — the fact-checker will need them. Several of the most evidence-heavy paragraphs (the di Mauro quote, the 66,500 defects figure, the $360 million Denver delay cost) appear without attribution. The fact-checker will flag every one.
- **Recommendation:** Either add inline source attribution now (saves the editor a pass) or add a working source table at the bottom of the draft so the editor and fact-checker can verify against the briefs.

---

## H. Things the Strategist got right (so the next draft does not break them)

The Munich opening is the best paragraph in the essay. Keep it.

The "architecture of silence" frame is doing real work — even where it is asserted rather than scened, it gives the argument a center of gravity.

The Counter-Case section concedes more honestly than most consultant-grade analyses do. The five objections are real and the section addresses them in good faith. The problem is structural (it's too long and stacks the same move six times), not substantive.

The LGA section is the right kind of complication for the thesis — it is the case where the standard four-signal framework doesn't cleanly catch the failure mode, and the Strategist acknowledges that. Do not lose this section.

The closing photograph image, even underdeveloped, is the right note to land on.

---

## Bottom line for the Strategist

The piece reads as a strong draft of a board-grade analysis dressed up as long-form essay. The argument is sound. The evidence is real where it is sourced. Three numbers and one whole case (Kansas City) need to be either sourced or struck. The structural revisions are bigger than the factual ones: the Executive Summary needs to be rebuilt around the sharper thesis the Counter-Case produces; the Implications need to be cut from seven points to three or four; the subsection openers need to stop announcing themselves like deck slides. The lenses from chief-engineer, airline-commercial-strategist (US dehub pattern), aviation-historian (current wave is the largest since 1989-1998), and airport-CEO (covenant mechanics) are not adequately used. Pull them in.

The thesis is publishable. The draft is not yet.
