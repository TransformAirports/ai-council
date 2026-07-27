# Technology Scout Brief — Data Centers at Airports: The Machine, Not the Box

**Run:** Data Centers at Airports: Airside Risks
**Lens:** Airport operational technology — the engineering that creates the hazard, and the engineering available to test for it
**Prepared for:** Stage 2 synthesis. Independent evidence; no other Stage 1 brief was read.

---

## The reframing this brief exists to make

A height-and-land-use review evaluates a shape: how tall is the box, does it pierce a Part 77 surface, does it cast a shadow on a NAVAID. That review is blind to the thing that makes a data center different from a warehouse of the same dimensions. The hazard a data center poses to aircraft is not a function of its silhouette. It is a function of the machinery inside and on the roof — how it rejects heat, how it makes backup power, and how much metal and radio noise it stacks near a localizer.

Put bluntly: **two data centers with identical footprints and identical heights can pose completely different airside risks, and the difference is invisible to an obstruction review.** One uses a closed-loop dry/liquid cooling plant and emits an invisible, modest thermal plume. The other runs banks of open evaporative cooling towers that throw a visible, buoyant, saturated plume hundreds of feet into a departure corridor. The regulatory surfaces treat them the same. The physics does not.

So the technology-scout's job here is two taxonomies:
1. **The hazard-generating technology** — which cooling and power configurations actually create airside risk, and which don't.
2. **The hazard-testing technology** — what's available off-the-shelf in 2026 to quantify plume velocity, EMI, and turbulence *before* approval, versus what still requires bespoke study.

Both matter because the thesis's core claim — *test for demonstrated compatibility, not just obstruction clearance* — only has teeth if the tools to demonstrate compatibility actually exist and are affordable. They do, and they are. That's the strategically useful finding.

---

## Key findings

1. **The airside risk is entirely configuration-dependent.** Evaporative/wet cooling towers produce buoyant, saturated, visible plumes; air-cooled and dry-cooler systems produce weaker, invisible thermal plumes; liquid/immersion cooling (now spreading fast because of AI compute density) rejects heat through outdoor dry or evaporative loops that vary case by case [Source: https://www.datacenterfrontier.com/cooling/article/55389787/tech-explainer-data-center-cooling-air-evaporative-liquid-and-hybrid-approaches]. A screening framework that does not ask *which cooling technology* is asking the wrong first question.

2. **There is a hard, quantified, aviation-specific plume criterion — and it is not American.** Australia's CASA sets a limiting **average vertical velocity of 4.3 m/s**; any facility whose plume exceeds that at the Obstacle Limitation Surface (or 110 m AGL elsewhere) must be assessed as a potential hazard to aircraft [Source: https://www.jandakotairport.com.au/images/files/ControlledActivity/CASA%20AC139-05%20Plume%20Rise%20Assessments.pdf]. The FAA has *no equivalent published numeric threshold*; it declares thermal plumes "incompatible with airport operations" and handles them case-by-case through obstruction evaluation and a free MITRE tool. This is a defensible-standard gap MWAA can close by importing the CASA number as a screening trigger.

3. **The most concentrated data-center cluster in the world already sits under an airport's flight paths.** Roughly 200 data centers in Ashburn/Sterling ("Data Center Alley") lie in the vicinity of Dulles, and a proposed "Dulles Cloud South" would add up to ~56 million sq ft south of the airport [Source: https://www.datacenterdynamics.com/en/news/loudoun-county-is-home-to-26-million-sq-ft-of-data-centers-dulles-cloud-south-could-add-another-56-million-sq-ft-if-it-passes/]. This is the natural-experiment reference case — and notably, the public fight there has been about noise, water, and power, *not* airside compatibility. The airside question has been under-asked, which is precisely the thesis.

4. **Plume turbulence is a documented aircraft-upset hazard, not a theoretical one.** The FAA's own guidance warns the turbulent effects of an exhaust plume can extend **over 1,000 ft above the top of a stack or cooling tower**, most dangerously in calm, cold, low-altitude conditions in approach/departure corridors [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html]. Documented encounters include an aircraft rolled 50–60° off level over cooling towers at ~550 ft AGL [Source: http://www.wacaz.com/services/obstruction-evaluation/the-effect-of-industrial-exhaust-thermal-plume-turbulence-on-aircraft/].

5. **The controlling operating scenario is prolonged emergency generation, not normal cooling.** Diesel backup generators typically run 50–150 hours/year each for testing, emitting PM2.5 and NOx [Source: https://www.wri.org/insights/us-data-center-growth-impacts]. A grid outage during a heat event flips a hyperscale campus from "invisible plume" to "dozens of diesel exhaust stacks running simultaneously at peak thermal load" — the worst-case plume, visibility, and emissions state, and the one an averaged environmental review will understate.

6. **Off-the-shelf assessment tools exist and are cheap.** MITRE's Exhaust Plume Analyzer is available at no cost and models plume flow plus aircraft-upset response for four aircraft classes (light-sport, light GA, business jet, large jet) [Source: https://www.mitre.org/our-impact/intellectual-property/exhaust-plume-analyzer]. General-purpose CFD (Fluent, OpenFOAM) and airport EMI suites (e.g., IDS EMACS) can model plume trajectory and ILS reflection respectively [Source: https://www.idscorporation.com/pf/emacs/]. The demonstration the thesis demands is technically routine; the gap is procedural, not technological.

7. **EMI risk comes from the box being a mirror, not just a transmitter.** A large, metal-clad structure near a runway can reflect and distort the ILS localizer's 90/150 Hz sideband pattern (multipath), independent of any radio noise the facility emits [Source: https://www.academia.edu/118801608/Electromagnetic_Interference_Analysis_on_Localizer_Beam_for_Various_Obstacles_at_Expanded_Airport]. Data centers are unusually dense, reflective, and RF-active. Both coupling paths — reflective obstacle and emitted RFI — warrant modeling.

8. **Wildlife and stormwater risk is a design-choice risk, not an inherent one.** FAA AC 150/5200-33C wants attractants kept beyond 10,000 ft (turbine airports) and 5 statute miles where they'd move wildlife across approach/departure airspace; it also wants detention basins to stay dry between storms [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf]. A data center's large impervious footprint and stormwater management can create standing water and bird habitat — or not, depending entirely on how the site engineer designs the basins.

---

## The hazard technology taxonomy (what actually creates airside risk)

### Cooling — the dominant variable

Heat rejection is where a data center meets the sky, and it is the single most important screening question. The configurations, from highest to lowest plume hazard:

- **Open (wet) evaporative cooling towers.** Reject heat by evaporating water into an induced-draft airstream. Output is a *warm, saturated, buoyant* plume that is visible in cool/humid conditions and carries real vertical momentum. This is the classic aviation-plume source — the same technology the FAA and CASA guidance was written around for power plants. Highest airside concern. Evaporative systems are attractive because they can cut cooling electricity 10–35% versus air-cooled in peak summer [Source: https://www.datacenterfrontier.com/cooling/article/55389787/tech-explainer-data-center-cooling-air-evaporative-liquid-and-hybrid-approaches], so the operator's efficiency incentive points *toward* the higher-hazard choice.

- **Hybrid / adiabatic coolers.** Run dry most of the year, spray water only on hot days. Plume behavior is intermittent — dry (invisible, modest) in normal operation, more buoyant on peak days. Screening must evaluate the *peak* state, not the annual average.

- **Dry coolers / air-cooled chillers.** No evaporation, no visible plume, no water consumed — but they reject the same total heat into the air as an *invisible* thermal plume, and use more energy to do it [Source: https://www.datacenterfrontier.com/cooling/article/55389787/tech-explainer-data-center-cooling-air-evaporative-liquid-and-hybrid-approaches]. Lower plume-turbulence risk, but "no visible plume" is not "no thermal plume." This is exactly the conflation the run warns against.

- **Liquid / immersion cooling.** Servers submerged in dielectric fluid or fed by direct-to-chip cold plates; heat is carried to an outdoor loop that is *still* either dry or evaporative [Source: https://www.vertiv.com/en-us/solutions/learn-about/liquid-cooling-options-for-data-centers/]. Immersion changes the indoor thermodynamics but does not eliminate the outdoor heat-rejection question — you must still ask what's on the roof. AI-driven rack densities are pushing the industry here fast, so 2026-era campuses increasingly mix liquid cooling indoors with large dry or evaporative fields outdoors.

**Scout's takeaway:** the plume hazard is a property of the *outdoor heat-rejection stage*, and it ranges from serious (open wet towers) to modest-but-real (dry coolers) to negligible. No single "data center plume" exists. Screening must classify the specific outdoor system and evaluate its worst-case (peak-load, still-air) state.

### Backup power — the controlling scenario

Hyperscale campuses back up with rows of diesel (increasingly some natural-gas or fuel-cell) generators, tested ~50–150 hours/year each [Source: https://www.wri.org/insights/us-data-center-growth-impacts]. Three technology facts matter airside:

- A grid outage during a heat wave is the **controlling scenario**: peak thermal load (highest cooling plume) *plus* full generator run (dozens of hot exhaust stacks) *plus* worst-case air quality, simultaneously. Any assessment averaged over normal operation misses it.
- Generator exhaust is hot and vertically directed — a second, independent plume source physically separate from the cooling plant.
- Emergency-response load: large fuel storage (tens of thousands of gallons of diesel), lithium-ion or VRLA battery rooms, and high-density electrical plant raise the ARFF/hazmat profile near the movement area — a public-safety cost that obstruction review never sees.

### The building as an RF obstacle

Two distinct EMI mechanisms, both modelable:
- **Reflective/multipath** — a large metal-clad box near the localizer distorts the beam's horizontal guidance pattern [Source: https://www.academia.edu/118801608/Electromagnetic_Interference_Analysis_on_Localizer_Beam_for_Various_Obstacles_at_Expanded_Airport]. This is a *shape-and-material* problem, so it partly overlaps obstruction review — but current review checks penetration, not reflectivity.
- **Emitted RFI** — dense switching power supplies and comms gear as a source; coupling via front-door (antenna) and back-door (cabling, seams) paths [Source: https://www.mdpi.com/2079-9292/14/12/2483].

---

## The assessment technology taxonomy (what's available to demonstrate compatibility)

This is the load-bearing half of the brief, because the thesis asks proponents to *prove* compatibility. Here's what 2026 offers.

**Off-the-shelf, low-cost, mature:**
- **MITRE Exhaust Plume Analyzer** — free; convective flow model + aircraft-upset response for four aircraft classes + turbulence probability [Source: https://www.mitre.org/our-impact/intellectual-property/exhaust-plume-analyzer]. This is the FAA's de facto screening tool and directly outputs the "will this upset an aircraft" answer.
- **CASA-style plume-rise assessment** — a defined method with the 4.3 m/s vertical-velocity trigger at the OLS/110 m AGL [Source: https://www.jandakotairport.com.au/images/files/ControlledActivity/CASA%20AC139-05%20Plume%20Rise%20Assessments.pdf]. Directly importable as a screening threshold.
- **Airport EMI modeling suites** (e.g., IDS EMACS) — model ILS/VOR/radar distortion from proposed structures [Source: https://www.idscorporation.com/pf/emacs/].
- **FAA AC 150/5200-33C** — deterministic wildlife-separation distances and stormwater-design rules [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf].

**Requires custom engineering work (project-specific, but routine):**
- **Full CFD plume trajectory modeling** (Fluent/OpenFOAM) for a specific building geometry, stack layout, and local wind climatology — needed when a facility is near the 4.3 m/s line or has complex multi-source geometry [Source: https://www.sciencedirect.com/science/article/abs/pii/S0360544220317187]. Meaningful cost, but standard consulting-engineering scope.
- **Site-specific meteorological analysis** — the plume hazard peaks in calm, cold, stable air, so a credible assessment needs local wind/temperature statistics, not generic assumptions.
- **Combined worst-case scenario modeling** (peak cooling + full generator run in still air) — not a packaged product; must be specified by the reviewing authority.

**Genuinely immature / hype-adjacent:**
- **"Digital twin of the airspace" for continuous plume monitoring.** Vendors market airport digital twins and there is real academic CFD work on aerodrome-surface jet effects, but a validated, real-time, operational plume-and-turbulence twin tied to live sensors is *not* an off-the-shelf product you can buy and trust in 2026. Treat any such claim as pre-commercial.
- **Real-time in-plume turbulence sensing feeding ATC.** Conceptually attractive, operationally unproven at airports. Don't build a compatibility case on it.

---

## Maturity assessment: what's real, what's hype

**Real:**
- The plume-turbulence hazard. It's in FAA guidance, it has a foreign numeric standard, and it has documented aircraft upsets [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html].
- The tools to assess it before approval. Mature and mostly cheap.
- The configuration-dependence. This is engineering fact, not opinion.

**Overstated / needs skepticism:**
- **Vendor "sustainable/waterless cooling" marketing** implies zero externality; waterless (dry) cooling still rejects the full heat load as an invisible plume and uses more power [Source: https://www.datacenterfrontier.com/cooling/article/55389787/tech-explainer-data-center-cooling-air-evaporative-liquid-and-hybrid-approaches]. "Waterless" solves the water fight, not the airside plume.
- **Any figure quantifying data-center airside risk specifically.** There is essentially no independent, airport-specific empirical literature on *data-center* plumes and aircraft. The evidence base is borrowed from power plants and cooling towers — physically analogous, but an honest brief flags that the direct data center case history is thin. The Data Center Alley/Dulles cluster is the closest thing to a live experiment, and no airside incident has been publicly documented there. That absence is weak evidence of safety and should not be oversold either way.
- **"The FAA process already covers this."** It covers obstruction and, case-by-case, plumes via the MITRE tool — but there is no automatic trigger that flags a *data center* as a plume source, and no numeric U.S. threshold. Coverage is discretionary, not systematic. That's the gap the thesis exploits.

**Honest counter-argument (steelman):** most modern hyperscale campuses are moving toward dry and liquid cooling for water-scarcity reasons, which *reduces* the visible-plume problem; the 4.3 m/s criterion was written for power-station cooling towers with far greater single-point heat flux than a distributed data-center dry-cooler field; and no documented data-center-caused aircraft upset exists. A fair screening framework should therefore be *risk-tiered* — heavy scrutiny on open-evaporative near approach corridors, light-touch on dry/liquid systems well outside them — not a blanket obstacle.

---

## Verbatim data points for the strategist

1. "An exhaust plume with a vertical velocity in excess of **4.3 metres per second may cause damage to an aircraft airframe, or upset an aircraft when flying at low levels** — Australia regulates to this number; the FAA publishes no equivalent threshold." [Source: https://www.jandakotairport.com.au/images/files/ControlledActivity/CASA%20AC139-05%20Plume%20Rise%20Assessments.pdf]

2. "The significant turbulent effects of an exhaust plume can extend to heights of **over 1,000 feet above the top of the stack or cooling tower**, and are most dangerous in calm, cold air within approach and departure corridors." [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html]

3. "**Roughly 200 data centers** already sit in Data Center Alley within the vicinity of Dulles flight paths, and a proposed expansion would add up to **56 million square feet** south of the airport — yet the public debate has been about noise, water, and power, not airside compatibility." [Source: https://www.datacenterdynamics.com/en/news/loudoun-county-is-home-to-26-million-sq-ft-of-data-centers-dulles-cloud-south-could-add-another-56-million-sq-ft-if-it-passes/]

4. "The tool to test for this is free: MITRE's Exhaust Plume Analyzer models plume flow and **aircraft-upset response for four aircraft classes** — the demonstration the thesis demands is technically routine; the gap is procedural." [Source: https://www.mitre.org/our-impact/intellectual-property/exhaust-plume-analyzer]

5. "Backup diesel generators run roughly **50 to 150 hours per year** each for testing — but the controlling airside scenario is a grid outage during a heat wave, when peak cooling plume and full generator exhaust occur simultaneously." [Source: https://www.wri.org/insights/us-data-center-growth-impacts]

---

## Implications for the MWAA screening framework (technology inputs only)

1. **Classify the outdoor heat-rejection system first** (open evaporative / hybrid-adiabatic / dry / liquid-with-dry / liquid-with-evaporative). This single answer sets the risk tier.
2. **Import the 4.3 m/s vertical-velocity trigger** at the OLS or 110 m AGL as the screening threshold the U.S. framework lacks.
3. **Require a MITRE Exhaust Plume Analyzer run** for any evaporative or hybrid system inside the approach/departure footprint; escalate to full CFD with local met data when results approach the threshold.
4. **Require worst-case combined-scenario modeling**: peak thermal load + full generator run + still, cold air — the state an averaged environmental review omits.
5. **Require an ILS/NAVAID reflection-and-RFI study** using an airport EMI suite, treating the building as both a reflective obstacle and an RF source.
6. **Apply AC 150/5200-33C wildlife/stormwater design conditions** as approval conditions, not afterthoughts — dry-basin design, no standing water.
7. **Score public-safety load** (diesel storage volume, battery chemistry, hazmat) as an emergency-response cost, separate from obstruction.

**Bottom line for Stage 2:** the technology to demonstrate compatibility is mature, mostly cheap, and already used for power plants. The reason data centers slip through is that the U.S. review is triggered by *shape*, and the hazard lives in the *machinery*. Close that gap with a configuration-first, risk-tiered screen — and be honest that the direct data-center incident record is thin, so the framework should scale scrutiny to the cooling choice rather than ban the land use.

---

### Sources
- Data Center Frontier — cooling technology types: https://www.datacenterfrontier.com/cooling/article/55389787/tech-explainer-data-center-cooling-air-evaporative-liquid-and-hybrid-approaches
- Vertiv — liquid/immersion cooling: https://www.vertiv.com/en-us/solutions/learn-about/liquid-cooling-options-for-data-centers/
- CASA AC 139-05 / 139.E-02 — plume rise assessments (4.3 m/s): https://www.jandakotairport.com.au/images/files/ControlledActivity/CASA%20AC139-05%20Plume%20Rise%20Assessments.pdf
- CASA AC 139.E-02 v1.1: https://www.casa.gov.au/sites/default/files/2023-03/advisory-circular-139e-02-plume-rise-assessments.PDF
- FAA AIM 7-6-16 — avoid flight near exhaust plumes: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html
- MITRE Exhaust Plume Analyzer: https://www.mitre.org/our-impact/intellectual-property/exhaust-plume-analyzer
- WACAZ — effect of industrial thermal plume turbulence on aircraft (documented upset): http://www.wacaz.com/services/obstruction-evaluation/the-effect-of-industrial-exhaust-thermal-plume-turbulence-on-aircraft/
- DataCenterDynamics — Loudoun/Dulles Cloud South: https://www.datacenterdynamics.com/en/news/loudoun-county-is-home-to-26-million-sq-ft-of-data-centers-dulles-cloud-south-could-add-another-56-million-sq-ft-if-it-passes/
- WRI — data center community impacts (generators, emissions): https://www.wri.org/insights/us-data-center-growth-impacts
- FAA AC 150/5200-33C — hazardous wildlife attractants: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf
- Academia — EMI/localizer beam analysis for obstacles at airports: https://www.academia.edu/118801608/Electromagnetic_Interference_Analysis_on_Localizer_Beam_for_Various_Obstacles_at_Expanded_Airport
- MDPI Electronics — RFI mitigation in civil aviation: https://www.mdpi.com/2079-9292/14/12/2483
- IDS EMACS — airport electromagnetic analysis: https://www.idscorporation.com/pf/emacs/
- ScienceDirect — CFD simulation of exhaust jet near aerodrome surfaces: https://www.sciencedirect.com/science/article/abs/pii/S0360544220317187
