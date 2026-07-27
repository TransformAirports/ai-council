# Operations-Analyst Brief — Data Center in the RWY 1L/19R Approach–Departure Surface at IAD

**Question I was asked to strengthen or disprove:** Should MWAA build a data center on the parcel inside the RWY 19R departure and RWY 1L approach surfaces at Washington Dulles (IAD)? The author says no. My job is to test which of his concerns are load-bearing from an operations/airspace/throughput standpoint, arm them with primary sources and numbers, and flag where the argument is weakest so it is not overstated.

**Bottom line for the writer:** The author's strongest ground is not "land use" in the abstract — it is the *thermal-plume airspace hazard* and the *foreclosure of runway capacity*, both of which convert a soft planning objection into a quantifiable, FAA-recognized operational problem. His wildlife/stormwater point is correct but should cite the current AC. His weakest ground is treating the plume hazard as automatically disqualifying under U.S. rule — it is not; it triggers a study. Frame it as "require the analysis before you can approve," not "it is already proven unsafe."

---

## 1. The single strongest mechanism: thermal-plume turbulence in the approach/departure corridor

This is the argument's best operational anchor because it is measurable and because a data center is an unusually plume-intensive use (continuous heat rejection from cooling systems plus periodic on-site/backup power generation).

- The FAA's own **Aeronautical Information Manual (AIM) 7-6-16** states that high-temperature exhaust plumes "can cause significant air disturbances such as turbulence and vertical shear," that these effects "can extend to heights of over 1,000 feet above the height of the top of the stack or cooling tower," and that they are "most critical during low altitude flight in calm and cold air, especially in and around approach and departure corridors or airport traffic areas." [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html] This is exactly the flight regime over the RWY 1L threshold and off the RWY 19R end.
- There is an internationally used quantitative threshold the writer can cite: aviation regulators treat a **critical average vertical plume velocity above 4.3 m/s** as a potential hazard to aircraft. Australia's CASA codifies this (Part 139.370 / AC 139-05): if a source's vertical exit velocity is below 4.3 m/s no further action is required; above it, a plume-rise assessment is required. [Source: https://www.jandakotairport.com.au/images/files/ControlledActivity/CASA%20AC139-05%20Plume%20Rise%20Assessments.pdf]
- The FAA has taken this seriously enough to build tooling: its Airport Obstruction Standards Committee (AOSC) tasked MITRE to develop an **Exhaust Plume Analyzer**, and the FAA published a *Technical Guidance Assessment Tool for Thermal Exhaust Plume Impact* for use around federally obligated airports. [Source: https://www.faa.gov/sites/faa.gov/files/airports/environmental/land_use/Technical-Guidance-Assessment-Tool-Thermal-Exhaust-Plume-Impact.pdf]

**Honest limit (give this to the writer so red-team can't blindside them):** The U.S. has *no codified numeric plume regulation*. The 4.3 m/s figure is Australian/international practice; the FAA route is the AIM advisory plus a case-by-case obstruction evaluation. So the defensible claim is procedural: *this parcel's plume profile must be modeled and cleared before it can be approved, and a data center with on-site generation is precisely the kind of source that fails a screen.* Do not assert the hazard as already proven — assert that MWAA cannot know it is safe without the study the proposal skipped.

**Data-center-specific reinforcement:** Data centers almost universally rely on diesel backup generators, run 50–150 test-hours/year each; a single 2.5 MW unit emits roughly 1.2 metric tons of NOx and 0.05 t of particulates annually during testing. [Source: https://insideclimatenews.org/news/12112025/data-center-diesel-generators-noise-pollution/] A campus can hold dozens of such units — a concentrated, elevated thermal/exhaust source directly under the approach.

## 2. Second strongest mechanism: this parcel is strategic runway land, and a data center is close to irreversible

The author's "protect the land for future capacity" point is stronger than it reads, because of *what* a data center is.

- IAD is in demonstrable growth. It set a 19-year record in 2024 at **27.25 million passengers, 10.38 million of them international**, even as aircraft movements fell by ~2,000 year-over-year — growth is coming through larger widebodies, which is exactly the traffic that eventually forces new runway geometry. [Source: https://simpleflying.com/washington-dc-airport-new-records-2024/]
- MWAA's 2025 master plan explicitly envisions growth to **90 million annual passengers** and protects for a **future fifth runway (12R/30L)**. [Source: https://www.ffxnow.com/2025/07/17/new-master-plan-for-dulles-airport-envisions-growth-to-90-million-annual-passengers/] RWY 1L/19R itself is the newest north-south runway, opened 2008 at 9,400 ft. [Source: https://www.flydulles.com/d2-projects-fourth-runway] Land in its approach/departure surface is not spare land.
- A data center is effectively permanent: nine-figure sunk capital, dedicated power interconnect, and fiber routes make it far harder to relocate than the surface parking, cargo, or warehousing that usually occupy non-aeronautical parcels. Sterilizing this surface with a 30–50-year asset forecloses runway-extension and taxiway geometry the master plan has not yet foreclosed. The relevant planning horizon (50 years) exceeds the data center's useful life *and* the term of most land agreements.

## 3. The RPZ / obstruction-evaluation trigger the proposal appears to have skipped

- Under FAA's **2012 interim RPZ land-use guidance**, any proposal that would place *buildings/structures, above-ground utilities, fuel/hazmat storage, or parking* inside a Runway Protection Zone requires the ADO/Region to consult the **National Airport Planning and Environmental Division** and to document alternatives that avoid or mitigate the encroachment. [Source: https://crp.trb.org/acrpwebresource13/faa-interim-guidance-on-land-uses-within-a-runway-protection-zone/] A data center is all of those things at once. If any part of the footprint touches the RPZ, this is not a discretionary local call.
- Separately, FAA obstruction evaluation (7460/JO 7400.2, PHAM Ch. 6) holds that a structure has a *substantial adverse effect* if it "causes electromagnetic interference to the operation of an air navigation or radar/surveillance facility or the signal used by aircraft." [Source: https://www.faa.gov/air_traffic/publications/atpubs/pham_html/chap6_section_3.html] This validates the author's EMI concern as a recognized FAA evaluation criterion, and — critically — the proposal has *not* been through the 7460 process with the ADO. That procedural gap is itself a defensible objection.

## 4. The wildlife/stormwater point is correct — but update the citation

The author cites AC 150/5200-33B. **That AC has been cancelled and superseded by AC 150/5200-33C.** Using the dead reference is an easy credibility hit; fix it.

- The current standard: separate hazardous-wildlife attractants by **5,000 ft for piston-aircraft airports, 10,000 ft for turbine-aircraft airports** (IAD is turbine — use 10,000 ft), and **5 statute miles** where the attractant could cause hazardous wildlife movement into approach/departure airspace. [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf]
- The specific rule the writer wants: **new water impoundments of ¼ acre or larger should not be allowed within an approach corridor or within 5,000 ft of a runway end**, and stormwater facilities that must exist near air operations should be designed to be steep-sided, netted, or covered so they do not hold standing water attractive to birds. A proposed retention pond next to the data center, inside the approach, is a textbook violation to flag.

## 5. Grant assurances — keep them, they are the enforcement teeth

The author's list is sound. The two that carry the most operational weight and are hardest for a revenue-minded proponent to dismiss:
- **Assurance #20 (Hazard Removal and Mitigation)** — obligates the sponsor to prevent the *establishment* of future airport hazards. Building a plume source and wildlife attractant under the approach is establishing one.
- **Assurance #21 (Compatible Land Use)** — restricts land in the immediate vicinity to uses compatible with landing and takeoff.
These convert the planning argument into a federal-obligation argument, which is the level MWAA's board and bond counsel respond to.

---

## Counter-case (steelman — the writer must answer these or lose to red-team)

1. **"Airports are supposed to monetize non-aero land."** True. FAA permits non-aeronautical development on airport property where it does not interfere with aeronautical use and revenue stays on-airport. Data centers are a hot revenue play precisely because airports have flat, secured land near power and fiber. The rebuttal is not "no non-aero" — it is "not *this* parcel," because of the approach-surface location, not the land use per se.
2. **"If it doesn't penetrate the Part 77 surfaces and clears a 7460 study, FAA will issue 'No Hazard.'"** Correct — height/penetration is the codified trigger, and a low-rise data center may clear it. The author's argument must therefore lean on the *non-height* effects (plume, EMI, wildlife, RPZ, capacity foreclosure), which are real but require studies the proposal hasn't done. That's why "require the analysis first" is the winning frame, not "it's obviously unsafe."
3. **"Near-term capacity pressure is soft — movements are *falling* at IAD."** Also true (down ~2,000 in 2024). This weakens urgency. Answer it head-on: land decisions are 50-year decisions; the master plan protects a fifth runway; you do not sell the option on future geometry to capture near-term rent.
4. **"Data centers already cluster next to IAD (Loudoun/Ashburn is the world's densest) without aviation incident."** True, but those are *off-airport, outside the approach surface.* Proximity to the airport is not the issue; siting inside the departure/approach surface is.

---

## Verbatim data points / quotes a strategist can lift

- **FAA AIM 7-6-16:** exhaust-plume turbulence "can extend to heights of over 1,000 feet above the height of the top of the stack or cooling tower," and is "most critical during low altitude flight in calm and cold air, especially in and around approach and departure corridors or airport traffic areas."
- **CASA plume standard (international benchmark):** vertical plume velocities "in excess of 4.3 m/s" are treated as "a potential hazard to aircraft operations."
- **AC 150/5200-33C:** hazardous-wildlife attractants must be separated **10,000 ft** from turbine-aircraft airports; no new water impoundment ≥ ¼ acre within an approach corridor or within 5,000 ft of a runway end.
- **IAD scale/trajectory:** 27.25 M passengers in 2024 (19-year record; 10.38 M international); 2025 master plan targets 90 M and protects a fifth runway (12R/30L).
- **FAA obstruction criterion (7460):** a structure has a "substantial adverse effect" if it "causes electromagnetic interference to the operation of an air navigation or radar/surveillance facility."

## What I'd tell the writer to change in the original

1. Swap **AC 150/5200-33B → 33C** (the cited AC is cancelled).
2. Lead with the **plume hazard as a required-study trigger**, not a settled fact — cite AIM 7-6-16 and the 4.3 m/s benchmark, and note the proposal has done neither the plume assessment nor the 7460 evaluation.
3. Add the **RPZ interim-guidance consultation requirement** as the procedural hook: if the footprint touches the RPZ, FAA HQ consultation is mandatory, and the local 2025 land-use review does not substitute for it.
4. Confront the **revenue counter-argument and the falling-movements fact** explicitly; win on "wrong parcel / 50-year option," not "no data centers."
