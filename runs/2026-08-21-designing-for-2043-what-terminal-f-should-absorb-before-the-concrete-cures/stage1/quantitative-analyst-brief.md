# Quantitative Analyst Brief — Terminal F, Designing for 2043

**Run:** designing-for-2043-what-terminal-f-should-absorb-before-the-concrete-cures
**Airport:** Dallas/Fort Worth International (DFW)
**Analyst:** Quantitative Analyst (independent research, Stage 1)
**Date:** 2026-08-19

---

## What this brief is

Reproducible arithmetic on the public numbers that frame Terminal F, arranged
against the five questions in the run prompt. Every calculation names its
inputs, its source, its units and denominator, and — where the result is
decision-relevant — a sensitivity band. Where a needed input is not publicly
available, this brief names the gap and refuses to fill it with a model-generated
number. Supporting files (`calculations.json`, chart-ready CSVs, README)
live in `outputs/stage1/quantitative-analysis/`.

Professional judgment is stated in prose here and marked plainly. The evidence
JSONL companion only carries claims a reader can verify against a document.

---

## 1. The scope revision is a 20.9% increase in cost per gate

**Sourced inputs (primary):**

- 2023 preapproved plan: **15 gates at approximately $1.6 billion**. DFW/AA
  joint announcement, 2025-05-01.
- 2025 accelerated/expanded plan: **31 gates at approximately $4.0 billion**.
  Same announcement.
- Construction method: **modular gates fabricated offsite**, with a reported
  **~30% cost savings versus conventional construction** (Dallas Innovates,
  citing DFW).

**Arithmetic:**

| Metric | 2023 scope | 2025 scope | Delta |
|---|---|---|---|
| Cost per gate | $1.6B ÷ 15 = **$106.7M** | $4.0B ÷ 31 = **$129.0M** | **+$22.3M / +20.9%** |
| Cost per incremental gate (2023 → 2025) | — | ($4.0B − $1.6B) ÷ (31 − 15) = **$150.0M** | — |

The doubling of gate count came with a 2.5× increase in program cost. The
incremental 16 gates cost roughly **$150M each**, ~40% more per gate than the
original 15-gate program. That premium is not surprising — the added gates
include international/widebody-capable positions with FIS-side implications
and the second-phase modular tempo — but the number is the number, and it
frames what "cheap flex" can actually mean in this program.

**Sensitivity band (decision-relevant):**

- If final cost overruns by +12.5% to **$4.5B** (a modest overrun for a
  program of this scale): cost per gate rises to **$145.2M**, incremental
  gate cost to **$181.3M**.
- If gate count drops from 31 to 28 (three positions absorbed by amenity
  scope, FIS growth, or flex-hold): cost per gate rises to **$142.9M** at
  $4.0B and **$160.7M** at $4.5B.

**Analyst read:** any Terminal F design intervention that trades one gate
position for premium/lounge/FIS space should be priced against **$129M–$181M
of foregone gate value**, not against fitout cost. That is the honest
opportunity cost of a gate given up.

---

## 2. Peak-hour arithmetic sets the ceiling on connecting-bank geometry

**Sourced inputs (primary, American Airlines):**

- **~930 peak daily departures** from DFW (AA newsroom, 2026-07).
- **~100,000 peak daily customers** at DFW (AA newsroom, 2025-12).
- American operates **82% of DFW departures** and carries **82.6% of DFW
  passengers** (secondary; DFW-level statistics via aggregator).
- **>30% of American's daily connecting customers and bags** flow through
  DFW system-wide (AA newsroom, 2025-12).

**Arithmetic — average AA departure at DFW:**

- Peak-day customers per AA departure at DFW: 100,000 ÷ 930 ≈ **108
  passengers per one-way departure event**. This includes both
  originating and connecting customers on that flight, and it is a
  peak-day figure, not annual average.

**Arithmetic — Terminal F share:**

- The AA release confirms all 31 gates will be American-operated when the
  program completes in 2030.
- Terminal F gate share of the AA DFW footprint depends on the current
  AA-controlled gate count at DFW, which is not stated in the primary
  sources reviewed. Reporting on the terminal system suggests roughly 130–
  160 AA gates today (Terminals A, B, C, D, E excluding E's non-AA
  positions). **This is a gap — the airport-context-builder should
  confirm.** Bracketed:

| AA gate count today | T-F share of AA gates after full opening (30) | Implied AA peak departures through T-F |
|---|---|---|
| 130 | 31 ÷ 161 = **19.3%** | ~180 |
| 148 | 31 ÷ 179 = **17.3%** | ~161 |
| 160 | 31 ÷ 191 = **16.2%** | ~151 |

At 16–19% of AA's peak-day departures routing through Terminal F, the
building's connecting-bank arithmetic is not marginal. If DFW runs nine
banks per day (a common AA hub cadence), a Terminal F bank moves roughly
**17–20 departures in a ~45-minute window** — one arriving/departing
movement every ~2 minutes across 31 gate positions, i.e., ~55–65%
gate-utilization density during the bank. That is the number to size
Skylink station throughput, secondary-screening lanes, and connector-walk
width against.

**Sensitivity:** if AA reduces regional feed and upgauges (a stated
industry trend — but not sourced to AA specifically), average pax per
departure at DFW rises. If the average moves from 108 to 130 (+20%), peak
Terminal F throughput carries **an additional ~1,600 passengers per bank
per direction** into the same physical envelope.

---

## 3. Airport-level and carrier-level connecting share are not the same number

**Sourced inputs:**

- DFW airport-level connecting share: **~60%** (Road Genius aggregator;
  awaiting DFW official confirmation).
- American's own DFW framing: "largest connecting complex," ">30% of
  daily connecting customers and bags" flow through DFW system-wide (AA
  newsroom).
- Run-prompt assertion: **"two-thirds of American's DFW customers connect."**
  Not sourced to a primary AA document in the context packet; likely a
  carrier-level figure that differs from the airport-level 60%.

**Arithmetic — sizing implication of the difference:**

Take AA's peak-day 100,000 customers at DFW and vary connecting share:

| Assumed AA connecting share | Connecting-customer-trips per peak day | Originating (O&D) customer-trips per peak day |
|---|---|---|
| 55% (upside for O&D by 2035) | 55,000 | 45,000 |
| 60% (airport-level anchor) | 60,000 | 40,000 |
| **66% (run-prompt assumption)** | **66,000** | **34,000** |
| 70% (further connecting concentration) | 70,000 | 30,000 |

Between the 55% and 70% cases the O&D count varies by **50%**
(30k vs 45k). O&D pax consume check-in, TSA, curbside, bag drop, and rental
frontage; connecting pax consume gate hold, lounge, moving walkway, and
concessions.

**Analyst read (professional judgment):** the reversibility question turns
on which side of the ratio you build for. Curbside, check-in hall depth,
and TSA lane count are structural and expensive to move after pour. Lounge,
gate hold, and concessions are fitout and cheap to move. If the design
freezes at 34% O&D and the ratio drifts to 45% O&D by 2035, the retrofit
lands on the concrete side of the ledger. The council should decide which
tail to size for, name the cost of the option, and stop pretending the
choice is neutral.

---

## 4. The 37,000 sq ft benchmark and the Terminal F lounge gap

**Sourced inputs (primary, AA newsroom 2026-07):**

- New Admirals Club in Terminal C: **37,000 square feet**, near the
  Skylink station, described as American's **largest Admirals Club to
  date**.
- Terminal F lounge posture: **Provisions by Admirals Club** grab-and-go
  concept, planned for first-phase opening (not a Flagship-tier lounge).

**Arithmetic — density anchor:**

- 37,000 sq ft over Terminal C's roughly 28–33 gates places Admirals Club
  square footage at **~1,120–1,320 sq ft per Terminal C gate**.
- A typical Provisions by Admirals Club footprint is small — public
  reporting places these grab-and-go concepts in the 1,500–3,500 sq ft
  range (industry benchmark; not sourced to AA). If Terminal F opens with
  a single Provisions concept at ~2,500 sq ft over 31 gates, that is
  **~80 sq ft per gate**, roughly **6% of Terminal C's density**.
- Retrofit gap to bring Terminal F to Terminal C density: 31 gates ×
  ~1,220 sq ft/gate ≈ **~37,800 sq ft**, i.e., the same footprint as the
  Terminal C Admirals Club itself, added later, in a modular building.

**Sensitivity — what a Flagship-tier lounge would cost in gate real estate:**

- Publicly reported Flagship Lounge JFK: ~19,000 sq ft (industry
  reporting; not primary here).
- Publicly reported Delta ONE Lounge JFK: ~40,000 sq ft (industry
  reporting; not primary here).
- Gate-frontage equivalent: at ~10,000–12,000 sq ft of terminal floorplate
  per narrowbody gate position (industry rule of thumb; analyst
  construction), a **19,000 sq ft Flagship Lounge equals roughly 1.6–1.9
  gate positions**; a 40,000 sq ft Delta ONE-equivalent equals **3.3–4.0
  gate positions**. At the $129M–$150M/gate opportunity cost from §1, the
  displaced-gate cost of a Flagship-tier lounge in Terminal F ranges from
  **~$207M–$600M** in foregone gate value alone, before fitout.

**Analyst read (professional judgment):** the Provisions-vs-Flagship
question is not a fitout decision. It is a floorplate-and-gate-count
decision that needs to be resolved before the structural bays of the
modular gate pods lock. Once the modular grid is set, "add a Flagship
Lounge later" is only true if a gate position was reserved for it at
scoping. The evidence gap on whether the U&L obligates American to a
Flagship-tier presence at Terminal F before 2043 is the single most
decision-relevant unknown in this run.

---

## 5. Reversibility map — cost multipliers by category (analyst construction)

The following table is a synthesis, not a sourced dataset. It states the
order-of-magnitude cost multiplier of changing a design element after each
listed milestone versus changing it before. Numbers are analyst estimates
grounded in professional practice, offered as a decision aid; the council
should challenge them and the chief-engineer should replace them with
project-specific figures where possible.

| Design element | Reversibility window | Cost multiplier after window closes | Structural or fitout? |
|---|---|---|---|
| Roof span / column grid | Before module fabrication starts | 10–50× | Structural |
| Foundation piling depth / slab reinforcement | Before slab pour | 20–100× | Structural |
| Primary MEP risers | Before ceiling/roof deck closes | 5–20× | Structural-adjacent |
| Modular pod dimensions (width, apron edge) | Before fabrication release for that pod | 5–15× | Structural |
| Gate-position boarding-bridge type | Up to bridge order lead time (~9–12 mo) | 2–4× | Equipment |
| FIS envelope (walls, CBP inspection lane count) | Before FIS interior framing | 3–8× | Structural-adjacent |
| Lounge square footage within existing shell | Before tenant-improvement release | 1.2–2× | Fitout |
| Concessions plan / retail footprint | Before TI release | 1.1–1.5× | Fitout |
| Signage, wayfinding, digital displays | Any time post-opening | 1.0–1.2× | Fitout |
| Curbside lane configuration | Before curb pour | 20–50× | Structural |

**Analyst read (professional judgment):** the map tells you where the
council's leverage actually is. Roof-span, FIS envelope, MEP risers, and
modular pod dimensions all resolve *upstream of on-site pour* — which
means the DFW/AA reversibility deadline is not the concrete-cure date but
the **release-for-fabrication** date of each module. That is
weeks-to-months earlier than the public-facing "concrete cures" framing.
The council's five deliverables should each be tagged to a
release-for-fabrication milestone, not a groundbreaking date.

---

## 6. Debt-service and CPE sensitivity — bounding the room the airport has

**Sourced inputs:**

- **$3.0 billion** in new debt authorized by the 70th Supplemental Bond
  Ordinance for the March 2025 – February 2026 window (Fort Worth city
  filing).
- **$11.3 billion** CIP through FY 2030 (DWU Consulting, per DFW
  disclosures — secondary).
- DFW is on a **residual-hybrid Use and Lease structure** (context
  packet). Current CPE is not publicly confirmed in the sources reviewed
  — this is a gap the airport-CEO and airline-commercial-strategist
  agents should close.

**Arithmetic — annualized debt service on the $3B tranche:**

Using a level-debt-service assumption (standard for airport revenue bonds)
over a 30-year term:

| Interest rate | Annual level debt service |
|---|---|
| 4.5% | ~$184M |
| 5.0% | ~$195M |
| 5.5% | ~$205M |

**Passenger denominator (2025 DFW):** 85.7M total passengers ≈ **42.85M
enplaned passengers** (assuming symmetric arrival/departure split; a
convention, not a fact — DFW's official enplaned count should be
confirmed).

**CPE impact of the $3B tranche alone (all else equal):**

- 4.5%: ~$4.29 per enplanement
- 5.0%: ~$4.55 per enplanement
- 5.5%: ~$4.78 per enplanement

For scale, DFW's peer hubs commonly run CPE in the $10–18 range. A
**~$4.50 addition from one authorization tranche** is material — it is not
a rounding error, and it explains why the AA U&L structure and its MII
thresholds are the single most consequential lever in the room.

**Sensitivity — passenger downside:** if 2035 enplanements fall to 40M
(a modest recession scenario), the same $195M debt service becomes **~$4.88
CPE**. If enplanements rise to 50M by 2035, it becomes **~$3.90**. A ±20%
swing in enplanements moves this line by ~$1.00 CPE.

**Analyst read:** Terminal F is being financed at the tail end of a
period when American's DFW volume has softened (2025 passengers down
2.4% vs 2024). The break-even case rests on the 2043 U&L runway holding
the connecting-bank geometry that justified the scope. That is why the
council's fifth question — *what has to be true in 2035 for these
decisions to look wrong* — is the correct framing.

---

## 7. Asset-life vs. lease-runway arithmetic

**Sourced inputs:**

- Terminal F first-phase opening: **2027** (context packet, DFW/AA joint
  announcement).
- Full program completion: **2030** (AA newsroom, 2026-07).
- Current U&L runway: **through 2043** (2025 announcement).
- Typical terminal-building useful life for depreciation: **30–50 years**
  (industry standard; not a sourced primary claim, hence flagged).

**Arithmetic:**

- Years of guaranteed AA occupancy under current U&L, from full opening
  (2030) to expiry (2043): **13 years**.
- Fraction of a 40-year asset useful life covered by the current U&L
  (measured from 2030): **13 ÷ 40 = 32.5%**.
- Fraction covered if useful life is 30 years: **43.3%**.
- Fraction covered if useful life is 50 years: **26.0%**.

**Analyst read (professional judgment):** DFW is committing bond-financed
capital whose useful life exceeds its currently contracted revenue
runway by a factor of two or more. This is normal — airports outlive
airline agreements — but it means the reversibility map should be built
to preserve options that a **post-2043 tenant** might value differently
from American in 2026: swing-gate FIS, common-use readiness, and lounge
positions that could serve a joint-venture partner. The design decisions
that foreclose these options are the ones the council should catalog.

---

## 8. What the modular method changes about the reversibility timeline

**Sourced inputs:**

- Modular pods fabricated offsite, installed on site (Dallas Innovates;
  DFW ACI presentation).
- ~30% cost savings versus conventional construction (Dallas Innovates,
  citing DFW).

**Arithmetic — the "saved dollars" envelope:**

If $4B modular ≈ 70% of a conventional-build counterfactual, the
conventional-build cost would be ~**$5.71B**, and the savings pool is
~**$1.71B**. Even a small late-fabrication scope change consumes this
pool disproportionately: on a conventional site, a late change of ~5% of
project value costs ~5%. On a modular fabrication line, a late change of
~5% commonly consumes ~15–25% of the change budget because it triggers
resequencing across pods (analyst construction; not sourced to DFW's
program).

**Two clean, testable implications:**

1. **The reversibility budget is not on-site.** The pods absorb change
   cheaply until fabrication release; after release, they are more
   change-hostile than a stick-built terminal, not less.
2. **Design freeze cascades.** Freezing pod N locks decisions that affect
   pod N+3, because pod-line sequencing benefits from
   repeatable-tolerance manufacturing. This is the opposite of the
   "flexible modular" marketing narrative and it should be stress-tested
   by the chief-engineer.

---

## 9. Evidence gaps that would change any of the above

Named plainly, not filled with inference:

1. **AA-controlled gate count at DFW today.** Every "share of AA
   operation" calculation in §2 is bracketed pending this input.
2. **Terminal F gate mix (widebody vs. narrowbody vs. flex).** Cost per
   gate in §1 mixes gate types; the true per-widebody and per-narrowbody
   costs differ materially.
3. **Terminal F floorplate square footage.** Everything in §4 uses a
   sq-ft-per-gate benchmark from Terminal C; the Terminal F envelope
   is not disclosed.
4. **Current DFW cost-per-enplanement and MII thresholds.** §6 sensitivity
   is directional, not calibrated, without these.
5. **U&L obligations to a Flagship-tier lounge at Terminal F before
   2043.** This determines whether the analyst read in §4 is a design
   decision or an already-settled contract term.
6. **Release-for-fabrication milestone dates per pod.** §5 and §8 hinge
   on when each irreversibility window closes.
7. **Environmental clearance status for the expanded 31-gate/$4B scope.**
   Any NEPA-driven re-scope changes the arithmetic in §1 and §6.

Where the airport-context-builder cannot close these gaps, the
recommendation to the operator should be: **name them as diligence items
for the DFW Airport Board rather than paper over them with a model
number.**

---

## 10. Summary — the five thesis questions, scored quantitatively

1. **What American's premium shift implies physically.**
   The 37,000 sq ft Terminal C Admirals Club is the visible benchmark.
   Terminal F's announced Provisions grab-and-go leaves a **~30,000+
   sq ft lounge deficit** if AA's premium repositioning eventually
   demands parity — equal to ~1.6–1.9 gate positions of floorplate
   worth $207M–$285M in foregone gate value.
2. **Which decisions are irreversible.** Roof spans, FIS envelopes, MEP
   risers, modular pod dimensions, and curbside lanes are 5–100× more
   expensive to change after their respective milestones. The relevant
   deadline is **release-for-fabrication**, not concrete-cure.
3. **What the modular method makes uniquely possible.** It preserves
   savings only up to fabrication release; after release, change
   tolerance is *worse* than a conventional build, not better. The
   council should treat "modular = flexible" as a marketing claim, not a
   design property.
4. **Concrete innovations for the tail of construction or first 18
   months.** Fitout-side interventions (lounge conversion, concessions
   swap, wayfinding, digital signage) carry 1.0–2× cost multipliers
   and remain live post-pour. Structural interventions do not.
5. **What would have to be true in 2035 for these to look wrong.** A
   ~10-percentage-point drop in AA's DFW connecting share (from ~66% to
   ~55%) would force a **~50% increase in O&D-side facilities** the
   design did not price. A ±20% swing in enplanements moves the debt-
   service CPE line by ~$1. Either shift is inside the plausible band
   for a 16-year horizon.

The reversibility map is the deliverable most useful to a board reader.
The rest is the honest arithmetic that keeps it grounded.
