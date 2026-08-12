# Quantitative Analysis — Quiet-by-Design Standards for MWAA Terminals

This folder contains the reproducible quantitative work behind
`outputs/stage1/quantitative-analyst-brief.md`. The brief is the analytical
argument. These files are the arithmetic.

## Files

- `calculations.json` — every exhibit with inputs (labeled SOURCE, ASSUMPTION,
  or COMPUTED), formulas, outputs, and caveats. Read this first.
- `e1_design_vs_retrofit_cost.csv` — acoustic treatment unit costs and totals,
  new-build vs retrofit, sized to Concourse E's 435,000 sqft envelope.
- `e3_intelligibility_criteria.csv` — code and consensus intelligibility
  thresholds a MWAA standard would inherit, plus the analyst's translation.
- `e4_announcement_burden.csv` — announcement-density arithmetic contrasting
  US-hub baseline practice with the Helsinki/London City reduced-PA model.
- `e6_cpe_sensitivity.csv` — cost-per-enplanement impact of the incremental
  capital stack under low, high, and doubled-capex scenarios.
- `e7_iad_vs_dca_context.csv` — the physical and operational deltas that force
  common-requirement / different-prescription design between the two airports.

Six earlier CSVs (`accessibility-coverage.csv`, `announcement-load.csv`,
`compliance-thresholds.csv`, `concourse-e-cost-sensitivity.csv`,
`cpe-sensitivity.csv`, `macleamy-change-cost.csv`) are prior scratch outputs
kept for continuity; the authoritative exhibit CSVs are the `e1_…` through
`e7_…` files listed above.

## How to reproduce

Every number in the CSVs is either (a) traceable to `calculations.json` under
its exhibit `id`, which lists the source or the assumption, or (b) computed
from those inputs by the stated formula. Recomputing:

```
IAD_2025_enplanements ~= 29.01M / 2 = 14.5M    # order-of-magnitude only
DCA_2025_enplanements ~= 24.89M / 2 = 12.45M   # order-of-magnitude only
CPE_impact = (capex * 0.075) / (14.5M + 12.45M)
retrofit_premium_per_sqft = retrofit_unit_cost - new_build_unit_cost
PA_duty_cycle = (announcements_per_boarding * duration_sec) / 3600
acoustic_share_of_program = new_build_acoustic_cost / concourse_E_budget
```

No spreadsheet is required; the arithmetic is deliberately elementary. That
is the point: if the number is fragile, the fragility is in the input, not
the math.

## What is missing and what would replace it

The `evidence_gaps` array in `calculations.json` lists five items that would
turn assumption-driven numbers into measured ones. The three that matter
most:

1. Existing acoustic surveys of IAD and DCA holdrooms (measured STI, LAeq,
   RT60). MWAA Engineering likely holds these for recent construction
   packages.
2. PA telemetry — announcements per hour, per gate, by category — from
   MWAA's paging system. This collapses Exhibit E4 from assumption to fact.
3. Airline gate-by-gate missed-boarding logs. Without these, the
   operational downside of a reduced-PA standard cannot be quantified.

Once operator data is available, the JSON's `ASSUMPTION` labels are the
exact lines to replace.

## What is not in this folder

No PNG or SVG charts. The strongest exhibits here are the criteria table
(E3), the design-vs-retrofit cost delta (E1), and the CPE sensitivity (E6).
Each is table-shaped and reads better in the brief as a compact table than
as a rendered chart. A chart would decorate, not clarify.
