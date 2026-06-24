# Technology Scout Brief — Procurement Technology and the MWAA Contracting Manual

**Run:** From Compliance to Capability: A Strategic Review of the MWAA Contracting Manual
**Lens:** What "digital procurement" and "operational intelligence" mean concretely in a contracting function — what they cost, what they return, what is real in 2026, and what is still vendor theater.
**Scope note:** I read the Contracting Manual (Revised Sixth Edition 6.0, effective 5/20/2026) before any outside research, and I quote it directly. I did not read any other Stage 1 brief.

---

## 1. The headline conflict: MWAA defines its "system" as paper, not software

The single most revealing line in the Manual is its definition of MWAA's procurement infrastructure. General Policy §1.2(10) states that all procurements are "made within a Contract management system, for which the OSCM is responsible. **This system, which consists of procurement policies and processes**, ensures, at a minimum, that: (a) Solicitations and Contracts are properly issued… (e) Payments are made only for goods and services received" [Source: Contracting Manual v6.0 §1.2(10)].

Read that again. The Manual's "Contract management system" is a *governance construct* — policies and processes — not a software platform. In every modern procurement organization the phrase "contract management system" means a digital contract lifecycle management (CLM) tool: a searchable repository, clause libraries, obligation tracking, renewal alerts, and analytics. MWAA uses the same words to mean a binder of rules. That is the gap this brief exists to name.

This is not a drafting accident. Across 130 pages the Manual references technology almost nowhere. The few digital touchpoints are thin:

- **Advertising:** Solicitations ≥$50,000 are posted "on the Airports Authority's website or its managed portal accessible via the website" [Source: §4.1.5]. A sourcing portal apparently exists, but the Manual neither names it, requires electronic bid submission through it, nor builds any process around it.
- **Transparency:** Quarterly procurement reports are "made available on the Airports Authority's website: www.mwaa.com" [Source: §1.5.2] — i.e., a static PDF, not a queryable open-data feed.
- **Micro-purchases:** Governed by a separate "Purchasing Card (P-card) Policy" [Source: §3.2]. The one genuinely automated channel sits outside the Manual.
- **Vendor registration:** Interested parties "may register to be included in a list" — the Planholders List [Source: §4.1.8] — a manual, opt-in distribution list, not a managed supplier-relationship database.
- **Past performance:** "COTRs shall assess Contractor performance through written evaluation" and these "may be used when considering past performance during future Solicitations" [Source: §5.15]. Two sentences. No central, scored, structured vendor-performance database; no requirement that the data be used; no governance over its quality.

The Manual is a well-built compliance instrument from the FTA/FAR tradition (Chapter 10 alone imports FTA Circular 4220.1F wholesale). It is essentially silent on the technology layer that has reorganized public procurement over the last fifteen years. **That silence — not any specific bad rule — is the modernization opportunity a technology scout flags.**

---

## 2. A taxonomy: what "procurement operational intelligence" actually is

To benchmark MWAA, you need a shared vocabulary. Procurement technology is not one thing. It is five layers, in rough order of maturity and proven return:

**Tier 1 — Transactional digitization (mature, proven, commodity).**
e-Sourcing (electronic RFx and bid submission), e-Auctions/reverse auctions, electronic catalogs, P-cards, and purchase-order/invoice automation (procure-to-pay, P2P). This is off-the-shelf in 2026 from a dozen vendors. The question is not whether it works; it is whether you've bought it.

**Tier 2 — Source-to-pay (S2P) suites (mature, integration-heavy).**
A single platform spanning intake, sourcing, contract authoring/CLM, supplier management, and P2P. JAGGAER, Ivalua, Coupa, SAP Ariba, and public-sector specialists like Euna (formerly Bonfire/mdf) and OpenGov dominate. Real, but implementations are where money and timelines die.

**Tier 3 — Supplier and market intelligence (maturing).**
Centralized supplier registration and qualification, structured past-performance scoring, diversity/DBE tracking, and spend analytics ("category management" by data rather than anecdote). The federal analog is CPARS (performance) and SAM.gov (registration/exclusions).

**Tier 4 — Cooperative and pre-competed access (mature, policy-dependent).**
Sourcewell, OMNIA Partners, NASPO ValuePoint — a $65+ billion market that lets a public agency buy off a contract someone else competed [Source: https://www.sledai.com/blog/cooperative-purchasing-vendor-guide/]. This is a *speed* technology as much as a savings one. MWAA already permits it (§3.7, "Contracts Procured by or with Other Governmental Entities") but builds no muscle around it.

**Tier 5 — AI/analytics (real in narrow uses, hype-saturated overall).**
Generative AI for RFP/solicitation drafting, contract summarization and clause extraction, spend classification, and supplier discovery. This is the loudest category and the least mature in deployment.

**What does *not* count as operational intelligence:** posting a PDF on a website, an opt-in email list, or relabeling a policy binder a "system." Those are the analog substitutes for each tier — and they are roughly what the Manual codifies today.

---

## 3. Key findings

1. **MWAA's Manual is a compliance document with a technology hole.** It governs *what is allowed* but is silent on *the platform that would make it fast, measurable, and transparent.* The word "system" in §1.2(10) means policy, not software — a tell that procurement digitization has not been conceptualized as infrastructure.

2. **The proven, low-risk wins are Tier 1–2, not AI.** Electronic sourcing, structured supplier registration, and spend analytics have a longer and more independently verified track record than anything with "AI" in the name.

3. **Virginia runs the most relevant benchmark in MWAA's own backyard — eVA — and MWAA is not on it.** As a federal-compact authority MWAA is not bound to the Commonwealth's system, but eVA is the obvious reference class and a ready-made comparison the board will understand.

4. **Vendor ROI numbers are aggressive and should be quarantined.** Claims of "40–60% cycle-time cuts" and "300–500% ROI in 18 months" come from vendor marketing, not audits. Use them as direction, not as business-case inputs.

5. **The most credible airport-specific evidence is modest and peer-reviewed:** digital procurement at Airports Company South Africa cut procurement turnaround from ~8 days to ~4 days. Halving cycle time is a real, defensible target — and far below the vendor headline numbers.

6. **Reverse auctions are a cautionary tale, not a slam dunk.** GAO documented real savings *and* one-bidder auctions, opaque fees, and unverifiable savings claims; GSA shut its own reverse-auction platform in 2018. Technology adds value only inside good process design.

7. **Past-performance data is only as good as the discipline behind it.** The federal CPARS system — far more structured than MWAA's §5.15 — is independently criticized for late, inaccurate, "satisfactory"-biased entries. A MWAA vendor-scoring database without enforced data discipline will reproduce that failure.

8. **AI in procurement is mostly intent, not deployment.** EY's 2025 CPO survey: 80% of CPOs plan generative-AI use within three years, but only ~36% have meaningful implementations today. Plan for the narrow, supervised uses; discount the autonomous ones.

---

## 4. Evidence

### Tier 1–2: e-procurement returns (mixed provenance — read the source line)

The most quotable benchmark is Virginia's **eVA**, which sits adjacent to MWAA's jurisdiction. Reported results: more than **$25 million in savings annually**, **$280 million cumulative** since 2001, order processing costs cut **up to 50 percent**, and processing time reduced **up to 70 percent** in some cases, across 245+ state agencies and 900+ local bodies [Source: https://www.cgi.com/en/cgi-contract-extended-commonwealth-virginia-state-reaps-benefits-eva-procurement-system]. **Provenance caveat:** these figures originate from CGI, the system integrator, and the Commonwealth — vendor- and operator-reported, not independently audited. eVA today runs on an Ivalua S2P platform [Source: https://www.ivalua.com/press-releases/virginia-uses-ivaluas-platform/], which is relevant if MWAA wants a proven public-sector reference architecture rather than a bespoke build.

Generic S2P vendor claims run much hotter: "58% faster sourcing cycle times," "40–60% cycle-time cuts within 90 days," and "300–500% ROI within 18 months" [Source: https://www.ivalua.com/blog/procurement-automation-software/]. **Treat as marketing.** The same body of vendor literature concedes that "traditional ERP-based procurement implementations routinely take 6 to 12 months, with industry data showing 80% go over budget and over schedule" [Source: https://www.ivalua.com/blog/procurement-automation-software/] — a rare honest admission that the implementation, not the software, is the risk. Public-sector specialists (Euna, OpenGov) quote 3–6 month go-lives, which is more plausible for a focused sourcing module than a full suite.

**Airport-specific, peer-reviewed evidence** is the most trustworthy and the most sobering. A 2023 study of digital procurement at Airports Company South Africa found procurement cycle time fell from "approximately eight days down to four days" [Source: https://www.mdpi.com/2071-1050/15/5/4610]. That is a 50% cut — real, material, and an order of magnitude below the vendor headline numbers. It is the figure I would anchor a MWAA business case to.

### Tier 1: reverse auctions — the independent-evaluation cold shower

Reverse auctions are the cleanest example of why MWAA should distinguish vendor claims from audits. The optimistic read: GAO found reverse auctions saved buyers ~23% against estimates, and GSA's platform generated "22 percent savings off Independent Government Cost Estimates" [Source: https://www.gao.gov/products/gao-14-200T].

The skeptical read, from the same auditor: GAO-18-446 found that mandating reverse auctions "may contribute to agencies obligating more money through reverse auctions that attract only one bidder" — at the State Department, nearly **40 percent** of reverse-auction dollar value drew a single bidder. Agencies "indirectly paid $3 million in fees when a free alternative was likely available," 28 of 30 contracting officials "did not fully understand how fees were set," and there was "a lack of sufficient data available for agencies to verify actual cost savings" [Source: https://www.gao.gov/products/gao-18-446]. GSA closed its reverse-auction platform in 2018 [Source: https://federalnewsnetwork.com/reporters-notebook-jason-miller/2018/08/gsa-to-close-down-reverse-auction-platform-after-5-years/].

**Lesson for MWAA:** a tool that produces a single bidder and unverifiable savings is worse than the §3.3 three-quote process it would replace. Technology amplifies process; it does not fix it.

### Tier 3: supplier/performance intelligence — CPARS as the warning

MWAA's §5.15 past-performance provision is two sentences. The federal system it would have to grow into, CPARS, is far more structured — and independently criticized. Federal News Network: the system "takes too much time to fill out, lacks important details and isn't as accurate as it needs to be"; the DoD IG repeatedly found "a large percentage of DoD performance assessment reports are late and not prepared correctly"; and agencies give "satisfactory" ratings "more often than any other rating because the system is too cumbersome to justify higher or lower ratings" [Source: https://federalnewsnetwork.com/reporters-notebook-jason-miller/2019/06/why-contractor-past-performance-data-is-becoming-both-more-less-valuable/]. **Implication:** a vendor-scoring database is only as valuable as the COTR discipline feeding it. Build the data-quality requirement into the Manual, or don't build the database.

### Tier 4: cooperative purchasing — speed MWAA already has permission to use

Cooperative contracts (Sourcewell, OMNIA Partners, NASPO ValuePoint) let an agency "win one pre-competed master contract… and then sell to thousands of… agencies without responding to individual RFPs," a "$65+ billion market" [Source: https://www.sledai.com/blog/cooperative-purchasing-vendor-guide/]. Sourcewell aggregates 50,000+ members; OMNIA reaches 90,000+ eligible agencies [Source: https://www.omniapartners.com/industries/government]. MWAA's §3.7 already authorizes buying through other governmental entities' competed contracts — the policy door is open; what's missing is the operating discipline and the data to know when a co-op buy beats a fresh solicitation. **Caveat to name honestly:** co-op contracts trade speed for arms-length price competition, and overreliance can erode local market engagement and DBE participation (a core MWAA value per Chapter 2). The control is a documented "best value vs. fresh competition" test, not a blanket preference.

### Tier 5: AI — separate the narrow-and-real from the autonomous-and-hyped

The credible near-term uses are supervised and narrow. CPO polling puts the top generative-AI use cases at spend analytics/dashboarding (53%), RFP/RFQ generation (42%), and contract summarization/clause extraction (41%) [Source: https://artofprocurement.com/blog/state-of-ai-in-procurement]. The deployment reality is far behind the intent: EY's 2025 Global CPO Survey found 80% of CPOs plan to deploy generative AI within three years, but "only 36 percent [of] procurement organizations have meaningful generative AI implementations" today [Source: https://www.speclens.ai/blog/ai-in-procurement-complete-guide]. GAO has separately cautioned that agencies buying AI should "collect and apply lessons learned to improve future procurements" [Source: https://www.gao.gov/products/gao-26-107859] — a reminder that the public sector is still early on *buying* AI, let alone running procurement on it. **For MWAA:** AI-assisted solicitation drafting and contract summarization are usable now with a human in the loop; autonomous evaluation or award is neither mature nor defensible against a protest (Chapter 9).

---

## 5. Honest maturity assessment: what's real, what's hype

**Real and buyable off-the-shelf in 2026:**
- Electronic sourcing with online bid submission (replaces the §4.1.5 "post a PDF" model and the §4.1.8 manual Planholders List).
- Supplier registration/qualification portals with integrated DBE/SLBE tracking (Chapter 2 is run today on goodwill and spreadsheets).
- Spend analytics / category dashboards (the §1.5.2 quarterly PDF could be a live feed).
- P2P / invoice automation (extends the §3.2 P-card logic up the value chain).
- Cooperative-purchasing access (§3.7 already permits it).

**Real but implementation-risky (the budget killer):**
- Full source-to-pay suites and CLM. The software is proven; the integration with MWAA's finance systems, the data migration, and change management are where 80% of public-sector ERP-class projects run late and over budget. Phase it; never big-bang it.

**Narrow-real, supervised only:**
- Generative AI for drafting solicitations, summarizing contracts, classifying spend. Useful copilot; not an autonomous agent.

**Hype / not ready for a public airport authority:**
- Autonomous AI sourcing or evaluation. Indefensible against protest, unaudited, and outpaced by the documentation duty in Chapters 3–4 and 9.
- Vendor ROI multiples (300–500% in 18 months; 40–60% cycle cuts). Directionally interesting, evidentiarily worthless for a board paper.

**The honest synthesis:** MWAA does not have an AI problem; it has a Tier-1 problem. The Manual hasn't yet codified electronic sourcing, structured supplier data, or live spend transparency — the unglamorous layer with the deepest evidence base. Skipping that to chase AI would be buying the roof before the foundation.

---

## 6. Five data points a strategist can use verbatim

1. **"MWAA's Contracting Manual defines its 'Contract management system' as one that 'consists of procurement policies and processes' (§1.2(10)) — a governance binder, not a software platform. Everywhere else in public procurement, that phrase means a digital tool. The gap between those two definitions is the modernization agenda."**

2. **"Virginia's eVA reports saving the Commonwealth more than $280 million since 2001 and cutting order-processing time up to 70 percent — a working e-procurement reference architecture operating in MWAA's own region, which MWAA does not use."** [Source: https://www.cgi.com/en/cgi-contract-extended-commonwealth-virginia-state-reaps-benefits-eva-procurement-system] *(operator/integrator-reported, not audited)*

3. **"The most trustworthy airport-specific evidence is modest: digital procurement at Airports Company South Africa cut turnaround from about eight days to four. Halving cycle time is the realistic prize — not the 40–60 percent the software vendors advertise."** [Source: https://www.mdpi.com/2071-1050/15/5/4610]

4. **"GAO found nearly 40 percent of one agency's reverse-auction dollars drew a single bidder, that officials couldn't explain the fees they paid, and that there was 'a lack of sufficient data… to verify actual cost savings.' GSA shut its reverse-auction platform in 2018. A procurement tool that yields one bidder is worse than the three-quote rule it replaces."** [Source: https://www.gao.gov/products/gao-18-446]

5. **"Eighty percent of chief procurement officers plan to deploy generative AI within three years; only about 36 percent have meaningful implementations today. MWAA should buy for the supervised, narrow uses that exist — solicitation drafting, contract summarization, spend analytics — and discount the autonomous-AI pitch entirely."** [Source: https://www.speclens.ai/blog/ai-in-procurement-complete-guide]

---

## Sources

- MWAA Contracting Manual, Revised Sixth Edition (6.0), effective 5/20/2026 — §1.2(10), §1.4.1, §1.5.2, §3.2, §3.3, §3.7, §3.8.7, §3.8.8, §4.1.2–4.1.5, §4.1.8, §5.15 (operator-supplied source)
- [eVA results — CGI](https://www.cgi.com/en/cgi-contract-extended-commonwealth-virginia-state-reaps-benefits-eva-procurement-system)
- [Commonwealth of Virginia on Ivalua — Ivalua](https://www.ivalua.com/press-releases/virginia-uses-ivaluas-platform/)
- [Procurement automation buyer guide — Ivalua](https://www.ivalua.com/blog/procurement-automation-software/)
- [Digital procurement at an airport company (ACSA) — MDPI Sustainability](https://www.mdpi.com/2071-1050/15/5/4610)
- [Reverse auctions savings — GAO-14-200T](https://www.gao.gov/products/gao-14-200T)
- [Reverse auctions, additional guidance — GAO-18-446](https://www.gao.gov/products/gao-18-446)
- [GSA closing reverse-auction platform — Federal News Network](https://federalnewsnetwork.com/reporters-notebook-jason-miller/2018/08/gsa-to-close-down-reverse-auction-platform-after-5-years/)
- [CPARS past-performance criticism — Federal News Network](https://federalnewsnetwork.com/reporters-notebook-jason-miller/2019/06/why-contractor-past-performance-data-is-becoming-both-more-less-valuable/)
- [Cooperative purchasing market — SLED.AI](https://www.sledai.com/blog/cooperative-purchasing-vendor-guide/)
- [OMNIA Partners government cooperative](https://www.omniapartners.com/industries/government)
- [State of AI in Procurement 2026 — Art of Procurement](https://artofprocurement.com/blog/state-of-ai-in-procurement)
- [AI in procurement guide / EY CPO survey figure — SpecLens](https://www.speclens.ai/blog/ai-in-procurement-complete-guide)
- [AI acquisitions lessons learned — GAO-26-107859](https://www.gao.gov/products/gao-26-107859)
