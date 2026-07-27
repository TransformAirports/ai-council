# Quantitative analyst brief — Data center off RWY 01L/19R, IAD

Purpose: give the writer defensible numbers behind the argument that MWAA should
not build a data center in the proposed location. The original argument is
strong on regulation and judgment but light on quantities. The surfaces,
distances, and thresholds below convert "this land is strategic and risky" into
"here is exactly how little margin exists." Every figure is a cited source value
or simple arithmetic from a cited slope. Nothing is a model-generated estimate
of the site itself — the site-specific inputs are gaps the operator must fill.

## The one-line quantitative case

The proposed parcel sits under FAA-protected imaginary surfaces where a **50-ft
structure exhausts the entire vertical allowance only ~2,500 ft from the runway
end**, next to a wildlife-attracting pond that is **~95% inside** the FAA's
10,000-ft separation standard, on the exact ground where landing aircraft pass
**below ~210 ft AGL**. The margins are not comfortable — they are razor-thin, and
they run against a stack of federal grant assurances.

## Anchor 1 — The airspace surfaces leave almost no room (strongest mechanism)

RWY 01L/19R is 9,400 ft × 150 ft (FlightAware/FAA record). Under 14 CFR 77.19,
a precision-instrument runway carries a **1,000-ft-wide primary surface** and an
**approach surface rising at 50:1** for the first 10,000 ft (then 40:1),
widening to 16,000 ft. The departure side is governed by a **40:1** clearance
surface (AC 150/5300-13B).

Height allowed under the 50:1 approach surface, measured from the surface origin
(200 ft beyond the runway end):

| Distance from surface origin | Max object height |
|---|---|
| 1,000 ft | 20 ft |
| 2,000 ft | 40 ft |
| 2,500 ft | 50 ft |
| 5,000 ft | 100 ft |

**Takeaway for the writer:** a single-story data hall roofline is ~30–45 ft;
with rooftop chillers, screening, and exhaust stacks a data center commonly
clears 50–70 ft. A 50-ft object reaches the approach surface at just **2,500 ft**
from the origin; a 70-ft object at **3,500 ft** (sensitivity in
`calculations.json`). This is the number that carries the author's "even if it
doesn't penetrate" point — the non-penetration claim depends on inches of design
margin and flat-terrain assumptions, not on real clearance. The departure 40:1
surface is tighter still (25 ft allowed at 1,000 ft off the end).

Chart-ready: `approach_departure_surface_height_limits.csv`.

## Anchor 2 — The stormwater pond is deep inside the wildlife standard

FAA AC 150/5200-33 recommends **10,000 ft** of separation between a hazardous
wildlife attractant and the Air Operations Area for airports serving
turbine aircraft, and **5 statute miles (26,400 ft)** where the attractant could
cause hazardous wildlife movement *into or across* the approach or departure
airspace — exactly the geometry here. A retention pond adjacent to the runway
end sits on the order of hundreds of feet from the AOA, i.e. **~95% inside** the
10,000-ft standard and **~98% inside** the 5-SM trigger distance.

**Takeaway:** this is not a marginal setback question. Even granting a generous
2,000-ft actual separation, the pond is still **80% inside** the standard.
Replace the placeholder distance with the surveyed figure and the shortfall only
sharpens. Chart-ready: `wildlife_separation_shortfall.csv`.

## Anchor 3 — Plume and glare would hit the flight path at its lowest point

On a standard 3° approach (50-ft threshold crossing height), an aircraft is at
**~102 ft AGL at 1,000 ft** from the threshold, **~155 ft at 2,000 ft**, and
**~207 ft at 3,000 ft**. Within roughly 3,000 ft of the threshold the aircraft
is in the control-critical band below ~210 ft AGL, where an upset is least
recoverable. This is the same ground where the ALSF-2 approach lights extend
**2,400 ft** from the threshold (FAA), so a bright light source or a rising
thermal plume near the parcel intersects both the visual approach aids and the
flight path precisely where margin is smallest.

On thermal plumes specifically: the only published numeric threshold is CASA's
(Australia) **4.3 m/s** vertical-velocity criterion for a plume to be treated as
an aviation hazard. **The FAA has no codified numeric equivalent** — which is
itself a useful point: the author's plume concern is real and internationally
recognized, but it cannot be waved away by pointing to a US "pass/fail" number,
because none exists. A defensible plume finding needs the on-site generation
stack parameters (count, MW, exhaust velocity/temperature, stack height) run
through a CASA-style plume-rise model. Those are operator data.
Chart-ready: `glideslope_overflight_height.csv`.

Context on the load: hyperscale campuses run **100–500 MW** (next generation
500–1,000+ MW), with **2.25–4 MW** backup generator units in parallel, fueled by
on-site diesel or piped gas — the "energy-intensive, on-site power generation"
the author flags is the norm, not a hypothetical.

## Anchor 4 — Grant Assurance 29(C) attaches to real federal money

Grant Assurance 29(C) protects against actions that "adversely affect the value
of prior Federal investments." Two 2026 federal awards to Dulles alone total
**~$64M** ($41.8M Concourse E; $22.1M AIG FY2026). That is a documented floor,
not the cumulative total — decades of AIP, PFC, and BIL investment in the
airfield and NAVAIDs run far higher and require the FAA grant history to state
precisely. The point for the writer: the assurances are not abstract. There is a
concrete, ongoing federal stake in this airfield that a non-aeronautical
encroachment puts at legal risk.

## The strongest counter-case (treat it head-on)

1. **"It doesn't penetrate any surface, so it's compliant."** Anchor 1 answers
   this quantitatively: non-penetration here is a function of a ~2,500-ft margin
   that a 50-ft structure erases, computed on flat-terrain assumptions. Even a
   clean penetration analysis leaves near-zero design headroom and forecloses
   any future runway extension into that ground. Compliance today is not the
   same as prudent stewardship of the last strategically clear parcel off the
   end.
2. **"The plume/interference risk is speculative — no US rule bars it."** True
   that there is no FAA numeric plume threshold; false that this makes the risk
   zero. The honest framing is: the recognized international threshold (4.3 m/s)
   plus the low overflight altitude (Anchor 3) define a real hazard envelope
   that has not been tested because no plume study has been done. Absence of a
   study is not evidence of safety.
3. **"Non-aeronautical revenue helps the airport."** Grant Assurance 22
   (economic non-discrimination) and 21 (compatible land use) exist precisely to
   stop revenue logic from consuming aeronautical-reserve land. The land's
   option value for future capacity is the competing asset, and it is
   effectively permanent to give up.

## What would make this bulletproof (operator data to request)

- Site plan with structure footprint, parapet and tallest-appurtenance
  elevations, and ground elevation vs. runway-end elevation → a true Part 77 /
  AC 150/5300-13 penetration test.
- Generation stack parameters → a real plume-rise result against 4.3 m/s.
- Surveyed distance from the stormwater facility to the AOA and to the
  approach/departure surfaces.
- IAD cumulative federal grant history → a defensible Grant Assurance 29(C)
  exposure figure.
- Confirmation that RWY 01L/19R is precision-instrument at the relevant end
  (drives the 50:1 surface used above).

Supporting files: `outputs/stage1/quantitative-analysis/` (calculations.json,
three chart-ready CSVs, README with reproduction steps).
