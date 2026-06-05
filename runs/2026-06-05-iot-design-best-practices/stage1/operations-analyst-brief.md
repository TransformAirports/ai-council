# Operations Analyst Brief: Airport IoT Architecture — The Stranding Problem

**Run:** IoT Design Best Practices  
**Agent:** Operations Analyst  
**Date:** June 2026  

---

## Key Findings

1. **The majority of IoT programs never leave the pilot phase.** A 2017 Cisco survey of 1,845 IT and business decision-makers found that 60% of IoT initiatives stall at the proof-of-concept stage. Only 26% of companies considered any IoT initiative a complete success. A 2018 McKinsey survey put the share of companies stuck in pilot mode at 84%. These numbers have improved modestly but not dramatically: a 2023 Beecham Research study found a 28% improvement in IoT project success metrics vs. 2020 — which still means most programs fail to scale. [Source: https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2017/m05/cisco-survey-reveals-close-to-three-fourths-of-iot-projects-are-failing.html]

2. **Platform vendor exit is a realized risk, not a hypothetical.** Google Cloud IoT Core, launched March 2017, was shut down in August 2023 — six years of life for a hyperscaler IoT product. Sigfox, a LPWAN network provider that had raised over $300 million and operated dedicated IoT networks across 70+ countries, filed for bankruptcy protection in January 2022 and sought a buyer while owing nearly $150 million in unsecured debt. Airports that built on either platform as their connectivity or management layer without portable data architectures faced unplanned migrations. [Sources: https://akenza.io/blog/google-iot-core-shutdown; https://techcrunch.com/2022/01/27/sigfox-the-french-iot-startup-that-had-raised-more-than-300m-files-for-bankruptcy-protection-as-it-seeks-a-buyer/]

3. **Most large US airports have not moved beyond pilots on their most ambitious IoT programs.** As of early 2026, DFW is the only large-hub US airport with a published, multi-year digital twin operations contract. Of 31 large-hub US airports, 17 remain in pilot or planning stages. Globally, only four airports — Dubai (DXB), Singapore (SIN), Amsterdam Schiphol (AMS), and London Heathrow (LHR) — have moved a digital twin beyond pilot operations. The gap between financial case and deployment is structural, not financial. [Source: https://dwuconsulting.com/dwu-ai/twin]

4. **Condition-based maintenance at Schiphol demonstrates what a scaled deployment looks like — and what it requires.** In 2021-2022, Schiphol deployed 300 sensors on baggage conveyors and other assets via private LoRaWAN infrastructure. Over 10 months, the anomaly detection model triggered 42 inspections; 83% of triggered inspections found real problems; 60% of those required active intervention. The program's own post-mortem found that 26% of historical incidents could have been identified before they occurred with this architecture. The program is continuing to expand. [Source: https://www.vanderlande.com/news-insights/providing-condition-based-maintenance-at-amsterdam-airport-schiphol/]

5. **Network layer choices made in 2018–2022 are already obsolescing in some cases.** 2G/3G IoT deployments are being actively decommissioned across major markets. Sigfox's dedicated LPWAN network is in post-acquisition limbo. Wi-Fi-based asset tracking deployments (those using passive Wi-Fi probe sniffing for passenger flow) have been undermined by iOS 14 and Android randomized MAC addresses, rendering triangulation-based people-counting inaccurate without hardware changes. Technologies built on unlicensed spectrum (LoRaWAN, Zigbee) or licensed spectrum with mature 3GPP integration paths (LTE-M, NB-IoT) have substantially better 10-year horizon survival probability. [Source: https://iotsquad.tech/iot-connectivity-2025-expert-guide/]

6. **The OT/IT security boundary is the most frequently underestimated architectural risk.** A Pacific Northwest airport sustained a Rhysida ransomware attack in August 2024, forcing employees to handwrite boarding passes, triggering 90,000+ breach notifications, and consuming over 4,000 hours in emergency response. The ransom demand was 100 Bitcoin (~$6.5 million). A separate September 2025 attack on a shared check-in system simultaneously compromised operations at Heathrow, Berlin Brandenburg, and Brussels — what incident responders called "one system, one target, massive damage." In both cases, the architectural failure was inadequate segmentation between IoT/OT infrastructure and operational IT. [Source: https://rm-cyber.com/resource/articles/lessons-from-unanticipated-ot-and-iot-vulnerabilities-at-major-airports/]

7. **Open-protocol architectures solve the stranding problem by design.** The Deloitte airport IoT study found only 12% of airport representatives consider their organizations "very prepared" to benefit from IoT. The airports that have successfully deployed at scale share a common pattern: they treat data portability as a procurement requirement, not a vendor benefit. The adoption of MQTT and AMQP/REST as the integration surface — rather than proprietary device SDKs — is the specific architectural choice that separates programs with migration optionality from those that are silently single-vendor by year 3. [Sources: https://www.deloitte.com/us/en/insights/industry/government-public-sector-services/iot-in-smart-airports.html; https://pmc.ncbi.nlm.nih.gov/articles/PMC6864635/]

---

## Evidence: The Stranded Deployment Pattern

### Why Programs Stall

The Cisco finding is worth sitting with: 60% of IoT PoCs stall, and 60% of respondents said IoT initiatives "prove much more difficult than anyone expected." This is not primarily a sensor problem or a budget problem. The top five failure factors Cisco identified are: time to completion, limited internal expertise, quality of data, integration across teams, and budget overruns. Four of those five are architectural governance problems. Only one (budget) is a funding problem, and it consistently arrives *after* the integration and data quality failures surface — not before.

The McKinsey framing is sharper: many airports have "legacy software systems, scattered data, and stalled infratech projects that seem forever stuck in pilot mode." The 84% pilot-mode figure reflects a specific dynamic in airports: departments that procure IoT pilots rarely procure with a migration or data ownership path in mind. The pilot proves technical feasibility. It fails to prove organizational scalability. The contract expires. The data stays in the vendor's format.

### The Platform Dependency Problem

Google Cloud IoT Core is the cleanest case study because it is recent, documented, and involved a hyperscaler — a vendor no airport IT department would have flagged as exit-risk at procurement. Google launched the product in 2017, built it on MQTT and HTTP with proprietary device SDKs deeply embedded in firmware, and shut it down in August 2023 with 12 months' notice. Organizations that had built on it using Google's proprietary registry model and device token architecture faced non-trivial migrations — one analysis noted the MQTT protocol implementation "was proprietary and heavily embedded into device SDKs which could add greater complexity to migration." [Source: https://www.emqx.com/en/blog/why-emqx-is-your-best-google-cloud-iot-core-alternative]

Sigfox is the network-layer equivalent. By 2022 it had 10 million deployed devices across 70+ countries, a $300M raise, and a compelling propagation story for low-power sensors. Then it filed for bankruptcy, owing nearly €91 million net loss on €24 million in revenue. The French government had to intervene to prevent network shutdown during the sale process. Companies that had deployed Sigfox-only hardware — modules without cellular fallback — faced either continued dependency on the acquirer (UnaBiz) with no competitive alternative, or hardware replacement. Neither option was in the original capital plan.

The specific architectural lesson: the LPWAN layer is not commodity infrastructure in the way that Ethernet or TCP/IP is. It has vendor and carrier risk. Any airport IoT program that treats its network layer as a permanent given rather than a replaceable component is one corporate acquisition away from a stranding event.

### The Airfield Lighting Case: A Documented Proprietary-to-Open Migration

The Airport Lights Control and Monitoring System (ALCMS) provides a well-documented case of what legacy IoT lock-in looks like in safety-critical infrastructure. The existing proprietary AFS (Application Field Server) architecture used closed protocols that "cannot keep up with technology evolution in terms of software complexity and increased device heterogeneity." Integration with any third-party system required "prohibitively expensive" custom development. Security updates required vendor approval cycles.

The remediation architecture — an AFS-AMQP Gateway translating legacy proprietary protocols to standard AMQP and REST/JSON with OData — achieved maximum end-to-end delays of 43 milliseconds, well within the 500-millisecond regulatory constraint for stop bar operations. The architecture preserved the legacy hardware investment while creating a standardized data surface accessible to third-party developers. The lesson: even in safety-critical, regulatory-constrained environments, open protocol translation is achievable. The migration cost was lower than the continued lock-in cost. [Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC6864635/]

---

## Evidence: Network Layer Durability

For a 10-year horizon, the network technology decision is the single choice most likely to strand a deployment. The landscape as of 2026:

**LoRaWAN (Private)** is the strongest choice for high-density, cost-sensitive, facility-owned sensor networks. It operates on unlicensed ISM spectrum (915 MHz in North America), supports 5–10 year battery life on sensor nodes, carries zero recurring per-device fees on private deployments, and range in urban/dense environments of 2–5 km with appropriate gateway placement. Schiphol's private LoRaWAN deployment covers all public and non-public areas of the airport with a handful of gateways. The key durability risk: the Semtech LoRa chipset is the de facto standard but not the only implementation; the LoRaWAN Alliance open specification ensures forward compatibility regardless of chipset vendor. [Sources: https://www.kerlink.com/references-alliances/references/schiphol/; https://iotsquad.tech/iot-connectivity-2025-expert-guide/]

**LTE-M and NB-IoT (Cellular)** are now formally integrated into 3GPP 5G standards (Rel-15 onward), which means their lifecycle is tied to cellular evolution rather than a single vendor's commercial viability. LTE-M supports full mobility and handovers — useful for GSE and mobile asset tracking applications. NB-IoT provides superior deep indoor penetration and is better suited to static sensors in basements or dense building materials. Per-device annual costs run approximately $10–12/year in North America. For a 1,000-sensor deployment, that is $10,000–12,000 annually in recurring costs — manageable. For a 10,000-sensor deployment at a large hub, that is $100,000+ annually in recurring cost with no asset ownership of the network infrastructure. At that scale, private LoRaWAN becomes economically compelling even after gateway infrastructure costs.

**Private 5G (CBRS in US)** offers sub-5ms latency, supports high-bandwidth applications (video analytics, autonomous ground equipment), and enables unified connectivity for both IoT sensors and high-throughput devices. Dallas Love Field deployed the first airport CBRS private network in 2018 via Boingo and has expanded it to manage thousands of connected devices including ATC situational awareness systems. DFW deployed private 5G across 200+ access points. The durability case for private 5G is strong (CBRS spectrum licensing is a 10-year grant from the FCC), but capital costs are substantially higher than LPWAN, and the use cases that justify private 5G are specifically the high-bandwidth, low-latency applications — not basic environmental monitoring or asset location. Deploying private 5G because it's future-proofed and then using it to track restroom occupancy is capital misallocation. [Sources: https://airportscouncil.org/2023/06/09/airport-5g-update-leveraging-cbrs-for-smart-operations/; https://airportimprovement.com/article/love-field-deploys-next-generation-wireless-system/]

**Wi-Fi 6E** is the right choice for passenger-facing applications and for high-bandwidth back-office uses where infrastructure already exists. It is not a sensor network. Treating Wi-Fi as an IoT transport creates security exposure (shared network) and regulatory risk (Wi-Fi usage policies change with device operating system updates, as iOS 14 demonstrated with MAC randomization).

The durability hierarchy: private LoRaWAN ≥ LTE-M/NB-IoT >> private 5G (cost-justified for specific use cases) >> Wi-Fi (not a sensor network) >> Sigfox/proprietary LPWAN (exit risk demonstrated).

---

## Evidence: Integration Patterns

The integration question has a cleaner answer than most airport IT departments want to hear: event brokers win in operational technology environments. Enterprise iPaaS tools (MuleSoft, Boomi, Informatica) are designed for synchronous API integration between enterprise systems with moderate data volumes. IoT infrastructure is asynchronous, high-volume, and latency-sensitive. Forcing IoT data through a synchronous iPaaS layer introduces latency, creates single points of failure, and produces integration contracts that are difficult to version across firmware releases.

The high-performing pattern is: MQTT at the edge (device-to-gateway protocol) → lightweight event broker (MQTT broker or Kafka) for real-time stream processing → downstream consumption by SCADA, BMS, AODB, and analytics systems. This is the architecture underlying Schiphol Group's data streaming approach, documented in detail using Apache Kafka and Apache Flink. [Source: https://kai-waehner.medium.com/the-digitalization-of-airport-and-airlines-with-iot-and-data-streaming-using-kafka-and-flink-20861d7183ab]

The key architectural principle: the event broker is infrastructure, not an application. It should not be owned by a vendor that also owns the sensors or the analytics layer. When the same vendor provides the sensor, the integration platform, and the analytics dashboard, the airport has consolidated three layers of vendor dependency into one contract. When that vendor is acquired, pivots its business model, or changes its pricing, the exit cost encompasses all three layers simultaneously.

---

## Evidence: Edge Compute Placement

The rule is simple: processing that must survive a WAN outage belongs at the edge. Operational systems that control physical infrastructure — stop bar lighting, HVAC setpoints, access control triggers — cannot accept cloud round-trips as part of their decision loop. A 2024 Pacific Northwest airport ransomware attack demonstrated exactly what happens when operational technology is insufficiently isolated from internet-dependent systems: employees handwriting boarding passes is the physical manifestation of misplaced compute.

The practical framework:
- **On-sensor**: anomaly detection on continuous signals (vibration, temperature thresholds). Reduces data egress by 90%+ on high-frequency sensors.
- **On-gateway**: aggregation, protocol translation, edge ML inference for time-sensitive decisions (passenger queue depth, equipment fault classification).
- **On-premises**: SCADA/BMS control loops, real-time operational dashboards, data retention for regulatory compliance. Must operate when internet is unavailable.
- **Cloud**: analytics, model training, multi-airport benchmarking, reporting. No operational dependency.

Any airport IoT architecture that puts operational control logic in a cloud-only deployment is designing for the nominal case and ignoring the failure mode.

---

## Evidence: Vendor Strategy

The airports that maintain optionality share two procurement patterns. First, they require data export in open formats as a contract term — not as a vendor feature. The question at procurement is not "does your platform support data export?" (every platform does) but "what is the contractual penalty if data cannot be exported in schema-portable format within 30 days of contract termination?" That question changes the vendor conversation.

Second, they separate the sensor procurement from the platform procurement. A vendor that supplies both sensors and the cloud platform for those sensors has built a natural lock-in mechanism: the sensors only fully function with the platform, and migrating the platform means replacing the sensors. Treating these as distinct categories — evaluated separately, contracted separately, renewed on different cycles — preserves competition at both layers.

The specific failure mode that produces quiet single-vendor consolidation: a pilot deploys 20 sensors from Vendor A, using Vendor A's platform for data visualization. The pilot succeeds. Procurement expands the contract to cover 500 sensors. At 500 sensors, the switching cost has grown proportionally, and the business case for switching no longer pencils. By year 3, the airport has 2,000 sensors from Vendor A and a platform contract that auto-renews. The CISO flags the platform for security review. The ops team depends on it for daily operations. Nobody has budget to migrate. This is not a hypothetical sequence — it is the documented pattern of enterprise IoT consolidation.

---

## Counterexamples: Where Architecture, Not Operations, Was the Constraint

**Denver International Airport Automated Baggage System (1995):** The most documented large-scale airport technology failure in US aviation history. A $193 million contract scaled to $400+ million, delayed airport opening by 16 months, and produced a system that was largely decommissioned within years. The cause was not operational: it was architectural ambition that outstripped the technology's maturity. A system of 3,100 telecars, 5,000 optical detectors, and 55 networked computers had to be built in two years because project scope was expanded mid-development from one concourse to three. Independent consultants advised against the design timeline before construction began; their recommendations were not followed. The lesson for IoT: some architectural bets simply cannot be made before enabling technology matures. Pilot-to-scale failures that stem from missing sensor reliability or network immaturity are not organizational failures — they are correct responses to premature technology deployment.

**Private 5G for Autonomous Ground Equipment:** CBRS-based private 5G is not substitutable by LoRaWAN or LTE-M when the use case is autonomous tow tractors or autonomous baggage carts operating at airport apron speed. The sub-5ms latency requirement and the need for deterministic handoffs across the apron cannot be met by LPWAN technologies. Dallas Love Field's CBRS deployment was justified specifically because its ramp operations required guaranteed low-latency connectivity for vehicle-mounted devices that LPWAN could not provide. This is a legitimate case where network infrastructure investment was the correct answer — the operational need was real and the technology alternatives were genuinely insufficient.

**Video Analytics at Security Checkpoints:** No network technology short of fiber or Wi-Fi 6E/5G can transport uncompressed 4K video from 40 camera feeds per checkpoint. If the use case is real-time video-based threat detection or queue length estimation from camera feeds (rather than from occupancy sensors), the network must support the throughput. LoRaWAN is categorically wrong here. The architectural decision is not whether to use video analytics, but whether to process the video on-premise (eliminating most bandwidth requirements) or transmit raw feeds to cloud. Processing on-premise with edge GPUs changes the network requirement from hundreds of megabits to a few kilobits of metadata.

---

## Quotable Data Points for Strategists

**1.** "60% of IoT initiatives stall at the Proof of Concept stage. Only 26% of companies have had an IoT initiative they considered a complete success." — Cisco IoT Survey, 2017, n=1,845 IT and business decision-makers [Source: https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2017/m05/cisco-survey-reveals-close-to-three-fourths-of-iot-projects-are-failing.html]

**2.** "Of 31 large-hub US airports, 17 remain in pilot or planning stages [for digital twin deployments]. DFW is the only US large-hub airport with a published multi-year digital twin operations contract." — DWU Consulting, 2026 [Source: https://dwuconsulting.com/dwu-ai/twin]

**3.** "26% of incidents could have been identified before they occurred" — Schiphol Airport post-mortem on 300-sensor condition-based maintenance program, June 2021–April 2022 [Source: https://www.vanderlande.com/news-insights/providing-condition-based-maintenance-at-amsterdam-airport-schiphol/]

**4.** Google Cloud IoT Core was launched March 2017 and shut down August 2023 — six years of life for a hyperscaler IoT product. Sigfox, which raised over $300 million and operated IoT networks in 70+ countries, filed for bankruptcy in January 2022. Both events forced unplanned migrations on customers who had built on platform-dependent architectures. Neither event was theoretically unforeseeable; both were systematically underweighted by enterprise procurement frameworks. [Sources: https://akenza.io/blog/google-iot-core-shutdown; https://techcrunch.com/2022/01/27/sigfox-the-french-iot-startup-that-had-raised-more-than-300m-files-for-bankruptcy-protection-as-it-seeks-a-buyer/]

**5.** "To create massive damage, you just need to target one specific software." — Incident responder analysis of September 2025 ransomware attack on shared check-in system affecting Heathrow, Berlin Brandenburg, and Brussels simultaneously [Source: https://rm-cyber.com/resource/articles/lessons-from-unanticipated-ot-and-iot-vulnerabilities-at-major-airports/]

---

## Synthesis: What This Means for Capital Planning

The operational evidence converges on a single thesis: the stranding problem in airport IoT is not a procurement failure of choosing the wrong product. It is an architectural failure of not designing the surrounding decisions — data ownership, network layer, integration pattern, vendor separation — for a 10-year operational horizon rather than a 12-month pilot.

The airports that have moved beyond pilot at scale (DXB, SIN, AMS, LHR, and DFW among US large hubs) share an architecture that separates sensor hardware from platform software, that uses open-protocol integration surfaces, that processes operationally critical logic on-premises or at the edge, and that treats vendor portability as a procurement requirement enforced at contract signature rather than a future migration project.

The airports still in pilot mode — the 17 of 31 large-hub US airports that cannot yet point to a scaled IoT operation — are mostly not short on sensors. They are short on the organizational architecture around the sensors: the data governance, the integration ownership, the IT/OT boundary management, and the procurement discipline to keep vendor layers separable.

Building more infrastructure does not fix this. Changing how the surrounding decisions are made does.

---

*Sources consulted for this brief: Cisco Newsroom (2017), Deloitte Insights Smart Airports IoT study, DWU Consulting Airport Digital Twin analysis (2026), Vanderlande/Schiphol condition-based maintenance case study (2022), TechCrunch/Sigfox bankruptcy reporting (2022), Akenza/Google Cloud IoT Core shutdown analysis (2023), RMCyber airport OT/IoT vulnerability case studies (2024–2025), PMC/NCBI airfield lighting systems IoT paper (2019), ACI-NA CBRS/private 5G update (2023), Airport Improvement Magazine Love Field CBRS deployment, IoT Squad connectivity comparison guide (2025), IoT Now pilot failure analysis.*
