# Contrarian Brief: The Case for Infrastructure-First Thinking in BHS

**Council Run:** Baggage Handling Best Practices  
**Agent:** Contrarian — senior infrastructure advocate and capacity planner  
**Position:** The governance-failure narrative, while true for day-one disasters, systematically underweights the physical capacity constraints that make BHS degradation inevitable as traffic grows. You cannot process your way to infinite throughput on finite iron.

---

## 1. The Strongest Version of the Pro-Infrastructure Argument

**a. Physical throughput is arithmetic, not management.**  
Every BHS has a hard ceiling set by its iron: the linear feet of conveyor per minute, the cars per hour a sortation loop can process, the number of makeup positions, the square footage of Early Bag Storage, the count of claim carousels. No governance improvement, no testing discipline, no software layer expands that ceiling. At IAD today, peak-hour bag volumes are pressing against limits that were specified when the airport handled materially fewer passengers. The governance lessons from T5 and DEN are irrelevant to an airport that is running a 30-year-old system at 90% utilization. The question at that point is not "did we test it properly?" — it is "does the pipe have enough capacity?"

**b. The DEN '95 lesson is only half the story.**  
The canonical governance lesson from Denver is correct as far as it goes: integration testing was deferred, scope was added mid-build, no one was managing the interface. But the forensic record also shows the system was mechanically undersized and architecturally wrong from inception. The scope expansion to cover all airlines — added without corresponding physical capacity — meant the system was never correctly specified. Perfect governance applied to a physically insufficient design would have caught the problem earlier and cost even more to fix. The governance failure and the capacity failure were compounding, not independent. Separating them makes for cleaner lessons; it does not make for accurate ones.

**c. Aging infrastructure fails regardless of software quality.**  
The thesis is accurate for new BHS deployments. It is largely irrelevant for airports where the iron is old. A conveyor's design life is approximately 15 years without refurbishment [Source: https://www.aviationpros.com/airports/article/53072604/airports-plan-major-investments-on-baggage-handling-systems]. The United States is currently replacing systems that are 30 years old — double design life. Predictive maintenance software can give a 3-week warning that a bearing is about to fail [Source: https://www.sciencedirect.com/science/article/abs/pii/S0360835223000578]. It cannot replace the bearing. It cannot increase the conveyor's rated speed. It cannot add sortation capacity the system was never designed to have. At the point of asset exhaustion, the choice is not "software versus infrastructure" — it is "replace or close."

**d. EBS undersizing is a square-footage problem, not a governance problem.**  
Early Bag Storage capacity determines how much scheduling flexibility an airport has for connection bags. When EBS throughput cannot keep pace with peak inbound volume, the system creates a cascade: bags released too early create downstream congestion; bags held too long miss the sortation window; recirculation rates rise. The Beumer Group's own analysis is plain: "If its rate of flow cannot keep pace and help flatten the peaks, the system becomes a bottleneck" [Source: https://www.beumergroup.com/knowledge/airport/early-baggage-storage/]. Critically, the fix is throughput capacity and footprint — physical assets — not software. An airport can optimize its EBS scheduling algorithm indefinitely on an undersized EBS and still lose bags on the wave break.

**e. RFID read-rate claims are not operations claims.**  
The RFID enthusiasm sweeping the industry conflates two different problems. RFID improves tracking accuracy — knowing where a bag is — but it does not improve sortation capacity. A bag tracked at 99.9% accuracy by RFID that is sitting in an undersized EBS, or waiting for a congested sortation loop, or circling an overfull claim carousel is still a late bag. Amsterdam Schiphol achieved only 94.1% actual RFID read rates in operational conditions, against a 99% target [Source: https://www.researchgate.net/publication/220474820_The_state_of_RFID_for_effective_baggage_tracking_in_the_airline_industry]. The gap between vendor-quoted read rates in controlled pilots and operational reality at scale is systematic and well-documented. More fundamentally, the RFID investment is a data layer on top of the physical system — it does not substitute for physical capacity.

**f. Physical redundancy is the only reliable resilience strategy.**  
The airports that recover from sortation loop failures in hours — Frankfurt, Amsterdam, Atlanta — share one characteristic: physical redundancy. Parallel loop paths. Backup sortation capacity. Overflow carousel positions. Software-based degraded-mode operations require functioning physical infrastructure to switch between. When the primary loop fails and there is no alternate path, the software has nothing to route. Resilience briefs routinely undersell this point because physical redundancy is expensive capital expenditure and software-based redundancy management sounds more sophisticated. It is not. You cannot software your way through a mechanical failure when there is nowhere to re-route the bags.

**g. Europe's mishandling rate is infrastructure's report card.**  
IATA's 2024 mishandling statistics document a stark geographic divergence: Asia at 3.1 mishandled bags per 1,000 passengers; North and South America at 5.5; Europe at 12.3 [Source: https://avitrader.com/2025/06/13/asia-pacific-leads-in-baggage-handling-as-global-systems-improve/]. The technologists will attribute Asia's advantage to RFID penetration rates (88% full adoption in China and North Asia versus 40% in Europe). But Asia also has the newest BHS infrastructure on the planet — Changi, Hamad, KLIA, and a wave of greenfield Chinese airports built to current specifications in the last 15 years. The technology advantage and the infrastructure advantage arrived together. Attributing the performance gap solely to software adoption is the kind of correlation-causation confusion that sells consulting engagements.

**h. The $9 billion IAD program is a maintenance obligation, not a strategic choice.**  
MWAA's 15-year capital program at Dulles — projecting $9 billion in investment — includes new security, baggage, and terminal facilities [Source: https://www.mwaa.com/business/dulles-international-airport-capital-improvements]. This is sometimes framed as a strategic question: infrastructure versus operational intelligence. It is not. An airport cannot legally operate a baggage system it knows to be life-expired. It cannot ethically tell passengers their bags will make connections when the EBS lacks the physical capacity to guarantee the timing. The baggage tunnel question, the makeup room question, the sortation architecture question — these are capital-or-close decisions, not infrastructure-versus-software decisions.

---

## 2. Evidence

**Denver International Airport, 1995**  
The DEN baggage disaster cost an additional $560 million USD in delays, and the system was decommissioned entirely in 2005 — replaced by a conventional manual system [Source: https://sebokwiki.org/wiki/Denver_Airport_Baggage_Handling_System]. The post-mortem literature focuses almost exclusively on governance: no integrating systems engineer, scope expansion, deferred testing. What it tends to skip: the expanded scope added all airlines to a mechanical design specified only for United, without corresponding physical capacity. The governance failure occurred inside a capacity specification error. One does not cure the other.

**Heathrow Terminal 5, 2008**  
T5's opening-week failure had genuine software components (a testing filter left in the live system, insufficient server capacity). But it also had a building-baggage interface failure: the baggage system was physically incapable of handling transfer bags from other terminals because the connection infrastructure wasn't complete. Server capacity — "lack of server capacity and capability in handling the generated messages" [Source: https://www.studocu.com/en-gb/document/coventry-university/engineering-management/case-study-of-heathrow-terminal-5/16572656] — is itself a physical constraint. The T5 system processed up to 12,000 bags per hour by specification but was overwhelmed because the physical capacity was there on paper and not in practice. The lesson most often drawn — "you must test" — is correct. The lesson often missed: a system rated at theoretical peak throughput that cannot handle the actual operational load was never correctly sized.

**BER Berlin Brandenburg, opened 2020**  
BER opened nine years late and three times over budget, with inspectors having catalogued approximately 120,000 defects [Source: https://www.airportwatch.org.uk/2020/10/nine-years-late-and-x3-over-budget-due-to-problems-berlins-brandon-airport-finally-opens-during-a-pandemic/]. The governance failure thesis applies perfectly to BER. The infrastructure failure thesis applies equally: 170,000 kilometers of incorrectly wired cable cannot be fixed by software. The fire suppression system that failed inspection was a physical system. The baggage system's commissioning delays were partly driven by the fact that the physical building it was meant to operate within kept changing. Governance was catastrophic. But the governance catastrophe was in service of an infrastructure procurement that was chronically under-resourced.

**Conveyor Design Life and US Renewal Cycle**  
Standard industry design life for BHS conveyors is 15 years without major refurbishment. The US is currently executing a large-scale renewal of systems installed in the late 1980s through mid-1990s [Source: https://www.aviationpros.com/airports/article/53072604/airports-plan-major-investments-on-baggage-handling-systems]. Chicago O'Hare's Terminal 3 upgrade involved 14,361 linear feet of new conveyor; Seattle-Tacoma installed 7 miles of new conveyor infrastructure. These are not capability enhancements. They are depreciation schedules made physical.

**Amsterdam Schiphol RFID Trials**  
Schiphol handled 60–70 million bags annually and ran detailed RFID trials with six antenna arrays, achieving a 94.1% correct read rate versus the 99% target [Source: https://www.researchgate.net/publication/220474820_The_state_of_RFID_for_effective_baggage_tracking_in_the_airline_industry]. The 6-point shortfall is operationally significant: at 60 million bags, the 99% target misses 600,000 bags per year; the 94.1% actual misses 3.5 million. The vendors' controlled-trial conditions cannot replicate the interference environment of a live, congested BHS floor.

**Physical Sortation Limits**  
Cross-belt sorters face a physical speed ceiling: accuracy degrades materially above 2.5 meters per second. A carousel pusher loop sorter at 1 m/s handles up to 2,700 bags per hour per induction point [Source: https://alstefgroup.com/baggage-handling/solutions/high-speed-system/]. These are engineering constants. They cannot be optimized away. A peak 20-minute window at a large hub airport can require throughput 2.5 times the average hourly rate. If the physical infrastructure was sized for average, not peak, no software intervention closes the gap.

**EBS and Flow Rate as Physical Problems**  
The authoritative Beumer Group analysis of Early Bag Storage frames the problem correctly: "throughput speed tends to be more important than total storage size" — but both are physical specifications [Source: https://www.beumergroup.com/knowledge/airport/early-baggage-storage/]. Modern Delivery Buffer System (DBS) facilities are designed around flow rates that must be specified in square footage and equipment capacity at design time. Retrofitting an undersized EBS in an existing terminal is a capital project, not a software upgrade.

---

## 3. Scenarios Where the Thesis Is Wrong

The thesis — governance and testing discipline are the primary failure modes — is correct in three specific scenarios:

**Scenario A: Greenfield, day-one deployments.** For any new BHS opening, the primary risk is exactly what the thesis identifies: compressed testing, optimistic vendor throughput claims, and an owner unwilling to delay opening. DEN and T5 are canonical examples. The thesis is correct here and the lessons are actionable.

**Scenario B: Vendor performance specification fraud or incompetence.** When a vendor specs a system that cannot perform as promised, governance — specifically, rigorous acceptance testing and contractual leverage — is the right tool. The owner who signs off without independent verification is culpable. Again, the thesis is correct.

**Scenario C: Control system failures in otherwise adequate physical infrastructure.** When software routing logic, scheduling algorithms, or SCADA systems fail in a physically sound BHS, the fix is software governance. This is a real category of failure.

**Where the thesis fails:**

**Scenario D: Capacity exhaustion.** When traffic growth outpaces the physical throughput capacity a BHS was designed for, no governance improvement recovers lost bags. The system is not failing — it is operating correctly and at its limit. The only fixes are physical: new makeup positions, expanded sortation loops, additional EBS capacity. This is the scenario most relevant to IAD's current capital program.

**Scenario E: Life-expired assets.** When conveyors, drives, and sortation equipment have exceeded design life, governance is irrelevant. Testing a 30-year-old belt conveyor rigorously does not extend its service life. The asset renewal argument does not enter the governance-versus-intelligence framing at all, which is the framing's most important blind spot.

**Scenario F: Absent physical redundancy.** When a sortation loop fails and there is no alternate physical path, the system is down until it is repaired. Software-managed degraded-mode operations require alternate physical paths to manage. Airports with strong resilience (ATL, AMS, FRA) have invested in redundant physical infrastructure, not better degraded-mode software.

---

## 4. Claims a Strategist Must Address or Concede

**1. Europe's mishandling rate of 12.3 per 1,000 passengers is four times Asia's rate of 3.1, and the primary structural difference is infrastructure vintage, not governance quality.**  
IATA's 2024 data [Source: https://avitrader.com/2025/06/13/asia-pacific-leads-in-baggage-handling-as-global-systems-improve/] cannot be explained away as governance failure. Asia's airports are newer. The infrastructure is newer. The correlation between infrastructure vintage and operational performance is strong. If governance were the dominant variable, Europe would have closed the gap through process improvement alone by now.

**2. A cross-belt sorter running above 2.5 m/s begins to misdeliver bags. That is physics, not governance.**  
When throughput demand exceeds the designed physical capacity of the sortation technology, there is no governance intervention that maintains accuracy. The only response is capital investment — either in additional sortation lanes or in faster-throughput technology (DCV systems). Any BHS strategy brief that does not acknowledge physical throughput limits as hard engineering constraints is incomplete.

**3. The DEN system was not merely poorly governed — it was decommissioned and replaced with a manual system after $1.2 billion in total investment. That is an infrastructure verdict, not a governance verdict.**  
The system was decommissioned in 2005 [Source: https://sebokwiki.org/wiki/Denver_Airport_Baggage_Handling_System]. A governance lesson would have produced a repaired system. A system that gets torn out and replaced by manual carts was physically wrong. The strategist must account for why the best-tested, best-governed version of that system would not simply have reached its design limits sooner.

**4. Amsterdam Schiphol's operational RFID read rate was 94.1%, not the 99% promised — a miss of roughly 2.9 million bags per year at Schiphol's volume.**  
This is not a governance failure. The airport invested in the technology. The technology underperformed in the field relative to vendor claims. This is the track record that operational intelligence investments must be evaluated against: controlled-pilot read rates are not operational read rates.

**5. The US renewal cycle is replacing baggage systems that are 30 years old — twice their 15-year design life. That is a maintenance crisis that governance cannot cure and that software cannot defer.**  
At IAD, the relevant question is not "did we test our existing system properly?" It is "how long can we legally and safely operate infrastructure that is operating years past its design life?" The capital program is the answer. It is not one strategic option among several.

---

## Bottom Line for the Council

The governance thesis is not wrong. It is incomplete. Applied to new BHS procurements, it is the most important operational lesson in airport engineering. Applied to aging, over-utilized, life-expired infrastructure — which describes IAD's current situation with specificity — it is a distraction. MWAA's capital program should be evaluated on whether the physical specifications are correctly sized for 30-year demand projections, whether the architecture supports genuine redundancy, and whether the EBS and makeup areas are built to handle peak-hour bag volumes with margin. Those are infrastructure questions. The governance improvements should be designed around the capital program, not offered as an alternative to it.

The strategist who argues that better testing discipline is the primary lesson for IAD's BHS investment program has read the right history and drawn the wrong conclusion from it.
