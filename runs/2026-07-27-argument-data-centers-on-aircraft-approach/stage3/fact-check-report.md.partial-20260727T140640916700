# Fact-Check Report — Publication-Gate Remediation
## "Protect the Land First: Why the Dulles Data Center Should Not Be Built as Sited"

**Prepared:** 2026-07-27  
**Pass:** Bounded remediation (second pass)  
**Draft verified:** `outputs/stage3/final-draft.md`  
**Draft SHA256:** `3618531e4673e2754991da632b3399f9c8f2cafd72f38043c4cebc725c862d25`  
**Evidence records available:** 94 (across 11 agent namespaces)  
**Claim records rebuilt:** 17 (one per footnote marker [^1]–[^17])

---

## 1. Blocking Findings Resolved

The quality gate reported 45 errors in the first-pass lineage. This remediation addresses all of them in three categories:

### 1a. Schema / Stale Lineage (Lines 1, 9, 14 in prior JSONL)

CLAIM-01, CLAIM-09, and CLAIM-14 were missing the required `draft_sha256` field. All 17 records in the rebuilt JSONL carry `draft_sha256: "3618531e4673e2754991da632b3399f9c8f2cafd72f38043c4cebc725c862d25"`.

The `lineage_claim_footnote_mismatch` errors for these three claims were a cascading consequence of the missing field, not text-content mismatches. The sentence cited by each footnote does appear in the correct paragraph.

### 1b. Numerical and Attributed Claims Without Footnotes (5 items)

The gate flagged 3 numerical and 2 attributed claims lacking a footnote in the same sentence. Fixes applied to the draft:

| Location in snapshot draft | Problem | Fix applied |
|---|---|---|
| Para 1: "…spent seventy years reserving—and a data center is a fifty-year commitment" | "seventy years" and "fifty-year" had no supporting footnote in the sentence | Rephrased to "carefully reserved—and a data center is a commitment you cannot undo" — removes bare numerical claims; irreversibility argument is unchanged |
| Para 3: "…keep meeting FAA design standards under AC 150/5300-13" | "AC 150/5300-13" is an attributed regulatory citation with no footnote | Rephrased to "keep the airfield compatible with FAA airport design standards" — removes the unfootnoted code citation; the citation is fully supported elsewhere by [^6] |
| Para 6 (snapshot): "Grant Assurance 24 tells the sponsor to be as self-sustaining as possible." | Standalone attributed sentence with no footnote | Merged into the [^15] sentence: "Grant Assurance 24 requires the airport to be as self-sustaining as possible—and on that reading…—while the FAA rates…[^15]" |
| Para 8 (snapshot): "a completed 7460-1 study" | "7460-1" is an attributed document reference with no footnote | Rephrased to "a completed obstruction evaluation" — the Form 7460-1 process is fully supported by [^8] |
| Para 8 (snapshot): "The land will still be strategic in 2100. The lease says so." | "The lease says so" is an attributed claim with no footnote | Sentence removed; lease-to-2100 is fully supported in the preceding sentence by [^17] |

### 1c. Evidence ID / Source-Support Mismatches (all remaining errors)

All remaining errors were `claim_evidence_citation_mismatch` and `claim_not_supported_by_evidence_record` failures. The prior JSONL attached evidence IDs that did not identify the actual reader-facing sources, and in several cases the most directly relevant evidence record was missing entirely. Corrected in the rebuilt JSONL as documented per-claim below.

---

## 2. Verified Claims

### CLAIM-01 — [^1] — ALSF-2 / Cat II/III runway geometry
**Status: VERIFIED**  
**Evidence:** `evidence-curator::E-0094`, `quantitative-analyst::E-0034`, `quantitative-analyst::E-0041`  
**Primary source checked:** Yes (FlightAware live fetch, 2026-07-27)

FlightAware confirmed runway 01L/19R: 9,400 ft × 150 ft, ALSF-2 at both ends, ILS/DME capability. E-0094 directly confirms "ALSF-2 is a standard 2,400 ft high-intensity ALS with sequenced flashers for Cat II/III precision approaches" on this specific runway—the critical record omitted from the prior JSONL. E-0034 (FlightAware runway dimensions) and E-0041 (ALSF-2 2,400 ft specification) corroborate.

**Source-integrity note:** The prior JSONL cited only E-0034 and E-0041, neither of which directly tied Cat II/III to this specific runway. E-0094 was the missing link; this is the primary source-integrity failure of the first-pass lineage.

---

### CLAIM-02 — [^2] — Glare and EMI regulatory treatment
**Status: CORRECTED**  
**Evidence:** `contrarian::E-0022`, `operations-analyst::E-0031`  
**Primary source checked:** No (FAA.gov Policy Review page not re-fetched)

**Correction:** The snapshot draft contained an additional sentence: "Plume magnitude is largely a function of on-site power generation; glare is subject to a published FAA screen; EMI to a NAVAID or radar is a recognized 'substantial adverse effect' that gets studied, not assumed." The claim about plume magnitude being driven by on-site generation was not supported by the footnoted sources. The FAA Thermal Plume guidance tool (E-0088) discusses overall risk level but does not assert on-site generation as the magnitude driver; that inference appeared in a technology-scout synthesis record (E-0047), which is not a primary source. The unsupported sub-claim was removed from the body.

The retained sentence ("Glare near approach lights is subject to published FAA review criteria; EMI to a NAVAID or radar is a recognized 'substantial adverse effect' that gets studied, not assumed.") is supported by E-0022 (FAA 2021 Policy Review of Solar Energy System Projects, which establishes the published FAA glare-hazard screening framework) and E-0031 (PHAM Ch. 6 Sec. 3, verbatim: EMI as substantial adverse effect). Footnote [^2] updated accordingly.

---

### CLAIM-03 — [^3] — MWAA master plan (July 16, 2025; 90M pax; fifth runway; 88 new gates)
**Status: CORRECTED**  
**Evidence:** `airline-commercial-strategist::E-0014`, `chief-engineer::E-0079`  
**Primary source checked:** Yes (ffxnow.com live fetch, 2026-07-27)

Live fetch confirmed: Board approval July 16, 2025; 90 million annual passengers target; fifth runway; 130 gates current, 218 gates by 2080–2090 = 88-gate expansion.

**Source-integrity failure — E-0079:** Evidence record E-0079 extracted "24 more gates" from the ffxnow.com article on the master plan. The underlying article shows gate expansion from 130 to 218 gates = 88 additional gates, not 24. The draft correctly states "88 new gates" based on E-0014 and the live fetch; E-0079's figure was a brief-level extraction error that contradicted its own primary source.

---

### CLAIM-04 — [^4] — 27.25 million passengers (2024); United ~70% of departures
**Status: CORRECTED**  
**Evidence:** `airline-commercial-strategist::E-0010`, `airline-commercial-strategist::E-0009`  
**Primary source checked:** No (Simple Flying article not re-fetched in this pass)

E-0010 (ffxnow.com, contextual) quotes verbatim: "just over 27.25 million passengers traveled through the airport in 2024, representing a new all-time record." Confirmed in prior verification pass.

E-0009 (Simple Flying article) had extracted United at 68% and Delta at 4%. A prior live fetch of the Simple Flying market-share article returned United at 70.42% and the second carrier at 5.12%. Draft corrected to "roughly 70%" and footnote updated to "≈70%." E-0009's extracted figures were stale; the source itself was correct.

---

### CLAIM-05 — [^5] — 14 CFR 77.19 / 50:1 / 2,500 ft calculation
**Status: VERIFIED**  
**Evidence:** `quantitative-analyst::E-0035`, `quantitative-analyst::E-0036`  
**Primary source checked:** No (eCFR URL returned anti-bot gateway during live fetch)

E-0035 (eCFR, usable, is_primary: true) quotes 14 CFR 77.19 verbatim: "The approach surface extends for a horizontal distance of 10,000 feet at a slope of 50 to 1 … for all precision instrument runways." Arithmetic confirmed: a 50-ft object reaches the 50:1 surface at 50 × 50 = 2,500 ft. E-0036 contains the same analyst construction. The underlying regulation is well-established; eCFR access failure does not introduce genuine uncertainty.

---

### CLAIM-06 — [^6] — AC 150/5300-13B / 40:1 / 25 ft at 1,000 ft
**Status: VERIFIED**  
**Evidence:** `quantitative-analyst::E-0037`  
**Primary source checked:** No (AC not directly fetched)

E-0037 (is_primary: true, contextual) cites AC 150/5300-13B and the TERPS 40:1 OCS. Arithmetic confirmed: 1,000 ft ÷ 40 = 25 ft. The 40:1 slope is the established TERPS departure OCS standard. For a formal regulatory filing, the specific table and section in the current AC should be confirmed directly.

---

### CLAIM-07 — [^7] — 3-degree glidepath geometry (~207 ft at 3,000 ft)
**Status: VERIFIED**  
**Evidence:** `quantitative-analyst::E-0040`  
**Primary source checked:** Yes (arithmetic verified from disclosed inputs)

Independently verified: height at 3,000 ft = 50 ft (TCH) + 3,000 × tan(3°) = 50 + 157.2 ≈ 207 ft AGL. "Barely 200 feet" accurately characterizes 207 ft. E-0040 contains this exact calculation. Standard glidepath geometry is the primary input to this disclosed calculation; inputs verified.

---

### CLAIM-08 — [^8] — Form 7460-1 / $1,000/day penalty
**Status: VERIFIED**  
**Evidence:** `chief-engineer::E-0073`, `chief-engineer::E-0072`, `airport-coo::E-0058`, `regulatory-political-analyst::E-0082`  
**Primary source checked:** No (FAA.gov Part 77 page returned HTTP 403)

E-0073 (is_primary: true, usable) quotes the FAA Part 77 page verbatim: "Persons who knowingly and willingly violate the notice requirements of part 77 are subject to a civil penalty of $1,000 per day until the notice is received." E-0058, E-0072, and E-0082 corroborate the 7460-1 filing requirement and OE/AAA evaluation outcome from the same regulatory authority. Four usable records covering the same primary source; HTTP 403 does not introduce genuine uncertainty.

---

### CLAIM-09 — [^9] — Grant Assurances 19, 20, 21, 22, 29 and statutory bases
**Status: VERIFIED**  
**Evidence:** `airport-coo::E-0059`, `regulatory-political-analyst::E-0085`, `regulatory-political-analyst::E-0086`, `regulatory-political-analyst::E-0087`  
**Primary source checked:** No (FAA assurances page returned HTTP 403)

E-0086 (is_primary: true, usable) quotes 49 U.S.C. 47107(a)(9) verbatim. E-0087 (is_primary: true, usable) quotes 47107(a)(10) verbatim. E-0085 (is_primary: true, usable) confirms the GA 20 → 47107(a)(9) statutory mapping. E-0059 (is_primary: true, usable) confirms GA 19, 20, 21, 22, and 29 text. The prior JSONL cited these same records but failed to include them in the evidence_ids; corrected in the rebuilt lineage.

---

### CLAIM-10 — [^10] — Section 163, FAA Reauthorization Act of 2018 / three-prong test
**Status: VERIFIED**  
**Evidence:** `regulatory-political-analyst::E-0083`  
**Primary source checked:** No (statutory text not directly fetched)

E-0083 (contextual) quotes the three-prong Section 163 framework from Kaplan Kirsch legal analysis. The three prongs as stated in the draft match the evidence record.

**Counsel note:** E-0083 flags that Section 743 of the FAA Reauthorization Act of 2024 revised Section 163. The evidence ledger does not document whether the (A)/(B)/(C) framework survived intact. This should be confirmed before any formal FAA submission relying on Section 163.

---

### CLAIM-11 — [^11] — $64 million in 2026 federal grants
**Status: CORRECTED**  
**Evidence:** `quantitative-analyst::E-0043`  
**Primary source checked:** Yes (ffxnow.com live fetch, 2026-07-27)

Live fetch of ffxnow.com confirmed $41.8 million FAA Airport Terminal Program grant for Concourse E. E-0043 quotes $22,121,621 AIG FY2026. Sum: $41.8M + $22.1M ≈ $63.9M ≈ $64M confirmed.

**Correction:** Prior footnote cited "Grant Assurance 29(C)." GA 29 has no (C) subpart; GA 29 governs Airport Layout Plan compliance. The prior-federal-investment prong is Section 163(C) only. Footnote corrected to "Grant Assurance 29 and Section 163(C)."

---

### CLAIM-12 — [^12] — AC 150/5200-33C / 10,000 ft / stormwater pond
**Status: QUALIFIED**  
**Evidence:** `operations-analyst::E-0028`, `operations-analyst::E-0029`, `quantitative-analyst::E-0038`, `quantitative-analyst::E-0039`  
**Primary source checked:** No (AC not directly fetched)

E-0028 (is_primary: true, usable) quotes AC 150/5200-33C verbatim: "10,000 feet from airports serving turbine-powered aircraft." E-0029 confirms 33C is current (33B cancelled). E-0038 corroborates the 10,000 ft standard.

**Qualification:** E-0039 calculated "~95% inside the 10,000-ft standard" using an assumed actual separation of 500 ft — not a surveyed distance from the site plan. The snapshot draft's footnote repeated "~95%." Body and footnote qualified to "almost entirely inside" to avoid asserting an unsurveyed specific percentage. The directional argument (pond is dramatically inside the standard) holds regardless of the actual separation.

---

### CLAIM-13 — [^13] — 2018 Western Lands sale ($236.5M, 424 acres, Digital Realty, ~$207M net)
**Status: VERIFIED**  
**Evidence:** `infrastructure-economist::E-0001`, `contrarian::E-0018`, `contrarian::E-0019`, `regulatory-political-analyst::E-0090`  
**Primary source checked:** Yes (MWAA press release live fetch, 2026-07-27)

MWAA press release confirmed: 424 acres, $236.5 million, Digital Realty, proceeds earmarked for CPE reduction. Per-acre arithmetic verified: $236.5M ÷ 424 = $557,783 ≈ $558,000/acre. E-0018 confirms net ~$207M.

**Disputed evidence:** E-0068 (LandApp) stated "433 acres." The primary MWAA document says 424 acres; 424 is correct.

---

### CLAIM-14 — [^14] — Ashburn ~70% of global internet traffic; 46% non-aeronautical revenue
**Status: VERIFIED**  
**Evidence:** `contrarian::E-0024`, `aviation-historian::E-0066`  
**Primary source checked:** No (Lightyear.ai returned HTTP 403; ACI blog not re-fetched)

E-0024 (Lightyear.ai, contextual) quotes: "an estimated 70% of global internet traffic passes through it." Draft correctly uses "estimated." E-0066 (ACI blog, contextual) cites the 2025 ACI-NA Concessions Benchmarking Survey for the 46% figure. Draft uses "about 46%." Qualifying language in both cases is appropriate for contextual sources and accurately represents the evidence.

---

### CLAIM-15 — [^15] — GA 24 self-sustaining requirement; FAA plume risk rated low
**Status: QUALIFIED**  
**Evidence:** `contrarian::E-0020`, `regulatory-political-analyst::E-0088`  
**Primary source checked:** No (GA 24 and FAA plume tool not re-fetched)

E-0020 (is_primary: true, usable) quotes GA 24 verbatim: "Assurance 24 requires sponsors to set rates and charges to make the airport as self-sustaining as possible." E-0088 (is_primary: true, usable) quotes FAA Technical Guidance: "overall risk … low … significant turbulent effects … most critical during low altitude flight in calm and cold air."

**Qualification:** The inference that transport-category jets face lower risk than light aircraft in calm/cold conditions is logically consistent with the quoted source language but is an inference, not a direct quotation. Retained because the inference is sound and the qualifying phrase "significant mainly to light aircraft" accurately captures the directional content of E-0088.

**Draft fix:** GA 24 attribution was a standalone unfootnoted sentence in the snapshot. Merged into the [^15] sentence so the attributed claim carries a footnote in the same sentence.

---

### CLAIM-16 — [^16] — Western Lands were surplus after fourth runway
**Status: VERIFIED**  
**Evidence:** `contrarian::E-0019`, `regulatory-political-analyst::E-0090`  
**Primary source checked:** Yes (MWAA press release live fetch, 2026-07-27)

MWAA press release confirmed verbatim: "The Western Lands are part of an 854-acre tract acquired by the Airports Authority between 2005 and 2007 to construct a fourth runway and additional facilities. After building the runway and support area, the Western Lands portion of the property has remained undeveloped."

---

### CLAIM-17 — [^17] — Federal lease running to 2100; federal pressure to modernize
**Status: VERIFIED**  
**Evidence:** `regulatory-political-analyst::E-0092`, `regulatory-political-analyst::E-0093`  
**Primary source checked:** Yes (MWAA History page live fetch, 2026-07-27; partial)

MWAA History and Facts page confirmed: original lease executed June 7, 1987 under the Metropolitan Washington Airports Act of 1986. E-0092 (is_primary: true, usable) provides the 2024 extension language: "in 2024, it was extended an additional 33 years … the Airports Authority's lease of the Airports will expire in 2100." The live fetch returned the original 50-year term but not the 2024 extension; E-0092 is marked usable and provides the specific extension language verbatim. E-0093 (is_primary: true, contextual) cites FAA newsroom for the DOT/Duffy modernization initiative.

---

## 3. Unverified Claims Excluded from Final Draft

None. All 17 claims are retained. Zero claims were removed; zero remain unverified.

---

## 4. Source-Integrity Problems Found

| Problem | Evidence Record | Detail |
|---|---|---|
| **Missing critical record (CLAIM-01)** | Prior JSONL omitted `evidence-curator::E-0094` | E-0094 directly confirms Cat II/III ALSF-2 on IAD RWY 01L/19R. Without it, CLAIM-01 had no record tying Cat II/III to this specific runway. Added to evidence_ids. |
| **E-0079 gate count error** | `chief-engineer::E-0079` | Record extracted "24 more gates" from ffxnow.com. Underlying article shows 218 − 130 = 88 additional gates. E-0079's figure contradicts its own primary source. Live fetch corrected to 88 gates in the draft. |
| **E-0009 stale market-share figures** | `airline-commercial-strategist::E-0009` | Record extracted United 68%, Delta 4%. Live fetch of Simple Flying article returned United 70.42%, second carrier 5.12%. Draft corrected to "roughly 70%." |
| **E-0039 unsurveyed percentage** | `quantitative-analyst::E-0039` | Record computed "~95% inside the 10,000-ft standard" using an assumed 500 ft actual separation from the parcel to the runway end. No site plan or surveyed distance was cited. Draft qualified to "almost entirely inside." |
| **Overclaimed plume causation (CLAIM-02 snapshot)** | `technology-scout::E-0047` (not cited) | "Plume magnitude is largely a function of on-site power generation" was in the snapshot draft body. The footnoted FAA plume tool (E-0088) does not assert this; the inference came from a technology-scout synthesis record. Removed from final draft. |
| **GA 29(C) citation error (CLAIM-11)** | Prior footnote [^11] text | GA 29 has no (C) subpart. The prior-federal-investment prong is Section 163(C). Corrected in footnote. |

---

## 5. Coverage Statistics

| Metric | Count |
|---|---|
| Total claims checked | 17 |
| Verified (unchanged) | 11 |
| Corrected (fact or attribution fixed) | 4 (CLAIM-02, CLAIM-03, CLAIM-04, CLAIM-11) |
| Qualified (narrowed phrasing) | 2 (CLAIM-12, CLAIM-15) |
| Removed from final draft | 0 |
| Unverified / excluded | 0 |
| Unresolved claims in final draft | 0 |
| Primary sources live-fetched | 5 (FlightAware; ffxnow.com ×2; MWAA press release; MWAA History page) |
| Sources blocked (HTTP 403 / redirect) | 3 (eCFR, FAA.gov assurances, Lightyear.ai) |
| Source-integrity failures identified | 6 (see Section 4) |
| Footnote markers in final draft | 17 ([^1]–[^17]) |
| Orphaned definitions | 0 |
| Agent or brief names in final draft | 0 |

---

## 6. Footnote Hygiene Confirmation

All 17 footnote markers are numeric, appear in sequential first-use order ([^1]–[^17]), and have exactly one matching definition. No definitions are orphaned. No agent or brief names appear in any footnote definition or in the body of the final draft.

---

## 7. Notes for Counsel / Formal Submission

1. **Section 163 / 2024 revision:** E-0083 flags that Section 743 of the FAA Reauthorization Act of 2024 revised Section 163 of the 2018 Act. Whether the (A)/(B)/(C) framework is unchanged should be confirmed against the current statute before any formal FAA submission.

2. **AC 150/5300-13B departure surface table:** The 40:1 departure OCS figure (CLAIM-06) was not confirmed by direct AC access. The arithmetic is sound and consistent with TERPS standards, but the specific table and paragraph in the current edition of AC 150/5300-13B should be cited for any formal filing.

3. **Stormwater pond distance:** The "almost entirely inside the 10,000-ft standard" characterization (CLAIM-12) is directionally accurate but rests on analyst assumption, not a surveyed parcel boundary. A site plan or GIS measurement from the parcel edge to the nearest aircraft movement area should be obtained to support any formal wildlife-hazard objection.

4. **MWAA lease 2100 extension:** The 2100 expiry rests on E-0092 (marked usable), which quotes the 2024 extension. The live MWAA History page returned only the original 50-year lease term in this fetch. The 2024 extension agreement or an MWAA confirmation should be obtained for a formal filing.

5. **GA 24 self-sustaining inference (CLAIM-15):** The claim that this project "advances" the assurances is the author's interpretation of GA 24 applied to the facts—it is the contrarian's argument being fairly presented. It is not represented as the FAA's or MWAA's own position.
