# Operations-Analyst Brief: Data Centers Near Airfields — Where the Throughput Risk Actually Lives

**Run:** Data Centers at Airports: Airside Risks
**Lens:** Airport operational performance — airfield throughput, approach/departure integrity, low-visibility operations, wildlife, and emergency-response load. This brief deliberately does not repeat the economics, engineering, or regulatory framing that other Stage 1 agents own. My question is narrower and operational: *if a data center is built near a flight path, what breaks in the daily and future running of the airfield, under which operating scenario, and can operations manage around it?*

A discipline note that the run file demands and that most of the popular coverage fails: **a visible plume is not turbulence, and turbulence is not exhaust.** These are three separate hazard mechanisms with three different controlling scenarios and three different mitigations. Conflating them produces both false alarms and missed risks. I keep them separate throughout.

---

## 1. Key Findings

1. **The turbulence hazard is a vertical-velocity problem, not a "tall building" problem.** The relevant international threshold — CASA's — treats a plume with a critical vertical velocity above **4.3 m/s** at the height an aircraft would encounter it as a potential hazard, with turbulence graded Light (1.5–6.1 m/s), Moderate (6.1–10.6 m/s), and Severe (10.6–15.2 m/s) [Source: https://www.casa.gov.au/sites/default/files/2023-03/advisory-circular-139e-02-plume-rise-assessments.PDF]. A data center that clears every Part 77 obstruction surface can still inject a >4.3 m/s buoyant column into a final-approach segment. Height review and turbulence review are not the same test.

2. **This is not hypothetical — it is already an active airfield conflict.** At **The Eastern Iowa Airport (CID)**, Google requested a temporary certificate of occupancy for a completed data center building while the airport evaluates mitigation, because **"heat and steam plumes from the data center … could interfere with landings and takeoffs"** [Source: https://www.kcrg.com/2026/06/22/cedar-rapids-set-agreement-with-google-regarding-data-center-impacts/]. A finished building is negotiating its way to occupancy over a plume-vs-runway dispute. That is the operational failure mode this run is about, happening in real time.

3. **The FAA already treats thermal exhaust plumes as presumptively incompatible near airports** — not merely as obstructions. FAA technical guidance frames significant thermal plumes in approach/departure corridors and the traffic pattern as a hazard to aircraft in critical phases of flight, and points assessors to the MITRE Exhaust-Plume-Analyzer to evaluate impact [Source: https://www.faa.gov/sites/faa.gov/files/airports/environmental/land_use/Technical-Guidance-Assessment-Tool-Thermal-Exhaust-Plume-Impact.pdf]. The regulatory vocabulary exists; what is missing is a data-center-specific screening trigger.

4. **The controlling scenario is not "normal operation."** For turbulence it is **peak sensible-heat rejection** (hottest day, full IT load, dry-cooler/free-air mode). For visibility obscuration it is **cold, humid, high-load evaporative operation**, which maximizes the visible condensation plume in an otherwise VMC sky. For exhaust and emergency load it is **prolonged utility outage with the full generator plant running** — a scenario that often coincides with the regional weather that already stresses the airfield. Any compatibility study benchmarked to average operation is measuring the wrong day.

5. **Backup generation is a fleet, not a box.** Virginia data centers hold permits for more than **10,500 diesel generators totaling roughly 27 GW** of backup capacity, and a single large campus can field dozens [Source: https://virginiamercury.com/2026/02/17/lawmakers-debate-how-to-regulate-data-centers-diesel-backup-generators/]. Even at "less than an hour per week" of testing, VCU researchers put data-center generator emissions on par with power-plant output regionally [Source: https://news.vcu.edu/article/northern-virginia-data-center-air-pollution-rivals-power-plant-emissions]. Near a runway, the operational concern is not annual tonnage — it is the coincident hot-exhaust plume and visible smoke of many units starting at once during an outage.

6. **The wildlife vector is the most quantifiable and the most underappreciated.** FAA guidance directs managers to eliminate hazardous wildlife attractants within **10,000 ft (≈3.0 km)** of the air operations area for turbine airports, and stormwater impoundments are specifically flagged as attractants [Source: https://www.faa.gov/airports/airport_safety/wildlife/management]. Roughly **95% of reported bird strikes occur below ~1,067 m AGL** — exactly the approach/departure band [Source: https://www.sciencedirect.com/science/article/abs/pii/S0169204613001138]. A data center's warm stormwater ponds and large flat roofs are textbook attractants inside that ring.

7. **Glare has a settled regulatory analog that data centers currently escape.** The FAA's solar policy exists precisely because reflective glass can produce glint/glare causing "ocular impact" to tower controllers and pilots, and it mandates a Sandia glare-hazard analysis before a 7460-1 filing [Source: https://www.federalregister.gov/documents/2021/05/11/2021-09862/federal-aviation-administration-policy-review-of-solar-energy-system-projects-on-federally-obligated]. Data centers routinely carry large curtain-wall glass, metal roofing, and rooftop solar — the same reflective surfaces — but face no equivalent mandatory glare screen unless the airport imposes one.

8. **The airfield inherits a new emergency-response tenant it did not staff for.** Lithium-ion battery (BESS) fires at data centers produce hydrogen-fluoride off-gas, resist suppression, and reignite; standard doctrine is contain-and-monitor, not interior attack [Source: https://www.iafc.org/topics-and-tools/resources/resource/recommended-fire-department-response-to-energy-storage-systems-(ess)-part-1]. An ARFF index built to a fuel-fire standard is not resourced for a multi-hour thermal-runaway event next to the movement area — a latent draw on the same crews that must keep the runway open.

---

## 2. Evidence

### 2.1 The turbulence mechanism — distinct from the visible plume

Buoyant rising air is the actual flight hazard. A steady vertical gust displaces the wing and can roll or pitch the aircraft during the low-energy, low-altitude approach and departure regime where recovery margin is thinnest. The MITRE Exhaust Plume Analyzer models this directly: it pairs a plume-rise model with **aircraft-response models that compute the vertical gust required to cause aircraft upset — defined as a 45° bank** via the Houbolt roll model [Source: https://www.techbriefs.com/component/content/article/33600-exhaust-plume-analyzer]. CASA's framework, the most explicit publicly, sets the assessment trigger at a **4.3 m/s** critical vertical velocity at aircraft-encounter height and grades severity upward from there [Source: https://www.casa.gov.au/sites/default/files/2023-03/advisory-circular-139e-02-plume-rise-assessments.PDF].

Two honesty caveats a skeptical reader will demand:
- **The 4.3 m/s figure is CASA's, not an FAA-published bright line.** The FAA uses the MITRE tool and treats significant plumes as incompatible but does not publish a single equivalent numeric threshold in its land-use guidance [Source: https://www.aviationairportdevelopmentlaw.com/2012/11/articles/federal-aviation-administration-faa/faa-finally-issues-guidance-on-plume-hazards-to-aircraft-from-power-plants-or-does-it/]. A U.S. screening framework has to adopt or reference a threshold; there isn't a domestic default to point at.
- **The published plume literature is overwhelmingly about power plants and cooling towers, not data centers.** Data-center heat flux per unit area is lower than a power-plant stack, which cuts both ways: lower peak buoyancy per source, but a very large, distributed roof-and-coolant footprint rather than a single point stack. The dispersion geometry is genuinely different and under-studied — an evidence gap, not an all-clear.

### 2.2 The visible plume — a low-visibility problem in a clear sky

Separate mechanism. Evaporative and hybrid cooling reject heat as warm, saturated air that condenses into a visible plume in cold, humid conditions. This is not turbulence; it is **obscuration and heat-haze refraction**. Operationally it degrades the visual segment: it can sit across a visual approach, obscure a PAPI/runway-end sightline, or shimmer the visual picture on a hot day. The FAA's own airman guidance warns pilots to avoid flight in the vicinity of exhaust and smoke because of both turbulence and visibility [Source: https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap7_section_4.html]. The controlling scenario here is the opposite weather to the turbulence case — cold and humid, not hot and dry — which is why a single "worst case" does not exist. The study must run both envelopes.

### 2.3 The exhaust/generation scenario — the coincident-failure case

Backup generators change the risk in three ways at once: hot buoyant exhaust (a turbulence and thermal source), visible smoke (obscuration), and the operational reality that **prolonged emergency generation tends to coincide with severe weather or grid stress** — precisely when the airfield is already degraded. The scale is not trivial: 10,500+ permitted generators (~27 GW) across Virginia and campuses running dozens of units [Source: https://virginiamercury.com/2026/02/17/lawmakers-debate-how-to-regulate-data-centers-diesel-backup-generators/], with regional emissions rivaling a power plant even at sparse runtime [Source: https://news.vcu.edu/article/northern-virginia-data-center-air-pollution-rivals-power-plant-emissions]. Newer state rules push Tier 4 / SCR controls, which cut chemistry but not the plume's thermal buoyancy or the visible smoke of a simultaneous cold-start [Source: https://www.datacenterknowledge.com/build-design/virginia-deq-revises-data-center-generator-rules-as-community-pushback-builds]. **This is the controlling scenario for the combined hazard** and the one a compatibility study is most likely to under-model, because it is rare, correlated with bad weather, and never the day the consultant picks.

### 2.4 Wildlife — the most defensible operational objection

This is where operations analysts have the firmest ground. FAA policy sets separation distances (5,000 ft piston / **10,000 ft turbine**, plus a 5-mile conical protection zone) for attractants and names stormwater management facilities explicitly [Source: https://www.faa.gov/airports/airport_safety/wildlife/management]. Peer-reviewed work finds stormwater impoundments near airports are used by hazard species and that **95% of strikes occur in the low-altitude approach/departure band** [Source: https://www.sciencedirect.com/science/article/abs/pii/S0169204613001138], and separately argues wildlife is a "missing component of land-use planning for airports" [Source: https://www.sciencedirect.com/science/article/abs/pii/S016920460900142X]. A hyperscale campus adds two attractants inside the ring: large warm stormwater basins (open water + thermal refuge in winter) and expansive flat roofs (loafing/nesting). Unlike plume turbulence, this risk is quantifiable with existing strike data and existing FAA distance standards — it should be the anchor of any screening tool.

### 2.5 Glare, lighting, and EMI — borrowed frameworks

The FAA already regulates reflective glare for a reason it has itself validated: glint/glare causes ocular impact to tower personnel and pilots, mitigated via the Sandia Solar Glare Hazard Analysis Tool before a 7460-1 filing [Source: https://www.federalregister.gov/documents/2021/05/11/2021-09862/federal-aviation-administration-policy-review-of-solar-energy-system-projects-on-federally-obligated]. Data centers present the same surfaces (curtain-wall glass, metal roof, rooftop PV) and add **security and obstruction lighting** that can wash out the visual approach at night, plus dense switchgear and RF that raise EMI questions for nav/comm. The Inyokern case shows an airport enumerating exactly this bundle — **visual approaches and departures, thermal plumes/heat exhaust, electromagnetic interference, lighting and glare, wildlife, and power/transmission impacts** — as the areas requiring analysis before it would accept the project [Source: https://www.kget.com/news/environment/inyokern-airport-asks-for-aviation-impact-analysis-as-possible-data-center-looms/]. The frameworks exist in fragments; no single instrument bundles them for data centers.

### 2.6 Emergency-response load — the hidden operational tenant

A large data center sited on or adjacent to airport property becomes an ARFF and mutual-aid dependency. BESS and lithium-ion fires demand containment-and-monitor tactics, produce toxic HF off-gas, and can burn or reignite for hours [Source: https://www.iafc.org/topics-and-tools/resources/resource/recommended-fire-department-response-to-energy-storage-systems-(ess)-part-1]; the Hillsboro data-center BESS fire is a documented illustration of the scale and duration [Source: https://eticaag.com/hillsboro-data-center-fire-bess-safety/]. The operational point: an airport's ARFF index is dimensioned for aircraft fuel fires and a mandated runway-response time, **not** for a sustained hazmat event on the fence line. A prolonged data-center incident can pull the exact crews and command capacity that keep the movement area open — a throughput risk that never appears in a plume model.

### 2.7 Documented near-airfield examples

- **Eastern Iowa (CID) / Google:** finished building held on a temporary CO while heat/steam-plume impacts on takeoffs and landings are mitigated; the airport commission had already been buying contiguous land "for continued protection of the airport operation and future growth" [Source: https://www.kcrg.com/2026/06/22/cedar-rapids-set-agreement-with-google-regarding-data-center-impacts/] [Source: https://www.thegazette.com/local-government/cedar-rapids-city-council-approves-annexation-of-land-near-airport/].
- **Inyokern (IYK):** airport formally requested an aviation-impact analysis covering plumes, EMI, glare, lighting, and wildlife before a proposed data center [Source: https://www.kget.com/news/environment/inyokern-airport-asks-for-aviation-impact-analysis-as-possible-data-center-looms/].
- **Manassas Regional (HEF):** ~22 acres rezoned for a data center near the airport amid contested land-use debate, with a runway-extension program in the same master plan — the collision of data-center demand and **future airfield capacity** on the same parcels [Source: https://www.princewilliamtimes.com/news/supervisors-approve-data-centers-near-manassas-apartments-airport/article_ed4998fe-ac12-43ad-baf3-ec78c37d9895.html].

The pattern: airports are being asked to approve these on ordinary land-use timelines, and the airfield-specific analysis is being invented case-by-case, after the building is designed or built.

---

## 3. Counterexamples — where operations could NOT solve it and siting/relocation is the right answer

Intellectual honesty requires naming where the operational toolkit runs out. My general operational bias is that most airfield constraints are coordination problems, not concrete problems — but data-center plume and wildlife risk contains a genuinely location-locked residue:

- **A buoyant plume in the final-approach segment cannot be metered away.** Departure metering, sequencing, or A-CDM-style coordination — the moves that unlock "hidden capacity" elsewhere — do nothing to a column of rising air. If the >4.3 m/s vertical velocity intersects the approach at flare-relevant height, the only real mitigations are **source relocation, cooling-technology change (closed-loop/air-cooled to kill the plume), or a permanent procedure change that sterilizes the affected approach** — which is itself a capacity loss. This is the case where infrastructure/siting, not operations, is the correct answer.
- **Wildlife attractants inside the FAA separation ring are a design fact, not a management program.** Harassment and habitat management reduce but do not eliminate a standing warm-water attractant 8,000 ft off the threshold. Where the stormwater regime cannot be made unattractive (sub-surface detention, no open water, no thermal refuge), the honest answer is that the pond — or the campus — is in the wrong place.
- **A single-approach airport has no operational slack to absorb any of this.** At a multi-runway hub you can shift flows; at a single-runway field (Inyokern, many regionals) a plume, glare source, or sterilized segment on the one approach is a hard capacity hit with no coordination workaround.

These are the cases where "just manage it operationally" is wrong and the run's thesis — demand independent evidence of compatibility *before* approval — is vindicated.

---

## 4. Direct quotes / data points for the strategist (usable verbatim)

1. **"Heat and steam plumes from the data center … could interfere with landings and takeoffs at the airport"** — the operative concern in the Eastern Iowa Airport/Google occupancy negotiation, June 2026 [Source: https://www.kcrg.com/2026/06/22/cedar-rapids-set-agreement-with-google-regarding-data-center-impacts/]. *Use to prove this is a live airfield conflict, not a theoretical one.*

2. **CASA grades plume turbulence Light (1.5–6.1 m/s), Moderate (6.1–10.6 m/s), Severe (10.6–15.2 m/s), with 4.3 m/s critical vertical velocity as the assessment trigger** [Source: https://www.casa.gov.au/sites/default/files/2023-03/advisory-circular-139e-02-plume-rise-assessments.PDF]. *Use as the concrete number MWAA can adopt as a screening threshold — while noting it is CASA, not FAA.*

3. **The MITRE Exhaust Plume Analyzer defines aircraft upset as a 45° bank and solves for the vertical gust that produces it (Houbolt roll model)** [Source: https://www.techbriefs.com/component/content/article/33600-exhaust-plume-analyzer]. *Use to show a validated, FAA-referenced tool already exists — the gap is triggering its use for data centers.*

4. **Over 10,500 permitted diesel generators (~27 GW of backup) sit at Virginia data centers; emissions rival a power plant even at "less than an hour per week" of testing** [Source: https://virginiamercury.com/2026/02/17/lawmakers-debate-how-to-regulate-data-centers-diesel-backup-generators/] [Source: https://news.vcu.edu/article/northern-virginia-data-center-air-pollution-rivals-power-plant-emissions]. *Use to size the emergency-generation scenario the compatibility study must model.*

5. **FAA wildlife guidance: eliminate hazardous attractants within 10,000 ft of the AOA for turbine airports; ~95% of bird strikes occur below ~1,067 m AGL — the approach/departure band; stormwater impoundments are named attractants** [Source: https://www.faa.gov/airports/airport_safety/wildlife/management] [Source: https://www.sciencedirect.com/science/article/abs/pii/S0169204613001138]. *Use as the most quantifiable, hardest-to-rebut operational objection.*

---

## 5. Operational bottom line for the MWAA screen

The controlling operational insight: **height review passes the building; it does not test the air above and around it.** A data center can clear every Part 77 surface and still push a >4.3 m/s buoyant column, a winter obscuration plume, a coincident generator smoke event, a warm attractant pond, a glare source, and a multi-hour hazmat load into the approach environment. Each has a *different* controlling weather/operating scenario, so a single "worst case" study is disqualifying on its face.

The operational studies MWAA should require before approving a data center near aviation operations:
1. **Plume/turbulence assessment** via MITRE Exhaust Plume Analyzer at peak sensible-heat rejection, reported against an adopted vertical-velocity threshold (CASA's 4.3 m/s as the reference), evaluated at aircraft-encounter height on every affected approach/departure and pattern segment.
2. **Visible-plume/obscuration modeling** under the cold-humid envelope, including PAPI and visual-segment sightlines.
3. **Generator scenario** modeling prolonged full-plant emergency generation coincident with adverse weather — thermal plume, visible smoke, and ingestion path — not annual-average emissions.
4. **Wildlife hazard assessment** against FAA separation distances, specifically the stormwater regime and roof design, with a no-open-water default.
5. **Glint/glare (Sandia) analysis** for all reflective surfaces plus a night-lighting/visual-approach conflict review.
6. **EMI study** for nav/comm and surveillance.
7. **ARFF/EOC load assessment** for BESS/lithium-ion incident duration and the draw on runway-response capability.

And the throughput point that unifies them for an executive audience: the test is not whether the building fits today's obstruction surfaces, but whether it **forecloses future airfield capacity** — a sterilized approach segment, a lost runway extension corridor, or a permanent wildlife liability is a capacity decision made by a real-estate reviewer who never priced it.

---

*Evidence gaps I am flagging honestly for Stage 2:* (a) no FAA-published numeric plume-velocity threshold for U.S. use — the CASA number is a borrowed reference; (b) the plume-turbulence literature is power-plant/cooling-tower-derived, and data-center-specific dispersion (large distributed footprint, lower per-source flux) is genuinely under-studied; (c) most airport-adjacent data-center cases (CID, Inyokern, Manassas) are mid-process, so operating-history-with-impacts data does not yet exist. The absence of a smoking gun is not evidence of safety; it is evidence the compatibility question is being answered after the concrete is poured.
