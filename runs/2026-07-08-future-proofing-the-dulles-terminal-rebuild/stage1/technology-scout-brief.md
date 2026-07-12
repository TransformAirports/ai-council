# Technology Scout Brief: What "Operational Intelligence" Actually Costs and Returns

**Run:** Future-Proofing the Dulles Terminal Rebuild
**Lens:** Airport operational technology — what deploys, what it costs, what it returns, and what it means for built form
**Date:** 2026-07-08

---

## Why this brief matters to the Dulles decision

Operational intelligence is a *volatile-layer* asset. Every system in this brief — A-CDM, predictive turn, digital twins, biometric flow, ops-center dashboards — has a useful life of 5 to 15 years and is replaced or re-platformed on that cadence. None of it belongs to the 50-year structural spine. The design mistake is not "which software do we buy" — that decision should be deferred and re-made repeatedly. The design mistake is failing to provision the *durable* substrate these systems all require: conduit, power density, camera/sensor sightlines, riser and comms pathways, an apron instrumented for computer vision, and a clean operational data architecture. Provisioning is cheap now and unaffordable to retrofit into a finished terminal. The software is the opposite. That inversion is the whole point.

So this brief does two things: it defines operational intelligence rigorously and prices it, and it separates the vendor narrative from what airports have actually measured.

---

## 1. A taxonomy: what counts as operational intelligence, what doesn't

Operational intelligence is the layer that turns airport telemetry into *decisions that change resource allocation in the next minutes-to-hours*. It is not passenger-facing convenience tech, and it is not enterprise IT. The test: does it move an aircraft, a gate, a staff member, or a queue in near-real-time based on a prediction? Four tiers:

**Tier 1 — Coordination protocols (data-sharing, not analytics).** A-CDM and its milestone times (TOBT, TSAT, TTOT). This is a shared-data discipline that synchronizes airport, airline, ground handler, and ATC on a common departure sequence. Mature, standardized, mandated in Europe. Low technology risk; high organizational-change risk.

**Tier 2 — Predictive operational systems.** Predictive turnaround (computer-vision ApronAI/TurnaroundControl), stand-and-gate optimization, queue/passenger-flow forecasting, predictive maintenance. These forecast a milestone or a bottleneck 30–120 minutes ahead and prescribe an action. This is where the near-term ROI lives — and where most vendor claims concentrate.

**Tier 3 — Integrated command layer.** The APOC/AOCC ("virtual operations center") — a dashboard that fuses Tier 1 and Tier 2 feeds into one operating picture with event-driven alerts. Off-the-shelf in 2026 but only as good as the feeds beneath it.

**Tier 4 — Digital twin.** A live, physics-and-data model of the facility used for simulation, predictive maintenance, and what-if planning. Highest theoretical impact, widest deployment gap, most illustrative (i.e., unaudited) ROI.

**What does NOT count:** biometric identity itself is passenger *processing*, not operational intelligence — but the *flow analytics* riding on biometric and sensor data (queue prediction, throughput balancing) does count. Retail personalization, mobile apps, and Wi-Fi analytics are commercial tech, not operations. Keeping this boundary clean matters because vendors deliberately blur it to inflate the category's ROI.

---

## 2. Key findings

- **The measured returns are real but modest; the large returns are modeled, not audited.** A-CDM's independently assessed benefit is 0.25–3 minutes of taxi-out saved per departure [Source: https://www.eurocontrol.int/publication/airport-collaborative-decision-making-cdm-impact-assessment]. The headline "$900M per airline / $300–500M per hub" figure is a vendor's own projection to 2035 [Source: https://www.assaia.com/resources/ai-optimised-aircraft-turnarounds-are-unlocking-billions-in-long-term-value-for-airports-and-airlines]. The gap between those two numbers *is* the maturity story.

- **Predictive turnaround is the most deployment-ready Tier 2 system in 2026.** Computer-vision turn monitoring (Assaia) is live at SEA, JFK T4, Heathrow, Gatwick, Berlin, Toronto — dozens of airports, off-the-shelf, camera-based. This is the single technology most worth provisioning for at Dulles (apron sightlines, camera power/data).

- **The durable requirement under every one of these systems is the same: sensors, sightlines, conduit, power, and clean data.** Schiphol's operational intelligence rides on 80,000+ indoor/outdoor sensors [Source: https://dwuconsulting.com/dwu-ai/twin]. That instrumentation layer is a built-form decision, not a software one.

- **Digital twins have a wide "deployment gap": clear financial case, almost no live large-hub instances.** Only DFW operates an established U.S. large-hub twin; 17 of 31 U.S. large hubs remain in pilot or planning [Source: https://dwuconsulting.com/dwu-ai/twin]. Buying a twin in 2026 is buying a program, not a product.

- **The dominant failure mode is organizational, not technical.** Over 50% of GenAI/analytics pilots are abandoned after proof-of-concept; deployments without C-level sponsorship are 3x more likely to stall [Source: https://intuitionlabs.ai/pdfs/enterprise-ai-rollout-failures-causes-and-case-studies.pdf]. Denver's baggage disaster failed because airlines were never brought into planning [Source: https://www.wrike.com/blog/lessons-learned-from-project-failure-at-denver-international-airport-why-checking-bags-is-still-a-pain/].

- **Nearly every quoted ROI is self-reported by the operator or the vendor.** Changi's "15% equipment downtime reduction, 20% queue-management improvement" and Dubai's "OTP 80%→95%" are operator/vendor statements, not third-party audits [Source: https://dwuconsulting.com/dwu-ai/twin]. Treat them as directional, not bankable.

- **The command layer (APOC) is a commodity; the value is in the feeds.** Amadeus, TAV, Barco, WAISL, and others sell integrated ops-center platforms off-the-shelf in 2026 [Source: https://amadeus.com/en/airports/products/virtual-airport-operations-center-apoc]. A dashboard over dirty or missing data produces a confident-looking wrong answer.

- **Biometric/flow analytics scaled fast — 350+ airports, doubled in three years** [Source: https://www.travelaiagent.com/research/airport-operations-vendor-benchmark-2026] — but "4–5x throughput at equipped gates" is a 2026 vendor benchmark, and it is the *gates equipped*, not the whole terminal, that improve.

---

## 3. Evidence

### A-CDM (Tier 1) — the best-documented, most independently measured category
A-CDM is fully implemented at 34+ European airports including Heathrow and Munich (Brussels first, Munich second) [Source: https://www.eurocontrol.int/concept/airport-collaborative-decision-making]. EUROCONTROL's 17-airport impact assessment is the closest thing to an independent audit in this whole field: taxi-out time reduced by roughly 0.25–3 minutes per departure; the standard deviation of take-off times roughly halved (≈14 → ≈7 minutes), improving predictability; on-time performance improved 0.5–2 minutes per flight; and ATFM delay reductions of up to 20–25% projected as network participation scales [Source: https://www.eurocontrol.int/publication/airport-collaborative-decision-making-cdm-impact-assessment]. These are small per-flight numbers that compound into real fuel and slot value at hub volume — and notably, they come from a data-sharing protocol, not an AI product. The lesson for Dulles: the cheapest operational intelligence is a shared data standard and the discipline to use it.

### Predictive turnaround & stand optimization (Tier 2) — the deployment-ready category
Assaia's ApronAI/TurnaroundControl uses fixed cameras and computer vision to predict off-block times and turn milestones, live at SEA, JFK T4 (JFKIAT), Heathrow, Gatwick, Berlin Brandenburg, and Toronto Pearson [Source: https://www.assaia.com/resources/ai-optimised-aircraft-turnarounds-are-unlocking-billions-in-long-term-value-for-airports-and-airlines]. Heathrow is expanding ApronAI to 116 gates with 540 additional cameras inside its ~£2.3bn capital program [Source: https://dwuconsulting.com/dwu-ai/twin]. Vendor-reported aggregate results across operating airports: ~25% reduction in departure delays and ~5% gate-efficiency improvement, from analysis of 450,000+ turns at 15 airports (April 2024–March 2025) [Source: https://www.assaia.com/resources/ai-optimised-aircraft-turnarounds-are-unlocking-billions-in-long-term-value-for-airports-and-airlines]. **Attribution caveat:** this is Assaia's own 2025 Turnaround Report, authored and quoted by its CEO, with no independent auditor named. The "$900M airline / $300–500M hub by 2035" figure is a modeled projection, not observed. The observed, defensible claim is the DFW-style capacity logic: one or two additional daily gate rotations translate to roughly $15–25M/year in aeronautical revenue at a large hub [Source: https://dwuconsulting.com/dwu-ai/twin] — a *capacity* gain, which the same source is careful to label "illustrative," not a dollar-for-dollar receipt.

### Passenger-flow & queue prediction (Tier 2)
Modern models forecast where congestion will form 30–60 minutes ahead (up to ~2 hours in experimental settings) using flight schedules, historical patterns, weather, and live sensor feeds [Source: https://www.travelaiagent.com/research/airport-operations-vendor-benchmark-2026]. Biometric processing is now at 350+ airports, doubled in three years [Source: https://www.travelaiagent.com/research/airport-operations-vendor-benchmark-2026]. The broader smart-airport market is projected to grow from ~$8.59B (2025) to ~$22.71B (2035), ~10.2% CAGR [Source: https://www.travelaiagent.com/research/airport-operations-vendor-benchmark-2026] — a market-sizing figure, which is a demand signal, not evidence of returns.

### Integrated ops centers (Tier 3)
Off-the-shelf in 2026: Amadeus Virtual APOC (built with Microsoft, Teams-integrated, event-driven alerts and prescriptive analytics) [Source: https://amadeus.com/en/airports/products/virtual-airport-operations-center-apoc]; TAV AirportCockpit; Barco OpSpace; WAISL AeroWise; and AirportCOCKPIT, which signed launch contracts at Passenger Terminal Expo 2026 [Source: https://www.eurocontrol.int/sites/default/files/2026-05/eurocontrol-prc-apoc-factsheets-ed-2026.pdf]. EUROCONTROL now publishes an APOC factsheet series (2026 edition), a sign the concept has standardized. Munich runs one of the reference AOCC implementations [Source: https://www.munich-airport.com/international/airport-operations-control-centers].

### Digital twins (Tier 4) — strongest hype-to-deployment gap
McKinsey forecasts digital twins as having the highest overall potential impact of any novel digital technology for airports [Source: https://www.mckinsey.com/industries/travel/our-insights/smart-airports-clearing-the-runway-for-digital-takeoff] — a forecast, not a measurement. Concrete deployment reality: DFW's twin is a five-year Willow/Parsons contract valued at ~$2.9M covering Runway 18R/36L and Terminal D [Source: https://dwuconsulting.com/dwu-ai/twin]; the ACRP research project (03-66) that codified airport-twin practice was funded at just $350K [Source: https://dwuconsulting.com/dwu-ai/twin]. Schiphol's Common Data Environment fuses BIM, GIS, and live feeds from 80,000+ sensors; self-reported building-scale results include HVAC energy cut by up to 88%, ~€82,000 operating-cost savings, and 375 tonnes of CO₂ avoided [Source: https://dwuconsulting.com/dwu-ai/twin]. Changi used a twin on Terminal 4 for real-time planning and scenario simulation, reporting 15% equipment-downtime reduction (by 2021) and 20% queue-management improvement (by 2022) [Source: https://www.internationalairportreview.com/article/297689/singapore-changi-international-airport-the-benchmark-for-smart-airports/]. Dubai reports OTP improving from ~80% to ~95% and ~5 minutes off turnaround [Source: https://dwuconsulting.com/dwu-ai/twin]. **Every one of these is operator- or vendor-reported.** The category's own analysts concede: "the financial case for airport digital twins is clear but the deployment gap remains wide" [Source: https://dwuconsulting.com/dwu-ai/twin].

### Failure taxonomy — the record is about people and data, not algorithms
- **Denver DIA automated baggage (the canonical warning):** budgeted $193M, spent ~$311M, ~$560M over the airport's budget overall, 16-month opening delay, and ultimately a ~$80M manual backup system built after automation failed testing. Root cause: excessive complexity the consultants flagged and the city pursued anyway — and airlines, the most affected stakeholder, were left out of planning [Source: https://www.wrike.com/blog/lessons-learned-from-project-failure-at-denver-international-airport-why-checking-bags-is-still-a-pain/].
- **Heathrow T5 baggage:** failed at 2008 opening and failed again in May 2026 (~20,000 bags stranded), a reminder that even mature, centralized systems remain brittle single points of failure [Source: https://spectrum.ieee.org/baggage-problem-hits-heathrow-terminal-5-].
- **Analytics/AI generally:** >50% of GenAI projects abandoned after PoC; no C-level sponsor → 3x more likely to stall in integration [Source: https://intuitionlabs.ai/pdfs/enterprise-ai-rollout-failures-causes-and-case-studies.pdf]. McKinsey's own framing: many airports "harbor grand ambitions" but "few are capturing measurable results," with projects "stuck in pilot mode" on legacy systems and scattered data [Source: https://www.mckinsey.com/industries/travel/our-insights/smart-airports-clearing-the-runway-for-digital-takeoff].

---

## 4. Maturity assessment: what's real, what's hype in 2026

**Real and buyable off-the-shelf today:**
- A-CDM protocol and TOBT/TSAT/TTOT milestone discipline (standardized, mandated in Europe, proven).
- Camera-based predictive turnaround and stand optimization (Assaia and peers — dozens of live airports).
- APOC/AOCC dashboard platforms (Amadeus, TAV, Barco, WAISL).
- Biometric processing and queue-forecasting analytics (350+ airports).

**Real but still a custom program, not a product:**
- The digital twin. You can buy the platform (Willow, Bentley, NVIDIA Omniverse-based) but the *working* twin — integrated, live, trusted for decisions — is bespoke integration work. Budget it as a multi-year program with an uncertain payoff, not a procurement.
- Cross-stakeholder data integration. The APOC is a commodity; getting airlines, handlers, concessionaires, and ATC to share clean, timely data into it is the hard, human 80% of the work.

**Hype — treat timelines as bets:**
- "$900M/$300–500M perfect-turn" and similar 2035 projections. Vendor-modeled, unaudited, contingent on universal adoption.
- Digital twins as "highest-impact technology." A forecast repeated until it sounds like a finding.
- Fully autonomous, self-optimizing operations. No large hub runs on this; every live system is decision-support with a human in the loop.

**The honest through-line:** independently measured returns are small-but-compounding (A-CDM minutes; turnaround minutes). The large returns are all modeled. A strategist should assume the *category* works and the *specific dollar claims* don't — and should design the terminal so that whichever product wins the next decade can be plugged into a substrate that's already there.

---

## 5. Verbatim data points for the strategist

1. "A-CDM implementation reduced taxi-out times by roughly 0.25 to 3 minutes per departure and roughly halved the standard deviation of take-off times, from about 14 to 7 minutes." — EUROCONTROL 17-airport impact assessment [Source: https://www.eurocontrol.int/publication/airport-collaborative-decision-making-cdm-impact-assessment]. *Use it as the field's one genuinely independent measurement.*

2. "The financial case for airport digital twins is clear but the deployment gap remains wide — only one U.S. large hub (DFW) operates an established twin, and 17 of 31 remain in pilot or planning." [Source: https://dwuconsulting.com/dwu-ai/twin]. *Use it to puncture twin hype without dismissing the technology.*

3. "By 2035, consistently achieving the 'perfect turn' could generate up to $900 million annually for a major airline and $300–500 million for a large hub airport." — Assaia's own 2025 Turnaround Report, CEO-authored, no independent auditor [Source: https://www.assaia.com/resources/ai-optimised-aircraft-turnarounds-are-unlocking-billions-in-long-term-value-for-airports-and-airlines]. *Use it as the archetype of a vendor projection dressed as a finding.*

4. "Denver's automated baggage system ran ~$560M over budget and delayed opening 16 months — and the airlines most affected were never brought into the planning." [Source: https://www.wrike.com/blog/lessons-learned-from-project-failure-at-denver-international-airport-why-checking-bags-is-still-a-pain/]. *Use it as the case for governance-first, stakeholder-inclusive tech decisions.*

5. "Schiphol's operational intelligence runs on more than 80,000 indoor and outdoor sensors across a 7,000-acre campus." [Source: https://dwuconsulting.com/dwu-ai/twin]. *Use it to make the built-form point: the durable investment is the instrumentation layer, not the software on top of it.*

---

## Bottom line for the $22B rebuild

Do not design the terminal around any specific operational-intelligence product; every one of them will be replaced twice before the building is 50 years old. Do design the terminal to be *instrumentable to the teeth*: dense conduit and power at the apron and in the terminal, camera and sensor sightlines with dedicated data paths, an apron laid out for computer vision, generous comms risers, and — the one genuinely durable software decision — a clean, open operational-data architecture that any future vendor can plug into. Provision heavily for the volatile layer now, because retrofitting sightlines and conduit into a finished mega-terminal is the expense you cannot undo. The software you can always re-buy.
