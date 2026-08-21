# Technology Scout Brief — Operational Intelligence at Terminal F

**Run:** designing-for-2043-what-terminal-f-should-absorb-before-the-concrete-cures
**Author agent:** technology-scout
**Date:** 2026-08-19
**Frame:** what "operational intelligence" actually is in 2026, what it has cost and returned at named airports, and — the reason a technology scout is on this panel — which pieces have to be trenched into Terminal F's structure before the concrete cures and which can be bolted on after opening at ordinary refresh cost.

The brief is deliberately narrow. It is not a wishlist. Every category below is scored against three questions Terminal F actually needs answered:

1. Does this require conduit, backbone fiber, sensor mounting points, power, or airfield-side cabling that becomes ten times more expensive to add post-pour?
2. Does the modular gate manufacturing method — gates built offsite and installed on the apron — change the answer?
3. Is there a documented deployment at a comparable hub, and did the reported ROI come from the vendor or from someone who didn't sell the system?

---

## 1. A taxonomy of "operational intelligence" — what counts, what doesn't

The phrase is used loosely. I use it here to mean: **systems that ingest live operational data from multiple owners (airline, airport, ground handler, ATC, CBP, TSA), fuse it into a shared picture, and either automate a decision or shorten the loop from event to action**. Under that definition, seven categories are in scope:

- **A-CDM / TTOT / TSAT.** Airport Collaborative Decision Making — the discipline of publishing Target Off-Block, Target Start-Up, and Target Take-Off Times as a single shared feed to airline, tower, ground handler, and network manager. Mature in Europe, still nascent in the US. Requires clean AODB, a signed information-sharing agreement, and a network manager on the other end. [Source: https://www.eurocontrol.int/concept/airport-collaborative-decision-making]
- **Predictive turn (computer-vision-driven).** Gate cameras plus a model that recognizes every sub-process of a turnaround — chocks, jetbridge, fuel truck, catering, cabin service, cargo doors — and calls delay while there is still time to intervene. Assaia is the reference vendor. [Source: https://www.assaia.com/customer-stories/44-reduction-at-toronto-pearson-international-airport]
- **Digital twin.** A live 3D model of the airport fed by IoT streams. Ranges from asset-management tools that call themselves twins (mature) to full physics-informed operational twins that run "what-ifs" against tomorrow's schedule (early, expensive, mostly bespoke). HKIA is the most-cited deployment. [Source: https://blog.aci.aero/digital-twin-a-real-time-interactive-airport-visualization-tool/]
- **Biometric flow.** Face-as-token across curb, bag drop, checkpoint, lounge entry, boarding, and CBP arrival. In the US, split between CBP's Traveler Verification Service / Simplified Arrival (federal, mandatory-ish for international) and airline/airport-side deployments (SITA Smart Path, IDEMIA, Amadeus ICM). [Source: https://www.cbp.gov/newsroom/local-media-release/cbp-s-simplified-arrival-lands-dfw]
- **Queue prediction.** Overhead 3D sensors (Xovis is dominant; Veovo, iinside adjacent) counting bodies, timing dwell, and forecasting the next 15–60 minutes so the checkpoint or CBP FIS opens the right number of lanes. [Source: https://www.xovis.com/technology/airport-software]
- **Ramp coordination / integrated ops dashboards.** AODB + Resource Management System + workflow layer that binds gate assignment, stand allocation, bag belt, jetbridge, GSE dispatch, and passenger-flow feeds into one view for the airport ops center. Amadeus AODB, Veovo, INFORM GS, SITA, Amorph. [Source: https://amadeus.com/en/airports/products/airport-operational-data-base-aodb]
- **Passenger-facing wayfinding intelligence.** Personalized walking-time-to-gate, dynamic security wait broadcasts, gate change push notifications — sits on top of the sensing layers above and requires very little that is not commodity.

Two things I explicitly exclude from "operational intelligence" for this brief because their operational contribution at Terminal F would be marginal or unproven at 2027 opening: fully autonomous ramp vehicles (still airside-restricted pilot cases), and generative-AI "operations copilots" (there are marketing decks; there are not deployments with audited ROI at hub scale). Both belong on a 2035 watch list, not a 2027 spec sheet.

---

## 2. Key findings

- **The reversibility split is stark.** Sensor conduit, fiber backbone density, PoE+ ceiling drops, gate-camera mounts, and biometric-kiosk power/data are cheap during pour and punitively expensive after. Software, algorithms, dashboards, and passenger apps are cheap to defer and get better every year you wait. A Terminal F spec that gets the physical layer generous and the software layer explicitly deferred is a strictly dominant strategy.
- **A-CDM at DFW would be a US-first at meaningful scale.** European hubs run it as a network-integrated system through EUROCONTROL. In the US there is no equivalent network manager, and FAA Surface CDM is a research/demo program at ATL, CLT and a handful of others rather than a settled operational spec. Reported European taxi-out savings are 0.25–3 minutes per departure; Munich reports up to 3. [Source: https://www.eurocontrol.int/publication/airport-collaborative-decision-making-cdm-impact-assessment] [Source: https://www.eurocontrol.int/archive_download/all/node/9779] Terminal F designed to be Surface-CDM-ready would be adopting a discipline whose data plumbing is real but whose partner ecosystem in the US is still forming.
- **Predictive turn is the most audit-able tech in this brief.** Toronto Pearson reports a 44% reduction in average taxi-in time attributed to Assaia's turnaround control; Alaska at SEA reports a 12% reduction in turn time (~4 minutes/departure) and 17% reduction in excess hold time. Both figures are Assaia-published and therefore vendor-sourced; they are directionally consistent across airports and airlines and are easier to independently instrument than most claims in this space. [Source: https://www.assaia.com/customer-stories/44-reduction-at-toronto-pearson-international-airport] [Source: https://aerospaceglobalnews.com/news/ai-aircraft-turnarounds-financial-savings-assaia/]
- **"Digital twin" ranges from real product to slideware.** HKIA's twin (with CHAIN Technology) is a live deployment feeding IoT into a 3D operational picture; specific capex has not been publicly disclosed. What is available off-the-shelf in 2026 is asset-management with 3D visualization (Bentley, Autodesk Tandem, ESRI Indoors). What still requires bespoke work is a *predictive* operational twin that runs tomorrow's bank against actual constraints. That capability is not shippable in a box. [Source: https://www.hongkongairport.com/en/media-centre/press-release/2019/pr_1334] [Source: https://web.bentley.com/cities-airport-digital-twins-1786.html]
- **Biometric flow at DFW is not greenfield.** American already runs biometric boarding at DFW (launched 2019 in Terminal D, expanded to A/B/C/D international gates); CBP Simplified Arrival is live at DFW; Terminal F should therefore be scoped to the mature version of this stack, not the pilot version. The design question is not "should we do biometrics" but "should the biometric identity be the pass everywhere in the building — bag drop, checkpoint divest, lounge, boarding, and (via CBP) FIS." [Source: https://news.aa.com/news/news-details/2019/Biometric-Boarding-Arrives-at-DFW-for-American-Airlines-Customers/default.aspx] [Source: https://www.cbp.gov/newsroom/local-media-release/cbp-s-simplified-arrival-lands-dfw]
- **The independent ROI evidence base is thin and mostly European.** EUROCONTROL's A-CDM impact studies are the closest thing this industry has to independent third-party evaluation. Digital twin ROI and integrated-ops-dashboard ROI numbers in the trade press are, with very few exceptions, vendor-sourced. A strategist should treat any single-source ROI figure as a hypothesis, not a fact.
- **Failure modes are almost always integration, not the box.** Heathrow T5 in 2008 lost 42,000 bags in the first few days not because the baggage system was primitive but because it was inadequately tested end-to-end with the airline's staff and processes. Berlin Brandenburg was delayed nearly a decade in part because its custom fire-safety control system could not be programmed correctly. The 2025 BER cyberattack propagated through a third-party check-in/baggage vendor. Terminal F's dominant technology risks are the same ones: integration testing, vendor concentration, and change-management with airline staff. [Source: https://spectrum.ieee.org/thousands-of-bags-miss-flights-at-british-airways-heathrow-terminal-5-again] [Source: https://erena.me/2025/01/28/german-construction-fiasco/] [Source: https://www.internationalairportreview.com/news/296718/cyber-attack-disruption-to-continue-at-ber/]
- **Modular construction changes the tech calculus in a specific way.** Because gate modules are built in a factory and installed on the apron, sensor mounting, camera positions, PoE runs, and gate-side biometric-kiosk data drops can be baked into the module template — every module identical, tested in the factory before it ships. This is the one thing DFW gets for near-free that a stick-built terminal cannot get. The recommendation follows: fix the sensor and cabling schedule at the module-template level, then ship 31 identical, forensically instrumented gates.

---

## 3. Evidence — what deployments actually did, and where the numbers came from

**A-CDM in Europe (independent, EUROCONTROL).** A-CDM is fully implemented at 34 European airports including Amsterdam, Barcelona, Frankfurt, London Heathrow, Paris CDG, and Munich. Average taxi-out time savings range 0.25–3 minutes per departure across the network. Over 34% of ECAC departures now originate from a CDM airport and transmit improved take-off estimates to the Network Manager. Wider EU deployment could reduce total network ATFM delays 18–23% and improve sector capacity up to 4%. [Source: https://www.eurocontrol.int/publication/airport-collaborative-decision-making-cdm-impact-assessment] These figures are the most defensible in this brief because the buyer, the seller, and the evaluator are three different parties.

**Munich specifically.** MUC reports up to 3 minutes taxi-out saving per departure and up to 2 minutes schedule-adherence improvement per flight after A-CDM implementation, and now holds the most accurate take-off estimate of the 42 airports considered by EUROCONTROL. Note: this is Munich's own reporting to a EUROCONTROL workshop and should be read as self-reported but network-audited (the accuracy of MUC's TTOT is verifiable by anyone with FR24 and a scheduling file). [Source: https://www.eurocontrol.int/archive_download/all/node/9779]

**Predictive turn — Assaia at Toronto Pearson.** GTAA deployed Assaia's Turnaround Control across 106 gates, integrated with Toronto's A-CDM initiative; Assaia publishes a 44% reduction in average taxi-in time as the headline result at YYZ. Assaia's Turnaround Report 2025 aggregates similar figures across a customer set including Cathay at HKG, Alaska at SEA, JFK operations, and European hubs. Vendor-published, but instrumented against gate cameras that any airport can independently verify. [Source: https://airportindustry-news.com/toronto-pearson-deploys-assaias-apronai-to-optimise-operations/] [Source: https://www.assaia.com/customer-stories/44-reduction-at-toronto-pearson-international-airport] [Source: https://www.assaia.com/turnaround-report-2025]

**Predictive turn — Alaska at SEA.** Alaska Airlines reports 12% reduction in turn times and 17% reduction in excess hold time at SEA using Assaia. Reported through trade press; also traceable to Assaia's own case-study set. Directionally consistent with YYZ. [Source: https://aerospaceglobalnews.com/news/ai-aircraft-turnarounds-financial-savings-assaia/]

**Digital twin — HKIA.** The Airport Authority Hong Kong developed the "HKIA Digital Twin" with CHAIN Technology, collecting real-time IoT data and visualizing it in a 3D interface, with predictive analytics feeding operational alerts. Deployment is real and live. Program capex has not been publicly disclosed; industry publications describe the ambition ("smart airport") more than the ledger. [Source: https://www.hongkongairport.com/en/media-centre/press-release/2019/pr_1334] [Source: https://blog.aci.aero/digital-twin-a-real-time-interactive-airport-visualization-tool/] Bentley markets an "airport digital twin" product line whose case studies are largely asset-management applications rather than live operational prediction. [Source: https://web.bentley.com/cities-airport-digital-twins-1786.html]

**Biometric flow — DFW.** American Airlines launched biometric boarding at DFW in August 2019 (Terminal D international) and planned expansion to ~75 international gates across A/B/C/D by end of 2019. CBP Simplified Arrival went live at DFW under CBP's Traveler Verification Service, using facial comparison against a gallery built from passport/visa photos. [Source: https://news.aa.com/news/news-details/2019/Biometric-Boarding-Arrives-at-DFW-for-American-Airlines-Customers/default.aspx] [Source: https://www.cbp.gov/newsroom/local-media-release/cbp-s-simplified-arrival-lands-dfw] SITA reports 45 airports globally using its Smart Path biometric single-token product, including PEK, BKK and EWR. [Source: https://www.biometricupdate.com/202104/sita-smart-path-biometrics-launched-for-domestic-us-passengers-as-airport-investments-accelerate]

**Queue prediction.** Xovis operates 3D overhead sensors delivering queue length and wait time at 10-minute cadence across terminals globally; Amorph offers a passenger-flow prediction engine that combines live sensor data with airport-specific layouts to forecast queues, dwell, and density. Both are used at European and US hubs; case-level results (e.g., specific checkpoint wait-time reductions) are typically joint marketing rather than independent audit. [Source: https://www.xovis.com/technology/airport-software] [Source: https://amorph.aero/solutions/]

**Amadeus AODB.** Cloud-hosted Airport Operational Database from Amadeus; positioned as A-CDM-compliant and holding schedules for 95% of airlines one year in advance. Amadeus does not publish a public price list; large-hub deployments are typically multi-year enterprise contracts and treated as opex not capex. [Source: https://amadeus.com/en/airports/products/airport-operational-data-base-aodb]

**Failures — Heathrow T5 (2008).** On T5's first days of operation, roughly 28,000–42,000 bags were misplaced and ~15% of BA flights cancelled over nearly a week, on a £4.3B terminal. Post-mortems attributed the failure to inadequate end-to-end testing, poor BAA/BA coordination, and staff-training gaps — not to the baggage system itself. [Source: https://spectrum.ieee.org/thousands-of-bags-miss-flights-at-british-airways-heathrow-terminal-5-again] [Source: https://www.businesstraveller.com/news/2008/11/03/t5-the-lessons-learned/]

**Failures — Berlin Brandenburg (BER).** Opened nearly a decade late at roughly €10B against a €2B initial budget. Fire-safety control system was custom, never successfully programmed to specification, and drove a large share of the delay. In September 2025 BER's passenger and baggage systems were disrupted by a cyberattack that propagated through a third-party check-in vendor, forcing manual check-in and creating multi-day baggage disruption. [Source: https://erena.me/2025/01/28/german-construction-fiasco/] [Source: https://www.internationalairportreview.com/news/296718/cyber-attack-disruption-to-continue-at-ber/]

---

## 4. Honest maturity assessment — what is real, what is hype

**Real and shippable in 2026.**

- Common-Use Passenger Processing (CUPPS/CUSS) and cloud AODB. Commodity.
- CBP Simplified Arrival / TVS. Live at DFW. The design question is FIS layout, not whether to buy.
- SITA/IDEMIA/Amadeus biometric boarding gates. Real product, real deployments, integration cost is the variable.
- Xovis-class overhead sensor networks with queue forecasting. Mature enough that omitting it from a new-build in 2026 is negligence.
- Assaia-class computer-vision turn monitoring. Mature enough to be gate-standard equipment on new-build modular gates.
- Bentley/ESRI 3D asset visualization. Mature as an asset-management tool. Do not call it a twin.

**Real but with a caveat.**

- A-CDM in the US. The protocol is mature; the network-manager counterparty is not the same animal as EUROCONTROL. Building Terminal F's data plane to A-CDM message specifications is a low-cost hedge; expecting European-scale delay-reduction benefits by 2027 is not defensible.
- Full-airport predictive digital twin. Real at HKIA. Everywhere else, mostly bespoke consulting engagements with a Bentley or Autodesk backbone; results depend heavily on data quality upstream.

**Hype until proven otherwise.**

- "AI operations copilot" products marketed at airport C-suites in 2025–2026. No independent audited ROI at hub scale that I could find. Watch, don't buy.
- Fully autonomous ramp GSE at line-operational scale. Pilots, not deployments.
- Vendor-published ROI figures from any category above, absent a way to independently instrument the outcome. Treat as directional at best.

---

## 5. Quotable data points a strategist can use verbatim

1. "Average taxi-out time savings from A-CDM in Europe range 0.25 to 3 minutes per departure; Munich, the highest-performing implementation, reports up to 3." [Source: https://www.eurocontrol.int/publication/airport-collaborative-decision-making-cdm-impact-assessment] [Source: https://www.eurocontrol.int/archive_download/all/node/9779]

2. "Toronto Pearson reports a 44 percent reduction in average taxi-in time after deploying Assaia's turnaround-control AI across 106 gates, integrated with the airport's A-CDM initiative." [Source: https://www.assaia.com/customer-stories/44-reduction-at-toronto-pearson-international-airport]

3. "Alaska Airlines reports Assaia's platform cut aircraft turn times by 12 percent at Seattle-Tacoma — approximately four minutes per departure — and reduced excess hold time by 17 percent." [Source: https://aerospaceglobalnews.com/news/ai-aircraft-turnarounds-financial-savings-assaia/]

4. "SITA reports its Smart Path biometric single-token product is in use at 45 airports worldwide including Beijing, Bangkok and Newark." [Source: https://www.biometricupdate.com/202104/sita-smart-path-biometrics-launched-for-domestic-us-passengers-as-airport-investments-accelerate]

5. "Heathrow Terminal 5's opening in 2008 stranded approximately 42,000 bags and cancelled roughly 15 percent of British Airways flights in the first week, on a £4.3 billion terminal — a failure attributed to inadequate end-to-end testing and staff training, not to the baggage system's design." [Source: https://spectrum.ieee.org/thousands-of-bags-miss-flights-at-british-airways-heathrow-terminal-5-again]

6. "American Airlines began biometric boarding at DFW in August 2019 and planned expansion to approximately 75 international gates across Terminals A, B, C, and D by year end." [Source: https://news.aa.com/news/news-details/2019/Biometric-Boarding-Arrives-at-DFW-for-American-Airlines-Customers/default.aspx]

---

## 6. Terminal F–specific reversibility map (professional judgment, marked as such)

This is my reading, not sourced to a single publication; the underlying tech-cost dynamics are, however, well-documented in the categories above.

**Design in now — cheap before pour, punitive after (must be in the module template):**

- Dense conduit and pull-boxes on 20-foot centers in ceiling grids, apron-side, and gate-podium areas. Fiber + PoE++ backbone provisioned at 3–5× current sensor count.
- Camera mounts, power, and data drops at every gate module's four apron corners plus jetbridge tunnel — the physical prerequisite for Assaia-class predictive turn on all 31 gates.
- Sensor mounting rails and power at overhead intervals throughout ticketing, checkpoint queue serpentines, connector spines, hold rooms, and FIS — Xovis-class 3D sensors need line of sight and cabling, both of which are cheap now.
- Structural provisions and dedicated power/data closets for biometric e-gates at checkpoint entry, boarding, and CBP arrival — even if the specific vendor is chosen later.
- FIS geometry that accommodates larger CBP biometric processing arrays and a future Global Entry-parity domestic biometric option.
- Fiber diversity out of the terminal — at least two physically separated paths to the DFW campus core — before landscaping goes in.
- Enough Skylink Station data/power capacity for a full 2035 sensor grid, not a 2027 one.

**Defer — cheap to add during commissioning or after opening:**

- The AODB/Ops Dashboard vendor selection and integration. Software layer; refreshes on 5–7 year cycles anyway.
- Digital twin visualization tooling. Buy after you have a year of live sensor data to feed it.
- Passenger-facing wayfinding app and personalized walk-time. Software; can and should iterate post-opening.
- Any "AI operations copilot." Wait for audited hub-scale results.

**Reject as premature for the 2027 spec:**

- Fully autonomous ramp GSE fleet commitments (leave conduit for chargers; do not commit to a vehicle stack).
- Bespoke custom control systems along the BER pattern — anything the airport can only get from one integrator with a single-source software stack is a repeat of a documented failure mode.

**What the modular gate method uniquely enables (and Terminal F should exploit):**

Because gate modules are factory-built, sensor and cabling schedules can be finalized once, tested in the factory against a live A-CDM/Assaia/CBP stack, and shipped 31 times identically. Every gate on Terminal F can be forensically instrumented from day one — a data uniformity no stick-built terminal in the US can match. The strategic recommendation is to treat the module template itself as the airport's most important digital asset: get it right once, get it right 31 times.

---

## 7. Evidence gaps

- No public capex figure for the HKIA digital twin. Cost order of magnitude for a Terminal F-class digital twin is therefore an estimate at best, and the brief does not claim one.
- Amadeus AODB, SITA Smart Path, and Assaia commercial terms are not publicly listed; industry-typical figures exist in trade conversation but are not documented at citable quality.
- US Surface CDM benefit realization at hub scale is not yet published to a level comparable to EUROCONTROL's A-CDM assessments; Terminal F designers should not assume European-scale delay-reduction benefits transfer 1:1.
- The gate-camera density and PoE budget assumptions embedded in Terminal F's current design documents are not public; whether the module template already includes Assaia-ready mounts is a question for the chief-engineer thread of this run to answer.
- Whether DFW's current cybersecurity posture segregates a third-party check-in vendor from the AODB — the BER 2025 failure mode — is not public and belongs on the Terminal F risk register regardless.
