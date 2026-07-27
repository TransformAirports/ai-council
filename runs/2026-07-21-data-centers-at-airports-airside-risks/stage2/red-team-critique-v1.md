# Red Team Critique — Strategist Draft v1
**Run:** Data Centers at Airports: Airside Risks
**Target:** `outputs/stage2/strategist-draft-v1.md`
**Date:** 2026-07-21

The draft is strong on structure and honest about the counter-case — better than most first drafts. That is exactly why its remaining defects matter: they are the ones a hostile reader at a zoning board, a developer's counsel, or the FAA will find. Twenty-four items follow. Items 1–4 are the ones that can sink the piece.

---

## A. Internal contradictions and logical gaps

**1. The draft asserts both "directly under Dulles operations" and "aircraft do not routinely fly through its plumes." Pick one, or distinguish the geography.**
- **Location:** "A geometry test for a machinery problem," final paragraph ("roughly 200 data centers... directly under and adjacent to Dulles operations") vs. "Why the Counter-Case Is Insufficient," second rebuttal ("the Digital Dulles site sits to the west, so aircraft do not routinely fly through its plumes... The quiet is partly geometry").
- **Issue:** These claims cannot both carry weight as written. If Data Center Alley sits "directly under" Dulles departures (Chief-Engineer brief, citing City Journal: "departures routinely overflying facilities"), then the natural experiment *does* include routine overflight, and the "quiet is geometry" rebuttal collapses. If the clusters sit off the flight paths (Deep-Research, on Digital Dulles specifically), then "directly under" is rhetorical inflation. The two claims are about different sites — Ashburn/Sterling to the north/east vs. the Digital Dulles parcel to the west — but the draft uses each where convenient and never says so. A contrarian reader will quote one section against the other.
- **Recommendation:** Disaggregate. State explicitly: the Ashburn/Sterling cluster is overflown (which is why the natural-experiment argument has force there and demands the "never investigated" rebuttal), while Digital Dulles sits west of the north–south flow (which is why *its* quiet record proves little). Then the rebuttal holds on both fronts instead of neither.

**2. The published screen abandons the risk-tiering the entire argument promised.**
- **Location:** "Implications for MWAA," third move ("Publish the screen, and require these studies on any data center within the 5-statute-mile approach/departure zone...") vs. "Why the Counter-Case Is Insufficient," final two paragraphs ("configuration-first, risk-tiered screen... Classify the outdoor heat-rejection system first... not by a proximity line drawn around every building").
- **Issue:** The draft spends two full sections agreeing with the Contrarian that a proximity-triggered blanket gate "would deserve to lose" — then publishes a proximity-triggered blanket gate. Every data center inside the 5-mile ring gets all five studies, including the closed-loop dry design the draft said should be "waved through." The Technology-Scout's core instruction — cooling-type classification *sets* the tier, and study requirements scale to it — appears in the rhetoric and vanishes from the tool. The Contrarian brief says explicitly: "If the tool is a generic precautionary gate applied to every building over a proximity line, this brief is the argument that will be used to defeat it at the zoning board." The Strategist quoted that warning and then built the tool it warns against.
- **Recommendation:** Restructure the screen as a two-stage gate: Stage 1 (universal, cheap): configuration disclosure — cooling type, generator fleet size and permitted run-hours, stormwater design, capacity-foreclosure geometry. Stage 2 (triggered): full study package scales with the Stage 1 answers. Capacity-foreclosure and wildlife/stormwater remain universal pass/fail (they are configuration-independent); plume, EMI, and emergency-response studies tier by configuration.

**3. The screen assumes jurisdiction MWAA does not have — the exact failure the COO predicted.**
- **Location:** "Implications for MWAA," third move, and generally throughout the screen.
- **Issue:** The Airport-COO brief warns in plain terms: "On the parcels that matter most — the ones off the airport fence but under the approach — the operator is a commenter, not a decider... A recommendation that pretends the COO can veto a Loudoun parcel will fail in execution and everyone in the ops center knows it." The draft's screen "requires" studies on "any data center within the 5-statute-mile approach/departure zone" — most of which is Loudoun, Fairfax, and Prince William land where MWAA holds no approval authority. The draft never distinguishes what MWAA can *require* (its own land, via lease) from what it can only *advocate* (off-airport, via 7460 comments, the §743 notification, and intergovernmental agreements). This is not a nuance; it is the difference between a decision tool and a wish.
- **Recommendation:** Split the screen into two instruments: (a) the binding version, applied to MWAA land through the ground lease and ALP process; (b) the advocacy version — the same technical standard published as MWAA's formal position, deployed through 7460 comments, the §743 "materially impacts" framing, and county land-use proceedings. The Virtual-Chris brief's "become the reference standard" framing is the honest way to sell (b); use it, but label the difference in enforceability.

**4. The emergency-response counter-argument is presented at full strength and never answered.**
- **Location:** "The Counter-Case, Honestly Presented," fourth paragraph ("a low-occupancy, highly automated, clean-agent-suppressed building... may be a *lighter* burden than the hotel, arena, or hospital that zoning would otherwise allow") vs. "Why the Counter-Case Is Insufficient," which rebuts only three things: the controlling scenario, absence-of-evidence, and irreversibility.
- **Issue:** The draft's Executive Summary point 3 makes emergency response a headline pillar ("an industrial fire the airport was never sized to fight"). The counter-case then concedes the opposing view. The rebuttal section never returns to it. The Director-of-Public-Safety's own brief contains the answer ("the airport does not have to own the fire... the marginal draw on ARFF can be bounded" — but only if fire flow, battery suppression, mutual-aid pre-plans, and SIDA access are proven *before* approval, which is the thesis), and the Emergency-Management brief adds the "proves too much" rejoinder: "'It's engineerable if EM is consulted early' concedes the whole point." The draft has the ammunition in the briefs and leaves the pillar standing half-demolished.
- **Recommendation:** Add a fourth rebuttal — one paragraph. The lighter-than-a-hotel argument is a *design claim*, and design claims are exactly what the screen makes the developer prove. Same move the draft already makes for wildlife and plume. Also address the "singling out data centers" objection (DPS brief: "every large industrial tenant carries fire load") — the answer is scale and correlation (EM brief), not category.

**5. "That concession is fatal to the counter-case" — overclaim.**
- **Location:** "Why the Counter-Case Is Insufficient," third rebuttal.
- **Issue:** The Contrarian conceded that land-use permanence is "a real cost the height-only review does miss." That is narrower than "fatal." The Contrarian's actual bottom line is conditional: the thesis wins *if* the screen is scenario-specific and loses if it is a generic gate. Moreover, irreversibility is not data-center-specific — a hospital or fulfillment center forecloses a runway just as permanently. The draft never explains why capacity-foreclosure discipline is a *data-center* screen rather than a general land-disposition discipline, which invites the response "then this isn't about data centers at all."
- **Recommendation:** Downgrade "fatal" to what the evidence supports: the concession removes the counter-case's ability to oppose the *capacity-preservation* gate specifically. Then own the generalization: capacity foreclosure is a land-discipline question that applies to any permanent building; what makes data centers the forcing case is the combination of permanence + scale + the operating-envelope risks (generation, water, fire) that other permanent tenants don't carry. That is a stronger, more honest formulation.

## B. Cherry-picked evidence and unreconciled brief conflicts

**6. Generator-count number-shopping: the draft quietly picks the biggest of three conflicting figures.**
- **Location:** Executive Summary point 2; "The wrong day," third paragraph.
- **Issue:** The panel produced three inconsistent Virginia generator counts: 10,500+ permitted / ~27 GW (Operations-Analyst, citing Virginia Mercury), ~9,000 statewide / ~4,700 in Loudoun (Chief-Engineer, citing VPM), and 4,700 in one county at 12 GW (Emergency-Management, citing Environment America). The draft uses only the largest, twice, with no acknowledgment that its own panel disagrees by a factor of two-plus. The fact-checker will trip on this; a hostile reader will call it inflation. (Same pattern at "26 to 50 million square feet" — see item 8.)
- **Recommendation:** Either reconcile (permitted units vs. installed units vs. one county vs. statewide are probably different denominators — say which) or use the most conservative defensible figure with the source's framing. The argument survives fine on 4,700 generators in one county.

**7. Generator test-hours: the draft cites both "capped near 100 hours a year" and "20-minutes-a-month test profile" without noticing they differ by an order of magnitude.**
- **Location:** Executive Summary point 2 and "The wrong day," third paragraph (100-hour cap) vs. same section, final sentence of third paragraph ("today's 20-minutes-a-month test profile").
- **Issue:** 100 hours/year (COO brief, backuppower.ai — a regulatory *cap*) and 10–30 minutes/month actual testing (Chief-Engineer, VPM — observed practice) and 50–150 hours/year (Technology-Scout, WRI) are three different quantities: permitted maximum, observed practice, and typical range. The draft deploys the cap when it wants the scenario to look big and the 20-minute figure when it wants today's baseline to look small. Both uses are individually sourced; together they are incoherent unless labeled.
- **Recommendation:** One sentence fixes it: "actual testing runs 10–30 minutes a month per unit; the federal *cap* is near 100 hours a year; and the emergency-run allowance is unlimited — the risk lives in the gap between the second number and the third."

**8. Data Center Alley sizing: "some 26 to 50 million square feet" launders a 2x disagreement between briefs into a range, with wrong attribution.**
- **Location:** "A geometry test for a machinery problem," final paragraph.
- **Issue:** 26M sq ft is the COO's figure (DataCenterDynamics, Loudoun operating stock); ~50M is the Chief-Engineer's (City Journal, a different scope). Presenting the disagreement as a range implies a source said "26 to 50." None did. The bracket cites [Technology-Scout, Airport-COO briefs], but 50M appears in neither. Also unresolved nearby: the Western Lands acreage is 424 in five briefs and 433 in the Airport-CEO brief — pick one and note the variance for the fact-checker.
- **Recommendation:** Use one figure with its actual source and scope ("roughly 26 million square feet of operating data center in Loudoun County alone"), or state that estimates run from 26M (operating, Loudoun) to ~50M (broader corridor). Fix the citation.

**9. Bird-strike altitude: the panel's numbers conflict and the exec summary glosses the altitude band.**
- **Location:** Executive Summary point 4; "The risk with a number."
- **Issue:** The Operations-Analyst says ~95% of strikes occur below ~1,067 m (≈3,500 ft); Deep-Research says 78% below 1,000 ft and 90% below 3,000 ft, per FAA data. The draft states the 95% figure twice and calls 3,500 ft "the low-altitude approach and departure band," which flattens a meaningful difference — 3,500 ft is not "low altitude" in the sense the plume argument uses. A reviewer who knows the FAA wildlife data will notice.
- **Recommendation:** Use the layered FAA formulation (78% below 1,000 ft, ~90% below 3,000 ft) or keep the 95%/1,067 m figure with its actual altitude stated. Either works for the argument; the current hybrid does not.

**10. The single-controlling-scenario claim overstates convergence and buries the Operations-Analyst's explicit finding that no single worst case exists.**
- **Location:** "The wrong day," second paragraph ("Every brief that touched the physics converged on this... The COO, the emergency manager, the operations analyst, and the contrarian all landed in the same place independently").
- **Issue:** The Operations-Analyst explicitly did *not* land there: "For turbulence it is peak sensible-heat rejection (hottest day...). For visibility obscuration it is cold, humid, high-load evaporative operation... a single 'worst case' does not exist... The study must run both envelopes." Deep-Research separately identifies the cold-still-day full-IT-load case as most critical for plume rise. The draft's screen then requires the plume tool run only on "the full islanded-generation load case under calm, cold, stable conditions" — and omits the visible-plume/obscuration study under the cold-humid envelope and the peak-cooling turbulence case entirely. The run file's own success criterion ("Compare normal cooling, peak demand, generator testing, utility outages, and prolonged emergency generation") is only partially delivered.
- **Recommendation:** Keep prolonged generation as the *headline* controlling scenario (it is defensible and three briefs plus the Contrarian's concession support it), but state the Ops-Analyst's multi-envelope point honestly, add the obscuration study (cold-humid, PAPI/visual-segment sightlines) to the screen, and add a short passage that actually walks the five operating states the run file asked for.

**11. The fire-water claim drops the configuration-dependence the draft champions everywhere else.**
- **Location:** "The tenant the airport did not staff for," second paragraph ("hyperscale cooling draws 1 to 5 million gallons a day, silently re-rating the airport's available fire flow").
- **Issue:** 1–5 MGD is the *evaporative* hyperscale figure. A closed-loop or dry-cooled facility — the design the draft's screen rewards and waves through — draws a fraction of that. Stating the water draw unconditionally, in a section arguing the emergency burden, is the same conflation the draft accuses others of on plumes: treating the worst configuration as the category.
- **Recommendation:** Condition it: "an evaporative hyperscale campus draws 1 to 5 million gallons a day" — and note that this is one more reason the cooling-type disclosure is the screen's first question.

**12. The dry-cooling economics and the closed-loop industry trend are left pointing in opposite directions.**
- **Location:** "Why the market will always argue 'yes,'" third paragraph ("The plume-free option is the one the developer can least afford") vs. "The Counter-Case," fifth paragraph ("the industry is moving to closed-loop liquid and 'zero-water' cooling... the marginal new campus is *less* plume-generating than the last one").
- **Issue:** Both are sourced, and both cannot govern. If water scarcity is already pushing hyperscalers to closed-loop designs at their own expense (Contrarian, citing Oracle; Technology-Scout on AI density), then "the market will always argue yes [to evaporative]" is overstated — the market is partially self-correcting on exactly this axis. The draft never reconciles. The honest synthesis is available in the Technology-Scout brief: "waterless" dry cooling still rejects the full heat load as an invisible thermal plume and burns 25–35% more power, so the trend solves the *water* fight and the *visible* plume without eliminating the thermal column or the generation scenario.
- **Recommendation:** Add two sentences making the reconciliation explicit. It converts an apparent contradiction into a sharper point: even the de-risking trend leaves the two risks the screen actually targets — islanded generation and capacity foreclosure — untouched.

## C. Invented or constructed figures

**13. "Several hundred megawatts of heat" — analyst construction, no brief cites it.**
- **Location:** Second paragraph of the opening ("how it rejects several hundred megawatts of heat").
- **Issue:** No brief attributes several hundred MW of heat rejection to a single facility. The Contrarian sizes an AI campus at 150–250 MW; the 345 MW figure is a *generator fleet* at one Colorado campus; 1 GW is the Digital Dulles *master plan across 14 buildings*. "Several hundred megawatts" for the generic data center in the thesis paragraph is a blend presented as fact.
- **Recommendation:** "how it rejects one to two hundred megawatts of heat" (sourced to the Contrarian's campus sizing) or tie the number to the campus-scale figure explicitly.

**14. The Cedar Rapids opening invents scene details the source does not contain.**
- **Location:** Opening paragraph ("Steel up, roof on, cooling plant installed"; "the switchgear was energized").
- **Issue:** The Operations-Analyst brief (citing KCRG) supports: a *completed building*, a request for a temporary certificate of occupancy, and the quoted plume concern. "Cooling plant installed" and "the switchgear was energized" are novelistic dressing with no source. The fact-checker will strike them; better to pre-empt. The scene itself is the right opening — this is the strongest paragraph in the draft — it just needs to be built from what the record supports.
- **Recommendation:** Rebuild the scene from sourced facts: completed building, temporary occupancy request, the airport commission's own history of buying contiguous land "for continued protection of the airport operation" (Ops brief cites The Gazette — a detail the draft skipped that would *strengthen* the irony: this airport was actively banking protective land while the building went up).

**15. "A 20-to-50-year fixed asset" — a splice of two briefs' different numbers.**
- **Location:** Executive Summary point 6 and "The risk you cannot un-build."
- **Issue:** Chief-Engineer says 20–30 years; Airport-CEO says a "30-to-50-year tail" (and elsewhere "30-to-50-year lease"). "20-to-50" is a constructed super-range attributed jointly to both. Small, but it is exactly the kind of derived figure the fact-checker exists to catch.
- **Recommendation:** Pick one sourced formulation ("a 20-to-30-year fixed asset on a lease that can run 50" is defensible from both briefs) or attribute the two figures separately.

## D. Unsupported claims

**16. "It will almost certainly operate, and it will almost certainly be fine" — an unsupported prediction in the closing paragraph.**
- **Location:** Final paragraph.
- **Issue:** No brief supports a probability judgment about the CID facility's future operation or safety; the Ops-Analyst explicitly flags that "operating-history-with-impacts data does not yet exist" for the mid-process cases. The sentence is rhetorically effective and evidentially naked.
- **Recommendation:** Reframe as the honest version: "It will probably operate, under conditions the airport is now negotiating from weakness" — or ground it in the brief's actual point that the mitigation agreement is being written after the concrete cured.

**17. "The tools to run that test exist, are mostly cheap" — supported for plume and wildlife, not for the whole list.**
- **Location:** Thesis paragraph (bold), and "the tools to run it are neither exotic nor expensive" in the rebuttal section.
- **Issue:** MITRE's tool is free and AC 150/5200-33C is deterministic — supported. But the Technology-Scout prices full CFD as "meaningful cost," the Procurement brief prices the full independent study package at 9–15 months, and EMI suites are specialty engagements. "Mostly cheap" is doing quiet work to make the ask look costless. The Procurement brief's honest framing — the burden is real and should sit on the developer — is stronger than pretending the burden is trivial.
- **Recommendation:** "The screening tools are mature and the first-pass tools are free; the full study package is 9 to 15 months of specialist work the developer, not the airport, should fund" — which also tees up item 20.

## E. Missed evidence and missed lenses

**18. The single most vivid piece of plume evidence in the record — a documented 50–60° roll at 550 feet — is never used.**
- **Location:** Absent; belongs in "A geometry test for a machinery problem" or the rebuttal section.
- **Issue:** The Technology-Scout brief documents an aircraft rolled 50–60° off level over cooling towers at ~550 ft AGL. The draft argues turbulence hazard entirely from guidance documents and thresholds; the one recorded upset in the panel's evidence — the thing that converts "the literature flags" into "this has happened to an airplane" — goes unused. For a piece that opens with a scene, skipping the only aviation scene in the evidence is a strange choice.
- **Recommendation:** Deploy it once, precisely, with the honesty caveat that it involved power-station cooling towers, not a data center — which slots perfectly into the "the chiller yard becomes the smokestack" argument.

**19. The run file demands documented airport examples; the draft delivers one and a half.**
- **Location:** Whole draft; run-file success criterion "Airport examples: Find documented data centers located on or near airports... For each, describe its location relative to flight operations, approval process, safeguards, operating history, and any reported impacts."
- **Issue:** CID gets full treatment; Digital Dulles gets the deal history. The panel documented at least four more: **Inyokern** (an airport formally demanding exactly the study bundle the thesis proposes — plumes, EMI, glare, lighting, wildlife — before approval; the closest thing to the draft's screen already existing in the wild), **Manassas HEF** (data-center rezoning colliding with a runway-extension program on the same parcels — the capacity-foreclosure thesis in miniature), **DFW Building F** (an on-airport data center that went through obstruction evaluation, sited lateral to the runway, no reported impacts — the *successful* case the draft needs for balance), and **KCI/Kestrel** (a 380-acre campus underway next to a hub). Omitting Inyokern is the worst miss: it is precedent that the screen is practicable, from a single-runway field with far less leverage than MWAA.
- **Recommendation:** Add a compact casebook passage (150–250 words) or a table: site, position relative to flight ops, review applied, outcome. Inyokern and DFW are load-bearing; the others can be single sentences.

**20. The screen never says who runs, funds, or controls the studies — the Procurement brief's central warning.**
- **Location:** "Implications for MWAA," the five-bullet screen.
- **Issue:** The Procurement brief is blunt: studies must be "airport-funded and airport-controlled, or developer-funded and performed by an airport-selected, airport-directed consultant... the developer's CFD model will find compatibility." The draft's screen lists five studies and is silent on governance — which means the screen as published permits developer-marked homework, the exact failure mode the thesis exists to prevent. The brief also flags that AIP funding of enabling work triggers Brooks Act QBS and the federal flow-downs — a funding decision that should be made up front.
- **Recommendation:** One added bullet: developer-funded, airport-directed, with the consultant selected by MWAA; note the AIP-funding trigger in a clause.

**21. The Chief-Engineer's causal chain — interconnection delay is *why* backup becomes primary — is missing from the section that needs it most.**
- **Location:** "The wrong day," third paragraph.
- **Issue:** The draft cites the DEQ run-hour variance trend but not its mechanism. The Chief-Engineer supplies it: 160-week transformer lead times, 36–60-month substation builds, 7-year Northern Virginia interconnection waits — "the grid-delay gap is exactly what converts 'emergency backup' diesel into de-facto primary generation." That is the difference between "regulators might loosen the rules" (speculative-sounding) and "the physics of the supply chain guarantees pressure to loosen them" (structural). It also connects to Virtual-Chris's interconnection-as-leverage point in the MWAA section, tightening the whole piece.
- **Recommendation:** Two sentences in "The wrong day" carrying the lead-time numbers and the causal claim, cited to the Chief-Engineer.

**22. The quarter-acre/5,000-foot impoundment rule — the reg analyst's "one plume-adjacent risk that already has a codified number" — is dropped.**
- **Location:** "The risk with a number: wildlife and water."
- **Issue:** The section's whole argument is that wildlife is the risk with an enforceable number, and it then omits the most enforceable number in the record: AC 150/5200-33C bars new water impoundments of ≥¼ acre within a runway approach and within 5,000 ft of a runway end (Regulatory-Political brief). The 10,000-ft and 5-mile figures used are separation *guidance*; the ¼-acre bar is the bright line.
- **Recommendation:** Add it. It is one sentence and it is the sharpest tooth in the section.

## F. Rhetoric and prose

**23. Pattern tics: the "not X; it is Y" construction, triads, and imperative asides are over-deployed.**
- **Location:** Throughout. Representative: "That is the plume, the smoke, and the fire call that matter" (triad); "the pond, the roof, and the permanence" (triad); "Read that sequence again" and "Name the cost honestly" (imperative asides); "The controlling risk is not the steam wisp... it is the process plant"; "That is a market-design problem, not a physics problem"; "not a best-practice nicety... it is the mechanism"; "not a bonus argument; it is the last enforceable one" — the not-X-but-Y machine runs a dozen-plus times.
- **Issue:** Individually these are fine sentences; at this density they read as a manner, and the manner reads as machine. The Matt-Levine register the run file asks for gets its effects from specificity and dry asides, not from repeated antithesis. The draft's best moments (the Cedar Rapids opening, "the hazard column clears the building," the grain of the MWAA section) don't use the construction at all.
- **Recommendation:** Keep the two or three strongest antitheses (the thesis paragraph earns one; the §743 section earns one) and rewrite the rest as plain declaratives. Cut "Read that sequence again." Retire at least half the triads.

**24. The Executive Summary is ~750 words against a ~1,100-word spec, and it front-runs the essay's best material.**
- **Location:** Executive Summary; run-file length spec.
- **Issue:** Two problems. First, it is roughly 350 words short of the spec — room that items 4, 10, and 19 could productively fill (the emergency-response rebuttal, the multi-envelope scenario point, and one sentence on the casebook). Second, its eight points are compressed versions of the body's eight sections, with the same quotes ("materially impacts the safe and efficient operation of aircraft" appears three times in the document) — so a reader who starts with the summary experiences the body as reruns. Minor inconsistency within it: point 4 says wildlife "should anchor any screen," but the published screen anchors on the capacity finding as its pass/fail item. Both can be true (most-enforceable vs. non-mitigable) but the draft doesn't say how.
- **Recommendation:** Expand toward spec with the missing material rather than more restatement; vary the load-bearing quotes between summary and body; add half a sentence distinguishing "anchor" (hardest to rebut at a zoning board = wildlife) from "governing criterion" (non-mitigable = capacity).

---

## Priority order for revision

1. Items **1–4** (contradictions the piece cannot ship with).
2. Items **6–12** (number reconciliation — everything the fact-checker will otherwise bounce).
3. Items **18–22** (missed evidence that materially strengthens the argument, especially Inyokern and the upset incident).
4. Items **13–17, 23–24** (precision and prose).

The thesis survives this critique. The draft's core architecture — geometry-vs-machinery, the controlling scenario, the wildlife anchor, irreversibility, the §743 door — is sound and well-evidenced. What does not survive is the pretense that the panel's numbers agree, that MWAA can require what it can only request, and that a screen described as risk-tiered is risk-tiered. Fix those and v2 is publishable.
