# Airport COO Brief: IoT Architecture Durability
## Stage 1 Research — Independent Lens
### Prepared for the Transform Airports AI Council | June 2026

---

## KEY FINDINGS

**1. The failure mechanism is architectural, and it is predictable every time.**

Airport IoT deployments do not strand because sensors fail. They strand because the procurement decision was made for a 20-sensor pilot, and nobody ever went back to re-make it for 2,000 sensors across three terminals, two network upgrades, and one vendor acquisition. ACRP's Transformative Tech program identified that airport IoT data streams "frequently fall under vendor control," making airport access to their own operational data "challenging or costly." That is not a sensor problem. That is a contract problem nobody fixed between the pilot in Terminal A and the enterprise deployment the CEO announced the following year. [Source: https://crp.trb.org/acrptransformativetech/technology-focus-areas/internet-of-things/]

**2. Fragmentation is not a failure mode — it is the default outcome of incremental procurement.**

Toronto Pearson's Baggage 2025 program opened by consolidating seven independent SCADA systems, built on three separate platforms by three separate vendor teams, accumulated over 15 years of individually defensible upgrade decisions. Each decision was correct in isolation. Collectively they produced a system that was "very hard and expensive to support, upgrade and maintain" with "a large number of latency issues." Consolidation required converting 60,000 data tags, translating 100-plus graphical displays, and running parallel systems for 12 months. That is the compounded cost of 15 years of choosing the right sensor and ignoring the integration question. [Source: https://inductiveautomation.com/resources/customerproject/toronto-airport-moves-from-seven-scada-systems-to-one]

**3. Network architecture is the longest-lived decision in any IoT deployment and is consistently made last.**

A major hub's communications infrastructure is already fragmented across Wi-Fi, cellular DAS, proprietary OT networks, and hardwired control systems before the first IoT sensor is placed. When LoRaWAN, NB-IoT, and private 5G or CBRS layers are added on top, the result is competing protocols fighting for shared unlicensed spectrum, metal structures creating coverage gaps that undersized gateways cannot compensate for, and network operations teams who did not design any of these layers now responsible for keeping all of them running. The 40-percent-or-higher sensor dropout rates reported in dense airport deployments are not discovered in production — they are designed in during procurement and discovered at 5:45 AM on a Monday when the ops center starts getting alerts. [Sources: https://oxmaint.com/industries/aviation-management/airport-iot-network-architecture-lorawan-nbiot; https://www.nokia.com/asset/i/200638/]

**4. The SEA attack proved that the airport's own operational layer is the least-protected network on the campus.**

Seattle-Tacoma's August 2024 Rhysida ransomware attack took down display boards, check-in kiosks, the flySEA app, and parking systems. Employees used dry-erase boards for flight information. 90,000 individuals required breach notifications. What stayed up: FAA, TSA, and airline proprietary systems — because they were segmented. What failed: the airport's own operational layer, which was not. Nozomi Networks, which provides OT/IoT monitoring at major airports, explicitly flags "low visibility into mix of OT/IoT/IT systems and isolated networks" as the primary gap at large hubs. The lesson is not that airports are uniquely vulnerable. The lesson is that a passenger counting pilot does not need enterprise OT security; a 24/7 operational facility with 90,000 people's personal data and full terminal control does. The moment between those two states is where the re-architecture decision was never made. [Sources: https://www.bleepingcomputer.com/news/security/port-of-seattle-says-ransomware-breach-impacts-90-000-people/; https://www.nozominetworks.com/industries/airport-cybersecurity]

**5. Capital project handoff is where embedded IoT systems go to die — and operations is brought in too late to stop it.**

Burns McDonnell's analysis of master systems integration at airports found that program requirements for systems integration are "frequently omitted entirely" from program definition documents, with each contractor assuming "someone else is responsible for the MSI safety net." The result: large terminal openings hand operations a building with 100-plus technology systems that do not talk to each other, commissioned by people who would never work a shift desk in them, with no documented integration path. ACRP Report 59 identified the same pattern in 2011. Burns McDonnell found the same pattern in 2024. The 13-year gap between those observations is data. [Sources: https://info.burnsmcd.com/white-paper/master-systems-integration-is-secret-key-to-unlocking-efficiency-for-airports-and-the-aviation-industry; https://crp.trb.org/acrpwebresource2/wp-content/themes/acrp-child/documents/207/original/acrp_r59.pdf]

**6. Data ownership is a structural problem, not a negotiating detail.**

An airport that does not own its own queue dwell-time data cannot retender the contract using performance benchmarks. An airport that cannot export its own baggage sensor logs cannot diagnose why the claim rate went up in Terminal B on Tuesday morning without calling the vendor. ACRP is explicit: data streams "may fall under ownership of the vendor or solution provider," and accessing that data "can be challenging or costly." This is the architecture of most existing IoT contracts. It is also the reason most airports are renegotiating from a position of dependency rather than leverage. [Source: https://crp.trb.org/acrptransformativetech/technology-focus-areas/internet-of-things/]

**7. Open architecture is now an active regulatory direction — which means the prior 15 years of procurement are acknowledged as wrong.**

In November 2023, ACI EUROPE, TSA, ACI World, Avinor, and Heathrow released inaugural guidance establishing 18 baseline cybersecurity requirements for open architecture in airport security systems, calling for open data formats, standard interfaces, and interoperable components. This framework exists because the prior generation of procurement produced proprietary systems that airports cannot escape without writing a large check. It does not apply retroactively. Every airport reading that guidance is doing so while operating systems it describes as the problem. [Sources: https://www.passengerterminaltoday.com/news/security/aci-tsa-and-partners-release-inaugural-guidance-on-open-architecture-for-airport-security-systems.html; https://www.aci-europe.org/press-release/468-inaugural-guidance-on-open-architecture-for-airport-security-systems]

---

## EVIDENCE

### Network Layer Durability

Airport communications infrastructure is described by Nokia's connected airports research as "complex and usually fragmented, encompassing multiple separate networks with different radio and wired technologies, some owned and operated by the airport and others operated by independent service providers." [Source: https://www.nokia.com/asset/i/200638/] Adding LoRaWAN, NB-IoT, and private 5G on top of existing Wi-Fi and DAS layers produces a multi-layer management problem before a single sensor has been read.

LoRaWAN co-channel interference, non-LoRaWAN devices operating in shared ISM band, and gateway underprovisioning are recurring causes of high dropout rates in dense airport deployments. [Source: https://www.choovio.com/5-common-lorawan-network-issues-and-solutions/] Dallas Love Field deployed CBRS private LTE and reported measurable improvements in capacity and latency versus unlicensed spectrum. [Source: https://ongoalliance.org/news/americas-shared-spectrum-workhorse-cbrs-powers-airports-factories-rural-broadband-schools-and-more-nationwide/] Miami International uses CBRS to coordinate baggage systems and ground operations across its campus. [Source: https://www.boingo.com/good-stuff/cbrs-for-airports-secure-reliable-connections-that-streamline-operations/] CBRS is now deployed across more than 420,000 radios in US private networks.

The honest durability assessment: CBRS infrastructure purchased today probably survives one network upgrade cycle cleanly and one with moderate pain. The "two network upgrades" framing in the thesis is aspirational for most installations.

### Vendor Lock-In

Toronto Pearson's prior IT structure — 150 separate vendors for IT services — was so expensive to manage that consolidating to a single managed services provider (Wipro) produced a 94 percent reduction in major IT system outages and a 38 percent reduction in mean time to resolution. [Source: https://www.cio.com/article/306555/how-torontos-airport-modernized-its-it-operations-by-changing-the-vendor-relationship.html] The lesson is not that single-vendor consolidation is always correct. The lesson is that the cost of 150-vendor fragmentation was severe enough that paying for full consolidation still produced a positive ROI. Any airport evaluating its current multi-vendor IoT stack should run that calculation before the next upgrade cycle.

The ACI/TSA Open Architecture initiative is an institutional acknowledgment that vendor lock-in in airport security systems is structural, not an edge case. [Source: https://www.aci-europe.org/downloads/resources/TSA-230504-7_4.1%20Attachment%201%20OA%20for%20Airport%20Security%20Systems%202nd%20Edition%20%20FINAL.pdf] Google's shutdown of Cloud IoT Core — which stranded multiple enterprise deployments and forced emergency migrations — is the cross-industry example of what happens when the data architecture depends on a cloud service not under the deploying organization's control. Airports face the same risk from any IoT platform built on a vendor-controlled cloud layer. [Source: https://www.infolitz.com/blog-post/how-to-build-a-vendor-neutral-iot-ecosystem-and-avoid-lock-in]

### Capital Handoff Reality

DEN's $193 million automated baggage system is the original case of record: technology complexity underestimated at procurement, no contingency architecture, 72 uncompleted certification tasks when operations were expected to begin, monthly operating losses of $13-19 million once debt service started, total cost reaching approximately $360 million before a conventional $51 million backup system was installed. [Source: https://www.govinfo.gov/content/pkg/GAOREPORTS-RCED-95-35BR/html/GAOREPORTS-RCED-95-35BR.htm] That was 1994. Burns McDonnell found the same integration-omitted-from-program-definition problem in 2024. The airport industry invokes DEN as a cautionary tale and then reproduces its preconditions in every major capital program. [Source: https://info.burnsmcd.com/white-paper/master-systems-integration-is-secret-key-to-unlocking-efficiency-for-airports-and-the-automation-industry]

Denver International's March 2026 power outage is a recent capital handoff failure compressed into a single event. Xcel Energy energized a new transformer at a substation; the new equipment had no functional backup pathway during the transition. Result: 544 flight delays, 9 cancellations, a ground stop from 9:54 to 11:30 AM, and eight passengers trapped in elevators for up to 19 minutes. Airport IoT and smart systems went dark simultaneously because the underlying power architecture was not designed with adequate redundancy for the infrastructure replacement period. [Sources: https://www.cbsnews.com/colorado/news/denver-international-airport-power-outages-cause-xcel-energy/; https://www.denver7.com/lifestyle/travel/denver-international-airport-experiencing-power-outage-impacting-trains-to-terminals]

### OT Security

CISA published 508 ICS advisories in 2025 — the first year exceeding 500 — with an average CVSS score of 8.07. [Source: https://socradar.io/blog/cisa-industrial-control-systems-ics-advisories-2025/] GAO's March 2024 report (GAO-24-106576) found CISA had only four federal employees and five contractors available for OT threat hunting and incident response across all critical infrastructure. Vulnerability disclosure often takes more than a year from initial report to public advisory. [Source: https://www.gao.gov/products/gao-24-106576] Nozomi Networks' 2024 threat report found transportation rose from ninth to third place in OT/IoT vulnerability rankings. The surface area is growing because IoT deployment is growing faster than security architecture is keeping pace.

### MTBF Reality

Baggage handling systems: a healthy BHS should maintain less than 1 jam per 10,000 bags. Aging systems frequently reach 1 jam per 1,000 bags — a tenfold degradation. [Source: https://www.amygdalabs.com/airports/baggage-handling-systems-predictive-maintenance/] Vendor specifications do not reflect this degradation curve under real airport load conditions.

Escalators and elevators: John Wayne Airport — a mid-sized operation — paid $494,256 annually in regular servicing and $464,528 in average emergency services for vertical transport, nearly $1 million per year for a single mid-scale installation. [Source: https://files.ocair.com/media/2021-05/Item%203%20-%20Approve%20Contract%20for%20Elevator%20and%20Escalator%20Maintenance%20Services.pdf] Top-tier manufacturers claim 0.5 percent or less downtime. Operational data at high-traffic terminals runs higher.

IoT devices themselves: sensors, gateways, and industrial edge devices are engineered for 5-10 year operational lifespans. In practice, the surrounding ecosystem — firmware support, cloud platform availability, protocol compatibility — obsoletes them before the hardware fails. The device still reads temperature. The cloud platform it reported to was sunsetted. That is the stranding mechanism.

### IROPS Dependency

The DFW/Love Field telecommunications failure of September 19, 2025: two cut fiber optic cables took out both the primary and backup FAA data pathways simultaneously. American Airlines managed nine departures from DFW in the 3-6 PM window versus its normal 100 per hour. More than 1,000 delays and 600 cancellations resulted across Friday and Saturday. FAA's statement: "the urgent need to modernize." [Source: https://www.govtech.com/transportation/tech-outage-snarls-hundreds-of-flights-at-dallas-area-airports] Southwest's December 2022 crew scheduling collapse — 16,700 flights canceled, 2 million passengers, $800 million in refunds — was not weather. It was IROPS caused by technology scaled from 58 to 120 destinations without being replaced. [Source: https://en.wikipedia.org/wiki/2022_Southwest_Airlines_scheduling_crisis] The airport-side lesson: when airline IROPS technology fails, the airport operations center absorbs the volume. Gate agents who cannot get crew assignments call the ops desk. Technology failure at the airline maps directly to workload at the airport.

48 percent of airport leaders report a lack of data and insight when disruption occurs; 38 percent report difficulty cascading key information between stakeholders during disruption events. [Source: https://www.airportsinternational.com/article/irops-preparing-worst] Those numbers do not improve while operational data stays siloed across systems that share no common integration layer.

---

## THE OPERATIONAL CASE FOR AND AGAINST

### The Case For — As the COO Sees It

This thesis is right about the failure mechanism. That is rare in airport technology writing. Most post-mortems blame the sensor or the vendor. This thesis places the fault where it actually lives: the architecture decisions that were made for a 20-sensor pilot and never revisited when asked to cover 2,000 sensors across three terminals.

The thesis is right that "what's the best sensor" is the wrong question. I have watched procurement committees spend three months on sensor specifications and 45 minutes on the data ownership clause. The sensor will work. The question is whether we can still read its data in year six when the vendor has been acquired and the cloud platform has been renamed twice.

The "three vendor changes, two network upgrades, one CIO turnover" framing is operationally honest in a way that strategy decks never are. CIO turnover at airports is real, and it is not the only turnover that matters. The network engineer who built the LoRaWAN gateway configuration for the 2018 pilot. The facilities technician who knows which BACnet address maps to which HVAC zone because it was never formally documented. Architecture that is not self-documenting and standards-based does not survive the personnel turnover that is a certainty at any organization over a 10-year horizon. Paris Orly's Windows 3.1 failure is not an IT anecdote — it is what knowledge dependency looks like when you wait long enough.

The open architecture direction from ACI/TSA/Heathrow/Avinor validates the thesis from a regulatory angle. Those institutions do not publish guidance documents because everything is going well.

### The Case Against — What I Would Bring to This Council

**The thesis understates the procurement constraint.** Airport capital programs are funded, designed, and procured under AIP grant assurances, FAA design standards, NEPA requirements, and local authority processes that can span 7-10 years from concept to ribbon-cutting. "Re-make the architecture decision for scale" is not a 6-month project. The architectural standards this thesis calls for need to be embedded in program definition documents before the first design consultant is hired — which means the COO needs to be in the room at program definition, not at commissioning. Most airports are not structured that way. That is an organizational problem, not a technical one, and the thesis should say so.

**Open architecture creates its own attack surface.** Every open API is a target. The ACI/TSA Open Architecture guidance acknowledges this with its 18 cybersecurity requirements. The airport that opens its BHS SCADA to a REST API integration layer has made that layer a target. The SEA attack did not come through a closed proprietary system — it came through systems that were networked. Openness and interoperability are necessary conditions; they are not free.

**"Three vendor changes" is not always survivable in practice.** If the underlying hardware protocol is proprietary — Modbus RTU on a 15-year-old PLC, a BACnet profile that only one manufacturer's gateway can parse — the abstraction layer the thesis proposes sits on top of a hardware layer that cannot be cleanly abstracted. The realistic version of this architecture survives one vendor change cleanly and one network upgrade with moderate pain. Two clean vendor changes and two clean network upgrades is aspirational at most installations and should be framed as a target condition, not a baseline expectation.

**Data governance without organizational governance is worthless.** If the airport authority's governance model puts IoT data under the CIO, facilities management under the COO, and airline-facing operational data under the VP of Airline Affairs, then the data ownership provisions in the vendor contract are irrelevant — nobody inside the airport has unambiguous authority to act on unified data. The architecture is only as durable as the organizational model it sits inside. The thesis needs to say this.

---

## FIVE EXAMPLES THAT FRAME THE THESIS CONCRETELY

### 1. Toronto Pearson — Seven SCADAs, 15 Years, One Consolidation Bill

Over 15 years of incremental BHS upgrades, each procurement team chose the best available SCADA platform for that specific project. No integration requirement was specified. By 2019 the airport was operating seven independent SCADA systems on three platforms. The Baggage 2025 program could not begin modernization until it first consolidated its own supervisory layer: 60,000 data tags converted, 100-plus graphical displays translated, 12 months of parallel operation. No single procurement decision was wrong. The cumulative effect of 15 defensible individual decisions was a system that was broken as a whole. The architecture question that was never asked: at what point in the procurement of SCADA System #2 did anyone specify it must share a supervisory interface with System #1? [Sources: https://inductiveautomation.com/resources/customerproject/toronto-airport-moves-from-seven-scada-systems-to-one; https://www.internationalairportreview.com/article/181663/the-future-of-baggage-at-toronto-pearson/]

### 2. Seattle-Tacoma — The OT Security Architecture Failure

August 24, 2024: Rhysida ransomware. Display boards dark, check-in kiosks offline, flySEA app gone, employees on dry-erase boards. 90,000 breach notifications. FAA, TSA, and airline proprietary systems stayed up — they were segmented. The airport's own operational layer was not. This is the thesis's stranding mechanism operating in the security domain: the network architecture was designed for a campus where the airport's operational systems were not high-value targets. They became high-value targets when the IoT deployment grew. The re-architecture decision that should have happened as the deployment scaled never happened. [Sources: https://www.bleepingcomputer.com/news/security/port-of-seattle-says-ransomware-breach-impacts-90-000-people/; https://www.portseattle.org/news/port-seattle-providing-notice-individuals-affected-fall-2024-cyberattack]

### 3. Denver International Airport Baggage System (1994) — The Original

$193 million BAE contract. Technology never deployed at this scale. 17 miles of track, 5,500 conveyor miles, thousands of sensors — and no modeling of system-level interactions. 72 uncompleted certification tasks at expected commissioning. Monthly operating losses of $13-19 million. Total cost approximately $360 million. Conventional backup system installed for $51 million. Root cause: integration was treated as a residual, not a first-class design requirement. Burns McDonnell found airports still omitting integration requirements from program definition documents in 2024. The cautionary tale the industry invokes while reproducing its preconditions. [Source: https://www.govinfo.gov/content/pkg/GAOREPORTS-RCED-95-35BR/html/GAOREPORTS-RCED-95-35BR.htm]

### 4. Charlotte Douglas — Right Sensor, Unanswered Architecture Questions

CLT is embedding 2,000 sensors in its fourth parallel runway, opening September 2027. $6.5 million project, sensors designed for a decade of life, feeding FAA pavement research and a digital twin. First-in-the-nation deployment. The architecture questions not answered in any public statement: who owns the data pipeline after the UNC Charlotte research program concludes? When FAA's pavement research interest moves on, who maintains the integration? The sensors last a decade; the runway will be in service for 30-40 years — what is the plan for sensor generations 2 through 4? The digital twin requires a platform: what happens when that vendor is acquired? This is not criticism of CLT specifically. It is the standard condition of airport technology deployments — the sensor decision is made, the architecture decision is not. [Sources: https://country1037fm.com/2026/04/29/charlotte-douglas-international-airport-installs-2000-sensors-in-nations-first-smart-runway-project/; https://www.prweb.com/releases/bdi-selected-to-design-fabricate-and-install-first-in-nation-runway-pavement-sensor-system-at-charlotte-douglas-international-airport-302759212.html]

### 5. Paris Orly — What Knowledge Dependency Looks Like at End State

DECOR, linking Orly's ATC with Meteo France for low-visibility operations, ran on Windows 3.1. It failed in November 2015 and closed the runway. France had three specialists who could work with it. One was retiring without a replacement identified. The response was delayed because institutional knowledge of the system existed in three people rather than in documentation and a standards-based architecture anyone could interrogate. This is the "one CIO turnover" framing made concrete. It is not only the CIO. It is the network engineer who built the LoRaWAN configuration. It is the facilities technician who knows which BACnet address maps to which HVAC zone. Architecture that is not self-documenting does not survive personnel turnover, which is a certainty over any 10-year horizon. [Source: https://www.vice.com/en/article/windows-31-is-still-alive-and-it-just-killed-a-french-airport/]

---

## THE OPERATOR'S BOTTOM LINE

The thesis is right about the failure mechanism and right that this is an architecture question, not a technology question. But architecture does not exist in isolation. It exists inside a procurement process, a capital program structure, a contract, an organizational chart, and a governance model. All of those have to change simultaneously with the architecture, or the architecture will not survive the first organizational disruption that tests it.

The airports that get this right will write integration requirements into program definition documents before the first design contract is signed, require data portability as a non-negotiable contract term, designate a master systems integrator role with actual authority before construction begins, and treat network infrastructure as a 20-year decision rather than a 5-year one.

The airports that will not get this right are the ones where the COO finds out about the new IoT deployment at the same meeting where the vendor demos the dashboard.

I know which meeting happens more often. That is why this thesis is worth the council's time.

---

*Prepared from the operator's chair. All sources cited inline. No vendor briefings consulted; all evidence drawn from public audit records, ACRP research, regulatory guidance, and documented operational incidents.*
