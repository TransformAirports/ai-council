# COO Brief: Baggage Handling System Operations
## From the Operator's Chair — Baggage Handling Best Practices Council Run

**Prepared for:** AI Council — Stage 1 Research Brief
**Role:** Airport COO / 25-year hub operations perspective
**Date:** June 2026

---

## Key Findings

1. **The failure taxonomy is actually short.** Every major BHS disaster since 1995 — DEN, HKG, T5, BER — compressed to three root causes: scope expansion mid-build, testing that validated the system in lab conditions but never at design-day volume, and an owner who let political or commercial pressure override operational readiness. The technology was never the lead villain. Governance was. The thesis is correct on this, and the case is stronger for it.

2. **The operator's leverage over BHS is narrower than any capital deck will admit.** The airport owns the infrastructure and writes the standards. But TSA controls the inline EDS screening tempo, airlines control check-in discipline and how early bags feed the system, and ground handlers control bag loading and makeup area staffing. A sortation loop running at 98% read rate still fails on a Monday-morning irregular operations day when two airlines' third-party handlers are short-staffed and checking in passengers 90 minutes before departure instead of 2 hours. The BHS is only as reliable as the people on both ends of it.

3. **The "95% read rate" number hides the real operational problem.** Published barcode read rates average 75–85% in actual production environments, not the 99%+ in vendor specs [Source: https://www.internationalairportreview.com/article/75586/baggage-performance-rfid/]. Delta Air Lines' 97% barcode success rate — considered best-in-class — still meant 4 million bags per year with no confirmed routing. RFID pushes this toward 99.9% but depends on airline tag issuance, which the airport does not control. The gap between specified and as-operated performance is where operational pain accumulates, not in the sortation technology itself.

4. **Capital pays for the hardware; operations pays for the system.** The 20-year lifecycle cost of a BHS breaks roughly 35% CAPEX, 65% OPEX — energy, parts, labor, and maintenance contracts [Source: https://www.beumergroup.com/knowledge/airport/what-is-the-most-cost-effective-bhs-and-how-do-we-calculate-it/]. A jam rate of <1 per 10,000 bags is the benchmark for a healthy system; aging infrastructure routinely hits 1 per 1,000, requiring manual intervention at cost [Source: https://www.roycemedia.com/post/airport-system-availability-when-system-failure-breaks-operational-continuity]. Most airports design BHS to a capital budget, then discover in year 3 that the OPEX is what will actually determine whether the system holds up on the peak summer Saturday.

5. **Early Bag Storage is the most under-designed piece of the baggage chain.** Conventional EBS is sized for static capacity; high-performing airports (Frankfurt, Amsterdam, Atlanta) have migrated to dynamic bag storage sized for flow — specifically, the rate at which the system can intake and release bags to flatten the peak, not just hold them [Source: https://www.beumergroup.com/knowledge/airport/early-baggage-storage/]. Under-sized EBS turns the makeup area into the bottleneck on every day that schedule compression or irregular operations pushes early-check bags into the system simultaneously with same-day bags. That bottleneck is invisible in planning models.

6. **ORAT is the difference between a capital project and an operational airport.** Industry best practice calls for integrated operational trials no later than 4 months before opening, with transition planning starting 12 months out [Source: https://www.iata.org/en/services/consulting/airports/operational-readiness-and-airport-transfer-orat/]. In practice, ORAT is often treated as a late-stage activity that gets compressed when construction is behind schedule — which it always is. The result is a system that passes acceptance testing under controlled conditions and then fails on day one under real-world load, with real staff who have never run it before.

7. **Degraded mode is not a feature — it is an architecture decision.** The airports that recover from a sortation loop failure in hours rather than days are the ones that designed for graceful degradation before the first conveyor was installed. Cascading jam events require operator intervention within 20–30 seconds to prevent upstream blocking; systems that lack clear degraded-mode routing logic force controllers into manual reconciliation that can take hours to resolve [Source: https://www.roycemedia.com/post/airport-system-availability-when-system-failure-breaks-operational-continuity]. Most BHS designs optimize for throughput at design capacity; few are formally tested at degraded capacity.

---

## Evidence Section

**The DEN case as the canonical template.** Denver International's BHS opened February 1995, 16 months late, with cost overruns of $560 million attributed substantially to the baggage system. The system was originally scoped for United Airlines only; mid-construction, the city expanded scope to all airlines, dramatically increasing complexity without commensurate schedule or budget adjustment. Airlines were excluded from planning until late in the process, then required redesign of ski equipment handling, oversized luggage routing, and maintenance tracks. The automated system used unproven DCV technology at unprecedented scale. Integrated testing was never completed at design-day volume. The system was eventually decommissioned in 2005 and replaced with a conventional manual cart system — a $560 million lesson that the operator's community has largely failed to internalize. [Source: https://peimpact.com/the-denver-international-airport-automated-baggage-handling-system/; https://www.wrike.com/blog/lessons-learned-from-project-failure-at-denver-international-airport-why-checking-bags-is-still-a-pain/]

**T5 as the testing failure.** Heathrow Terminal 5 opened March 27, 2008. Within hours, 28,000 bags piled up across the terminal, 15% of British Airways' flights were cancelled over five days, and the total loss reached £16 million (approximately $32 million). The root cause was not a mechanical failure — it was a software filter forgotten after the pre-opening trials, staff who had not completed training with realistic loads (only 80% of staff had completed familiarization by opening day), and a system that had never been tested under live operational volume. Two BA directors resigned. Willie Walsh called it "not our finest hour." The system itself worked. The governance of commissioning it did not. [Source: https://calleam.com/WTPF/?p=473; https://spectrum.ieee.org/thousands-of-bags-miss-flights-at-british-airways-heathrow-terminal-5-again]

**HKG 1998 as the political-timeline failure.** Chek Lap Kok (HKIA) opened July 6, 1998, with commercial operations under intense political pressure to meet the handover anniversary. On opening day, up to 10,000 bags went astray. Cargo had to revert to Kai Tak by day three. Baggage wait times averaged 30 minutes versus the 20 at Kai Tak — the new airport was slower than the one it replaced. Signs malfunctioned, air conditioning failed, washrooms had no water. A large number of defects remained open at opening. This is the purest example of an owner who let a deadline override an operations-readiness gate. [Source: https://www.washingtonpost.com/archive/politics/1998/07/09/set-to-fly-hong-kongs-airport-flops-instead/b2a4d876-0d88-44e1-a092-7f859f206f6a/; https://app7.legco.gov.hk/rpdb/en/uploads/1998-1999/RP/RP01_98-99_19980716_en.pdf]

**The ACRP research baseline.** ACRP Research Report 252 (2023) — *Airport Baggage Handling System Decision-Making Based on Total Cost of Ownership* — provides the formal framework for BHS governance, procurement, and lifecycle cost analysis. It is the current state of the research art on this topic. [Source: https://nap.nationalacademies.org/catalog/27050/airport-baggage-handling-system-decision-making-based-on-total-cost-of-ownership]

**IAD capital context.** MWAA's $7 billion capital program at Dulles includes Concourse E (14 gates, United Airlines, 435,000 sq ft, autumn 2026 opening), with dedicated baggage tunnels, tug tunnels, and pedestrian walkback tunnels as part of the Tier 2 concourse program. This is the capital program that makes the BHS architecture question genuinely consequential: when you are designing dedicated underground baggage infrastructure, you are locked in for 40 years. [Source: https://www.mwaa.com/business/dulles-development-projects; https://www.ffxnow.com/2024/12/04/new-dulles-airport-concourse-on-track-to-arrive-in-2026/; https://www.hntb.com/projects/washington-dulles-international-airport-tunnel/]

---

## The Operational Case For and Against the Thesis

### The Case For (from the operator's chair)

The thesis holds up everywhere that matters to the operator. The failure taxonomy is accurate and short. The warning signs at DEN, HKG, and T5 were all visible before those systems went live — compressed testing schedules, scope changes late in design, staff training deferred to the last weeks before opening. An operator who had walked DEN's control center six months before February 1995 would have seen a system still in debug mode with no realistic end-to-end test on record. The same is true of T5's commissioning. The technology question is a distraction; the governance question is the only one that matters.

The claim that MWAA should evaluate its BHS investment against operational readiness and integration discipline rather than vendor specs is not just correct — it is the only framing that will survive first contact with actual operations. I have watched enough capital projects come over the fence to know that substantial completion on paper and operational readiness are not the same thing, and the gap between them is where the operator inherits the pain.

The argument for dedicated baggage tunnel infrastructure at IAD is also operationally sound, but only if the design phase answers the questions that the operator will be asking on day one: Where does the system go when a zone goes down? What is the degraded-mode routing? How much EBS capacity is built into the tunnel footprint, and is it sized for flow or just for static storage? These questions belong in schematic design, not in the commissioning phase.

### The Case Against (the operator's honest reservation)

The thesis risks overstating the degree to which governance failures are *avoidable* in the political reality of major airport capital programs. The DEN scope expansion that destroyed the BHS program was a political decision made above the operator's pay grade. T5 opened on schedule because BAA and British Airways had contractual and reputational commitments that could not be moved. HKG opened when it opened because the political symbolism of the handover anniversary was non-negotiable. 

The operator doesn't control the opening date. The operator controls whether there is a credible, documented operational readiness gate that gives leadership a factual basis for pushing back on a premature opening — but leadership can overrule that gate, and often does. The brief should be clear that the failure mode is not "airport management was incompetent." The failure mode is "airport management had the data they needed and the opening happened anyway." That is a different problem, and it requires a governance solution above the COO level, not just better commissioning discipline.

The other reservation: the "mature technology" claim in the thesis needs to be carefully bounded. BHS software — the control logic, the ATC (airport transfer cart) routing, the SCADA integration, the EDS interfaces — is significantly more complex in 2026 than it was in 2008. The BER cyberattack of 2025, which disrupted the Collins Aerospace-operated baggage and passenger handling system for days, is a reminder that the technology risk has migrated from hardware to software and vendor dependency, not disappeared. [Source: https://www.travelwires.com/disruptions-continue-at-ber-due-to-cyberattack-on-baggage-system/]

---

## Specific Examples That Frame the Thesis

### 1. Denver's DCV System: The $560M Lesson Nobody Applied

The DEN BHS used destination-coded vehicles — the highest-throughput, highest-flexibility sortation architecture. The technology was not wrong for the application; it was right. What was wrong was building it on a schedule that compressed end-to-end testing into weeks, with a scope that had been expanded by a year of late-breaking airline requirements. The system decommissioned in 2005 was not a bad DCV system — it was a DCV system that had never been properly commissioned. The replacement was not a better BHS; it was tug carts and conventional conveyors, which United already operated. The lesson: technology selection matters less than whether the selected technology is tested at volume before day one.

### 2. Heathrow T5: The Forgotten Software Filter

The T5 failure is the purest test-compression case on record. The baggage system passed pre-opening acceptance testing. The software filter that caused the failure was deliberately disabled during trials to allow the test to complete. It was supposed to be re-enabled before go-live. It wasn't. The staff who would have noticed the discrepancy hadn't completed hands-on training with the live system. The cascade took five days to clear. The COO's operational lesson: your commissioning checklist needs to document not just what was tested, but what was deliberately bypassed during testing and why — and who is accountable for restoring it before operations begin.

### 3. IAD Concourse E — The Next 90 Days Are the Critical Period

MWAA's Concourse E is targeting an autumn 2026 opening. It is a 14-gate facility with AeroTrain integration, dedicated to United Airlines, with baggage systems and ramp control upgrades as part of the program. The testing phase is scheduled for summer-fall 2026. That timeline means ORAT integration testing against design-day bag volumes needs to begin no later than June 2026 — now — to have any credibility as a meaningful operational validation rather than a certificate-of-occupancy exercise. The question I want answered before that opening: has the end-to-end BHS been run at peak United day volume, with EDS handoffs included, with the actual ground handler staffing that will be on duty at 6 AM on a Tuesday in October?

### 4. Early Bag Storage: The Invisible Bottleneck in the IAD Capital Plan

The MWAA tunnel program for Tier 2 is designed around baggage conveyor systems. That is the right infrastructure decision. The question is whether the EBS component of that infrastructure is sized for flow or for capacity. The difference is operational: a static-capacity EBS holds the bags; a flow-sized dynamic bag storage system can release bags to the makeup area in batches, on schedule, at the rate the sortation loop needs them. At IAD, where United operates a connection hub with tight turns and early-check volumes from international arrivals, an under-sized EBS is the bottleneck that will not show up in any planning simulation because planning simulations run the system at design-day average load, not at the combination of early-check international bags plus late-connecting domestic bags at 9 AM on the peak Wednesday of August.

### 5. BER's 2025 Cyberattack — The New Technology Risk Vector

Berlin Brandenburg Airport's 2025 cyberattack on Collins Aerospace (the airport's external IT service provider for the baggage and passenger handling system) triggered manual check-ins, baggage delays, and security checkpoint congestion for days. BER outsourced the software layer of its BHS to an external provider — standard practice, but it created a single point of failure that was exploited from outside the airport's own security perimeter. For MWAA's IAD capital program, this is a design constraint, not an operational afterthought: the software architecture of any new BHS, and specifically how it is isolated from third-party systems that have internet-facing exposure, belongs in the design documents, not the vendor contract. [Source: https://www.internationalairportreview.com/news/296718/cyber-attack-disruption-to-continue-at-ber/]

---

## The COO's Bottom Line for the Council

The thesis is operationally sound, and it gets stronger because it acknowledges operational reality rather than retreating to vendor specifications. The risk in the brief is over-rotation toward the governance narrative at the expense of the specific questions the operator needs answered during design.

For IAD: the capital program is the right moment to design for degraded mode first and peak throughput second. Every airport that has failed a BHS opening failed it because the system was optimized for design-day performance and never stress-tested for the day it breaks. Design the degraded-mode routing. Size the EBS for flow, not just capacity. Run the ORAT at realistic volume before October 2026, not in the last four weeks before the ribbon gets cut. And document explicitly — in writing, signed by the COO — what the operational readiness gates are and what authority overrides them.

That's the job. The technology will work if we let it be tested properly. The governance will hold if we build the gates before the political pressure to open arrives.

---

*Sources cited inline throughout. Primary sources: ACRP Research Report 252 [https://nap.nationalacademies.org/catalog/27050]; IATA ORAT Best Practices [https://www.iata.org/en/services/consulting/airports/operational-readiness-and-airport-transfer-orat/]; International Airport Review BHS coverage [https://www.internationalairportreview.com]; MWAA Dulles Development Projects [https://www.mwaa.com/business/dulles-development-projects]; BEUMER Group EBS analysis [https://www.beumergroup.com/knowledge/airport/early-baggage-storage/]; BER cyberattack reporting [https://www.internationalairportreview.com/news/296718/cyber-attack-disruption-to-continue-at-ber/]; T5 case analysis [https://calleam.com/WTPF/?p=473]; DEN case studies [https://peimpact.com/the-denver-international-airport-automated-baggage-handling-system/]; Washington Post HKG 1998 [https://www.washingtonpost.com/archive/politics/1998/07/09/set-to-fly-hong-kongs-airport-flops-instead/b2a4d876-0d88-44e1-a092-7f859f206f6a/]; ENR Concourse E milestone [https://www.enr.com/articles/61094-new-dulles-airport-concourse-reaches-construction-milestone].*
