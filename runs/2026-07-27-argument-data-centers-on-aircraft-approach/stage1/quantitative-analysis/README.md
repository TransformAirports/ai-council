# Quantitative analysis — Data center off RWY 01L/19R at IAD

Reproducible support for the argument recommending against a data center in the
proposed location. Every number is either a cited source value or an analyst
construction derived from a cited regulatory slope/geometry. No operator data
was available; site-specific figures are flagged as gaps.

## Files

- `calculations.json` — raw inputs (with sources), formulas, outputs, sensitivities, and the operator-data gaps.
- `approach_departure_surface_height_limits.csv` — max object height vs. distance under the Part 77 50:1 approach surface and the AC 150/5300-13 40:1 departure surface. Chart: height (y) vs. distance from surface origin (x); takeaway = a 50 ft object reaches the approach surface at only ~2,500 ft.
- `glideslope_overflight_height.csv` — aircraft height AGL on a 3° approach vs. distance from threshold. Chart takeaway = within ~3,000 ft of the threshold the aircraft is below ~210 ft AGL, the control-critical band a plume or glare source would intersect.
- `wildlife_separation_shortfall.csv` — how far a runway-end stormwater pond falls inside FAA AC 150/5200-33 separation guidance.

## How to reproduce

All calculations are closed-form arithmetic from published slopes/geometry:

- Approach surface: `max_height_ft = distance_ft / 50` (Part 77, first 10,000 ft).
- Departure surface: `max_height_ft = distance_ft / 40` (AC 150/5300-13B).
- Glideslope: `height_AGL_ft = 50 + distance_ft * tan(3°)`.
- Wildlife shortfall: `required_ft − actual_ft` (required from AC 150/5200-33; actual is a placeholder pending the site plan).

Recompute with any spreadsheet; no external code required.

## Caveats

- The 50:1 approach surface assumes RWY 01L/19R is a precision-instrument runway end — confirm the approach category per end.
- Actual penetration depends on ground elevation under the structure and the true tallest-appurtenance height; the tables assume flat terrain at runway-end elevation.
- The 4.3 m/s thermal-plume threshold is CASA (Australian) guidance; the FAA has no codified numeric equivalent. It is a reference anchor, not a US standard.
- Wildlife separation is analyzed with a placeholder actual distance; replace with the surveyed distance from the site plan.
