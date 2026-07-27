# Infrastructure-Economist Brief — Data Centers at Airports: The Money Behind the Airside Risk

**Run:** Data Centers at Airports: Airside Risks
**Lens:** Airport capital expenditure, land economics, project ROI, opportunity cost
**Prepared for:** MWAA capital planners and policy readers
**Date:** 2026-07-21

---

## Framing: follow the money, then price the risk

The airside-risk debate is usually argued in the language of physics — plume velocity, glare angles, EMI. That is the operations-analyst's and chief-engineer's domain. My job is narrower and, I think, more uncomfortable: to show that the *economics* of a data center near an airport are structured so that the party best positioned to prevent airside risk (the developer, through cooling and backup-power design) faces the strongest financial incentive **not** to, and the party that bears the residual risk (the airport, and the flying public) captures the **smallest** slice of the value created. That asymmetry — not any single plume — is the controlling variable.

MWAA is not a bystander to this. It is a case study. In 2018 the Airports Authority sold the land under what is now one of the largest data center campuses on Earth. The economics of that decision, and what they foreclose, are the spine of this brief.

---

## 1. Key findings (numerically grounded)

1. **MWAA sold land it had bought for a runway.** In September 2018 the Authority sold 424 acres of Dulles "Western Lands" to Digital Realty for **$236.5 million** (~$558,000/acre; ~$200–207M net of costs). That parcel was part of an **854-acre tract acquired 2005–2007 to build the fourth runway and support facilities** [Source: https://www.mwaa.com/news/airports-authority-announces-sale-424-acres-western-lands-dulles-international].

2. **The value that landed on that dirt dwarfs what MWAA received.** The Digital Dulles campus is master-planned for up to **~11.7 million sq ft, 14 buildings, and ~1 GW of critical IT load across six substations** [Source: https://www.datacenterfrontier.com/cloud/article/11429999/dulles-land-buy-gives-digital-realty-runway-for-data-center-expansion]. At **~$10.7M per MW** to build a standard hyperscale facility (2025), 1 GW implies on the order of **$10 billion** of private capital — roughly **45× the sale price** — on land the airport monetized once [Source: https://www.truelook.com/blog/data-center-construction-costs].

3. **The county, not the airport, harvests the recurring value.** Loudoun's personal-property tax on data-center computer equipment grew from **$60M (FY2013) to over $800M (FY2026)**, and data centers are projected to supply roughly **45% of county tax revenue (~$1.3B of ~$2.9B) by FY2027** [Source: https://netchoice.org/jaw-dropping-numbers-loudouns-data-center-tax-revenue-could-top-real-estate-taxes-in-just-a-few-years/]. The airport captured a one-time land payment; the county captures an annuity.

4. **The "no future airport use" premise has aged poorly.** Dulles now runs **>560,000 annual operations** and the **fifth runway — approved in a 2005 FAA Record of Decision but never scheduled — is under fresh FAA review in 2025** [Source: https://www.flydulles.com/d2-projects-future-fifth-runway; https://simpleflying.com/faa-reviewing-washington-dulles-plan-5th-runway/]. Airfield land is a call option on future capacity; selling it is writing that option cheaply.

5. **Power is the binding constraint, and it prices the risk.** Northern Virginia topped **~4,900 MW** of active data-center capacity by Q1 2025 (largest market globally); Dominion's contracted data-center load jumped from **~21 GW (Jul 2024) to ~40 GW (Dec 2024)** [Source: https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10]. In a market this power-starved, the cooling and backup choices that reduce airside risk are the ones that cost the most power — so the risk-reducing option is the economically penalized option.

6. **Plume-free cooling carries a hard cost premium.** DOE estimates dry cooling costs **3–4× wet cooling to install**, and full dry cooling imposes a **25–35% power penalty** (relative PUE ~1.25–1.40 vs 1.0 for evaporative) [Source: https://www.datacenterknowledge.com/cooling/the-pros-and-cons-of-dry-coolers-for-data-centers]. Evaporative cooling — the source of visible moisture plumes and 1–5 million gallons/day of water use at hyperscale — is chosen precisely because it is cheaper and less power-hungry [Source: https://dgtlinfra.com/data-center-water-usage/].

7. **The controlling airside-risk scenario is economic, not steady-state.** Normal cooling is a modest, continuous heat source. The tail scenarios — **peak-summer evaporative operation (visible plume) and prolonged emergency generation during a grid outage (many diesel gensets firing at once)** — are where thermal and exhaust effects concentrate. Both are driven by the same power-and-water scarcity that makes mitigation expensive. That is the scenario a screening framework must size to, not the nameplate.

8. **The FAA's economic signal on plumes is weak.** US guidance (AIM 7-6-16 "Avoid Flight in the Vicinity of Exhaust Plumes"; the thermal-exhaust-plume assessment tool) is **advisory and largely qualitative** — turbulence "can extend over 1,000 ft above" a stack or tower, but there is **no mandatory quantitative velocity threshold** a developer must clear [Source: https://www.faa.gov/Air_traffic/Publications/atpubs/aim_html/chap7_section_6.html]. Absent a priced standard, the externality is unpriced, and unpriced externalities get built.

---

## 2. Evidence

### 2a. The MWAA transaction as economic archetype

The 2018 sale is the cleanest available data point on why airports lease or sell land to data centers. MWAA's own stated rationale was revenue and cost control: proceeds went into a dedicated account to **manage Dulles' cost per enplaned passenger**, restricted by federal rules to aeronautical use at Dulles only (not the Silver Line or Toll Road) [Source: https://www.mwaa.com/news/airports-authority-announces-sale-424-acres-western-lands-dulles-international]. Chief Revenue Officer Jerome L. Davis framed it explicitly as keeping Dulles "an attractive option for expanded air service."

This is the core alignment problem. Lowering CPE is a legitimate, even admirable, goal — high CPE drives carriers away. But the instrument chosen (disposing of runway-reserve land) trades a *future capacity* asset for a *present cost* relief. In 2018, with the fourth runway (1L-19R, opened 2008) complete and no imminent fifth-runway plan, that looked costless. In 2026, with operations past 560,000 and the fifth runway back in FAA review, the premise "no future airport uses envisioned" is exactly the assumption that deserved independent stress-testing — the same standard the thesis demands for plume compatibility.

To be fair to the counter-argument: the planned fifth runway sits on the **south side**, parallel to Runway 12-30, west of Chantilly [Source: https://www.flydulles.com/d2-projects-future-fifth-runway], not on the western parcel that was sold. The Western Lands sale did not directly consume the fifth-runway footprint. The point is not that MWAA paved a runway site — it is that the *category* of decision (monetizing airfield-reserve land under a "not needed" assumption) is being made across the industry precisely when demand is rising, and the assumption is rarely re-underwritten.

### 2b. The value-capture asymmetry

Three numbers, side by side, tell the story:

- **What MWAA got:** $236.5M, once, for 424 acres (2018) [Source: https://wtop.com/business-finance/2018/09/data-center-operator-to-pay-237m-for-land-near-dulles-airport/].
- **What it may have left on the table:** In December 2023, Amazon paid **$27.72M for 20 acres near Manassas Regional Airport — over $1.3M/acre**, roughly **2.5× MWAA's per-acre price** five years earlier [Source: https://www.landapp.com/post/maximizing-airport-land-with-data-centers]. Data-center land in this corridor was appreciating faster than a one-time 2018 sale could capture. (FAA grant assurances require **fair market value** for non-aeronautical land [Source: https://www.cbre.com/insights/reports/diversifying-airport-revenue-through-non-aeronautical-land-development] — but FMV prices the dirt, not the foreclosed airfield option, and not the airside externality.)
- **What the ecosystem captures forever:** ~$1.3B/year in Loudoun taxes by FY2027 [Source: https://netchoice.org/jaw-dropping-numbers-loudouns-data-center-tax-revenue-could-top-real-estate-taxes-in-just-a-few-years/], and ~$10B of developer capital [Source: https://www.datacenterfrontier.com/cloud/article/11429999/dulles-land-buy-gives-digital-realty-runway-for-data-center-expansion].

The airport sits at the bottom of this value stack while holding the top of the risk stack — it owns the airspace the plume and the gensets sit under. When a party captures little upside but retains the downside, screening discipline is the only protection, because the deal economics will always argue "yes."

### 2c. Power scarcity is why mitigation won't come free

The reason the developer's incentives cut against airside safety is the power market. PJM capacity prices for the Dominion zone rose roughly **10× (an 833% jump in the 2024 auction for 2025–26)**, clearing at the FERC cap of **$329.17/MW-day for 2026/27** [Source: https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10]. Commercial electricity sales in Virginia have surged on data-center load [Source: https://www.eia.gov/todayinenergy/detail.php?id=67664]. In that environment, a **25–35% power penalty for dry cooling** is not a rounding error — it is the difference between a viable and unviable pro forma. So developers default to evaporative cooling (cheaper, less power, but visible plume and 1–5 MGD water) and to large diesel/gas backup fleets (cheaper than the grid interconnection they often can't get fast enough). Every one of those cost-minimizing choices pushes airside risk up. That is the mechanism the screening framework must counter, because the market will not.

### 2d. The regulatory price signal is missing

The FAA does treat exhaust plumes as a flight hazard — AIM 7-6-16 warns pilots away from stacks and cooling towers, and research cited by FAA finds turbulence can extend **>1,000 ft above** the source [Source: https://www.aopa.org/news-and-media/all-news/2010/august/05/thermal-plumes-a-potential-danger-near-airport]. The FAA also publishes a thermal-exhaust-plume assessment tool [Source: https://www.faa.gov/sites/faa.gov/files/airports/environmental/land_use/Technical-Guidance-Assessment-Tool-Thermal-Exhaust-Plume-Impact.pdf]. But the guidance is advisory and qualitative; obstruction evaluation (Form 7460-1) is keyed to physical **surfaces**, not thermal or exhaust behavior. There is no mandatory pass/fail plume-velocity number a US developer must clear near an airport that I could verify. From an economist's view, that is an **unpriced externality**: the cost of airside risk is borne by aviation, not internalized by the data center, so the market over-produces it. Land-use compatibility (FAA AC 150/5190-4B) is the lever, but it is exercised locally and inconsistently [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150_5190_4b_Land_Use_Compatibility.pdf].

---

## 3. Implication for the MWAA screening framework (economics module)

A defensible screen should force the deal economics to reveal the risk they'd rather not price:

1. **Require a dry-cooling / plume-abated cost delta from the applicant.** If the developer argues evaporative cooling is necessary, make them quantify the capital and power premium of the plume-free alternative. That converts a physics dispute into a number MWAA can weigh against airfield value.
2. **Underwrite the foreclosed-capacity option explicitly.** Any land within potential runway-extension, RPZ, or future-ALP reach should be valued as an option, not a vacant lot. If MWAA disposes of it, the memo should state the capacity being written off and why it will never be needed — and survive an independent review, not an internal assumption.
3. **Size to the controlling scenario, not nameplate.** Base compatibility findings on **peak-summer evaporative operation and prolonged emergency generation simultaneously**, because that is the worst realistic thermal/exhaust load and it is driven by the same grid stress that is now chronic in this corridor.
4. **Price the externality into the ground lease.** Structure rent or covenants so that plume-reducing design (dry cooling, cleaner/quieter backup, generator run-hour caps) is contractually required or financially rewarded — internalizing what the FAA does not mandate.

---

## 4. Caveats and limitations

- **I did not model plume physics.** Whether a given plume actually reaches a hazardous velocity at approach altitude is an engineering question; my claim is only about incentives and unpriced risk. Do not conflate visible vapor with aerodynamic turbulence — the thesis rightly warns against this, and my economic argument does not depend on any single plume being dangerous.
- **No US case of a data-center approval denied for plume/thermal reasons was found.** The absence may mean the risk is genuinely minor, or that the screen simply isn't being applied. I cannot distinguish these from public data. This is an honest gap.
- **The "$10B" and "45×" figures are order-of-magnitude.** They multiply a planned 1 GW by a market-average $/MW build cost; actual Digital Dulles spend is not publicly itemized, and much of that capital is IT equipment, not real estate value MWAA could have captured. Treat as illustrative of the value stack, not a precise foregone gain.
- **The Manassas per-acre comparison is imperfect.** Different year (2023 vs 2018), parcel size, entitlements, and buyer. It shows the *direction* of land-value appreciation, not that MWAA mispriced the 2018 sale, which may have been fair value at the time under FAA FMV rules.
- **I could not verify a specific FAA vertical-velocity threshold** (e.g., the ~4.3 m/s figure sometimes cited from UK CAA practice). US guidance appears to lack a mandatory numeric standard; I state that as a finding, not an assumption.
- **Federal revenue-use rules cut the other way too.** MWAA's proceeds were legally confined to reducing Dulles CPE — a genuine benefit to carriers and passengers. The counter-case (this was good stewardship of otherwise-idle land) is real and should be argued at full strength.

---

## 5. Verbatim data points for the strategist

1. *"MWAA sold 424 acres it had bought to build a runway for $236.5 million; the campus now planned on that land is master-planned for up to 1 gigawatt of IT load — implying roughly $10 billion of private capital, about 45 times the sale price. The airport captured the smallest slice of the value chain and kept the airside risk."* [Sources: https://www.mwaa.com/news/airports-authority-announces-sale-424-acres-western-lands-dulles-international; https://www.datacenterfrontier.com/cloud/article/11429999/dulles-land-buy-gives-digital-realty-runway-for-data-center-expansion]

2. *"By FY2027, data centers are projected to supply about 45% of Loudoun County's tax revenue — roughly $1.3 billion of $2.9 billion. The county gets an annuity; the airport got a one-time check."* [Source: https://netchoice.org/jaw-dropping-numbers-loudouns-data-center-tax-revenue-could-top-real-estate-taxes-in-just-a-few-years/]

3. *"Dry cooling — the option that eliminates the visible plume — costs 3 to 4 times as much to install and carries a 25–35% power penalty. In a market where PJM capacity prices just rose roughly tenfold, the plume-free choice is the one the developer can least afford. That is why the risk-reducing design is the economically penalized design."* [Sources: https://www.datacenterknowledge.com/cooling/the-pros-and-cons-of-dry-coolers-for-data-centers; https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10]

4. *"Dulles now runs more than 560,000 operations a year, and a fifth runway approved in a 2005 FAA Record of Decision is back under federal review in 2025. 'No future airport use envisioned' is an assumption, not a fact — and it is the assumption airfield-reserve land is sold on."* [Sources: https://www.flydulles.com/d2-projects-future-fifth-runway; https://simpleflying.com/faa-reviewing-washington-dulles-plan-5th-runway/]

5. *"The FAA warns pilots that exhaust-plume turbulence can extend more than 1,000 feet above a cooling tower or stack — but there is no mandatory numeric plume standard a developer must clear near a runway. An unpriced externality gets over-produced. That is not a physics problem; it is a market-design problem."* [Source: https://www.aopa.org/news-and-media/all-news/2010/august/05/thermal-plumes-a-potential-danger-near-airport]
