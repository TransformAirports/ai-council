# Infrastructure vs. Intelligence: Why the Next Billion in Airport CapEx Deserves a Harder Test

**Draft v2 — Strategist Synthesis (revised after Red Team critique v1)**
**Date:** April 17, 2026
**Run:** infrastructure-vs-intelligence

---

## 1. Thesis

US airports are allocating capital against a physical problem they diagnosed two decades ago, while a material share of the binding constraint on throughput has migrated to coordination, staffing, and software. The industry's own aggregate return numbers — with ACI World reporting 6.3% global airport ROIC in 2024 against a weighted average cost of capital that still exceeds it — sit alongside an 86% cross-sector megaproject overrun baseline and a PFC that has lost 40% of its construction-cost purchasing power since 2001. Some portion of the current capital program is not earning its cost of capital, and a separate portion is mandatory safety and asset-renewal work that no rebalancing will touch. The thesis is narrow: the discretionary portion of the next billion in airport CapEx — the portion not driven by pavement PCI, safety compliance, or irreducible physical overload — should have to clear a defeat test. That test is whether a much smaller operational intelligence investment, applied first, could compress the apparent demand for the physical project enough to stage, defer, or resize it. Most US hubs do not run that test. They should.

---

## 2. Executive Summary

1. **Airport CapEx, in aggregate, is not earning its cost of capital.** ACI World reports global airport ROIC at 6.3% in 2024 and states directly that this remains below the sector's weighted average cost of capital [Economist brief, Finding 1, Quotable 1]. The Economist brief flags that the precise ACI ROIC figure is drawn from press releases rather than the paywalled primary report and could not be independently verified [Economist brief, Section 3, Caveats]. The direction is clear; the decimal precision is not. An industry that cannot clear WACC in aggregate cannot average its way out — it can only outperform with projects that earn materially above the mean.

2. **Megaproject overruns are the baseline.** Flyvbjerg's 258-project transport dataset finds an 86% overrun rate with a 28% average magnitude [Economist brief, Finding 2]. Airport-specific cases sit above that baseline: Berlin Brandenburg 132% over, nine years late; LAX APM 76% over with no opening date as of March 2026; Denver Great Hall at roughly three times original city exposure [Economist brief, Finding 2, Evidence]. Heathrow Terminal 5 is the counter-case, and its lesson is governance, not category feasibility.

3. **The US delay picture is not primarily a runway picture.** FAA OPSNET data show 74% of system delays attributed to weather and 15% to volume; BTS flight-level data attribute 39% of delayed minutes to late-arriving aircraft and 35% to air carrier causes [Operations brief, Findings 1 and 2]. Nineteen of the 30 largest ATC facilities operate below 85% of staffing targets and produce 40% of all NAS delays [Operations brief, Finding 2, citing Brookings].

4. **Operational interventions have delivered independently validated double-digit gains.** RECAT at Memphis: 15%+ FAA-estimated capacity increase, nine added movements per hour [Operations brief, Finding 4]. TBS at Heathrow: 62% first-year reduction in headwind delays, 2.9 additional landings per hour in strong-wind conditions [Operations brief, Finding 4]. EUROCONTROL's A-CDM impact assessment across 17 airports: 34,000 tonnes of fuel saved annually and 250,000 minutes of flow management delay avoided [Technology Scout brief, Finding 4]. These sit a category apart from vendor claims in credibility and a category apart from 40%+ marketing figures in magnitude — mid-single-digit to low-double-digit percentage, measured, and audited.

5. **Most runway expansions do not hold their value.** The Bilotkach/Mueller analysis of 55 runway capacity expansions at the 150 busiest global airports between 2000 and 2016 found that by 2016, 15 airports were operating peak hours below 90% of *pre-expansion* capacity (meaning expansion was unnecessary on its own terms) and 19 were already operating at 90%+ of post-expansion capacity (meaning construction bought only temporary relief) [Operations brief, Finding 5]. Only the remainder — at most roughly one-third of the sample — operationalized the expansion into sustained high utilization.

6. **MWAA's financial envelope is tightening.** The 2025–2039 capital program is approximately 5.6x the prior cycle [Economist brief, Evidence: MWAA-Specific]. Some portion of the step-up is catch-up on deferred asset renewal; the remaining discretionary portion is what this paper is about. Between 2025 and 2028 MWAA plans to issue approximately $5.5 billion in new debt; adjusted debt per O&D enplanement is projected to peak near $400 (from $223 in 2024), and net revenue DSCR is projected to fall from 1.63x to approximately 1.3x [Economist brief, Finding 5]. Moody's shifted the US airport sector outlook to negative in May 2025 [Economist brief, Finding 5].

7. **Operational intelligence is optionable. Concrete is not.** A bad A-CDM deployment is recoverable in tens of millions and a few years. A bad concourse is a balance-sheet obligation for thirty. That asymmetry is the strongest argument for sequencing: committing operational intelligence first reveals what physical investment a higher operational baseline actually requires. Committing infrastructure first forecloses the test.

---

## 3. The Argument

### 3.1 The economics don't work at the top of the stack

Start at the top of the industry's own income statement. ACI World reports 2024 global airport ROIC at 6.3% and states in its own press release that this "remains below the sector's weighted average cost of capital" [Economist brief, Quotable 1]. One caveat the Red Team was right to flag: the precise ACI figure comes from a press release summarizing a paywalled primary report, and the Economist brief notes that the precise 2023 ROIC and regional breakdowns could not be independently verified [Economist brief, Section 3, Caveats]. The direction of the ROIC-to-WACC gap is the finding this paper relies on; the exact percentage point is not. ACI has disclosed that the gap exists in its own external communications. A sector's own trade body does not publicly concede value destruction unless the pattern is directionally robust.

Total 2024 global airport revenue of $194.9 billion was 2.1% below pre-pandemic levels in real terms even though passenger traffic was 4% above 2019 [Economist brief, Evidence: Global CapEx Trajectory]. Traffic recovered. Revenue did not. The explanation is structural, not cyclical: airports raised capital aggressively during the pre-pandemic boom and again to bridge the pandemic gap, and interest expense rose 18% year-over-year in 2023 as that debt repriced against higher rates [Economist brief, Evidence: Global CapEx Trajectory]. The 2023 global airport capital cost figure of $40 billion is 1% above pre-pandemic levels [Economist brief, Evidence: Global CapEx Trajectory]. ACI's own long-run outlook, prepared with Oxford Economics, projects $2.4 trillion in global airport CapEx from 2021 to 2040 [Economist brief, Evidence]. That trajectory presupposes the industry can, at some point, clear its cost of capital. The current evidence says it cannot.

When aggregate ROIC sits below WACC, you cannot average your way out with "good" projects. You can only outperform with projects that earn materially above the mean — and the margin for execution error on those projects is small.

### 3.2 Overruns are the baseline

Flyvbjerg's 258-project transport infrastructure dataset finds 86% of projects experience cost overruns, with a 28% average magnitude [Economist brief, Finding 2]. Airport megaprojects sit above that baseline:

- Berlin Brandenburg: €2.8 billion budget, €6.0–6.5 billion final cost, nine years late, total value destruction estimated near €11.9 billion including interest and unrealized revenue [Economist brief, Evidence: Cost Overrun Case Studies].
- LAX Automated People Mover: $1.9 billion contract in 2018, $3.34 billion as of July 2024, no opening date announced as of March 2026 [Economist brief, Evidence].
- Denver Great Hall: approximately $770 million original city exposure, now $2.1–2.35 billion across multiple phases. A January 2025 city audit found DIA "still is not following procurement procedures or requiring contractors to submit documentation of actual costs" [Economist brief, Evidence].
- Denver original automated baggage system (1995): $560 million in overruns, deployed to one concourse for one airline's outbound flights [Economist brief, Evidence].

GAO-20-298 makes the procurement problem concrete: airports' planned infrastructure costs for FY2019–2023 averaged $22 billion annually, a 19% increase over prior estimates, with terminal projects specifically increasing 51% [Economist brief, Evidence: US Federal Framework]. That is not inflation. It is systematic optimism bias embedded in the planning phase.

Heathrow Terminal 5 is the counter-case. The £4.3 billion terminal opened on schedule in March 2008, within budget, after BAA conducted a two-year pre-construction study explicitly designed to avoid megaproject failure modes [Economist brief, Evidence: Cost Overrun Case Studies]. T5 demonstrates that airport megaprojects can hit their targets. Its lesson is not that the sector is capable of this as a matter of course; its lesson is that hitting targets required an extraordinary pre-commitment to governance most authorities do not make. Section 6.4 specifies what "T5-class governance" actually means operationally — a point the Red Team was right to press. The base rate remains what it is.

### 3.3 The delay data does not say what the planning data assumes

Walk into a US airport planning meeting and you will hear about runway throughput, gate counts, and peak-hour aircraft movements. Walk over to the FAA's delay data and the picture shifts.

FAA OPSNET data over the six years ending May 2023 attribute 74.26% of system-impacting delays (>15 min) to weather, 14.92% to volume, 5.96% to runway unavailability, 0.61% to equipment, and 4.25% to other factors [Operations brief, Finding 1]. Read quickly, this looks like an argument that nothing is tractable: weather is weather. Read carefully, and the argument is different. "Volume" delays are not physical runway limits — they are the gap between instantaneous demand and the *operationally realized* capacity of an airport at that moment. That gap is where coordination lives.

Then look at BTS flight-level data, which records what airlines experience rather than what the NAS produces. From January–April 2023, late-arriving aircraft accounted for 38.99% of total delayed minutes, air carrier delays 35.43%, and NAS delays (which include ATC, runway, and heavy traffic volume) a smaller share [Operations brief, Finding 2]. Late-arriving aircraft delay is entirely a scheduling and turnaround phenomenon. It has no physical solution. You cannot concrete your way out of an aircraft that landed at LGA 20 minutes behind and now has to push back late at EWR.

Then look at the ATC data. The FAA has approximately 11,000 certified professional controllers against a model requirement near 14,000 [Operations brief, Finding 6]. Nineteen of the 30 largest facilities operate below 85% of staffing targets, and those 19 facilities alone account for 40% of all NAS delays [Operations brief, Finding 2, citing Brookings]. At peak dysfunction, DOT Secretary Duffy reported controller staffing accounted for half of all flight delays versus a normal baseline of 5% [Operations brief, Finding 6].

None of this changes with a new concourse. The Contrarian brief's own Scenario 2 concedes the point: "At some airports, delay is genuinely a coordination problem rather than a physical capacity problem... The argument for operational intelligence is strongest where this diagnosis is correct and infrastructure investment is therefore treating a symptom rather than a cause" [Contrarian brief, Part III, Scenario 2].

### 3.4 The operational-intelligence evidence base is real, not theoretical

This is where the conversation usually degenerates into vendor slides. The honest version cites only the data points that survive scrutiny.

**RECAT at Memphis (2012).** The FAA reclassified aircraft wake-turbulence categories. No construction. The result: an FAA-estimated 15%+ increase in airport capacity and nine additional aircraft movements per hour, with FedEx reporting 4.18 million gallons of fuel saved annually, monthly fuel cost savings of $1.8 million, and a three-minute cut in average taxi time [Operations brief, Finding 4]. The change took months, not a decade of environmental review.

**Time-Based Separation at Heathrow (2015).** NATS replaced distance-based arrival separation with time-based separation, neutralizing the headwind penalty that collapses runway throughput in strong winds. First-year result: 62% reduction in headwind delays, 2.9 additional landings per hour in strong-wind conditions, and more than 80% of landing aircraft separated more closely than under the old system [Operations brief, Finding 4]. Over ten years: 1.5 million minutes of airborne holding removed, 100,000+ tonnes of fuel saved, approximately USD 70 million in fuel cost savings [Operations brief, Evidence].

An honest framing of what TBS did and did not do: Heathrow operates at 98% of its 480,000 annual movement cap [Operations brief, Counterexamples]. TBS delivered large throughput gains *while the third-runway debate proceeded in parallel* — it did not substitute for the runway. Heathrow is still pursuing the third runway because TBS's gains were insufficient to close the demand gap at a two-runway airport serving 1,300+ daily movements. The correct claim is that TBS delivered measured capacity gains at a tiny fraction of a runway's cost while a separate infrastructure case — with its own long political and legal arc — continued. For airports not at a 98%-of-cap ceiling, TBS-class interventions can plausibly defer or resize the infrastructure question. For Heathrow itself, it did not, and an honest paper should say so.

**A-CDM across 17 European airports.** EUROCONTROL's independent 2016 impact assessment — compiled from network operations data, not vendor-reported — documented 34,000 tonnes of annual fuel savings (~€26.7M at then-current prices) and approximately 250,000 minutes of flow management delay avoided (~€15.5M) [Technology Scout brief, Finding 4]. Two caveats the Technology Scout brief is explicit about: (1) "the marginal benefit of adding one more airport decreases as the network penetration increases" — European A-CDM gains are partly a network effect that a US deployment will not fully capture without other US airports on the same protocol [Technology Scout brief, Finding 4]; (2) the FAA's TFMS is not a CDM equivalent, so a US A-CDM deployment at a single airport is a more isolated intervention than the European benchmarks imply [Technology Scout brief, Section 4]. That said, Munich's SESAR DMAN trials produced granular airport-level numbers in a single-airport measurement environment: 9% taxi time reduction, 14.6 kg fuel savings per flight, ATFM slot adherence improved from 76% to 81%, off-block time predictability up 7.8% [Technology Scout brief, Finding 4]. The Munich numbers are the most relevant benchmark for a US deployment — smaller than the 17-airport network figures, but more transferable.

**FAA TFDM at Charlotte.** Testing over four years saved more than 275,000 gallons of fuel per year, cut greenhouse gas emissions by 8 tonnes of CO2 daily, and eliminated 916 hours of delay per year at a single airport [Operations brief, Evidence: FAA TFDM Surface Metering]. At national rollout, the FAA projects 7 million gallons saved annually and 75,000 tonnes of CO2 eliminated.

These are single-digit to mid-double-digit percentage improvements. They are not the 40–80% figures vendors put on slides. They are what independent, disclosed-methodology studies produce — smaller than the marketing, larger than zero, and large enough to change a capital plan if you take them seriously.

### 3.5 The price-tag ratio, honestly framed

The Red Team was right to push back on the v1 framing. Here is the corrected version.

Global airport IT spending reached $8.9 billion in 2024 [Economist brief, Finding 6]. Global airport capital costs in 2023 were approximately $40 billion [Economist brief, Finding 6]. That produces a gross ratio of roughly 1:4.5 between total airport IT and total physical CapEx. But SITA's 2024 Air Transport IT Insights survey identifies cybersecurity as the #1 IT priority at 100% of respondents, with passenger processing #2 at 95% [Technology Scout brief, Evidence: Industry IT Spending Context]. The overwhelming majority of that $8.9 billion is not buying A-CDM or DMAN or surface metering — it is buying cybersecurity, passenger processing, payroll, networking, and back-office systems.

Operational intelligence in the Technology Scout taxonomy — A-CDM/DMAN, predictive turnaround/ramp coordination, operational-simulation digital twins, AI queue prediction, integrated operations centers — is a *narrow slice* of that $8.9 billion. The brief does not quantify exactly how narrow, but the deployment counts give a floor: only 3 of 31 US large hubs have operational digital twins [Technology Scout brief, Finding 2]; A-CDM is live at 34 *European* airports with no US equivalent program at comparable scale [Technology Scout brief, Finding 4]; SFO's AIOC opened in January 2026 as one of the first serious US APOC deployments [Technology Scout brief, Section 4]. Operational intelligence in the narrow sense is a single-digit-percentage-of-IT-spend category at most.

That sharpens, rather than weakens, the allocation argument. The ratio is not $8.9B of operational intelligence against $40B of concrete. It is much less operational intelligence against $40B of concrete. The v1 draft claimed "closer to 1:10 or worse at many large US hubs pursuing aggressive capital programs" — that specific hub-level ratio is not in any Stage 1 brief. The Red Team is correct that this figure was invented and it is removed from v2. The honest formulation is:

- Gross: airport IT of $8.9B vs. airport CapEx of $40B = 1:4.5 globally.
- Net: the narrow "operational intelligence" subset is a small fraction of $8.9B; against $40B of CapEx, that is a much larger asymmetry.
- Per project: the LAX APM alone at $3.34 billion consumes the equivalent of more than a third of annual global airport IT spend [Economist brief, Evidence]. The full upper-range estimate for a large-hub digital twin deployment ($15–40M over 24–36 months plus 10–20% annual recurring) [Technology Scout brief, Evidence: Digital Twins] is roughly 1.2% of the APM's current cost overrun alone.

The allocation argument does not turn on decimal precision. It turns on the order of magnitude between physical CapEx and the operational intelligence subset. The order of magnitude holds.

### 3.6 Induced demand, welfare, and capacity that evaporates

The Bilotkach/Mueller analysis of 55 runway capacity expansions at the world's 150 busiest airports between 2000 and 2016 found that by 2016, more than half of the expanded airports were back below pre-expansion capacity or congested again. Fifteen of the 55 were operating peak hours below 90% of their pre-expansion capacity — meaning expansion was unnecessary for them on its own terms. Nineteen of the 55 were already operating at 90%+ of their post-expansion capacity within a decade [Operations brief, Finding 5].

The Red Team's challenge here is fair: re-congestion after expansion is not automatically a failure. If the new capacity was fully absorbed by latent demand that was previously being rationed, that is welfare-positive — the airport is now serving passengers it previously could not. Denver at 82.4 million through a 50-million-design airport is the canonical example [Contrarian brief, Part IV-3]. The narrow claim this paper is willing to make: expansions whose economic case depended on sustained post-expansion capacity headroom — which is the justification most planning documents actually use to underwrite the bonds — are defeated when that headroom disappears within a decade. That is the 19-of-55 pattern. Separately, expansions in markets where the pre-expansion level itself went unreplicated (15 of 55) are defeated on their own planning terms regardless of welfare counterfactuals. That is 34 of 55 cases (62%) where the expansion either was unnecessary on its pre-construction justification or did not hold its post-construction justification.

In the remaining 21 cases, the welfare case may be strong, but the financial case depends on demand projections that, at airport timescales, cannot be underwritten with confidence. That is the point: infrastructure pays where the binding constraint is physical and demand is inelastic over the asset's 30–50 year life. Frankfurt Runway 18 West raised movements per hour from 83 to 126, a 52% increase, because the prior runway geometry did not permit simultaneous independent operations and no procedural change could replicate that [Operations brief, Counterexamples]. It is a legitimate case. It is also not the modal US hub.

### 3.7 MWAA's balance sheet, with the Red Team's correction

MWAA's 2025–2039 Capital Construction Program is valued at approximately $9 billion, replacing a 2015–2024 program of roughly $1.6 billion — a 5.6x step-up between consecutive cycles [Economist brief, Evidence: MWAA-Specific]. The Red Team is correct that 5.6x as a bare number assumes the prior $1.6B cycle was correctly sized. It was not, at least in part: US airport infrastructure in aggregate has been running $142B behind projected 10-year need [Economist brief, Finding 3], and the Contrarian's Part II argument on asset depreciation and mandatory FAA PCI-driven pavement rehabilitation [Contrarian brief, Part II] applies with force to any multi-decade capital plan. Some fraction of MWAA's 5.6x is genuine catch-up on deferred safety, security, accessibility, and asset-renewal work. None of that is what this paper is about.

The allocation argument applies only to the *discretionary* portion of the $9B — the capacity-growth tranche, the demand-contingent tranche, the non-mandatory passenger-experience tranche. Sections 6.1 and 6.2 identify which specific projects fall on which side of that line at DCA and IAD. The non-discretionary tranche should be funded. The discretionary tranche should be defeat-tested.

The financial environment is the frame. MWAA plans to issue approximately $5.5 billion in new debt between 2025 and 2028. Adjusted debt per O&D enplanement is projected to nearly double, from $223 in 2024 to approximately $400 in 2028 [Economist brief, Finding 5]. Net revenue debt service coverage is projected to fall from 1.63x in 2024 to approximately 1.3x over five years — still above bond covenant minimums (typically 1.10x–1.50x depending on indenture), but the cushion is shrinking [Economist brief, Finding 5]. At Dulles specifically, DSCR is projected to deteriorate from 2.79x in FY2024 to 1.70x by FY2030 even under favorable traffic assumptions [Economist brief, Finding 5]. Moody's shifted its US airport sector outlook from stable to negative in May 2025 [Economist brief, Finding 5].

The PFC backdrop compounds the issue. The statutory PFC cap has been $4.50 since 2001. A RAND study commissioned by Congress concluded that the purchasing power of that $4.50 had declined to the equivalent of $2.72 in year-2000 dollars indexed to construction prices — a 40% real loss — and the 2024 FAA Reauthorization left the cap unchanged [Economist brief, Finding 3]. Airports are being asked to finance an expanding capital envelope from a passenger-level revenue stream whose real value is shrinking.

### 3.8 The opportunity cost is not recoverable on airport timescales

The deepest argument against the marginal *discretionary* dollar of airport CapEx is not that the project will fail. It is that the capital is committed for 30–50 years whether the project succeeds or not. Bond covenants require debt service regardless of utilization. A terminal built in 2026 for a demand projection that proves wrong in 2035 cannot be un-built.

The structural warning case is CVG. After Delta's dehubbing, Cincinnati's CPE rose from under $5 to over $10 on collapsing enplanements [Economist brief, Finding 7]. The infrastructure was fine. The airlines left. The capital stack had no flexibility.

Compare the optionality of an operational intelligence investment. A-CDM implementation, an APOC, a surface metering system, a computer-vision turnaround monitoring deployment — these are measured in single-digit-million to low-tens-of-million commitments, deployable in months to a few years, and reconfigurable as the operating environment changes. Assaia's 2025 report on AI turnaround monitoring across 15 airports and 450,000+ turns found median departure delay cut from 4 to 3 minutes (a 25% reduction), with North American airports saving approximately $100 per turnaround per minute of delay reduction [Technology Scout brief, Finding 7]. Transmit the Technology Scout's caveat: this is vendor-published research drawn from vendor-customer airports; it is not peer-reviewed and has not been independently audited; the sampling methodology (which airports, which flights, how baselines were established) is not disclosed [Technology Scout brief, Predictive Turnaround / Ramp Coordination]. Treat Assaia's numbers as mechanistically plausible, corroborated by multi-airport deployment, and subject to aggressive discounting. The higher-confidence anchor remains Munich's SESAR DMAN result: 9% taxi time reduction, 14.6 kg fuel savings per flight, disclosed methodology [Technology Scout brief, Finding 4].

Here is the sharpened version of the optionality claim, with the Red Team's correction applied. A bad airport-level operational intelligence investment is recoverable in tens of millions and months; a bad concourse is a balance-sheet problem for 30 years. That is different from saying software failure is costless — NextGen proves it can cost tens of billions at federal scale, and Section 5.2.1 addresses that directly. At the *airport* level, under the *commercial* deployment model this paper recommends, the optionality asymmetry holds. The claim is scoped, not universal.

### 3.9 The false-precision trap in on-time performance data

Over 2012–2023, average US airline schedule padding increased 27%, adding roughly 3 minutes of buffer time per flight. Research cited by FinanceBuzz finds that a 10% increase in scheduled block times produced a 20-percentage-point artificial improvement in measured on-time performance over five years [Operations brief, Finding 7]. Zhang, Salant, and Van Mieghem's 2018 work documents this as a systematic competitive response to chronic operational variance.

This matters because many airport capital programs are justified, in part, by recent improvements in on-time performance and passenger experience metrics. Those metrics are partially accounting. The underlying operational variance — the true gap between the airport's realized and potential capacity — is larger than the reported numbers suggest. Strip the padding out, and the case for operational intelligence gets stronger, not weaker: the hidden variance is what A-CDM, TBS, and surface metering are designed to compress.

### 3.10 Summary of the case

- Industry aggregate ROIC is reported below WACC by the industry's own trade body, with a verification caveat on the precise figure.
- Megaproject overruns are the baseline; terminal projects are the worst category.
- The dominant delay drivers are weather resilience, ATC staffing, and carrier-side coordination — not runway or terminal constraints at the modal US hub.
- Operational interventions have delivered independently validated single-digit-to-low-double-digit capacity gains in months-to-years, at percentages of megaproject cost.
- Runway expansion fails to hold its value, or was unnecessary on its own terms, in 34 of 55 documented cases (62%).
- MWAA's specific debt trajectory is moving toward a DSCR that leaves little room for a demand or rate shock, with the non-discretionary tranche of the capital plan segregated from this argument.
- The opportunity cost of misallocated discretionary airport capital is locked in for decades; the opportunity cost of a misallocated airport-level operational intelligence dollar is recoverable in years.

The argument is not that airports should stop building. It is that the discretionary portion of the next billion dollars should have to prove it belongs on the physical side of the ledger, under a defeat test that almost no current planning framework applies.

---

## 4. The Counter-Case, Honestly Presented

The strongest version of the pro-infrastructure argument is not a defense of current practice. It is a specific set of claims that, taken together, describe conditions under which operational intelligence cannot substitute for physical investment. This section presents those claims using the Contrarian's own framings where load-bearing, with attribution.

### 4.1 Physical ceilings are real, and software is not geography

Runways, taxiways, gate frontage, and airspace sectors have mathematically fixed throughput maxima. LaGuardia is capped by the FAA at 71 scheduled operations per hour not as administrative preference but because its two-runway geometry produces effective single-runway operation during peak hours in a slot-saturated New York corridor [Contrarian brief, Part I-1]. DCA handles 25 million annual passengers on infrastructure designed for 15 million, with the Potomac, federal facilities, and residential neighborhoods forming a hard perimeter; the FAA has imposed a hard slot cap of 62 takeoffs or landings per hour maximum, and has explicitly stated no additional flights can be accommodated [Contrarian brief, Part II, DCA section]. Denver processed 82.4 million passengers in 2024 through infrastructure built for 50 million — 65% over design capacity — and is planning four new concourses to reach 125 million [Contrarian brief, Part I-4; Part II]. As the Contrarian puts it directly: "The physics do not negotiate" [Contrarian brief, Part I-4, quoted verbatim].

The software case concedes physical ceilings in principle and then can quietly ignore them when costing alternatives. Not in this paper. Sections 5 and 6 segregate the ceiling cases from the discretionary cases explicitly.

### 4.2 O'Hare is the cleanest infrastructure ROI case in modern commercial aviation

The O'Hare Modernization Program — converting an intersecting-runway airfield to six parallel east-west runways — produced a documented 64% reduction in system-impact delays comparing 2003–2008 to 2009–2020, a 79% reduction in flight delay rates, and a 50% increase in peak operational capacity [Contrarian brief, Part I-2; Operations brief, Counterexamples]. These are measured FAA outcomes over a decade, not modeled projections. The mechanism is simple and cannot be replicated in software: intersecting runways force mandatory sequencing between operations; parallel runways dissolve that dependency.

The Operations brief adds one caveat: O'Hare's expansion also included significant operational and technology upgrades (Terminal Sequencing & Spacing, Time-Based Flow Management), making it difficult to isolate the pure infrastructure contribution [Operations brief, Counterexamples]. That caveat does not overturn O'Hare's core case. It does suggest that even the cleanest infrastructure ROI story in modern aviation was executed as a coupled infrastructure-plus-operations program, which is how Sections 6.1 and 6.2 recommend MWAA treat its own major projects.

### 4.3 NextGen is the empirical indictment

This is the single most damaging data point in the debate, and any honest strategist has to address it. The FAA's NextGen program — the largest operational intelligence initiative in the history of commercial aviation — has consumed over $15 billion in federal investment (combined public and private investment through 2030 exceeding $35 billion) and, per the DOT OIG, delivered approximately 16% of its projected benefits [Contrarian brief, Part I-5]. The original $199 billion benefit projection from 2013 was revised to $63 billion by 2024. The NAS Voice System was terminated after $160 million with minimal benefits, then required an additional $274 million to sustain legacy systems through 2030. The Terminal Flight Data Manager program was delayed three years, cost 20% more than budgeted, and had its scope cut from 89 to 49 sites [Contrarian brief, Part I-5; Part II].

The DOT OIG's language is direct: the program is "narrower in scope, more expensive, and later than the version originally promised" [Contrarian brief, Part I-5, quoted verbatim]. Benefit-to-cost ratio for the 2010–2018 measurement period was below 1.0 [Contrarian brief, Part I-5].

A proposal to reallocate discretionary airport capital from physical infrastructure to operational intelligence has to explain why the largest operational intelligence program in aviation history delivered a BCR below one, and what is structurally different about the investments this paper proposes. Section 5.2.1 answers that directly.

### 4.4 The base rate for AI project success in infrastructure and operations is low

A Gartner analysis published in April 2026 found that only 28% of AI projects in infrastructure and operations fully succeed and meet expectations; 20% fail outright [Contrarian brief, Part I-7]. Among leaders reporting failure, 57% cited "expecting too much, too fast." Data quality issues and skill gaps are the other leading causes — and the aviation data environment is particularly hostile on both dimensions: inconsistent formats across carriers and ground handlers, legacy system encoding, real-time latency challenges, and no common data standard across stakeholders [Contrarian brief, Part I-7].

Between 60–85% of enterprise AI projects fail overall, with 68% of failed implementations attributable to data quality issues [Technology Scout brief, Finding 5]. SITA's 2024 Air Transport IT Insights survey identifies fragmented data as the primary barrier to realizing value from the $8.9 billion already being spent annually on airport IT [Technology Scout brief, Finding 5]. SEA spent $13.4 million integrating seven vendors (Saab Aerobahn, Assaia, Inform GroundStar, Safedock, Genetec, Accipiter, FlightAware) to get basic ramp situational awareness, and the case study does not report a single quantified performance outcome — secondary-source figures of "17% on-time performance improvement and 44% taxi-in reduction" could not be confirmed to a primary source [Technology Scout brief, Quotable 3, Finding 1]. Section 5.2.5 addresses the SEA case directly rather than using it only as cautionary decoration.

### 4.5 Infrastructure is accountable; operational intelligence, characteristically, is not

A runway, a concourse, a gate — these are inspectable, auditable, and produce observable outcomes. When they fail, everyone can see the failure. When a $15 billion operational intelligence program delivers 16% of promised benefits, the vendor community's response is not to refund the money but to argue for more funding and longer timelines [Contrarian brief, Part I-8].

The counter-response in Section 5.2.4 is that Denver Great Hall, LAX APM, and Berlin Brandenburg were all inspectable, auditable, and still catastrophic. The accountability argument is an argument for governance structure, not for concrete over code.

### 4.6 Software creates new fragility; infrastructure creates durable redundancy

The July 2024 CrowdStrike incident grounded Delta for multiple days. A single failed hardware component at a data center grounded Alaska Airlines for hours in 2025, producing over 150 cancellations [Contrarian brief, Part I-6]. The GAO found that 40 of 41 airports it surveyed are actively investing in physical electrical resilience — backup power, microgrids, redundant distribution — precisely because operational intelligence requires physical substrate to function [Contrarian brief, Part I-6]. A runway does not crash. Concrete does not experience an unplanned outage.

### 4.7 Demand is real and growing faster than optimization can absorb

The FAA's 2025–2045 Aerospace Forecast projects US airline enplanements surpassing 1.28 billion annually by 2038. IATA's 20-year forecast projects global air travel reaching 7.8 billion passengers by 2036 [Contrarian brief, Part I-4]. Operational intelligence can improve throughput at the margin. It cannot serve 82 million passengers through a terminal designed for 50 million.

### 4.8 The $151 billion backlog is largely non-discretionary

ACI-NA's 2023 Infrastructure Needs Report puts US airport infrastructure need at $151 billion over five years, up more than 30% from $115 billion two years prior [Contrarian brief, Part I-3; Part II]. Contrarian Part II states that "the $151 billion ACI-NA infrastructure needs figure... reflects primarily mandatory safety, security, and accessibility compliance projects, not discretionary amenity investment" [Contrarian brief, Part II, Asset Depreciation]. More than 50% of Airport Improvement Program funding goes toward constructing or rehabilitating runways, taxiways, and aprons, because that is what FAA safety standards require. A runway with a deteriorated Pavement Condition Index score must be rehabilitated before other capital projects can be approved for AIP funding [Contrarian brief, Part II].

This is the single most important concession the thesis has to make, and Section 5.1 concedes it directly. The allocation argument applies to discretionary capital, not to mandatory compliance and asset-renewal spending.

### 4.9 Synthesizing the counter-case

Put together, the pro-infrastructure argument is not "build everything." It is:

1. Physical ceilings exist and are absolute where they bind.
2. Where the ceiling is genuinely physical, infrastructure has a measured track record of large and durable gains (O'Hare, Frankfurt).
3. The largest operational intelligence experiment in aviation history delivered 16% of its promises.
4. Base rates for AI success in infrastructure and operations are low; the aviation data environment is harder than average.
5. A majority of the $151B need is mandatory safety and asset-depreciation investment, not discretionary build.
6. Demand growth is real and physical.

That is a serious argument. It deserves a serious answer.

---

## 5. Why the Counter-Case Is Insufficient

The counter-case has to be conceded where it is right. The thesis still holds on a narrower footprint. The order of this section leads with the strongest rebuttal (NextGen), then moves to the SEA case (the strongest US airport-level counterexample), then the Gartner base rate (honestly engaged rather than defined away), and only then to the softer concessions.

### 5.1 What must be conceded

**Physical ceilings are real.** The thesis does not survive contact with an airport operating at 98% of a genuine physical cap. Heathrow is such an airport [Operations brief, Counterexamples]. DCA is at a federal slot cap plus physical perimeter [Contrarian brief, Part II, DCA section]. LGA is at a hard FAA cap with geometry that enforces effective single-runway operation at peak [Contrarian brief, Part I-1; Part II]. Where the binding constraint is physical geometry with active safety conflicts, infrastructure is the right answer.

**O'Hare is a real data point.** The O'Hare Modernization Program produced large, durable, measured gains [Contrarian brief, Part I-2]. Any framework that would have deferred this investment needs to explain what would have replaced it. Nothing would have.

**NextGen's failure is real.** The $15 billion, 20-year, 16%-of-promised-benefits record is the single hardest fact the operational intelligence case has to answer [Contrarian brief, Part I-5]. The failure was not primarily technical; it was governance, scope creep, and a federal contracting apparatus not built to deliver complex software systems on commercial timelines. But the failure is real, it is documented, and it happened in the exact institutional environment a US operational intelligence expansion would partially inherit.

**Safety and depreciation spending is not substitutable.** A cracked runway cannot be offset by a surface metering system. The majority of the $151B ACI-NA need is mandatory safety, security, and accessibility compliance [Contrarian brief, Part II, Asset Depreciation]. The 50%+ share of AIP funding that goes to pavement rehabilitation is baseline compliance, not discretionary capacity investment [Contrarian brief, Part II]. This paper's allocation argument does not touch that spend.

**Demand growth is real.** 82.4 million passengers passed through DEN in 2024 [Contrarian brief, Part I-4; Part IV-3]. At some airports, in some markets, demand will exceed what optimization can serve. DEN is one such airport; a paper that recommended Denver optimize instead of build four new concourses would not survive the first planning session.

### 5.2 Why the thesis still holds

#### 5.2.1 The NextGen indictment is about the wrong category of investment

NextGen was an attempt to modernize the national air traffic control system via a federal program that spanned two decades, multiple administrations, and dozens of contractors — reworking a safety-critical distributed system used by every commercial flight in US airspace. Its closest comparables are not airport operational intelligence investments. Its closest comparables are other federal IT modernizations: IRS modernization, DoD defense business systems, the VA electronic health record rollout. Those programs, collectively, are the empirical basis for the claim that large federal IT modernizations underperform.

The airport operational intelligence investments this paper argues for are categorically different in three ways that the thesis puts positive weight on rather than using as rhetorical cover.

*First*, they are airport-level, not national. A Seattle or a Dulles deploying A-CDM operates inside a defined organizational perimeter with an accountable executive. NextGen's stakeholders spanned the FAA, every commercial airline, every controller local, and Congress. Governance complexity compounds rather than adds. The EUROCONTROL A-CDM evidence base — 34,000 tonnes of fuel saved annually across 17 airports, independently compiled [Technology Scout brief, Finding 4] — is what airport-level deployments actually produce. That number is not 16% of its promise. It is an independently audited network-level result.

*Second*, they are commercially off-the-shelf. A-CDM, DMAN, computer-vision turnaround monitoring, queue prediction, surface metering are productized by multiple vendors with multi-year operational track records at European hubs [Technology Scout brief, Sections 2 and 4]. NextGen was a custom federal development effort. The base rate for custom federal IT is not the base rate for commercial airport IT.

*Third*, they are scoped in years, not decades. Munich's SESAR DMAN trials ran, produced measured results, and fed into iterative deployment [Technology Scout brief, Finding 4]. Heathrow's A-CDM was live within timeframes orders of magnitude shorter than NextGen's 20-year arc. An airport that commits to A-CDM in 2026 will know by 2028 whether it worked. A terminal expansion that breaks ground in 2026 will not reveal its verdict until 2040.

The Contrarian's own Scenario 4 makes the concession the thesis needs: "NextGen's failure reflects 2003-era ambition colliding with 2010s-era technology and 2020s-era implementation capacity. Modern AI capabilities in computer vision, real-time optimization, and multi-agent coordination are categorically more powerful than the rule-based systems NextGen tried to deploy. The historical record does not necessarily indict future capability, and a fair reading of the evidence acknowledges that the infrastructure advocate is pointing at a past failure to discredit a category of investment whose current-generation capabilities may genuinely differ" [Contrarian brief, Part III, Scenario 4]. That is not a rhetorical fig leaf; it is the Contrarian brief's own analytical concession, and this paper takes it seriously.

#### 5.2.2 The SEA $13.4M case: a real failure the thesis has to address

The Technology Scout brief states plainly: "Seattle-Tacoma International Airport spent $13.4 million integrating seven operational intelligence vendors... to achieve basic ramp situational awareness. The case study does not report a single quantified performance outcome. This is the honest picture of what operational intelligence actually costs and how difficult it is to measure" [Technology Scout brief, Quotable 3].

SEA is not NextGen. It is a US, airport-level, commercial-vendor operational intelligence deployment — exactly the category this paper recommends. And it produced no published operational results. The Red Team is correct that this is an unanswered airport-level counterpoint to the thesis. Here is the answer.

First, SEA is evidence that deploying seven vendors without unified data architecture produces integration cost and no measurable outcome. The Technology Scout brief identifies the mechanism directly: "SITA identifies fragmented data as the primary barrier to realizing value from $8.9 billion in annual airport IT spending. The problem is not insufficient investment in technology. The problem is that the data infrastructure connecting those investments does not exist" [Technology Scout brief, Quotable 4]. SEA's $13.4M bought seven point solutions, not a coherent operational intelligence platform. The integration absorbed the investment because the data layer was not built first.

Second, "no published performance outcome" is not the same as "no performance outcome." It is consistent with the Tech Scout's broader finding that US airports deploy without publishing: "The absence of independently audited US airport operational intelligence outcomes is itself a finding: airports are deploying technology without publishing results, which makes the ROI case harder to make and easier to overclaim" [Technology Scout brief, Closing Note]. SEA's failure is a disclosure failure as much as an operational failure. That is the standard MWAA should not accept.

Third, the prescription: a credible MWAA operational intelligence program starts with a unified AODB and data layer, treats point solutions as modules on that layer, and publishes before/after metrics as a contractual condition. Section 6.5 makes that specific. The SEA case does not invalidate airport-level operational intelligence; it invalidates the "procure seven vendors and integrate at the edges" architecture SEA actually used. That distinction is load-bearing, not decorative.

#### 5.2.3 The Gartner base rate: engaged, not defined around

The v1 draft argued that A-CDM, TBS, and RECAT "are not AI projects" and therefore sit outside the Gartner 28%-success denominator. The Red Team is right that this is special pleading without an independent source to anchor it. The Technology Scout brief does not explicitly endorse that taxonomy. V2 withdraws the claim and engages the base rate honestly.

The Gartner finding: 28% of AI projects in infrastructure and operations fully succeed, 20% fail outright, with "expecting too much, too fast," data quality issues, and skill gaps as the leading failure causes [Contrarian brief, Part I-7]. Two qualifications are supportable from the briefs, but neither is a dodge.

First, the 28% figure is a denominator that *includes* speculative ML projects across every sector of infrastructure and operations broadly — not a base rate specific to productized airport coordination technology. The Technology Scout brief's credibility hierarchy is explicit: EUROCONTROL A-CDM and SESAR DMAN sit in the "high credibility (independent data)" tier with documented multi-airport audits; Assaia and Copenhagen Optimization vendor claims sit in the "low credibility for specific figures" tier; IATA One ID's 40% processing-time figure and extrapolated 2035 projections sit in "not verifiable / should be excluded from capital justification" [Technology Scout brief, Section 6]. A responsible airport that buys from tier 1 and disciplines tier 2 with aggressive discounting is not drawing randomly from the Gartner denominator. That does not mean the base rate is irrelevant — it means the portfolio the thesis recommends is actively selected against the modal failure mode in the Gartner data.

Second, for the investment categories that *are* squarely within the Gartner denominator — computer-vision turnaround monitoring, queue prediction, predictive maintenance, passenger flow AI — the thesis has to concede: expected success rate is lower, data backbone is a prerequisite, and ROI figures should be discounted hard. The Technology Scout brief is blunt on this: "Every substantive ROI figure in this space requires a credibility haircut" [Technology Scout brief, Finding 3]. V2 concedes this and treats it as an argument for portfolio structure: lead with high-confidence, independently audited categories (A-CDM, DMAN, surface metering — Munich-class numbers), treat mid-confidence vendor-productized categories (turnaround AI, queue prediction) as tier-2 investments sized to fail cheaply, and defer low-confidence categories (operational-simulation digital twins, agentic AI) until the data backbone is demonstrably in place. That is a portfolio structure the Gartner data actually supports. It is not a redefinition of the denominator.

Third — and this is where the base rate argument cuts back — the comparison case for AI project failure is megaproject failure. Flyvbjerg reports 86% of transport infrastructure projects overrun by an average of 28% [Economist brief, Finding 2]. Airport-specific overruns are larger. The right question is not "do AI projects fail?" It is "do airport-level, commercially productized AI projects fail at a higher rate than airport megaprojects, adjusting for magnitude and recoverability?" Neither brief answers that directly. But the comparison is not: infrastructure reliably delivers vs. software reliably fails. It is: both fail at high rates, but their failure modes have asymmetric financial consequences on airport timescales. That is the real argument.

#### 5.2.4 The accountability argument cuts both ways

The Contrarian's argument that infrastructure is accountable while software is not is rhetorically powerful and empirically selective. Denver's DIA Great Hall was inspectable, auditable, and still produced approximately a 3x cost overrun, a terminated public-private partnership, and a January 2025 city audit finding that DIA "still is not following procurement procedures or requiring contractors to submit documentation of actual costs" [Economist brief, Evidence]. The LAX APM was inspectable, auditable, and has no announced opening date after $3.34 billion spent against a $1.9 billion contract [Economist brief, Evidence]. Berlin Brandenburg was the most inspectable airport project of its generation and opened nine years late at roughly €11.9 billion in total value destruction [Economist brief, Evidence].

Infrastructure is visible when it is complete. During construction — where most of the risk lives — it is not meaningfully more accountable than a software program. The accountability argument is an argument for T5-style governance, not for concrete-over-code. Section 6.4 operationalizes what T5-class governance actually means.

#### 5.2.5 The fragility argument is real but asymmetric

The CrowdStrike incident grounded Delta. It did not ground the NAS [Contrarian brief, Part I-6]. The Alaska Airlines hardware failure produced 150 cancellations at a carrier with approximately 1,300 daily flights — a bad day, not a systemic failure. Software fragility is real and has to be designed around. But the asymmetric case cuts the other way too: a runway that cannot be built cannot ground flights it was not yet serving. A terminal that was canceled at the planning stage does not trap 30 years of capital. An operational intelligence investment that fails at the airport level costs tens of millions; a terminal that fails costs billions and encumbers the balance sheet for decades.

The correct response to software fragility is redundancy, backup protocols, and failover design — all of which cost a fraction of physical redundancy. It is not to build concrete instead.

#### 5.2.6 Physical ceilings bind at a minority of hubs, but this paper should not overclaim

The v1 draft asserted that the thesis conditions "describe a supermajority of the US large-hub system." The Red Team is correct that this quantified claim is not supported in any Stage 1 brief. V2 withdraws "supermajority" and replaces with specifics.

LGA, DCA, Heathrow at 98% of cap, and pre-modernization O'Hare are the canonical physical-ceiling cases [Operations brief, Counterexamples; Contrarian brief, Part I-1, Part II]. DEN is a demand-overload case that is physical-ceiling-equivalent given 82.4M through a 50M design [Contrarian brief, Part IV-3]. The Operations Analyst brief documents at 55 airports globally (not US hubs specifically): 15 of 55 at under 90% of *pre-expansion* capacity, 19 of 55 at 90%+ of post-expansion within a decade, with the sustained-high-utilization remainder concentrated in Asia [Operations brief, Finding 5, Counterexamples]. The Technology Scout brief reports only 3 of 31 US large hubs have operational digital twins; 17 of 31 remain in pilot or planning [Technology Scout brief, Finding 2] — suggesting the data backbone for serious operational intelligence is not yet in place at most US large hubs, which is a precondition for this paper's recommendations.

The honest statement: the thesis applies where (a) peak-hour utilization does not sit above 90% of declared capacity for the bulk of operating hours, (b) delay attribution data shows meaningful contribution from air carrier, late aircraft, ATC staffing, or ground coordination causes, (c) the airport has not deployed the core commercially productized operational intelligence categories at scale, (d) the capital program's debt trajectory is moving toward DSCR below 1.5x within five years, and (e) the demand forecasts embed assumptions that could be disrupted by hub strategy changes, fuel price shocks, or post-pandemic pattern shifts. Multiple US large hubs meet most of those conditions; neither brief enumerates exactly how many. Where the conditions are met, the defeat test should be applied. Where they are not, this paper's argument does not apply. That is a narrower claim than "supermajority," and it is the claim the briefs actually support.

### 5.3 The honest disposition of the argument

Concede: genuine physical ceilings, safety-and-depreciation spending as the dominant share of the $151B ACI-NA need, O'Hare-class legitimate infrastructure cases, NextGen as a real warning about federal IT governance, SEA as a real warning about airport-level integration architecture, and the Gartner base rate as a real portfolio-selection constraint. Do not concede: the aggregate allocation ratio on the discretionary tranche, the false equivalence between federal-scale modernization and airport-level commercially productized operational technology, or the assumption that demand growth is physical when 39% of delay minutes come from late-arriving aircraft and 40% of NAS delays come from 19 understaffed ATC facilities. The case for an allocation shift is not a case against all concrete. It is a case against unexamined discretionary concrete, and for treating the operational intelligence stack as the first option to defeat rather than the last.

---

## 6. Implications for MWAA

MWAA is a two-airport authority running an airport at a federal-and-physical cap (DCA) and an airport with physical room but exposed hub economics (IAD). The allocation argument applies to both, but in different forms. This section names specific projects, specific operational-intelligence complements, specific investment envelopes, specific KPIs, and specific defeat tests. The Red Team was right that v1 Section 6 was the weakest section in the piece. V2 aims to fix that.

### 6.1 DCA: the physical-ceiling case, with nested constraints

DCA has two distinct binding constraints that the analysis has to separate. Constraint A: physical geography (Potomac, federal facilities, residential neighborhoods) plus a terminal designed for 15M annual passengers now serving 25M [Contrarian brief, Part I-1; Part II]. Constraint B: federal policy — a 62 takeoffs-or-landings-per-hour slot cap plus the perimeter rule [Contrarian brief, Part II]. Constraint A is physical and not movable. Constraint B is policy and is theoretically movable but has not moved despite decades of political pressure. The Red Team is correct that v1 conflated these.

The $2.4 billion DCA Project Journey program (Terminal B/C redevelopment within the 2025–2039 capital plan) is a response to Constraint A, not Constraint B [Economist brief, Evidence: MWAA-Specific]. It does not add flights; it handles passengers associated with the flights DCA is already allowed to operate. That makes the program legitimate — and, critically, it makes the program a *throughput-per-passenger* investment rather than a throughput-per-aircraft investment.

**Specific complement, envelope, KPI, defeat test.**

- **Specific project:** DCA Project Journey Terminal B/C redevelopment. Approximately $2.4B, within the $9B authority-level program [Economist brief, Evidence].
- **Operational intelligence complement (not substitute):** A coupled program — not a serially-following IT subline — of (i) security queue prediction and staffing optimization (Copenhagen Optimization / Xovis / Vision Platform AI category), (ii) biometric passenger processing at gates and immigration where federal rules allow, (iii) predictive gate resource allocation and ground coordination (computer-vision turnaround monitoring), and (iv) an airport operations data backbone that can serve all three. Deployable inside the construction schedule, not after it.
- **Indicative investment envelope:** $25–60M over 24–36 months for the full four-category stack, plus 10–20% annual recurring [Technology Scout brief, Evidence: Digital Twins, which sets that envelope at the large-hub level]. That is approximately 1–2.5% of the Project Journey capital budget.
- **KPIs with disclosed baselines (the SEA lesson):**
  - Security peak-hour wait time (median and 95th percentile) — target measurable reduction within 12 months of deployment; Copenhagen Optimization's 30–50% peak wait reduction across 40+ airports is the vendor benchmark and should be discounted toward the Munich-class low-double-digit range for a realistic ambition [Technology Scout brief, Finding 4, Queue Prediction].
  - Security throughput per FTE per hour — target directional movement toward Copenhagen's 42% improvement, with a disciplined, discounted target set pre-deployment [Technology Scout brief, Queue Prediction].
  - Taxi-out time median per departure — target Munich-class 9% reduction over 24 months [Technology Scout brief, Finding 4].
  - On-time departure performance — stripping schedule padding per Section 3.9, and with airline agreement on the padding-adjusted baseline.
- **Defeat test:** If after 24 months the deployed stack has not produced a statistically significant, disclosed-methodology, published reduction in at least two of the four KPIs, the authority pauses further operational-intelligence investment at DCA and commissions an independent post-mortem before committing additional capital. The defeat test is not "did it hit a vendor projection" — it is "did disclosed-baseline metrics move at all in the expected direction."
- **The architecture lesson from SEA:** the data backbone (unified AODB, real-time feeds from airlines and ground handlers, documented data-sharing agreements) is the first investment, not the seventh. SEA spent $13.4M integrating seven vendors without that backbone and produced no disclosed outcome [Technology Scout brief, Quotable 3]. DCA should not repeat that architecture.

### 6.2 IAD: the demand-exposed hub

Dulles has physical room. It has an active Concourse E expansion within the broader $9 billion 2025–2039 capital program [Economist brief, Evidence: MWAA-Specific]. It is a primary international gateway with legitimate long-haul hub economics. It is also the exposed flank of MWAA's balance sheet: DSCR projected to deteriorate from 2.79x in FY2024 to 1.70x by FY2030 even under favorable traffic assumptions [Economist brief, Finding 5], and adjusted debt per O&D enplanement at the system level peaking near $400 in 2028 [Economist brief, Finding 5] implicates Dulles most.

The CVG warning case applies to IAD more than to DCA. CVG's CPE rose from under $5 to over $10 on collapsing enplanements after Delta dehubbed [Economist brief, Finding 7]. IAD is not CVG, but it is more structurally exposed to airline network decisions than DCA is. A capital program sized to a traffic forecast that assumes continued hub commitment from United carries asymmetric risk: if the hub holds, the investment earns; if the hub thins, the investment encumbers the balance sheet with bond obligations that follow the Authority regardless of who is flying.

**Specific complement, envelope, KPI, defeat test.**

- **Specific project:** IAD Concourse E expansion within the $9B program. Exact sub-project cost is not disclosed at brief-level granularity; Authority filings should govern the number.
- **Staging proposal:** Segregate the Concourse E program into (i) a high-confidence core tranche — airside infrastructure, apron, and taxiway work tied to aircraft-size/NextGen compatibility requirements, code compliance, and asset renewal; and (ii) a demand-contingent tranche — additional gate count, hold room expansion, and terminal square footage justified by forecast international growth. The high-confidence core tranche proceeds on its own financial case. The demand-contingent tranche is subject to the defeat test.
- **Operational intelligence complement:** A-CDM / DMAN deployment at IAD paired with surface metering (TFDM-class), computer-vision turnaround monitoring at high-variance stands, and an APOC organizational container (see 6.5). Explicitly scoped to move IAD's throughput baseline before the demand-contingent tranche is committed.
- **Indicative investment envelope:** $30–75M over 24–36 months for the coupled stack, plus 10–20% annual recurring [Technology Scout brief, Evidence: Digital Twins; Evidence: A-CDM and DMAN]. A fraction of any single major Concourse E sub-project.
- **KPIs with disclosed baselines:**
  - Taxi-out time at IAD (median and 95th percentile per departure) — Munich-class 9% reduction as 24-month ambition [Technology Scout brief, Finding 4].
  - Off-block time predictability — Munich-class 7.8% improvement ambition [Technology Scout brief, Finding 4].
  - Turnaround delay median — Assaia-class 1-minute reduction as ambition, with the Technology Scout caveat on vendor-reported sampling transmitted openly [Technology Scout brief, Finding 7, Section 4].
  - Peak-hour aircraft movements achieved per runway per hour — baseline before A-CDM, tracked monthly after.
  - A-CDM network-effect risk: explicit internal tracking of whether IAD's isolated-deployment gains underperform the 17-airport EUROCONTROL benchmark, with a pre-registered acceptance criterion (e.g., the Munich single-airport benchmark is the floor; the 17-airport network benchmark is not) [Technology Scout brief, Finding 4].
- **Defeat test for the demand-contingent tranche:** If A-CDM + surface metering + turnaround monitoring at IAD move the peak-hour-movement KPI and the taxi-out KPI by measured amounts within 24 months, the demand-contingent Concourse E tranche is resized and rescheduled based on the higher baseline. If they do not move, the demand-contingent tranche proceeds on original terms — with the operational-intelligence program paused for independent review. Either outcome is a real decision rather than a default forward motion.

### 6.3 The financial envelope question

The authority is at a specific decision point that makes the allocation question concrete. The 2025–2039 plan is approximately 5.6x the prior cycle; $5.5 billion of new debt is scheduled for issuance 2025–2028; Moody's sector outlook is negative; the PFC cap is frozen at $4.50 [Economist brief, Finding 5, Finding 3]. In that environment, the marginal bond is more expensive, more scrutinized, and more consequential than at any point in the authority's recent history.

The operational intelligence allocation within this envelope should not be framed as a subtraction from infrastructure. It should be framed as an uplift to the revenue base that supports the infrastructure. A Munich-class 9% taxi time reduction [Technology Scout brief, Finding 4] or a EUROCONTROL-class 0–3 minute per-departure taxi-out saving across MWAA's annual operations translates into fuel savings, gate availability, and delay reductions that feed both airline economics (which shapes CPE tolerance) and passenger experience (which shapes non-aeronautical revenue). These are the same dollars.

Sizing: at the system level, a coupled DCA + IAD operational intelligence investment envelope of $55–135M over 36 months (combining 6.1 and 6.2 ranges) plus 10–20% annual recurring is roughly 0.6–1.5% of the $9B capital plan. That is a materially sub-one-percent allocation against a program facing the rating environment described above. It is not the heroic reallocation the shorthand suggests. It is a rounding-error allocation that buys a defeat test on a multi-billion-dollar discretionary tranche.

### 6.4 Governance: what "T5-class" actually means

The Red Team is correct that v1 invoked T5 without operationalizing it. The Economist brief notes Terminal 5 required "a two-year pre-construction study explicitly designed to avoid megaproject failure modes" [Economist brief, Evidence: Cost Overrun Case Studies]. Beyond that single primary-source sentence, the Stage 1 briefs do not detail T5's governance mechanisms. Rather than invoke a phrase the briefs do not unpack, this paper makes the governance ask concrete on its own terms:

- **Ring-fenced scope at contract signature.** Post-signature scope changes require board-level approval with disclosed cost impact. Denver Great Hall's public-private partnership terminated because cost-and-scope disputes were not managed at that level [Economist brief, Evidence].
- **Independent cost validation before each major gate.** Not contractor-provided cost, not owner-provided cost — third-party validation, published to the authority board.
- **Contractual clarity on risk allocation.** Which party bears escalation risk, design-change risk, weather-delay risk, regulatory-change risk is specified at signature and does not migrate.
- **Contingency reserve discipline.** Contingency is ring-fenced at the project level and cannot be cross-subsidized across the program without explicit board action.
- **Procurement discipline audited externally.** The DIA 2025 audit finding — "still is not following procurement procedures or requiring contractors to submit documentation of actual costs" [Economist brief, Evidence] — is the exact failure mode MWAA cannot replicate on a 5.6x program. An annual independent procurement audit published to the authority board is the check.

MWAA's $9B program at the 5.6x step-up threshold needs its governance architecture stress-tested by someone other than the people who wrote it. That is not a marketing claim; it is a specific audit and a specific set of procurement controls. Where the Stage 1 evidence does not disclose T5's exact mechanism, the paper substitutes an explicitly constructed list of failure-mode controls derived from the documented Denver, LAX APM, and Berlin cases.

### 6.5 The APOC question: the container, not the room

SFO opened the first serious US Airport Operations Center in January 2026 — a 22,000-square-foot facility with 67 workstations [Technology Scout brief, Section 4]. Documented operational results are not yet published. The facility is a container. It is not yet a capability.

EUROCONTROL's April 2025 APOC Performance Study reviewed Airport Operations Centre implementations across European airports, surveyed 62 participants from 34 airports, documented a catalogue of performance indicators and "reported benefits" — and notably did not itself quantify those benefits with audited before/after comparisons [Technology Scout brief, A-CDM and DMAN]. After years of APOC deployment in Europe, rigorous cross-airport performance comparison still does not exist in the literature. That is directly relevant to MWAA: the European APOC benchmark is less evidence-rich than the A-CDM or DMAN benchmark, and an APOC commitment should be sized accordingly.

MWAA has neither a DCA APOC nor an IAD APOC in the European sense. The question is not whether to build one. The question is whether the organizational, data, and governance architecture that makes an APOC coherent exists — a unified AODB, real-time feeds from all major operational stakeholders, formal data-sharing agreements with airlines and ground handlers, and accountable executive ownership of operational outcomes. Without that architecture, an APOC is a room with screens. With it, an APOC is the organizational container that makes every other operational intelligence investment compound.

**Specific steps (the prerequisite, before the room):**
- Internal audit of current AODB coverage and real-time feed completeness at both airports, published to the board.
- Data-sharing agreements with the five largest airlines and the major ground handlers, with agreed latency and completeness SLAs.
- A named accountable executive — not a committee — for operational performance outcomes at each airport.
- An indicative APOC investment envelope of $20–50M combined across both airports, staged behind the data-backbone prerequisite, not in front of it.
- KPI: taxi-out median, gate-availability predictability, on-time departure (padding-adjusted), weather-event recovery speed.
- Defeat test: if 18 months after data-backbone deployment the KPIs have not moved from a disclosed baseline, the APOC facility investment is deferred and reviewed.

### 6.6 What this piece is not

It is not a recommendation that MWAA pause Project Journey, halt Concourse E, or cancel any specific committed project. The pavement, the asset renewal, the code compliance, and the capacity components responsive to documented demand are legitimate investments. The thesis is narrower than the v1 wording implied and narrower than a casual reader might think. It is:

*The discretionary tranche of the next billion in MWAA CapEx — not the mandatory safety, asset-renewal, or physical-overload tranche — should have to pass a defeat test against a $55–135M operational intelligence alternative deployed first, measured against disclosed-baseline KPIs, with published outcomes and independent post-mortem authority.*

That thesis is the same across Sections 1, 3.10, and 6.6 of this draft. The Red Team was right that v1's thesis drifted across sections. V2 holds it.

The bond market, the rating agencies, and the authority's own DSCR trajectory now require that question be answered on the record, not assumed away. The next billion dollars is going to get built. It should be built knowing what $100M–$150M of operational intelligence would have done first — and knowing that the answer to that question is not allowed to be "we didn't ask."

---

*Draft v2. Inline citations reference the Stage 1 briefs. This draft addresses Red Team critique v1 issue-by-issue; where the critique was pushed back on rather than accepted, the disposition is argued in-text rather than elided. Fact-checker verification against source briefs to follow.*
