# Evidence Map — Data Center on the RWY 1L/19R Approach at IAD

**For:** the strategist. **From:** evidence-curator.
**Run:** `data-centers-on-aircraft-approach` (strengthen mode).
**Thesis being strengthened:** MWAA should not build the currently proposed data
center in its proposed location off the RWY 1L approach / 19R departure end at
Dulles, on airport-planning, airspace, and grant-assurance grounds.

**Ledger:** `outputs/evidence-ledger.jsonl` — 94 records (44 usable, 47
contextual, 3 disputed). 128 raw researcher records were normalized to the
target schema and deduplicated: same-source repeats were merged (folded agents
noted in each record's `caveat`), independent-source corroboration preserved and
cross-linked via `corroborated_by`. One record (E-0094) is a curator gap-fill.

This is an argument kit, not a report. It tells you what to lead with, what the
other side will say, and what you may not claim. Every bracketed ID is auditable
against the ledger.

---

## 1. The load-bearing evidence, ranked

Ranked by argumentative weight and difficulty to rebut. The top is where the
thesis is strongest.

1. **E-0014 / E-0079 / E-0091 — The fifth runway and 90M-passenger build-out is a
   live, board-reaffirmed plan, not a hypothetical.** Planned since the 1950s, in
   the 1985 master plan, FAA-approved alongside the fourth runway in the mid-2000s,
   and reaffirmed by the MWAA Board in July 2025 (airlines concurred; ~$20B
   program). This is the least-rebuttable pillar: the airport's own governing body
   has an active claim on protecting airfield capacity. `airport_document` +
   `journalism`, high. *Caveat carried inside E-0014: the published fifth runway
   parallels 12-30 on the south side — see gap #5; the capacity argument here is
   about the 1L/19R surfaces, not the fifth runway footprint itself.*
2. **E-0094 (curator gap-fill) + E-0034 + E-0041 — The parcel sits off a
   precision runway with ALSF-2 lighting at both ends.** Verified against
   FlightAware/GlobalAir/FAA: RWY 01L and 19R each carry an ALSF-2 (2,400 ft)
   supporting Cat II/III precision approaches. This is what makes the 14 CFR 77.19
   50:1 approach surface apply and makes the letter's approach-lighting-
   interference concern concrete rather than speculative. `primary_dataset`, high.
3. **E-0035 + E-0036 — The Part 77 approach surface is unforgiving here.** Under
   14 CFR 77.19 the precision approach surface rises at 50:1; a 50-ft object
   reaches the surface only ~2,500 ft from the surface origin. Data-hall roofs
   plus rooftop chillers/stacks routinely exceed 50 ft, so "does not penetrate" is
   a razor-thin margin. `primary_regulation` + analyst construction, high/med.
4. **E-0037 + E-0040 — The control-critical band is exactly where the parcel is.**
   The 40:1 departure surface allows only 25 ft of height at 1,000 ft off the
   departure end; on a 3° approach the aircraft is below ~210 ft AGL within
   3,000 ft of the threshold — the least-recoverable phase of flight. Any plume or
   glare source near the approach lights intersects the flight path where the
   pilot has least margin. Analyst constructions from published geometry
   (`primary_dataset`, contextual — reproducible, in
   `outputs/stage1/quantitative-analysis/`).
5. **E-0059 + E-0072 + E-0082 + E-0085/E-0086/E-0087 — The regulatory gate is real
   and enumerated.** Grant Assurances 19, 20, 21, 22, 29 bind MWAA; construction in
   the approach surface requires a Form 7460-1 filing (14 CFR Part 77) and an FAA
   obstruction evaluation/airspace analysis ending in a Determination of Hazard or
   No Hazard. GA 20/21 trace to 49 U.S.C. 47107(a)(9)/(10). `primary_regulation`,
   high.
6. **E-0083 — Section 163 is the frame, and it cuts both ways.** The FAA
   Reauthorization Act of 2018 (§163) limited FAA authority over on-airport land
   use to development that (A) materially impacts safe/efficient aircraft
   operation, (B) adversely affects safety of people/property on the ground, or
   (C) adversely affects the value of prior federal investment. **The letter's own
   (A)/(B)/(C) test is the §163 test.** Argue on that standard, not
   grant-assurance maximalism (see §5–6). `authoritative_research`, high.
7. **E-0038 + E-0039 — The stormwater pond is not marginally non-compliant.** AC
   150/5200-33C recommends 10,000 ft separation for turbine aircraft and up to 5
   statute miles where an attractant could move wildlife into approach/departure
   airspace. A pond at the runway end sits ~95% inside the 10,000-ft standard and
   ~98% inside the 5-mile trigger. `primary_regulation` + analyst, high/med.
8. **E-0090 + E-0018 + E-0019 — The 2018 precedent is double-edged; own it first.**
   MWAA sold 424 acres of Dulles "Western Lands" to Digital Realty for $236.5M
   (~$558K/acre) in 2018, netting ~$207M directed to hold down cost per enplaned
   passenger. This is the opposition's best weapon (§5). The distinguishing fact to
   lead with (E-0019, MWAA primary): the Western Lands were the **surplus that
   remained after the fourth runway and its support area were built** — capacity
   was protected first, then surplus was sold. `airport_document`, high.
9. **E-0026 vs E-0088 — FAA's own plume record is split (a genuine contradiction).**
   FAA AIM 7-6-16 says exhaust-plume turbulence can extend over 1,000 ft above a
   stack and is "most critical in approach and departure corridors" (E-0026). But
   the FAA plume assessment tool characterizes the **overall** flight-disruption
   risk as low, significant mainly to light aircraft in calm/cold/unstable
   conditions (E-0088). Both are FAA. `contradicted_by` links set on both. This is
   the fault line the contrarian will attack — handle as tension, not a knockout.
10. **E-0031 + E-0045 — NAVAID/EMI is a recognized, evaluable effect.** FAA
    obstruction criteria treat electromagnetic interference with navigation/radar
    as a substantial adverse effect (E-0031); NTIA wind-turbine studies show
    navaid/radar degradation is real but avoidable with siting (E-0045). Supports
    both "study it" and the letter's "we don't yet know the EMI impact."
11. **E-0092/E-0048 + E-0093 + E-0091 — The political stack is loaded toward
    building.** MWAA operates under a federal lease to 2100; DOT Secretary Duffy
    launched an initiative/RFI to modernize Dulles; the ~$20B expansion has White
    House backing. The thesis swims against federal pressure to develop — name it.
12. **E-0009 + E-0010/E-0032 — Single-carrier hub, at a record.** United flies
    ~68% of IAD flights; IAD set a record 27.25M passengers in 2024. Capacity
    protection is not abstract at a growing United hub.

Honorable mention: **E-0041** (ALSF-2 extends 2,400–3,000 ft from threshold,
defining the lighting-interference zone); **E-0073** (Part 77 notice violation
carries a $1,000/day civil penalty); **E-0043** (two 2026 grants total ~$64M — a
documented *floor* for the prior-federal-investment exposure §163(C) protects).

---

## 2. What is genuinely non-obvious

- **The strongest argument is capacity foreclosure, not the hazard list.** Each
  individual hazard (plume, glare, wildlife, EMI) is an *evaluable, conditionable*
  FAA question — none is an automatic disqualifier. The argument that does not
  dissolve under FAA process is that this specific land sits inside the
  approach/departure surfaces of an active precision runway (E-0035, E-0094) and
  is strategic capacity land (E-0014). Lead with the irreversible land commitment.
- **Section 163 is the letter's friend, not its enemy.** A reader may assume §163
  (which *limited* FAA authority over airport land use) weakens the case. It does
  not: the letter already argues on the exact (A)/(B)/(C) criteria §163 preserved.
  Framing the objection as the §163 test makes it more durable than a
  grant-assurance-violation claim the FAA might decline to entertain post-§163.
- **The 2018 sale supports careful siting, not "we already do this."** The
  precedent proves MWAA protects runway land first and sells only surplus (E-0019)
  — precisely the discipline the current proposal skips.
- **A data center's plume risk is a design choice, not a fixed property.** Plume
  magnitude is driven almost entirely by on-site generation (E-0047). Grid-only,
  no-on-site-generation is a real mitigation — but E-0081/E-0076/E-0077 show
  on-site diesel is standard in this market, so a no-generation lease condition is
  not costless and may not be offered.
- **The 4.3 m/s plume number everyone cites is Australian, not FAA (E-0089).**
  Several agents presented it as an FAA threshold. It is not. See §7.

---

## 3. Where the swarm agrees, and where it fights

**Agreement (high-consensus, safe to build on):**
- The parcel is inside the Part 77 approach/departure surfaces of precision RWY
  1L/19R; construction there triggers a 7460-1 aeronautical study. (E-0035,
  E-0058, E-0072, E-0082, E-0094 — multiple agents.)
- A runway-end stormwater pond conflicts with AC 150/5200-33 wildlife guidance.
  (E-0038, E-0039, E-0057 — coo/engineer/regulatory/quant concur.)
- MWAA has an active, board-level plan to expand capacity, including a fifth
  runway. (E-0014, E-0079, E-0091.)
- FAA formally recognizes exhaust plumes as an aircraft hazard and publishes a
  tool to assess them. (E-0026, E-0027, E-0088.)

**Genuine contradictions / tensions (preserved in the ledger):**
- **Plume hazard magnitude:** E-0026 ("most critical in approach/departure,
  >1,000 ft") vs E-0088 (FAA: overall risk low, mainly light aircraft). Both FAA;
  `contradicted_by` set on both. The fault line the contrarian will attack.
- **Hazard vs. mitigable condition:** thesis-aligned agents read the hazard list
  as grounds to reject; the contrarian reads every item as a conditionable FAA
  screen (E-0020, E-0021, E-0022, E-0025). The core dispute — resolve it with the
  capacity-foreclosure argument, not by winning each hazard.
- **Acreage of the 2018 sale:** 424 acres (E-0090/E-0001/E-0018, primary MWAA) vs
  433 acres (E-0068, secondary trade blog, `disputed`). Use 424;
  `contradicted_by` links set.
- **CPE peak:** $26.55 in 2014 (E-0011) vs $26.47 in 2013 (E-0054). Both
  `disputed`. If you cite the CPE peak, attribute the range; do not assert one
  figure.

---

## 4. Candidate airport cases and quantitative exhibits

**Comparable cases (analogy, not proof):**
- **Inyokern Airport / NAWS China Lake (June 2026)** opposed a 99 MW hyperscale
  data center ~1 mile away, citing thermal plume and 40 diesel generators as
  threats to navigable airspace (E-0044). The closest live analog to this exact
  objection.
- **The 2018 Digital Realty "Western Lands" sale at IAD** (E-0090/E-0019) — the
  on-property precedent; frame as "protect capacity first, sell surplus second."
- **National airport data-center pattern** (E-0069: Eastern Iowa, Manassas,
  Buckeye, Colorado Springs) — the opposition's "everyone's doing it"; concede it
  exists, distinguish on siting inside the approach surface.
- **Loudoun ended by-right data-center approval (March 2025)** and Prince William
  rejected a 2,000-acre rezoning (E-0080, E-0056) — even the host jurisdictions
  are tightening. Useful against "if we don't, a neighbor will."

**Quantitative exhibits ready for the deck (reproducible, in
`outputs/stage1/quantitative-analysis/`):**
- **Approach-surface height limits** (E-0036): 50-ft object hits the 50:1 surface
  at ~2,500 ft from origin; 70-ft object at ~3,500 ft.
- **Departure-surface height limits** (E-0037): 25 ft allowed at 1,000 ft off the
  departure end.
- **Glideslope overflight band** (E-0040): 102 ft AGL at 1,000 ft, 155 ft at
  2,000 ft, 207 ft at 3,000 ft from threshold — the control-critical zone.
- **Wildlife-separation shortfall** (E-0039): pond ~95% inside 10,000-ft standard,
  ~98% inside the 5-mile trigger.
- **Prior federal-investment floor** (E-0043): two 2026 grants total ~$64M — a
  documented *floor*, not the cumulative total, for the §163(C)/GA-29(C) exposure.

---

## 5. The strongest case against the thesis

Do not caricature this. The contrarian brief is well-built; the strategist must
answer it, not dodge it.

1. **This is a conditions memo mislabeled as a kill memo.** Every hazard (plume,
   glare, EMI, wildlife) has a quantitative FAA screen and a mitigation path
   (E-0022 solar-glare policy, E-0088 plume tool, E-0031 EMI evaluation, E-0057
   detention-basin design). The correct output of the 7460 process is conditions,
   not rejection.
2. **The grant-assurance argument points the other way.** GA 24 requires the
   airport to be "as self-sustaining as possible"; fair-market non-aeronautical
   development that lowers CPE *advances* the assurances the letter cites (E-0020,
   E-0021, E-0060; 46% of US airport revenue is non-aeronautical, E-0066).
3. **MWAA already ran this play here and called it compliant** (E-0090/E-0018):
   $236.5M in, ~$207M earmarked to cut airline costs.
4. **The opportunity cost is enormous and unquantified by the letter.** Ashburn
   carries an estimated 70% of global internet traffic (E-0024); airport-adjacent,
   power-and-fiber-served land is among the most valuable non-aeronautical acreage
   in US aviation.
5. **FAA itself rates the plume flight-disruption risk as low for the aircraft
   that matter** (E-0088) — transport-category jets, not light aircraft.

**How to beat it without overclaiming:** concede that each hazard is
conditionable, then win on the two things conditions cannot cure — (a)
irreversibly committing strategic capacity land inside an active precision
runway's approach/departure surfaces (E-0014, E-0035, E-0094), and (b) that the
2018 precedent *is* the rule the current proposal breaks: protect capacity first,
monetize only surplus (E-0019). Recommend the gate, not the wall: no approval on a
"project email"; require ADO coordination, a 7460 study, glare/plume/EMI analyses,
a compliant stormwater design, an ALP amendment, and a no-on-site-generation lease
condition — and reject *this* siting because it forecloses reserved capacity,
regardless of study outcomes.

---

## 6. Evidence gaps that could change the conclusion

Unresolved. Some are not publicly answerable and should be flagged to the reader
as decision-critical unknowns.

1. **The actual proposal.** There is **no public evidence record of the specific
   2025–2026 data-center proposal** — footprint, structure/appurtenance heights,
   ground elevation, exact distance to the surfaces and to the ALS. The entire
   penetration analysis is geometric and generic until MWAA's site plan is run
   through a true Part 77 / AC 150/5300-13 test. Internal to MWAA; not closable by
   web research. **Biggest gap.**
2. **On-site generation.** Whether the tenant is grid-only or runs on-site
   generation determines the plume case almost entirely. On-site diesel is standard
   in this market (E-0081), so a no-generation condition is not costless and may
   not be offered. Unknown for this project.
3. **Cumulative prior federal investment.** Only a ~$64M recent floor is documented
   (E-0043); the decades-long AIP/PFC/BIL total on the airfield and NAVAIDs (the
   real GA-29(C) / §163(C) exposure) requires FAA grant history not yet compiled.
4. **The capacity trigger.** The fifth-runway plan is real and board-reaffirmed,
   but the *timing* — whether a 19R/1L-affecting extension is ever triggered by a
   capacity forecast — is not established. The contrarian's fair point (E-0090
   logic) is that IAD is land-rich and the reservation could sit idle for decades.
5. **Whether the parcel is inside the fifth-runway footprint or merely nearby.**
   The published fifth runway parallels 12-30 on the south side (detail folded into
   E-0014); the proposal is off 1L/19R. The "precludes future capacity" argument
   rests on protecting 1L/19R extension and its associated surfaces, which needs
   the ALP overlay to confirm. **Do not assume the data center sits on the planned
   fifth runway itself.**

---

## 7. Source-quality warnings and stale data

- **The 4.3 m/s plume threshold is CASA (Australian), not FAA** (E-0089). Its
  original basis is reportedly lost and CASA uses it only as a screening trigger.
  Folded records show several agents presented it as an FAA number. Cite it only as
  "the best-available published numeric anchor, foreign-derived" (E-0074 adds a
  10.6 m/s higher screen).
- **Some wildlife records cite AC 150/5200-33B, which is cancelled** and superseded
  by 33C (E-0029). Use **33C** as current (E-0028, E-0038).
- **Analyst constructions (E-0036, E-0037, E-0039, E-0040) are derived geometry,
  not external sources** — marked `contextual`. Transparent and reproducible, but
  they assume flat terrain at runway-end elevation and a precision approach — the
  latter now validated (E-0094), the former not against the real site plan.
- **Market/context claims rest on trade-web or advocacy sources** (opportunity
  cost, national pattern, tax-revenue records — several `anecdotal`: E-0024,
  E-0042, E-0069, E-0068). Directionally fine for context; must not carry a safety
  or legal conclusion.
- **Bond ratings, CPE figures, and passenger records are journalism** (E-0050,
  E-0011/E-0054, E-0010), not audited financials — no `audited_financial` source
  reached the ledger. Treat as reported, not verified from statements.

---

## 8. Do not claim

- **Do not claim the data center is automatically prohibited or an automatic
  grant-assurance violation.** It triggers FAA adjudication; the honest claim is
  "it must not proceed as drawn without that adjudication, and this siting should
  be rejected because it forecloses reserved capacity."
- **Do not present 4.3 m/s as an FAA plume threshold** (E-0089). It is CASA-derived.
- **Do not assert the plume "will" endanger heavy jets.** FAA rates the overall
  risk low for transport-category aircraft (E-0088). Claim the *geometry* puts any
  plume/glare in the control-critical band (E-0040), not a proven upset.
- **Do not state a single CPE peak or the 433-acre figure as fact** — both
  `disputed` (use 424 acres, E-0090; range the CPE, E-0011/E-0054).
- **Do not claim the parcel sits on the planned fifth runway.** The published fifth
  runway is off 12-30; the argument is about the 1L/19R surfaces and reserved
  capacity, which needs ALP confirmation (gap #5).
- **Do not quantify "nine figures of forgone revenue" as fact against the thesis,
  or a specific safety probability for the thesis** — neither is evidenced for this
  parcel. Both sides' dollar/risk magnitudes are un-sourced here.
- **Do not treat the 2018 sale as precedent *for* this project** without the
  "surplus after the runway was built" distinction (E-0019).
