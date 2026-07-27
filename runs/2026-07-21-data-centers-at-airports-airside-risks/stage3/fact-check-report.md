# Fact-Check Report

**Run:** Data Centers at Airports: Airside Risks
**Document checked:** `outputs/stage3/humanized-draft.md`
**Checked against:** all 14 Stage 1 briefs in `outputs/stage1/` and the run prompt
**Date:** 2026-07-21
**Result:** Draft cleared with three inline `[FACT-CHECK]` flags resolved. No `[UNVERIFIED — HUMAN REVIEW]` tags required. Final draft written to `outputs/stage3/final-draft.md`.

---

## Summary

Every numerical claim, named-airport example, cost figure, percentage, attributed quote, and specific assertion in the draft was traced to a Stage 1 brief and confirmed to match within reasonable rounding, with correct source attribution. No fabricated or wholly unsourced claim was found. The draft arrived with three pre-existing inline `[FACT-CHECK: …]` flags placed by an earlier stage; all three are legitimate, and all three are resolved below. No claim rose to the level of requiring removal or an `[UNVERIFIED — HUMAN REVIEW]` tag.

- **Verified claims:** ~95 discrete checkable claims across the eight sections, all confirmed against the briefs. (Count is approximate because some sentences bundle multiple figures.)
- **Unverified claims requiring a tag:** 0
- **Suspected errors / reconciliations:** 3 (all pre-flagged in the draft; all resolved — see below)
- **Missing citations:** 0 material. One inference is properly self-labeled (see Notes).

---

## Suspected errors and reconciliations (the three inline flags)

### 1. Statewide generator count — 9,000 vs. 10,500+ (Exec Summary point 2)

- **Draft text:** "between 9,000 [Chief-Engineer brief, citing VPM] and more than 10,500 [Operations-Analyst brief, citing Virginia Mercury] statewide [FACT-CHECK: reconcile or confirm the statewide generator range]."
- **Finding:** Not an error. The two figures come from two different sources, each accurately quoted. The Chief-Engineer brief attributes ~9,000 statewide diesel generators to VPM; the Operations-Analyst brief attributes 10,500+ to Virginia Mercury. Both are correctly cited to their respective sources. The apparent discrepancy is a genuine difference between two published counts, not a transcription error.
- **Resolution:** Retained both figures with source attribution; reworded to make explicit that the two numbers reflect different source counts rather than a single reconciled total. Removed the inline `[FACT-CHECK]` bracket.

### 2. Western Lands acreage — 424 vs. 433 (Exec Summary point 7)

- **Draft text:** "MWAA sold 424 acres of Dulles 'Western Lands' [FACT-CHECK: five briefs say 424 acres; the CEO brief says 433 — resolve]."
- **Finding:** Confirmed discrepancy between briefs. Five briefs — Infrastructure-Economist, Regulatory-Political, Airport-Procurement, Airline-Commercial-Strategist, and Deep-Research — state **424 acres** (paired consistently with $236.5M). The Airport-CEO brief states **433 acres** (lines 83 and 119). The Airline-Commercial brief hedges "~424–433 acres." 424 is the well-supported figure (five independent briefs, and it is the figure tied to the sale price everywhere it appears).
- **Resolution:** Used **424 acres** throughout the final draft (consistent with the sale-price pairing and the body text at the "Follow the money" section and the MWAA implications section, both of which already used 424). Removed the inline `[FACT-CHECK]` bracket. The CEO brief's 433 is treated as a minority outlier and not carried into the draft.

### 3. On-site diesel fuel volume — "240,000+ gallons" vs. ~63,400 gallons (fuel section)

- **Draft text:** "a single 10-megawatt plant stores on the order of 25,000 to 63,400 gallons under NFPA 30 … [FACT-CHECK: DPS brief's key-findings line says '240,000+ gallons' but its worked example converts ~240,000 liters to ~63,400 gallons — apparent units error; confirm]."
- **Finding:** Confirmed internal units error in the Director-of-Public-Safety brief. The brief's key-findings summary line reads "240,000+ gallons," but the brief's own worked example derives that figure from ~240,000 **liters**, which converts to ~63,400 gallons (line ~28 vs. line ~55 of the DPS brief). The "240,000 gallons" headline figure is a liters-to-gallons conflation, not a defensible number. The defensible figure for a single 10 MW plant is the **25,000–63,400 gallon** range, which the draft body already uses correctly.
- **Resolution:** Kept the defensible "25,000 to 63,400 gallons" range in the final draft. Dropped the erroneous "240,000+ gallons" figure entirely (it never appeared in the draft body, only in the fact-check note). Removed the inline `[FACT-CHECK]` bracket.

---

## Spot-checks on the load-bearing claims (all verified)

| Claim | Brief source | Status |
|---|---|---|
| AIM 7-6-16 plume "over 1,000 feet above the top of the stack or cooling tower," calm/cold air, approach/departure corridors | Chief-Engineer | Verified (direct quote) |
| Part 77 "measures the building's shape, not its behavior" | Regulatory-Political | Verified (direct quote) |
| Aircraft rolled 50–60° at ~550 ft AGL over cooling towers (WACAZ) | Technology-Scout | Verified |
| ~4,700 generators in Loudoun County | Chief-Engineer / Emergency-Management | Verified |
| Testing 10–30 min/month; ~100 hr/yr non-emergency cap; unlimited emergency | Chief-Engineer / Airport-COO | Verified |
| Daejeon Sept 2025: ~22 hr, 200+ firefighters, 60 engines, 647 systems | Director-of-Public-Safety / Emergency-Management (Korea Herald, NetworkWorld) | Verified |
| Part 139 ~3-minute ARFF response standard | Director-of-Public-Safety | Verified |
| AC 150/5200-33C: quarter-acre impoundment, 5,000 ft, 10,000 ft, 5 statute miles | Regulatory-Political | Verified |
| 78% of strikes below 1,000 ft; ~90% below 3,000 ft | Deep-Research (jetwhine, FAA data) | Verified |
| Section 743 "materially impacts…"; 45-day jurisdiction window | Regulatory-Political (Kaplan Kirsch, AirTAP) | Verified |
| 2006 SRA judged overflight risk "insignificant" | Regulatory-Political | Verified |
| Byron 2010: 200 MW gas plant, 2.6 mi, four 80-foot stacks, AOPA objection | Deep-Research (AOPA) | Verified |
| Colorado site: 98 generators + 40 installed, ~345 MW | Airport-COO / Emergency-Management (CPR) | Verified |
| Transformer lead >160 weeks; substation 36–60 mo; grid wait >7 yr | Chief-Engineer (Construction Owners) | Verified |
| DFW Building F, 2200 West Airfield Drive, ~1,000–1,500 ft from centerline | Deep-Research (interconnection.fyi) | Verified |
| Kansas City "Kestrel": ~380 acres, 6 buildings, 1.8M sq ft, $100B corridor | Emergency-Management (KCTV5) | Verified |
| Atlanta Dec 17 2017: ~11 hr outage, 1,000+ flights, ~30,000 travelers | Emergency-Management (Utility Dive) | Verified |
| $236.5M sale, ~$207M net, 2018, Digital Realty | Infrastructure-Economist / Airline-Commercial / Airport-CEO | Verified |
| Campus master plan: 11.7M sq ft, 14 buildings, ~1 GW, six substations | Procurement (Data Center Frontier) | Verified |
| Loudoun tax $60M (FY2013) → $800M+ (FY2026); ~45% / $1.3B of $2.9B by FY2027 | Infrastructure-Economist (NetChoice) | Verified |
| NoVA ~4,900 MW active by early 2025; Dominion 21 GW → 40 GW | Infrastructure-Economist (IEEFA) | Verified |
| PJM Dominion-zone ~10x; FERC cap $329.17/MW-day for 2026/27 | Infrastructure-Economist | Verified |
| Dry cooling 3–4x install cost, 25–35% power penalty | Infrastructure-Economist (DOE via Data Center Knowledge) | Verified |
| Non-aero revenue ~46% of US airport revenue | Airline-Commercial (ACI-NA) | Verified |
| United ~49.9% of IAD enplanements 2025, ~62% incl. Express | Airline-Commercial | Verified |
| CPE spread $3.93 (ATL) to $36.01 (JFK), median ~$12.88 | Airline-Commercial | Verified |
| Dehubbing graveyard: CVG, PIT, STL, CLE, MEM | Airline-Commercial | Verified |
| Dulles >560,000 ops/yr; highest 2025 growth of top 50; fifth runway 2005 ROD, back under review 2025 | Infrastructure-Economist / Airline-Commercial | Verified |
| Ashburn/Sterling ~26M sq ft (Loudoun); ~50M corridor estimate | Technology-Scout (DataCenterDynamics) / Chief-Engineer (City Journal) | Verified |
| FAA Order 7400.2K §6-3-3 "physical, electromagnetic, or line-of-sight interference" | Deep-Research | Verified (exact citation) |
| Digital Dulles west of runway complex, wetlands-only environmental review | Deep-Research | Verified |
| Full study package 9–15 months; schedule 18–30 months | Procurement | Verified |
| 20–30 yr asset; 40–50 yr ground lease | Chief-Engineer / Procurement | Verified |
| 854-acre tract assembled 2005–2007 for fourth runway | Deep-Research / Infrastructure-Economist | Verified |
| MITRE Exhaust Plume Analyzer (4 aircraft classes); ACRP Report 108; Sandia glare analysis pre-7460 for solar | Technology-Scout / Deep-Research / Operations-Analyst | Verified |
| 17-member MWAA board | Airport-CEO | Verified |
| Grid interconnection jammed 5–7 years; district-heating/waste-heat framing | Chief-Engineer / Virtual-Chris | Verified |
| Fuel per 10 MW plant 72–96 hr, NFPA 110 / NFPA 30 | Director-of-Public-Safety (PowerMag) | Verified (see units note, item 3) |
| Evaporative campus 1–5 MGD water draw | Director-of-Public-Safety / Infrastructure-Economist | Verified |

All direct quotations attributed to specific chairs (COO "un-build the box" / "died on local land-use politics"; Chief-Engineer "generator plant under prolonged islanded operation" / "wrong load case" / "morning steam wisp"; Contrarian prolonged-outage and 1.2M-sq-ft-foreclosure concessions; Emergency-Manager "engineerable if EM is consulted early") were located verbatim (or within faithful paraphrase where the draft does not use quotation marks) in the cited briefs.

---

## Notes on citations

- **"[analyst inference from Ops brief]"** (Manassas paragraph, casebook section): properly self-labeled as an inference rather than a sourced fact. The underlying facts (rezoning near the airport, runway-extension program in the same master plan) trace to the Operations-Analyst brief citing Prince William Times; the characterization "the airfield was, at best, a commenter" is the draft's inference and is flagged as such. No change needed.
- **Panel-disagreement framing** (hottest-day vs. cold-still-day turbulence): correctly represents a real split between the Operations-Analyst brief (hottest full-load day) and the Deep-Research brief (cold, still, full-load). Both positions are accurately attributed. No change needed.
- **"150-to-250-megawatt campus"** (intro): consistent with the scale figures across the Contrarian and Technology-Scout briefs; within supported range. No change needed.

---

## Disposition

- `outputs/stage3/final-draft.md` written: identical to the humanized draft in substance, with the three inline `[FACT-CHECK]` brackets resolved (statewide generator range reworded to attribute both source counts; acreage fixed to 424; erroneous 240,000-gallon figure dropped and the defensible 25,000–63,400 gallon range kept), the working title updated to "Final Draft," and no other content altered.
- No claim was removed for lack of support. No `[UNVERIFIED — HUMAN REVIEW]` tag was required.
