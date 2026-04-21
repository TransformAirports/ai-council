# Red Team Critique of Strategist Draft v1

**Agent:** red-team
**Target:** `outputs/stage2/strategist-draft-v1.md`
**Date:** April 17, 2026
**Disposition:** Adversarial quality control. No diplomacy.

---

## 1. Misstates ACI's own claim about ROIC vs. WACC

- **Location:** Section 2, bullet 1; Section 3.1, opening paragraph.
- **Issue:** The draft writes: *"ACI World's own 2024 figure puts global airport return on invested capital at 6.3% — below the sector's weighted average cost of capital"* and *"ACI itself concedes that this figure remains below the sector's weighted average cost of capital."* The Economist brief's actual quotable (Quotable 1) reads that ROIC "rose to 6.3% in 2024, which remains below the sector's weighted average cost of capital." The Economist's own caveat (Section 3, Caveats) states: *"The precise 2023 ROIC figure and regional breakdowns could not be independently verified against the primary report."* Most of the ROIC/WACC data in the brief is drawn from ACI press releases and third-party coverage — not the primary ACI report. The Strategist presents it as a verified structural finding.
- **Recommendation:** Soft-flag the ROIC/WACC framing. Add one sentence acknowledging that the precise ACI figure is not independently verifiable and that the Economist brief flagged this as a data access limitation. Do not let a single, unverified press-release number carry the entire opening thesis.

## 2. The 1:4.5 IT-to-CapEx ratio is misread and overextended

- **Location:** Section 3.5 (entire section); Section 3.10 final paragraph.
- **Issue:** The draft argues the "roughly 1:4.5 IT-to-CapEx globally, and closer to 1:10 or worse at many large US hubs" is "the wrong ratio." But the Economist brief compares **$8.9B global airport IT spend** against **$40B annual global airport capital costs** — that is total IT (cybersecurity, passenger processing, payroll systems, cloud, networking, back-office) against physical CapEx. The overwhelming majority of that $8.9B is NOT operational intelligence in the sense the Strategist argues for. Per the Technology Scout taxonomy, operational intelligence is a narrow slice (A-CDM, DMAN, computer-vision turnaround, queue prediction, APOC). The "1:4.5" ratio is apples-to-oranges, and the "1:10 at large US hubs" figure is nowhere in the briefs — it is invented.
- **Recommendation:** Drop the "1:10" claim entirely unless it can be sourced. Reframe the ratio argument to compare CapEx against the operational-intelligence subset of IT spend (which would make the asymmetry even starker, but honestly). Flag that SITA's survey identifies cybersecurity as the #1 IT priority at 100% of respondents — i.e., most of the $8.9B is not buying A-CDM.

## 3. Unsupported assertion that A-CDM "is not an AI project"

- **Location:** Section 5.2.2, paragraph 2.
- **Issue:** The draft asserts *"A-CDM is not an AI project in the Gartner sense. It is a deterministic information-sharing and sequencing protocol. TBS is not an AI project. RECAT is not an AI project at all."* This is a rhetorically convenient redefinition. It lets the Strategist dodge the Gartner 28%-success base rate from the Contrarian brief by simply redefining the recommended technologies out of the denominator. The Technology Scout brief never explicitly endorses this taxonomy. The Contrarian can (and will) rebut: you do not get to recommend $100M+ of "operational intelligence" and then claim the "AI projects fail at scale" base rate does not apply.
- **Recommendation:** Either (a) concede that some of the recommended investments do fall under the Gartner denominator and argue separately about why their success rate is higher, or (b) provide an independent industry source — not a strategist assertion — that treats A-CDM/TBS/RECAT as categorically distinct from AI projects. Right now it reads as special pleading.

## 4. "Supermajority of US large-hub system" is unsourced

- **Location:** Section 5.2.6, final paragraph.
- **Issue:** The draft claims the stated conditions "describe a supermajority of the US large-hub system." Nothing in any Stage 1 brief supports a quantified majority/supermajority claim. The Operations brief describes a pattern across 55 airports globally (not US large hubs specifically), and the Technology Scout brief notes 3 of 31 US large hubs have digital twins. Neither brief enumerates what fraction of US large hubs meet all five stated conditions.
- **Recommendation:** Replace "supermajority" with specific examples, or drop the quantifier and say "many US large-hub airports." Or — preferably — identify which US large hubs meet the five conditions and which do not, then say so. "Supermajority" is the kind of weak rhetoric this critique is supposed to flag.

## 5. Cherry-picks Contrarian's Scenario 4 concession but ignores Scenarios 1–3

- **Location:** Section 5.2.1, last paragraph.
- **Issue:** The Strategist quotes the Contrarian's Scenario 4 ("the software has improved") concession as leverage, but the Contrarian brief lists **four** scenarios where the pro-infrastructure thesis is wrong — (1) underutilized hubs, (2) coordination failures masquerading as capacity failures, (3) greenfield in unconstrained markets, (4) software has improved. Scenarios 1–3 are the *stronger* concessions from the Contrarian, and they map directly onto the Strategist's own thesis. By only citing Scenario 4, the Strategist leaves the Contrarian's most helpful concessions on the table.
- **Recommendation:** Pull Scenarios 1 and 2 into Section 5. They explicitly concede that delay-as-coordination-failure is real and that optimization dominates at underutilized hubs — exactly the Strategist's thesis.

## 6. DCA slot cap number is wrong

- **Location:** Section 6.1, paragraph 1.
- **Issue:** The Contrarian brief states DCA's slot cap is **"62 takeoffs or landings per hour maximum"** (Part II, DCA section). The draft says DCA "has FAA slot caps and perimeter rules preventing additional movements" without giving the number. That is fine. But Section 4.1 earlier notes DCA handles 25M on infrastructure designed for 15M and cites the Contrarian. The Contrarian's original assertion is that DCA is at a hard cap with no more flights possible — the Strategist's framing in 6.1 as a "paradigm case of physical constraint" is correct but then the draft pivots to argue DCA's binding constraint is "the slot cap" not the terminal. That slot cap is federal policy, not physical. This is a distinction the Contrarian would press hard: a policy-imposed cap can theoretically be lifted; a river cannot be moved. The Strategist's argument that "throughput-per-passenger" is where operational intelligence wins is fine, but it relies on mischaracterizing DCA's constraint type.
- **Recommendation:** Clarify DCA's nested constraints: FAA policy (slot cap, perimeter rule) plus physical geography (Potomac, federal facilities). The terminal overload is a distinct problem from the movements cap. The argument for operational intelligence at DCA is about passenger processing throughput downstream of a fixed flight count — make that mechanism explicit.

## 7. "5.6x step-up" implies the prior cycle was sized correctly

- **Location:** Sections 2 (bullet 6), 3.7, 6.3, 6.4.
- **Issue:** The draft repeatedly uses "5.6x step-up in capital program scope" as evidence of danger. But it does not question whether the **prior** $1.6B program was adequate, under-invested, or reflective of a period when MWAA was deferring maintenance. If the 2015–2024 cycle was structurally under-funded (and safety/depreciation needs compounded), then the 5.6x comparison is misleading — the current program may be partially catching up on deferred work. The Contrarian's asset-depreciation argument (Part II) is directly relevant here and the Strategist does not engage it.
- **Recommendation:** Acknowledge that some fraction of the 5.6x is catch-up on deferred asset renewal, which the Contrarian's $151B backlog / PCI / mandatory compliance argument supports. Then show that even after netting out that fraction, the remaining discretionary capital still faces the allocation question.

## 8. Vague hedging throughout the MWAA section

- **Location:** Section 6 (all subsections).
- **Issue:** Section 6 is the section the reader cares most about, and it is the weakest in the draft. It is full of soft verbs and vague qualifiers: "should be coupled with, not serially followed by," "scoped as a first-class program with published before/after metrics," "the organizational, data, and governance architecture," "T5-class governance." What does any of this mean operationally? What specific project? What budget envelope? What KPIs? What is the defeat test? The Strategist's own thesis (Section 3.10) demands that "the next billion dollars should have to prove it belongs on the physical side of that ledger" — but Section 6 never tells MWAA what the proof looks like.
- **Recommendation:** Section 6 needs specifics. For each of DCA, IAD, and the APOC question: (a) name the specific capital item, (b) propose a specific operational-intelligence alternative or complement, (c) state the investment envelope, (d) name the KPI that would validate or defeat the investment, (e) name the decision gate. Without these, Section 6 is the weakest section of the piece and will be the first thing a skeptical MWAA board member challenges.

## 9. Section 3.4 misses the EUROCONTROL caveat on marginal benefit decay

- **Location:** Section 3.4 (A-CDM paragraph).
- **Issue:** The Strategist quotes the EUROCONTROL 34,000 tonnes / 250,000 minutes figure but omits the Technology Scout's caveat in Finding 4: *"the marginal benefit of adding one more airport decreases as the network penetration increases."* That matters for a US airport considering A-CDM today — the European evidence base is compiled from airports that benefit from network effects most US airports cannot replicate. The FAA TFMS is not an A-CDM equivalent (Technology Scout §4), so a US A-CDM deployment is a more isolated intervention.
- **Recommendation:** Add one sentence acknowledging the network-effect caveat and the US ATC architecture gap. Do not let the European headline numbers stand in without that context.

## 10. "Bad operational intelligence investment is embarrassing" is rhetoric, not argument

- **Location:** Section 3.8, final sentence.
- **Issue:** *"A bad operational intelligence investment is embarrassing. A bad concourse is a balance sheet problem for 30 years."* This is clever phrasing that ignores NextGen: a bad operational intelligence program was $15B (combined $35B) and continues to encumber federal budgets. The Strategist does not get to dismiss the balance-sheet consequences of software failure this cheaply, especially when Section 5.2.1 spends pages working to distinguish federal IT from airport IT. At a minimum, the rhetorical punch line undercuts that careful distinction.
- **Recommendation:** Cut the line, or qualify it: "A bad airport-level operational intelligence investment is recoverable in tens of millions and months; a bad concourse is a balance sheet problem for 30 years." Don't concede ground you already defended with more nuance a section later.

## 11. The induced-demand argument cuts both ways and the draft does not notice

- **Location:** Section 3.6.
- **Issue:** The Strategist uses the 55-expansion study to argue that runway expansions don't hold their value. But induced demand is ambiguous evidence: if a capacity expansion induces traffic that fully absorbs the new capacity, that is not a failure — that is service to latent demand that was being rationed. The Contrarian brief's Denver example (82.4M through a 50M-capacity airport) implicitly argues that the induced demand *is* a benefit the airport was previously unable to serve. The Strategist treats re-congestion as a failure mode without establishing the welfare counterfactual.
- **Recommendation:** Either (a) narrow the claim to "expansions whose value depended on the post-expansion capacity being sustained above pre-expansion levels, which in 34/55 cases did not hold," or (b) engage the welfare argument directly — accepted, expansion plus induced demand can be positive-sum if the latent demand is real. Without engaging this, the Contrarian will counter.

## 12. "The physics do not negotiate" rhetoric is borrowed from the Contrarian

- **Location:** Section 4.7 (counter-case presentation).
- **Issue:** Section 4 is labeled "The Counter-Case, Honestly Presented," but it quotes the Contrarian's rhetoric including *"The physics do not negotiate"* verbatim from the Contrarian brief Part I-4 — without flagging this as a direct quotation. This is not plagiarism in the normative sense (the whole section is citing the Contrarian), but the load-bearing rhetorical lines should either be in quotation marks or rephrased. Right now it reads as the Strategist endorsing the Contrarian's framing rather than presenting it.
- **Recommendation:** Put load-bearing phrasings in quotation marks with attribution, or paraphrase. Cleaning this up also clarifies which arguments the Strategist actually concedes versus presents.

## 13. Assaia's "$100 per turnaround per minute" figure is used without its caveat

- **Location:** Section 3.8.
- **Issue:** The draft cites Assaia's $100-per-turnaround-per-minute figure and the 25% median departure delay reduction. But the Technology Scout brief (Finding 3 and Section 6) is emphatic: *"This is vendor-published research drawn from vendor-customer airports. It is not peer-reviewed and has not been independently audited. The sampling methodology (which airports, which flights, how baselines were established) is not disclosed."* The Strategist adds the word "caveated" but that is not the same as transmitting the caveat. The reader does not know the sampling methodology was undisclosed.
- **Recommendation:** Either cite only the Munich SESAR numbers (which the Technology Scout rates as high credibility) or transmit the Assaia caveat explicitly. Consistency: Section 5.2.2 does flag the Technology Scout's cautions about vendor numbers — Section 3.8 should match that discipline.

## 14. No engagement with the SEA $13.4M / zero-metrics case as a risk to the thesis

- **Location:** Sections 3 and 6 (mentioned, but not engaged).
- **Issue:** The Strategist mentions the SEA $13.4M integration project twice — once in 3.4's implicit context and once in 6.1 — but in both places uses it as a cautionary tale about *how* to deploy operational intelligence, not as evidence *against* it. But the Technology Scout brief's Finding 2 quote is damaging: SEA "spent $13.4M integrating seven vendors to get basic ramp situational awareness" with "no published performance outcome." That is a real US operational-intelligence failure case, in the same weight class as the Contrarian's NextGen argument but at the airport level. The Strategist's NextGen rebuttal (5.2.1) argues airport-level operational intelligence is different — but SEA is airport level, and it failed too.
- **Recommendation:** Section 5.2.1 or 5.2.2 needs to address SEA directly. If the rebuttal is "SEA chose the wrong architecture," say so and specify what architecture would have worked. Do not leave SEA as an unanswered US-airport-level data point that contradicts the thesis.

## 15. Heathrow T5 lesson is invoked but the draft never operationalizes it

- **Location:** Sections 2 (bullet 2), 3.2, 5, 6.4.
- **Issue:** T5 is cited three times as a governance counter-case. Section 6.4 says MWAA needs "T5-class governance" but does not define it beyond *"two-year pre-construction discipline, ring-fenced scope, accountable executive ownership with contractual clarity on risk allocation."* That is vague. The Economist brief notes T5 required "a two-year pre-construction study explicitly designed to avoid megaproject failure modes." What is *the actual governance structure*? Was it BAA's risk-transfer approach? A specific contract form? The Strategist keeps invoking T5 without explaining what to copy.
- **Recommendation:** Either dig into T5's specific governance mechanisms (risk sharing, single-point accountability, specific contract structure) or drop it as a specific recommendation and replace with "a governance structure that MWAA would need to design and have independently validated."

## 16. Section 4 is longer and more charitable to the counter-case than Section 5 is to the rebuttal

- **Location:** Structural — Section 4 (~1,400 words) vs. Section 5 (~1,600 words) — but Section 4 is tight and aggressive; Section 5 is defensive and hedges.
- **Issue:** The Strategist's "steelman the counter-case, then refute" structure is the right move, but Section 4 lands punches (NextGen, O'Hare, $151B backlog, CrowdStrike) with concrete numbers and sharp prose. Section 5 spends significant energy conceding (5.1 is 80% concession) and when it finally rebuts (5.2.1–5.2.6), the rebuttals feel like scope-limiting rather than counter-punches. The NextGen rebuttal is the best but even it leans heavily on "these are categorically different" without delivering the positive case for why.
- **Recommendation:** Section 5 needs a tighter, more assertive structure. After conceding what must be conceded in 5.1 (which is fine), 5.2 should lead with the single strongest rebuttal (probably 5.2.1 on NextGen) and then move to weaker-but-sufficient rebuttals. Right now the order buries the best rebuttal under preamble.

## 17. Section 2 Executive Summary omits the opportunity-cost argument that is Section 3.8's payload

- **Location:** Section 2 (Executive Summary bullets).
- **Issue:** The six bullets of the exec summary focus on: (1) ROIC/WACC, (2) overruns, (3) delay cause misattribution, (4) operational gains exist, (5) runway value doesn't hold, (6) MWAA's balance sheet. But Section 3.8's argument — that operational intelligence is *optionable* in ways concrete is not — is arguably the strongest intellectual move in the draft. It does not appear in the summary.
- **Recommendation:** Add a seventh bullet on optionality. The exec summary is what a busy MWAA board member reads. The optionality argument belongs there.

## 18. "Roughly 1:4.5" and "roughly 5.6x" repetition loses force

- **Location:** Sections 2, 3.5, 3.7, 3.10, 6.3 — "roughly" appears 12+ times.
- **Issue:** The draft repeats "roughly" before nearly every ratio. At some point "roughly" stops meaning "approximately" and starts meaning "I have not actually computed this carefully." That is a weakness a skeptical reader will notice.
- **Recommendation:** Replace "roughly" with the actual computation or the source's precision ("5.63x per the Authority's own filings"). If the ratio is approximate, state the precision ("within ±5%"). Otherwise cut the word.

## 19. Missing counter-argument: the Heathrow TBS lesson is incomplete

- **Location:** Sections 3.4, 3.6.
- **Issue:** The Strategist uses Heathrow TBS as a success story for operational intelligence without engaging the Contrarian's Part I-1 framing: Heathrow is at 98% of its movement cap. Yes, TBS delivered gains — but Heathrow is also still pursuing a third runway because TBS's gains were insufficient to meet demand. The infrastructure debate at Heathrow is not closed; it is ongoing *despite* TBS. That undercuts the framing that TBS proved a third runway unnecessary.
- **Recommendation:** Be honest: TBS delivered meaningful capacity; Heathrow is still pursuing the runway anyway. The right claim is that TBS delivered large gains at a fraction of the runway's cost *while* the runway debate proceeded. Do not imply TBS substituted for the runway — it didn't.

## 20. The thesis definition slips between sections

- **Location:** Section 1 vs. Section 3.10 vs. Section 6.6.
- **Issue:** Section 1 says the next billion "should have to clear a bar that current planning frameworks do not ask it to clear." Section 3.10 says "the current allocation ratio ... is the wrong ratio" and "the next billion dollars should have to prove it belongs on the physical side." Section 6.6 says the piece "is not a recommendation that MWAA pause Project Journey, halt Concourse E, or cancel any specific committed project" and recommends the operational intelligence allocation "be scoped, resourced, governed, and measured as a first-class program."
- **Issue continued:** These are three different theses. Section 1 is a defeat-test framing. Section 3.10 is an allocation-ratio framing. Section 6.6 is a governance framing with no defeat test. The reader ends not knowing which claim the draft is defending.
- **Recommendation:** Pick one thesis and hold it throughout. My recommendation: the defeat-test framing (Section 1) is the strongest and most falsifiable. Section 6.6 should restate it, not soften it.

---

## Pattern summary

The draft is strongest on **Economics** (Section 3.1–3.2) and **Operations** (3.3–3.4), where the evidence base is solid and the Strategist transmits it with discipline. It is weakest on **MWAA-specific application** (Section 6), which is vague, under-operationalized, and softens the thesis exactly where it should land hardest.

Second pattern: the Strategist is **better at presenting the counter-case (Section 4) than at refuting it (Section 5)**. Section 5.2.1 on NextGen is the only rebuttal that punches at the weight class of the counter-case. The other rebuttals narrow the thesis rather than defending it.

Third pattern: **citation discipline decays over the course of the piece**. Sections 3.1–3.4 carry tight inline citations to the Stage 1 briefs. Section 6 has fewer citations and more unsupported assertions ("supermajority," "T5-class governance," "first-class program"). If the reader challenges Section 6 on sourcing, much of it does not survive.

Fourth pattern: **several Contrarian objections are ignored, not answered**. The SEA $13.4M zero-metrics case. The Heathrow-still-pursuing-a-runway problem. The asset-depreciation / $151B backlog / mandatory-compliance share of capital budgets. Section 5 concedes these at the level of category but does not engage them at the level of specific cases.

Fifth pattern: **the draft redefines its way around inconvenient evidence**. The Gartner base rate is dodged by declaring A-CDM, TBS, RECAT "not AI projects." The 1:4.5 ratio is used as structural evidence without acknowledging that most of the $8.9B IT spend is not operational intelligence. Both moves are rhetorically convenient and will not survive skeptical scrutiny.
