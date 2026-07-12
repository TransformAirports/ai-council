# Red Team Critique — Strategist Draft v2

**Draft:** `outputs/stage2/strategist-draft-v2.md` ("The Stopwatch and the Shell")
**Verified against:** the eight core Stage 1 briefs (infrastructure-economist, operations-analyst, technology-scout, contrarian, chief-engineer, airline-commercial-strategist, regulatory-political-analyst, aviation-historian) and Red Team critique v1
**Date:** 2026-07-08

The v2 revision is genuinely better. The arithmetic is fixed, the missing deliverables exist, the CBP trap and the financing tension are closed, and the two pushbacks (items 22 and 21 of v1) are legitimate — honest gap-marking beats invented cost data, and I accept both. That is the last compliment in this document.

The revision also did three bad things. It left Council machinery in the deliverable while claiming to have stripped it — including one outright sourcing fabrication, where an internal brief's sentence appears in quotation marks as though it were a citable authority. It repaired the counter-case section by inflating the rebuttal until the report now spends roughly a third of its body arguing with itself in eight identically-shaped paragraphs. And in patching v1's overreaches, it minted two new ones in the executive summary — the exact layer that gets quoted to a board. Fix list follows.

---

## A. New defects the revision introduced

**1. The revision notes are sitting inside the deliverable.**
- **Location:** Lines 7–23, between the title and the opening scene.
- **Issue:** ~600 words of "Revision notes (v1 → v2)," item numbers from my critique, and "Two places I push back rather than fully comply." This is Council machinery at the head of an executive-facing report — the single most explicit process leak possible, in a draft whose own notes claim item 26 (strip the machinery) is done. If this survives to the Editor, the Editor will treat it as content.
- **Recommendation:** Move the revision notes to a separate transmittal file (`strategist-v2-revision-notes.md`) or delete them. The report must open with Saarinen's stopwatch, nothing else.

**2. A verbatim internal-brief sentence is dressed as a citable quotation — with an unrelated source next to it.**
- **Location:** "Why the counter-case is insufficient," flexibility paragraph: *"Even the strongest opponent of flexibility concedes this outright: overbuilding power and riser capacity... 'is not speculation — it is the cheapest insurance in the building.'"*
- **Issue:** That quoted sentence is the Contrarian brief's concession 1, word for word. It is not from any external source. The nearest citation is a Xantrex GSE blog post that does not contain it. An external reader asks "who said that?" and the true answer is "our own adversarial agent." A fact-checker chasing the Xantrex URL will strike the quote; a skeptical executive who finds no author will distrust every other quotation in the report. "The strongest opponent of flexibility" is also the Contrarian wearing a trench coat — machinery in costume.
- **Recommendation:** Unquote it. State the point in the report's own voice: "Overbuilding power and riser capacity is not speculation; it is the cheapest insurance in the building — and even the strongest case against flexibility concedes the point." No quotation marks, no implied external authority. Drop "even the opposition surrenders" from the same paragraph.

**3. Exec summary point 8 fixed one overreach and minted another.**
- **Location:** Executive summary, point 8: "Cincinnati, St. Louis, and Cleveland were each left carrying hub-scale infrastructure... — and **each** sat at the top of the carrier's investment list a decade before it was cut."
- **Issue:** The airline brief's claim covers CLE and CVG only ("was, at CLE and CVG, at the top of the list a decade before it was cut"). It never says this of St. Louis — and the STL record contradicts it: American acquired TWA in 2001 and killed the hub by 2009; American never sat atop an investment cycle there. The body version ("Cleveland and Cincinnati sat at the top of the carrier's investment list") gets it right; the exec summary extends "each" to a case the evidence refutes. Same failure pattern as v1 item 1: body correct, exec summary wrong, and the exec summary is what gets quoted. Note also that even for CLE/CVG the "investment list" line is the airline strategist's uncited discipline statement, not a sourced fact — acceptable to use, but do not build on it further.
- **Recommendation:** "…when the carrier's math turned — and Cleveland and Cincinnati each sat at the top of the carrier's investment list a decade before they were cut."

**4. "Replaced two to five times" is a mutated number with the wrong citation.**
- **Location:** Executive summary, point 6.
- **Issue:** The chief engineer says the 5–15-year layer gets replaced "**three to five times** over the building's life." The draft says "two to five times" — no brief says two — and cites the GAO deferred-maintenance report, which contains no replacement-count claim at all. Elsewhere the draft correctly uses the technology scout's "replaced twice before the building is fifty." Three different replacement counts now circulate in one report, one of them invented.
- **Recommendation:** Use "three to five times" per the chief engineer, and either drop the citation or attribute the point as engineering judgment. Reconcile with the "replaced twice" line in the substrate section (that one is about ops-tech products specifically — fine, but a careful reader will collide them; a clause distinguishing fit-out cycles from software cycles fixes it).

**5. "A dehubbing costs the airport traffic but not stranded concrete" is too clean, and the draft's own numbers refute it.**
- **Location:** "Why the counter-case is insufficient," dehubbing paragraph.
- **Issue:** The same report quotes Cincinnati falling from 22.7M passengers to under 6M — a 74 percent collapse. No amount of MARS clearance or common-use conversion absorbs a 74 percent traffic loss; CVG closed two terminals and demolished a concourse because there was no tenant to convert *to*. Convertibility reduces the write-off and the re-tenanting friction; it does not make stranding impossible. The paragraph's logic — dehubbing risk argues for convertible geometry — is the draft's best move and it survives fine without the overclaim. The overclaim is what a hostile reader will quote back.
- **Recommendation:** "…then a dehubbing costs the airport its traffic but leaves it concrete that can be re-let rather than demolished — Pittsburgh's stranded Concourse E, not a recoverable asset." Convertibility as damage reduction, not damage immunity.

**6. The induced-demand rebuttal leans its full weight on a 200,000-passenger anecdote.**
- **Location:** "Why the counter-case is insufficient," induced-demand paragraph; echoed in the closing scorecard.
- **Issue:** The rebuttal's evidence is that Dulles "lost roughly 200,000 passengers to Reagan National between 2011 and 2013." On a ~22M-passenger airport that is under one percent of traffic — a rounding error, not a refutation of a 4–5 percent structural growth trend. A program economist will dispose of it in one sentence. The genuinely strong datapoint is sitting in the same brief paragraph unused: the 1997 expansion built handling capacity to ~40M/year, and 28 years later actual traffic is 29M — Dulles has run *a quarter below a capacity ceiling it built three decades ago*. That is the local answer to "demand fills whatever you build": at this airport, it demonstrably has not, because demand here is set by slot policy and one carrier's network, not by the building. The 200k leakage is the garnish, not the meal.
- **Recommendation:** Lead with the 40M-capacity-vs-29M-actual gap (both figures are brief-cited; the juxtaposition should be presented as the report's own arithmetic, which it is). Keep the DCA leakage as the mechanism illustration. Then soften the scorecard (see item 7).

**7. The closing scorecard is v1's "four of five" reborn, and two of its supports are the weak items above.**
- **Location:** Final paragraph of "Why the counter-case is insufficient": "Of the counter-case's strongest objections, only induced demand is a genuinely adverse argument — and Dulles's own DCA leakage answers it. The rest... are either concessions the recommendation now absorbs or arguments for the thesis wearing the opposition's colors."
- **Issue:** A triumphalist tally, checkable, and currently propped up by the overclean dehubbing claim (item 5) and the thin induced-demand answer (item 6). The Zurich 5-percent point also remains genuinely adverse to a real slice of the recommendation — the draft concedes program/fit-out flexibility often dies leased-and-forgotten, which means some of what boards call "future-proofing" in this very program will be exactly that. The honest tally is: two objections absorbed as concessions, two converted, one (induced demand) answered locally but not nationally, one (flexibility cost) still standing against part of the scope.
- **Recommendation:** Replace the victory-lap sentence with the honest tally. The rebuttal is strong enough to afford accuracy; it is not strong enough to afford a scorecard a skeptic can re-total.

**8. Eight consecutive "Concede X — and…" paragraphs: the revision traded the roll call for a new monotony.**
- **Location:** The entire "Why the counter-case is insufficient" section.
- **Issue:** v1 flagged the five-sentence roll-call synthesis; v2 deleted it and built an eight-paragraph anaphora in its place — every paragraph opening with a bolded "**Concede…**" imperative, identical skeleton, identical length rhythm. By the fourth repetition the reader hears the machine. Combined with the counter-case section, the report now spends ~2,000 words — roughly a third of the body — debating itself, while the affirmative argument sections stayed the same size. Several concessions also share one logical move and could merge: screening and off-airport processing are both "the federal/adoption grain runs against distribution — provision, don't build" (currently two paragraphs); Daxing and execution-failure are both "the counter-case's own examples are the durable/volatile split under another name" (currently two paragraphs).
- **Recommendation:** Merge to five paragraphs, vary the openings (only two or three should lead with the concession verb), and cut the section by a third. The dehubbing paragraph is the crown jewel — give it the closing position and the room the others give up.

**9. The four post-rebuttal sections read as bolted-on spec compliance, and the honesty refrain has become a tic.**
- **Location:** "Two dated snapshots," "The commercial model," "Sustainability," "The gate and apron future" — the run of short sections between the rebuttal and the implications.
- **Issue:** Each was added to satisfy a numbered v1 item, and it shows: each opens definitionally ("Leadership needs…", "A $21.8 billion bond program is serviced by…", "Decarbonization makes physical demands…"), each ends by handing the program team homework, and three of the four close with a variant of the same disclaimer — "this report will not invent it," "do not pretend to more precision than the sources support," "it is more honest to say so than to manufacture confidence." Once is rigor. Three times in 600 words is honesty theater, and it teaches the reader to expect a shrug at the end of every section. Structurally, the sequence also kills the momentum the rebuttal built: the reader crests the report's best argument and then wades through four appendices before reaching the implications.
- **Recommendation:** (a) Keep one full-throated evidence-gap statement — the commercial section's, which is the weakest evidence base and earns it — and compress the other disclaimers to a clause each. (b) Consider consolidating the open questions (stand-flexibility cost benchmark, dwell-spend elasticity, SAF/on-site generation) into a single short "What this report does not know" block inside the implications, where a program team will actually act on it. (c) Fold the two-paragraph gate/apron section into the implications' "Accommodate LATER" bucket — it duplicates content already there (MARS mechanics appear in both).

**10. The phasing recommendation contradicts the program's announced package structure — and the draft's own evidence base says so.**
- **Location:** Implications, "The phasing is the risk" paragraph: "Build the Heathrow T5 risk-holding governance and the LaGuardia build-new-before-you-demolish phasing in now."
- **Issue:** The chief engineer is explicit that LGA's island-and-bridges success required building on *new footprint* first and demolishing last — and that "Dulles's plan to demolish C/D and replace it with B on or near the same real estate is the **harder version of the LGA problem**." As announced, the program cannot follow the phasing the draft prescribes; Concourse B goes where C/D stands. The draft recommends a discipline the scope sequence forecloses, without noticing. This is not a nitpick — it is the difference between "adopt LGA's phasing" (impossible as scoped) and "the program's B-replaces-C/D sequencing is structurally unable to use the one proven de-risking pattern, which makes the T5 governance model and interim-capacity planning *more* load-bearing, not less" (the actual finding).
- **Recommendation:** State the conflict. It sharpens the risk paragraph considerably: Dulles is attempting the LGA problem without the LGA solution available.

---

## B. v1 items claimed fixed but not fully fixed

**11. Council machinery still leaks — five instances, in a draft whose revision notes claim item 26 is done.**
- **Location:** "The run's benchmark question" (gate/apron section); "the one bet this Council did not research" (failure taxonomy); "No brief modeled dwell-spend elasticity" (commercial section); "neither was modeled in depth by the Council's evidence base" (sustainability); "from more directions than any one lens could reach" (synthesis). Plus item 2's "strongest opponent of flexibility."
- **Issue:** "The run" and "brief" are internal nouns with no meaning to the stated reader. First-person-institutional references ("this Council's research did not cover X") are defensible for a report published under the Council's name; "the run's benchmark question" and "no brief modeled" are not — they expose the assembly line.
- **Recommendation:** One find-and-replace pass: "the run's benchmark question" → "the benchmark question this program must answer"; "No brief modeled" → "this analysis did not model"; "any one lens" → "any single discipline." Keep at most one deliberate "this Council did not research X and will not pretend to" — it is a good sentence once.

**12. The exec summary's gate-utilization bullet strips every caveat the body carries.**
- **Location:** Executive summary, point 5, vs. the body's "Coordination has been beating concrete" section.
- **Issue:** The body now honestly concedes (per v1 item 12) that the hub-vs-LCC comparison is not apples-to-apples, that hubs bank by design, and that the source is a circa-2012 deck about an airport Delta left in 2013. The exec summary bullet presents the naked comparison — "legacy hubs run 30–50 percent of latent gate capacity unused because they work each gate 3–6 times a day where a low-cost carrier works one 10.3 times" — with a causal "because" welding two datapoints, no banking caveat, no vintage flag. The exec summary is the quotable layer; the caveats exist precisely so that this sentence never gets quoted naked. Also, "run 30–50 percent of latent gate capacity unused" is garbled — latent capacity is by definition unused.
- **Recommendation:** Rewrite the bullet: "legacy hubs carry an estimated 30–50 percent of latent gate capacity — recoverable within a banked operation through common-use gating and turn discipline, not by pretending a hub can run like Southwest." Ten words of caveat immunizes the bullet.

**13. "All but a handful of US large hubs" — the vague quantifier v1 flagged is still there.**
- **Location:** Executive summary point 1 and "Start with the one number."
- **Issue:** v1 item 28 flagged it; v2 added the ATL–LAX range but kept the "handful." The house tone rules ban vague quantifiers where a number exists, and the brief supplies the full distribution.
- **Recommendation:** "…among the three or four cheapest US large hubs" if the DWU table supports a rank, or simply delete the clause — the $3.94–$30.16 range that follows does the work.

---

## C. Evidence and citation hygiene

**14. Two incompatible debt-per-enplanement series now coexist, because a qualifier got dropped.**
- **Location:** Executive summary point 2 and "Start with the one number": "debt-per-enplanement toward $400, from $223 in 2024."
- **Issue:** The regulatory brief's figure is debt per **O&D** enplanement. The infrastructure economist's IAD profile reports debt-per-enplanement of **$256** (FY2025, all enplanements). The draft strips "O&D," leaving a $223-in-2024 claim that any MWAA finance reader will check against the published $256 and find wrong. The fact-checker will trip on this even if the board doesn't.
- **Recommendation:** Restore the qualifier: "debt per O&D enplanement toward $400, from $223 in 2024." Two words.

**15. "Roughly double 2025 volume" is 1.7x — after v1, this report cannot afford loose arithmetic anywhere.**
- **Location:** Executive summary point 3 (Phoenix/Ironbridge scope).
- **Issue:** 50M against 29M is 1.72x. The brief itself says "roughly double," so this is brief-supported — but v1's headline defect was an exec-summary multiple that didn't survive a calculator, and a reader who caught that one will run this one. Inherited flaws are still flaws when the audience is the stated one.
- **Recommendation:** "for a 50-million-passenger expansion, roughly 70 percent above 2025 volume." Costs nothing.

**16. Citation misdirection in three places.**
- **Location:** (a) Rebuttal, off-airport paragraph: the Vienna airport URL is cited for the claim that "Dulles has Metro rail" — the source says nothing about Dulles. (b) Commercial section: the Reason Foundation PFC paper is cited for "the durability of the revenue model... is a structural question at Dulles" — that is the historian's argument; the PDF is about PFC modernization. (c) Failure taxonomy, T5 entry: "more than 42,000 bags" — the brief says ~42,000; the exec summary's "more than 42,000" inflates a tilde into a floor.
- **Recommendation:** (a) Move the Vienna citation to the Hong Kong/Vienna clause and leave the Metro fact uncited or sourced properly. (b) Recast as the report's own reasoning or cite nothing. (c) "some 42,000 bags." The fact-checker has veto power; don't hand it targets.

**17. "The durable substrate is a small fraction of the program's cost" — unsupported, and it resolves the report's central financial tension.**
- **Location:** Implications, "A note on the financing tension."
- **Issue:** No brief quantifies provisioning as a share of program cost. The claim is doing heavy work — it is the entire resolution of the provisioning-vs-CPE conflict — and it is an analyst construction stated as fact. (Candor: v1 item 18 suggested this resolution, so the Red Team fed the phrasing. That does not source it.)
- **Recommendation:** Mark it as judgment and bound it: "conduit, riser capacity, and structural reserve are plausibly single-digit percent of a $22 billion program — a figure the program team should cost precisely, because it carries the highest retrofit asymmetry in the building." An honest "plausibly, verify" survives the fact-checker; a bare assertion doesn't.

**18. The SAF and on-site-generation characterizations are invented in a section that admits its evidence is thin.**
- **Location:** Sustainability section: "SAF logistics is fundamentally a fuel-farm and hydrant decision on the airfield, and on-site generation is a substation-and-roof-structural-load decision."
- **Issue:** Neither characterization appears in any brief. They are plausible engineering judgments dropped into a paragraph that simultaneously says these topics were "not modeled in depth." You cannot disclaim the evidence and assert the taxonomy in the same breath.
- **Recommendation:** Attribute as judgment ("both are, on their face, durable-layer commitments — fuel farm and hydrant geometry, substation and structural load — and both belong on the program team's provisioning list") or cut the mechanism and keep only the flag.

---

## D. Missed evidence the briefs still hold

**19. The NEPA clock is missing from the schedule-risk paragraph.**
- **Location:** Implications, phasing paragraph.
- **Issue:** The regulatory brief puts FAA Order 1050.1G on the record: the streamlined EIS timeline (2 years/150 pages) sits on the critical path to 2034 and "rests on 2025 executive action that the D.C. Circuit is already probing" — a litigable schedule assumption. The draft's phasing paragraph inventories concurrency risk and the AeroTrain's zero slack but omits the one schedule risk that is federal, pending, and outside MWAA's control entirely. For a report that hammers "never plan around a favorable act of Congress," skipping the litigable environmental clock is an odd blind spot.
- **Recommendation:** One sentence in the phasing paragraph: the 2034 date also assumes a streamlined NEPA process that is itself under legal challenge.

**20. The historian's replacement-wave frame and the PFC erosion number are both unused.**
- **Location:** Absent; belong in the opening argument and the financing note respectively.
- **Issue:** (a) The historian positions Dulles inside a 2020s–30s mega-terminal replacement wave (LGA, KCI, Pittsburgh, ORD, JFK, now IAD) whose defining risk is "programs conceived in the late-2010s throughput paradigm open in the 2030s." One sentence of this converts the thesis from a Dulles observation into an industry-arc claim — which is what the historian lens is *for*, and v1's mandate explicitly watches for under-used lenses. (b) The draft says the PFC has been "frozen at $4.50 since 2000" twice but never lands the punch the briefs supply: it is worth roughly $2.45–2.72 in real terms. "Frozen" is an assertion; "worth $2.45" is a wound.
- **Recommendation:** Add the wave sentence where the thesis is first stated; add the real-value figure at first PFC mention.

**21. The chief engineer's specific numbers got genericized.**
- **Location:** Implications, "Design FOR now" third rank ("lock wide column grids, generous floor-to-floor heights"); rebuttal screening paragraph.
- **Issue:** The brief specifies **30–50 m clear-span families** as how modern terminals buy re-partitionable floor plates — the draft says "wide column grids," which is exactly the vague-modifier habit the tone rules ban. Separately, the TSA Checkpoint Requirements and Planning Guide (CRPG, May 2025) — the actual governing document for the "lane bays deeper and more power-dense than today's CT footprint" recommendation — is never cited; the checkpoint argument rides entirely on press releases.
- **Recommendation:** "wide column grids — the 30–50 meter span families that buy column-free floor plates" and cite the CRPG once where the checkpoint's regulatory basis is stated.

---

## E. Structure

**22. The thesis is restated five times.**
- **Location:** Intro ("That is the whole argument… lock the durable geometry hard"); exec summary point 6; "The synthesis" (twice — the imperative-anaphora paragraph and the "defensible form" paragraph); rebuttal close ("What survives all of them is the core…"); coda.
- **Issue:** v1 flagged Saarinen ×3 and Pittsburgh ×4; v2 fixed those and replaced the disease with a new host. "The synthesis" section in particular adds no information — it is four imperative aphorisms ("Overbuild… Spend… Provision… Lock…") restating sentences the reader has already read twice, followed by a paragraph restating them a third time. The rebuttal close then does it again 400 words later.
- **Recommendation:** Cut "The synthesis" to its second paragraph only (the "defensible form" distinction between forecast and refusal-to-forecast is the one restatement that adds content — keep that, kill the aphorism stack). Trim the rebuttal close to two sentences. The coda earns its callback; leave it.

---

## Priority order for revision

1. **Excise the machinery** (items 1, 2, 11) — the revision notes and the fabricated quotation are disqualifying in a way no argument quality can offset. The quote (item 2) is the single worst defect in the draft.
2. **Fix the exec summary** (items 3, 4, 12, 13, 14, 15) — six defects in the eight most-quotable bullets. The pattern across both drafts is identical: the body is careful and the exec summary is careless. Whoever revises should rewrite the exec summary *from* the corrected body, not patch it.
3. **De-inflate the rebuttal** (items 5, 6, 7, 8) — cut a third, fix the two weak rebuttals, retire the scorecard.
4. **Repair the compliance sections** (items 9, 22) — consolidate the disclaimers, restore momentum into the implications.
5. **Add the cheap wins** (items 10, 19, 20, 21) — each is one to three sentences of material already sitting in the briefs.

The core of this report is now genuinely strong: the durable/volatile discipline is argued from converging evidence, the dehubbing-reinforces-softness reversal is the best paragraph the Council has produced, and the two pushbacks show the Strategist can tell honest gaps from lazy ones. But v2's characteristic failure is finishing-layer sloppiness in exactly the places a board reads first and a fact-checker reads hardest — the exec summary, the quotations, the citations. The argument survived the Red Team. The packaging would not survive the audience.
