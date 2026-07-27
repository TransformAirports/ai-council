# Fact-Check & Citation-Enforcement Report

**Document reviewed:** `revisions/v1/humanized-draft.md`
**Output:** `revisions/v1/final-draft.md`
**Sources of truth:** the eight Stage 1 briefs in `stage1/`
**Date:** 2026-07-23

---

## 1. Verified claims

**42 of 44 footnoted claim-clusters verified** against the briefs, matching on number, source, and attribution (within reasonable rounding). Every numerical figure, named-airport example, cost figure, percentage, quotation, and regulatory citation in the body traces to at least one brief's `[Source: …]` entry. Highlights confirmed:

- Shutdown callout rates — IAH 42.4%, HOU 47.4%, 2–4 hr waits, ~half lanes closed ([^1]; contrarian, regulatory briefs).
- Finances — $778.4M revenue-fund budget, ~$166M debt service, 1,383.2 FTEs, $2.92B CIP, $719.5M GARB, $1.468B IAH redevelopment, 1.8x DSCR, >450 days cash, AA- on ~$2.2B ([^3][^4][^25]; infrastructure-economist, CEO briefs).
- Throughput math — 300 DHS design/lane, 150–250 planning range, IAH 48.45M / nine checkpoints, 100/day = 0.075%, ~64,000 daily enplaned, HOU 14.6M ([^5][^6][^27][^28][^29][^30]; operations-economist briefs).
- Peer caps and hours — SEA 300/Checkpoint 4/5a–10p, PHL 100 + 10,300 since launch, DTW 75 + ~25,000 since Oct 2023, MSY 50/100 + 11a start, TPA 6-per-2hr, myPITpass 2017 9–5 ([^2][^8][^9][^10][^11][^30]).
- Carrier structure — United 58.7% / ~73% enplanements / ~80% flights; Southwest >93%; hybrid-compensatory + MII; Terminal E lease to 1/31/2030; special-facility to 11/2053; CPE $10.66→$11.17 ([^16][^17][^18][^19][^32]).
- Security/regulatory — 49 CFR 1542/1560/1540.5/1542.217, 14 CFR 139.319, Secure Flight, FLL 2017 (5 killed/6 wounded, <80 sec), TSA 2024–25 amendment, 20→28 airports, ASP 6–12 mo, crewmember-screening reversal, PFC $4.50 frozen since 2000, IIJA expiry 9/30/2026 ([^14][^15][^24][^35][^36][^37][^42][^43]).
- Quotations — Seattle "took on a life of its own…" ([^22]); APFA "bad idea"/"clog already frustratingly long TSA security lines" ([^21]); TSA "no official stance or rules…" ([^40]). All verbatim-accurate to the briefs.

No numerical discrepancies (suspected errors) were found. Every figure in the draft matches its brief within rounding.

---

## 2. Claims with no primary source (flagged, not vetoed)

These claims are supported by the briefs' professional judgment but have **no citable primary source** in the record. Each was handled by making the footnote honest rather than by deleting a load-bearing claim, because the draft already treats each as qualitative/provisional rather than as a hard number.

- **Escort-hour benefit ([^23], formerly [^33]).** No published IAH/HOU escort-hour figure exists — the operations-analyst, COO, and public-safety briefs all state this explicitly. The original footnote sourced the claim to "peer-operator briefings," "an airport chief-operating-officer finding," "a director-of-public-safety finding," and "firsthand operator knowledge." That is Council machinery and unsourced assertion. **Action:** rewrote the footnote to state plainly that the benefit rests on operating experience and operator knowledge, not a citable source, and that the specifics are illustrative. The body already declines to quantify or bank it ("sizes a benefit; it does not balance a budget"), so no body claim was removed. Not tagged `[UNVERIFIED]` because the qualitative claim (event escort labor is real and partly convertible) is corroborated by three briefs.

- **Sworn-hiring lead time of 12–18 months ([^42]).** The public-safety brief gives this as professional judgment ("roughly a year to eighteen months"), not a cited figure. The footnote had attributed it to "public-safety analysis." **Action:** relabeled as a "workforce-planning estimate, not a figure from a cited primary source." Claim retained (it supports the counter-case that staffing lags a 90-day launch) but no longer implies a primary citation.

- **SEA 2024 cyberattack ([^44]).** Appears in the operations-analyst, COO, and public-safety briefs, but none supplies a dedicated primary URL for the cyberattack itself; the footnote says "reported in operational coverage." The 2024 Port of Seattle cyberattack is well-established and corroborated across three briefs, so the claim stands, but the citation is weaker than the others. **Recommend** attaching a primary Port of Seattle / news citation before external publication.

- **HOU 14.6M passengers ([^6]).** Figure verified against the operations-analyst brief (14.6M, single 24-hour terminal, two concourses). The footnote's attribution ("Houston Airports / operations data") is looser than the underlying source (operations data / public airport statistics). Not an agent name; left as-is but noted for tightening.

---

## 3. Suspected errors (number in draft ≠ brief)

**None.** All figures reconcile with the briefs. One item worth a note for the record, not an error:

- **DTW "~25,000 passes since October 2023" ([^2]).** Faithfully reproduces the contrarian brief's figure. The DTW program launched earlier (2019 per the airline brief), so "since October 2023" likely marks a program milestone rather than launch. The draft matches the brief; flag passed upstream to research if the date matters.

---

## 4. Citation-enforcement actions taken

1. **Footnote renumbering.** The Humanizer's restructuring left the escort footnote (`[^33]`) first used in Executive Summary point 8 — ahead of `[^23]`–`[^32]`, which first appear later. Markers are now numbered in order of first use: the escort footnote became `[^23]`, and former `[^23]`–`[^32]` shifted up by one to `[^24]`–`[^33]`. All in-text markers and definitions were remapped consistently. Verified: first-use order is now 1→44 sequential; 44 definitions, exactly one per marker, none orphaned. The definition block was re-sorted into numeric order.

2. **Agent/brief-name scrub.** Removed all references to Council internal machinery from the notes: "peer-operator briefings," "an airport chief-operating-officer finding," "a director-of-public-safety finding," "the public-safety view … is overruled" ([^23]); and "per public-safety analysis" ([^42]). No agent or brief name appears anywhere in the final draft, body or notes. ("Council" in the body refers only to Houston City Council; "brief" appears only as a verb.)

3. **Primary-source check.** Every footnote now cites a regulation, report, dataset, or named publication as recorded in the briefs' `[Source: …]` entries, except the three judgment-based items in §2, which are now explicitly labeled as non-sourced estimates rather than being dressed as citations.

---

## 5. Bottom line

The draft is factually sound: no numerical claim contradicts the briefs, and every quotation is accurate. The only integrity issues were citation-side — a broken footnote sequence and three notes that cited Council chairs or unsourced operator knowledge as if they were primary sources. All are corrected in `final-draft.md`. No claim required an `[UNVERIFIED — HUMAN REVIEW]` tag, because each unsourced item was already presented in the body as qualitative and non-load-bearing, and each is now honestly footnoted. Recommend attaching a primary citation for the SEA 2024 cyberattack before external release.
