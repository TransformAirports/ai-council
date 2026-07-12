# Red Team Critique — Strategist Draft v1

**Draft:** `outputs/stage2/strategist-draft-v1.md` ("The Stopwatch and the Shell")
**Verified against:** run prompt + the eight core Stage 1 briefs (infrastructure-economist, operations-analyst, technology-scout, contrarian, chief-engineer, airline-commercial-strategist, regulatory-political-analyst, aviation-historian)
**Date:** 2026-07-08

The draft's core argument is sound and the Saarinen frame is genuinely good. That is what makes the following defects dangerous: this piece reads confidently enough that a board member will quote the broken numbers. The exec summary's first sentence contains an arithmetic error, two deliverables the run prompt explicitly requires are missing entirely, and the Contrarian's two strongest surviving objections were never rebutted. Fix list follows.

---

## A. Broken, unsupported, or overstated claims

**1. The executive summary's first number is arithmetically wrong.**
- **Location:** Executive summary, point 1.
- **Issue:** "proposes to issue roughly four to five times the airport's entire existing $3.7 billion debt stack." $21.8B ÷ $3.7B = **5.9x**, not 4–5x. The infrastructure-economist derived 4–5x against MWAA's *aviation-enterprise* debt of $4.7–4.9B, not IAD's $3.7B. The body (¶2 of "Start with the one number") uses the correct $4.7–4.9B base; the exec summary swapped in the wrong denominator and kept the old multiple. This is the most-quotable sentence in the report and it doesn't survive a calculator.
- **Recommendation:** Pick one base and stick to it in both places. Either "$21.8B against MWAA's $4.7–4.9B aviation-enterprise debt — four to five times" or "$21.8B against IAD's own $3.7B — nearly six times." Do not mix.

**2. "Lost ~42,000 bags on opening day" is a conflation the briefs don't support.**
- **Location:** Executive summary, point 3.
- **Issue:** The infrastructure-economist says ~42,000 bags and 500+ flight cancellations *within ten days*; the chief-engineer says 23,000+ bags *on opening day*. The exec summary welds the big number to the short timeframe. The body paragraph ("first ten days") gets it right — the exec summary contradicts the body.
- **Recommendation:** "lost more than 42,000 bags in its first ten days" or "23,000+ bags on opening day." A fact-checker with veto power will strike the current version.

**3. "It always breaks at the same place... never the poured structure" — an absolute the chief-engineer's own brief contradicts.**
- **Location:** Executive summary, point 3; echoed in "The failure taxonomy" section ("almost monotonous in its consistency").
- **Issue:** Denver's Great Hall P3 blew up partly on "weak 1990s-era concrete discovered under the existing terminal" — unknown existing conditions, i.e., the poured structure — per the chief-engineer brief. That case is directly relevant to Dulles (renovating 1960s–80s Concourse A with as-builts that won't match reality) and the draft never uses it. "Always/never" invites the one counterexample your own evidence base contains.
- **Recommendation:** Soften to "almost always," and *add* the Great Hall case where it belongs: the renovation packages, where unknown existing conditions are the analog risk.

**4. The Kansas City causal claim is an inference dressed as a finding.**
- **Location:** Executive summary point 3 and failure-taxonomy section: "Kansas City delivered forty gates for $1.5 billion on time and on budget **by keeping novel systems off the critical path**."
- **Issue:** The brief documents that MCI was on time and on budget, and *separately* infers that the distinguishing variable across failures is novel systems on the critical path. No source says MCI succeeded *because* of that discipline. The draft states the mechanism as documented fact, twice.
- **Recommendation:** "on time and on budget — and, notably, with no bespoke system on its critical path" preserves the point as observation rather than proven cause.

**5. "Each built or paid for hub-scale infrastructure to a carrier's specification" overreaches the case file.**
- **Location:** Executive summary, point 8.
- **Issue:** "To a carrier's specification" is documented for Pittsburgh only. The airline brief's pattern claim is weaker: "the airport had recently built or was still paying for hub-scale infrastructure." Nothing establishes STL, CVG, or CLE built to the carrier's spec.
- **Recommendation:** "Pittsburgh built to US Airways' specification; Cincinnati, St. Louis, and Cleveland were each left carrying hub-scale infrastructure when the carrier's math turned."

**6. "Dulles already paid — twice — to rip out a processing model" — the second payment is never named.**
- **Location:** Thesis paragraph (intro) and synthesis section.
- **Issue:** The line is lifted from the aviation-historian, who also never itemizes the two payments. As written it's an applause line without a receipt. The receipt exists in the infrastructure-economist brief: the **2010 AeroTrain, ~$1.4–1.5B**, was payment one; the $22B program's AeroTrain extension and lounge retirement is payment two.
- **Recommendation:** Name both payments with the AeroTrain figure. It converts the draft's best rhetorical move into its best evidentiary one.

**7. The opening scene contains invented specifics.**
- **Location:** Opening paragraph: "In 1959, before he drew a single roofline, Eero Saarinen stood in airports with a stopwatch."
- **Issue:** No brief supplies "1959" or "stood in airports." The historian says Saarinen "studied passenger flow for over a year — famously with a stopwatch." The Dulles commission was 1958 and design work was underway well before 1959, so "before he drew a single roofline" is likely false as dated. Separately, the intro says the concept "was dead inside a decade" while line 11 says it "died in twelve years" — both have brief support, but pick one; a skeptical reader notices.
- **Recommendation:** Drop the year or verify it. "Before he drew a roofline, Saarinen timed passengers with a stopwatch" loses nothing. Standardize on "roughly a decade" or "twelve years" throughout.

**8. "The 2013 cost structure that put IAD on United's dehub list in the first place" overstates CPE's causal role.**
- **Location:** Implications, financial-decision paragraph.
- **Issue:** The airline brief is explicit that CPE is "necessary-but-not-sufficient" and that what put IAD at risk was post-merger network redundancy — and what saved it was EWR's physical constraint, not cost. The brief's careful phrasing is "the last time IAD sat near this cost basis, United considered leaving." The draft's version asserts a causal chain the brief deliberately avoided.
- **Recommendation:** Match the brief's phrasing. The correlation is damning enough without the manufactured causation.

**9. "Qualified bidders priced this exact scope" — the brief's own evidence says the scopes differed.**
- **Location:** Executive summary, point 2 ("a spread of more than $35 billion on the same building").
- **Issue:** The infrastructure-economist's evidence section notes the Phoenix/Ironbridge $35–50B variant was sized for **50M+ annual passengers — roughly double 2025 volume** — i.e., a different program, not the same building. (The brief's own verbatim quote carries the same flaw; the Strategist should have caught it rather than amplified it.) "Same scope, 3x disagreement" is a great line that a sophisticated reader — the stated audience — will dismantle.
- **Recommendation:** Keep the ±50% conclusion, but qualify: "responses to the same RFI, at scopes ranging from a rebuild of today's airport to a 50M-passenger expansion, priced the program from $14.4B to $50B." The uncertainty point survives; the false precision doesn't.

---

## B. Cherry-picked evidence

**10. The single most load-bearing number in the report carries a caveat the draft strips.**
- **Location:** Executive summary point 1 and "Start with the one number" — the $9.56 CPE.
- **Issue:** The infrastructure-economist flags in bold: "the single most load-bearing number in this brief — current CPE — is secondary-sourced" (DWU aggregation, not the audited ACFR), and recommends verification before external quotation. The draft builds its entire capital-allocation frame on the number and never discloses this.
- **Recommendation:** Either get the fact-checker to verify against MWAA's ACFR, or carry the caveat in a footnote. An executive audience at MWAA will know their own ACFR.

**11. CPE is presented as falling when the evidence base says it has already turned back up.**
- **Location:** "Start with the one number": "$9.56... down from $12.88 the year before as debt amortized and traffic recovered."
- **Issue:** The regulatory brief reports signatory CPE **rising from $9.56 (FY25) toward $12.77 (2026 H1)** on the ~$5.5B of debt MWAA already plans through 2028 — before the $22B program adds anything. The draft quotes the flattering downtrend and omits the reversal that is already underway, which actually *strengthens* its own thesis.
- **Recommendation:** Add the 2026 H1 figure and the $5.5B/coverage-toward-1.3x trajectory. The story "the cheap-hub advantage is already eroding before the first program bond is issued" is sharper than the one you told.

**12. The gate-utilization argument ignores the hub-banking objection your own airline brief supplies.**
- **Location:** "Coordination has been beating concrete" — the Southwest 10.3-turns-at-BWI vs. legacy 3–6 comparison.
- **Issue:** Three problems. (a) The airline brief explains that hubs *bank* flights into waves precisely to manufacture connections — a connecting hub's gates sit between banks by design, so comparing it to Southwest point-to-point is a category mismatch the draft never acknowledges. (b) The ops brief quantifies latent legacy-hub capacity at 30–50%; the draft inflates that to "a large multiple of throughput," which is both vaguer and bigger. (c) The underlying source is a circa-2012 SlideShare deck; Delta hasn't hubbed Memphis since 2013. For a report whose audience "has read McKinsey decks and is tired of them," a fourteen-year-old SlideShare is a soft foundation for a load-bearing exec-summary bullet.
- **Recommendation:** Keep the utilization point but (a) concede the banking constraint and argue the recoverable margin *within* a banked operation (common-use gating, variance compression — the ops brief's actual mechanism), (b) use 30–50%, (c) flag the data vintage or have the fact-checker find current turn data.

**13. United's current investment in Dulles is omitted entirely.**
- **Location:** Absent — should appear in the counter-case or the implications.
- **Issue:** The airline brief documents United building a >$500M, 14-gate Concourse E opening late 2026, growing departures +25% vs. 2023, and adding 13 routes in 2024 — "more than any other U.S. carrier added from any U.S. airport." The draft repeatedly treats United's commitment as fragile without disclosing that the anchor tenant is actively pouring its own money into the airport *right now*. The brief itself both presents this and disarms it ("commitment is a snapshot, not a covenant"). Omitting known counter-evidence is exactly what this report accuses others of.
- **Recommendation:** Add Concourse E to the counter-case, then deploy the brief's own disarm: CLE and CVG were at the top of the carrier's investment list a decade before they were cut.

---

## C. Logical gaps and unaddressed counter-arguments

**14. "From six different starting points" — five are listed.**
- **Location:** "The synthesis" section, first paragraph.
- **Issue:** Economist, engineer, operations analyst, technology scout, historian. That is five. Trivial, and exactly the kind of error that costs a report its credibility with a skeptical reader.
- **Recommendation:** Count your lenses. (Or add the sixth — see item 16 — and make the number true.)

**15. The Contrarian's induced-demand argument is never rebutted — or even mentioned.**
- **Location:** Absent from the counter-case and the rebuttal.
- **Issue:** The Contrarian's argument: air travel grows 4–5%/year, expanded capacity reliably fills, therefore sizing durable assets to genuine peak ages *best* — which directly attacks the draft's "pull coordination levers first, then build smaller" recommendation. The draft built a counter-case section specifically to be comprehensive and skipped one of the Contrarian's eight numbered arguments — arguably the one most likely to be raised in a program meeting ("demand will fill whatever we build").
- **Recommendation:** Add it and rebut it on the draft's own evidence: Dulles's lived record cuts against local induced demand — the 1997 expansion nearly tripled capacity to ~40M/year and the airport then *lost* ~200,000 passengers to DCA in 2011–13 when the perimeter loosened (infrastructure-economist brief). That datapoint is sitting unused and it is the perfect rebuttal.

**16. The Contrarian's asset-renewal reframe is never engaged, and it threatens the whole premise.**
- **Location:** Absent.
- **Issue:** The Contrarian argues the $22B program is *depreciation-driven renewal* of a worn-out 1962 plant — not a bet on any processing paradigm — and that renewal should be governed by lifecycle and throughput certainty. If that framing is right, much of the draft is answering a question the program isn't asking. The draft's whole durable/volatile apparatus actually survives this reframe comfortably (renewal is precisely when you decide what to lock for 50 years), but it has to say so.
- **Recommendation:** One paragraph in the rebuttal section: concede the program is renewal-driven, then observe that renewal is the *only* moment the durable/volatile split can be acted on — which makes the framework more urgent, not less.

**17. The draft says "lock the international geometry" without confronting the CBP staffing trap its own regulatory brief warns about.**
- **Location:** Implications, "Design FOR now."
- **Issue:** The regulatory brief is blunt: "MWAA can build international gates CBP will not staff... A Dulles concourse designed for international growth that CBP will not staff is a stranded asset in the most expensive part of the building." CBP officers are appropriated annually; the Reimbursable Services Program only rents overtime. The draft recommends locking exactly this geometry — the widebody international gateway — and never mentions the one federal constraint that can strand it. This is the regulatory analyst's fourth verbatim-ready quote and it contradicts an unqualified recommendation in the draft.
- **Recommendation:** Keep "lock the FIS geometry" (the ATDS argument is right) but add the staffing condition: build FIS *geometry* for the 2050 ceiling, phase FIS *fit-out and gate count* against CBP staffing reality, and put the appropriations risk in the same politics-hedging paragraph as the perimeter rule.

**18. The central recommendation — over-provision the substrate — has an unaddressed funding problem the regulatory brief hands you.**
- **Location:** "Provision the substrate" and Implications; absent everywhere.
- **Issue:** The draft says overbuild conduit, power, risers, floor loading "because retrofit is unaffordable." The regulatory brief says the money for exactly that is the problem: the PFC cap frozen at $4.50 since 2000 (fourth failed raise attempt in 2024), BIL terminal money sunsets **September 30, 2026** — before the first concourse is poured — and the next FAA reauthorization isn't until 2028. So every provisioning dollar is a bonded dollar that raises the CPE the draft spends its opening section defending. The draft never closes this loop; it recommends spending and defends the cost discipline in separate sections without reconciling them.
- **Recommendation:** Add the financing reality to the provisioning section and resolve the tension explicitly — presumably: provisioning is a small fraction of program cost with the highest retrofit-cost asymmetry, so it is the *last* scope to cut, not the first. Say that, with the PFC/BIL facts attached. This also supplies the missing sixth lens for item 14.

**19. The chief-engineer's lifecycle-tail argument is missing, and it undercuts the report's own cost framing.**
- **Location:** Absent; belongs in the capital-allocation frame or implications.
- **Issue:** The draft treats $22B as the cost. The chief-engineer's finding 4: the bond figure is capital-plus-financing, not 30-year cost of ownership — baggage, HVAC, vertical transport, AeroTrain rolling stock all renew on 5–25-year cycles *inside the operating building*, and GAO puts preventive-maintenance returns at $4–10 per $1. A report about what survives to 2050 that never mentions the renewal tail is missing the part of the 2050 story the operator actually lives.
- **Recommendation:** One paragraph. It also strengthens the volatile-layer argument: the 5–15-year layer isn't just replaceable, it's *scheduled* to be replaced — budget the cadence or manufacture the next crisis.

---

## D. Missing deliverables the run prompt explicitly requires

**20. The two dated snapshots (2035 and 2050) are absent.**
- **Location:** Required by the run prompt's success criteria ("Two dated snapshots... so leadership gets the distinct 10-year and 25-year pictures"); nowhere in the draft.
- **Issue:** This is a named deliverable, and the operations analyst wrote both snapshots ready-made (brief §6, passenger/operator day in 2035 and 2050). The Strategist left finished, on-thesis material on the table.
- **Recommendation:** Adapt the ops brief's two snapshots into a short section before the implications. They also dramatize the durable/volatile split better than the abstract statements of it.

**21. The commercial and experience model — dwell, retail, revenue architecture — is missing.**
- **Location:** Required success criterion ("does dwell/retail grow, shrink, or relocate? What does that do to terminal volume... and the revenue architecture the building is sized around?"); the draft's only gesture is "check-in halls convertible to dwell, lounge, and revenue space."
- **Issue:** A $21.8B bond program is serviced by aeronautical *and non-aeronautical* revenue; the historian brief explicitly says the durability of the revenue model (retail, dwell, parking) "is a structural, not cosmetic, question for Dulles" because the debt is multi-decade. The draft sizes its whole argument around CPE and never asks what the building's revenue architecture assumes. If the core briefs are thin here, say so and flag it as an open question for the program — silence reads as an oversight, a named gap reads as rigor.
- **Recommendation:** Add a section, even a short one. Minimum viable version: the check-in-hall-to-dwell conversion argument, the parking/curb revenue exposure to ground-transport shifts, and an honest "the Council's evidence base is weakest here."

**22. The gate/apron benchmark set — ICN, DOH, Changi T5, ORD Global Terminal — is absent.**
- **Location:** Required: "How are ICN, DOH, Changi T5, and the ORD Global Terminal hedging stand flexibility today — and what does that cost them?" The draft's stand-flexibility case rests on MARS generally, Frankfurt, and Daxing.
- **Issue:** The Contrarian confirms the hedges are "real, deployed... at ICN, DOH, and ORD" in one line, but no brief develops them and the draft doesn't mention them at all. The run prompt names four specific airports; the report answers with none of them.
- **Recommendation:** Either mine the remaining Stage 1 briefs (COO, virtual agents) for this material, commission a targeted gap-fill, or explicitly state the benchmark question the program team should answer — with the four airports named.

**23. The failure taxonomy doesn't meet its own spec.**
- **Location:** "The failure taxonomy" section vs. the run prompt: "catalog 6–10 recent large hub terminals (T5 '08, BER '20, IST, PKX, LGA, MCI, Jewel) and identify the single design decision that dated fastest in each."
- **Issue:** The draft covers BER, DEN, LAX APM, T5, MCI/KCI. IST appears only as a walking-distance datapoint, PKX only as the Daxing counter-example, Jewel not at all, and the "single fastest-dating decision" is named for maybe three cases. The draft *reframed* the taxonomy (systems-on-critical-path, not dated-form) — which is a defensible intellectual move, but it should be made explicitly, and the named airports should still be dispositioned even if the disposition is "IST's fastest-dating decision was walking distance, which is geometry, which proves our point."
- **Recommendation:** One tight paragraph per remaining airport, each ending with the single decision. The reframe then lands as a conclusion drawn from the full catalog rather than from a curated subset.

**24. Sustainability is reduced to GSE conduit; SAF, on-site generation, and thermal load are absent.**
- **Location:** Required success criterion; the draft covers electrified-GSE power provisioning only.
- **Issue:** The run prompt names "SAF logistics, on-site generation, thermal load" as physical demands to evaluate. The chief-engineer covered GSE and fast-charge power density; the draft uses that but goes no further and doesn't acknowledge the rest.
- **Recommendation:** Extend the provisioning section or name the gap. Fast-charge power density (Level 2's ~8-hour windows can't serve three-shift GSE — chief engineer) is in the brief and unused; add it at minimum.

**25. The executive summary is short of spec and the "prioritized" moves aren't prioritized.**
- **Location:** Exec summary (~750 words vs. the requested ~1,100); Implications section.
- **Issue:** The run prompt asks for "a prioritized set of moves the senior design and executive teams can take into a program meeting." The FOR/LATER/AGAINST sort exists, but nothing within those buckets is ranked, sequenced, or tied to the program's actual decision calendar (the regulatory brief maps forces to MWAA's calendar — April 2027 construction start binds the checkpoint decision, FY26–28 bond issuances bind the grant assumptions — and the draft uses none of it).
- **Recommendation:** Rank the moves inside each bucket and anchor the top three to program dates. The regulatory brief's decision-calendar table is the scaffolding; use it.

---

## E. Rhetoric, prose, and structure

**26. Council process language leaks into an executive-facing report — repeatedly.**
- **Location:** Intro ("the whole argument... the run prompt is asking about"; "narrower and harder than the one we were handed"); rebuttal section ("the run's original thesis," "the counter-case's own author grants," "even the contrarian concedes this outright"); counter-case ("the regulatory brief hardens this," "the second half of the operations brief's finding," "the airline lens supplies").
- **Issue:** The stated audience is airport executives and policy readers, not the Council. "The contrarian concedes" and "the run prompt" are internal machinery. This is the single most consistent tell that the document was assembled rather than written, and the run prompt's model — Matt Levine — never shows the reader his outline.
- **Recommendation:** Global rewrite pass. "Even the strongest version of the opposing case concedes..." / "the strongest objection comes from the airline side of the table..." Every reference to a brief, a lens, a run, or a contrarian must be converted to the argument's own voice.

**27. The synthesis paragraph is a consultant-memo roll call.**
- **Location:** "The synthesis": "The economist says... The engineer says... The operations analyst says... The technology scout says... The historian says..."
- **Issue:** Five identical-skeleton sentences that restate conclusions already delivered, in the exact "As the X brief notes" register the tone rules prohibit. It also contains the five/six miscount (item 14). The section adds no new information — it is a stacked summary paragraph.
- **Recommendation:** Cut it to two sentences or rebuild it around the one genuinely new observation it contains (six starting points converging is itself evidence). If kept, vary the syntax and lose the job titles.

**28. Vague quantifiers where the briefs supply numbers.**
- **Location:** Throughout: "a large multiple of throughput" (brief: 30–50% latent), "by wide margins" (exec summary point 4 — the margins are quantified two sentences later; cut the throat-clearer), "cheaper... than all but a handful of US large hubs" (the brief gives the full range; "third-lowest" or the ATL-to-LAX span is available), "rearranging deck chairs" (cliché, in the counter-case's mouth but still the Strategist's pen).
- **Recommendation:** Replace each with the brief's number. The house tone rules ban exactly this.

**29. Repetition is eroding momentum: Saarinen ×3, Pittsburgh ×4, MARS ×3.**
- **Location:** Saarinen/mobile lounges: intro, "the building itself already answered," coda. Pittsburgh: exec summary, counter-case, rebuttal ("concede the dehubbing risk"), implications. MARS: rebuttal, "Accommodate LATER," counter-case.
- **Issue:** The Saarinen frame is the draft's best asset and it is spent by the third telling. Pittsburgh does real work once (the $6-CPE severing of the cheap-terminal assumption) and then gets re-summarized three more times at decreasing resolution. Combined with an essay-style intro *followed by* a numbered exec summary *followed by* an argument section that re-covers the intro's ground, the reader hits the same material three times before anything new happens.
- **Recommendation:** Structural pass: (a) intro tells the Saarinen story once, fully; the argument section references it in a clause; the coda gets one new detail (it currently earns its callback — keep it). (b) Pittsburgh gets its full treatment in one place — the rebuttal's "dehubbing reinforces the thesis" paragraph, which is the draft's single best piece of reasoning — and pointers elsewhere. (c) Consider whether the exec summary should open the document per convention, with the Saarinen intro leading the report body instead.

**30. The counter-case section is the best-written part of the draft — and that's a problem of emphasis, not a compliment.**
- **Location:** "The counter-case, honestly presented" (~1,100 words) vs. "The argument" sections.
- **Issue:** The counter-case has the most concrete detail, the most named sources, and the most momentum. The affirmative argument, by contrast, leans on the roll-call synthesis and the padded gate-utilization comparison. A skeptical reader may finish the counter-case more persuaded by it than by the thesis — especially with the induced-demand and asset-renewal objections (items 15–16) missing from the rebuttal, which currently claims "four of its five strongest points argue for it" while having engaged only the points it could convert.
- **Recommendation:** After adding items 15–16, re-verify the "four of five" scorecard — it will change. And upgrade the affirmative sections with the unused evidence flagged above (AeroTrain $1.4–1.5B, the 1997-expansion/DCA-leakage precedent, the 2026 CPE upturn) so the thesis carries as much specific weight as its opposition.

---

## Priority order for revision

1. **Fix the numbers** (items 1, 2, 9) — these are veto-bait for the fact-checker and credibility-enders with the audience.
2. **Add the missing run-prompt deliverables** (items 20, 21, 22, 23, 24) — the report currently fails its own spec sheet.
3. **Close the logical gaps** (items 15, 16, 17, 18) — the rebuttal section's "we answered everything" claim is checkable and currently false.
4. **Strip the Council machinery and the roll call** (items 26, 27) — one global pass.
5. **Structural de-duplication** (item 29) — buys back the word count items 20–24 will spend.

The skeleton is right. The Saarinen frame, the durable/volatile discipline, and the dehubbing-reinforces-softness reversal are genuinely strong. But v1 ships a wrong number in its first bullet, skips two named deliverables, and declares victory over counter-arguments it never engaged. Fix those and this becomes the report the run prompt asked for.
