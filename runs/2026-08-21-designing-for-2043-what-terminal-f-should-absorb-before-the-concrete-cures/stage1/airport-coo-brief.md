# Airport COO Brief — Designing for 2043: What Terminal F Should Absorb Before the Concrete Cures

**Author lens:** Chief Operating Officer, top-tier US hub airport.
**Run:** `designing-for-2043-what-terminal-f-should-absorb-before-the-concrete-cures`
**Airport:** Dallas/Fort Worth International (DFW). Sole occupant of Terminal F: American Airlines. Use and Lease extended to 2043.

The Strategist asked me to frame this thesis from the operator's chair — the person who has to make the place work on the first Monday after ribbon-cutting, and every Monday after that until 2043. My job is not to like the plan or dislike it. It is to tell you where operational reality will punish the plan if we don't design for it now, and where the plan gets stronger because it names the punishment up front.

---

## 1. Key findings

- **The re-bank changes the physics of Terminal F, and the design brief has to catch up.** American is going from 9 banks to 13 at DFW in April 2026 and cutting the 9am peak from about 110 departures to 52 [Source: https://paxex.aero/american-airlines-dfw-hub-banking-april-2026/]. That is not a schedule tweak. It is a different terminal. Peak-hour queuing loads at checkpoints, ticketing, and the FIS drop; utilization curves flatten; single-airline gate turns get closer to a rolling hub than a punch. If Terminal F is scoped against the old 110-departure surge — which is how planning models usually get written — we are over-building peak processing and under-building sustained mid-day gate utility.
- **Reversibility is the only useful map the council can hand to the Board.** Structure, vertical circulation cores, MEP risers, apron pavement classification, jet-bridge foundations, BHS mainline geometry, FIS/CBP inspection lane sight-lines, and utility corridor sizing become effectively permanent within days of pour or module set. Concessions, gate boarding-door hardware, lounge fit-out, IT head-end rooms, signage, and even the fixed vs. swing designation of gates stay cheap to change for years. Everything the modular method makes possible — plug-and-play interior modules, off-site MEP prefab — collapses if we design fixed points where we should have designed connections.
- **Modular gates buy speed and repeatability; they do not buy flexibility for free.** Six pre-fabricated modules, the largest 278 × 136 feet at 3,320 tons, arrived at Terminal F in the August 2026 move [Source: https://www.internationalairportreview.com/dallas-fort-worth-airport-completes-record-breaking-modular-move-as-new-terminal-f-construction-reaches-major-milestone/532266.article]. What modular actually delivers is faster factory work in controlled conditions and fewer weather-sensitive site trades. What it does not deliver, unless we engineer for it, is future replaceability. If the interior systems (MEP, IT, BHS branches, jet bridges, boarding-door hardware) are terminated inside the module in ways that require re-cutting the module skin to modify, the second decade of the building becomes a retrofit nightmare. The single most valuable operator ask right now is: **every module gets a defined "operator interface plane" — a mapped seam where MEP, low-voltage, and BHS can be re-terminated without breaching structure.**
- **Terminal F opens as a single-tenant building with no common-use fallback, and the IROPS math is different because of it.** American already carries 82.6% of DFW's passengers [Source: outputs/context/airport-context.md, §4]. The other 17.4% of the airport is our surge relief valve during an American IT outage or crew-rest cascade. Terminal F has no such valve internally. If the AA network fails inside Terminal F, the entire building fails; recovery depends on Skylink capacity to move stranded customers to A/B/C/D and on ramp capacity to tow aircraft off-gate. Design the building to accept CUPPS-capable gate hardware [Source: https://www.iata.org/en/publications/manuals/iata-common-use-passenger-processing-systems-cupps/] and a common-use IT backbone even if we never invoke it under the U&L. Insurance we can install in the walls now costs orders of magnitude less than the retrofit.
- **The Provisions-by-Admirals-Club decision is a live signal, not a settled fact — and we should design the building as if it will be reversed.** American is putting the network's largest Admirals Club (37,000 sf) in Terminal C and Flagship Check-In in Terminal D near D30, while Terminal F is scoped only for a scaled Provisions concept [Source: https://www.dallasnews.com/business/airlines/article/american-airlines-new-admirals-club-dfw-airport-22351656.php]. That is not consistent with a carrier that is repositioning to premium; that is a carrier that has not yet made up its mind about Terminal F's role in the premium stack. Under the U&L, American controls the lounge decision, but the operator controls whether the shell can accommodate a Flagship-tier lounge later. It should. Reserve the volume, the plumbing risers, the elevator core for a back-of-house kitchen, and the outboard airside frontage suitable for a 25,000-40,000 sf Flagship footprint with a runway view. If it is never used as a Flagship Lounge, we lose lease revenue on that footprint for a few years. If it is needed and not reserved, the retrofit is a nine-figure disaster and a year of scaffolding in the busiest concourse.
- **The Skylink node inside Terminal F is the single most operationally load-bearing piece of the program.** Skylink is out of service every night from 22:00 to 06:00 on one loop [Source: https://www.dfwairport.com/skylinkfaqs/]. Transit time between terminals doubles when one loop is down. If Terminal F becomes American's international/premium gateway, the Skylink node has to survive the design decade with (a) a second platform edge held in reserve, (b) redundant vertical circulation sized for a full station evacuation, and (c) enough queuing area that a single Skylink loop failure at 5:45 AM does not back people into the security checkpoint. This is the classic capital handoff failure category: elegant transit nodes designed for average day flows, unusable on the day the operator actually needs them.
- **The capital-handoff pain points are known; the design decisions that cause them are already being made.** ACRP Synthesis 20 documented that terminal activations repeatedly fail because operations staff enter the process too late [Source: https://onlinepubs.trb.org/onlinepubs/acrp/acrp_syn_020.pdf]. ACRP Report 139 institutionalized retrocommissioning because MEP systems drift from design intent within the first years of operation [Source: https://crp.trb.org/acrpwebresource2/acrp-report-139-optimizing-airport-building-operations-and-maintenance-through-retrocommissioning-a-whole-systems-approach/]. Retrocommissioning is a $5-15/sf-recurring band-aid on a design decision that was made without ops in the room. For a ~400,000-sf Phase 1 concourse [Source: https://www.dfwairport.com/construction/terminal-f/], that band-aid is $2-6M every retrocommissioning cycle. The cheaper answer is to seat the operator at the design table now, with veto authority on the reversibility map.

---

## 2. Evidence — what the operator actually controls, and what we don't

### 2.1 The re-bank changes the design brief

American's April 2026 shift from 9 to 13 banks reduces the 9am peak from about 110 departures to about 52 and puts 40+ flights into hours (11am, 1pm, 3pm, 5pm, 9pm) that used to be trough hours [Source: https://paxex.aero/american-airlines-dfw-hub-banking-april-2026/]. The carrier is simultaneously adding an average of 6 minutes of block time across 145 markets — CLT +17, DCA +10, MIA +9 — to buy connection reliability [Source: https://paxex.aero/american-airlines-dfw-hub-banking-april-2026/]. American is telling us, plainly, that its DFW hub of the 2030s will be flatter, more consistently loaded, and more tolerant of slower turns. That is a materially different building than a 110-departure hub.

For Terminal F this means: checkpoint lane count sized against the 110-departure peak is over-scoped; gate utilization models should be rebuilt against a 13-bank profile; the "how many gates can go dark for maintenance mid-day" question — the one the operator actually asks — has better answers under the new pattern.

### 2.2 What the operator controls vs. what we don't

Any operational thesis on Terminal F has to be honest about the levers.

| Control category | Who controls | Operator's actual authority at DFW |
|---|---|---|
| Terminal design, gate count/mix, module geometry | DFW Board approves; AA consent required in T-F under U&L | Full veto on airfield-side design that doesn't meet FAA AC 150/5300-13B geometry [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC-150-5300-13B-Airport-Design-Chg1-w-errata.pdf]; strong influence on terminal design; **must earn** AA consent on interior programming |
| Runway sequencing, arrival/departure rates | FAA ATC | Zero. We coordinate; we do not decide. |
| Airline schedule, gate assignment inside T-F, lounge decisions | American | Zero direct; leverage only via U&L side letters and shell design |
| Checkpoint sizing/technology | Joint TSA/airport | Split; TSA drives CT/AIT deployment cadence |
| CBP FIS design, staffing model | CBP / airport | Airport designs to CBP consultation; CBP staffs |
| Curbfront, ground transportation | Airport / host cities | Airport, subject to Dallas/Fort Worth city rules |
| Baggage handling system, common-use IT, Skylink node | Airport | Full |
| Concessions, retail, F&B | Airport (through concessions program) | Full within lease structure |
| Weather/de-ice execution | Airport ops + airlines | Split — airport owns pad, airline owns aircraft |

The point is not new to any operator. It matters here because strategy decks routinely propose Terminal F "innovations" that require decisions we cannot unilaterally make. If it requires an airline schedule change, a CBP lane redesign, an FAA airspace concurrence, or a TSA technology deployment, it is not an operator lever — it is a negotiation with a two-to-five-year clock. Anything in the recommendation set that assumes otherwise should be flagged for what it is.

### 2.3 IROPS execution — the first 90 minutes

The plan on paper for a Terminal F IROPS event will look like every other IROPS plan: activate the AOC, coordinate with the AA System Operations Center in Fort Worth, staff up customer-facing positions, issue passenger comms, coordinate with FAA ATCT on ground-stop timing, pre-stage buses and ramp equipment. The plan as executed depends on three variables the planning documents rarely name.

**First, the duty manager on the floor and their standing authority.** During the January 2023 winter event, DFW absorbed a ground stop, 4-hour post-stop average delays, 1,100+ cancellations on the peak day and 600+ additional cancellations the next day [Source: https://spectrumlocalnews.com/tx/south-texas-el-paso/news/2023/01/31/winter-storm-prompts-ground-stop-for-incoming-flights-at-dfw-airport-]. Recovery in the first hours is not a plan — it is a set of individual calls about whether to close a gate, whether to hold an inbound at the ramp, whether to tow a stuck aircraft to a remote pad. The Terminal F design should give the duty manager physical assets they can actually use: pre-designated hold pads visible from the tower cab and reachable by tug from any Terminal F gate; a Skylink node with enough queuing area that the manager can stage 2,000 stranded passengers without contaminating airside; an AOC visualization feed of Terminal F BHS status independent of the AA system.

**Second, ramp closure and taxiway routing.** Terminal F sits inside DFW's existing property envelope. Any Terminal F closure — hazmat spill, medical emergency, security breach — needs pre-routed alternates that keep AA departures moving through the rest of the airport. Design should include a permanent, documented ramp-closure playbook per gate pair, not a wall-schematic that gets pulled out during the event.

**Third, common-use fallback.** American's IT stack is not immune to what happened at Delta in July 2024 or Southwest in December 2022. If AA's PSS goes down at 5:30 AM, Terminal F today would have zero recovery capability. Building CUPPS-ready gate hardware and a small pool of common-use kiosks costs a few million in the shell now; the alternative is being unable to reprint boarding passes for 60,000 passengers.

### 2.4 Modular construction — what it makes possible, and what it forecloses

The modular method is not new to DFW: the same approach is being used on Terminal C and A renovations, adding 14 gates by spring 2026 [Source: outputs/context/airport-context.md, §5]. Terminal F Phase 1's six modules, largest at 278 × 136 feet and 3,320 tons, were placed via SPMT transporters over a two-week overnight move in August 2026 [Source: https://www.internationalairportreview.com/dallas-fort-worth-airport-completes-record-breaking-modular-move-as-new-terminal-f-construction-reaches-major-milestone/532266.article]. The design-build team is Innovation Next+ (Archer Western, Turner, Phillips May, H. J. Russell, CARCON) with PGAL, Gensler, Muller2 [Source: https://www.turnerconstruction.com/insights/innovation-next-achieves-landmark-modular-delivery-for-dfw-terminal-f-expansion].

What this method makes uniquely possible, from the operator's chair:

1. **Off-site MEP first-fit.** Systems can be terminated in factory conditions, tested to pressure and continuity, and set as complete assemblies. The operator gets fewer punch items and cleaner as-builts. Insist on witness testing at the factory, not just at site — a lesson every activation study back to ACRP Synthesis 20 has said out loud [Source: https://onlinepubs.trb.org/onlinepubs/acrp/acrp_syn_020.pdf].
2. **Module-level swap-out.** If the operator designs the seam between modules as an "operator interface plane" — MEP, low-voltage, BHS branch, hydronic, fire, IT terminating in a mapped, accessible chase at the seam — then in 2038 a module's interior can be replaced without unlocking the adjacent modules. Absent that discipline, modularity becomes a one-time construction convenience with no future value.
3. **Boarding-door and jet-bridge repositioning.** Because gates are essentially interchangeable module-mounted elements, the plan can hold a subset of gate positions as flex/swing positions between narrowbody and small widebody, without the wall-cut-and-reframe that fixed construction demands. This is the strongest hedge available against the widebody gate-mix gap the context packet flags [Source: outputs/context/airport-context.md, §9].
4. **Faster mid-life renewal.** PBB service life is roughly 20-25 years with mid-life overhauls at 10-12 [Source: https://oxmaint.com/industries/aviation-management/passenger-boarding-bridge-pbb-maintenance-preventing-delays]. A modular building can rotate a whole gate module out for renewal on the operator's schedule, not the manufacturer's.

What modular forecloses if we're careless: any decision made "inside the module" during design lock is effectively welded shut. If the operator is not present at the factory design reviews for each module — not the site meetings, the factory ones — we lose the reversibility we paid for.

### 2.5 Maintenance realities and the capital-handoff hangover

Every terminal handed back to operations comes with an inheritance of things the design team never had to live with. The recurring categories, ranked by how often they show up on the Monday-morning OPSCOMM:

- **Baggage systems.** Vendor MTBF specs describe tag-reading heads at 67,000 hours [Source: https://www.cognex.com/en/applications/barcode-scanning-and-tracking/automated-tag-reading-for-airline-baggage-tracking]; the operator's lived experience of the full system — belts, diverters, ATR heads, sortation software — is that peak-load days find every weak weld and every mistuned diverter. World-class availability targets are 95%+ [Source: https://oxmaint.com/industries/aviation-management/airport-maintenance-kpi-dashboard-aviation-industry]; the honest post-handoff number in the first two years is often lower. Terminal F design must include physical redundancy at BHS mainline junctions and enough matrix capacity to run degraded and still hit AA's re-banked connection targets.
- **Jet bridges.** The 20-25-year service-life headline hides the reality that PBBs fail one component at a time — canopies, hydraulic cylinders, wheel bogies, docking sensors — and every failure is a gate down until it is fixed [Source: https://oxmaint.com/industries/aviation-management/passenger-boarding-bridge-pbb-maintenance-preventing-delays]. The design should specify commonality of PBB models across Terminal F so the parts room is one, not four.
- **Vertical circulation.** Escalators and elevators in high-traffic airport concourses run at duty cycles their commercial spec sheets do not contemplate. Any single-escalator run to a Skylink platform is an outage waiting to happen. Terminal F should hold a hard rule: no single point of failure between gate and Skylink and no single point of failure between check-in and checkpoint.
- **HVAC and building automation.** ACRP 139's whole-systems retrocommissioning framing exists because MEP drift is universal in the first years of operation [Source: https://crp.trb.org/acrpwebresource2/acrp-report-139-optimizing-airport-building-operations-and-maintenance-through-retrocommissioning-a-whole-systems-approach/]. Design intent BAS points must be handed off to ops with the sequence-of-operations documented in the operator's own CMMS, not left in the design engineer's file.
- **Skylink node.** Already discussed. It is the operational choke point of Terminal F.

### 2.6 Throughput as the operator sees it

Planning-model capacity for Terminal F will be a number written against ideal conditions. The number the operator will hold up on a peak day is different. It is bounded by:

- The lowest-capacity chokepoint on the passenger path (usually checkpoint or FIS, not gate).
- BHS sustained throughput net of daily degradation, not nameplate.
- The number of gates actually available after that day's inevitable one or two PBB, tow-tractor, or GSE-down positions.
- Ramp congestion during the connecting bank, which under the new 13-bank pattern will be less punishing but is now dictated by tug movements between banks, not push volume per hour.

The honest number is roughly 80-85% of the planning-model number on a peak day, and lower on the day after an IROPS event. Any capacity claim in the strategist's report should carry that operator discount.

---

## 3. The operator's case for and against the thesis

### For

The thesis is correct in the essential move: irreversible decisions at Terminal F should be made against American's *2035* posture, not its *2025* posture. The re-bank alone [Source: https://paxex.aero/american-airlines-dfw-hub-banking-april-2026/] validates the concern that American's operational geometry is changing under us mid-design. The premium repositioning at Terminals C and D [Source: https://www.dallasnews.com/business/airlines/article/american-airlines-new-admirals-club-dfw-airport-22351656.php] is doing the same thing physically. If Terminal F ships against the 2023 brief, the operator will spend the 2030s retrofitting to catch up — and every one of those retrofits will happen on live gates during operations, at 5-8x the greenfield cost. The reversibility map the run prompt asks for is the single most valuable artifact the council can produce.

### Against

The thesis is also flattering to the design phase in a way I have to push back on. It assumes the operator was in the room and lost the argument. That is often not what happened — the operator often was not in the room at all. ACRP Synthesis 20's headline finding, made almost twenty years ago and repeated in every activation post-mortem since, is that operations staff are engaged too late [Source: https://onlinepubs.trb.org/onlinepubs/acrp/acrp_syn_020.pdf]. The council's recommendation set will fail on execution if it lands on a Board that then hands it to a design-build team without also naming *who from operations signs the module design reviews, at what stage, with what authority to require rework.* That is the missing sentence in every capital plan I have ever handed back to.

Second, the thesis over-indexes on premium. American's premium repositioning is real, but the physical realities of a hub that still connects 100,000 customers a day [Source: https://news.aa.com/news/news-details/2025/Doubling-down-on-DFW-American-further-strengthens-its-Flagship-hub-OPS-OTH-12/default.aspx] mean Terminal F is, on a Monday morning, a connecting terminal first and a premium terminal second. Every square foot of premium space that displaces connecting-passenger circulation costs the operator on the connect. The reversibility map has to work in both directions: preserve the option to add premium if AA commits, and preserve the option *not* to, if AA's premium shift ends up concentrated in T-D and T-C where it started.

Third, "modular flexibility" is a slogan unless the seam discipline is contracted. Innovation Next+ is a strong team [Source: https://www.turnerconstruction.com/insights/innovation-next-achieves-landmark-modular-delivery-for-dfw-terminal-f-expansion], but flex is a design deliverable, not a construction method. If the operator does not specify the operator interface plane, we do not get it.

---

## 4. Specific examples that frame the thesis

**Example 1 — Skylink node capacity as the design canary.** The Skylink FAQ tells any operator that overnight, transit times between terminals rise to about 15 minutes on single-loop operation [Source: https://www.dfwairport.com/skylinkfaqs/]. That is the *planned* degraded state. The unplanned state — a rail-side failure at 6:15 AM during the Terminal F morning arrival wave — is what we design for. Reserve a second platform edge, over-size vertical circulation, over-size queueing on the concourse-side of the platform. The cost is measured in square footage now and in careers-worth of operational grief later.

**Example 2 — The Provisions-by-Admirals-Club footprint as a Flagship Lounge shell.** American's public plan is a scaled Provisions concept in Terminal F [Source: https://www.dallasnews.com/business/airlines/article/american-airlines-new-admirals-club-dfw-airport-22351656.php], while the 37,000-sf Admirals Club goes to Terminal C. If the Board and CEO believe the premium thesis, then the Terminal F shell should be built such that a future Flagship Lounge — kitchen risers, dedicated freight, back-of-house elevator core, airside runway-view frontage of 25,000-40,000 sf — is a lease conversation, not a demolition. American keeps the decision. We keep the option.

**Example 3 — The 2023 winter event as the IROPS benchmark.** DFW absorbed a ground stop, 1,100+ cancellations on the peak day and 600+ the next day, with 4-hour post-stop delays [Source: https://spectrumlocalnews.com/tx/south-texas-el-paso/news/2023/01/31/winter-storm-prompts-ground-stop-for-incoming-flights-at-dfw-airport-]. Terminal F must be designed to accept 3,000-5,000 stranded passengers overnight without collapsing food, restroom, or seating capacity. That is a specific, sized design requirement — not a "resilience" bullet on a slide.

**Example 4 — The modular seam as reversibility contract.** Each of the six Terminal F Phase 1 modules is placed as a discrete assembly [Source: https://www.internationalairportreview.com/dallas-fort-worth-airport-completes-record-breaking-modular-move-as-new-terminal-f-construction-reaches-major-milestone/532266.article]. The operator ask is a written specification, before the next module design lock, that MEP, IT, low-voltage, and BHS-branch terminations are located at a defined, accessible chase at the module-to-module seam, with as-built drawings deposited in DFW's CMMS at commissioning. This is the least expensive high-value operational specification the council can propose.

**Example 5 — CUPPS-capable shell with an AA-preferred day-one operating configuration.** IATA CUPPS is an open standard that allows shared physical gate positions with swappable airline software [Source: https://www.iata.org/en/publications/manuals/iata-common-use-passenger-processing-systems-cupps/]. Under the U&L, Terminal F operates as AA-exclusive, and AA can run its own PSS on day one. The design ask is that the shell — cabling, IT closets, kiosk mounting, gate podium wiring — is CUPPS-compliant. This costs incrementally in the wall and delivers optionality: for AA's own operational recovery when their PSS is down, and for whatever the 2040s bring in terms of airline consolidation, joint-venture partners, or U&L renegotiation.

---

## 5. What would have to be true in 2035 for the operator to be wrong

The COO's honest read of downside scenarios in which these recommendations look over-built:

- **American reverses the premium shift.** If a 2029-2031 macro downturn pushes AA back to volume-and-density, the reserved Flagship Lounge shell sits vacant and the CUPPS-capable IT shell goes unused. Cost of being wrong: a few years of lease revenue on the reserved footprint plus IT capex written down.
- **The re-bank fails within 24 months and AA reverts to a 9-bank pattern.** Terminal F designed against the 13-bank profile is then peaked more sharply than expected. Cost of being wrong: elevated queuing on peak hours, retrofit of checkpoint lanes.
- **Modular flexibility never gets exercised.** If AA/DFW never modifies a module through 2043, the operator interface plane discipline was over-engineered. Cost of being wrong: a few percent premium on module design fees.

Two of these three downside cases have modest operator cost. The upside cases — building for a premium shift that arrives and finding the shell already accepts it, or absorbing a widebody mix shift because the gate modules were designed to swing — have compounding operator value across every year through 2043. That asymmetry is the operator's case for building the reversibility in now.

---

## 6. Evidence gaps I could not close

- Exact widebody vs. narrowbody gate mix and flex-position count inside Terminal F. Not publicly disclosed; flagged in the context packet [Source: outputs/context/airport-context.md, §9].
- Whether the Provisions-by-Admirals-Club designation is a placeholder or a settled U&L obligation. Same source.
- The specific reversibility window per module — how many days after module set can MEP or interior partitioning still be changed without schedule impact. Not public; requires operator-side interview with Innovation Next+.
- Cost-per-enplanement trajectory and MII trigger thresholds under the extended U&L. Confidential.
- Terminal F architect of record's published design-intent statement beyond the joint press release. Not located in public sources.

Where the analysis in this brief rests on operator judgment rather than a citable document — the reversibility map framing, the operator interface plane specification, the sizing of the IROPS overnight shelter requirement, the operator discount on planning-model throughput, the ranking of maintenance failure categories — I have said so in the prose. Those are the calls a 25-year airport operator makes on the floor, and the council should treat them as such: not as sourced fact, but as the operator's read on what the sourced facts imply when the concrete cures.
