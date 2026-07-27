# Technology-Scout Brief: Data-Center Technology vs. the Approach Surface at IAD

**Run:** data-centers-on-aircraft-approach · **Lens:** what the technology actually does, and whether the physics supports the author's objections
**Bottom line:** The author's strongest, most defensible objection is the thermal-plume/atmospheric-disturbance concern — because the FAA already treats exhaust plumes as an aviation hazard in its own guidance, and because an airport is *right now* (2026) formally opposing a near-identical data center on exactly these grounds. The lighting objection is the weakest as written and should be reframed. The electromagnetic-interference objection is legitimate but should be framed as "a formal study is required," not "interference is proven."

---

## 1. What the technology is, and why it matters to this argument

A hyperscale data center is not a passive box. Its aviation-relevant emissions come from three subsystems, and the author's case is only as strong as the subsystem it points at:

- **On-site / backup power generation** — banks of diesel or gas generators, sometimes on-site gas turbines. This is the dominant thermal-plume and exhaust source. A single hyperscale campus routinely fields dozens of multi-megawatt gensets. The Inyokern, CA proposal is a 99 MW data center with **40 diesel generators** [Source: https://bakersfieldnow.com/news/local/inyokern-airport-joins-opposition-to-proposed-data-center-citing-community-impacts].
- **Cooling** — evaporative cooling towers produce visible vapor plumes and localized fog; air-cooled/dry coolers and closed-loop liquid cooling produce far weaker buoyant plumes. Plume magnitude is a *design choice*, so the objection is strongest when tied to the specific cooling and generation design, not to "a data center" in the abstract.
- **The building envelope and site** — exterior/security lighting, obstruction lighting, glass/glare, and the adjacent stormwater pond.

The single most useful move for the writer: **anchor the plume argument to the generators and any evaporative cooling, not to the building.** That is where the physics and the FAA guidance line up.

## 2. Key findings

1. **The FAA already classifies exhaust plumes as an aviation hazard — in writing.** AIM §7-6-16 (formerly §7-5-5) states that high-temperature exhaust plumes "can cause significant air disturbances such as turbulence and vertical shear," that results "may include airframe damage, aircraft upset, and/or engine damage/failure," and that turbulent effects "can extend to heights of over 1,000 feet above the height of the top of the stack or cooling tower." Critically, it says these hazards "are most critical during low altitude flight in calm and cold air, especially in and around approach and departure corridors or airport traffic areas" [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html]. That is a verbatim description of the IAD site.

2. **The FAA has a dedicated assessment tool for this exact question.** The agency publishes "Thermal Exhaust Plume Impact on Airport Operations: Technical Guidance and Assessment Tool," and directs airports to AC 150/5190-4 (Airport Land Use Compatibility Planning) [Source: https://www.faa.gov/sites/faa.gov/files/airports/environmental/land_use/Technical-Guidance-Assessment-Tool-Thermal-Exhaust-Plume-Impact.pdf]. The existence of a formal FAA tool means the plume concern is not speculative — it is a recognized study category MWAA can (and arguably must) invoke.

3. **A near-identical fight is live right now.** In June 2026, Inyokern Airport and NAWS China Lake both filed letters opposing a 99 MW hyperscale data center ~1 mile from the airport, citing "potential impacts to aviation safety, navigable airspace," and specifically that "the facility's cooling system and forty diesel generators will generate a considerable thermal plume" [Source: https://www.kget.com/news/environment/inyokern-airport-asks-for-aviation-impact-analysis-as-possible-data-center-looms/][Source: https://bakersfieldnow.com/news/local/inyokern-airport-joins-opposition-to-proposed-data-center-citing-community-impacts]. This is a contemporaneous, named precedent of an airport making the author's argument.

4. **There is a quantitative hazard threshold — but it is international, not FAA.** Australia's CASA (MOS Part 139) treats a plume with vertical velocity exceeding **4.3 m/s** as a potential hazard to aircraft [Source: https://efiling.energy.ca.gov/GetDocument.aspx?tn=57789]. The FAA's own approach is qualitative (the assessment tool), so cite 4.3 m/s as an international benchmark, not as a U.S. regulatory line — otherwise a reviewer will catch it.

5. **The electromagnetic-interference concern is legitimate but siting-dependent.** The closest evidentiary analog is wind-turbine interference with radar and navaids, studied extensively by an FAA/DoE/DoD/NOAA interagency effort. Those studies found VOR/DVOR degradation is avoidable "if sited according to standard guidelines established by the FAA" [Source: https://windharvest.com/wp-content/uploads/2017/04/Assessment-of-the-Effects-of-Wind-Turbines-on-Air-Traffic-Control-Radars-John-J.-Lemmon-John-E.-Carroll-Frank-H.-Sanders-Doris-Turner-U.pdf]. Read into this argument: EMI from switchgear, gensets, and UPS is a real, studiable risk, and the correct posture is "no build without an FAA electromagnetic/navaid study," which is exactly the author's "we don't know" framing.

6. **MWAA has a standing motive to say yes — which is why discipline matters.** MWAA has previously moved to monetize Dulles land for data centers, including a proposed sale of 424 acres to Digital Realty [Source: https://www.loudounnow.com/2018/09/14/424-acres-at-dulles-airport-could-be-sold-for-data-centers/], inside the densest data-center market on earth (Loudoun County, "Data Center Alley"). Loudoun already runs an Airport Impact Overlay District to protect Dulles airspace [Source: https://www.loudoun.gov/5657/Airport-Impact-Overlay-District]. The land pressure is real; the author is the check on it.

7. **The lighting objection, as written, is the weakest link.** Modern hyperscale data centers are typically windowless, low-glare structures with security-grade — not stadium — lighting. "Data centers generate bright lights" is easy to rebut. The defensible version is *glare and obstruction-lighting placement near the RWY 19R approach lighting system*, plus *vapor-plume fog reducing approach visibility* — both of which sit under FAA glare/lighting and land-use guidance. Reframe or drop the raw "bright lights" claim.

## 3. What is real vs. hype in the objection

- **Real:** plume turbulence/vertical shear as a recognized FAA hazard in approach/departure corridors; the FAA assessment tool; a live 2026 airport-vs-data-center precedent on identical grounds; EMI as a studiable risk with regulatory precedent.
- **Overstated as written:** "bright lights" (reframe to glare/fog); implying certainty of EMI harm (it's siting-dependent — demand a study, don't assert the outcome); citing 4.3 m/s as if it were a U.S. rule (it's Australian — label it).
- **The cleanest logical spine:** the plume/atmospheric hazard and the land-use/future-capacity arguments do not require MWAA to *prove* harm. They require MWAA to show the project was never studied against FAA plume, glare, and EMI guidance, was not on an approved ALP, and forecloses future runway capacity — so the burden is on the proponent to complete those analyses first.

## 4. Data points a writer can use verbatim

- "High temperature exhaust plumes can cause significant air disturbances such as turbulence and vertical shear… Results of encountering a plume may include airframe damage, aircraft upset, and/or engine damage/failure… most critical during low altitude flight in calm and cold air, especially in and around approach and departure corridors." — FAA AIM §7-6-16 [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html]
- "Some studies do predict that the significant turbulent effects of an exhaust plume can extend to heights of over 1,000 feet above the height of the top of the stack or cooling tower." — FAA AIM §7-6-16 [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html]
- Inyokern data center: "the facility's cooling system and forty diesel generators will generate a considerable thermal plume" — NAWS China Lake letter, June 2026 [Source: https://bakersfieldnow.com/news/local/inyokern-airport-joins-opposition-to-proposed-data-center-citing-community-impacts]
- International hazard benchmark: plume vertical velocity **> 4.3 m/s** may be a hazard to aircraft (Australia CASA MOS Part 139) [Source: https://efiling.energy.ca.gov/GetDocument.aspx?tn=57789]

## 5. Caveats on the evidence

- The 4.3 m/s figure is a foreign regulator's criterion, widely cited in plume studies but not codified by the FAA; the FAA path is the qualitative assessment tool + AIM warning.
- The Inyokern precedent is a proposal in dispute, not an adjudicated denial; use it as "airports are actively raising this," not "the FAA has ruled."
- EMI evidence is analogical (wind turbines/power infrastructure), not a data-center-specific FAA study — which is itself the point: the absence of a study is the argument.
