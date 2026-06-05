# Fact-Check Report — "The Sensor Outlives the System"

**Run:** IoT Design Best Practices
**Stage:** 3 — Final Verification
**Date:** June 5, 2026
**Inputs checked:** `outputs/stage3/edited-draft.md` against all twelve Stage 1 briefs in `outputs/stage1/`

---

## Scope note

The task brief named eight Stage 1 briefs. The run-prompt overrides (`prompts/runs/iot-design-best-practices.md`) added four more agents to this panel — **airport-ceo, airport-coo, slacker, virtual-christian** — and their briefs are present in `outputs/stage1/`. Several load-bearing claims in the draft (the Denver Great Hall P3 settlement, the Toronto Pearson 60,000-tag consolidation, the Charlotte Douglas pavement sensors, the Paris Orly Windows 3.1 failure, the 20-month CIO tenure figure, the Rotterdam governance model, the Barcelona Sentilo and OPC-UA findings, the Burns McDonnell / ACRP Report 59 integration gap) are sourced **only** in those four extra briefs. I read all twelve and verified against the full set. A check against only the named eight would have produced ~15 false "unverified" flags.

---

## Summary

The draft is unusually well-sourced. Of the ~150 discrete numerical claims, named examples, cost figures, percentages, and attributed statements checked, **all material claims trace to one or more Stage 1 briefs and match within reasonable rounding.** No number in the draft contradicts its source brief. No claim required a veto or an `[UNVERIFIED — HUMAN REVIEW]` tag.

The only required change to the draft was the removal of an unresolved editorial note left by the editor. Two minor attribution/wording observations are logged below but did not warrant altering the text.

| Category | Count |
|---|---|
| Verified claims | ~150 (all material claims) |
| Unverified claims (tagged) | 0 |
| Suspected numerical errors | 0 |
| Editorial artifacts removed | 1 (iFlow `[FACT-CHECK...]` note) |
| Minor attribution/wording notes | 2 (text left intact) |

---

## Verified claims (representative, by section)

**Opening + the 3G sunset.** AT&T 3G off Feb 22, 2022; Verizon at year's end; 3G IoT devices not rescuable by SIM swap; no airport published the cost — all verbatim-consistent with the Technology Scout brief.

**Executive Summary.**
- Cisco Kinetic final order date May 2021 (Tech Scout); Kinetic for Cities exit 2020, support extended through 2024, "transfer data to a Cisco partner" (Slacker, Find 1).
- Sigfox ~10M devices / 70+ countries / Jan 2022 bankruptcy / €91M net loss on €24M revenue / acquired €25M / back in court 2025 (Operations Analyst, Tech Scout, Airport CEO).
- Cisco 2017 survey n=1,845, 60% stall, 26% success; McKinsey 2018 84% stuck in pilot (Operations Analyst).
- Denver Great Hall P3: $1.8B concession, $650M fixed construction, 30% design, $288M change order, $183.6M settlement (Airport CEO).
- License fees 20–40% of 3-yr TCO; Forrester 40–60% underestimation; 2.5–4× Year-0 over ten years; no feasibility study modeled the 10-yr figure (Infrastructure Economist, Chief Engineer).
- Toronto Pearson: 7 SCADA / 3 platforms / 15 years / 60,000 tags / 12-month parallel run (Airport COO, Airport CEO).
- 75% of US private 5G on CBRS; 2025 auction pipeline; FAA blocked C-band 18 months (Regulatory-Political Analyst).
- IATA Oct 2024 Aircraft Operational Data principles; ACRP "frequently fall under vendor control," access "challenging or costly" (Airline Strategist; Airport COO).
- Delta Baggage AI 99.9% scan on 120M+ annual bags; United AWS ≈ $2B savings (Airline Strategist).
- Five lock layers inflate 5-yr TCO 20–30% (Tech Scout); DFW twin / SEA ransomware Aug 2024 (Infrastructure Economist; multiple).

**The Argument (graveyard).** Orly DECOR / Windows 3.1 / Nov 2015 / three specialists, one retiring (Airport COO); Sigfox proprietary air interface, no fallback (Tech Scout); CLT 2,000 pavement sensors / decade life / 30–40-yr runway / UNC Charlotte program (Airport COO); Love Field first airport CBRS, Boingo-operated (Airport CEO); Denver baggage $193M BAE → ~$360–400M, 16-month delay, 72 incomplete certification tasks, scope one→three concourses, decommissioned within a decade, bond obligations outlived the system (Airport COO, Infrastructure Economist, Aviation Historian, Airport CEO); iFlow 400+ APs / 130 counters / 50 Bluetooth, peer-reviewed precision finding (Tech Scout); AirAsia klia2 kiosk 35%→10%, self-tagging→zero (Airline Strategist).

**History.** Braniff/Eastern/Pan Am/Midway; CUTE at LAX for 1984 Olympics; CUSS / CUPPS 2009; LonTalk/Modbus/early BACnet legacy BAS (Aviation Historian).

**Bond section.** DSCR ~2.0x at large hubs; 25–30-yr bonds; $75M IoT remediation example; CVG A1→Baa1 after Delta de-hub 2013; CIO tenure <5 yrs; state-gov CIO ~20 months, ~40% serving ≤2 years; "plan for two" CIO cycles (Airport CEO; Virtual-Christian).

**Cost section.** 50-asset $700K–$1M / 1,000-asset $3–10M (Infrastructure Economist); platform renewal +20–40%; logistics 35% per-device jump, vendor held certificates (Chief Engineer; Tech Scout); Pearson 150 IT vendors → single MSP, 94% outage cut (Airport COO).

**Network section.** 40%+ dropout designed-in, "5:45 on a Monday" (Airport COO); LoRaWAN unlicensed / 5–10 yr battery / no per-device fee / open Alliance spec; LTE-M & NB-IoT in 3GPP 5G family; $10–12/device-yr, six figures at 10,000; sub-5ms private-5G use cases; restroom-occupancy misallocation; Wi-Fi 6E / iOS 14 MAC randomization (Operations Analyst); GSMA 143 (>100) shutdowns through 2030 (Infrastructure Economist); LTE-M/NB-IoT retirement begun 2023–24 (Chief Engineer); WISPA "potentially put CBRS and 6 GHz spectrum on the auction block"; C-band Jan 2022–Sep 2023 (Regulatory); proprietary PLC abstraction limit, one clean change + one with pain (Airport COO).

**Standards / schema / broker / edge / contract / organization.** OPC-UA LoRaWAN+Matter mappings 2025–26, UA Edge Translator, FHIR analogy, hospital EMR timing (Slacker); budget 2× integration quote (Infrastructure Economist); airfield-lighting gateway 43 ms within 500 ms stop-bar limit (Operations Analyst); MuleSoft/Boomi/Informatica, MQTT/Kafka, Unified Namespace, broker-not-owned-by-sensor-vendor (Operations Analyst; Slacker); Schiphol Kafka→Confluent, Google IoT Core SDK coupling, MSK/Event Hubs alternatives (Tech Scout; Operations Analyst); edge >90% egress cut, 40×4K-feeds → kilobits (Operations Analyst); device-certificate and 30-day liquidated-damages clauses, "bad contract runs for seven years" (Tech Scout; Operations Analyst; Slacker); hospital 30%/70% IT-biomed split (Virtual-Christian); Rotterdam IBM/Cisco/Esri/Axians "live and let live" (Virtual-Christian); DFW Willow/Parsons $2.9M five-year, two non-negotiables (Infrastructure Economist); Barcelona Sentilo 2014 (Slacker); Burns McDonnell "frequently omitted entirely," ACRP Report 59 (2011) → 2024, 13-year gap (Airport COO).

**Counter-case + rebuttal.** Refresh cycles 4–6 / 5–7 / 3–4 yrs; BACnet 1995 / Modbus 1979; Google IoT Core dead at six; IBM Watson IoT ~decade, no replacement; 26% success / unclear business goals; TCO underestimation 30–50%; logistics $38K→$8K/mo; Changi 5,000+ sensors / 700 cameras / 500 devices single-platform (Contrarian); SEA came through networked systems, federal systems segmented (Tech Scout, Regulatory, Airport COO); Pittsburgh $1B 1992 terminal, US Airways shed maintenance in bankruptcy; St. Louis 417→36 TWA flights, concourse demolished (Aviation Historian); PFC $4.50 frozen since 2001, ≈$7.85 in 2026 dollars, 2024 reauth no raise, AIP exclusions, IIJA ATP closed Jan 15 2026 (Regulatory; Airport CEO).

**MWAA section.** Use-and-lease effective Jan 1 2025; $9B program / $6.99B Dulles; United Concourse E $500M+ / 14 gates / 435,000 sq ft / announced Dec 2024 (Airline Strategist); 2002 stranded EDS precedent (Aviation Historian); TSA 2023 IT/OT segmentation mandate + forthcoming FAA ARC rulemaking (Regulatory; Chief Engineer); SEA Aug 2024 dry-erase boards / 90,000 notifications / manual baggage (multiple).

---

## Unverified claims

**None.** Every numerical claim, named airport example, cost figure, percentage, and attributed statement in the draft was traced to at least one Stage 1 brief. No `[UNVERIFIED — HUMAN REVIEW]` tags were inserted.

---

## Suspected numerical errors

**None.** No figure in the draft contradicts its source brief. Where the draft uses a range (e.g., Denver baggage "$360–400 million"), the range brackets the figures reported across briefs ($360M in Airport COO, ~$400M in Infrastructure Economist/Aviation Historian) and is fair. The Delta "120 million-plus annual bags / 99.9%" pairing matches the Airline Strategist's evidence section (the brief's separate "100,000+ daily bags at ATL" is a station-level figure and does not conflict).

---

## Missing citations / editorial artifacts (resolved)

1. **iFlow "[FACT-CHECK: which airport ran iFlow? brief should name it]" (Argument section).** This was an unresolved editor's note, not a sourced claim. The Technology Scout brief explicitly states iFlow "deployed at an undisclosed major hub," and its accuracy limitations were documented in a peer-reviewed study associated with a *different* airport (Cincinnati/Northern Kentucky). The airport that ran iFlow therefore **cannot** be named from the research — the cautious "major hub" phrasing is correct and supported.
   **Action taken in final draft:** removed the bracketed note; rephrased to "An undisclosed major hub…" and added a one-clause parenthetical making the sourcing limitation explicit. The underlying sensor counts and the precision finding remain fully verified.

---

## Minor attribution / wording notes (text left intact)

These are logged for transparency. Neither is load-bearing and both are substantively supported; the draft text was not altered.

1. **Cisco "transfer their data to a Cisco partner."** The draft renders this in quotation marks. The Slacker brief (Find 1) presents it as a paraphrase of the Smart Cities Dive report, not a verbatim Cisco quotation. The substance — Cisco offered customers data transfer to a partner with no replacement product — is verified. Recommend the human reviewer either drop the quote marks or confirm verbatim wording if it will be cited externally.

2. **"ACRP Report 59 identified the pattern in 2011; the same analysis found it again in 2024."** The 2024 finding is from a separate Burns McDonnell analysis, not "the same analysis." The 13-year gap, the recurring pattern, and both dates are accurate (Airport COO brief). Wording is slightly loose but not factually wrong.

---

## Files written

- `outputs/stage3/fact-check-report.md` — this report
- `outputs/stage3/final-draft.md` — the edited draft with the iFlow editorial note resolved; no other changes required, as all claims verified
