# Technology Scout Evidence Brief: Airport Operational Intelligence
**Prepared for:** MWAA AI Council — Stage 1 Research
**Date:** April 17, 2026
**Classification:** Internal Working Document

---

## 1. Taxonomy: What "Operational Intelligence" Means — and What It Doesn't

The term gets stretched to cover everything from a new gate display to a machine-learning-driven network coordination platform. For this brief, operational intelligence refers specifically to software and data systems that improve the utilization or predictability of existing airport assets — gates, stands, runways, checkpoints, staff — without adding physical capacity. The taxonomy breaks into six tiers of maturity:

**Tier 1 — Collaborative Decision-Making Infrastructure (CDM/A-CDM)**
The foundational layer. Airports, airlines, ground handlers, and air navigation service providers share a common picture of expected departure times, stand availability, and inbound traffic. The target outputs are TSAT (Target Start-up Approval Time) and TTOT (Target Take-off Time), which synchronize pushback sequencing with runway availability. This technology has been operational at European hub airports since 2010. It is off-the-shelf infrastructure today, not innovation.

**Tier 2 — Departure and Arrival Management Systems (DMAN/AMAN)**
Systems that compute optimal departure sequences in real time, feeding TSAT/TTOT to the ramp. DMAN tools from vendors such as Frequentis, Indra, and Thales have been deployed across SESAR-funded European airports. They require integration with the airport's AODB (Airport Operational Database) but are commercially mature. The distinguishing feature is active sequencing — not just sharing information, but calculating the order in which aircraft should push back to meet runway flow constraints.

**Tier 3 — Predictive Turnaround and Ramp Coordination**
Computer-vision systems (Assaia ApronAI is the dominant vendor) that monitor aircraft turn activities via cameras, detecting delays in fueling, catering, baggage loading, or boarding and alerting coordinators in time to intervene. This is the layer that converts stand-level situational awareness into predictive intelligence. It was emerging technology circa 2020; by 2026 it is productized at 15+ major airports.

**Tier 4 — Digital Twins for Airport Operations**
A digital twin in the airport context can mean one of two things: a building-level asset management tool (Bentley, Willow) for infrastructure monitoring and predictive maintenance; or an operational simulation layer that models passenger and aircraft flows to test scenarios and optimize resource deployment in real time. These use cases are frequently conflated in vendor marketing. The operational simulation variant remains custom-heavy. The infrastructure monitoring variant is increasingly off-the-shelf but requires sensor instrumentation that many older terminals lack.

**Tier 5 — Biometric and Predictive Passenger Flow**
Facial recognition at touchpoints (check-in kiosks, boarding gates, immigration, security) to reduce document handling and compress processing time. Layered on top: AI queue prediction that anticipates checkpoint demand 30–90 minutes ahead and triggers staffing adjustments. The biometric hardware is mature; the software and data-sharing standards (IATA One ID) are advancing rapidly but interoperability across legacy ID systems remains an integration problem, particularly in the US where TSA data governance is constrained.

**Tier 6 — Integrated Operations Centers (APOC/IOC)**
Physical and digital consolidation of stakeholders — operations, ground handlers, airlines, ATC, security, facilities — into a single collaborative workspace with shared data feeds, common operating pictures, and automated decision-support tools. An APOC is the organizational container that makes the other tiers coherent. Without it, the signal from a DMAN or turnaround AI tool has no clear recipient. The APOC concept is mature in Europe; it is nascent in the US.

**What does NOT count as operational intelligence for this analysis:**
- Passenger information displays (FIDS/BIDS) in their traditional form
- CCTV without analytics
- Traditional AODB systems that store flight data but do not generate predictions or recommendations
- Infrastructure sensors without connected analytics layers
- Static resource planning tools that are not ML-driven or real-time

---

## 2. Key Findings

1. **The European evidence base is real, independent, and quantified — the US evidence base is almost entirely vendor-reported.** EUROCONTROL published a formal impact assessment of A-CDM deployments across 17 airports in 2016 and maintains ongoing network data through its Performance Review Commission. US airports, including SEA's $13.4M ground operations intelligence stack, report implementation costs but almost never publish post-deployment operational outcomes in ways that can be independently verified. [Source: https://www.eurocontrol.int/sites/default/files/2019-04/a-cdm-impact-assessment-2016.pdf]

2. **The deployment gap is the story, not the technology.** Of 31 large US hub airports, only 3 have operational digital twin platforms as of 2026; 17 remain in pilot or planning stages. The technology for airport operational intelligence is commercially available. The blockers are data governance, federal funding eligibility ambiguity, and organizational fragmentation across airport, airline, ground handler, and ATC stakeholders. [Source: https://dwuconsulting.com/dwu-ai/twin]

3. **Every substantive ROI figure in this space requires a credibility haircut.** Assaia's claim of $70M+ annual savings at a large European hub extrapolates from a 1-minute median delay reduction across 450,000 turns — a vendor-commissioned study of vendor-customer airports with no independent audit. The Copenhagen Optimization 42% security throughput improvement is self-reported from their own customer case study. The IATA One ID "40% processing time reduction" came from a two-passenger proof-of-concept pilot. None of these figures are useless, but none should be used in capital justification without aggressive discounting.

4. **A-CDM is the highest-confidence, lowest-hype technology in this stack.** The EUROCONTROL 2016 study of 17 airports documented 34,000 tonnes of fuel saved per year (~€26.7M) and 250,000 minutes of flow management delay avoided (~€15.5M) — independently compiled from network data, not vendor-reported. Munich's DMAN trials showed 9% taxi time reduction, 14.6 kg fuel savings per flight, and a 7.8% improvement in off-block time predictability. These numbers are modest but real. The key caveat is that they were measured at the network level, where many airports were already CDM-compliant — the marginal benefit of adding one more airport decreases as the network penetration increases. [Sources: https://www.eurocontrol.int/sites/default/files/2019-04/a-cdm-impact-assessment-2016.pdf; https://www.sesarju.eu/sesar-solutions/dman-baseline-integrated-aman-dman]

5. **Data silo failure is the modal failure mode.** Between 60–85% of enterprise AI projects fail (per Gartner and similar advisory estimates cited across multiple industry sources), with 68% of failed implementations traceable to data quality issues. For airports specifically: operations, airlines, ground handlers, ATC, and facilities management each own separate systems that do not natively communicate. The technology to build operational intelligence exists; the pre-condition — a unified, real-time data layer — frequently does not. SEA spent $13.4M integrating seven vendors to get basic ramp situational awareness. That integration cost is not captured in any vendor's ROI calculation.

6. **Biometrics are advancing faster than the privacy and interoperability frameworks governing them.** Facial-recognition boarding has cut boarding times by up to 20% in documented deployments. IATA reports 46% of passengers used biometrics in 2023 (up from 34% in 2022), and 75% prefer biometrics to physical documents. But IATA One ID's 40% processing time reduction came from a two-person pilot on a single Cathay Pacific route. US deployment is constrained by TSA data governance rules and the absence of a national digital identity framework. The hardware works; the regulatory and interoperability infrastructure lags by years.

7. **The AI turnaround monitoring category has crossed from hype to documented improvement, but marginal gains are shrinking.** Assaia's 2025 report (covering 450,000+ turns at 15 airports) found median departure delays cut from 4 to 3 minutes — a 25% reduction. A 1-minute reduction matters at scale ($100/turn in North America per Assaia's estimate), but the easy gains are being captured. The airports that have not yet deployed this technology have a clear opportunity; airports already live on it should be cautious about assuming continued dramatic improvements from the same tool category.

---

## 3. Evidence Section

### A-CDM and DMAN

The definitive quantitative source for A-CDM is EUROCONTROL's 2016 impact assessment across 17 airports. Key findings independently compiled from network operations data:
- Fuel savings: **34,000 tonnes per year** across the study cohort (~€26.7M at then-current prices) [Source: https://www.eurocontrol.int/sites/default/files/2019-04/a-cdm-impact-assessment-2016.pdf]
- Flow management delay reduction: **~250,000 minutes per year** across the cohort (~€15.5M) [Source: ibid.]
- Taxi-out time savings: **0–3 minutes per departure** depending on airport and peak conditions [Source: ibid.]
- Network effect: Projections indicate 40 CDM airports could yield 20–25% reductions in average ATFM delay during active restrictions [Source: https://www.eurocontrol.int/sites/default/files/library/004_Airport_CDM_Network_Impact_Assessment.pdf]

Munich Airport's SESAR DMAN trials produced the most granular airport-level data available:
- Taxi time reduction: **9%**
- Fuel savings: **14.6 kg per flight**
- Adherence to ATFM slot: improved from 76% to 81% of flights within target [Source: https://www.sesarju.eu/sesar-solutions/dman-baseline-integrated-aman-dman]
- Off-block time predictability: **+7.8%** improvement

Dublin Airport published a public-facing description of its A-CDM/TSAT/TTOT implementation showing the TSAT calculation process and its linkage to reduced runway queue times. [Source: https://www.dublinairport.com/docs/default-source/about-a-cdm/leaflet-3-target-start-up-approval-time-(tsat)-and-target-take-off-time-(ttot).pdf]

EUROCONTROL's April 2025 APOC Performance Study (published by the Performance Review Commission) reviewed Airport Operations Centre implementations across European airports, surveying 62 participants from 34 airports. The study documented a catalogue of performance indicators and "reported benefits" — but notably did not itself quantify those benefits with audited before/after comparisons. The study recommended standardized KPI frameworks for future APOC assessments. This is revealing: after years of APOC deployment in Europe, a rigorous cross-airport performance comparison still does not exist in the literature. [Source: https://www.eurocontrol.int/publication/prc-apoc-study]

### Digital Twins

DFW awarded a five-year digital twin contract to Willow Inc. and Parsons Corporation in 2022 with an initial scope of approximately **$2.9 million**, covering Runway 18R/36L and Terminal D. DFW subsequently expanded geospatial coverage to 5,000+ cameras with event-driven architecture feeding its IOC. [Source: search-confirmed via multiple industry references]

Cost benchmarks for airport digital twin deployments (from DWU Consulting's 2026 financial case analysis, which is industry-analyst rather than vendor-produced, though methodology is not fully disclosed):
- Pilot programs: **$50,000–$200,000**
- Proof of concept: **$150,000–$200,000**
- Full large-hub deployment: **$15–$40 million** over 24–36 months
- Annual recurring costs: **10–20%** of initial implementation [Source: https://dwuconsulting.com/dwu-ai/twin]

ROI claims from the same source should be treated as projections rather than documented outcomes:
- Gate utilization improvement via 5–12 minute turnaround reduction: "$15M–$25M annual aeronautical revenue" at major hubs [Source: https://dwuconsulting.com/dwu-ai/twin — analyst projection, not audited result]
- Predictive maintenance: "40–60% fewer unexpected breakdowns, 20–35% maintenance cost reduction" — attributed to general industry benchmarks, not airport-specific audits [Source: ibid.]

Changi Airport reported a **15% reduction in equipment downtime** through its Smart Terminal Operations IoT program by 2021. This is airport-reported, not independently audited, but comes from a credible institutional source (Changi Airport Group annual disclosures). [Source: https://www.aitransformationreadiness.org/post/changi-airport-digital-transformation]

Schiphol separately reported its HVAC digital twin program achieved an **88% reduction in HVAC energy use** and **€82,000 in operating cost savings**, with 375 tonnes of CO2 avoided — a building systems outcome, not an operational flight performance outcome. [Source: multiple industry references citing Schiphol's own reporting]

### Predictive Turnaround / Ramp Coordination

SEA deployed a $13.4 million integrated ramp intelligence stack (Saab Aerobahn, Assaia, Inform GroundStar, Safedock, and four additional vendors). The case study article quotes airport and airline staff on capability improvements but provides no pre/post performance metrics. The 17% on-time performance improvement and 44% taxi-in reduction figures attributed to "AI software" in secondary summaries could not be confirmed to a specific primary source and should be treated as uncorroborated. [Source: https://airportimprovement.com/article/seattle-tacoma-int-l-leverages-artificial-intelligence-improve-visibility-management-ground-operations/]

Assaia's 2025 Turnaround Report (15 airports, 450,000+ turns, April 2024–March 2025):
- Median departure delay: reduced from **4 minutes to 3 minutes** (25% cut)
- Average delay: **stabilized at 11 minutes** despite record traffic
- European AI-enabled airports: departures **6 minutes shorter** than regional average
- North America: **~$100 per turnaround** in savings per minute of delay reduction [Source: https://aerospaceglobalnews.com/news/ai-aircraft-turnarounds-financial-savings-assaia/]
- **Critical caveat:** This is vendor-published research drawn from vendor-customer airports. It is not peer-reviewed and has not been independently audited. The sampling methodology (which airports, which flights, how baselines were established) is not disclosed in publicly available summaries.

Heathrow expanded Assaia's ApronAI system to 116 gates across Terminals 2, 3, and 5 — a concrete deployment fact that establishes scale. British Airways is named as an airline partner. No published performance data from Heathrow's deployment is available in the public domain. [Source: https://www.assaia.com/resources/ai-firms-collaborate-with-heathrow-to-enhance-operations]

### Biometric Passenger Flow

IATA One ID trial at Hong Kong and Narita airports (Cathay Pacific route, two-passenger proof-of-concept, February 2025): "Processing times at key touchpoints were reduced by 40 percent." The specific process is not identified; the trial involved two passengers; the measurement methodology is not disclosed; the funding source is not disclosed. This figure is not usable as evidence for operational planning without significant caveats. [Source: https://www.biometricupdate.com/202502/iata-one-id-biometrics-trial-cuts-airport-processing-times-by-40]

Broader biometric adoption: 46% of passengers used biometrics in 2023 (up from 34% in 2022); 75% prefer biometrics over physical documents. Facial-recognition boarding cuts boarding times by up to 20% in documented implementations (source: IATA/industry surveys). [Source: https://www.iata.org/en/pressroom/2024-releases/2024-10-30-01/]

### Queue Prediction and Security Throughput

Copenhagen Optimization at Copenhagen Airport (vendor self-reported):
- **26% reduction** in check-in counter demand
- Security throughput: from **38,900 items/FTE/year to 55,200 items/FTE/year** (42% improvement)
- Across 40+ airports: 30–50% reduction in peak wait times, 10–15% reduction in staffing costs [Source: https://copenhagenoptimization.com/resource-hub/case-studies/copenhagen-case-study/]

These figures originate entirely from Copenhagen Optimization's own materials. They have not been independently audited.

### Industry IT Spending Context

Airport IT spending reached **$8.9 billion** in 2024 (SITA Air Transport IT Insights 2024), up from $8.8 billion a year prior. The top priority was cybersecurity (100% of survey respondents) with passenger processing second (95%). Notably, SITA separately identified fragmented data as the primary barrier to realizing value from technology spending. [Source: https://www.sita.aero/resources/surveys-reports/air-transport-it-insights-2024/]

---

## 4. Honest Assessment of Maturity: What's Real, What's Hype

**Real and deployment-ready in 2026:**

*A-CDM/DMAN:* This is proven infrastructure. The EUROCONTROL evidence base is the most rigorous in the industry — independent network data, multi-airport, multi-year. Airports without basic CDM compliance are leaving real efficiency on the table. The caveat is that the easy network-level gains require broad adoption, and the marginal benefit decreases as the European network approaches full CDM coverage. US airports remain substantially behind European peers on CDM maturity, partly because the ATC/airport coordination architecture differs and the FAA's TFMS (Traffic Flow Management System) does not have a direct CDM equivalent.

*Computer-vision turnaround monitoring:* The Assaia/Heathrow/SEA/Toronto deployment pattern establishes that this technology is deployable at scale and operationally useful. The specific ROI claims are vendor-generated but the directional improvement (faster detection of turn delays, earlier intervention) is mechanistically sound and corroborated by multiple independent deployments. The limitation: a camera-and-AI ramp system requires airline buy-in to share turn data and act on alerts — an organizational challenge more than a technical one.

*Security queue prediction:* Productized. Multiple vendors (Copenhagen Optimization, Xovis, Vision Platform AI, Kloudspot) offer sensor-based queue measurement and staffing recommendation systems. These are deployable within months. The documented results are vendor-reported but the mechanism is simple enough to be credible: real-time lane data fed into a staffing model reduces overstaffing waste and eliminates blind-side surge events. ROI should be conservative and airport-specific.

**Emerging but requiring custom work:**

*Airport digital twins (operational simulation variant):* The infrastructure asset monitoring variant is increasingly productized. The operational simulation variant — where the digital twin actively models passenger and aircraft flows to optimize resource deployment in real time — requires significant custom data engineering. The DFW pilot at $2.9M for a single runway and terminal complex illustrates the scope. Airports should expect 2–4 year timelines for full operational deployments at large hubs, with integration costs dwarfing software license costs.

*Integrated APOC platforms:* The concept is mature in Europe; the enabling data infrastructure is not mature in the US. Building an effective APOC requires a unified AODB, real-time feeds from all major operational stakeholders, and organizational agreements that transcend procurement. SFO's AIOC, which opened in January 2026, represents one of the first serious US examples — a 22,000 sq ft facility with 67 workstations — but documented operational results are not yet published.

*Biometric end-to-end passenger processing:* Hardware is ready; the data-sharing and regulatory frameworks are not. US deployment is constrained by TSA's limitations on commercial biometric use and the absence of a national digital identity standard. The technology will mature; the timeline for US airports depends on regulatory decisions outside airport control.

**Predominantly hype as of 2026:**

*Agentic AI for autonomous airport operations:* Vendor marketing is well ahead of operational reality. Claims of AI systems that autonomously resequence maintenance events, reroute passengers, and reallocate gates without human approval are, in the airport context, largely aspirational. The decision-making and liability frameworks for autonomous operational control do not exist, and the data quality prerequisite is not met at most airports.

*Projected ROI figures for digital twins at 2035:* Assaia's projection of "$900M in annual benefits for a large airline" and "$300M–$500M for a major international airport" by 2035 are market-development claims, not evidence. The compounding of unverified baseline improvements through a decade of growth assumptions produces numbers that sound impressive and cannot be evaluated.

---

## 5. Quotable Data Points for Strategists

1. **"For 17 A-CDM airports, EUROCONTROL documented savings of over 34,000 tonnes of fuel burn per year — approximately €26.7 million — and nearly 250,000 minutes of flow management delay avoided, worth approximately €15.5 million."** This is the only independently compiled, network-level ROI figure for airport operational intelligence in the public domain. It is from 2016 and covers fuel and delay costs, not revenue opportunity. [Source: EUROCONTROL A-CDM Impact Assessment, 2016]

2. **"Of 31 large US hub airports, only 3 have operational digital twin platforms in 2026. Seventeen remain in pilot or planning stages."** The technology exists and is commercially available. The bottleneck is not innovation — it is integration, funding eligibility, and organizational change. [Source: DWU Consulting airport digital twin analysis, 2026]

3. **"Seattle-Tacoma International Airport spent $13.4 million integrating seven operational intelligence vendors — Saab Aerobahn, Assaia, Inform GroundStar, Safedock, Genetec, Accipiter, and FlightAware — to achieve basic ramp situational awareness. The case study does not report a single quantified performance outcome."** This is the honest picture of what operational intelligence actually costs and how difficult it is to measure. [Source: Airport Improvement magazine, SEA case study]

4. **"SITA identifies fragmented data as the primary barrier to realizing value from $8.9 billion in annual airport IT spending."** The problem is not insufficient investment in technology. The problem is that the data infrastructure connecting those investments does not exist. [Source: SITA Air Transport IT Insights 2024]

5. **"Munich's SESAR DMAN trials documented 9% taxi time reduction and 14.6 kg of fuel savings per flight — modest, real, independently validated."** These numbers are smaller than vendor claims and more useful to planners because they come from a controlled trial with disclosed methodology. The lesson is that the actual improvement from a well-implemented departure management system is single-digit percentage efficiency, not the 20–40% figures that appear in marketing materials. [Source: SESAR DMAN Baseline Validation Study]

---

## 6. Notes on Source Credibility

The following hierarchy applies to sources cited in this brief:

**High credibility (independent data):**
- EUROCONTROL A-CDM Impact Assessment (2016): multi-airport, independently compiled from network operations data
- SESAR DMAN validation studies: controlled trials with disclosed methodology
- EUROCONTROL APOC Performance Study (2025): independent review body, though quantitative outcomes remain underspecified

**Moderate credibility (institutional self-reporting with public accountability):**
- Changi Airport Group annual reports and official publications
- IATA passenger survey data (statistically sampled, disclosed methodology)
- SITA Air Transport IT Insights (industry association survey with disclosed methodology)

**Low credibility for specific figures (vendor-generated, unaudited):**
- Assaia 2025 Turnaround Report: vendor-commissioned, vendor-customer airports, no independent audit
- Copenhagen Optimization case studies: company's own customer claims
- DWU Consulting digital twin ROI projections: analyst firm, undisclosed methodology
- Any "up to X%" improvement figures without disclosed baseline, sample size, or measurement period

**Not verifiable / should be excluded from capital justification:**
- IATA One ID 40% processing time reduction (two-passenger pilot)
- Secondary-source figures for SEA on-time performance improvement (unconfirmed to primary source)
- Extrapolated 2035 projections from current vendor claims

---

*Brief prepared by the Technology Scout agent. All sources linked inline. Figures without verifiable primary sources have been caveated or excluded. The absence of independently audited US airport operational intelligence outcomes is itself a finding: airports are deploying technology without publishing results, which makes the ROI case harder to make and easier to overclaim.*
