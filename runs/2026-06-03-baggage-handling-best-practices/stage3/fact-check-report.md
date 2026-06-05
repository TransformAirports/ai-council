# Fact-Check Report: Stage 3 Edited Draft

**Council Run:** Baggage Handling Best Practices
**Stage:** 3 — Fact-checker pass
**Date:** June 3, 2026

---

## Scope and method

This report verifies every numerical claim, attributed quote, named example, and specific assertion in `outputs/stage3/edited-draft.md` against the Stage 1 research briefs.

The user's instruction listed eight briefs to consult by name. The `outputs/stage1/` directory contains twelve. Because the Strategist and Editor demonstrably drew from briefs beyond the eight (notably `airport-ceo-brief.md` for credit metrics and `airport-coo-brief.md` for the BER 2025 cyberattack), this report verifies against the full Stage 1 corpus and notes in each case which brief carries the source. Claims supported only by briefs outside the named eight are noted as such.

---

## Counts

- **Total discrete factual / numerical / attributed claims checked:** 87
- **Verified against Stage 1 briefs:** 81
- **Unverified or unable to source:** 4
- **Suspected errors / phrasing mismatches:** 2
- **Already flagged in draft with `[FC: confirm]` (4 instances) — all subsequently verified:** 4

---

## Verified claims (sampled)

The following classes of claim were verified against the briefs and do not require further detail here:

- **T5 opening narrative.** Date (March 27, 2008), 28,000 stranded bags, 500 cancelled flights, Vanderlande 12,000 bags/hour rating, £4.3 billion building, twenty-year planning horizon, BA's £10M demand against BAA, the testing-filter root cause, six-week deferral of BA familiarization, Willie Walsh's Transport Committee quote, the 2007 BHS project-team paper quote — all verified (Operations, Infrastructure Economist, Tech Scout, Chief Engineer, Aviation Historian).

- **Denver case.** $193M original contract, 17 miles of track, 4,000 DCVs, 100 computers, 5,000 photo eyes, 400 radio receivers, 56 barcode scanners, scope expansion to 20 carriers, February 1995 opening, GAO RCED-95-35BR's $360M aggregate, $230M operating deficits, $37M foregone income, $8.3M underwriting fees, $1.1M/day debt service, $1M/month maintenance, 2005 United decommissioning, $520–600M total spend, Jeff Green's "level of quality customer service" quote, the GAO "city of Denver initially planned to open DIA with a conventional baggage system" quote, the Munich-warned-Denver story — all verified (Chief Engineer, Infrastructure Economist, Operations, Airline Commercial Strategist, Tech Scout, Aviation Historian).

- **Chek Lap Kok.** July 6, 1998 opening, simultaneous system collapse across baggage / FIDS / parking / cargo, HACTL July 7 shutdown, Kai Tak reactivation through August, ~10,000 misrouted bags, £102M HK Financial Secretary damage estimate, LegCo TAMS-not-commissioned finding — all verified (Operations, Infrastructure Economist, Chief Engineer, Tech Scout, Slacker).

- **KLIA.** Five-days-before-Hong Kong opening — verified (Operations).

- **Berlin Brandenburg.** October 31, 2020 opening, nine years late, €6.5B vs €2.8B initial estimate, smoke-extraction designer credential issue, TÜV 2014 catalog of 75,000+ defects, ~120,000 defects through opening day, 15,000 trial bags before BHS opening — all verified (Operations, Tech Scout, Contrarian, Infrastructure Economist).

- **Munich T2 ICS.** 2003 commissioning, 22 years of operation, 99.9% availability (vendor-self-disclosed), 8–10 minute mean time to repair, breakdowns once every ~8 years, 20,000 BPH peak, passenger growth from 25M to 41M annually, expansion of track from 40 to 45 km — all verified (Tech Scout). The Frankfurt 1972 ICS continuous-operation claim is verified in Operations.

- **Architecture trade-offs.** Tilt-tray 5,000–6,000 BPH per loop; cross-belt 2.5 m/s ceiling at 4,000–4,500 BPH; ICS tote ~48" vs bare bag 30" and the ~25% EDS throughput penalty; ICS energy at ~1/3 of conventional conveyor — all verified (Tech Scout, Chief Engineer, Contrarian).

- **Read-rate and EBS data.** IATA barcode 75–85% field vs 95–99% vendor spec; Schiphol RFID 94.1% vs 99% target; MAA PEGS 16.2 5% misread acceptance; 90 bags/hour at 1,800 BPH induction × 5% — all verified (Operations, Contrarian).

- **ACRP 252 lifecycle.** 15–20% initial purchase and installation; 30–40% capital broadly defined; 60–70% OPEX; ~10%/year annual maintenance — all verified (Infrastructure Economist, Chief Engineer).

- **Commissioning standards.** Changi T3 1M+ test bags / 90-day ORAT; Changi T4 100+ trials with 2,500 staff + 1,500 volunteers / 1M+ bags / Oct 2017 opening; Newark Terminal A 30 trials over 6 months / 3,000 bags / 700 trial passengers; Munich T1 satellite 32 trial days over ~2 months; IATA ORAT 4-month minimum — all verified (Operations, Tech Scout).

- **BEUMER 10-minute outage → ~6,000 unresolved bags.** Verified (Operations).

- **Asia / Americas / Europe mishandling.** 3.1 / 5.5 / 12.3 per 1,000 passengers; 88% RFID adoption in China and North Asia vs ~40% in Europe — verified (Contrarian).

- **Seattle-Tacoma.** 10 miles conveyor / 3,000 motors / 28 CTX machines / ~60M annual passengers / 12-year three-phase ~$1B — verified (Chief Engineer, Operations, Contrarian).

- **Melbourne.** $500M international BHS replacement / 1,800 → 4,000+ BPH / 12–13M → 24–25M passenger target / 1,400-bag dynamic bag store — verified (Operations, Contrarian, Tech Scout).

- **Pittsburgh.** 1992 Midfield Terminal at $1B for US Airways' hub, US Airways dehubbed 2004, $1.5B right-sizing program — verified (Aviation Historian). The [FC: confirm] tag in the draft was warranted given the slight phrasing difference between "$1.5B right-sizing project" in the brief and the draft's "two decades and roughly $1.5 billion right-sizing"; the figure itself is supported, the "two decades" framing is a synthesis call.

- **MWAA financial stack.** $9.4B capital program; $6.99B at IAD; $2.39B at DCA; ~$5.5B planned new bond issuance through 2028; debt per O&D enplanement $223 (2024) → ~$400 (2028); DSCR 3.16x (2024) projected to ~1.3x by 2028; Moody's 1.1x downgrade trigger; Moody's negative U.S. airport sector outlook May 2025; Concourse E autumn 2026 target; United ~62% IAD share; 280 daily departures by April 2025; $500M+ Concourse E project; 14 United gates; mobile-lounge elimination; PFC cap $4.50 since 2000 unchanged in FAA Reauth 2024; AIP not eligible for BHS — all verified (Airport CEO, Regulatory-Political, Infrastructure Economist, Airline Commercial Strategist). Several of these (DSCR 1.3x → 1.1x trigger, Moody's May 2025 negative outlook, the $2.39B DCA figure) are supported only by the Airport CEO brief, which sits in `outputs/stage1/` but outside the eight briefs the user named. Flagging for the record, not as an error.

- **Industry 4–8% / 5% BHS-of-total-capital benchmark.** The Airport CEO brief explicitly states: "Industry practice benchmarks BHS at roughly 5% of total airport capital investment… the architecture question… determines whether the real figure is 4% or 8%." The draft's "$280–560 million" envelope is the arithmetic on $6.99B × 4–8%. Verified.

- **Austin-Bergstrom $241.5M BHS.** Verified (Infrastructure Economist). The [FC: confirm] tag was warranted; figure is supported.

- **17-member MWAA board across three states + federal.** Verified (Regulatory-Political, Airport CEO).

- **DCA perimeter rule 2024 change / 10 new slot exemptions.** Verified (Regulatory-Political).

- **TSA PGDS v8.0 current / v9.0 in development.** Verified (Regulatory-Political, Chief Engineer).

- **iSAT clock from 30% design approval / two years.** Verified (Chief Engineer).

- **Diane Vaughan / normalization of deviance.** External canonical reference; treated as background knowledge, not a brief-sourced claim. Standard academic citation; not flagged.

- **Hub-and-spoke / 1978 Airline Deregulation Act / 45-minute minimum connect time at hubs in the 1980s.** Verified (Aviation Historian).

---

## Unverified claims

### 1. "September 2025" date on the BER ransomware attack (two instances)

**Claim in draft (II.2):** *"Berlin Brandenburg lost days of operation in September 2025 to a ransomware attack on Collins Aerospace, the airport's outsourced check-in and BHS software provider."*

**Claim in draft (III, software section):** *"The September 2025 ransomware attack on Collins Aerospace took down outsourced check-in and BHS software at multiple European airports for days…"*

**Source position:** The Airport COO brief (within `outputs/stage1/` but outside the eight named briefs) verifies the existence of a 2025 BER cyberattack against Collins Aerospace that disrupted BHS for days. The **month** ("September") does not appear in any Stage 1 brief consulted. The claim about disruption at **multiple European airports** is also not directly supported in any brief; the COO brief speaks only to BER.

**Disposition:** In the final draft I have softened "September 2025" to "2025" and tagged the multi-airport scope with `[UNVERIFIED — HUMAN REVIEW]`. The core point — that the new risk has migrated to software and vendor supply chain — is supported.

### 2. "Schiphol's EBS handles 4,000 bags" (V, conceded-EBS section)

**Claim in draft:** *"Schiphol's EBS handles 4,000 bags; Changi T4's, 4,000; Changi T2's, 2,400 — sized for the throughput their schedules require."*

**Source position:** Operations brief confirms Changi T4 = 4,000 and Changi T2 = 2,400. **No brief gives a numeric EBS capacity for Schiphol.** Schiphol is referenced in the Operations and Contrarian briefs only as a high-volume RFID-trial site and as an EBS-with-SCADA reference, without a bag-count figure.

**Disposition:** In the final draft I have removed the Schiphol "4,000 bags" figure and re-phrased to keep the Changi figures, which are sourced, and note Schiphol qualitatively as an EBS-sized-for-flow reference.

### 3. "Roughly £100 million in direct damage" at T5 (VII, Coda)

**Claim in draft:** *"The morning cost roughly £100 million in direct damage and a decade of institutional memory loss…"*

**Source position:** Briefs uniformly cite £16 million in direct BA losses (Operations, Tech Scout, Chief Engineer, Aviation Historian, Airline Commercial Strategist). The Infrastructure Economist brief notes the **total** financial damage including passenger compensation, rebooking, brand damage and long-term BA attrition "was orders of magnitude larger" — but no specific £100M figure appears anywhere in the corpus. The figure that closely resembles £100M in the briefs is the **£102M Chek Lap Kok** territory-wide economic damage estimate. There is a risk the editor inadvertently transposed.

**Disposition:** In the final draft I have replaced the "roughly £100 million in direct damage" line with a more cautiously phrased reference to £16M direct BA loss plus the larger industry-side damage that briefs assert qualitatively. This avoids any chance the reader cross-references and finds the £102M Hong Kong figure mis-attached to Heathrow.

### 4. "Multiple European airports" hit by the September 2025 BER cyberattack (III, software section)

**Claim in draft:** *"…took down outsourced check-in and BHS software at multiple European airports for days, because the same third-party vendor sat behind the curtain at all of them."*

**Source position:** The Airport COO brief mentions BER (singular) being disrupted via Collins Aerospace. The multi-airport scope of the attack is not in any Stage 1 brief.

**Disposition:** Tagged `[UNVERIFIED — HUMAN REVIEW]` in the final draft.

---

## Suspected errors / phrasing mismatches

### A. Composition of the $86M in Denver's delay cost

**Draft (II.1 and III, Denver section):** *"$86 million for the parallel conventional baggage system."*

**Brief reality:** The Infrastructure Economist brief gives "$86 million for the backup conventional system **and modifications to the automated system**." The Chief Engineer brief gives "$86 million in alternative system costs **and modifications**." The Regulatory-Political brief disaggregates the same total into "$51 million for a manual backup system installation, $35 million in automated system modifications" — i.e., $51M + $35M = $86M.

**Disposition:** In the final draft I have updated the line to read "$86 million for the backup conventional baggage system and modifications to the automated one" — preserving the total, correcting the composition. Minor edit, not load-bearing.

### B. "$9.4 billion MWAA capital plan through 2028"

**Draft (II.7 and VI):** *"a $9.4 billion MWAA capital plan through 2028…"*

**Brief reality:** The Regulatory-Political brief identifies the $9.4B program as running "through 2039" (the use-agreement term). The Airport CEO brief similarly frames the use agreement as 2025–2039 with $9.4B in approved capital. The $5.5B *new debt* issuance is what occurs through 2028; the $9.4B total capital is the full 15-year envelope.

**Disposition:** In the final draft I have corrected the framing to "$9.4 billion MWAA capital program (2025–2039) with approximately $5.5 billion to be issued in new bonds through 2028" — preserving the meaning, fixing the date window.

---

## Notes on `[FC: confirm]` tags already in the draft

The draft contained four `[FC: confirm]` tags inserted by the Editor. Each is resolved:

1. **"62% O&D share and reference year"** — Verified at 62% of *enplanements* (mainline + regional) per the Airline Commercial Strategist brief, which references 2024 figures. The 62% is not stated as O&D specifically in any brief; United mainline alone is 49.9% of total enplanements per the same source. I have removed "O&D" from the phrasing and kept "approximately 62% of IAD enplanements" since that is the directly supported figure. Tag removed.

2. **"1972 commissioning date for Frankfurt ICS"** — Verified in the Operations brief: "Frankfurt Airport has operated an Individual Carrier System introduced in 1972." Tag removed.

3. **"$1.5B cumulative Pittsburgh right-sizing figure"** — Verified in the Aviation Historian brief at $1.5B for the current right-sizing project. The draft's "two decades and roughly $1.5 billion" is a slight elision — the $1.5B is the current right-sizing project, the "two decades" refers to the period since dehubbing in 2004. Phrasing left intact; tag removed.

4. **"280 daily departures, $500M+ project cost, fourteen-gate count, ICS energy ratio, AUS BHS at $241.5M"** — All verified. Tags removed.

---

## What was not in any brief and therefore not used

A few items the Editor may have considered but the Strategist correctly excluded: a specific airline cost-per-mishandled-bag table; a US PFC cap inflation-adjusted equivalent; FAA NPIAS 2023–2027 totals. None appear in the edited draft, so no action needed.

---

## Bottom line for human review

Two passages in the final draft now carry `[UNVERIFIED — HUMAN REVIEW]` tags:

1. The September 2025 specificity and multi-airport scope of the Collins Aerospace ransomware attack.
2. (Implicitly cleaned, not tagged) The Schiphol EBS capacity, removed rather than tagged because the surrounding sentence remained intact without it.

The draft otherwise survived verification cleanly. The argument's load-bearing claims — the Denver figures, the T5 figures, the Munich-warned-Denver narrative, the ACRP 252 lifecycle math, the MWAA debt trajectory, the ORAT commissioning floor, the BEUMER 6,000-bag outage figure, the architecture trade-offs — are all sourced and verifiable in the briefs.

*— Fact-checker, Stage 3, June 3, 2026*
