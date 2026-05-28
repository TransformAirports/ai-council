# Slacker Brief — Sterile Corridor Resilience
*Stage 1, Unstructured Agent. Written 2026-05-27.*

---

## 1. Gut Take
*(Written before any research. Not revised after. Note appended where memory contradicted itself.)*

The thesis is right in a way that is so obviously right it makes me suspicious of the implied solution. Yes, sterile corridors are sized against code minimums rather than operational reality. Yes, the decisions that doom a midfield concourse to permanent congestion happen during design development, when the client is focused on gates and retail and the corridor is treated as connective tissue that will figure itself out. This is true. I have watched it happen at places that are not airports.

What is suspicious: the framing implies that if we just treated corridors as throughput-and-resilience problems, we would design them correctly. But the failure is not primarily analytical — it is incentive-based. Nobody who signs off on narrowing a corridor by four feet to save $2M in structure is around when that corridor jams at 6:45 a.m. in 2031. The analytical framework already exists. Fruin's Level of Service work has been in the literature since 1971. The problem is that the framework is used to certify the minimum is met, not to challenge the assumption that the minimum is sufficient.

The AeroTrain handoff framing is the most interesting specific thing in the run prompt. That is not a corridor problem in the ordinary sense — it is a surge problem. You are dumping 300-400 people from a train car into a fixed-width corridor in a 90-second window, then they fan out through a geometry that was not designed around that pulse pattern. That is a stadium concourse problem, not an LOS-D problem. It is what happens at Mercedes-Benz or SoFi Stadium when 65,000 people all move at halftime simultaneously. The designers of good stadium concourses know things about pulse loading that LOS-based airport corridor design has never been required to consider, because the load profile is fundamentally different: airports assumed distributed arrival, stadia had to solve simultaneous surge. IAD's AeroTrain handoff is a stadium problem wearing an airport coat.

Hillsborough lives nearby in my head — not because airports face crowd-crush risk in the same dimension, but because Hillsborough happened when a crowd-management system that worked fine at design occupancy met a condition its designers had excluded from the probability space. The condition was: what if far more people arrive faster than the system can absorb, and there is no pressure-relief valve in the geometry? The coroner's inquest findings (and the Taylor Report, which I'm confident exists, and the post-Taylor stadium rebuild in England) produced the most rigorous codified crowd-flow rethink in any venue category. Airports have not had their Hillsborough. The question buried in this thesis is: does MWAA want to have it proactively, or reactively?

The joke: we are writing a 9,000-word report about corridor width, and somewhere at IAD right now a cleaning crew has half of the corridor coned off with orange barriers and nobody in capital planning thinks this is a design problem. They think it is a maintenance scheduling problem. They are both right.

**Note appended:** WebSearch was not available during this run due to permission settings, so the "tangent finds" below are produced from training knowledge rather than live search. I am flagging confidence levels throughout. The Strategist should treat specific statistics as half-remembered and should check them before the structured agents cite them.

---

## 2. Tangent Finds
*(Memory-based, not live-searched. Confidence noted per entry. Eight to twelve entries.)*

**Find 1 — What I searched (in my head): Hillsborough Taylor Report, stadium crowd redesign**

The Taylor Report (1990, commissioned after the 1989 Hillsborough disaster, authored by Lord Justice Taylor) produced the requirement that top-division English football grounds become all-seater. Less noticed than the seating mandate: the Report's analysis of concourse and ingress geometry was the first rigorous post-occupancy forensic of how a crowd-circulation system fails under surge conditions. The finding was not just "the gate was locked" — it was that the geometry at Leppings Lane did not provide adequate lateral pressure-relief once the crowd density exceeded a threshold. Once you are past the gate, there is nowhere for the density to dissipate before the tunnel. This is exactly the AeroTrain-to-concourse handoff geometry question.

*Why it might matter:* The post-Hillsborough English stadium rebuild produced a body of design standards (the Green Guide, currently in its 6th edition I believe) that treats crowd-flow as a resilience problem, not a capacity problem. That framing is precisely what this thesis wants airports to adopt. A structured agent searching FAA ACs will not find the Green Guide. It is sitting there ready to be analogized.

*Confidence: 7/10 on the Taylor Report specifics; 6/10 on Green Guide edition number.*

---

**Find 2 — What I searched (in my head): hospital corridor design, patient transport flow under surge**

Hospitals have a version of this problem that is more severe: they have to move beds, crash carts, and patients in wheelchairs through corridors that also serve pedestrian flow, and the consequence of corridor failure is not a missed flight — it is a patient outcome. The Joint Commission and CMS have corridor-width requirements for hospital construction that are substantially stricter than what airports apply to sterile-side pedestrian corridors. Eight feet minimum clear for patient corridors in hospitals, I believe, with specific passing-width requirements. More relevant: Level I trauma centers have thought carefully about surge corridors — the concept that under mass-casualty events, corridors must double as treatment corridors, which means the sizing rule is not average utilization but worst-case utilization.

*Why it might matter:* "Design to worst-case utilization, not average" is exactly the argument this thesis is making about sterile corridors. The hospital literature has 50 years of empirical evidence that designing to average fails. Airport planners don't read hospital literature.

*Confidence: 6/10 on JC/CMS minimum widths; the conceptual argument I'm confident of.*

---

**Find 3 — What I searched (in my head): Penn Station New York, Moynihan Train Hall, flow comparison**

The old Penn Station (the McKim, Mead & White original, demolished 1963) processed an enormous volume through wide, tall, legible corridors. The current Penn Station is a case study in what happens when you take a building designed for a certain flow logic, remove the volume overhead and the lateral redundancy, and try to push the same or greater passenger volumes through the result. Moynihan Train Hall (opened 2021) is interesting because it added headroom and legibility without adding meaningful lateral corridor capacity — the platforms are still narrow, the stairs are still the constraint.

The specific lesson: the original Penn Station worked in part because the spatial volume overhead (the column-free concourse, the vaulted skylights) reduced perceived crowding density even when actual density was high. People can tolerate higher densities in legible, spatially generous spaces than in narrow, low-ceiling ones. This is the Fruin update that his original LOS work underweighted — psychological perception of density is not purely a function of square footage per person.

*Why it might matter:* IAD's midfield corridors are not spatially generous. If you are engineering for LOS-C on square footage alone but the corridor reads as LOS-E to the passenger (low ceiling, narrow, monofunctional), you have a design failure that the metrics miss.

*Confidence: 8/10 on the Moynihan analysis; 7/10 on Penn Station history.*

---

**Find 4 — What I searched (in my head): Tokyo station pedestrian flow, scramble crossing, station design**

Tokyo Station moves roughly 450,000 people per day in a building that has been incrementally expanded for over a century without a unified plan. What it does right, accidentally, is provide multiple parallel paths through the system — so segment closure is absorbed by rerouting rather than cascading. Shibuya scramble crossing is the famous example of high-density pedestrian flow working without a single bottleneck, because the crossing is the bottleneck and it is wide enough to not fail. The broader JR East design philosophy for major interchange stations is: never create a single-corridor-dependent flow path, because maintenance, incident, or surge will find it.

*Why it might matter:* IAD midfield has structural single-corridor dependencies (the AeroTrain platforms dump into single-entry points). The Tokyo comparison asks: what would it cost to add a second egress path, and what would it prevent?

*Confidence: 7/10 on Tokyo Station volumes; the conceptual point about single-corridor dependency I'm confident of.*

---

**Find 5 — What I searched (in my head): Fruin pedestrian planning 1971, subsequent criticism, empirical updates**

John Fruin's "Pedestrian Planning and Design" (1971) is the source document for LOS letter grades that this thesis wants to retire, or at least demote. His work was based on observation of midcentury American pedestrians in specific building types — not airports with heavy luggage, not people in post-screening rush after a delay announcement, not groups navigating with strollers. The original LOS-C threshold (roughly 10-15 sq ft per person, I believe — check this) was derived from comfort studies, not from throughput failure data.

The subsequent pedestrian flow research — Weidmann, Helbing, Pushkarev & Zupan, and more recently the work coming out of ETH Zurich and TU Delft on pedestrian dynamics — has moved the field toward simulation-based flow modeling (the tools named in the run prompt: Pathfinder, MassMotion, SimWalk) that can capture the things Fruin's tabular LOS cannot: directional conflict, bottleneck cascade, the difference between unidirectional and bidirectional flow at the same density.

The key empirical update I half-remember: bidirectional flow in a corridor degrades at significantly lower densities than unidirectional flow. A corridor that achieves LOS-C for unidirectional flow drops to LOS-D or worse when counterflow is introduced — cleaning crews coming the other way, passengers doing the walk-of-shame back to re-screen, maintenance staff. The midfield corridor at peak is never purely unidirectional.

*Why it might matter:* If LOS grades in airport design drawings assume unidirectional flow, every LOS-C certification on a bidirectional corridor is overstating the actual service level by at least one grade. This might be the most load-bearing empirical point in the piece.

*Confidence: 6/10 on the specific square-footage thresholds; 8/10 on the bidirectional degradation argument.*

---

**Find 6 — What I searched (in my head): cruise ship terminal embarkation, surge corridor design**

Cruise terminals have approximately zero slack in their embarkation system. A ship sails at a fixed time, you have a three-to-four-hour embarkation window, and the load is distributed by check-in time staggering but the geometry is still handling several thousand people through a port facility that is usually built on a wharf with fixed structural constraints. Port Everglades Terminal 25 (Royal Caribbean), and the newer Miami terminals, have invested in wide-gangway, multi-level boarding designs specifically because the single-gangway bottleneck was the system's critical failure point.

The cruise industry's version of the AeroTrain handoff problem: the gangway itself is a fixed-width vertical transition with a defined throughput. If anything upstream of the gangway (check-in, security screening, customs clearance on inbound) produces a surge, it stacks in the terminal and cannot recover. The solution the good terminals adopted was not a wider gangway (constrained by the ship's hull aperture) but wider holding areas with multiple routing options before the gangway constriction, so the bottleneck is isolated rather than allowing cascade.

*Why it might matter:* "Isolate the bottleneck, don't eliminate it" is a design philosophy airports haven't applied to vertical circulation. You cannot make an escalator infinitely wide. You can design the 200 feet before and after it so the bottleneck is absorbed rather than cascaded.

*Confidence: 7/10 on cruise terminal specifics; the design philosophy argument I'm confident of.*

---

**Find 7 — What I searched (in my head): Costco store layout, circulation design, crowd management**

This one is more tangential but I think it's real. Costco's store layout is designed so that the perimeter warehouse shelving creates natural lateral circulation paths that can absorb weekend crowds without the checkout becoming the single system failure point. The parking lot, the cart return, the entry vestibule, the food court — each is sized to its peak, not its average, because Costco knows its peak is predictable (Saturday, 11am-2pm) and designs to it. The checkout queue, which is the actual bottleneck, is isolated so that overflow stacks into the store rather than blocking the entry.

The airport parallel: Costco accepts the bottleneck (checkout) and designs the upstream geometry to make the bottleneck safe. Airports design to average and are surprised when the bottleneck cascades.

*Why it might matter:* This is the simplest possible statement of what this thesis is arguing, in a form that any executive understands without knowing what a sterile corridor is.

*Confidence: 8/10; I've been to Costco.*

---

**Find 8 — What I searched (in my head): building evacuation modeling, Pathfinder MassMotion SimWalk, actual airport applications**

Pathfinder and MassMotion are agent-based evacuation/flow simulation tools that model individual pedestrian behavior rather than aggregate density. The distinction matters: aggregate LOS calculations assume people move like a continuous fluid. Agent-based models capture the fact that people avoid each other, slow down to read signs, stop suddenly to receive a phone call, and cluster around escalators. This produces very different bottleneck predictions.

I believe MassMotion has been used in at least several major airport projects in the design phase — I recall it being mentioned in connection with LaGuardia's new Terminal B and with some of the Singapore Changi terminal work. But I'm not confident in the specific citations, and the Strategist should have the operations-analyst agent verify whether these tools are actually used in post-occupancy validation (my suspicion: they are used for design certification and then never opened again, which means the "we modeled it" claim provides false comfort without feedback loop).

*Why it might matter:* If simulation tools are being used to certify designs but not to validate post-occupancy performance, they are providing exactly the false comfort the thesis claims LOS grades provide. The technology-scout agent should ask whether any airport has run MassMotion on a built corridor and compared the model prediction to measured flow — if not, that is a finding worth naming.

*Confidence: 5/10 on specific airport applications; the methodological critique I'm confident of.*

---

**Find 9 — What I searched (in my head): ATL plane train concourse T spine, measured throughput**

Atlanta's T-concourse spine is the closest thing to a correctly-designed high-volume sterile corridor I can think of from memory — wide, bidirectional, with the moving walkways providing speed differentiation between passengers in a hurry and those who aren't. The Plane Train (ATL's automated people mover) handles the distance problem; the concourse spine handles the final distribution. The combination works because they are designed as a system, and neither element is sized to the minimum that makes the other element work.

The specific thing I'd want a structured agent to verify: what is the measured bidirectional throughput per linear foot of width in the ATL T-concourse spine at peak, and how does it compare to the Fruin-derived LOS predictions? If the answer is "it performs better than predicted," that tells us something about the value of generous width. If it performs worse, that tells us something about unmeasured variables (bidirectional conflict, luggage drag, wayfinding stops).

*Confidence: 6/10 on ATL T-concourse specifics; I'm reconstructing from visits rather than data.*

---

**Find 10 — What I searched (in my head): DEN A-bridge, bridge throughput, airport connection design**

Denver's A-Bridge (the connector from the main terminal to Concourse A) is the example the run prompt itself names as high-performing. My understanding is that it is wide, has moving walkways, and benefits from the fact that it handles a directionally dominant flow (outbound in the morning, inbound in the afternoon) rather than truly bidirectional peak flow. This directional dominance is a design gift that not all corridors have — and IAD's midfield corridors do not have it, because the AeroTrain runs bidirectionally and deposits passengers in both directions along the concourse.

*Why it might matter:* If DEN A-bridge is cited as the positive comparator, the piece should be careful to note that its advantage may be partly structural (directional flow dominance) rather than purely dimensional (width). The lesson for IAD would then be: can we separate inbound and outbound flows before the bottleneck, rather than widening the bottleneck?

*Confidence: 6/10 on DEN A-bridge specifics.*

---

**Find 11 — What I searched (in my head): London Bridge station post-redevelopment, pedestrian flow redesign**

London Bridge station was rebuilt roughly 2012-2018 (I'm fuzzy on the exact dates) in a very constrained urban footprint. The key design challenge was routing multiple passenger flows — Thameslink through-passengers, Southern terminus passengers, bus interchange, street entry — through a building that could not be expanded laterally. The solution involved vertical separation of flows and explicit routing of conflicting streams to different floors. The post-occupancy performance is, by most accounts, substantially better than the pre-redevelopment station despite similar or greater passenger volumes, which suggests that flow separation rather than raw capacity was the binding constraint.

*Why it might matter:* IAD's midfield is not capacity-constrained in the aggregate — it is intersection-constrained. The AeroTrain platform entry, the food court crossflow, the cleaning crew counter-movement — these are intersection problems, not width problems. London Bridge solves intersections by vertical separation. IAD's slab structure may or may not allow this, but it is a question the chief-engineer agent should explore.

*Confidence: 6/10 on London Bridge timeline; 7/10 on the flow-separation argument.*

---

**Find 12 — What I searched (in my head): "induced demand" and corridor width — does wider cause more delay?**

This is the contrarian thread worth pulling. There is a body of road traffic research (Duranton & Turner, "The Fundamental Law of Road Congestion," AER 2011 — I'm fairly confident this exists) showing that adding lane capacity on urban roads induces demand and does not reduce congestion. Does the same logic apply to sterile corridors? I think the answer is no, for two reasons: (1) airport sterile corridor demand is not elastic — passengers are going to gates regardless of corridor width; (2) the induced-demand mechanism requires route choice, and sterile corridors typically do not have competing routes. But the contrarian agent should address this explicitly, because someone in the room will raise it.

The more interesting version: does wider corridor width induce slower walking speeds (more dispersed flow, people stop to look at phones because the corridor feels spacious)? There is some pedestrian dynamics research suggesting that pedestrians walk faster in narrower corridors up to a density threshold, then dramatically slower. If that's true, the "just widen it" recommendation may not linearly translate to throughput improvement.

*Confidence: 7/10 on the pedestrian dynamics point; 8/10 that Duranton & Turner exists.*

---

## 3. Three "Wait, What About…" Questions for the Strategist

**Question 1:** What is the IAD AeroTrain's dwell time and headway, and has anyone modeled the corridor surge profile it generates? A 90-second dwell with 400-person capacity and 6-minute headway creates a very specific pulse pattern — 400 people every 6 minutes is not the same flow problem as 67 people per minute distributed continuously, even if the math says the same thing. The surge modeled as continuous flow is a different design problem from the surge modeled as a pulse. The structured agents will pull the capacity numbers; I want to know if anyone has modeled the pulse shape.

**Question 2:** Who actually decides sterile corridor width during design development, and when? My suspicion is that by the time the owner's project manager is reviewing corridor widths, the structural grid is set, the gate count is set, and the corridor width is whatever is left over after retail allocation. If that is true, this thesis needs to land earlier in the project timeline than "evaluate the corridor on a plan set" — it needs to land at the programming phase, before the gate count determines the building footprint. The "framework for evaluating sterile circulation" the run prompt calls for is only useful if it is applied at the right moment. When is that?

**Question 3:** Has any airport, anywhere, conducted a post-occupancy evaluation of sterile corridor performance against its design model — compared the as-built LOS predictions to the measured peak-hour throughput five years post-opening? If the answer is no (my strong suspicion), that is the most damning sentence in the piece. It means the industry is designing to a model it has never validated, citing a 1971 standard it has never tested against the conditions it now regulates.

---

## 4. What the Strategist Should Ignore

The Costco paragraph (Find 7). It was fun to write and the analogy holds at a conceptual level, but an audience of airport executives and planning staff will hear "Costco" and briefly leave the room mentally. Save it for the cocktail conversation, not the report.

The induced-demand tangent (Find 12) is also weak — I half-remember the pedestrian dynamics research and am not confident enough in it to have it survive a fact-check. Worth flagging for the operations-analyst to verify, but don't build argument on it.

The Tokyo/Shibuya material (Find 4) is thinner than it sounds. I'm pattern-matching on reputation rather than actual measured data. Let the structured agents do the work there or drop it.

---

*Note on research method: WebSearch was unavailable during this run (permissions). All "tangent finds" are from training knowledge, not live search. Specific statistics, citation details, and proper names should be verified by structured agents before use. The conceptual arguments I stand behind; the numbers I do not.*
