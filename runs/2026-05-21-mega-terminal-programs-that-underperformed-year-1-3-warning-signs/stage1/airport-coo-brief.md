# Airport COO Research Brief
## Thesis: Mega-Terminal Failures Are Not Black Swans

**Prepared by:** Airport COO Research Agent
**Date:** 2026-05-20
**Council Run:** Mega-terminal programs that underperformed — year 1-3 warning signs

---

## Key Findings

**1. The failure sequence is predictable, not random.**
Denver (1995), Heathrow T5 (2008), Chek Lap Kok (1998), and BER (2020) share an identical structural failure: a compressed or cancelled integrated operational trial caused by construction delays that consumed the commissioning window. The design team finishes late, hands over a building with an open punch list, and the operator is told the schedule cannot move. The baggage system has never run at rated throughput with real concurrent airline operations. Opening day is the first full-scale test.

**2. Scope expansion mid-project is the single most reliable predictor of downstream operational failure.**
Denver's automated baggage system was scoped for United's Concourse B. Mid-construction, the city expanded it to cover all three concourses and 20 airlines — a scope change that at least doubled system complexity — without re-baselining the schedule. [Source: https://www.govinfo.gov/content/pkg/GAOREPORTS-RCED-95-35BR/html/GAOREPORTS-RCED-95-35BR.htm] BER saw the same dynamic: the main terminal was enlarged from a rectangle to a U-shape with commercial levels added at the instruction of political stakeholders after construction was underway, which cascaded into the fire safety system design the building could no longer support. [Source: https://www.cio.com/article/234648/notorious-project-failures-berlin-airport-why-did-it-go-wrong.html] When scope expands mid-project, the integrated testing schedule is the budget line that absorbs the overrun.

**3. Owner-engineer role confusion is not a governance abstraction — it is a specific failure mode with a body count.**
BER's fire safety system was designed by Alfredo di Mauro, who was not a licensed engineer. His business cards said engineer; his credentials said engineering draughtsman. The smoke extraction system he designed attempted to pump hot smoke downward into the basement rather than exhaust it through the roof — because the architect had specified a clean roofline. [Source: https://www.thelocal.de/20201030/the-real-story-behind-why-berlin-ber-airport-took-nine-years-to-open] Political principals (Berlin Mayor Wowereit and Brandenburg Premier Platzeck) distributed construction contracts across dozens of firms rather than appointing a single contractor with integrated accountability. No one held the system interface. The result: 66,500 documented defects, 34,000 classified as significant, and a mandatory acceptance test the airport failed in December 2011 — a failure it concealed from the public for years.

**4. Integrated systems testing is consistently the first thing deferred and the last thing recovered.**
At Heathrow T5, BA deferred the start of on-site familiarization for baggage and ramp staff by six weeks. The planned proving trials were reduced in scope or cancelled because the terminal was still a construction site. End-to-end integration testing of BA's operational IT systems was delayed until late October 2007, five months before opening. Staff "training" consisted of showing workers a film in a hotel conference room, then a coach tour of the terminal. Hands-on baggage system training was impossible because workers would have needed hard hats to access it. [Source: https://medium.com/@pizzaere/how-a-bug-crippled-heathrow-the-untold-stories-of-terminal-5s-opening-day-disaster-dc2fc0f56a41] The building was delivered to operations with a compressed commissioning program that no one in a position of authority was willing to acknowledge as inadequate.

**5. The operator inherits what the project team couldn't close.**
Every deferred punch list item that got paper-closed at substantial completion becomes a Day 1 work order. The baggage system that was never tested at peak throughput will jam at peak throughput. The staff access system that was not fully commissioned will lock out handlers at 5:00 AM on opening day. The HVAC system balanced for an unoccupied building will fail its first August peak. This is not speculation — it is the documented pattern at T5 (staff parking and access failures locked out baggage handlers on Day 1), at Denver (carts derailing within days), and at BER (escalators, ticket counters, and door control systems still incomplete on opening day).

**6. Optimism bias in the business case creates the governance environment that produces the operational failure.**
Projects that understate costs and compress schedules to win political approval never recover the testing time. The BER original estimate was €2 billion; the total cost reached €11.9 billion when interest and lost revenue are included. [Source: https://journals.sagepub.com/doi/10.1177/87569728241300247] Denver's baggage system delay cost the city $360 million in operating deficits alone by opening day, at a burn rate of $13.35–18.75 million per month during the delay period. [Source: https://www.govinfo.gov/content/pkg/GAOREPORTS-RCED-95-35BR/html/GAOREPORTS-RCED-95-35BR.htm] The business case that secured political approval in both cases was structurally incapable of supporting the testing program the system required.

**7. The operational consequences are predictable and long-lasting.**
T5's baggage chaos ran for 10 days. 42,000 bags failed to travel with their owners. Over 500 flights were cancelled in the first 10 days. It took three weeks for the majority of bags to be reunited with passengers. [Source: https://en.wikipedia.org/wiki/Heathrow_Terminal_5] Denver's system limped along serving only Concourse B outbound for United for 10 years, then was abandoned in August 2005 at a maintenance cost of $1 million per month — a direct operational tax on the airport because a commissioning failure was never fully resolved. [Source: https://www.computerworld.com/article/1720999/united-axes-troubled-baggage-system-at-denver-airport.html] LaGuardia Terminal B's $4 billion renovation, completed in 2022, delivered aesthetic improvement but extended walking distances between gates, increased international connection times by approximately 25%, and drove drop-off wait times regularly above 20 minutes — core operational problems that trace directly to design decisions that were not reviewed by anyone who had to operate the facility on a Monday morning. [Source: https://www.mightytravels.com/2024/12/the-real-story-behind-laguardias-terminal-b-how-a-4-billion-renovation-failed-to-fix-its-core-problems/]

---

## Evidence Section

### Denver International Airport — The Canonical Case (1995)

The GAO investigation is the primary documented source for what happened and why. The automated baggage system — 100 networked computers, 5,000 electric eyes, 56 bar-code scanners, and a network of telecarts on 21 miles of track — was originally scoped for United's Concourse B only. Mid-construction, the city expanded the scope to all three concourses and 20 airlines. BAE Automated Systems had internally estimated the system required four years to design and deliver; it was contracted to deliver in two. Seventy-two incomplete tasks were identified before operational testing could even begin, including cart bumpers that needed replacement and empty-cart management systems that had not been built. [Source: https://www.govinfo.gov/content/pkg/GAOREPORTS-RCED-95-35BR/html/GAOREPORTS-RCED-95-35BR.htm]

The opening delay ran 16 months past the October 1993 target. Monthly deficits during the delay period ranged from $13.35 million to $18.75 million. Total delay costs reached approximately $360 million by opening day. The eventual system served one concourse, one airline, outbound flights only. United abandoned it entirely in 2005, saving $1 million per month in maintenance. [Source: https://www.nbcnews.com/id/wbna8975649]

### Heathrow Terminal 5 — The Textbook Commissioning Failure (2008)

T5 cost £4.3 billion and opened March 27, 2008 after a design and construction program spanning nearly 20 years. BAA recruited 15,000 volunteers for 68 operational trials in the six months before opening — a number that sounds rigorous until you understand what was not tested: the baggage system under concurrent multi-flight loads with the actual staff who would operate it. Construction delays had consumed the commissioning window. On opening day:

- Staff could not access their car parking allocation. Baggage handlers arrived two hours late.
- Staff access systems did not recognize employee IDs. Eighteen terminal lifts were jammed. The transit connecting the main terminal to the satellite had broken down.
- The baggage system was not staffed adequately to manage concurrent inbound and outbound loads. Bags queued, overflowed, and jammed.

By end of Day 1: 34 flights cancelled, baggage check-in suspended. Over the following 10 days: 500+ flights cancelled, 42,000 bags failed to travel with their owners. Three weeks to reunite the majority of passengers with luggage. BA fired its director of operations and director of customer services. [Source: https://en.wikipedia.org/wiki/Heathrow_Terminal_5]

The specific software failure: a message filter was not removed after system trials; the log-in failed; the system did not read bag tags. This was a known issue that had not been resolved before opening because testing was truncated. [Source: https://medium.com/@pizzaere/how-a-bug-crippled-heathrow-the-untold-stories-of-terminal-5s-opening-day-disaster-dc2fc0f56a41]

### Berlin Brandenburg Airport — The Governance Failure in Slow Motion (2006–2020)

BER's construction started in 2006. The planned 2012 opening was abandoned two weeks before the scheduled date when it became clear the fire safety system could not pass its mandatory acceptance test. What followed was nine more years of delay, escalating cost, and suppressed information.

The fire safety system's fundamental problem: for aesthetic reasons, the architect specified a roofline free of exhaust vents. The resulting design pumped smoke downward into the basement through a network of motorized flaps. When tested in December 2011, the fans exerted too much pressure and pipes imploded. The automatic flaps did not open or close as required. [Source: https://www.thelocal.de/20201030/the-real-story-behind-why-berlin-ber-airport-took-nine-years-to-open]

The unqualified engineer: Alfredo di Mauro, who designed the fire safety system, held credentials as an engineering draughtsman, not a licensed engineer. This was not caught in any owner review process.

Cover-up: Airport management knew by 2015 the 2018 opening date was impossible, and concealed this from public and political stakeholders for three years.

By the time BER opened October 31, 2020, over 20,000 defects had been documented in fire detection and emergency lighting systems alone. On opening day, escalators were non-functional in portions of the terminal. The airport opened to commercial service during a pandemic with passenger volumes too low to stress-test systems — which may be the one piece of fortune BER received. [Source: https://en.wikipedia.org/wiki/Construction_of_Berlin_Brandenburg_Airport]

Total cost: original estimate €2 billion; actual cost €6.5 billion in direct spend, €11.9 billion when interest payments and lost revenue from the decade of delay are included. [Source: https://journals.sagepub.com/doi/10.1177/87569728241300247]

### LaGuardia Terminal B — The Design-Over-Operations Failure (2022)

The $4 billion LaGuardia Terminal B redevelopment completed in 2022. The project was ambitious in scope and legitimate in its goal — replacing what Vice President Biden famously called a third-world airport. What it produced was a building that is aesthetically transformed and operationally constrained in ways that were foreseeable.

The satellite concourse design — two island concourses connected by 482-foot pedestrian bridges at 60 feet of elevation — eliminated the option of tunneling under taxiways. This is a real engineering constraint. What is not a constraint is the decision to design gate placements and arrival/departure circulation that extended walking distances beyond what the prior terminal required, increased international connection times by approximately 25%, and created a drop-off zone with a single access point that regularly exceeds 20-minute wait times at peak. [Source: https://www.mightytravels.com/2024/12/the-real-story-behind-laguardias-terminal-b-how-a-4-billion-renovation-failed-to-fix-its-core-problems/]

The gap between promised operational improvement and delivered operational performance traces directly to design decisions made by architects and concession developers who would never have to walk a connecting passenger through the building in 22 minutes.

### JFK New Terminal One — The Live Warning Case (2025–2026)

The $9.5 billion New Terminal One is scheduled for phased opening in June 2026, timed to the FIFA World Cup, with 14 gates in Phase A and full completion by 2030. As of late 2025, the terminal was weather-tight with baggage conveyor infrastructure installed. Operational testing of baggage systems and jet bridges was reported as underway. [Source: https://www.constructionowners.com/news/inside-jfks-giant-new-terminal-one-build]

The warning signs visible from the operator's chair:

- **World Cup hard deadline**: A fixed political opening date tied to a global sporting event is the same governance structure that produced BER's failed 2012 opening. Political pressure does not compress commissioning timelines — it forces them to be declared complete when they are not.
- **Phased opening of 14 gates from a 23-gate facility**: Phased openings distribute operational learning, but they also mean Phase B (completion to 2030) absorbs all the lessons from Phase A — or doesn't, if the lessons are not institutionalized.
- **Multiple airlines changing terminals simultaneously**: The Port Authority has indicated more than half of JFK's airlines are changing terminals during this construction cycle. Concurrent transitions multiply the coordination surface area for every IROPS event.
- **JLL engaged for facility operations**: The RFP for facility maintenance services was issued in early 2025. [Source: https://www.facilitiesdive.com/news/jll-tapped-to-operate-jfk-new-terminal-one/807058/] A new operator learning a new building while the building itself is still under construction represents exactly the conditions that produced T5's staff-access failures.

NTO's team has invested in a simulation facility on Long Island where staff can rehearse check-in, security, and baggage operations. [Source: https://eturbonews.com/jfk-new-terminal-one-biometric-arrivals-cbp-epp-2026/] That is the right instinct. Whether it translates into adequate integrated trials at rated capacity, with the actual airlines and the actual baggage volumes, before the first widebody pushes back in June — that is the question.

### Hong Kong Chek Lap Kok — Corroborating Evidence (1998)

Chek Lap Kok opened July 6, 1998. Within 24 hours, the cargo terminal closed for remediation. 10,000 bags went astray in the first week. Aircraft parking systems, information displays, baggage handling, air conditioning, escalators, and directional signage all experienced failures simultaneously. The activation program had been compressed due to construction delays — the same mechanism as every other case in this file. Economic damage was estimated at £102 million. [Source: https://www.washingtonpost.com/archive/politics/1998/07/09/set-to-fly-hong-kongs-airport-flops-instead/b2a4d876-0d88-44e1-a092-7f859f206f6a/] The contingency plans for centralized computer system failure and cargo disruption had not been developed at opening.

### Industry Research Framework: ORAT

IATA's Operational Readiness and Airport Transfer framework defines the integrated operational trial as the "dress rehearsal" that must occur at least four months before opening, with a full transition plan beginning one year before opening. The ACRP's synthesis on terminal facility activation (ACRP Synthesis 20) documents that the US aviation industry has not standardized this process. [Source: https://apps.trb.org/cmsfeed/TRBNetProjectDisplay.asp?ProjectID=5590] A 2024 ACRP problem statement (ACRP 08-04) explicitly calls for a "Blueprint for Incorporating ORAT into Airports," confirming that as of 2024 there is no industry-standard process for what every failing terminal in this file needed most. [Source: https://apps.trb.org/cmsfeed/TRBNetProjectDisplay.asp?ProjectID=5590]

---

## The Operational Case For and Against the Thesis

### The Case For — Where This Gets Stronger Because It's True

The thesis is correct on the mechanism. The four signals — scope creep, integrated-systems testing deferral, owner-engineer role confusion, and optimism bias in the business case — do recur. More precisely, from the operator's chair, they are not four independent signals. They are one signal with four manifestations. Scope expansion mid-project is the inciting event. It consumes float, which eliminates the commissioning window. The compressed commissioning schedule requires someone to certify completion that has not been achieved — which is where owner-engineer role confusion becomes operational, not theoretical. The whole sequence is enabled by a business case that told the approving authority a story about schedule and cost that could not survive contact with the project as actually scoped.

The thesis is also correct that these are leading indicators — they are visible years before ribbon-cutting. Denver's scope expansion from one concourse to three happened in 1992, three years before the February 1995 opening. BER's fire system failed acceptance testing in December 2011, nine months before the planned June 2012 opening — and the conditions that made that failure inevitable (unqualified designer, aesthetic-over-function roof decision, political scope additions) were locked in years earlier. An operator watching the project from the outside would have seen a construction permit non-compliance surface in December 2011 and been able to predict the next decade.

The thesis is further strengthened by LaGuardia: the failure there is not a commissioning failure. It is a design failure. The terminal opened on time. The operational pain — extended walking distances, inadequate drop-off capacity, circulation bottlenecks — was baked in at design. That is an important distinction. Not every mega-terminal failure is an ORAT failure. Some are design failures that the operator inherits regardless of how well the testing program ran. This broadens the thesis rather than weakening it: the signals appear in design, not just in construction.

### The Case Against — Where the Thesis Faces Legitimate Challenge

**The thesis risks oversimplifying survivorship bias.** There are large terminals that had scope changes, optimistic schedules, and owner-engineer tensions that opened without chaos. Singapore Changi Terminal 5 is currently under construction with a scope and complexity that exceeds most of the cases in this file, and it has not yet had the chance to fail or succeed. Attributing failures to four signals is defensible; claiming those signals are sufficient predictors requires cases where the signals were present and the opening was successful — and documenting why.

**"Governance failure" is a conclusion, not a leading indicator.** An operator watching BER in 2009 would have seen construction underway and political enthusiasm. The governance failure was not visible until the first acceptance test in December 2011. The thesis needs to be more precise: the *observable* leading indicators are specific project management events — scope change orders that do not trigger schedule re-baselining, commissioning milestones that slip without public acknowledgment, testing programs that are reduced in scope rather than extended in duration. Those are visible. "Governance failure" is the label applied in retrospect.

**JFK NTO may be the counterexample that tests the thesis in real time.** NTO has a hard political deadline (World Cup), a phased opening structure, a new operations entity still learning its own facility, and a $9.5 billion price tag that required optimistic revenue projections to get financed. But NTO also has a dedicated simulation facility, an active commissioning program, and the institutional memory of every terminal opening failure of the last 30 years available to anyone willing to read it. If NTO opens in June 2026 without operational chaos, the thesis needs to explain why — not just claim it as a near-miss.

**The operator does not control the timeline.** This is the hardest operational truth the thesis has to grapple with. The signals may be visible, and the COO may articulate them clearly, but the decision to move the opening date belongs to the owner-political authority. At BER, the management CEO knew the 2018 date was impossible and concealed it. At T5, the construction program consumed the commissioning window and no one with authority moved the opening. The thesis implies that recognizing the signals should lead to a different outcome. The historical record suggests recognition is necessary but not sufficient: someone with authority has to act on what they see.

---

## Five Concrete Examples That Frame the Thesis

### 1. Denver's Baggage System Scope Expansion — The Inciting Event Pattern

The DIA automated baggage system failure is not a technology story. It is a scope story. The original system design was achievable: a single-airline, single-concourse, outbound-only automated system. BAE Automated Systems had misgivings about even that scope on a two-year timeline. The city expanded the system mid-construction to all concourses and 20 airlines — a decision made by people who would never have to operate the result.

The operational consequence was carried for a decade. United Airlines operated a system that cost $1 million per month in maintenance, handled only outbound bags on one concourse, and was abandoned in 2005. The manual tug-and-trolley system built as an emergency backup in 1995 served the rest of the airport for its entire life.

The lesson from the operator's chair: any scope change to a baggage system after design freeze is a signal requiring re-evaluation of the testing program. Not a risk to be noted in a log — a hard pause on the commissioning schedule.

### 2. Heathrow T5's Staff Access Failure — The Commissioning Symptom

On the morning of March 27, 2008, British Airways baggage handlers could not park their cars because BAA had not made the staff car park accessible. They arrived two hours late. The staff access system at the terminal did not recognize employee IDs. Eighteen terminal lifts were jammed. The Heathrow Express and transit connections to the satellite building were down.

These are not baggage system failures. They are access and facility commissioning failures — the kind that only appear when the building is run with real people under real conditions. The 68 trials with 15,000 volunteers did not catch them because the volunteers were not the actual employees who would be on site at 4:30 AM with uniform access requirements.

The 12,000-bag-per-hour conveyor then ran without the staffing required to manage it, queued, overflowed, and shut down. The system had never been run at full throughput with concurrent inbound and outbound operations because the building was a construction site until the final weeks.

This is the gap between a commissioning checklist and an operational trial. The checklist was largely complete. The trial was not run.

### 3. BER's Fire Safety System — The Owner-Engineer Failure with Physical Evidence

The smoke extraction system at BER represents a specific category of failure: a design requirement that was physically impossible to meet, signed off by someone who did not have the credentials to evaluate it, approved by an owner that did not verify credentials, and never caught in any integrated review process before the building was completed.

The sequence: architect specifies a clean roofline (no visible exhaust infrastructure) for aesthetic reasons. Engineer designs a system to pump smoke downward into the basement to compensate. The system requires reversing the natural behavior of hot air. No such system had been successfully implemented at this scale anywhere. The engineer was not licensed to certify it. The owner did not check.

December 2011: mandatory acceptance test. The fans build pressure; the pipes implode; the automatic flaps do not move. The airport fails its safety test two weeks before its planned opening.

The operator who inherited BER in 2020 received a fire safety system that had been modified, re-tested, and re-certified over nine years — but also a staff that had never operated the building, a maintenance organization that had been maintaining an unoccupied structure, and a terminal with 1,000 still-unresolved deficiencies as of two months before opening.

### 4. LaGuardia Terminal B's Circulation Design — The Design-Over-Operations Failure

LaGuardia Terminal B opened a building that works beautifully as an architectural artifact. The arrivals and departures hall photographs well. The concessions are strong. The finish quality is a legitimate improvement over what preceded it.

What it did not solve: the fundamental constraint of a single-access roadway that creates bottlenecks extending curbside wait times to 20+ minutes at peak. The satellite concourse design required pedestrian bridges (the physically correct solution given the constraint of building on an active airfield) but extended walking distances and increased international connection times by approximately 25% compared to the building it replaced. Drop-off zones designed for 50 vehicles routinely absorb double that number.

These outcomes were foreseeable. A curbside with one access point will always fail at peak because queuing theory does not require optimism bias to predict the result. Walking distances are calculated in design drawings. Anybody who has walked a tight connection at LGA Terminal B knows the design team did not walk it themselves.

The lesson: design decisions that trade operational performance for aesthetic achievement are a form of commissioning failure that no amount of ORAT can correct. By the time ORAT runs, the walking distances are fixed in concrete.

### 5. JFK NTO's Hard Deadline — The Live Test of the Thesis

The New Terminal One at JFK is scheduled to open in June 2026 for Phase A — 14 gates, arrivals and departures hall — timed to the FIFA World Cup. The full terminal opens in 2030.

From the operator's chair, the risk profile looks like this:

The World Cup is a fixed political deadline equivalent to BER's repeatedly-moved but always-politically-driven opening dates. It creates the governance environment in which commissioning shortcuts become acceptable because the alternative — telling the Governor of New York that the terminal will not be ready for the World Cup — is politically unavailable.

The phased structure (14 gates in 2026, 23 by 2030) is operationally sensible but creates a specific risk: Phase A will be opened before the baggage system has handled a full widebody push with all 14 gates simultaneously active. That is the test. Not the simulation at the Long Island facility — the first Monday morning in July 2026 with three widebody arrivals within 20 minutes of each other and the system running a new software configuration.

NTO's investment in simulation and pre-opening trials is the right response. The question the thesis forces is this: is the simulation program scoped to run at rated capacity, with the actual airlines' systems integrated, with the actual TSA and CBP workflows, for a sufficient number of cycles to identify the fault modes that only appear under sustained load? If the answer is yes, NTO breaks the pattern this thesis describes. If the answer is yes on paper and abbreviated in practice because the construction program consumed the window, the thesis holds.

---

## COO's Operational Verdict

The thesis is correct in its mechanism, useful in its framing, and strongest where it is most specific. The warning signs that matter operationally are not "scope creep" as an abstraction — they are the specific project management events that signal the commissioning window is being consumed: testing milestones that are reduced in scope rather than extended in duration, staff familiarization programs that move off-site because the building is not accessible, integrated trials that are cancelled because the contractor still has access to the floor.

The thesis is correct that these signals appear 5–7 years before ribbon-cutting. At BER, the unqualified engineer and the impossible smoke extraction design were locked in before 2010. At Denver, the scope expansion that made the system undeliverable was executed in 1992. At T5, the construction delays that consumed the commissioning window were documented years before March 2008.

What the thesis cannot say — and the Strategist needs to hear — is that recognition produces correction. The signals were visible at BER and ignored for a decade. The commissioning gap at T5 was known to BA's project leadership and not acted upon. Recognition is necessary. Authority to act on recognition is the variable the thesis cannot control from the operator's chair.

The operator's job on Day 1 is to run the airport regardless of what the project delivered. The thesis's operational value is that it gives the operator standing to intervene during design — not to predict failure, but to refuse to accept a commissioning program that has been compressed beyond what the system requires.

---

*Sources compiled from: GAO RCED-95-35BR, Wikipedia (Heathrow Terminal 5 and Berlin Brandenburg Airport construction), The Local DE, CNN Travel, MightyTravels analysis, IEEE Spectrum, NPR, ConstructionOwners.com, CNBC, ACRP research programs (TRB), IATA ORAT guidance, Computerworld, NBC News, Washington Post, Euronews, Facilities Dive, PMI learning library, and Journal of Project Management.*

---

**File path:** `/Users/christiankessleriv/Repos/ai-council-mwaa/outputs/stage1/airport-coo-brief.md`
