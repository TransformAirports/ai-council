# Evidence Map — Quiet-by-Design Standards for MWAA Terminals

**Run:** `quiet-by-design-standards-for-mwaa-terminals-2`
**Curated:** 2026-08-10
**Curator:** evidence-curator
**Ledger:** `outputs/evidence-ledger.jsonl` (256 records, 14 agents)
**Purpose:** Rank the load-bearing evidence, expose corroboration and contradiction, mark stale or weak sources, list the do-not-claim items, and hand the Strategist a defensible argument kit.

The ledger is preserved with per-agent provenance intact. Records are keyed `agent-slug::ev-<hash>`; where the same underlying claim was independently discovered by multiple agents, this map identifies the corroboration cluster rather than collapsing the records. That preserves audit lineage while surfacing the consensus.

---

## 1. The ten load-bearing evidence points, ranked

These are the records the Strategist must build the argument on. Rank reflects load-bearing weight for the specific thesis (mandatory-vs-context standards for both airports), not aggregate citation count.

### E-01. ACRP Research Report 175 is the domestic technical anchor for terminal PA intelligibility

- **Claim:** ACRP 175 recommends a minimum STI of 0.45 and an SNR of 10–15 dB(A) for public address in pier-style departure lounges, with dedicated chapters on PA design (Ch. 7) and commissioning (Ch. 9).
- **Corroboration cluster:** `infrastructure-economist::ev-10c4d222451f`, `operations-analyst::ev-4cea7e413a8a` and `ev-c32805a56bc4`, `technology-scout::ev-4865732d074c`, `contrarian::ev-8959e4157d81`, `regulatory-political-analyst::ev-0c7f47529c0b`, `airport-ceo::ev-6da2186b9993`, `airport-coo::ev-850407c2b3d9` and `ev-30d4f0d8475a` and `ev-c1e6a8e83e24`, `airline-commercial-strategist::ev-a2f6964f0719`, `virtual-christian::ev-3dd07b82ecbe`, `quantitative-analyst::ev-d1b6bd6f446b` and `ev-d26464a4731e` (14 records, 10 agents).
- **Why it carries weight:** ACRP 175 is TRB/FAA-sponsored, open access, and directly names the terminal typology. Every mandatory acoustic and intelligibility number in the MWAA standard should route through this document first. Quantitative-analyst also captured the design range (0.46–0.53 target 0.50), which is a stronger operating window than the single "0.45 minimum" citation most agents used.
- **Status:** usable, primary/high. **Caveat:** guidance, not a code — the number lives in the MWAA Design Manual only if MWAA writes it there.

### E-02. NFPA 72 Chapter 24 sets the non-negotiable intelligibility floor for emergency voice systems

- **Claim:** Voice intelligibility for emergency communications is acceptable when ≥90% of measurement locations within each Acoustically Distinguishable Space achieve STI ≥ 0.45 (CIS ≥ 0.65) with an average STI ≥ 0.50 (CIS ≥ 0.70).
- **Corroboration cluster:** `quantitative-analyst::ev-8cb15085981e`, `contrarian::ev-58a4b35511d3`, `regulatory-political-analyst::ev-3a0fb861baf5`, `operations-analyst::ev-91f3046f0ad8`, `airport-emergency-management-director::ev-bf6c2224cb0c` and `ev-a53c7c5221b4`, `airport-coo::ev-c382f952da3e` (7 records, 6 agents).
- **Why it carries weight:** This is the floor any "quiet" regime has to survive. Reducing announcements must not reduce the ADS-level STI performance the code demands during an emergency reversion. It also implies that MWAA needs a documented ADS map at each terminal, which is a design deliverable, not a facilities-management afterthought.
- **Status:** usable, high. **Caveat:** NFPA 72 is paywalled and adopted through the Virginia/DC building codes on a version-specific cycle. Cite the edition in force at the AHJ. All ledger citations are secondary summaries.

### E-03. IEC 60268-16:2020 is the international measurement standard — with a known limitation

- **Claim:** IEC 60268-16:2020 defines the STI/STIPA model and measurement method; a STIPA value of ≥0.50 typically satisfies EN 54-16, BS 5839-8, and ISO 7240-19 for voice-alarm compliance. The standard explicitly does not cover the case of fluctuating noise.
- **Corroboration cluster:** `operations-analyst::ev-ee92641d9233`, `technology-scout::ev-3f4e63a0f381` and `ev-74059fa4a084`, `infrastructure-economist::ev-e379e758a90c`, `airport-ceo::ev-ccf80d0530ca`, `airport-coo::ev-895599477d44` and `ev-036e168941ec` and `ev-1ddfb18ee1b3`, `contrarian::ev-851bd0537852`, `quantitative-analyst::ev-2acb8729ef73` (10 records, 8 agents).
- **Why it carries weight:** This is the only international measurement method the MWAA specification can require by reference. The fluctuating-noise limitation (only Contrarian caught it) matters because airport terminals are precisely fluctuating-noise environments — announcement scoring at a moment of low ambient will differ from the same speaker's score during a passenger surge. The standard should be cited as the measurement method; the acceptance criteria should be MWAA's own.
- **Status:** usable, high. **Caveat:** paywalled. MWAA specifications can require compliance by reference without republishing the text.

### E-04. MWAA's 2020 Design Manual is the enforcement vehicle — and its current acoustic content is unverified

- **Claim:** MWAA maintains a seven-volume 2020 Design Manual described by the Authority as "a mandatory guide with the force of law on the airport property," updated annually, with airport-specific supporting volumes for IAD and DCA. Specifications are edited from MASTERSPEC.
- **Corroboration cluster:** `airport-ceo::ev-e36d706a5fbe`, `virtual-chris::ev-d6d475e3fe78`, `regulatory-political-analyst::ev-1660d73cfa9b`, `quantitative-analyst::ev-33cfe5aa6220`, `contrarian::ev-f90aca368b4b`, `technology-scout::ev-98a81e3fc5da`, `airport-emergency-management-director::ev-3dd83d0d81a8`, `virtual-christian::ev-a5d536807853` (8 records, 8 agents).
- **Why it carries weight:** This is the sentence that decides the shape of the recommendation. A quiet-by-design standard has to enter through the Design Manual and Specifications apparatus, not as a standalone policy or as an airline-tenant memo. Every implementation option in the article should be scoped as a Design Manual amendment or a new volume. **Open gap:** the Council did not verify whether the current 2020 Design Manual already contains acoustic, PA-zoning, STI, or L~Aeq~ requirements — that gap is called out explicitly in §5 below.

### E-05. The 2025 Airline Use and Lease Agreement and MWAA's debt trajectory define the political price of a new standard

- **Claim:** A new 15-year Airline Use and Lease Agreement took effect January 1, 2025, carrying at execution an approximately $9B capital construction program ($6.99B IAD, $2.39B DCA), with an approximately 140% airline-funded debt service coverage target. Standing MWAA credit ratings are Fitch AA−, Moody's Aa3, S&P AA− (stable). MWAA plans ~$5.5B of new debt across 2025–2028; adjusted debt per O&D enplanement peaks near $400 in 2028; DSCR compresses from 1.63× (2024) to ~1.3× over the five-year window.
- **Corroboration cluster:** `airline-commercial-strategist::ev-e40c8b59ee9e`, `airport-ceo::ev-f3c118688838` and `ev-4be11ef6d9d3` and `ev-2683ca17d772` and `ev-ec65eb1facf8`, `infrastructure-economist::ev-525ee186f14c` and `ev-bdbb755826ed` and `ev-dc8d320b20fa` and `ev-ed2a314947b9`, `regulatory-political-analyst::ev-e3085057f18a` and `ev-417ba030149a`, `virtual-christian::ev-ccfdf3a9ecf6`, `contrarian::ev-a6417525686b`, `quantitative-analyst::ev-41d72e9a58cc` and `ev-cf12ea3a2c51` (15 records, 7 agents).
- **Why it carries weight:** These numbers determine which recommendation the board can pass. Mandatory design specifications that reduce late-stage rework are the easy board sell; mandatory retrofit programs are not. The DSCR compression window (2025–2029) is exactly the window in which the concourse-C/D replacement and DCA Terminal 1 replacement are being scoped. The standards decision is not academic.
- **Status:** usable, high (most records). **Caveat:** Majority-in-interest thresholds, exempt-project categories, and cost-recovery categorization under the 2025 AUL are not verified from primary documents. Do not infer MII thresholds from industry convention.

### E-06. The airline concentration at each airport is asymmetric, and that asymmetry runs the whole implementation problem

- **Claim:** United controls approximately 67% of IAD passenger traffic (~19.7M of 29.01M in 2025) and operates 50 jetbridge-equipped gates in Concourses C and D; American Airlines held approximately 53% of DCA market share by end-2024 with more than 5× the routes of its nearest competitor. Concourse E adds 14 United gates and opens fall 2026. IAD signatory CPE is reported at $12.88 (FY24) and $9.56 (FY25); DCA CPE $9.05 (FY24) and $7.49 (FY25).
- **Corroboration cluster:** `airline-commercial-strategist::ev-df19b606cf60`, `ev-f9a970d8ef43`, `ev-934794d4c8c3`, `ev-aa67ff6041da`, `ev-821de341ddd7`, `ev-6ee2cd9496e1`.
- **Why it carries weight:** A single common MWAA standard cannot ignore that IAD is a one-anchor, international-connection hub and DCA is a slot-controlled, one-dominant-carrier domestic O&D airport. Airline paging behavior, agent-podium volume habits, hold-room audio spillover, and change-of-gate messaging are different problems in the two facilities. Any recommendation to bind airline hold-room audio through tenant standards has to survive the AUL negotiation with United at IAD and American at DCA on separate terms.
- **Status:** usable, medium (trade press). **Caveat:** shares are directional; not the primary MWAA disclosure a rate-setting analysis would use.

### E-07. The peer set frequently cited as "silent airports" is structurally different from IAD or DCA

- **Claim:** London City Airport has operated a silent policy since 2008 (extended 2016); Amsterdam Schiphol, Copenhagen (CPH), and Helsinki-Vantaa (HEL, since 2015) each describe reduced-announcement models with information moved to FIDS and airport apps.
- **Corroboration cluster:** LCY — `infrastructure-economist::ev-3bf14ae0605d`, `operations-analyst::ev-5d567abf10b8`, `technology-scout::ev-49076621090e`, `contrarian::ev-f94112da8250` and `ev-915503a5cdba`, `airline-commercial-strategist::ev-db5037838852`, `quantitative-analyst::ev-7a4770dbf392`. AMS — `infrastructure-economist::ev-f465616ef0c6`, `operations-analyst::ev-d05117e47cf7` and `ev-6a1482711034`, `contrarian::ev-37c78c08cfd1`, `quantitative-analyst::ev-53eac5308f0d`. CPH — `technology-scout::ev-9c7e329a7616`. HEL — `technology-scout::ev-436a5e8bb2a2`, `quantitative-analyst::ev-8a0758b6d0c1`.
- **Why it carries weight:** Every "silent airport" story cited is either single-terminal, short-haul European, business-traveler-dominant, or accompanied by air-side noise policy that is not a terminal-interior analogue. None matches IAD's 36%+ international share, non-English-speaking connecting flow, or DCA's slot-constrained peaking. The peer citations belong in the article as pattern evidence and cautionary tale, not as design precedent.
- **Status:** usable, high (operator self-descriptions) / medium (secondary reporting). Contrarian correctly flagged that LCY's noise-management apparatus is community-facing air noise, not terminal acoustics.

### E-08. SFO's Quiet Airport program is the closest North American precedent — and the least defensible on measurement

- **Claim:** SFO reports that its Quiet Airport program removed approximately 90 minutes of daily terminal announcement time, reduced individual paging from 492 to 261 occurrences per day (47%), reduced cumulative paging duration from 145 to 58 minutes per day (60%), reduced gate-seating announcements by 40%, and reduced overall onsite noise by more than 40%. Passenger-experience reporting includes accounts of missed flights and confusion.
- **Corroboration cluster (positive):** `infrastructure-economist::ev-941fb7139ec7`, `operations-analyst::ev-abe9980793ed`, `technology-scout::ev-6510887ff6a5`, `contrarian::ev-7bde4bb0adbf`, `virtual-christian::ev-b5214be3aea4` and `ev-9d246c576cda`, `airline-commercial-strategist::ev-ee84950199f2`, `airport-ceo::ev-4df8bdfff78e`, `airport-emergency-management-director::ev-c8908972475c` (9 records, 8 agents).
- **Contradiction cluster (negative):** `operations-analyst::ev-ccf2fd3ef094`, `contrarian::ev-3840eded78c8` — passenger complaints and missed-flight anecdotes.
- **Why it carries weight:** SFO is the most-cited North American precedent, and it is what a board member will bring up. But **not a single ledger record identifies a published SFO measurement methodology** (baseline dB, integration window, receiver locations, LEQ methodology). Every agent and every source reports the number the same way, and every one caveats it the same way. The Strategist should quote SFO for the operating model (zoning, final-call discontinuation, A-gate/B-gate separation) but must not quote the 40% and 90-minute numbers as if they were audited. The passenger-complaint counterweight is real reporting, not partisan spin.
- **Status:** medium confidence on program design; **low confidence on the headline numbers.** Airport Context Packet §9 already flags the same gap.

### E-09. The federal regulatory stack constrains what "reduce announcements" is allowed to mean

- **Claim:** MWAA is subject as a public entity to 28 CFR 35.160 (ADA Title II — effective communication and auxiliary aids); 2010 ADA Standards §219/§706 (assistive listening systems in each assembly area where audible communication is integral); airlines at IAD and DCA are subject to 14 CFR Part 382 (ACAA — accessible info at gate/ticket/customer service, accessible kiosks after Dec 12, 2016 up to 25% of installed machines); IAD and DCA as certificated airports are subject to 14 CFR Part 139 emergency-communications requirements; and 29 CFR 1910.95 requires a hearing-conservation program at 85 dB(A) 8-hour TWA employee exposure. IAD Main Terminal is a National Register-eligible historic district; changes trigger Section 106 consultation.
- **Corroboration cluster:** `regulatory-political-analyst::ev-3a0fb861baf5`, `ev-9c68fd9606da`, `ev-48c339c22ad1`, `ev-02b64dc7bbda`, `ev-22aec1117ee4`, `ev-92444680d4c6`; `contrarian::ev-aa028959594f` and `ev-209651e2f143`; `operations-analyst::ev-2c4b423a196e`; `virtual-christian::ev-2fcf4d1cea5b`; `virtual-christian::ev-0310472f48f9`.
- **Why it carries weight:** These are the "quiet does not mean fewer" hard constraints the thesis prompt itself flagged. The article's accessibility, safety, and preservation sections should cite these floors by regulation number, not by paraphrase. AIP eligibility (`regulatory-political-analyst::ev-92444680d4c6`) rules out federal AIP funding for exclusive-use terminal areas and revenue-producing terminal areas, which shapes the funding stack for any capex the standard implies.
- **Status:** usable, high (primary regulations).

### E-10. The January 29, 2025 DCA collision reset the political altitude of any "reduce PA" framing

- **Claim:** The January 29, 2025 midair collision at DCA (PSA/American 5342 and a U.S. Army UH-60L) killed 67 people; NTSB AIR-26/02 (February 2026 final) attributed the collision to overlapping systemic failures across FAA, ATC, and military operations. FAA responded with helicopter route changes on March 14, 2025 that affect DCA operational tempo.
- **Corroboration cluster:** `airport-emergency-management-director::ev-84be36aecf07`, `ev-57cf7ec5f0cc`, `ev-f77647c9aa61`; `airline-commercial-strategist::ev-4e948d383d14`; `regulatory-political-analyst::ev-f4fd32e75644`; `virtual-christian::ev-3faefcb5157a`.
- **Why it carries weight:** Board tolerance for any recommendation that could be paraphrased as "MWAA reduced safety announcements" is materially compressed for the foreseeable future. The framing "quiet-by-design preserves redundant emergency communication and localized intelligibility" is not a rhetorical flourish; it is a survival condition for the recommendation.
- **Status:** high confidence; NTSB report is the primary source.

---

## 2. What is genuinely non-obvious

The following observations do not appear on the surface of the individual briefs but emerge from cross-reading the ledger.

1. **The Silent Airport peer set is a category error.** LCY, HEL, CPH, and AMS are held up as models for MWAA, but three of the four are single-terminal, business-traveler-heavy Northern European airports with high English proficiency and low international-connection load. The Council found no ledger record showing any of them has published intelligibility measurements or missed-boarding data. They are policy analogues, not design precedents.

2. **The SFO number that circulates most widely (40% / 90 minutes) has no published methodology in any source the swarm found.** This is the single largest citation risk in the article. It is safe to reproduce as SFO's reported figure, attributed to SFO, with the caveat. It is not safe to treat as measured evidence.

3. **IEC 60268-16 explicitly excludes fluctuating noise from the STI model.** Only Contrarian caught this. Terminal environments are the paradigm fluctuating-noise environment. STIPA acceptance at commissioning is necessary but not sufficient; MWAA needs an operational verification protocol that measures under representative traffic conditions, not just at 06:00.

4. **NFPA 72 requires an Acoustically Distinguishable Space map before it can be measured.** MWAA cannot audit intelligibility until it decides what its ADS zones are. This is a Design Manual amendment before it is a spec, and it likely does not exist today (see gap §5.a).

5. **AIP will not fund the majority of the terminal-interior capex a quiet-by-design standard implies.** FAA AIP does not fund exclusive-use terminal areas or revenue-producing terminal areas. That routes the funding stack toward PFC ($4.50 cap, unchanged since 2000), airline recovery under the AUL, and MWAA general airport revenue bonds. The debt-service coverage compression window makes the recovery route the harder sell.

6. **The Cranky Flier / airline-briefing $90.64 CPE figure for IAD's transformation is directional airline-side positioning, not an MWAA number.** It appears once in the ledger (`airline-commercial-strategist::ev-ae855a6678ab`). Do not attribute it to MWAA. Do consider it as the number the airline consultation will start from.

7. **The 2025 AUL's MII provisions and cost-recovery categorization are not verified from primary text.** Any Strategist claim that "the airlines can/cannot veto" a specific design category is inference until MWAA's AUL cost-center language is read. The context packet flags this and the ledger does not close it.

8. **Automation and audit logging are the operational-governance breakthrough hiding inside this thesis.** ACI-NA (`operations-analyst::ev-08af28494c7c`) frames data-driven automated announcement platforms in terms of centralized management, replay/audit logs, and elimination of manual-initiation errors. That reframes "announcement governance" from a customer-experience conversation to an operational integrity and enforcement conversation, which is far more compatible with a Design Manual amendment.

9. **The strongest lateral analogy in the ledger is not another airport.** It is the Joint Commission's clinical-alarm National Patient Safety Goal (`virtual-christian::ev-780eab34e4f2`), enacted in two phases (2014/2016) after ICUs began measuring 771 alarms per bed per day. That is the model of a governance body forcing rank-and-consolidate discipline on legacy safety messaging. Cite it once, not twice, and only if the article has room for a lateral move.

10. **The DCA replacement of Terminal 1 is the actual reason to adopt this standard now.** IAD's C/D replacement gets more airtime because of the July 29, 2026 announcement, but the DCA Terminal 1 replacement is the smaller, less politicized project where an adopted MWAA standard can be piloted with the least MII friction and the most immediate architectural leverage.

---

## 3. Agreements and contradictions across the swarm

### Strong agreement (the numbers the article can rely on)

| Claim | Agents in agreement |
|---|---|
| ACRP 175 minimum STI 0.45 / SNR 10–15 dB(A) for pier-style lounges | 10 |
| NFPA 72 intelligibility floor STI 0.45 / avg 0.50 per ADS | 6 |
| IEC 60268-16:2020 as measurement standard | 8 |
| MWAA Design Manual has "force of law" and is the delivery vehicle | 8 |
| MWAA 2025 AUL: $9B capital, $6.99B IAD, $2.39B DCA | 7 |
| MWAA debt trajectory (Aa3/AA−/AA−; ~$5.5B new debt; DSCR 1.63→1.3×) | 7 |
| IAD 2025 traffic ~29.01M / 10.53M international | 6 |
| DCA 2025 traffic ~24.89M | 5 |
| SFO Quiet Airport program design (zoning, final-call discontinuation) | 8 |

### Live contradictions the Strategist must preserve

1. **SFO reported outcomes vs. SFO passenger experience.** The 40%/90-minute claim (positive) and the missed-flight / stress reporting (negative) coexist in the ledger. The article should not collapse this into a one-sided story. Both are real, both are secondary.
2. **STI floor claimed for NFPA 72.** `airport-coo::ev-c382f952da3e` reports one trade source saying the NFPA 72 target is 0.70 STI over 90% of the covered area, with a floor of 0.50; `quantitative-analyst::ev-8cb15085981e`, `contrarian::ev-58a4b35511d3`, `regulatory-political-analyst::ev-3a0fb861baf5`, and `airport-emergency-management-director::ev-bf6c2224cb0c` report the more common 0.45 measurement / 0.50 average formulation. Both trace back to secondary summaries of a paywalled code. The article should quote the more widely corroborated version (0.45/0.50) and cite the licensed edition MWAA adopts.
3. **General voice-alarm STI target.** Airport CEO records (`ev-7b922862ed5c`) cite 0.60+ for emergency voice alarm; other agents cite 0.50. Both are within the EN 54-16 / IEC 60849 space. The article should not pick a single number without naming the standard.
4. **Program cost figures for IAD.** The July 29, 2026 announcement is variously reported as "$20B+," "$20B+ transformation," and "$22.5B" (`airport-ceo::ev-2d60eddcc4ee`). Use "approximately $20 billion or more, announced July 29, 2026" and cite the MWAA release when it appears.
5. **United's posture toward the IAD program.** United publicly co-branded the announcement; Cranky Flier (`airline-commercial-strategist::ev-25589088b745`) reads Kirby's body language as reluctant and characterizes the airline as prepared to shelve pieces under a future administration. Both readings are in play. The article should not present United as unambiguously enthusiastic.

---

## 4. The strongest evidence against the thesis

The thesis is "MWAA should adopt a common quiet-by-design standard across IAD and DCA." The strongest evidence-based case against, drawn from the ledger:

1. **The measurement standards do not fit the environment.** IEC 60268-16 explicitly does not cover fluctuating noise; ACRP 175 is 2017 and its samples predate several new large-hub terminal typologies. A "common standard" built on numbers the standards themselves scope narrowly may be sold to a board as more rigorous than it is (Contrarian, Operations Analyst).
2. **The best-known North American precedent has no published methodology.** SFO's 40% and 90-minute claims are repeated across trade press without a single primary measurement source in the ledger. Building an MWAA standard around SFO's model without demanding SFO's methodology inherits the flaw (Contrarian, Ops Analyst).
3. **The peer set is structurally different.** LCY, HEL, CPH, and AMS do not process IAD's international-connection load or DCA's slot-constrained peaks; they were quieter in the first place. Copying their policy without their traveler mix is category-mismatch (Contrarian, Airline Commercial Strategist).
4. **Passengers who need announcements the most are the ones a quiet regime excludes.** Non-English-speaking travelers, infrequent flyers, travelers without smartphones, older adults, and people with cognitive or sensory-processing differences are the same populations 14 CFR Part 382, 28 CFR 35.160, and ACRP 239 obligate MWAA to serve. Reducing PA without compensating channels compounds exclusion (Regulatory-Political Analyst, Contrarian).
5. **MWAA is entering its tightest debt-service coverage window in the current capital cycle.** Adding cost-recovery-eligible standards during a DSCR compression is a hard sell; adding standards that reduce late-stage rework is an easier one. The thesis has to make the second case, not the first (Infrastructure Economist, Airport CEO).
6. **The post-collision political stack does not want a "reduce announcements" story.** Any headline that reads "MWAA cuts safety broadcasts" is politically radioactive in the wake of NTSB AIR-26/02 (Emergency Management Director, Regulatory-Political Analyst, Virtual Christian).
7. **The Design Manual pathway means change is slower than the case for standards implies.** Amendments run through the Office of Engineering, engage MASTERSPEC editing, and interact with the AUL — this is not a policy memo that ships in a quarter (Airport CEO, Virtual Chris).

**These are not fatal to the thesis; they are the constraints the thesis has to survive to be credible.** Every one of them is answerable inside the argument.

---

## 5. Evidence gaps the run did not close

Gaps are ranked by how much they could change the conclusion.

**a. Whether the current MWAA 2020 Design Manual already contains acoustic, PA-zoning, STI, or L~Aeq~ requirements — and at what tier.** This is the single most consequential unknown. Every agent flagged it; none closed it. The recommendation's shape (new volume vs. amendment vs. section-level insertion) depends on this. **Recommended targeted fill:** MWAA Design Manual Volume 2 (Design Development) and applicable Specifications sections. The document is public on mwaa.com.

**b. Majority-in-interest thresholds, exempt-project categories, and cost-recovery categorization under the 2025 AUL.** The article should not infer that airlines can or cannot veto specific quiet-by-design capex categories. Without primary AUL text, any assertion about airline consent is inference. Context Packet §10 flags the same gap.

**c. Current MWAA commissioning and post-occupancy verification requirements for audio, FIDS, and quiet-zone systems.** Whether Ch. 9 ACRP-175-style commissioning already appears in MWAA's specifications determines whether the standard is a spec revision or a program-management redesign.

**d. Enforcement mechanics for tenant-installed audio and television systems** — airline clubs, concessions, airline gate podium equipment. If tenant audio is out of scope of the Design Manual today, the recommendation must specify how it comes in scope (AUL amendment, tenant technology standards, both).

**e. Status of the DCA Terminal 1 main concourse replacement.** The Council could not confirm whether Terminal 1 is in design phase, procurement phase, or funded programming only. This changes the "when" of the mandatory-vs-context-dependent split for DCA.

**f. Primary methodology for SFO's Quiet Airport program.** SFO Airport Commission minutes or an internal Quiet Airport program report would resolve whether the 40% / 90-minute numbers rest on measurement or on operating logs. Absent that, the numbers should stay attributed and caveated.

**g. Primary operator documentation for LCY, HEL, CPH, AMS.** The ledger relies on airport self-descriptions and trade press. Before the article quotes any peer as design precedent (as opposed to policy analogue), it should cite the peer operator's design or specifications document, not just its accessibility page.

**h. Ambient sound and reverberation measurement at Concourse E as commissioned.** Concourse E opens fall 2026. It is the only IAD facility likely to have modern acoustic and PA design assumptions on the record. A baseline STI/LEQ read at commissioning would anchor every subsequent MWAA claim about what "as-designed" performance looks like.

---

## 6. Source-quality warnings and stale data

- **NFPA 72 and IEC 60268-16 are both paywalled.** Every ledger record on these codes is a secondary summary. MWAA specification language must cite the licensed edition adopted by the AHJ, not the industry blog it was paraphrased from.
- **ACRP 175 is 2017.** Its terminal survey base predates several of the large-hub terminal typologies now under construction. Cite as the standing U.S. reference; do not claim it as current.
- **ACRP 239 (2023) is more current** and is the right source for the accessibility and older-adult side of the argument (`contrarian::ev-7fb259c1c5c5`).
- **Cost-of-rework figures (5%, 1–9%, 70%) trace to reworkcost.com's restatement of CII data.** For citation-grade use pull the underlying CII publications (RT-153 and successors). `infrastructure-economist::ev-75cbcaa2a2a2` and `ev-10838ca6e52a`.
- **Denver International baggage system and Berlin Brandenburg case studies are widely cited but the ledger relies on blog and encyclopedia summaries.** For a peer-reviewed article they are fine as illustrative; for citation-grade use pull GAO / City of Denver audit and Bundesrechnungshof reports respectively.
- **Bond Buyer coverage is subscription-gated.** MWAA credit numbers should be traced to Fitch, Moody's, and S&P rating reports directly.
- **Cranky Flier is analyst commentary, not carrier or airport disclosure.** Cite as industry-analyst read, not as United or MWAA position.
- **Wikipedia entries** (`operations-analyst::ev-7c4c9dffd53b`, `infrastructure-economist::ev-b694ee5e8eb2`, `airport-emergency-management-director::ev-260e169b0f63`) — usable for convenience citation only. For any load-bearing claim replace with the primary.

---

## 7. Do not claim

Statements that appear plausible from the ledger but that the ledger does not actually support:

- **Do not claim that SFO's Quiet Airport program has been independently measured to reduce announcements by 40% or noise by 40%.** Both figures are self-reported without published methodology in every source the swarm found.
- **Do not claim that MWAA airlines can or cannot veto a specific quiet-by-design capex category.** The AUL's MII provisions were not verified from primary text.
- **Do not claim that LCY, HEL, CPH, or AMS have "measured" the benefits of their silent regimes.** No ledger record contains a published intelligibility, missed-boarding, or channel-redundancy measurement for any of them.
- **Do not claim that airline hold-room PA at IAD or DCA is subject to MWAA design authority today.** Preferential-use holdroom conventions suggest airline control at the podium; MWAA-specific gate arrangement is not confirmed from an MWAA document in this run.
- **Do not claim that the IAD $20B+ program includes a quiet-by-design specification.** The July 29, 2026 announcement summary in the ledger does not mention acoustic or PA design elements.
- **Do not claim the MWAA Design Manual currently lacks acoustic or PA-zoning requirements.** The Council did not verify what is or is not in the Manual today. The correct framing is "the current content is unverified in this research pass."
- **Do not claim that the 2020 Design Manual is out of date.** It is described by MWAA as annually updated; the 2020 label reflects the base edition, not the current effective content.
- **Do not attribute the $90.64 CPE figure to MWAA.** It is an airline-briefing figure reported by Cranky Flier.
- **Do not claim NFPA 72 uses a single STI number.** It uses two (measurement-location minimum 0.45; ADS average 0.50), and secondary summaries paraphrase them differently.
- **Do not claim quiet-airport policy reduces missed flights.** No ledger record shows this. The available evidence suggests the opposite is a real risk at SFO.

---

## 8. Candidate airport cases and quantitative exhibits for the article

### Peer cases the Strategist should choose from

| Airport | Use | Strength | Weakness |
|---|---|---|---|
| London City (LCY) | Longest-running silent regime; policy-as-brand exemplar | Airport-published, in force since 2008/2016 | Structurally unlike IAD/DCA; no published intelligibility data |
| Amsterdam Schiphol | Large-hub silent operating model with FIDS-first messaging | Operator-published; 2025 CSAT 3.84/5 | Composite CSAT does not isolate the announcement effect |
| Helsinki-Vantaa | Silent regime since 2015 with gate-area override | Long-tenured; explicit gate-area retention | Trade-press description; no primary Finavia doc in ledger |
| Copenhagen (CPH) | Explicit "no Go-to-Gate/Boarding" over PA; app-first | Operator-published policy language | Scope confined to gate/boarding announcements |
| San Francisco (SFO) | Closest North American operating model | Operating model is well-described; documented zoning approach | Reported outcome figures lack published methodology; documented passenger complaints |
| Phoenix Sky Harbor (PHX) | Hearing-loop deployment (Gates D11–D18) | Airport-published | Not a whole-terminal quiet program |
| Seattle-Tacoma (SEA) | Hearing loops + Sensory Room | Operator information available | Ledger has only secondary summary; get Port of Seattle direct |
| Indianapolis (IND) | Sensory rooms on Concourses A/B | Airport-published | Not a quiet-terminal program |
| Pittsburgh (PIT) | Presley's Place sensory suite (1,500 sq ft, 2019) | Well-documented sensory space | "World's most advanced" is PR framing |
| Atlanta (ATL) | Multi-Sensory Room in Concourse F | Consistent with best-practice cluster | Secondary reporting only |
| Fort Lauderdale (FLL) | 2017 active-shooter AAR — communications lessons | Primary airport AAR available | Cite as continuity/emergency case, not quiet-airport case |
| Berlin Brandenburg (BER) | Program-cost cautionary tale | Widely cited | Blog-level source in ledger; get Bundesrechnungshof for citation |

### Quantitative exhibits the article can support without additional research

- **The intelligibility performance band.** ACRP 175 target 0.50 STI, acceptable band 0.46–0.53, minimum 0.45; NFPA 72 emergency floor 0.45 measurement / 0.50 average; SNR 10–15 dB(A). All corroborated.
- **The IEC 60268-16 STI qualitative categories.** Bad (<0.30), Poor (0.30–0.45), Fair (0.45–0.60), Good (0.60–0.75), Excellent (>0.75).
- **OSHA employee-exposure floor.** 85 dB(A) 8-hour TWA (hearing-conservation trigger); 90 dB(A) PEL. `operations-analyst::ev-2c4b423a196e`; `virtual-christian::ev-2fcf4d1cea5b`.
- **Sensory-quiet zone reference benchmark.** ANSI/ASA S12.60 core-learning-space background not exceeding 35 dB(A) (approx. NC 27) — reference for MWAA-defined low-stimulation zones only, not for main terminal ambient. `quantitative-analyst::ev-9b2f7d231121`.
- **MWAA financial position.** Aa3/AA−/AA− stable; ~$5.5B new debt 2025–2028; DSCR 1.63× (2024) → ~1.3× over five years; adjusted debt/O&D peaking ~$400 in 2028; 2025 AUL $9B ($6.99B IAD + $2.39B DCA), 140% airline-funded DSCR target.
- **IAD / DCA traffic mix.** IAD 29.01M / 10.53M international (~36%+, up 6.4% YoY, highest 2025 growth among top-50 U.S. airports); DCA 24.89M (down 5.4% YoY).
- **Rework cost heuristics (framing, not measurement).** Direct rework ~5% average total project cost (2–20% range); design-related errors 1–9% total project cost and up to 70% of construction rework — CII-derived, restated by rework-cost.com. Use as framing.
- **IAD Concourse E facts.** ~435,000 sq ft, 14 United gates, AeroTrain-connected, opens fall 2026, project cost >$500M with United, MWAA, and federal infrastructure grant mix.
- **SFO Quiet Airport reported outcomes (with caveat).** 90 minutes daily announcement-time reduction, 40% gate-seating reduction, 40%+ onsite noise reduction, 47% paging occurrence reduction (492 → 261), 60% paging duration reduction (145 → 58 min). Every figure attributed to SFO; methodology not published.
- **Airline concentration.** United ~67% of IAD, ~50 jetbridge gates; American ~53% of DCA. Concourse E adds 14 United gates.
- **Regulatory floors.** 28 CFR 35.160; 2010 ADA §219/§706; 14 CFR Part 382 (kiosks: 25% accessible after Dec 12, 2016); 14 CFR Part 139 emergency comms; 29 CFR 1910.95; NFPA 72 Ch. 24; PFC cap $4.50 (unchanged since 2000); AIP eligibility excludes exclusive-use and revenue-producing terminal areas.

---

## 9. What the Strategist should not carry forward

- The infrastructure-economist's broad U.S. airport-industry capex numbers ($173.9B ACI-NA, $130–140B large-hub aggregate) — useful only as context. Not load-bearing for the thesis.
- Denver International baggage system and Berlin Brandenburg case studies — usable as one-line framing, not as central evidence.
- The 1-10-100 heuristic — cited by infrastructure-economist as framing, marked low-confidence in the ledger. Do not use as a calculated number.
- The airline no-show rate (5–18%, 14.4% avg from 2019) — conflates true no-shows with missed-at-gate; do not use as the operational-downside control number for a reduced-PA regime.
- The Johns Hopkins ICU 771 alarms/bed/day figure — illustrative magnitude only if the article makes the clinical-alarm lateral move.
- Any beam-steerable or directional-audio vendor claim — usable to establish that the technology exists; not usable to specify performance numbers without independent measurement.

---

## 10. Handoff notes for the Strategist

- **The argument's spine is E-04 (Design Manual as vehicle) + E-05 (financial window) + E-06 (airline asymmetry) + E-10 (post-collision political stack).** Everything else supports.
- **The article's technical credibility rests on citing ACRP 175, NFPA 72 Ch. 24, IEC 60268-16 correctly, with the fluctuating-noise caveat surfaced once.**
- **The peer-airport section is a policy-analogue section, not a design-precedent section.** Frame it that way.
- **The mandatory-vs-context-dependent split should track (a) safety and accessibility floors — mandatory both airports, (b) intelligibility performance thresholds — mandatory both airports, (c) announcement governance and PA zoning — mandatory in principle, context-dependent in tier, (d) sensory-quiet zones and hearing-loop deployment — mandatory presence, context-dependent scope, (e) tenant-audio and television controls — mandatory framework, context-dependent enforcement.**
- **The DCA Terminal 1 replacement is the pilot case.** Say so. It is the smaller, less-politicized project where an adopted standard can be exercised first.
- **Do not lead with SFO.** Lead with what MWAA already owns (the Design Manual) and what MWAA is already committed to spend (the AUL capital program and $20B+ transformation).

---

*The evidence ledger at `outputs/evidence-ledger.jsonl` is preserved with full per-agent lineage. Where duplicate records exist across agents, this map identifies the corroboration cluster rather than collapsing the underlying records — that preserves independent-discovery audit trail and lets a reviewer verify the consensus rather than take the curator's word for it.*
