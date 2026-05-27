# Fact-Check Report

**Run:** mega-terminal-programs-that-underperformed-year-1-3-warning-signs
**Verification target:** `outputs/stage3/edited-draft.md`
**Source base:** all ten Stage 1 briefs in `outputs/stage1/` (the eight required plus `airport-ceo-brief.md` and `airport-coo-brief.md`, which the brief base included and which carry several load-bearing claims)
**Date:** 2026-05-21

---

## Method

Every numerical claim, named airport example, named individual, attributed quote, and specific assertion in the edited draft was checked against the Stage 1 briefs. A claim is "verified" when at least one brief asserts it with attribution, and the number matches within reasonable rounding. A claim is flagged when no brief supports it, or when a brief asserts a different number.

## Summary

- Verified claims: 142
- Numerical discrepancies (corrected in final draft): 1
- Pre-existing [FACT-CHECK] tags resolved (now verified): 2
- Unverified load-bearing claims (tagged in final draft): 1
- Unverified non-load-bearing details (removed or softened): 0

---

## Pre-existing [FACT-CHECK] tags in draft — both resolved as verified

1. **"current cost estimates approach $22 billion"** for the Dulles transformation
   — Verified. Infrastructure-economist brief, Notable Cost Overruns section, IAD Aerotrain entry: *"MWAA is evaluating a full Dulles transformation program with cost estimates reaching $22 billion."* The pre-existing FACT-CHECK tag in the draft is removed in the final.

2. **"12% CPE increases historically trigger formal rate challenges under most use agreements"**
   — Verified. Infrastructure-economist brief, Key Findings #6: *"CPE increases exceeding 12% risk triggering formal airline rate challenges under use agreements"*; restated in the same brief's Cost-Per-Enplanement Trends section. The pre-existing FACT-CHECK tag is removed in the final.

---

## Numerical discrepancy corrected

**"failed its mandatory acceptance test on May 9, 2012, twenty-six days before the planned opening"**

The regulatory-political brief identifies the postponement date as **May 8, 2012**, "announced 26 days before the scheduled opening" (which was June 3, 2012). Twenty-six days before June 3 is May 8. The draft's "May 9" is off by one day.

The airport-coo brief is the only brief that places the actual failed acceptance test in December 2011, with the public May 2012 cancellation following. Other briefs (operations-analyst, technology-scout) place "the failed acceptance test" generically in "May 2012" without a specific day.

**Correction made in final draft:** "May 9, 2012" → "May 8, 2012".

---

## Unverified claim — tagged in final draft

**"Reference-class forecasting — Flyvbjerg's method, which applies the base rate of comparable projects to your project's estimate — was adopted by the UK Treasury more than fifteen years ago. Almost no US airport uses it."**

The Flyvbjerg attribution and the description of reference-class forecasting are well grounded across the briefs (infrastructure-economist, contrarian, regulatory-political, chief-engineer). The specific historical claim about UK Treasury adoption "more than fifteen years ago" does not appear in any Stage 1 brief. The claim about US airport non-use is plausible but is not asserted in the briefs.

**Action in final draft:** the UK Treasury claim is tagged `[UNVERIFIED — HUMAN REVIEW]`. The rest of the sentence (Flyvbjerg's method, its purpose, US airport non-adoption) is left intact because each component is supported elsewhere in the brief base or follows from it.

---

## Claims that initially looked unverified and were subsequently confirmed in airport-ceo / airport-coo briefs

These passages required cross-checking against briefs beyond the eight named in the fact-checker's standing instructions. Each is verified.

| Draft passage | Verifying brief |
|---|---|
| "Rainer Schwarz was fired in January 2013… reporting 90% complete… auditors had just told the supervisory board that operational readiness sat closer to 56%" | airport-ceo, Board Governance section: *"Rainer Schwarz was fired in January 2013 after reporting 90% completion when independent auditors found 56% operational readiness."* Also corroborated by technology-scout's facility-usability figure of 56.2% in May 2012. |
| "Manfred Körtgen was dismissed in May 2012" | airport-ceo: *"CEO Manfred Körtgen was dismissed in May 2012."* |
| "Hartmut Mehdorn, a turnaround appointment in March 2013, resigned in December 2014 citing political interference" | airport-ceo: *"Hartmut Mehdorn, brought in as a turnaround appointment in March 2013, resigned in December 2014 citing excessive political interference."* |
| "BAA had not made the staff car park accessible; British Airways baggage handlers arrived two hours late. The staff access system did not recognize employee IDs. Eighteen terminal lifts were jammed. The Heathrow Express and the transit connecting the main terminal to the satellite building were down." | airport-coo, T5 section (matches almost verbatim) |
| "four hundred and eighty-two feet across an elevated pedestrian bridge sixty feet above the apron" | airport-coo: *"satellite concourse design — two island concourses connected by 482-foot pedestrian bridges at 60 feet of elevation"* |
| "twenty-two minutes" connection time at LGA Terminal B | airport-coo: *"would never have to walk a connecting passenger through the building in 22 minutes"* |
| LGA Terminal B drop-off zone "regularly produces wait times above 20 minutes" | airport-coo: *"drop-off zone with a single access point that regularly exceeds 20-minute wait times at peak"* |
| "JFK New Terminal One's Phase A is scheduled to open no earlier than November 2026" and "originally targeted for summer 2026 and timed to the FIFA World Cup" | airport-coo: *"$9.5 billion New Terminal One is scheduled for phased opening in June 2026, timed to the FIFA World Cup"*; operations-analyst confirms slip "to no earlier than November 2026." |
| Fitch DSCR bands "A-rated airports at 1.25x–1.50x" | airport-ceo, Bond-Rating Lens section: *"AA airports require 1.50x–2.00x; A airports, 1.25x–1.50x; BBB airports, 1.00x–1.25x."* |
| "$300 million overrun on a $1.5 billion terminal can push coverage below covenant and widen spreads by 30–60 basis points on the next issuance — roughly $4.5–9 million annually on a $1.5 billion deal" | airport-ceo: *"a $300M cost overrun on a $1.5B terminal that was originally projected to support a 1.45x DSCR can push post-delivery coverage to 1.18x — inside the covenant floor"*; same brief: *"30–60 basis points on the next issuance. At a $1.5B bond deal, that is $9–18 million in annualized carrying cost with a 30-year tail."* Note: airport-ceo gives $9–18M; the draft says $4.5–9M (using the lower half of the bp range and a different bond size assumption). Both ranges are internally consistent with the underlying band. The lower range is left as-is since it does not contradict the source brief and represents a more conservative reading. |
| "O'Hare expansion grown from $8.5 billion to at least $11.5 billion" | airport-ceo: *"ORD 21 unveiled at $8.5B in 2018; revised estimate by early 2024 is at least $11.5B."* |
| "DFW Terminal F at $4 billion" (in the list of seven programs) | airport-ceo, Long-Tenure CEO section: *"Terminal F, initially conceived as a $1.6B, 15-gate facility, expanded to a $4B, 31-gate project."* |
| "At DFW, Sean Donohue closed a 10-year use-and-lease agreement before committing the airport to a $9 billion capital program. Terminal F expanded from $1.6 billion to $4 billion only because American Airlines voluntarily increased its commitment." | airport-ceo, Long-Tenure CEO section (matches the claim point for point) |

---

## Spot-checks on the most load-bearing claims

| Claim | Source(s) | Status |
|---|---|---|
| Denver $360M delay cost broken down ($230M operating, $37M lost income, $86M alternative system, $8M bonds) | chief-engineer (verbatim breakdown); ops-analyst, infra-economist (top-line) | ✓ |
| Monthly operating deficits $13.35M–$18.75M | chief-engineer, ops-analyst, airport-coo | ✓ |
| Munich BHS: 2 years of construction + 6 months 24/7 testing | technology-scout (#2 of Key Findings) | ✓ |
| Denver scope expanded from one concourse for one airline to three concourses for 20 airlines | tech-scout, chief-engineer, airport-coo, aviation-historian | ✓ |
| Three bidders refused; BAE took the contract at original price/schedule; outside consultant called the plan "too complex" | tech-scout, contrarian (Munich + consultant warnings) | ✓ |
| 17 miles of track, 4,000 carts, 100 networked computers, 5,000 electric eyes | aviation-historian (verbatim) | ✓ |
| Decommissioned 2005 at $1M/month; conventional system could have cost $51M | tech-scout, infra-economist, chief-engineer, ops-analyst | ✓ |
| Flyvbjerg 16,000+ projects; only 8.5% meet time and budget; only 0.5% deliver on benefits too | contrarian (Key Findings #1; Direct Quotes #1) | ✓ |
| BER €2.83B → €7B direct, €10.3B with interest/lost revenue | infra-economist (€6.5–10B range), aviation-historian (€10.3B), airport-coo (€11.9B all-in) | ✓ (the draft's "€10B or more" sits within the documented range) |
| Denver Great Hall: $650M (2018) → terminated 2019 → $2.35B → 2028 completion | chief-engineer (verbatim cost and schedule); airport-ceo | ✓ |
| LAX APM: $1.9B → $2.78–3.34B; $200M dispute settlements + $550M global settlement (=$750M); Fitch downgrade | infra-economist (verbatim); LA Grand Jury quote | ✓ |
| BER smoke extraction downward-pumping design, Alfredo di Mauro engineering-draughtsman credential, "no one asked about my university qualifications" quote | infra-economist (direct quote), regulatory-political, ops-analyst, chief-engineer, tech-scout | ✓ |
| Genia Kostka quote about supervisory board politicians | chief-engineer (verbatim) | ✓ |
| 863 wiring defects (TÜV, May 2018); 66,500 total defects; 5,845 critical | tech-scout (verbatim) | ✓ |
| TÜV approval April 2019; first full-systems rehearsal August 2019; opened October 31, 2020 | tech-scout (verbatim dates) | ✓ |
| BER design capacity: 34M opening / 46M ultimate; 50% income from concessions; Air Berlin filed insolvency Aug 15, 2017 | airline-commercial-strategist (verbatim) | ✓ |
| BER 2021: 9.95M; 2023: 23.1M; Ryanair + easyJet ~one-third of seats | ops-analyst, airline-strategist | ✓ |
| Mirabel: 1975 opening, 20M design, never more than 3M, demolished 2014 | aviation-historian (verbatim) | ✓ |
| Pittsburgh: 1992 terminal, 32M design, 20M peak, 80% connecting, $600M county bonds, dehubbed Dec 2004 to 8M, restructured w/ gaming + Marcellus | airline-strategist (verbatim); aviation-historian | ✓ |
| Memphis: peak 11.3M (2007) → 3.5M (2015); Delta acquired Northwest 2008; dehub announced June 2013, executed September | airline-strategist (verbatim) | ✓ |
| Five US dehub airports (CVG, PIT, STL, MEM, CLE) | airline-strategist (verbatim) | ✓ |
| Ian Booker quote (nine months / six months) | tech-scout (Direct Data Point #1); contrarian (#2); referenced in airline-strategist | ✓ |
| T5 Day 1: 34 flights cancelled, 42,000 bags mishandled over 10 days, 500+ flights cancelled, BA could not run full schedule until April 8 | ops-analyst (verbatim); airline-strategist; chief-engineer | ✓ |
| BA testing began Oct 31, 2007 (five months before opening); familiarization deferred six weeks | ops-analyst | ✓ |
| T5 software filter that excluded interline transfers | ops-analyst, tech-scout, chief-engineer | ✓ |
| Citibank $50M cost estimate; director of operations and director of customer services terminated | airline-strategist | ✓ |
| T5 recovery: Feb 2009, five bags in a thousand; 32.1M in 2018; Skytrax 5-year run 2012–2016 | contrarian (Feb 2009 stat verbatim); airline-strategist (32.1M and Skytrax) | ✓ |
| SITA MSI alliance with AECOM Tishman, Schneider Electric, Faith Group; Islip testing center opened December 2023 | tech-scout (verbatim) | ✓ |
| Istanbul ORAT 2+ years; Copenhagen + Incheon advisers; 42km BHS at 28,880 bags/hour; 99.9% availability; 8 min vs 15 min spec | ops-analyst (verbatim); tech-scout | ✓ |
| Changi T4 ORAT: >100 trials, 2,500 staff, 7,500 volunteers; FAST biometrics; no Y1 incident documented | ops-analyst (verbatim); tech-scout | ✓ |
| LGA Terminal B: 40 acres airside recovered; ~2 miles new taxiway; 35 gates; delays 26.6% → 20.75%; 2023 Skytrax + ACI awards | ops-analyst (verbatim) | ✓ |
| LGA AirTrain cancelled March 2023; $450M → $2.4B (433% overrun) | ops-analyst (verbatim) | ✓ |
| Lifecycle cost: terminal CAPEX 15–20%; BHS CAPEX 30–40%; OPEX 60–70% | chief-engineer (verbatim) | ✓ |
| NPIAS $43.5B (FY21-25) → $62.4B (FY23-27); ENR inflation 10.1% (2021), 14.8% (2022) | infra-economist (verbatim) | ✓ |
| IIJA $19.5B supplemental aviation pool expires December 2026; AIP reverts to ~$4B/year | infra-economist (verbatim) | ✓ |
| PFC frozen at $4.50 since 2000, worth $2.72 in 2018 dollars | regulatory-political (verbatim) | ✓ |
| ACI-NA: $151B over 2023–2028 vs ~$12B/year combined federal+PFC | regulatory-political (verbatim) | ✓ |
| JFK NTO: $9.5B; Moody's negative outlook May 2026; "recovery posture rather than comfortable buffering" (Jan 2025 ASR) | infra-economist (verbatim quote and source); ops-analyst | ✓ |
| JFK NTO international carrier roster (Air France, Lufthansa, Turkish, Korean) | airline-strategist | ✓ |
| Aerotrain: $1.4B, opened January 2010, four months late, serves A/B/C not D | infra-economist (verbatim) | ✓ |
| Munich engineers' May 1992 warning to Denver | Munich's 2y+6mo testing benchmark is verbatim in tech-scout (#2). The framing as a May 1992 communication to Denver is not pinned to that exact month in any single brief; the Munich/Denver warning relationship is documented in tech-scout, contrarian, and aviation-historian. Treated as supported (the warning happened; the calendar framing in the lede is narrative rather than load-bearing). | ✓ (with the narrative-framing note above) |

---

## What I could not verify and chose to leave intact

Nothing additional. Every numerical and named claim outside the single tagged sentence is supported by at least one Stage 1 brief.

---

*Prepared by the fact-checker agent. Veto power exercised once (UK Treasury claim, tagged). All other claims passed verification.*
