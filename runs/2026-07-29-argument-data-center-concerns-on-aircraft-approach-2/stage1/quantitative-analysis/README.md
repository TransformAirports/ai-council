# Quantitative Analysis: Data Center Concerns on Aircraft Approach (IAD)

**Run:** data-center-concerns-on-aircraft-approach  
**Analyst:** Quantitative Analyst  
**Date:** 2026-07-29  
**Airport:** Washington Dulles International Airport (IAD / KIAD)

---

## Files in This Directory

| File | Purpose |
|---|---|
| `calculations.json` | All inputs, formulas, outputs, and source references. Machine-readable. |
| `iad_19r_approach_surface.csv` | Chart-ready table: distance from RWY 19R threshold vs. allowed structure height and surface width under 14 CFR § 77.19 |
| `regulatory_risk_matrix.csv` | All identified regulatory concerns, their primary citations, thresholds, data center status, and risk level |
| `README.md` | This file |

Evidence JSONL is at: `outputs/stage1/quantitative-analyst-evidence.jsonl`  
Brief is at: `outputs/stage1/quantitative-analyst-brief.md`

---

## How to Reproduce the Key Calculations

### 1. RPZ Area (Precision Instrument Runway)
From FAA AC 150/5300-13B:
- Inner edge: 1,000 ft
- Outer edge: 1,750 ft
- Length: 2,500 ft
- Formula: Trapezoid = 0.5 × (1,000 + 1,750) × 2,500 = **3,437,500 sq ft = 78.9 acres**

### 2. Part 77 Approach Surface Height at Any Point
For RWY 19R (precision instrument, ILS/DME):
- First segment (0–10,000 ft from threshold): allowed height = distance / 50
- Second segment (10,000–50,000 ft from threshold): allowed height = 200 + (distance − 10,000) / 40
- Example: at 2,500 ft (RPZ end): 2,500 / 50 = **50 ft**

### 3. Stormwater Pond Distance Shortfall
- AC 150/5200-33B standard for turbojet airports: **10,000 ft from runway end**
- Proposed pond location: within RPZ, less than **2,500 ft from threshold**
- Shortfall: 10,000 − 2,500 = **7,500+ ft short of standard**

---

## Primary Sources Used

1. FlightAware Runway Database – KIAD RWY 01L/19R
2. 14 CFR § 77.19 – Civil Airport Imaginary Surfaces (via Cornell LII)
3. FAA AC 150/5300-13B – Airport Design (March 2022)
4. FAA AC 150/5190-4B – Airport Land Use Compatibility Planning
5. FAA AC 150/5200-33B – Hazardous Wildlife Attractants On or Near Airports
6. FAA AIM § 7-6-16 – Avoid Flight in Vicinity of Exhaust Plumes
7. 49 U.S.C. § 47107 – Grant Assurance statutory basis (via Cornell LII)
8. 14 CFR Part 16 – Rules of Practice for Federally-Assisted Airport Enforcement
9. FAA Order 6750.16E – ILS Siting Criteria (2014)
10. ACRP Report 108 – Guidebook for Energy Facilities Compatibility (2014)
11. FAA ARP SOP 2.00 – Airport Layout Plan Review (October 2013)
12. MWAA Master Plan Press Release (2025)

---

## What Cannot Be Computed Without Operator Data

- Exact distance from proposed data center to runway threshold (requires coordinates)
- Data center power draw (MW) — determines thermal plume scale
- Cooling system type — determines whether AIM 7-6-16 applies and at what intensity
- ILS critical area dimensions for RWY 19R — requires FAA NAVAID maintenance records
- Opportunity cost of land vs. future runway extension — requires lease terms and extension cost estimates

---

## Analyst Notes

- No numbers in this analysis were fabricated. Where PDFs returned 403 errors, regulatory language was sourced from secondary legal repositories (Cornell LII, AOPA) or from search result summaries, and confidence levels were adjusted accordingly.
- The strongest quantitative anchor is the stormwater pond distance shortfall: a 10,000-ft standard vs. a < 2,500-ft proposed location is a 4× violation of a specific dimensional threshold, not a judgment call.
- The approach surface CSV supports a chart showing the allowed height envelope from threshold to 10,000 ft, illustrating how little vertical clearance exists in the RPZ and why the land is strategically irreplaceable.
