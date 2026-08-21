# Quantitative Analysis — Terminal F 2043 Run

Reproducible supporting files for the Quantitative Analyst brief at
`outputs/stage1/quantitative-analyst-brief.md`.

## Files

- **`calculations.json`** — Every calculation used in the brief, with inputs,
  formulas, outputs, source references, and sensitivities. This is the
  canonical machine-readable record.
- **`cost_per_gate_scenarios.csv`** — Cost-per-gate table across 2023 plan,
  2025 plan, overrun sensitivity, and gate-count sensitivity. Chart-ready
  (bar chart or table). See §1 of the brief.
- **`connecting_vs_od_split.csv`** — Peak-day AA customer split at DFW under
  four connecting-share assumptions (55%, 60%, 66%, 70%). Chart-ready
  (stacked bar). See §3 of the brief.
- **`debt_service_cpe_sensitivity.csv`** — Annual debt service on the $3B
  authorization and its per-enplanement impact across three interest rates
  and two 2035 enplanement scenarios. Chart-ready (line or grouped bar).
  See §6 of the brief.
- **`reversibility_map.csv`** — Ten Terminal F design elements with the
  reversibility milestone that closes their cheap-change window, and the
  cost-multiplier band for changes made after that milestone. Chart-ready
  (dot or bar chart, log scale on cost multiplier). See §5 of the brief.

## How to reproduce

Every number in every file traces back to either (a) a primary source cited
in `calculations.json` and in the evidence JSONL at
`outputs/stage1/quantitative-analyst-evidence.jsonl`, or (b) an explicit
analyst construction labeled as such.

To rebuild the arithmetic:

1. Open `calculations.json`. Each calculation has `inputs`, `formulas`,
   `outputs`, and `caveats`. Read the input source references back to the
   evidence file to verify each number.
2. Re-run the formulas by hand or in any spreadsheet. All calculations are
   deterministic and use elementary arithmetic (division, multiplication)
   or the standard PMT loan-payment formula for the debt-service section.
3. For the debt-service CPE calculation, PMT is the standard financial
   function: `annual_debt_service = -PMT(rate, term, principal)`. For a
   $3.0B principal at 5.0% over 30 years, the level annual payment is
   approximately $195.1M.

## What is analyst construction vs. sourced fact

Labeled plainly at the calculation level in `calculations.json`. In summary:

- **Sourced**: $4B / 31 gates, $1.6B / 15 gates, 100,000 peak-day AA
  customers, 930 peak departures, 37,000 sq ft Admirals Club, 30% modular
  savings, $3B debt authorization, 85.7M passengers, U&L expiry 2043.
- **Analyst construction**: current AA gate count at DFW (bracketed range),
  Terminal C gate count (bracketed), narrowbody gate floorplate rule of
  thumb, Flagship Lounge and Delta ONE Lounge sq ft (industry reporting,
  not primary here), useful-life bands, PMT term/rate assumptions,
  reversibility map cost multipliers, Provisions grab-and-go footprint
  estimate.

The evidence JSONL contains only claims tied to verifiable documents.
Analyst constructions live in the brief and here in the README, never in
the evidence file.

## Known gaps

Listed in `calculations.json` under `known_gaps` and in §9 of the brief.
The most decision-consequential are the current AA gate count at DFW, the
Terminal F gate mix by aircraft class, and the current CPE / MII
thresholds under the residual-hybrid U&L structure.

## Charts not produced

No PNG or SVG exhibits are included with this pass. The CSVs are the
chart-ready data; the Art Director or Presentation Designer can choose
which to render. Titles, units, and takeaways for each chart are stated
in the corresponding brief section.
