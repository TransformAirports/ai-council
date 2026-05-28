# Technology Scout Brief: Operational Intelligence and Sterile Corridor Performance

**Run:** Sterile Corridor Resilience
**Stage:** 1 — Research
**Date:** 2026-05-27
**Scope:** Sensing, simulation, and digital analytics tools as instrumentation for corridor performance — not as substitutes for physical capacity

---

## 1. Taxonomy: What "Operational Intelligence" Means in This Context

For sterile corridor design, operational intelligence is any technology that measures, models, or predicts pedestrian throughput, density, or failure states in corridor space — and feeds that information into a decision (design, capital, or operational). The taxonomy has three tiers:

**Tier 1 — Design-Phase Simulation (load-bearing for approvals, rarely revisited)**
Tools in this category produce the pedestrian flow models that justify corridor widths, vertical circulation sizing, and level-of-service projections before a building opens. MassMotion (Arup/Oasys), AnyLogic, SimWalk, and Pathfinder (Thunderhead Engineering) are the primary platforms. These models drive design certification. They are not continuous monitoring tools. Once a building opens, they are almost never reopened to compare predictions against measured flows.

**Tier 2 — Operational Sensing (deployed at checkpoints, rarely at corridor midpoints)**
These tools measure actual passenger movement in real time. The main vendor categories are: 3D stereo-optical sensors (Xovis), Bluetooth/WiFi probe tracking (BlipTrack, now part of Veovo), and LiDAR arrays (Veovo's 2024 product addition, Outsight). They are predominantly deployed at high-value chokepoints — security lanes, immigration halls, check-in — not in the linear corridor segments that connect them. Corridor-level flow measurement (sustained density and directional flow along a 200-meter sterile corridor, for example) is not the primary use case for any of these platforms as commercially deployed at named airports.

**Tier 3 — Digital Twins (airport-wide data integration, mostly apron/equipment focused)**
Airport digital twins integrate IoT sensor data, AODB feeds, and building management systems into a unified visualization. The operational gains most documented in published case studies are in aircraft turnaround, equipment maintenance, and gate utilization — not in sterile corridor throughput. The passenger flow component of deployed digital twins is real but thin: it captures aggregate terminal occupancy, not corridor-segment density.

**What does not count as operational intelligence for this analysis:**
- A-CDM and TSAT/TTOT systems (airside departure sequencing — no terminal circulation component)
- Biometric enrollment and e-gate throughput optimization (checkpoint, not corridor)
- Ramp coordination platforms (TOBT, ground handler sequencing)
- Dynamic wayfinding signage driven by flight data (output to passengers, not flow measurement input to operators)

These are legitimate airport technology investments. They are not instrumentation for sterile corridor performance.

---

## 2. Key Findings

**1. The simulation-to-reality gap is real and undocumented.** MassMotion, AnyLogic, and SimWalk are used extensively during design to size corridors and justify level-of-service projections. A 2022 review of airport terminal pedestrian simulation practice found that "any references reporting validation of simulation results for pedestrian behavior in airport terminals were not identified" — making post-occupancy comparison a research gap rather than a standard practice. [Source: https://dl.acm.org/doi/10.1145/3745676.3745689] No published study was found comparing a pre-opening MassMotion prediction for a named airport concourse to a post-occupancy measured flow at the same point. This is the methodological exposure at the center of the corridor-sizing problem: the models that justify design decisions are not validated after the fact.

**2. Operational sensing is deployed at chokepoints, not at corridor midpoints.** Xovis reports deployment at over 120 airports and nearly 700 "mission-critical touchpoints." [Source: https://www.xovis.com/solutions/airport] Those touchpoints are security queues, check-in desks, immigration, and bag claim — not the 150- or 300-meter sterile corridor segment between an AeroTrain station and the nearest gate cluster. Veovo's corridor measurement capability exists (explicitly marketed for "long corridors, extended lines") [Source: https://veovo.com/insights/articles/a-guide-to-the-airport-passenger-tracking-sensor-landscape] but published case studies at named airports (Birmingham, CVG, Budapest) show corridor-level measurement described in capability terms, not in documented outcomes with measured throughput data. The CVG case study published by Veovo contains no quantified corridor-specific metrics — it emphasizes platform capability. [Source: https://veovo.com/insights/case-studies/enabling-smarter-decisions-at-cvg-airport-with-curb-to-flight-passenger-flow]

**3. Digital twin deployment is real but not yet passenger-flow-specific at named comparator airports.** Of the airports in scope, Singapore Changi's Smart Terminal Operations Program is most advanced: 15% equipment downtime reduction (2021) and 20% queue management efficiency improvement (2022) are cited. [Source: https://dwuconsulting.com/dwu-ai/twin] These are self-reported by the airport authority. HKIA's digital twin, per publicly available documentation, is primarily used for VR training simulations and design review of new construction — the virtual model of passenger-accessible Terminal 1 areas was still being completed in stages as of the most recent public reporting. [Source: https://www.hongkongairport.com/iwov-resources/html/sustainability_report/eng/SR1819/airport-city/smart-airport-city/] Heathrow's twin is focused on apron and turnaround (Assaia ApronAI, expanded to 116 gates). No named airport in the comparator set has published documented outcomes specifically attributing corridor-sizing or corridor-operational decisions to digital twin data.

**4. DEN's $300-700M concourse walkway project is the clearest evidence that the gap between corridor simulation and operational reality eventually becomes a capital problem.** Denver International Airport will repurpose underground baggage tunnels into pedestrian walkways between concourses A, B, and C — at a cost range of $300M to $700M, with construction planned to begin 2027 and complete 2028-2029. The explicit driver is that the airport has had "no redundancy" in its inter-concourse connection for 31 years. [Source: https://www.axios.com/local/denver/2026/05/26/denver-airport-dia-den-walkways-between-concourses] [Source: https://www.cbsnews.com/colorado/news/denver-international-airport-pedestrian-walkways-between-concourses/] The A-Bridge (pedestrian link from main terminal to Concourse A, previously the site of a small security checkpoint) reopened in August 2025 as a post-security alternative to the train. No publicly available documentation connects any pre-opening pedestrian simulation to the train capacity analysis that made the lack of redundancy visible. The problem was operational and obvious; the solution is belated and expensive.

**5. LiDAR for corridor measurement is marketed but not yet documented at load-bearing deployment in named U.S. airports.** Veovo announced LiDAR integration into its airport platform, marketed specifically for corridor and large-area coverage. [Source: https://veovo.com/insights/news/lidar-technology] Xovis has explicitly declined to adopt LiDAR, arguing its 3D stereo-optical sensors are better suited to the airport environment. [Source: https://www.internationalairportreview.com/article/299071/why-xovis-doesnt-use-lidar/] Neither vendor has published a case study where LiDAR-measured corridor density data changed a capital or operational decision at a named U.S. airport. Outsight (a standalone LiDAR analytics vendor) claims airport deployments but publishes no site-specific outcome data for sterile corridor segments. [from training-data, requires primary-source verification]

**6. The IAD Tier 2 East concourse (Concourse E, opening September 2026) appears to have no publicly documented corridor-level sensing deployment.** The PGAL-designed facility includes AeroTrain connection, digital signage, and intuitive sightlines — described as wayfinding aids rather than flow measurement infrastructure. [Source: https://www.pgal.com/projects/tier-2-concourse-east-at-washington-dulles-international-airport-iad/] No press release or design document found in this search describes a post-occupancy pedestrian flow monitoring system planned for Concourse E's corridor segments or AeroTrain handoff points. The design of the new concourse follows the same generation of tools as its predecessors.

**7. Market-size figures for airport digital twins are vendor-adjacent and should not be used in serious analysis.** Multiple sources report the global airport digital twin market at $1.12–2.1 billion in 2024, growing at 20–22% CAGR to $8.6–11.7 billion by 2033. These figures originate from commercial market research firms (Market Intelo, MarketWatch) whose methodology is opaque and whose client base includes vendors in the space. The McKinsey-cited figure that only 8% of respondents had "fully deployed" digital twins [Source: https://dwuconsulting.com/dwu-ai/twin] is more operationally meaningful — and is a more honest characterization of where the technology actually sits.

---

## 3. Evidence Section

### Simulation tools — design phase only

MassMotion's own verification and validation report, published by Oasys/Arup, validates model behavior against controlled experimental data and published pedestrian science (Weidmann, Fruin). [Source: https://www.oasys-software.com/wp-content/uploads/2017/11/The-Verification-and-Validation-of-MassMotion-for-Evacuation-Modelling-Report.pdf] This is validation of the model engine, not validation of a specific airport terminal prediction against post-occupancy measurement. SimWalk's client roster includes Aéroport de Paris and Zurich Airport. [from training-data, requires primary-source verification] AnyLogic publishes a Frankfurt Airport simulation case study showing the tool used for capacity planning during a planned expansion. [Source: https://www.anylogic.com/resources/case-studies/simulation-of-the-frankfurt-airport/] None of these case studies report a post-occupancy comparison.

The 2025 conference paper "The Role of Airport Simulation Technology in Airport Planning and Operation Management" (ACM DL) identifies the absence of post-occupancy validation as a recognized gap in the literature: practitioners are advised to exercise caution when using simulation tools to address pedestrian bottlenecks in airports because validation against airport terminal conditions has not been established. [Source: https://dl.acm.org/doi/10.1145/3745676.3745689]

### Xovis — checkpoint-centric, not corridor-centric

Xovis's 2024 Airport Technology Excellence Award was for its AERO managed service — a cloud-native passenger flow management system. [Source: https://www.airport-technology.com/featured-company/2024-xovis/] The Helsinki case study, the most detailed found, reports that the system enables "40-minute connections" — a checkpoint processing metric, not a corridor throughput metric. [Source: https://www.xovis.com/insights/detail/helsinki-airport-passenger-flow-management-system-case-study] The technology works. The question is whether it is being applied to corridor segments rather than to the queuing points on either end of those segments. The answer, based on all published case studies found, is: not yet at named airports.

### Veovo and BlipTrack — corridor capability claimed, corridor outcomes undocumented

Birmingham Airport, CVG, Budapest, and Keflavik are named as Veovo/BlipTrack deployments. [Source: https://veovo.com/insights/case-studies/flow-management-is-transforming-birmingham-airport] [Source: https://community.veovo.com/discover/news/cvg-airport-flow-management/] Birmingham's case study reports "near-trebling of data capturing capabilities" and "accurate wait times displayed." These are queue-wait metrics. The CVG case study contains no quantified outcomes at all — it is a capability description. Budapest's deployment was reported by Future Travel Experience in March 2023 as an investment in "analytics technology to improve passenger flows" — no post-deployment metrics. [Source: https://www.futuretravelexperience.com/2023/03/budapest-airport-invests-in-veovo-analytics-technology-to-improve-passenger-flows/]

### DEN — the capital consequence of insufficient redundancy

Denver International Airport confirmed in May 2026 the planned conversion of decommissioned baggage tunnels into pedestrian corridors connecting Concourses A, B, and C. The project costs $300–700M and has a 2027–2029 construction window. [Source: https://denverite.com/2026/05/26/denver-airport-walkways-tunnels-train/] The framing from airport leadership: "the airport has not had redundancy for 31 years." The A-Bridge (a separate structure connecting the main terminal to Concourse A) was restored to post-security pedestrian use in August 2025 after years as a checkpoint location. [Source: https://www.flydenver.com/press-release/changes-coming-to-a-bridge-ansbacher-hall-ahead-of-bridge-security-closure/] This is the clearest available example of a corridor capacity and redundancy decision made at design time becoming an expensive retrofit problem — without any documented sensing-based diagnosis.

### LGA Terminal B — acclaimed, but no corridor throughput data

LaGuardia Terminal B's $5.1 billion redevelopment opened fully in 2022. It earned Skytrax's 5-star terminal rating in 2023 and retained it in 2025. [Source: https://www.panynj.gov/port-authority/en/press-room/press-release-archives/2025-press-releases/laguardia-airports-terminal-b-awarded-top-5-star-skytrax-rating-for-second-time.html] The terminal handled approximately 18 million passengers in 2024. No post-occupancy corridor throughput study was found in the public domain. The design is praised; the flow performance in the elevated pedestrian bridges connecting the headhouse to the island concourses has not been documented in measurable terms against any pre-opening prediction. [from training-data, requires primary-source verification for bridge-specific flow data]

### JFK Terminal 1 (New Terminal One) — sensing not documented in design filings

JFK's New Terminal One, designed by Gensler/AECOM with a 2026 partial opening and 2030 completion target, includes a sterile corridor for international arrivals at concourse level. [Source: https://www.gensler.com/projects/new-terminal-one-at-jfk-international-airport] No public design filing or press release describes a planned corridor-level pedestrian sensing deployment or a post-occupancy flow validation plan. This is consistent with the industry pattern.

---

## 4. Honest Assessment of Maturity

### What is real and operational

Checkpoint-focused passenger flow measurement (Xovis, Veovo/BlipTrack) is mature, deployed at scale, and genuinely useful for queue management at security, check-in, and immigration. Over 120 airports have some form of this. It is not the same as corridor flow measurement.

Aircraft-operations digital twins (apron, gates, turnaround) are operational at a handful of major international airports — DXB, SIN, AMS, LHR. The passenger flow components are real but secondary. Gate utilization optimization and predictive maintenance are the documented ROI drivers.

Design-phase simulation tools (MassMotion, AnyLogic, SimWalk) are standard practice for major terminal projects and have been for 15+ years. They produce defensible LOS projections. They do not produce validated post-occupancy comparisons.

### What is pilot or early-stage

LiDAR-based corridor monitoring is commercially available (Veovo, Outsight) but lacks published case studies showing corridor-specific outcomes at named airports. It is marketed as the solution to coverage gaps in large, high-ceiling spaces. Deployment evidence at this level of specificity does not exist in the public record as of mid-2026.

Passenger-flow digital twins — meaning a system that continuously ingests corridor-level density data and feeds it back into operational or capital decisions — are not documented at any of the named comparator airports (DEN, ATL, SIN T3, LGA, JFK T1, LAX MSC, IAD). The technology components exist; the integrated use case does not appear to be operating at any of these sites.

### What is hype or vendor-adjacent

Market size projections for airport digital twins ($8–12B by 2033) are generated by commercial research firms and should not be cited without heavy qualification. The McKinsey figure — 8% "fully deployed" — is a more honest benchmark.

ROI figures from vendor case studies (15% equipment downtime reduction at Changi, 20% queue efficiency improvement) are self-reported by the airport authority, not independently audited. They may be accurate. They are not verified.

The claim that sensing and real-time flow management can substitute for physical corridor capacity is not supported by any evidence in the public record. It is a vendor-driven framing that confuses measurement with solution.

---

## 5. Verbatim Data Points for Strategist Use

**1.** "Any references reporting validation of simulation results for pedestrian behavior in airport terminals were not identified" — a 2025 conference paper at ACM explicitly flagging that the tools used to justify corridor sizing during design have never been validated against post-occupancy conditions. [Source: https://dl.acm.org/doi/10.1145/3745676.3745689]

**2.** Denver International Airport "has not had redundancy for 31 years" in its inter-concourse connections — the operational framing used by airport leadership to justify a $300–700M pedestrian tunnel project that will take until 2028 or 2029 to complete. [Source: https://www.axios.com/local/denver/2026/05/26/denver-airport-dia-den-walkways-between-concourses]

**3.** Xovis: "120 airports and nearly 700 mission-critical touchpoints" — the scale of flow sensing deployment. Those touchpoints are queuing nodes, not corridor segments. The scale is real; the coverage is misread by planners who assume it means corridors are being measured. [Source: https://www.xovis.com/solutions/airport]

**4.** Only 8% of airports surveyed had "fully deployed" digital twins as of a 2025 McKinsey study — despite the market being described in the same sources as a multi-billion-dollar growth sector. The gap between marketed capability and operational deployment is the defining characteristic of this technology category right now. [Source: https://dwuconsulting.com/dwu-ai/twin]

**5.** Veovo's corridor sensing guide notes that its Wi-Fi/Bluetooth technology is "particularly useful for measuring and predicting wait times in long corridors, extended lines" — but the specific airports where this is load-bearing for operational decisions are not named. The capability exists; the evidence of it changing a corridor design or operational decision is absent from the public record. [Source: https://veovo.com/insights/articles/a-guide-to-the-airport-passenger-tracking-sensor-landscape]

---

## 6. What's Off-the-Shelf in 2026 vs. What Still Requires Custom Work

| Capability | Status | Key Vendors |
|---|---|---|
| Queue wait-time measurement at checkpoint nodes | Mature, off-the-shelf | Xovis, Veovo, BlipTrack |
| Full-terminal passenger journey tracking (Bluetooth/WiFi) | Mature, off-the-shelf | Veovo, BlipTrack |
| Corridor-level density and directional flow (LiDAR) | Available, not proven at scale | Veovo (new), Outsight |
| Design-phase pedestrian simulation | Mature, off-the-shelf | MassMotion, AnyLogic, SimWalk |
| Post-occupancy simulation validation (design vs. measured) | Not commercially available; requires bespoke study | Research gap |
| Airport digital twin (apron/equipment) | Operational at select airports | Assaia, Bentley, WAISL |
| Airport digital twin (passenger corridor flow) | Pilot/early stage | No named deployment at comparator airports |
| Sensing-informed corridor capital decisions | Not documented at any named comparator airport | — |

The technology to measure corridor flow exists. The institutional practice of using that measurement to validate pre-opening design models — and to inform future corridor-sizing decisions — does not exist as a documented standard at any airport in the comparator set. The gap is not technical. It is a question of whether airports choose to close the feedback loop between what the simulation predicted and what the sensors record.

For IAD specifically: the Tier 2 East concourse opening in September 2026 represents the last near-term opportunity to establish a baseline before the AeroTrain-to-concourse handoff points are locked in for the next decade. If MWAA does not instrument those corridor segments at opening, the design assumptions embedded in the MassMotion or equivalent model will go unvalidated for the life of the building.

---

*Sources used in this brief:*
- [MassMotion Verification and Validation Report (Oasys/Arup)](https://www.oasys-software.com/wp-content/uploads/2017/11/The-Verification-and-Validation-of-MassMotion-for-Evacuation-Modelling-Report.pdf)
- [Airport Simulation Technology Role — ACM 2025 Conference](https://dl.acm.org/doi/10.1145/3745676.3745689)
- [Veovo Sensor Landscape Guide](https://veovo.com/insights/articles/a-guide-to-the-airport-passenger-tracking-sensor-landscape)
- [Veovo LiDAR Announcement](https://veovo.com/insights/news/lidar-technology)
- [Xovis — Why Not LiDAR](https://www.internationalairportreview.com/article/299071/why-xovis-doesnt-use-lidar/)
- [Xovis Airport Solutions](https://www.xovis.com/solutions/airport)
- [Xovis Helsinki Case Study](https://www.xovis.com/insights/detail/helsinki-airport-passenger-flow-management-system-case-study)
- [Xovis 2024 Airport Technology Excellence Award](https://www.airport-technology.com/featured-company/2024-xovis/)
- [Veovo CVG Case Study](https://veovo.com/insights/case-studies/enabling-smarter-decisions-at-cvg-airport-with-curb-to-flight-passenger-flow)
- [Veovo Birmingham Case Study](https://veovo.com/insights/case-studies/flow-management-is-transforming-birmingham-airport)
- [Budapest Airport Veovo Deployment (Future Travel Experience)](https://www.futuretravelexperience.com/2023/03/budapest-airport-invests-in-veovo-analytics-technology-to-improve-passenger-flows/)
- [Airport Digital Twins — DWU Consulting](https://dwuconsulting.com/dwu-ai/twin)
- [HKIA Smart Airport](https://www.hongkongairport.com/iwov-resources/html/sustainability_report/eng/SR1819/airport-city/smart-airport-city/)
- [DEN Walkways — Axios](https://www.axios.com/local/denver/2026/05/26/denver-airport-dia-den-walkways-between-concourses)
- [DEN Walkways — CBS Colorado](https://www.cbsnews.com/colorado/news/denver-international-airport-pedestrian-walkways-between-concourses/)
- [DEN A-Bridge Reopening](https://www.flydenver.com/press-release/changes-coming-to-a-bridge-ansbacher-hall-ahead-of-bridge-security-closure/)
- [LGA Terminal B Skytrax 2025](https://www.panynj.gov/port-authority/en/press-room/press-release-archives/2025-press-releases/laguardia-airports-terminal-b-awarded-top-5-star-skytrax-rating-for-second-time.html)
- [JFK New Terminal One — Gensler](https://www.gensler.com/projects/new-terminal-one-at-jfk-international-airport)
- [IAD Tier 2 East — PGAL](https://www.pgal.com/projects/tier-2-concourse-east-at-washington-dulles-international-airport-iad/)
- [ACRP Report 55 — Passenger LOS and Spatial Planning](https://crp.trb.org/acrp0715/wp-content/themes/acrp-child/documents/046/original/ACRP_55_Passenger_Level_of_Service_and_Spatial_Planning_for_Airport_Terminals.pdf)
- [AnyLogic Frankfurt Airport Simulation](https://www.anylogic.com/resources/case-studies/simulation-of-the-frankfurt-airport/)
- [Denverite — DEN Walkways Tunnel Article](https://denverite.com/2026/05/26/denver-airport-walkways-tunnels-train/)
