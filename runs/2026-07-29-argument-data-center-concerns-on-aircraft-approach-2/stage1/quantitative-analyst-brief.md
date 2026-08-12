# Quantitative Analysis Brief: Data Center Concerns on Aircraft Approach
**Airport:** Washington Dulles International Airport (IAD / KIAD)  
**Analyst:** Quantitative Analyst, Transform Airports AI Council  
**Date:** 2026-07-29  
**Runway Subject:** RWY 01L/19R  

---

## Purpose

This brief quantifies and anchors the regulatory citations in Jen Kandel's memo with specific thresholds, dimensional data, and statutory language. The argument is structurally sound. The gaps are specificity and precedent — both of which exist in the regulatory record. The writer should use these anchors to replace hedged language ("I believe we are at risk") with precise citations.

---

## 1. What the Runway Actually Is

RWY 01L/19R at IAD is 9,400 ft × 150 ft, concrete, ILS/DME at both ends, with an ALSF-2 approach lighting system — the highest-intensity, highest-criticality approach light configuration in FAA inventory. It serves precision Category I, II, and III approaches. These are the operations most sensitive to visual, electromagnetic, and atmospheric interference at low altitude.

**Source:** FlightAware Runway Database, KIAD RWY 01L/19R (accessed 2026-07-29).

---

## 2. The Approach Surface Is Enormous

Under 14 CFR § 77.19, a precision instrument runway (ILS) generates a protected approach surface with these dimensions:

| Segment | Length from Threshold | Slope | Max Structure Height at Far End |
|---|---|---|---|
| First | 0–10,000 ft | 50:1 (2.0%) | 200 ft above threshold elevation |
| Second | 10,000–50,000 ft | 40:1 (2.5%) | ~1,200 ft above threshold elevation |
| **Total** | **50,000 ft (9.47 miles)** | — | — |

The inner edge of this surface begins at the runway end, 1,000 ft wide. The surface is not just an obstacle-clearance envelope — it defines land that should remain uncommitted for future aeronautical use. A facility located within 2,500 ft of the threshold (inside the RPZ) sits where the 50:1 slope allows only 50 ft of structure height and where the protected corridor is at its most critical.

**Source:** 14 CFR § 77.19, Civil Airport Imaginary Surfaces; Cornell LII (accessed 2026-07-29).

---

## 3. The RPZ Itself Is 79 Acres of the Most Strategic Land on the Property

For a precision instrument runway, the Runway Protection Zone (RPZ) is 1,000 ft wide at the inner edge, 1,750 ft wide at the outer edge, and 2,500 ft long — a trapezoid of approximately 3.44 million sq ft (78.9 acres). Where the airport owner controls this land, FAA AC 150/5300-13B and AC 150/5190-4B prohibit uses that cause congregation of people or introduce incompatible development. The site described in the memo is within or immediately adjacent to this zone.

**Formula:** Trapezoid area = 0.5 × (1,000 + 1,750) × 2,500 = 3,437,500 sq ft = 78.9 acres  
**Source:** FAA AC 150/5300-13B Airport Design (March 2022); FAA AC 150/5190-4B Airport Land Use Compatibility Planning.

---

## 4. The Stormwater Pond Alone Is a Quantified Violation

FAA AC 150/5200-33B (Hazardous Wildlife Attractants On or Near Airports) explicitly lists stormwater management facilities as hazardous wildlife attractants. The standard for airports serving turbojet aircraft: **no hazardous attractant within 10,000 ft of a runway end.** The proposed stormwater retention facility is inside the RPZ — less than 2,500 ft from the threshold — placing it 7,500 ft inside the prohibited zone.

This is the argument's clearest quantitative anchor. It is not a discretionary concern — it is a specific dimensional standard the proposal fails by a factor of four.

| Metric | AC 150/5200-33B Standard | Proposed Location | Shortfall |
|---|---|---|---|
| Distance from runway end (turbojet) | ≥ 10,000 ft | < 2,500 ft | 7,500+ ft |
| Detention time if permitted on-airport | ≤ 48 hours | Not specified | Unknown |

If a wet-retention pond is proposed (no drainage cycle), it fails the design standard as well.

**Source:** FAA AC 150/5200-33B, Hazardous Wildlife Attractants On or Near Airports; available at FAA.gov (document library).

---

## 5. Thermal Plumes: FAA Has Already Acted on This Hazard

The AIM now contains explicit advisory language (§ 7-6-16) on exhaust plumes from power plants and cooling towers:

- Plumes extend **more than 1,000 ft above the top of the stack or cooling tower.**
- Effects include turbulence, vertical wind shear, airframe damage, aircraft upset, and engine failure.
- The hazard is **most critical in low-altitude flight in calm and cold air** — precisely the conditions during ILS approaches to an instrument-equipped runway.
- Plumes are **often invisible** to pilots.

Data center cooling infrastructure produces continuous thermal output. Air-cooled condenser arrays observed in research discharge air **14 to 25°F above ambient.** In one documented incident, an aircraft traversing a cooling tower plume was knocked approximately 50–60 degrees off center.

The most directly analogous precedent: the FAA raised concern about a 200-MW natural gas facility with four exhaust stacks proposed **2.6 miles from Byron Municipal Airport, CA.** The proposed data center would be within the RPZ — less than 0.5 miles from the threshold.

The FAA added AIM 7-6-16 in direct response to safety findings. The FAA's own Technical Guidance Assessment Tool for Thermal Exhaust Plume Impact exists for exactly this evaluation — which has not been conducted here.

**Sources:** FAA AIM § 7-6-16; AOPA News, "Thermal Plumes a Potential Danger Near Airport," August 5, 2010; Facilities Dive, data center temperature study citing ASU/Sailor research.

---

## 6. Electromagnetic Interference: Unquantified, Not Ruled Out

Data centers contain UPS systems, server power supplies, backup diesel generators, and substation equipment — all of which emit broadband electromagnetic interference. FAA Order 6750.16E (ILS Siting Criteria) establishes ILS critical areas and protects against multipath interference; it notes that any structure subtending a vertical angle greater than one degree from the ILS antenna warrants concern. The data center's proximity to the ILS localizer and glide slope for RWY 19R creates an unquantified but plausible multipath risk.

ACRP Report 108 (Guidebook for Energy Facilities Compatibility with Airports and Airspace, 2014) specifically identifies high-energy production and transmission facilities as potential sources of navaid interference and documents the FAA assessment process. That assessment is absent here.

The argument's honest framing: **the EMI impact is unknown because the required study has not been done.** That is itself a disqualifying gap.

**Sources:** FAA Order 6750.16E ILS Siting Criteria (June 2014); ACRP Report 108 (TRB, 2014).

---

## 7. Approach Lighting Interference: The Specific Risk Is Flash Confusion

The ALSF-2 system at RWY 19R end works by producing a "ball of light" effect traveling toward the runway twice per second — pilots use it to establish visual alignment on approach. FAA research confirms that extraneous bright lights near this system can cause:

- Confusion about the ALS boundary and runway threshold
- Perceived runway slope illusions
- Flash blindness or afterimage from high-intensity sources within the pilot's visual field

The AIM explicitly notes that "lights along a straight path, such as a road or lights on moving trains, can be mistaken for runway and approach lights." A large industrial facility with bright operational lighting directly adjacent to an ALSF-2 run introduces exactly this hazard.

**Source:** FAA AIM Chapter 2, § 2-1-1; FAA Airplane Flying Handbook (FAA-H-8083-3C), Chapter 11 (Night Operations).

---

## 8. Grant Assurance Exposure Is Statutory, Not Discretionary

The five assurances cited in the memo trace to 49 U.S.C. § 47107. The statutory language of § 47107(a)(9) requires the sponsor to ensure "terminal airspace required to protect instrument and visual operations to the airport will be cleared and protected by mitigating existing, and preventing future, airport hazards." Section (a)(10) requires compatible land use restriction. Section (a)(16) requires ALP approval before alterations.

Enforcement under 14 CFR Part 16:
- Director's Determination directing corrective action
- Withholding of future AIP grants
- Civil penalties up to **3× illegally diverted revenue** (49 U.S.C. § 46301(a)(3))
- Requirement to remove structure and restore aeronautical use

These are not advisory risks. They are the same legal obligations MWAA accepted when it accepted each AIP grant. The memo correctly identifies all five assurances. The writer should cite the statutory subsections directly rather than only the assurance numbers.

**Source:** 49 U.S.C. § 47107; 14 CFR Part 16; 49 U.S.C. § 46301.

---

## 9. The ALP Gap Is the Most Procedurally Decisive Point

MWAA's Dulles Master Plan was board-approved July 16, 2025, and submitted to FAA for concurrence — but FAA concurrence has not yet been received. The plan designates non-aeronautical development for **areas adjacent to Autopilot Drive**, not for the RWY 19R end area. The proposed data center was not included in that master planning process.

FAA ARP SOP 2.00 (ALP Review) requires that any addition to the ALP be evaluated using the same principles as master planning, with FAA approval. FAA disapproves ALP items that meet any one of three tests: (A) materially impact safe and efficient aircraft operations; (B) adversely affect safety of people on the ground; (C) adversely affect value of prior federal investments.

All three tests are plausibly triggered by this proposal. FAA disapproval would be legally available to the agency the moment the airport submits an ALP modification reflecting the data center.

**The argument's strongest procedural point:** the project cannot lawfully appear on the ALP without FAA review, and FAA has clear statutory authority to disapprove it. Proceeding without ALP approval violates Assurance 29 independently.

**Sources:** MWAA press release, "Dulles Master Plan Update Sets Framework for Decades of Airport Development," 2025; FAA ARP SOP 2.00, October 2013; 49 U.S.C. § 47107(a)(16).

---

## 10. What the Analysis Cannot Quantify Without Operator Data

| Missing Input | Why It Matters | Who Should Supply It |
|---|---|---|
| Exact coordinates of proposed data center footprint | Would allow precise measurement of distance from runway threshold and RPZ boundary | Developer / MWAA Planning |
| Data center power draw (MW) | Determines scale of thermal plume, cooling requirement, EMI output | Developer |
| Cooling system type (air-cooled vs. liquid-cooled vs. cooling tower) | Determines whether AIM 7-6-16 hazard applies and at what intensity | Developer |
| Stormwater facility design (wet vs. dry retention) | Determines whether AC 150/5200-33B design standard is met | Developer / Stormwater engineer |
| ILS critical area dimensions for RWY 19R localizer and glide slope | Would determine whether data center falls inside critical area | FAA ADO / NAVAID maintenance |
| Proposed lighting plan (type, intensity, hours of operation) | Would allow evaluation of ALSF-2 interference risk | Developer |
| Lease or revenue terms | Required for opportunity cost calculation against future aeronautical use | MWAA Finance |

---

## Key Numbers for the Writer

| Metric | Value | Source |
|---|---|---|
| RWY 01L/19R length | 9,400 ft | FlightAware |
| Approach type | ILS/DME, precision instrument, ALSF-2 | FlightAware |
| Part 77 protected surface length | 50,000 ft (9.47 miles) from threshold | 14 CFR § 77.19 |
| RPZ area (precision runway) | ~79 acres | AC 150/5300-13B (calculated) |
| Wildlife attractant exclusion zone (turbojet) | 10,000 ft from runway end | AC 150/5200-33B |
| Proposed stormwater pond distance from threshold | < 2,500 ft | Memo description |
| Stormwater pond shortfall vs. AC standard | 7,500+ ft short | Calculated |
| Thermal plume vertical extent above cooling tower | 1,000+ ft | FAA AIM 7-6-16 |
| Data center cooling discharge temp above ambient | 14–25°F | ASU/Sailor research via Facilities Dive |
| AIP civil penalty ceiling | 3× illegally diverted revenue | 49 U.S.C. § 46301 |
| Master plan approval date | July 16, 2025 (MWAA Board) | MWAA press release |
| Data center area in master plan | Not designated | MWAA Master Plan 2025 |

---

## Counterargument the Writer Must Address

**The objection:** A competent developer will design the facility to clear all Part 77 surfaces, shield EMI, point cooling towers away from approach paths, and commit to dry-retention stormwater design — making the technical objections addressable.

**Why this doesn't resolve the argument:** The issue is not engineering mitigation alone but the FAA process that does not yet exist. No aeronautical study (FAA Form 7460-1) has been filed. No ILS siting evaluation has been conducted. No wildlife hazard assessment has been performed. No FAA ADO coordination has occurred. These are sequenced prerequisites, not parallel workstreams. The project cannot demonstrate compliance with standards it has never submitted to. Until all those studies are complete and FAA issues a No Hazard determination, the right answer is not to proceed with construction.

The secondary objection is land. Engineering solutions do not restore the strategic option value of runway-end land for future extension. A data center — even a compliant one — permanently encumbers the most irreplaceable acreage on the airport.
