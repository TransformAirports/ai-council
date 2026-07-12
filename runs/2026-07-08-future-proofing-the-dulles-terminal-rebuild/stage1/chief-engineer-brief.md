# Chief Engineer's Brief: The Constructability Reality of the Dulles Rebuild

**Run:** Future-Proofing the Dulles Terminal Rebuild
**Lens:** Program delivery, constructability, lifecycle cost, design standards, asset condition, megaproject failure modes
**Stance:** Every project is harder, longer, and more expensive than the pre-construction estimate assumed, and the reasons are structural, not personal. Neither new concrete nor new software is as easy as its advocates claim.

---

## 1. Key Findings

1. **The durable/volatile split is a construction-sequencing fact, not a design metaphor.** The things with a 50-year life — substructure, column grid, floor-to-floor heights, apron geometry, the vertical-circulation and utility spines — are precisely the things you cannot touch again without shutting down the building. The things with a 5–15-year life — screening equipment, IT, sensing, fit-out, curtain wall systems — you will replace three to five times over the building's life *while it operates*. Future-proofing is almost entirely a decision about how much soft space, structural reserve, and conduit/power/comms capacity you overbuild in the durable layer to make the cheap-to-change layers actually cheap to change. Get the durable layer wrong and no amount of software fixes it.

2. **"Design for flexibility" collides with "screening is a regulated, evolving, level-of-service-driven function."** A distributed or gate-level screening future needs *more* structural provisioning today, not less — clear floor area, power, data, and vertical load capacity distributed to the concourses rather than concentrated at a central hall. That is the expensive kind of flexibility to leave soft. The centralized checkpoint exists for regulatory and staffing-efficiency reasons (TSA staffs lanes, not gates), and CT screening is currently *re-centralizing* throughput gains, not decentralizing them [Source: https://www.tsa.gov/sites/default/files/checkpoint-requirements-and-planning-guide-read-me-first-crpg-may-2025.pdf]. Betting the built form on distributed screening is a bet against the current regulatory grain.

3. **Phasing around a live airport is the single largest cost and schedule multiplier, and Dulles's own schedule already shows the strain.** The $22B program compresses a two-decade master plan into roughly eight years (2026–2034), with the new concourse/Concourse A work (~$6.2B) and the AeroTrain extension (~$3.75B) running concurrently from 2027–2028 [Source: https://northernvirginiamag.com/news/2026/05/12/a-22m-plan-could-transform-dulles-airport-by-2034/]. Concurrency at one airport is not additive; it is multiplicative. Every interface between two simultaneous programs — apron, utilities, baggage, tunneling under a live airfield — is a claim waiting to happen.

4. **The lifecycle tail dwarfs the ribbon-cutting.** The $22B headline is capital plus financing. It is not the 30-year cost of ownership. Baggage systems, apron and airfield lighting, HVAC, elevators/escalators, moving walkways, and the AeroTrain rolling stock all reach end-of-useful-life on staggered 5–25-year cycles and must be renewed *inside the operating building*. Deferring that renewal to protect the capital story is how you build a deferred-maintenance tail. FAA's own guidance is blunt on the economics: $1 of preventive maintenance at the right time saves $4–$10 later [Source: https://www.gao.gov/assets/gao-20-298.pdf].

5. **"First-of-a-kind" is a risk flag, not a selling point, in construction.** The failure taxonomy is consistent: the design decision that dates or fails fastest is almost always the one with the least precedent and the tightest coupling to a single technology or a single vendor's system. BER's fire-suppression/smoke-extraction system, Denver's automated systems and the Great Hall's owner-driven changes, and T5's baggage software filter were all first-of-a-kind or bespoke couplings that took the whole opening down with them.

6. **The 24–36 month intuition for any major component is optimistic by a factor that has a name: interface risk.** "Just add a gate" is a multi-year program because a gate touches pavement, utilities, baggage, fueling, apron sequencing, and the airline use-and-lease agreement. At Dulles specifically, the AeroTrain extension and mobile-lounge elimination mean the *access system itself* is being rebuilt while it carries passengers — the interdependency is total, not marginal [Source: https://www.ffxnow.com/2026/05/12/report-new-plan-to-overhaul-dulles-airport-would-eliminate-mobile-lounges/].

7. **Governance, not technology, separates the winners from the disasters.** Heathrow T5 delivered on time and on its £4.3B budget because the client held the risk and built one integrated team; it still had a catastrophic baggage meltdown on opening day because operational readiness was under-tested. BER tripled its budget and opened nine years late because of leadership churn, unqualified sign-off, and undocumented as-builts. Same decade, same building type, opposite outcomes — the variable was governance.

---

## 2. Evidence

### Constructability and phasing

Dulles is not a greenfield. The published program sequences a new concourse plus Concourse A renovation (~$6.2B, construction ~April 2027), demolition of Concourse C/D and a new 33-gate Concourse B for United regional flying (~$2.26B, ~January 2028), and a $3.75B AeroTrain extension (construction ~January 2028, targeted completion December 2033) — all inside a live United hub [Source: https://northernvirginiamag.com/news/2026/05/12/a-22m-plan-could-transform-dulles-airport-by-2034/]. Three of these run concurrently. Demolishing C/D while building B while extending the train while renovating A means shared laydown, shared haul routes, shared apron closures, and shared utility tie-ins — the classic conditions under which one contractor's delay becomes another's acceleration claim.

The comparable is LaGuardia Terminal B, described by its own delivery team as potentially "the most complex aviation project anywhere ever" precisely because the old terminal "remained fully operational during construction." The solution was an "island-and-bridges" concept — building the new headhouse and concourse on new footprint, then bridging over active taxiways — that let them build with "minimal disruptions" but at a $5.1B price on a single terminal [Source: https://www.theb1m.com/video/laguardia-airport-rebuild-terminal-b] [Source: https://stvinc.com/project/terminal-b-redevelopment-at-laguardia-airport/]. The lesson for Dulles: the only proven way to phase around live ops is to build on new footprint first and demolish last, which needs land, apron, and taxiway you must protect from the start. Dulles's plan to demolish C/D and replace it with B on or near the same real estate is the harder version of the LGA problem.

### Design standards and regulatory compliance (state carefully)

Several regimes drive cost in ways financial models understate. I can confirm the following apply and are non-optional; where I am uncertain about a specific numeric threshold I say so:

- **FAA airfield design (AC 150-series).** Airport pavement design and management are governed by AC 150/5320-6 (design) and AC 150/5380-7 (pavement management), with condition tracked via the Pavement Condition Index per ASTM D5340 [Source: https://www.faa.gov/documentlibrary/media/advisory_circular/150-5380-7b.pdf]. FAA structural pavement design uses a 20-year design life as the standard planning horizon; I am confident of the 20-year figure for pavement structural design, less certain of the exact current sub-revision letter, so treat "AC 150/5320-6" as the family, not a pinned edition.
- **TSA checkpoint design** is governed by the Checkpoint Requirements and Planning Guide (CRPG, May 2025) and the industry Checkpoint Design Guide, updated through PARAS 0004 — Recommended Security Guidelines for Airport Planning, Design and Construction [Source: https://www.tsa.gov/sites/default/files/checkpoint-requirements-and-planning-guide-read-me-first-crpg-may-2025.pdf] [Source: https://airportscouncil.org/wp-content/uploads/2018/09/Checkpoint_Design_Guide_CDG_Rev_4_0.pdf]. These are modular lane standards. CT screening changes the *depth and power* a lane needs — designing for today's lane geometry alone is how you strand the checkpoint.
- **FAA Part 139** (airport certification), **ARFF** (aircraft rescue and firefighting) index/response requirements, **ADA** accessibility, and **CBP Federal Inspection Services** design standards for the international arrivals hall all apply to a Dulles rebuild. FIS design in particular is CBP-driven and can force sterile-corridor geometry, queuing depth, and one-way circulation that constrains the very "de-sequenced" processing the thesis contemplates. I have not verified the current CBP Airport Technical Design Standard revision here; the design team must pull the live version because it changes.

The point for the Council: a "distributed, off-airport, on-the-device" processing vision must survive contact with CBP sterile-corridor rules, TSA lane certification, and Part 139 airfield separation. Some of that vision is a regulatory bet, not a design choice.

### Lifecycle cost vs. capital cost

The $22B is funded by roughly $21.8B in new bonds plus $1.1B in fees, and those figures *include inflation and future interest* — a financing number, not a cost-of-ownership number [Source: https://northernvirginiamag.com/news/2026/05/12/a-22m-plan-could-transform-dulles-airport-by-2034/]. What the bond number does not carry is the 30-year renewal profile: baggage handling systems and controls, HVAC and chillers, vertical transportation (elevators, escalators, moving walkways), apron and airfield lighting, and AeroTrain vehicles and track systems each hit end-of-life on their own clocks, most inside the 25-year window, and must be replaced under traffic.

GAO has documented both the funding gap and the mechanism by which it compounds: planned airport projects were estimated near $22B annually (FY2019–2023) against roughly $14B annually received (FY2013–2017 average), and "some airport officials have deferred needed infrastructure investments or completed projects in phases, steps that increased construction times and costs" [Source: https://www.gao.gov/assets/gao-20-298.pdf]. Deferral is not free — it "reduce[s] asset life and increase[s] asset life-cycle costs," and the preventive-maintenance return is $4–$10 per $1 spent on time [Source: https://www.gao.gov/assets/gao-20-298.pdf]. A sponsor that capitalizes glamorous new construction and underfunds O&M is manufacturing its own next crisis.

### Asset condition and the durable/volatile framework

The engineering framework the Council should adopt separates capital by *driver*, not by glamour:

- **Condition-driven capital** replaces what is worn out (a 20-year-PCI runway, a 25-year-old baggage system). It is predictable, plannable, and unglamorous.
- **Capacity-driven capital** adds throughput (gates, checkpoint lanes). It is what boards fund.
- **Adaptability-driven capital** — the future-proofing spend — is structural and utility reserve you buy now because retrofit later is unaffordable while the building operates.

The 50-year layer at Dulles: foundations, column grid (aim for the wide clear spans that make future re-partitioning possible — 30–50 m span families are how modern terminals buy column-free floor plates), floor-to-floor heights generous enough to re-route MEP and add sensing, apron and taxiway geometry, and the vertical-circulation and utility spines. The academic flexibility literature is explicit that terminals must be planned for a "20 to 50-year lifespan" with operational, tactical, and strategic flexibility designed in from the start [Source: https://www.academia.edu/36045894/Flexible_Airport_Terminal_Design_Towards_a_Framework_Sarah_Shuchi]. The 5–15-year layer: everything downstream of the conduit stub-out. **Overbuild the durable layer's electrical, structural, and spatial reserve; leave the volatile layer genuinely soft.**

### Sustainability as a hard structural constraint

Electrified GSE is not an operations line item — it is a substation-and-conduit decision that must be made in the durable layer. Modeling of US airport GSE electrification shows material new power and infrastructure demand [Source: https://www.nature.com/articles/s41467-026-71125-4], and real deployments are large: Sea-Tac installed 576 electric charging locations across all concourses [Source: https://xantrex.com/about-xantrex/blog/work-truck/evaluating-gse-electrification-strategies-choosing-the-right-approach-for-airports/]. The engineering reality: apron-edge power, transformer vault space, and conduit runs are cheap to provision in new slab and structure and brutally expensive to retrofit into a finished, operating apron. If Dulles wants a terminal still operating in 2050, the electrical backbone and thermal-load headroom are the cheapest thing to overbuild now and among the most expensive to add later. Fully electrified three-shift GSE also implies charging windows that today's Level 2 chargers (≈8 hours) cannot serve — plan for fast-charge power density, not just outlets.

### Megaproject failure modes, observed patterns

- **Denver Great Hall.** The $1.8B P3 was terminated after ~14 months. The fired contractor pegged delays at 3+ years and overruns at $300M+, citing "the multitude of Owner Changes being issued on the project" and weak 1990s-era concrete discovered under the existing terminal; the settlement ran ~$183.6M and the airport moved to finish with a new contractor for ~$2.1B, opening around 2028 [Source: https://www.constructiondive.com/news/great-hall-claims-dias-lack-of-engagement-contributed-to-airport-renovatio/567441/] [Source: https://www.westword.com/news/denver-airport-terminating-18-billion-great-hall-renovation-contract-11446629/]. **Failure mode: owner-driven change-order cascade plus unknown existing conditions.** Directly relevant to demolishing/renovating Concourse A and C/D, where 1960s–1980s as-builts will not match reality.
- **Berlin Brandenburg.** Opened October 2020, nine years late; cost rose from an initial ~€2.5–2.8B to ~€6.5B+. The controlling failure was the fire-protection/smoke-extraction system, "not built according to the construction permit," signed off by a designer who was a draughtsman, not a qualified engineer; compounded by undocumented cabling, mis-dimensioned escalators, and leadership churn through four directors [Source: https://en.wikipedia.org/wiki/Construction_of_Berlin_Brandenburg_Airport]. **Failure mode: bespoke life-safety system + governance vacuum + missing as-builts.**
- **Heathrow T5.** The counter-example on delivery: on time, on £4.3B budget, because "BAA... held all the risk," pooled contingency (~£100M) centrally, and co-located one integrated team under the relational "T5 Agreement" [Source: https://infrastructuredeliverymodels.gihub.org/case-studies/heathrow-terminal-5/]. And yet opening day lost 23,000+ bags and cancelled 500+ flights because a software filter from testing was never removed and staff/operational readiness was under-rehearsed [Source: https://cdn2.f-cdn.com/files/download/1815034/eLHMsHeathrow%20Fiasco.pdf]. **Lesson: delivery excellence and operational-readiness failure are independent risks. You can win the construction and still lose the opening.** Heathrow's repeated 2026 baggage meltdowns show the system layer keeps failing long after the concrete is signed off [Source: https://www.paddleyourownkanoo.com/2025/07/11/heathrow-airport-suffers-embarrassing-baggage-system-breakdown-on-same-day-it-announces-10-billion-investment-plan/].

### Interdependencies

You cannot evaluate the concourse, the AeroTrain, and the baggage system in isolation. Eliminating the mobile lounges *requires* the AeroTrain extension to be complete before you can retire the lounge fleet, which means the passenger-access system has zero slack — if the tunnel/train slips, the whole gate program's usability slips with it [Source: https://www.ffxnow.com/2026/05/12/report-new-plan-to-overhaul-dulles-airport-would-eliminate-mobile-lounges/]. Layer on utilities, fueling, apron sequencing, and the United use-and-lease agreement (33 regional gates in the new Concourse B is an airline-specific commitment), and you have a program where the critical path runs through the seams between contracts, not through any single trade.

---

## 3. Cost and Schedule Examples (real programs)

| Program | Headline | What actually happened |
|---|---|---|
| **Dulles rebuild** | $22B, 2026–2034 | Compresses a ~20-year master plan into ~8 years; three major packages run concurrently [Source: https://northernvirginiamag.com/news/2026/05/12/a-22m-plan-could-transform-dulles-airport-by-2034/] |
| **LGA Terminal B** | ~$5.1B, one terminal | "Most complex aviation project anywhere ever" — full ops maintained via island-and-bridges [Source: https://www.theb1m.com/video/laguardia-airport-rebuild-terminal-b] |
| **Denver Great Hall** | $650M budget | P3 terminated at ~14 months; +3 yrs, +$300M claimed; ~$183.6M settlement; refinanced to ~$2.1B [Source: https://www.constructiondive.com/news/denver-airport-officials-fire-great-hall-partners/560886/] |
| **Berlin BER** | ~€2.5–2.8B est. | Opened 9 yrs late at ~€6.5B+; fire system failed permit [Source: https://en.wikipedia.org/wiki/Construction_of_Berlin_Brandenburg_Airport] |
| **Heathrow T5** | £4.3B | On time, on budget — then lost 23,000+ bags on opening day [Source: https://cdn2.f-cdn.com/files/download/1815034/eLHMsHeathrow%20Fiasco.pdf] |

The pattern: the airports that controlled *cost and schedule* (T5, LGA-B) did it through risk-holding governance and build-new-then-demolish phasing. The airports that blew up (BER, Denver) did it through governance vacuums, owner-driven changes, and bespoke first-of-a-kind systems with no fallback.

## 4. Data Points a Strategist Can Use Verbatim

1. "Denver International Airport terminated its $1.8 billion Great Hall renovation contract after months of disputes; the fired contractor pegged the delay at more than three years and overruns at more than $300 million, citing 'the multitude of Owner Changes being issued on the project.'" [Source: https://www.constructiondive.com/news/great-hall-claims-dias-lack-of-engagement-contributed-to-airport-renovatio/567441/]

2. "Berlin Brandenburg opened nine years late, with costs rising from roughly €2.5–2.8 billion to more than €6.5 billion — and the controlling defect was a fire-safety system 'not built according to the construction permit,' designed by a man qualified as an engineering draughtsman, not an engineer." [Source: https://en.wikipedia.org/wiki/Construction_of_Berlin_Brandenburg_Airport]

3. "Heathrow Terminal 5 was delivered on time and on its £4.3 billion budget because the owner held all the risk in a single integrated team — and still lost more than 23,000 bags and cancelled over 500 flights on opening day because a test software filter was never removed." [Source: https://cdn2.f-cdn.com/files/download/1815034/eLHMsHeathrow%20Fiasco.pdf]

4. "GAO found planned airport projects running near $22 billion a year against roughly $14 billion actually received — and that deferring investment 'increased construction times and costs,' with preventive maintenance returning $4 to $10 for every $1 spent on time." [Source: https://www.gao.gov/assets/gao-20-298.pdf]

5. "LaGuardia's Terminal B — described by its delivery team as potentially 'the most complex aviation project anywhere ever' because the old terminal stayed fully operational throughout — cost roughly $5.1 billion for a single terminal, built on new footprint and bridged over live taxiways." [Source: https://www.theb1m.com/video/laguardia-airport-rebuild-terminal-b]

---

## 5. The Engineer's Bottom Line for the Dulles Decision

**Design FOR now:** the durable layer's reserve. Wide column grids, generous floor-to-floor, distributed electrical and conduit capacity to the concourses, transformer-vault and apron-edge power for electrified GSE, and structural provisioning for future vertical circulation. This is the spend you cannot recover later at any price.

**Accommodate LATER (leave soft):** screening geometry (design lane bays deeper and more power-dense than today's CT footprint, but don't hard-wire a screening topology), fit-out, IT/sensing, and gate equipment. Make these genuinely swappable by getting the durable stubs right.

**Bet AGAINST (explicitly):** fully distributed/off-airport processing as the *primary* built-form organizing principle, eVTOL-at-scale apron geometry, and any single-vendor, first-of-a-kind life-safety or baggage system with no operational fallback. Hedge these as options on soft space, not as load-bearing assumptions.

**And on the schedule:** the 2026–2034 window running three concurrent mega-packages around a live United hub, with the passenger-access system itself under reconstruction, is optimistic. Not because anyone is incompetent — because interface risk between concurrent contracts, unknown 1960s–1980s existing conditions, and operational-readiness testing are systematically underestimated in the first schedule. The first schedule is always wrong. Build the contingency, the risk-holding governance model (T5, not BER), and the build-new-before-you-demolish phasing (LGA-B) in now, or pay for their absence in claims later.
