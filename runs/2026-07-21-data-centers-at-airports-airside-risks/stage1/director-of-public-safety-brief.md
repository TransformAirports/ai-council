# Director of Public Safety — Stage 1 Brief
## Data Centers on the Airfield: The Public Safety Load Nobody Sizes Until It Burns

**Run:** Data Centers at Airports: Airside Risks
**Chair:** Director of Public Safety (airport police, ARFF/fire, 911/dispatch under one command)
**Lens:** Emergency-response capability, fire/hazmat load, first-responder communications, security, and the gap between a land-use approval and what my departments can actually deliver at 3 a.m.

---

## Framing: the risk the thesis undersells

The run thesis is about airspace and airfield-capacity compatibility — plumes, thermal turbulence, obstruction surfaces, wildlife, stormwater. Those are real. But the thesis treats "emergency-response demands" as one bullet among seven. From my chair it is the *controlling* public-safety scenario, and it is the one a height-and-land-use review is structurally incapable of catching.

Here is the core problem. A large-hub airport fire department is sized, staffed, equipped, and federally indexed to do one thing on a clock: get to a burning aircraft at the midpoint of the most distant runway and start agent application within roughly three minutes. That is the entire logic of 14 CFR Part 139 ARFF. A hyperscale data center is a different animal entirely — a high-value industrial occupancy with tens of thousands of gallons of stored diesel, lithium-ion battery rooms that behave like nothing an ARFF rig is built to fight, high-voltage substations, and a cooling plant that competes with my hydrants for water. Approving it against obstruction surfaces answers a question my teams were never asking. The question I ask is: when it goes bad, who fights it, with what, drawing water from where, and what am I *not* covering on the airfield while my apparatus is committed for the next twenty-two hours?

Compliance and competence are not the same thing. A data center can clear every FAA surface and still install a fire and hazmat problem my department cannot resource.

---

## 1. Key findings

- **ARFF is indexed for aircraft, not for a 100-megawatt building.** Part 139 sizes the fire department to the longest air-carrier aircraft normally operating — Index A through E — and to a three-minute response to the runway midpoint. Nothing in that index contemplates a structural-industrial occupancy with battery-room thermal runaway. A top-index (E) airport might field three ARFF vehicles and a shift crew that can be counted on one or two hands. That force cannot simultaneously cover the airfield and fight a data-hall fire. [Source: https://www.ecfr.gov/current/title-14/chapter-I/subchapter-G/part-139/subpart-D/section-139.315]

- **Lithium-ion battery fires are a category ARFF cannot extinguish with the agents it carries.** ARFF trucks carry AFFF/foam and dry chemical for hydrocarbon and three-dimensional fuel fires. Battery thermal runaway is self-sustaining, oxygen-generating, and reignites after knockdown; the only reliable tactic is massive, sustained water application or submersion. That is a municipal structural-fire problem measured in hours and thousands of gallons, not an ARFF problem measured in minutes and truck-borne agent. [Source: https://acerts.com/blogs/ups-systems/are-lithium-ups-batteries-a-fire-risk-the-truth-about-nfpa-855]

- **The controlling incident scenario is a battery/UPS fire, and it is a multi-hundred-firefighter, multi-day event.** The September 2025 fire at South Korea's National Information Resources Service data center in Daejeon burned for roughly 22 hours, required more than 200 firefighters and 60 fire engines, and knocked out 647 government IT systems. No airport ARFF force in the United States can generate that response from its own roster. Every unit on that fire came from mutual aid. [Source: https://www.koreaherald.com/article/10585058]

- **The data center imports a bulk fuel farm onto or beside the airfield.** NFPA 110 Level 1 standby power and Tier-III/IV designs drive 72–96 hours of on-site diesel. A single large facility can store from ~25,000 gallons up to 240,000+ gallons of diesel under NFPA 30 — a combustible-liquid inventory, with routine generator testing, sited near movement areas and fuel-vulnerable to the same events (aircraft overrun, fuel spill, vehicle strike) that already define airfield risk. [Source: https://www.powermag.com/understanding-diesel-fuel-storage-requirements/]

- **Cooling water and firefighting water draw from the same finite system.** Hyperscale facilities consume roughly 1–5 million gallons/day for cooling — the demand of a town of 10,000–50,000 people. On a constrained airport water system that competes directly with hydrant flow and fire-suppression supply. Whoever approves the data center is implicitly re-rating the airport's available fire flow, usually without telling the fire department. [Source: https://mostpolicyinitiative.org/science-note/data-center-water-use/]

- **Data centers are a documented source of electromagnetic interference — including near airports.** Power-quality distortion, harmonics, and high-frequency transients from switching supplies, VFDs, inverters, and cooling loads are recognized EMI sources. Airport public safety runs on land-mobile radio; degraded first-responder comms during an incident is a life-safety failure mode that a land-use review will never model. [Source: https://www.datacenterknowledge.com/physical-security/electromagnetic-interference-the-invisible-threat-to-data-center-uptime]

- **The stormwater and cooling footprint is also a wildlife-strike problem — a public-safety problem.** FAA AC 150/5200-33 treats stormwater retention and settling ponds as hazardous wildlife attractants and recommends no such attractant within 10,000 feet of an air-carrier runway end. Data-center-scale stormwater and any wet-cooling basins land squarely inside that concern. Bird strike is a flight-safety and emergency-response event, not just an environmental line item. [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf]

- **"Mutual aid will cover it" is an assumption, not a plan.** The entire off-airfield response to a data-center fire depends on host-jurisdiction structural companies arriving in force, knowing the site, and being able to draft water there. That is a signed-agreement question, a pre-plan question, an access-control (SIDA/AOA) question, and a water-supply question — all of which must be answered *before* approval, not discovered during the fire.

---

## 2. Evidence

### ARFF index and the three-minute standard
Under 14 CFR 139.315, the ARFF Index is set by the length of the longest air-carrier aircraft with an average of five or more daily departures (Index A: <90 ft; B: 90–<126; C: 126–<159; D: 159–<200; E: ≥200 ft), and 139.319 requires operational response — starting agent application at the midpoint of the most distant runway — within three minutes. The index dictates truck count and agent quantity, all tuned to aircraft fuel-fire suppression, not to structural or battery fires. [Source: https://www.ecfr.gov/current/title-14/chapter-I/subchapter-G/part-139/subpart-D/section-139.315] [Source: https://www.law.cornell.edu/cfr/text/14/139.319] Aircraft emergencies have "fundamentally different characteristics from structural firefighting" — jet fuel, time-critical evacuation, penetrating aircraft skin — which is precisely why an ARFF force is not a substitute for a structural fire department. [Source: https://www.aviatize.com/glossary/arff]

### Lithium-ion / BESS behavior and NFPA 855
NFPA 855 governs stationary energy-storage installation — separation, detection, ventilation, suppression, and thermal-runaway mitigation — and relies on UL 9540A large-scale propagation testing. The operative firefighting reality: "No portable fire extinguisher stops a lithium-ion thermal runaway… CO2… leaves the hot pack to reignite. A clean agent can knock down the open flame, but once it disperses, the still-hot pack reignites and continues to propagate cell to cell." [Source: https://acerts.com/blogs/ups-systems/are-lithium-ups-batteries-a-fire-risk-the-truth-about-nfpa-855] Data-center UPS is trending to lithium — projected ~38.5% of the data-center battery market by 2025, up from 15% in 2020 — so this failure mode is growing, not shrinking. [Source: https://www.networkworld.com/article/972090/data-center-fires-raise-concerns-about-lithium-ion-batteries.html]

### Daejeon 2025 — the controlling case study
The NIRS fire began during relocation of aging NMC lithium-ion battery packs; one pack entered thermal runaway in the basement. Firefighters reported that "the only effective ways to extinguish the batteries involved dousing them with large volumes of water or submerging them in tanks." Full extinguishment took ~22 hours, more than 200 firefighters, and 60 engines; 647 government systems went dark. [Source: https://www.koreaherald.com/article/10585058] [Source: https://www.koreaherald.com/article/10585116] Translate that to an airfield: a 22-hour commitment of regional structural fire resources, staged around a data center, while the airport still owes a 3-minute ARFF response to every departure.

### OVHcloud 2021 — total-loss precedent
The March 2021 OVHcloud Strasbourg fire, implicated in UPS systems, destroyed a data center, damaged others, affected ~65,000 customers, and cost the operator more than €105 million (less than half insured). It is the reference point for how completely and quickly these buildings burn. [Source: https://journal.uptimeinstitute.com/learning-from-the-ovhcloud-data-center-fire/]

### Diesel fuel inventory
NFPA 110 Level 1 requires minimum on-site fuel for 96 hours and a main tank at 133% of full-load consumption. Worked examples: a 3 MW generator burning ~200 gph needs ~25,536 gallons stored; a 10 MW Tier-IV plant needs ~240,000 liters (~63,400 gallons). [Source: https://www.powermag.com/understanding-diesel-fuel-storage-requirements/] [Source: https://generatordieselchina.com/data-center-generator-guide/] This is bulk combustible-liquid storage under NFPA 30, with recurring generator load-testing, placed in the airport environment.

### Water demand vs. fire flow
U.S. data centers consumed an estimated ~449 million gallons/day in 2021; large hyperscale sites use 1–5 million gallons/day each, and use peaks in warm months when residential demand also peaks. Localized draw "can stress water distribution infrastructure," and smaller utilities may not be able to upgrade. [Source: https://mostpolicyinitiative.org/science-note/data-center-water-use/] For a fire department, sustained cooling draw is a standing reduction in available fire flow unless the water system is explicitly re-engineered.

### EMI and first-responder communications
Data centers "generate electromagnetic interference through power quality distortion, harmonics, and high-frequency voltage transients from large electrical loads, switching power supplies, power inverters, variable frequency drives… and cooling systems," and can both emit and be sensitive near airports and towers. [Source: https://www.datacenterknowledge.com/physical-security/electromagnetic-interference-the-invisible-threat-to-data-center-uptime] The public-safety exposure is degraded LMR/dispatch performance precisely when incident traffic spikes.

### Wildlife / stormwater
FAA AC 150/5200-33 identifies stormwater and wastewater retention/settling ponds as hazardous wildlife attractants, recommends detention ponds be dry within 48 hours, engineered steep-sided/rip-rap/linear, and that new attractants be kept outside 10,000 ft of an air-carrier runway end. Data-center-scale stormwater and any evaporative-cooling basins fall inside this framework. [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf]

---

## 3. The public-safety case — for and against the thesis

**For the thesis (agrees with tightening review — my strong position).**
The thesis's core claim — that standard height/land-use review misses risks and the test should be affirmative evidence of compatibility — is exactly right from a first-responder seat, and the emergency-response dimension is its most defensible pillar. An obstruction-surface review does not ask whether the airport can suppress a battery-room fire, does not re-rate fire flow after cooling demand, does not model EMI to dispatch, and does not pre-plan a 22-hour mutual-aid commitment on airport property. Those are the failure modes that actually kill people and shut airfields, and they are invisible to the current test. If the thesis wins, my departments get the one thing a compliance review never gives them: a seat at approval, and a requirement that the developer prove fire, water, comms, and access are solved before the ribbon-cutting.

**Against the thesis (the honest counter).**
Two arguments cut the other way, and I won't pretend they don't. First, *most of these risks are mitigable through design and code, not location.* NFPA 855 battery separation and large-scale-tested cells, dedicated fire-water and separate hydrant supply, on-site foam/water reserves, bunded fuel storage, EMI shielding, and dry-detention stormwater are all engineerable. A rigorously code-built data center with a funded on-site fire brigade and a hardened water supply may impose *less* incremental public-safety load than a legacy cargo or MRO tenant already on the field. Second, *the airport does not have to own the fire.* If the facility is structured with its own suppression, its own water, its own private fire service, and an ironclad mutual-aid/pre-plan package, the marginal draw on ARFF can be bounded. The thesis risks proving too much — every large industrial tenant carries fire load; singling out data centers is defensible only if the review is genuinely evidence-based rather than a veto dressed as a study.

Where I come down: the risks are real and the current review misses them, but the correct output is not "no" — it is a mandatory public-safety compatibility study with the fire department holding a hard gate on fire flow, battery suppression, fuel siting, and a signed, pre-planned mutual-aid concept of operations. Compatibility, proven by evidence, before approval.

---

## 4. Operational realities a strategist can deploy

1. **The 3-minute clock and the 22-hour fire are incompatible commitments.** Part 139 obligates a 3-minute ARFF response to the runway midpoint (139.319), yet the controlling data-center scenario — Daejeon 2025 — consumed 200+ firefighters and 60 engines for ~22 hours. An airport cannot honor both from one roster. Any approval must name the outside force that carries the building fire so ARFF stays free to cover the airfield. [Source: https://www.law.cornell.edu/cfr/text/14/139.319] [Source: https://www.koreaherald.com/article/10585058]

2. **ARFF agents don't stop battery fires — full stop.** The fire service's own finding after these events is that lithium-ion thermal runaway needs "large volumes of water or submerging… in tanks," not the foam/dry-chem an ARFF truck carries. Approving a battery-dense occupancy without a water-based, structural-scale suppression plan is approving a fire the airport department is chemically unequipped to extinguish. [Source: https://www.koreaherald.com/article/10585116]

3. **You are storing 25,000–240,000 gallons of diesel next to the runway.** NFPA 110's 96-hour / 133% rule turns "backup power" into a bulk NFPA 30 combustible-liquid farm with routine generator testing in the airfield environment. Site it, bund it, and separate it as such — or it becomes a second fuel hazard layered onto the one the airport already manages. [Source: https://www.powermag.com/understanding-diesel-fuel-storage-requirements/]

4. **Cooling water is fire water.** A 1–5 MGD cooling draw silently reduces available fire flow. The fire department must re-run hydraulic fire-flow calculations for the *post*-data-center water system before approval — including a separate, protected fire-suppression supply for the facility itself. [Source: https://mostpolicyinitiative.org/science-note/data-center-water-use/]

5. **A signed mutual-aid agreement is not a response.** What shows up at 3 a.m. depends on pre-plans, site familiarization, SIDA/AOA access for outside companies, drafting points, and interoperable radios that survive the facility's own EMI. The deliverable to demand is a joint pre-incident plan and a live exercise with the host jurisdiction — not a memorandum in a binder. [Source: https://www.datacenterknowledge.com/physical-security/electromagnetic-interference-the-invisible-threat-to-data-center-uptime]

---

## Bottom line

Data centers don't just occupy airport real estate — they install an industrial fire, fuel, water, and communications load that the airport's federally indexed public-safety apparatus was never sized to carry. The current land-use test asks whether the building clears the airspace. The question my chair asks is whether the airport can respond when the building fails, and today that question is not being asked at all. The thesis is right to demand affirmative evidence of compatibility. From public safety, that evidence package is specific and non-negotiable: a battery-fire suppression concept, a re-rated and separately supplied fire-water system, code-sited fuel storage, EMI-hardened first-responder comms, and a rehearsed mutual-aid concept of operations — all proven before, not after, the first shovel.
