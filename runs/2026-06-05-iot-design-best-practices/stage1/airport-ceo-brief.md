# Airport CEO Brief: IoT Architecture and the Stranded-Deployment Problem

**Run:** IoT Design Best Practices  
**Agent:** Airport CEO  
**Date:** June 2026  

---

## My Thesis, Stated Plainly

The architects and technology officers will write about LoRaWAN versus private 5G, edge compute placement, and open data schemas. Those questions matter. But the CEO's question is upstream of all of them: *who authorized the pilot architecture to become the permanent financial commitment, and at what threshold did it stop being a procurement decision and become a bond decision?*

Every stranded airport IoT deployment I am aware of failed at that hand-off — not because the sensors stopped working but because the decisions that surrounded the technology were made for a 12-month proof of concept and never remade for a 25-year revenue bond program. The thesis here is correct. The framing that follows is how it looks from this chair.

---

## Key Findings

**1. IoT capital is a bond decision dressed as a technology decision.**  
When a deployment scales past the operating-budget threshold and enters the capital program, it joins the amortization schedule that rating agencies scrutinize. Stranded technology assets — equipment that becomes unserviceable before the debt is retired — create real credit exposure. Moody's, S&P, and Fitch all score airports on financial metrics that include debt service coverage ratios (target: 2.0x over three-year rolling periods at large hubs) and asset management quality. A capital program that routinely produces five-year stranded assets, while carrying 25-to-30-year bonds, is a story you do not want to tell in a rating-agency briefing.

**2. In a residual use-and-lease framework, the airlines are paying for stranded IoT.**  
Residual airports pass net costs to signatory carriers. That means an IoT architecture that requires rip-and-replace every five years — because the vendor changed, the network standard changed, or the CIO changed — is a structured recurring cost that flows directly to airline rates and charges. Majority-in-Interest (MII) clauses in use-and-lease agreements require signatory airline approval for capital expenditures above contractual thresholds. Airlines at residual airports do not approve capital programs that produce stranded assets graciously. They approve them once; then they litigate, negotiate, and delay the next one.

**3. The federal stack does not cover IoT, and the window that did is now closed.**  
FAA AIP grant eligibility is tightly constrained to airfield safety, capacity, security, and environmental improvements. IT and IoT infrastructure is not eligible in any material sense. [Source: https://www.faa.gov/airports/aip/overview] The IIJA Airport Terminal Program ($1 billion per year for terminal development, FY2022-2026) offered the best near-term path to federal cost-sharing for technology embedded in terminal construction projects, but the final application window closed January 15, 2026. [Source: https://www.faa.gov/newsroom/FY26-ATP-NOFO-8DEC2025] The PFC cap has sat at $4.50 since AIR-21 in 2000 — the FAA Reauthorization Act of 2024 did not raise it — so the self-funding tool is worth roughly half in real dollars what it was when it was set. [Source: https://www.congress.gov/bill/118th-congress/house-bill/3935/text] That means IoT capital goes on the revenue bond program, at rates the market determines and credit agencies evaluate. Architecture decisions made in a pilot are being locked in on a 30-year amortization schedule funded by bonds priced off coverage ratios.

**4. Board governance creates systematic technology authorization gaps.**  
Airport boards approve capital programs by project and threshold. Technology that enters as a pilot below the approval threshold, succeeds, and then scales without returning to the board for authorization is the source of most stranded-deployment debt. Politically appointed boards at city-department airports (the governance structure associated with a median one-notch rating downgrade compared to independent authorities, per S&P 2023 methodology) face chair transitions every four to six years. A technology strategy that depends on sustained board commitment across two chair tenures and one mayoral administration is a strategy that will be repriced, reframed, or abandoned partway through. [Source: https://crp.trb.org/acrpwebresource1/airport-governance-structures-and-their-impact-on-financial-strategies/]

**5. Carrier concentration risk and technology risk compound.**  
Rating agencies treat single-carrier dominance as a distinct credit factor. Dallas Love Field runs 97% Southwest concentration and is rated A/Stable by S&P, with an explicit caveat on Southwest's pricing flexibility. CVG fell from A1 to Baa1 after Delta's de-hubbing in 2013. [Source: https://dwuconsulting.com/dwu-ai/airline-concentration-risk-hub-airports] A large-hub airport with significant carrier concentration that simultaneously carries technology stranded-asset risk on the balance sheet is presenting rating agencies with two converging vulnerabilities. They will price that combination.

**6. The CISO has become a gate on IoT deployment, and that gate is getting harder to open.**  
In 2022, 16% of organizations placed operational technology (OT) security under the CISO. By 2025, that figure was 52%. [Source: https://www.fortinet.com/resources/reports/state-ot-cybersecurity] Airport CISOs who inherit OT/IoT networks they did not design, running on protocols they cannot monitor, installed by vendors whose support relationships have changed, will kill programs rather than assume liability for them. Security segmentation failures in IoT-class OT equipment are now documented as pathways to critical infrastructure disruption. [Source: https://rm-cyber.com/resource/articles/lessons-from-unanticipated-ot-and-iot-vulnerabilities-at-major-airports/] This is not a technology problem the CEO delegates to the CIO. It is a capital program risk that belongs in the next board briefing.

**7. The CIO's chair rotates faster than the bond's amortization schedule.**  
CIO tenure at large US organizations averages under five years. An airport that builds IoT architecture around a CIO's technology preferences — proprietary platforms, single-vendor integrations, bespoke data schemas — is building something that the next CIO will spend the first three years of their tenure identifying as the predecessor's mistake. That is not an organizational observation. It is a financial one: the cost of architectural correction appears in the capital program, gets bonded, and sits on the balance sheet for two decades.

---

## Evidence

**Toronto Pearson International Airport — Seven-SCADA Fragmentation**  
GTAA's operational systems accreted over 15 years into seven independent SCADA platforms built on three different vendor stacks, each designed by different teams using different principles. [Source: https://inductiveautomation.com/resources/customerproject/toronto-airport-moves-from-seven-scada-systems-to-one] The result was systems that were "very hard and expensive to support, upgrade and maintain." No specific remediation cost was published, but the consolidation project required 12 months of parallel operation before transition. This is the canonical example of pilot-architecture drift at scale — not a single bad decision but 15 years of locally rational procurement choices that compounded into a structurally fragmented estate.

**Denver International Airport — Great Hall P3 Termination (2019)**  
Not an IoT deployment, but the governance failure pattern is identical. DEN signed a $1.8 billion concession (with $650 million in fixed construction) at 30% design completion. Eleven months into construction, the contractor requested a $288 million change order. DEN terminated the agreement 14 months after notice to proceed and settled for $183.6 million. [Source: https://dwuconsulting.com/dwu-ai/denver-great-hall-p3-failure] The airport's CEO identified five root causes, including incomplete pre-contract feasibility and insufficient oversight. The direct lesson: committing long-term financial structures to incompletely designed programs is how airports produce stranded capital at scale.

**Denver International Airport — Automated Baggage System (1995)**  
The original DEN automated baggage system — the most documented technology failure in US airport history — cost approximately $400 million in overruns and delayed the airport's opening by 16 months. [Source: https://medium.com/@ketan.keshav7/the-400-million-lesson-what-the-denver-airport-baggage-fiasco-taught-us-about-escalation-and-c6f0bbc37305] The system was eventually decommissioned and replaced with conventional baggage handling. It ran for roughly a decade before being abandoned. The bond obligations it generated did not retire with it.

**Sigfox Bankruptcy (January 2022)**  
Sigfox filed for insolvency in January 2022 with $150 million in debt. The French IoT carrier was acquired by Singapore-based UnaBiz in April 2022 for approximately €25 million. [Source: https://www.rcrwireless.com/20220929/carriers/unsuccessful-iot-deployments-on-nb-iot-sigfox-helium-lorawan-a-furore-about-failure] Enterprises that built IoT architectures on Sigfox connectivity — including facilities-management and supply-chain deployments — found themselves mid-contract with a bankrupt network operator and a new owner with different strategic priorities. UnaBiz subsequently filed for court protection again in 2025. [Source: https://www.rcrwireless.com/20250909/internet-of-things/sigfox-unabiz-court] Any airport that had deployed Sigfox-based sensors for environmental monitoring, equipment tracking, or utility metering would have faced two network transitions within five years of the original deployment.

**Dallas Love Field — Boingo Private CBRS Network**  
Boingo launched the first airport private CBRS LTE network at Love Field in 2018 and has since deployed private networks at Newark Terminal A (Wi-Fi 6, cellular DAS, private LTE) and operates connectivity at O'Hare. [Source: https://airportscouncil.org/2023/06/09/airport-5g-update-leveraging-cbrs-for-smart-operations/] The infrastructure is owned and operated by Boingo. The airport controls CBRS spectrum access within its footprint, but the operating relationship is with a third-party infrastructure provider. What happens to the network in 2028 when the operating agreement expires, Boingo is acquired, or CBRS allocation rules change is the question the CEO needs answered before the next use-and-lease negotiation, not after.

**Heathrow Terminal 5 Baggage System Failure (March 2008)**  
T5 opened with 23,000 bags stranded over five days, 500 flights cancelled, and British Airways demanding £10 million in compensation from BAA. [Source: https://spectrum.ieee.org/baggage-problem-hits-heathrow-terminal-5-] Root cause: testing was compressed and staff training was incomplete. The IT systems were not technically defective; the governance surrounding go-live was. The distinction matters because the same failure mode — governance absent where technology is present — is the mechanism behind stranded IoT deployments.

**ACI-NA Financial Benchmarking**  
ACI-NA's Financial Benchmarking Survey (FY2022, published 2023) is the industry standard for peer comparison of coverage ratios, days-cash-on-hand, and cost-per-enplanement. The survey data is not publicly released — only participating airports receive access. [Source: https://airportscouncil.org/intelligence/industry-benchmarking-studies/financial-benchmarking-survey/] What is publicly documented: the 2023 ACI World Economics Report placed global airport debt-to-EBITDA at 5.74:1 in 2023, elevated relative to pre-pandemic levels. [Source: https://aci.aero/2025/04/28/airports-face-financial-challenges-despite-air-traffic-rebound-aci-world-economics-report-reveals/] Any new technology capital program competes for balance sheet capacity against that baseline.

**Open Architecture and the ACRIS Semantic Model**  
ACI World's ACRIS Semantic Model creates non-proprietary APIs for aviation data interoperability. The TSA's DICOS standard for imaging data and OPSL software library represent the same principle in security screening equipment. [Source: https://crp.trb.org/acrptransformativetech/applied-technology-in-airports/aviation-data-sharing-now-possible-the-semantic-model-spotlight/] These frameworks exist; they are not universally adopted. The gap between available standards and actual procurement practice is where vendor lock originates.

---

## Financial and Political Case: For and Against

### The Case For

From this chair, the thesis is correct and the timing is urgent. The IIJA ATP program is over. PFC purchasing power has been halved by 25 years of inflation with no cap adjustment. AIP cannot fund technology. That means every IoT device that gets capitalized and bonded in the next program is competing for coverage ratio headroom with terminal expansion, runway rehabilitation, and everything else on the 10-year capital improvement plan.

An airport that goes to the bond market with $500 million in IoT-related technology capital — spread across network infrastructure, edge compute, sensor arrays, and integration platforms — and cannot demonstrate asset longevity and open-standard architecture will face a harder rating-agency conversation than one that can. "Our sensors run on a proprietary protocol and our network is operated by a third party under a 10-year agreement" is not a phrase that improves a coverage ratio discussion.

The airline use-and-lease dimension is equally direct. Residual-framework airports that allow technology architectures to accrete without formal capital authorization are quietly building rate base additions that airlines will discover and contest at the next agreement renegotiation. MII clauses were designed exactly for this situation: to give airlines veto power over capital expenditures that flow into their cost structure without their buy-in. A CEO who presents an airline partners committee with a $75 million IoT remediation program — because the previous architecture required rip-and-replace — is a CEO in a renegotiation posture they did not choose.

The political case is this: technology decisions made quietly, below board approval thresholds, by a CIO who is gone in four years, on a vendor relationship that the airport does not fully control, are the definition of a governance failure waiting to become a political liability. When that program appears on the front page of the local paper — and it will, because these programs eventually require either a large remediation bond or a visible operational failure — the question the board chair asks is not "what went wrong technically?" It is "why didn't we know?"

### The Case Against (Steelman)

The strongest counter-argument is that excessive architecture deliberation is itself a form of risk. An airport that spends three years designing the perfect open-standard IoT framework deploys nothing; its competitors deploy imperfect systems that start generating operational data, improve iteratively, and build institutional knowledge. The internal expertise required to manage a genuinely open, multi-vendor IoT architecture is not available in the airport labor market at the volume needed. Open standards often mean slow standards. ACRIS exists; it is not universally implemented. DICOS exists for screening equipment; it took TSA a decade to get traction.

There is also a version of vendor relationship that is acceptable: a single sophisticated vendor under a performance-based contract with transparent exit costs, open data standards, and financial strength that survives a decade. Some airport executives have made that tradeoff deliberately and correctly. The question is whether the tradeoff was deliberate.

The second counter-argument is that stranded IoT at the operating budget level — sensors that get replaced, network gear that cycles — is not the same as stranded capital. If an airport structures IoT deployments as operating expenditures rather than capital, the coverage ratio exposure is different and the airline cost-allocation treatment is different. Smart financial engineering of the deployment structure matters as much as smart technical engineering of the architecture.

---

## Specific Data Points and Precedents for the Strategist

1. **DEN Great Hall P3 termination settlement: $183.6 million** on a $650 million fixed-price construction contract, terminated 14 months after construction notice to proceed, with only 30% design completion at financial close. The primary failure mechanism — committing to a financial structure before the design was sufficiently defined — maps directly onto IoT programs that commit to vendor relationships before the architecture is defined. [Source: https://dwuconsulting.com/dwu-ai/denver-great-hall-p3-failure]

2. **CVG bond rating decline: A1 to Baa1** following Delta's de-hubbing decision in 2013. The airport did nothing operationally wrong; an external decision by a carrier reshaped the credit profile. The parallel for IoT: a network provider's insolvency (Sigfox, 2022) or acquisition reshapes the operating context of every device on that network. Single-dependency risk in technology architecture is the credit analog of single-carrier concentration. [Source: https://dwuconsulting.com/dwu-ai/airline-concentration-risk-hub-airports]

3. **Toronto Pearson: 7 SCADA systems across 3 platforms, accumulated over 15 years.** No single bad decision; 15 years of locally rational procurement that produced a structurally unmanageable estate. Remediation required 12 months of parallel operation. No published cost, but the labor burden of supporting seven independently maintained platforms for a decade is the hidden financial exposure that never appears in a capital program approval document. [Source: https://inductiveautomation.com/resources/customerproject/toronto-airport-moves-from-seven-scada-systems-to-one]

4. **Sigfox filed for insolvency January 2022; acquired for €25 million; back in court 2025.** Any enterprise IoT architecture built on Sigfox connectivity faced two network ownership transitions in three years. The lesson is not Sigfox specifically — it is that LPWAN connectivity providers are financially fragile, and an architecture that depends on a single connectivity provider's continued operation is an architecture with unpriced counterparty risk. [Source: https://www.rcrwireless.com/20220929/carriers/unsuccessful-iot-deployments-on-nb-iot-sigfox-helium-lorawan-a-furore-about-failure]

5. **IIJA Airport Terminal Program: final application round closed January 15, 2026.** The $1 billion per year federal cost-sharing program for terminal development — the closest thing airports had to federal IoT co-investment for technology embedded in terminal projects — is now over. The next capital program cycle will not have that instrument. Technology capital that would have been partially offset by IIJA grants in 2023 goes fully on the revenue bond program in 2027 and beyond. This is the specific funding-cliff context in which architecture durability decisions made today will be evaluated. [Source: https://www.faa.gov/newsroom/FY26-ATP-NOFO-8DEC2025]

---

## What This CEO Will Tell the Strategist

The operational and technical agents on this panel will give you the architecture answers. I am telling you the authorization answers.

Before any IoT capital is committed: determine whether it is below or above the bond covenant and board approval threshold. Determine how it will be treated in the residual versus compensatory rate-setting calculation, and whether airlines have MII rights over it. Determine what the exit cost is if the vendor relationship fails in year three. Determine whether the data schema is portable to a successor system or proprietary to the current vendor. Ask those questions *before* the pilot becomes the permanent design.

The CEO who solves the IoT stranded-asset problem is not the one who chose the better network protocol. It is the one who built the governance structure that forced those questions to be answered at the right level, at the right time, before the bond documents were signed.

That is the job. Everything else is implementation.

---

*Sources cited inline. Classified information excluded. Findings based on publicly available rating agency methodologies, FAA program documentation, ACI World and ACI-NA published benchmarking, peer airport official statements, ACRP research reports, and documented technology program outcomes.*
