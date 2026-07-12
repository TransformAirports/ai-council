# Council Brief — Donella Meadows (Systems Lens)

## Run: Future-Proofing the Dulles Terminal Rebuild

---

## The claim in one line

The Dulles terminal will not date because MWAA forecasts technology badly. It will date because a terminal **couples stocks that move at wildly different speeds** — 50-year concrete bolted to a 10-year processing sequence — and when the fast thing changes, you are forced to pay to move the slow thing. The design question is not "what comes next" (nobody knows) but "how do I keep the fast layers free to change without dragging the slow layers with them." That is a systems-structure problem, not a forecasting problem. Almost every dollar the industry spends on "future-proofing" is aimed at the wrong level of the system.

---

## 1. Stocks and flows: the terminal has at least five clocks, and the failures happen at the seams

A terminal is not one thing accumulating. It is a stack of stocks, each with its own time constant. Stewart Brand's "shearing layers" framing is the right starting mental model; the airport version:

| Layer (stock) | Half-life | Cost to change once built |
|---|---|---|
| Site geometry: apron depth, runway/taxiway relationship, level changes | 50–100 yr | Prohibitive |
| Structure: column grid, floor-to-floor, vertical circulation spines | 50+ yr | Very high |
| Services: power feeders, conduit, comms pathways, thermal capacity | 20–40 yr | High if under-provisioned |
| Space plan: checkpoint halls, gate holds, back-of-house, retail | 10–20 yr | Moderate |
| Stuff/fit-out: IT, sensors, scanners, furniture, security regime | 3–10 yr | Low |

The **behavior of the whole system is governed by the slow stocks**, not by the fast events everyone argues about. When leadership debates "biometrics vs. no biometrics," they are arguing about the fastest, cheapest, most reversible layer — the one that will be replaced two or three times before the concrete is amortized. Meanwhile the decisions that actually lock the building's fate — floor-to-floor height, where the level changes fall, how deep the apron is, whether the checkpoint hall is load-bearing to the geometry above it — get made quietly, by engineers, on cost grounds, and are never revisited.

**The failures cluster at the seams between fast and slow layers.** A terminal dates fastest wherever a fast function (screening, processing sequence) was hard-wired *into* a slow layer (structure, geometry) so that changing the function requires moving the structure. That coupling is the disease. De-coupling is the cure. Everything below follows from that.

---

## 2. The reinforcing loop that already killed one Dulles design bet: lock-in by delay

Dulles is not a hypothetical for path dependence — it is the textbook case, and the current $22B program exists partly to pay off the last one.

**Loop R1 — Sunk-cost lock-in (the mobile lounge story):**

```
   design commitment (mobile lounges, 1962)
        │
        ▼
   terminal geometry built AROUND it
   (detached midfield concourses, no walking spine)
        │
        ▼
   whole operation fitted to the commitment
   (fleet of lounges, staffing, passenger habit)
        │
        ▼
   cost & disruption to reverse RISES every year
        │
        ▼
   "too expensive to change now" → keep it
        │
        └──────────► deeper commitment ──────┐
                                              ▼
                              (loop reinforces for 48 years)
```

Saarinen's 1962 mobile lounge was celebrated as future-proof — it decoupled the terminal from the aircraft so the airfield could grow without rebuilding the head house. But jet bridges and midfield concourses erased its benefit within a generation, and by then the *geometry* — a main terminal with no physical connection to where the planes actually were — was locked. The system ran the wrong answer for **48 years** (1962→2010 AeroTrain) and MWAA is *still* paying: the current program spends **$3.75B** to extend AeroTrain west and kill the last mobile-lounge legs on D and international arrivals.

The lesson is not "mobile lounges were dumb." They were a reasonable bet. The lesson is about **delay**: the gap between making the error and feeling it was so long that the reinforcing loop ran unchecked for half a century. **This is the single most important dynamic in the room, and the new program is structurally set up to repeat it** — it is drawing checkpoint halls, gate geometry, and a landside/airside split now, and will not learn whether those bets were wrong until ~2040, by which point R1 will again have made them unaffordable to reverse.

**Design rule that falls out of R1:** for every major decision, plot it on two axes — *(a) how many years until I learn if I was wrong, and (b) what it costs to reverse at that point.* Decisions in the top-right quadrant (long delay to feedback, expensive to reverse) are where you buy optionality regardless of cost, because the reinforcing loop will not let you fix them later.

---

## 3. The balancing loop the mega-terminals ignored: processing time is a draining stock

The thesis is right that IST, PKX, BER, and LGA "locked in geometry sized for the throughput logic of the decade they were drawn in." Here is the mechanism, as a loop.

**Loop B1 — Processing time governs terminal volume:**

```
   passenger processing time per head (a STOCK, draining)
        │  drained by: mobile check-in, off-airport bag,
        │  self-service/distributed screening, biometric ID
        ▼
   queue length & dwell-in-process FALLS
        │
        ▼
   the constraint that JUSTIFIED building volume
   (big checkpoint halls, deep gate holds) RELAXES
        │
        ▼
   but building volume is a LOCKED stock — it cannot drain
        │
        ▼
   result: OVERSHOOT — a building sized for a queue
   that no longer exists
```

A checkpoint hall is sized for peak queue depth. Gate-hold areas are sized for the dwell a sequential process forces on people. Both are downstream of *processing time*, which is a stock that technology is actively draining. TSA's self-service prototype at Harry Reid (LAS) is a live signal: PreCheck passengers already screen themselves at their own pace, and the second-gen unit is a small cabinet, not a hall. If on-person screening distributes and de-sequences over 10–25 years, B1 says the very spaces the building is being sized around today are the ones that will be over-scaled tomorrow. That is not a technology risk. It is a **stock-flow structure guaranteeing overshoot whenever a downstream stock (built volume) is locked while its upstream driver (processing time) keeps falling.**

The systems-honest move is not to bet that processing collapses (it might not — see the regulatory balancing loop in §5). It is to refuse to let volume be *load-bearing*. Make the checkpoint hall a large-span, low-obstruction floor plate that can be re-tenanted — screening today, something else in 2040 — without touching the structure above it.

---

## 4. Leverage points: the whole industry intervenes at the weakest level

Meadows' hierarchy of leverage, weakest to strongest, mapped to this program. The tragedy is that master plans, McKinsey decks, and program budgets concentrate almost entirely on levels 12–10 (parameters) and touch levels 4–2 (goals, paradigm) almost never — yet the leverage runs the other way.

**Level 12 — Parameters (weakest leverage; where 90% of the effort goes).**
Gate count, square footage, number of checkpoint lanes, PBB positions. Tuning these is what a master plan *is*. It feels like planning; it is almost useless as future-proofing, because it optimizes the current pipeline harder rather than freeing the building from it.

**Level 11 — Buffer/stock sizes (moderate).**
This is exactly the "durable vs. volatile" framework the run asks for, stated correctly. **Overbuild the slow, cheap-to-provision buffers now; starve the fast, expensive-to-fit-out ones.** Concretely for Dulles:
- Buy **structural bay depth and floor-to-floor height** you don't need yet — a taller, longer-span frame lets any future space plan drop in. Cheap now, impossible to retrofit.
- Buy **apron depth and stand-lot flexibility** now (see §5 gates).
- Massively over-provision **conduit, power feeders, comms pathways, and structural allowance for thermal/electrical load** — the decarbonization load (electrified GSE charging, on-site generation) is a near-certain future draw and is trivial to trench empty now, brutal to add under an operating terminal later.
- Do *not* build permanent, custom-fitted checkpoint or bag-hall enclosures. That is buying the fast layer as if it were slow.

**Level 10 — Flow/physical structure (strong).**
The column grid, where the level changes fall, the vertical-circulation spines. Set these to be reconfigurable. A regular, generous grid with services in accessible spines is the difference between a building that can be re-programmed and one that must be demolished. This is Dulles' actual weakness: level changes and circulation were historically organized around the mobile-lounge/AeroTrain logic. The new head-house extension (±300 ft each way) should be a **loose-fit, regular frame**, not a bespoke processing machine.

**Level 6 — Information flows.** A building that senses occupancy, queue, and stand state and lets operations re-allocate space in software rather than concrete. Cheap. Underrated.

**Level 5 — Rules of the system (very strong, mostly outside MWAA's hands).**
*Who* screens, *where*, and under what sterile-area rule is set by TSA/CBP, not MWAA. You cannot change this rule from the program office. So the leverage move is: **design so the building does not fight whichever rule wins.** Neither hard-commit to a monolithic central checkpoint nor hard-commit to distributed gate-level screening — build a frame that can host either, because you cannot control the rule and you will not know which way it breaks until after the concrete cures.

**Level 4 — Goals of the system (very strong).**
Right now the program's implicit goal is *maximize throughput of a known passenger sequence at lowest first cost.* That goal **guarantees** tight coupling, because the cheapest way to hit a throughput number is to size every space exactly to the current process. Change the goal to *preserve the maximum reconfiguration optionality per dollar over 50 years* and every downstream decision changes. This is a one-sentence change at a program meeting that is worth more than any gee-whiz technology.

**Level 2 — Paradigm (strongest).**
The governing paradigm is **"a terminal is a processing pipeline"** — a sequential machine that moves a passenger through fixed stations. The thesis' own words — screening distributes, gate:aircraft stops being 1:1, processing migrates onto the device — describe a **paradigm shift from pipeline to field/mesh**: a set of capabilities a passenger touches in variable order, some off-site entirely. A building drawn as a pipeline cannot gracefully become a field; a building drawn as a **flexible field with a pipeline currently running on it** can go either way. The single highest-leverage act available to the Dulles team is to stop drawing a pipeline and start drawing a re-programmable floor.

---

## 5. Which balancing loops will resist you — the unintended-consequence check

Every intervention trips other loops. Two will actively fight the flexibility this program buys, and if you ignore them you will build flexibility that never gets used.

**B2 — Regulation resists decentralization.** CBP Federal Inspection Station requirements, TSA sterile-area rules, and one-way flow mandates are a slow-moving, high-inertia stock. Distributed/gate-level screening is not merely a technology question; it is blocked today by rules that assume a consolidated sterile boundary. **Implication:** betting the *structure* on distributed screening is a bet against a slow regulatory stock that has every incentive to move last. Hedge — build central-capable and distributed-capable, hardwire neither.

**B3 — The lease structure re-locks the flexible gate.** You can pour MARS/swing-gate geometry (one widebody *or* two narrowbody, HKG-style) to hedge the collapsing 1:1 gate:aircraft relationship and fleet-mix uncertainty (widebody retirement, single-aisle long-haul, regional/eVTOL). But **preferential airline use-and-lease agreements with gate exclusivity will financially re-lock the physical flexibility you just paid for.** A swing gate leased exclusively to one carrier for 30 years is a fixed gate with extra hardware. The physical leverage (flexible apron) is defeated by the contractual rule (exclusive lease) unless common-use terms are written in parallel. Physical flexibility and commercial flexibility are one system; buying half of it wastes the money.

**B4 — The revenue loop that resists compression.** Dwell monetization is a reinforcing loop (more dwell → more retail → more concession revenue → more building sized for dwell). If processing compresses (B1), dwell shrinks or relocates landside/off-airport, and the concession revenue the building's *financial* model is sized around erodes. This is a "limits to growth" pattern: the retail-volume reinforcing loop hits the ceiling of a shrinking dwell stock. Do **not** underwrite the bond/revenue case on a dwell projection that assumes the current long, sequential, pre-security wait persists. High performers have historically over-projected airside retail; the honest planning number treats dwell as *volatile*, not durable.

---

## 6. Honest counter-argument: not everything here is a system, and over-flexing is its own failure loop

I am obligated to say where my own lens over-reaches.

**First, some of this is just plumbing, not systems epiphany.** "Pour a deeper apron and a taller floor-to-floor and trench empty conduit because it's cheap now and impossible later" is a Torvalds fix — concrete, local, obvious — not a feedback-loop revelation. Do not dress up cheap-provisioning-now in systems language to make it sound profound. Just do it.

**Second, optionality has a cost, and over-future-proofing is its own reinforcing failure loop.** A building softened everywhere serves no one well today — a flexible shed. BER's decade of paralysis is partly a monument to designing for every contingency and committing to none. There is a balancing counter to my whole argument: **each increment of flexibility adds first cost, complexity, and decision-deferral, which feeds schedule and budget risk, which can kill the program outright.** Rams would put it plainly: flexibility for its own sake is bad design. The discipline is not "make everything soft." It is **make the slow, expensive-to-reverse, cheap-to-provision layers robust; make the fast, cheap-to-reverse layers explicitly disposable; and stop agonizing over the middle.** Buy optionality only where the delay-to-feedback is long and the reversal cost is high (§2). Everywhere else, commit and move.

---

## 7. Two dated snapshots — as a delay, made concrete

The value of the 2035/2050 split is that it makes the **consequence delay** visible.

**2035 (the terminal opens into this).** Screening is partly self-service and biometric for trusted travelers but still anchored to a consolidated sterile boundary — B2 held. Gate:aircraft is loosening; MARS stands earn their keep as fleet mix churns. Dwell is compressing at the margin but the pipeline is intact. **A building drawn as a smart pipeline still basically works.** The errors are latent, not yet felt. This is exactly the window in which R1 (§2) quietly makes them permanent.

**2050 (the terminal must still operate in this).** If de-sequencing plays out, processing is distributed and partly off-site; the central checkpoint hall is over-scaled; dwell has migrated. The building's fate is now fully determined by whether the *slow layers* were left loose. If the head house was drawn as a re-programmable field with generous grid, spare structural capacity, and over-trenched services, 2050 is a re-tenanting exercise. If it was drawn as a bespoke pipeline, 2050 is the mobile-lounge story again — a celebrated design running the wrong answer, waiting for the next $4B program to undo it.

The delay between these two snapshots *is* the whole problem. Everything looks fine in 2035. That is the trap.

---

## 8. Sort for the program meeting: FOR now / accommodate LATER / bet AGAINST

Ranked by leverage, not by how much they cost.

**Design FOR now (the slow, cheap-to-provision, unaffordable-to-retrofit stocks — buy them regardless):**
- Generous, regular structural grid and extra floor-to-floor in the head-house extension. Loose fit over tight fit.
- Apron depth and stand-lot geometry for MARS/swing stands — *paired with common-use lease language* (or the flexibility is dead on arrival, §5-B3).
- Massively over-provisioned conduit, power feeders, comms spines, and structural/thermal allowance for the 2050 decarbonization load (GSE charging, on-site generation). Trench empty now.
- Non-load-bearing, re-tenantable checkpoint and bag-hall floor plates. The processing function sits *on* the structure, never *in* it.

**Accommodate LATER (build the frame to host it; do not commit the concrete):**
- Distributed/gate-level screening — the building can host it when B2 (regulation) moves, but nothing structural presumes it.
- Off-airport / on-device processing — leave landside capable of shrinking; don't hard-size a check-in hall to today's counts.
- eVTOL/regional apron — reserve the geometry, provision the power, build nothing speculative.

**Explicitly bet AGAINST (refuse to design around these unproven timelines — treat as bets, not givens):**
- Any single screening regime as permanent. Hardwire neither central nor distributed.
- Dwell/retail revenue holding at today's per-passenger levels — do not underwrite the bond case on it (§5-B4).
- Universal biometrics / full autonomy / eVTOL-at-scale arriving on a known date. Provision cheaply for optionality; commit structure to none of them.

**The one-sentence leverage move (Level 4 → Level 2):** change the program's goal from *"process a known passenger sequence at lowest first cost"* to *"preserve maximum reconfiguration optionality per dollar across 50 years,"* and stop drawing a pipeline — draw a re-programmable field with today's pipeline running on it. That reframing is free, and it outranks every technology decision on the table.

---

### Sources
- [A $22 Billion Program for Dulles — Airport Architecture (Substack)](https://byerussell.substack.com/p/a-22-billion-program-for-dulles)
- [US Plans $22 Billion Rebuilding of Washington Dulles Airport — US News](https://www.usnews.com/news/top-news/articles/2026-05-12/us-plans-22-billion-rebuilding-of-washington-dulles-airport)
- [A $22B Plan Could Transform Dulles Airport by 2034 — Northern Virginia Magazine](https://northernvirginiamag.com/news/2026/05/12/a-22m-plan-could-transform-dulles-airport-by-2034/)
- [Dulles International Airport Master Plan — flydulles.com](https://www.flydulles.com/about-airport/master-plan/dulles-international-airport-master-plan)
- [The Lonely Ballad of the Dulles Airport Mobile Lounge — Atlas Obscura](https://www.atlasobscura.com/articles/the-lonely-ballad-of-the-mobile-lounge)
- [Dulles Airport Replaces Distinctive Mobile Lounge System with AeroTrain — The Transport Politic](https://www.thetransportpolitic.com/2010/01/26/dulles-airport-replaces-distinctive-mobile-lounge-system-with-aerotrain/)
- [TSA and DHS S&T to Prototype Self-Service Screening System at Harry Reid International Airport — TSA](https://www.tsa.gov/news/press/releases/2024/03/06/tsa-and-dhs-st-prototype-self-service-screening-system-harry-reid)
- [Enhancing Aviation Operations Through Advanced MARS Gates — Sidara Collaborative](https://sidaracollaborative.com/Insights/Advanced-MARS-Gates)
- [Enhancing Airport Operations: The Power of MARS Gates — ACI-NA](https://airportscouncil.org/2024/09/03/enhancing-airport-operations-the-power-of-mars-gates/)
