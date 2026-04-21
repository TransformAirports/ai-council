# Red Team Critique of Strategist Draft v2

**Agent:** red-team
**Target:** `outputs/stage2/strategist-draft-v2.md`
**Date:** April 17, 2026
**Disposition:** Adversarial quality control. Round two. No diplomacy.
**Note to Strategist:** This is the last critique before v3. The human reviewer sees v3. Prioritize accordingly.

---

## Disposition of v1 issues (in brief)

- **v1 #1 (ROIC/WACC caveat):** Adequately addressed in 2.1 and 3.1. Move on.
- **v1 #2 (1:4.5 ratio / fictional "1:10"):** "1:10" removed. Ratio reframing in 3.5 is honest. Adequate.
- **v1 #3 (A-CDM "not an AI project"):** Withdrawn and engaged honestly in 5.2.3. Adequate, see new issue #3 below.
- **v1 #4 ("supermajority"):** Withdrawn. Replaced with five-condition test in 5.2.6. Mostly adequate, see new issue #4.
- **v1 #5 (Contrarian Scenarios 1–3 ignored):** Scenario 2 pulled in at 3.3, Scenario 4 still cited at 5.2.1. Scenarios 1 and 3 still under-engaged.
- **v1 #6 (DCA constraint mischaracterized):** Constraint A / Constraint B split in 6.1 is good. Adequate.
- **v1 #7 ("5.6x" assumes prior cycle was sized correctly):** Acknowledged at 3.7. Adequate but see new issue #7.
- **v1 #8 (Section 6 was vague):** Materially better. New envelopes and KPIs introduced — but they create their own problems. See new issues #1, #2, #5.
- **v1 #9 (A-CDM network-effect caveat missing):** Added at 3.4. Adequate.
- **v1 #10 ("embarrassing" line):** Cut and rewritten at 3.8. Adequate.
- **v1 #11 (induced demand cuts both ways):** Engaged at 3.6. Adequate but see new issue #6.
- **v1 #12 ("physics do not negotiate" attribution):** Now quoted with attribution in 4.1. Adequate.
- **v1 #13 (Assaia caveat not transmitted):** Caveat now transmitted in 3.8 and 6.2. Adequate.
- **v1 #14 (SEA case unanswered):** Engaged head-on in 5.2.2. Adequate as rebuttal, but see new issue #8.
- **v1 #15 (T5-class governance vague):** Honest move at 6.4 — concedes T5 specifics aren't in the briefs and substitutes a constructed list. Adequate.
- **v1 #16 (Sec 5 weaker than Sec 4):** Reordered, NextGen rebuttal now leads. Adequate.
- **v1 #17 (Exec summary missed optionality):** Added as bullet 7. Adequate.
- **v1 #18 ("roughly" overuse):** Mostly cleaned up. Adequate.
- **v1 #19 (Heathrow TBS / runway lesson incomplete):** Honest acknowledgment in 3.4. Adequate.
- **v1 #20 (thesis slips between sections):** v2 explicitly tries to hold one thesis (defeat test on the discretionary tranche). Adequate at 6.6 — but see new issue #1.

The v1 critique was largely respected. The work below identifies what is still wrong, what the revision broke, and where new claims have been introduced that do not survive scrutiny.

---

## NEW ISSUES IN v2 — RANKED BY IMPORT

## 1. The new dollar envelopes ($25–60M, $30–75M, $20–50M, $55–135M, $100M–$150M) are not in the briefs and the citation is misleading

- **Location:** Sections 6.1 (DCA stack at $25–60M), 6.2 (IAD stack at $30–75M), 6.3 ($55–135M coupled total, restated as "$100M–$150M of operational intelligence" in the closing paragraph), 6.5 (APOC at $20–50M).
- **Issue:** The Strategist cites the Technology Scout brief for these envelopes — specifically: *"plus 10–20% annual recurring [Technology Scout brief, Evidence: Digital Twins, which sets that envelope at the large-hub level]."* But the Technology Scout brief's *only* large-hub envelope is for **digital twin deployments** ($15–40M over 24–36 months). It is not an envelope for the four-category stack the Strategist assembles (queue prediction + biometrics + computer-vision turnaround + data backbone). There is no brief-anchored cost figure for an integrated A-CDM + DMAN + surface metering + APOC stack at a US large hub. The Strategist has bottom-up-estimated these envelopes by analyst inference, then attached citations as if the briefs supported the numbers. They do not.
- **Compounding problem:** the envelope drifts across sections. 6.3 says the system-level coupled investment is $55–135M. The closing paragraph at line 382 says "$100M–$150M of operational intelligence" — a different range. Add 6.5's APOC envelope of $20–50M and you get $75–185M total. The reader cannot reconcile these numbers, and the Strategist does not show the math.
- **Why this matters most:** Section 6 is what the human reviewer (and any MWAA board member) will scrutinize hardest. Specific dollar envelopes that look brief-cited but are not will destroy the document's credibility on first audit. SEA was *the* cautionary case in the briefs, and SEA itself was a $13.4M "integrated stack" that ballooned. The Strategist is now proposing 2–10x SEA's spend with envelope ranges presented as if anchored.
- **Recommendation:** Either (a) explicitly mark the envelopes as analyst-derived bottom-up estimates and show the construction (digital twin component + A-CDM component + surface metering component + APOC component, each with a citation), or (b) drop the dollar envelopes and replace with "low tens of millions to low nine figures, sized against the Technology Scout's component-level benchmarks." Reconcile 6.3's $55–135M with the closing paragraph's $100M–$150M. One number, defended once.

## 2. The DCA defeat test is not actually a defeat test

- **Location:** Section 6.1, defeat-test bullet.
- **Issue:** *"If after 24 months the deployed stack has not produced a statistically significant, disclosed-methodology, published reduction in at least two of the four KPIs, the authority pauses further operational-intelligence investment at DCA and commissions an independent post-mortem before committing additional capital."* This defeat test only stops *future operational intelligence* investment. It does not say what happens to the $2.4B Project Journey program. The thesis of the entire paper is that operational intelligence applied first should compress, defer, or resize the physical project. But the defeat test in 6.1 makes Project Journey unconditional and the operational intelligence investment the only thing under threat. That inverts the thesis. If operational intelligence at DCA delivers, what is resized? If it does not deliver, what is rebuilt? Neither question is answered.
- **Compounding:** Section 6.1 itself notes Project Journey is "a response to Constraint A, not Constraint B" — i.e., it handles passengers for the flights DCA is *already allowed* to operate. So 6.1 has effectively conceded that Project Journey is a non-discretionary throughput-per-passenger investment. Then the operational intelligence "complement" is a complement to a non-discretionary project. The defeat test cannot do work in that framing.
- **Recommendation:** Either (a) acknowledge that Project Journey at DCA is in the non-discretionary tranche and the defeat test does not apply — DCA is the wrong place to host the thesis's flagship example — or (b) identify which sub-element of Project Journey is discretionary (gate count beyond what the slot cap requires? hold-room expansion? specific concession build-out?) and apply the defeat test to that sub-element, not to "further operational-intelligence investment." Otherwise the defeat test is a defeat test only of the smaller investment, which is exactly the opposite of what the thesis requires.

## 3. The IAD defeat test fires the wrong way and may incentivize underperformance

- **Location:** Section 6.2, defeat-test bullet.
- **Issue:** *"If A-CDM + surface metering + turnaround monitoring at IAD move the peak-hour-movement KPI and the taxi-out KPI by measured amounts within 24 months, the demand-contingent Concourse E tranche is resized and rescheduled based on the higher baseline. If they do not move, the demand-contingent tranche proceeds on original terms — with the operational-intelligence program paused for independent review."* The Strategist intends this as an honest two-way decision. Read carefully, though, it creates a perverse incentive: the *only* outcome under which the Concourse E tranche proceeds *unmodified* is if operational intelligence fails. Anyone whose career or contract depends on Concourse E proceeding has a soft incentive to see operational intelligence fail. The Strategist's own thesis warns against this kind of governance pathology.
- **Second problem:** "By measured amounts" is undefined. How much movement triggers a resize? Munich's 9% taxi-out reduction? 5%? Any statistically significant change? The defeat test is not testable as written.
- **Recommendation:** Pre-register the threshold (e.g., "if taxi-out median falls by ≥7% sustained over six consecutive months"), and pre-register the resize formula (e.g., "demand-contingent gate count reduced proportionally to the throughput improvement"). Also: name the third party that adjudicates the defeat test, because the airport authority cannot be both player and referee.

## 4. The five-condition replacement for "supermajority" still does not enumerate which US hubs meet the conditions

- **Location:** Section 5.2.6, final paragraph.
- **Issue:** The Strategist replaced "supermajority" with five conditions (a)–(e) and then writes: *"Multiple US large hubs meet most of those conditions; neither brief enumerates exactly how many."* This is more honest than v1, but it is still hand-waving. The Red Team in v1 specifically asked the Strategist to *identify which US large hubs meet the conditions and which do not, then say so.* V2 declined to do that work. The result: the thesis applies to "multiple" hubs, count unspecified, identity unspecified. A skeptical board member reads this and asks "name three." The Strategist cannot answer from the briefs as written, but a small amount of analyst work could: ATL, MCO, IAH, MSP, DTW, PHX, SEA, BOS, MIA — most of which are not at 90%+ peak utilization, all of which have published delay attribution data, several of which have the financial stress described.
- **Recommendation:** Name three to five specific US large hubs that demonstrably meet most of the five conditions, with a one-line citation each (FAA OPSNET, BTS data, debt filings). If the briefs do not support this, say "the test would need to be applied airport-by-airport; the authors have not done that exercise outside MWAA." But do not leave "multiple" as the sole quantifier in a paper whose thesis is about applicability.

## 5. The A-CDM network-effect caveat is acknowledged but the IAD recommendation ignores it

- **Location:** Section 3.4 (caveat acknowledged) vs. Section 6.2 (IAD A-CDM recommended in single-airport isolation).
- **Issue:** Section 3.4 transmits the Technology Scout's caveat that *"the marginal benefit of adding one more airport decreases as the network penetration increases"* and that *"a US A-CDM deployment at a single airport is a more isolated intervention than the European benchmarks imply."* Section 6.2 then recommends A-CDM at IAD as if Munich-class numbers (9% taxi reduction, 7.8% off-block predictability) are the appropriate benchmark — but Munich was inside the European A-CDM network. A US-isolated IAD A-CDM deployment is more analogous to nothing in the brief evidence base. The Strategist hedges with "a pre-registered acceptance criterion (e.g., the Munich single-airport benchmark is the floor; the 17-airport network benchmark is not)" but Munich was not actually a single-airport deployment in isolation. The benchmark is misappropriated.
- **Recommendation:** Either (a) downscope IAD's A-CDM ambition explicitly — the realistic benchmark for an isolated US A-CDM deployment is "below Munich," with no published independent floor, and the defeat test should reflect that uncertainty by lowering the trigger threshold; or (b) recommend that MWAA pursue A-CDM at *both* DCA and IAD (and lobby for a regional cluster including BWI) so that the network-effect caveat is partially mitigated, then justify the larger investment envelope. Pick one. Right now the v2 draft has Munich as the benchmark in the KPI bullet and the network caveat in the "risk" bullet without resolving the contradiction.

## 6. The 34-of-55 (62%) framing of the runway-expansion data is still selective

- **Location:** Section 3.6, paragraph 2 and Section 2 bullet 5.
- **Issue:** The Strategist now writes *"That is 34 of 55 cases (62%) where the expansion either was unnecessary on its pre-construction justification or did not hold its post-construction justification."* But 15 + 19 = 34 only if the two groups do not overlap, and the Operations brief does not state that they are non-overlapping subsets. Re-read Operations Finding 5: "15 [of 55] were operating peak hours below 90% of their pre-expansion (pre-construction) capacity — meaning expansion was entirely unnecessary for them. And 19 expanded airports were already operating at 90%+ of their new post-expansion capacity within a decade." These are two different test conditions on the same 55-airport population. An airport could plausibly be in both groups (operating below pre-expansion peak average but having a peak-hour spike at 90% of post-expansion capacity), or neither. The arithmetic 15 + 19 = 34 requires an unstated mutual-exclusivity assumption.
- **Recommendation:** Either source mutual exclusivity from the Bilotkach/Mueller study directly (which neither the Strategist nor the Operations brief has done) or restate as "15 of 55 had expansion that was unnecessary on its own terms; a separate 19 of 55 re-congested within a decade; the two groups may overlap." Then drop the 62% headline. The induced-demand argument from v1 #11 is engaged elsewhere (3.6 paragraph 1) — but the headline number does not get to combine the two test populations without disclosure.

## 7. The "discretionary tranche" is the load-bearing concept and is never defined

- **Location:** Sections 1, 2 bullet 6, 3.7, 3.10, 4.8, 5.3, 6.6.
- **Issue:** The thesis now turns entirely on a binary distinction between "mandatory/non-discretionary" (safety, PCI pavement, code compliance, asset renewal, irreducible physical overload) and "discretionary" (capacity-growth, demand-contingent, passenger-experience). The Strategist invokes this distinction at least eight times. It is *never* operationalized. Specifically: (a) what fraction of MWAA's $9B program is discretionary by this definition? (b) Of Project Journey's $2.4B, what is discretionary? Section 6.1 implies *all* of Project Journey is non-discretionary (Constraint A response). Of Concourse E, what is discretionary? Section 6.2 splits it into "high-confidence core" and "demand-contingent" but does not size either. (c) Of the $151B ACI-NA need, the Strategist says "more than 50%" of AIP funding is pavement, and Contrarian Part II calls "primarily" the $151B mandatory — the Strategist now relies on this without quantifying.
- **Why this matters:** if the discretionary tranche is 5% of the $9B (~$450M), the entire defeat-test recommendation is a tail-of-the-tail allocation question. If it is 50% (~$4.5B), it is the dominant capital decision facing the authority. The reader cannot tell, and the Strategist has now made the entire thesis hinge on a number nobody has computed.
- **Recommendation:** Either (a) provide an order-of-magnitude estimate of the discretionary portion of MWAA's $9B (even a wide range — $1–3B — would be honest), with construction shown, or (b) acknowledge explicitly that quantifying the discretionary portion is a Stage 3 / fact-checker task and pre-register the criteria. The current draft pretends the distinction is operational when it has not been operationalized once.

## 8. The SEA rebuttal works as a critique of architecture but smuggles in an unfalsifiable claim

- **Location:** Section 5.2.2, second paragraph.
- **Issue:** *"'No published performance outcome' is not the same as 'no performance outcome.' It is consistent with the Tech Scout's broader finding that US airports deploy without publishing... SEA's failure is a disclosure failure as much as an operational failure."* This is rhetorically clever and almost certainly partly true, but it cannot be verified from the briefs and it functions as an unfalsifiable defense. By the same logic, a future MWAA operational intelligence deployment that fails to publish results could be characterized as "a disclosure failure, not an operational failure." That is exactly the move the Strategist is criticizing the vendor community for in 4.5. The argument cuts both ways.
- **Recommendation:** Either (a) drop the "disclosure failure" framing and rest the SEA rebuttal entirely on the architecture point (which is sufficient and well-defended in paragraphs 1 and 3), or (b) explicitly concede that the disclosure-failure interpretation is speculative and that SEA must be assumed to have produced no measurable improvement until proven otherwise — which strengthens the architecture argument in paragraph 3 by making it the *only* available rebuttal.

## 9. Section 5.2.3's Gartner counterpunch overstates what the Tech Scout's credibility hierarchy implies

- **Location:** Section 5.2.3, paragraph 2.
- **Issue:** *"A responsible airport that buys from tier 1 and disciplines tier 2 with aggressive discounting is not drawing randomly from the Gartner denominator."* This requires that "tier 1 vs. Gartner-denominator" mapping be valid. The Technology Scout's credibility hierarchy classifies *evidence sources* (EUROCONTROL audits vs. vendor case studies). It does not classify *projects*. An airport that *buys* A-CDM is not buying from EUROCONTROL — it is buying a deployment from Frequentis, Indra, or Thales. Whether that deployment succeeds depends on local data quality, organizational change, and integration — exactly the failure modes the Gartner data measures. So an airport "buying from tier 1" in the Tech Scout's sense is still subject to the Gartner base rate. The Strategist has conflated source credibility with project success rate.
- **Recommendation:** Reframe: "EUROCONTROL evidence shows that *successfully deployed* A-CDM produces audited fuel and delay savings. It does not show that *attempts* to deploy A-CDM at a new airport succeed at higher than the Gartner base rate." Then make the portfolio argument (lead with categories with the strongest deployment track record) without claiming immunity from the base rate. The current 5.2.3 claims more than the evidence supports.

## 10. The 4.7 demand-growth concession is conceded too cheaply, then re-attacked in 5.3

- **Location:** Section 4.7 (concedes growth) vs. Section 5.3 (attacks "the assumption that demand growth is physical").
- **Issue:** Section 4.7 presents the Contrarian's demand-growth argument as one of nine pillars and lets it stand. Section 5.3 then says *"Do not concede... the assumption that demand growth is physical when 39% of delay minutes come from late-arriving aircraft and 40% of NAS delays come from 19 understaffed ATC facilities."* But "demand growth is physical" is not the same claim as "current delay attribution is physical." The Contrarian's IATA / FAA forecasts (1.28B US enplanements by 2038, 7.8B global by 2036) are forecasts of *future* demand — they are not refuted by *current* delay attribution. The Strategist has conflated two distinct questions. A skilled Contrarian would press the gap.
- **Recommendation:** In 5.3, distinguish: (a) current delay attribution is dominated by coordination, staffing, and weather — true, and refutes the framing that current delay justifies new physical capacity; (b) future demand forecasts may or may not be physical — this is an open question that depends on hub strategy, fuel cost, post-pandemic patterns, and is outside the brief evidence base. Concede (b) explicitly. The thesis is robust to that concession. Trying to slip past it is a vulnerability.

## 11. "The discretionary tranche should be defeat-tested" is the entire thesis, but no defeat test in Section 6 actually tests the discretionary tranche

- **Location:** Sections 6.1, 6.2, 6.5.
- **Issue:** Triangulating the previous issues: 6.1's defeat test only threatens the operational intelligence investment, not Project Journey. 6.2's defeat test is the cleanest two-way test in the document but is qualitatively defined ("by measured amounts") and creates a perverse incentive. 6.5's APOC defeat test only defers the APOC facility — the operational intelligence program is "reviewed," but no infrastructure consequence is named. The composite: not one defeat test in Section 6 conditions an *infrastructure* decision on an operational intelligence outcome. The thesis ("discretionary tranche should have to clear a defeat test") is not implemented anywhere in the implementation section.
- **Why this matters most after issue #1:** the v1 critique flagged Section 6 as the weakest. v2 added specifics. The specifics, examined closely, do not implement the thesis. This is the single biggest gap between what the paper says and what it actually proposes.
- **Recommendation:** Pick one specific MWAA capital line item — sub-element of Project Journey, sub-element of Concourse E, or some other identified discretionary spend — and write a defeat test in which the operational intelligence outcome resizes, defers, or cancels that infrastructure spend. Without that, the implementation section is a recommendation to do operational intelligence *in addition to* infrastructure, not *as a test of* infrastructure. That is a different — and weaker — paper.

## 12. The "$100M–$150M" closing flourish breaks the previously established envelopes

- **Location:** Final paragraph, line 382.
- **Issue:** *"It should be built knowing what $100M–$150M of operational intelligence would have done first."* But Section 6.3's coupled DCA + IAD envelope is $55–135M, and 6.5's APOC adds $20–50M (combined across both airports). $55M + $20M = $75M (low) and $135M + $50M = $185M (high). Where does $100M–$150M come from? The Strategist appears to be picking a midpoint that sounds round, without showing the construction. A skeptical reader who has been tracking the envelopes through Section 6 will catch this immediately.
- **Recommendation:** Reconcile to the explicit Section 6 sums. If the closing should reflect a midpoint, say "approximately $75M–$185M" or "on the order of $100M." Do not introduce a fourth dollar range in the closing line.

## 13. The Heathrow A-CDM "50% reduction in departure delays" claim disappeared between v1 and v2 — good, but the Operations brief still has it

- **Location:** Section 3.4 vs. Operations brief Finding 8.
- **Issue:** This is a positive observation rather than a critique: the v1 draft cited Heathrow's 50% departure delay reduction; v2 quietly drops it in favor of the EUROCONTROL 17-airport network number. That is the right move — the 50% figure was vendor-adjacent and the EUROCONTROL number is independently audited. The Strategist should be credited for this self-correction.
- **Recommendation:** No action needed. Note for v3 that this restraint should be preserved.

## 14. Section 6.2's "exact sub-project cost is not disclosed at brief-level granularity; Authority filings should govern the number" is honest but punts

- **Location:** Section 6.2, first specific bullet.
- **Issue:** The Strategist concedes brief-level data does not give a Concourse E figure. Honest. But the rest of 6.2 then proposes to size operational intelligence as a fraction of Concourse E — without a Concourse E number. The math the Strategist wants to make ("a fraction of any single major Concourse E sub-project") cannot be made.
- **Recommendation:** Either (a) cite the WJLA source the Economist brief uses ($9 billion authority-wide contract, with Concourse E and DCA Project Journey both included) and back into a Concourse E sub-allocation, or (b) drop the percentage-of-Concourse-E framing in 6.2 and present the operational intelligence envelope on its own absolute terms. The current text gestures at a ratio it cannot compute.

## 15. "Fact-checker verification against source briefs to follow" is a flag the human reviewer will read literally

- **Location:** Final line, footer.
- **Issue:** The closing footer says *"Fact-checker verification against source briefs to follow."* This signals to the reviewer that the draft has not yet been fact-checked. Several of the issues above (envelope arithmetic, the 34-of-55 computation, the $100M–$150M figure, the Munich benchmark misappropriation) are fact-checker findings the Strategist could catch before v3. Ideally the v3 draft *is* fact-checked, and the footer says so.
- **Recommendation:** Resolve the fact-checker pass before v3 ships, and remove or update the footer. Otherwise the reviewer will find these issues anyway and ask why they were not addressed.

---

## Pattern summary for v2

**What v2 fixed well:** ROIC verification caveat, IT ratio honesty, NextGen rebuttal sequencing, T5 governance honesty (admitting the briefs do not support the phrase), Heathrow runway honesty, Assaia caveat transmission, SEA engagement at the architecture level, removal of the fabricated "1:10" and "supermajority" numbers, the optionality framing.

**What v2 broke or did not finish:**

1. **Section 6 dollar envelopes look brief-cited but are not.** This is the single biggest credibility risk in v3. The Strategist did the right thing by adding specifics, but the specifics over-attribute their sourcing.
2. **The defeat tests in Section 6 do not actually test the thesis.** They threaten the operational intelligence investment, not the discretionary infrastructure tranche. This is the single biggest *substantive* gap.
3. **"Discretionary tranche" is the load-bearing concept and is never sized.** The whole paper hinges on this distinction and the reader cannot tell whether it applies to 5% or 50% of MWAA's $9B.

**What v2 still does not engage:** specific US large-hub examples (#4), Contrarian Scenarios 1 and 3 (still unaddressed), the Bilotkach/Mueller mutual-exclusivity question (#6), and the Munich-vs-isolated-deployment benchmark conflict (#5).

**Overall judgment:** v2 is **substantially stronger** than v1 on rhetoric, citation discipline, structural balance, and on engaging the strongest counter-arguments (NextGen, SEA, Heathrow). v2 is **weaker than v1 in one important respect**: by adding specific dollar envelopes and defeat tests in Section 6, the Strategist has introduced concrete claims that do not survive scrutiny, where v1's vagueness was at least not disprovable. The fix is straightforward — make the envelopes traceable, and write at least one defeat test that actually conditions an infrastructure decision — but if it is not made before v3, the human reviewer will see specifics that look stronger than they are.

**Top three issues to fix before v3:**
1. **Issue #1 (envelope sourcing).** Either show the bottom-up construction with component-level citations, or mark the envelopes explicitly as analyst-derived.
2. **Issue #11 (defeat tests do not test the thesis).** At least one defeat test in Section 6 must condition an infrastructure decision on an operational intelligence outcome. Otherwise the implementation section does not implement the thesis.
3. **Issue #7 (discretionary tranche unsized).** Provide a wide-range estimate of what fraction of MWAA's $9B is discretionary by the paper's own definition. Without this, the thesis is unfalsifiable in scope.

Everything else is fixable in a paragraph.
