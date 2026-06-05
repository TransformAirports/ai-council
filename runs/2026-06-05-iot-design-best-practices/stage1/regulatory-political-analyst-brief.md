# Regulatory and Political Analyst Brief
## IoT Design Best Practices at U.S. Airports
**Stage 1 Research | Transform Airports AI Council**
*Prepared: June 2026 | Classification: Council Internal*

---

## Prefatory Note

The thesis under examination — that airport IoT deployments strand not because sensors fail but because surrounding architecture decisions were made for pilots and never remade for scale — lands squarely in the middle of an active regulatory environment that most IoT vendors and airport technology teams prefer not to dwell on. They should. The regulatory stack governing airport IoT in 2026 is more consequential than it was five years ago, and it is getting more consequential. What follows is an honest accounting of the forces that constrain, reshape, and occasionally kill IoT deployments through means that have nothing to do with sensor performance.

---

## Key Findings

1. **TSA's March 2023 cybersecurity directive amendment (SD 1542 series) imposed IT/OT network segmentation requirements on all TSA-regulated airports, retroactively.** IoT systems deployed before 2023 that share infrastructure with corporate IT networks are now out of compliance by design. This is regulation — TSA imposed it, and airports cannot negotiate their way around it.

2. **The FAA Civil Aviation Cybersecurity Aviation Rulemaking Committee (ARC), chartered in May 2025 under §395 of P.L. 118-63, is developing binding standards for airport ground support information systems.** The rulemaking pipeline is 2-4 years. Any IoT architecture designed without anticipating FAA-mandated cybersecurity baseline requirements is being designed into a compliance retrofit problem.

3. **CBRS spectrum — on which 75% of U.S. private 5G networks depend — faces non-trivial auction risk under the Trump administration's 800 MHz spectrum pipeline mandate.** The Wireless Internet Service Providers Association has publicly warned that the "Big Beautiful Bill" spectrum provisions "potentially put CBRS and 6 GHz spectrum on the auction block." An airport that bets its entire IoT network architecture on private 5G via CBRS is staking a 15-year asset on a spectrum license that is a political decision, not a legal permanence.

4. **The C-band/5G dispute (January 2022 through September 2023) is the canonical example of federal spectrum governance overriding planned wireless infrastructure.** The FAA unilaterally blocked C-band 5G deployments near airports based on radio altimeter interference concerns, with no prior notice to airports or carriers. It was resolved only after the airlines spent a year and a half retrofitting aircraft altimeters. The lesson: spectrum politics can interrupt operational wireless infrastructure plans at any time, and the airport has no standing to object.

5. **The PFC cap frozen at $4.50 since 2001 structurally tilts airport capital allocation toward AIP-eligible physical infrastructure and away from IoT, software, and operational intelligence.** AIP's primary eligibility categories — runways, taxiways, lighting, navigational aids — do not include general-purpose sensor networks, operational analytics platforms, or IoT middleware. The 2024 FAA Reauthorization (P.L. 118-63) extended the AIP authorization through FY2028 at $3.35–$3.73B annually but again did not raise the PFC cap. This is politics, not regulation. Congress could change it tomorrow. They have chosen not to for 23 consecutive years.

6. **The IIJA Airport Terminal Program ($5B over FY2022–FY2026) was the one mechanism that could fund terminal technology infrastructure, including network backbone for IoT.** The program expires at the end of FY2026. The funding cliff is estimated at $2.89B/year relative to combined AIP-plus-AIG levels. Airports that deferred IoT network infrastructure investment to FY2027 or beyond face a dramatically tighter capital environment.

7. **The SEA ransomware attack (August 2024) validated precisely the failure mode TSA was trying to prevent:** shared IT/OT infrastructure gave the Rhysida ransomware group lateral access from corporate systems to baggage handling, passenger displays, and check-in kiosks. The airport had to resort to dry-erase boards for flight information. Recovery took weeks, not hours. 90,000 individuals had personal data compromised.

8. **Rating agencies reward capital programs with visible, durable revenue streams and view operational technology investments with skepticism** unless they reduce OpEx in ways that can be modeled. IoT programs that cannot demonstrate bond-ratable cash flow benefits do not strengthen credit; they dilute it. This is the silent veto on airport operational intelligence programs that never makes it to the board presentation.

---

## Evidence

### The Federal Regulatory Stack

**TSA: The Retroactive Compliance Problem**

On March 7, 2023, TSA issued an emergency amendment to the security programs of TSA-regulated airport and aircraft operators, extending the cybersecurity directive framework originally applied to pipelines and rail systems to aviation. [Source: https://www.tsa.gov/news/press/releases/2023/03/07/tsa-issues-new-cybersecurity-requirements-for-airport-and-aircraft]

The directive requires airports to develop a TSA-approved implementation plan and assessment plan covering four core technical requirements: (1) network segmentation policies ensuring OT systems — including baggage handling, airfield lighting, ground vehicle communications, and all IoT-connected building systems — can operate independently if IT systems are compromised; (2) access control measures for critical cyber systems; (3) continuous monitoring and detection for all Tier 1/2 critical cyber systems; and (4) a 90-day patch management schedule for those systems.

The OT/IoT network segmentation requirement is the binding constraint. Any airport IoT deployment that was designed as a flat network — where sensors, building management systems, and operational control infrastructure share a common Layer 2 segment with corporate IT — fails the TSA standard. The directive does not grandfather existing systems. Airports that deployed IoT at scale before 2023 are currently executing forced-remediation programs to achieve segmentation they didn't build in.

The practical cost of retrofitting segmentation into an already-deployed IoT estate is substantially higher than building it in at design. The vendors who sold flat-network IoT platforms in 2018–2021 are no longer the vendors helping airports remediate. This is the first mechanism by which regulatory surprise kills IoT programs.

**FAA: The Forward Rulemaking Pipeline**

The FAA Reauthorization Act of 2024 (P.L. 118-63, signed May 16, 2024) directed the FAA to convene a Civil Aviation Cybersecurity Aviation Rulemaking Committee (ARC) by May 15, 2025 to develop findings and recommendations on cybersecurity standards specifically covering "airports, air traffic control mission systems, and aircraft ground support information systems." [Source: https://www.congress.gov/crs-product/IF12791]

The FAA chartered the ARC in May 2025. ARC recommendations typically take 2–4 years to reach final rulemaking. That puts binding FAA cybersecurity standards for airport IoT systems on a 2027–2029 timeline — well within the deployment horizon of systems being architected today. An airport that designs IoT infrastructure now without considering what the ARC will recommend is designing into a future retrofit. The committee's membership includes airports, aircraft manufacturers, and OEMs of ground-based aviation infrastructure — meaning the standards will have teeth that airport IT teams cannot dismiss as aircraft-centric.

Separately, on August 21, 2024, FAA published an NPRM codifying cybersecurity practices for aircraft systems (Federal Register 2024-17916). While this NPRM focuses on aircraft rather than ground systems, it signals the regulatory direction and will constrain how airports integrate airside IoT data with aircraft systems. [Source: https://www.federalregister.gov/documents/2024/08/21/2024-17916/equipment-systems-and-network-information-security-protection]

**FCC and CISA: The Spectrum and Standards Environment**

The FCC governs the spectrum on which airport IoT communications run. Three relevant bands are active:

- **CBRS (3.5 GHz, 3550–3700 MHz):** 150 MHz of shared federal-commercial spectrum; the foundational band for private 5G at airports. [Source: https://en.wikipedia.org/wiki/Citizens_Broadband_Radio_Service]
- **6 GHz unlicensed band (5.925–7.125 GHz):** 1200 MHz of spectrum opened by FCC in 2020 for Wi-Fi 6E and other unlicensed uses.
- **C-band (3.7–3.98 GHz):** Auctioned to Verizon and AT&T; previously subject to airport-area restrictions through September 2023.

The CBRS spectrum governance situation is the one to watch. The Trump administration's spectrum policy, documented in the Working Families Tax Cut Act, mandates a pipeline delivering 800 MHz of spectrum for auction by 2034. The Wireless Internet Service Providers Association warned in 2025 that the legislation "potentially puts CBRS and 6 GHz spectrum on the auction block at the FCC." [Source: https://www.theregister.com/2025/07/08/trump_budget_bill_spectrum_auctions/] If CBRS power limits are reduced or spectrum is partially reallocated, private 5G deployments built on CBRS coverage become unreliable — affecting range, throughput, and the entire IoT sensor coverage map that was engineered to those power levels.

CISA has separately issued a series of OT security guidance documents that create de facto compliance expectations: "Secure Connectivity Principles for Operational Technology" (2025), "Foundations for OT Cybersecurity: Asset Inventory Guidance" (August 2025), and joint guidance with the UK NCSC urging alignment with IEC 62443 and ISO/IEC 27001. [Source: https://www.cisa.gov/resources-tools/resources/secure-connectivity-principles-operational-technology-ot] While CISA guidance is not regulation, TSA references it in enforcement conversations with airports. An IoT architecture that ignores IEC 62443 today is an architecture that will be asked to justify itself to TSA examiners tomorrow.

**NIST: The IoT Device Baseline**

NIST SP 800-213, *IoT Device Cybersecurity Guidance for the Federal Government* (finalized November 2021), and its companion catalog SP 800-213A establish minimum IoT device capabilities expected in federally-connected environments: device identification, device configuration, data protection, logical access control, software updates, and cybersecurity event logging. [Source: https://csrc.nist.gov/pubs/sp/800/213/final] Airports are not federal agencies, but their federal partners — TSA, CBP, FAA — are. Any IoT device that connects to or exchanges data with federal systems must meet or be mappable to SP 800-213 requirements. Airports building shared data layers with federal agencies face this requirement without most recognizing it.

### Congressional Dynamics

**The PFC Freeze as Structural Bias**

The PFC cap of $4.50 per enplanement has been frozen since the Wendell H. Ford Aviation Investment and Reform Act for the 21st Century took effect in 2001. Adjusted for inflation, $4.50 in 2001 is approximately $7.85 in 2026 dollars — meaning airports have lost nearly 43% of their per-passenger capital raising capacity in real terms. [Source: https://www.gao.gov/products/gao-15-107]

The 2024 FAA Reauthorization (P.L. 118-63) authorized AIP entitlement funding at $3.35B for FY2024 rising to $3.725B for FY2028 but retained the $4.50 PFC cap despite sustained airport industry advocacy through ACI-NA. [Source: https://www.everycrsreport.com/reports/IF12791.html] ACI-NA has since sought meetings with DOT Secretary Duffy on PFC cap relief, and PFC cap increase remains a top legislative priority for the 119th Congress. The odds of passage in this Congress, given airline opposition and the current legislative agenda, are low.

The consequence for IoT is indirect but binding: AIP's eligible project categories — runways, taxiways, aprons, lighting, navigational aids, noise control, safety and security — do not cover general-purpose operational IoT networks or analytics platforms. Airports that cannot raise additional capital through higher PFCs must fund IoT from revenue bonds, meaning they must demonstrate bondable revenue impact — a standard that operational software rarely meets.

**The IIJA Cliff and What Comes After**

The Infrastructure Investment and Jobs Act (IIJA, P.L. 117-58, 2021) provided $25B for airports over five years: $14.5B through the Airport Infrastructure Grant (AIG) program and $5B through the Airport Terminal Program (ATP). The ATP's competitive grant structure was broad enough to include terminal network infrastructure and technology-adjacent capital. The IIJA's airport programs expire at the end of FY2026. ACI-NA projects the annual federal airport grant baseline reverts to approximately $3.5–4.0B/year, a reduction of roughly $2.89B annually. [Source: https://airportscouncil.org/intelligence/airport-infrastructure-needs-study/]

The 2025 ACI-NA Infrastructure Needs Study projects airports will require $173.9B over 2025–2029, against combined annual funding (AIP + IIJA + PFC) of approximately $12B per year — versus stated annual needs topping $30B. [Source: https://airportscouncil.org/wp-content/uploads/2025/03/2025-Infrastructure-Needs-Study.pdf] In a capital-constrained environment competing $30B in needs against $12B in funding, operational IoT infrastructure that lacks a visible ribbon-cutting narrative reliably loses.

---

## Case Studies

### Case Study 1: SEA Ransomware — The IT/OT Commingling Failure (August 2024)

On August 24, 2024, the Rhysida ransomware group accessed Port of Seattle systems and propagated through shared infrastructure to reach Seattle-Tacoma International Airport operational systems: Wi-Fi networks, baggage handling systems, passenger flight information displays, and check-in kiosks. Employees had to use dry-erase boards for flight information while the airport recovered system by system over multiple weeks. 90,000 individuals had personal data compromised; a $6 million ransom demand was issued and declined. [Source: https://www.portseattle.org/news/port-seattle-providing-notice-individuals-affected-fall-2024-cyberattack]

The architectural failure was precisely what TSA's 2023 directive exists to prevent: operational technology and IoT-adjacent passenger service systems shared network infrastructure with corporate IT systems in a configuration that allowed lateral movement. The lesson is not that SEA was negligent — the same flat-network architecture governed hundreds of airports in 2024. The lesson is that a regulatory requirement (TSA IT/OT segmentation) was issued in 2023 for a problem that reached catastrophic expression in 2024. Any airport whose IoT deployment plan does not include architectural segmentation as a first-order design constraint is operating in violation of current TSA direction and is one supply-chain compromise away from a SEA-scale incident.

### Case Study 2: The C-Band/5G Dispute — When Spectrum Governance Interrupts Infrastructure Plans (2022–2023)

In December 2020, the FCC auctioned C-band spectrum (3.7–3.98 GHz) to Verizon and AT&T for 5G deployment. Both carriers planned commercial service by January 2022. The FAA, which had not participated in the FCC auction proceeding in any substantive way, issued an objection in late 2021 asserting that C-band 5G would interfere with aircraft radio altimeters, creating safety risks during instrument approaches at major airports. [Source: https://www.faa.gov/5g]

The ensuing dispute involved the White House, the DOT, the FCC, the carriers, and the airlines. The FAA imposed airport-area exclusion zones for C-band transmitters. AT&T and Verizon repeatedly delayed deployment near airports. The resolution — completed September 2023 after aircraft altimeters were retrofitted across the entire airline fleet — required 18 months of disruption and hundreds of millions in carrier and airline costs. [Source: https://www.aviationtoday.com/2022/03/24/the-latest-5g-c-band-interference-on-radio-altimeters-research-testing-and-technology-updates/]

The architectural lesson for IoT planners is explicit: **the FCC can auction spectrum and the FAA can block its use near airports, and neither agency coordinates its actions to protect airport capital plans.** Any IoT architecture that depends on a single wireless technology is exposed to this kind of inter-agency spectrum conflict. Architecture that maintains optionality across LoRaWAN, Wi-Fi 6E, CBRS, and licensed LTE carries higher initial design cost and organizational complexity — but it is the only architecture that survives a spectrum governance dispute.

### Case Study 3: The PFC Cap as a Silent Veto on Operational Technology Investment

In every FAA Reauthorization cycle since 2001, airports and ACI-NA have advocated for raising the PFC cap. Airlines — principally through A4A and IATA — have opposed every increase. Airlines succeed because their congressional leverage (employment in hub cities, frequent flyer constituent bases) exceeds airports' leverage, and because the transaction cost of a PFC increase falls entirely on the passenger. The dynamic is described bluntly by the GAO in GAO-15-107: "Airlines generally oppose increasing the PFC cap and have argued that higher PFCs would adversely affect air travel demand." [Source: https://www.gao.gov/products/gao-15-107]

The PFC cap's effect on IoT investment is indirect. AIP, which is the dominant federal funding mechanism, requires sponsor cost-sharing (typically 10-25% depending on airport size) and limits eligible projects to categories that do not include operational software or general-purpose sensor networks. Airports raising capital for IoT must use PFC-backed revenue bonds, which require demonstrable bond-ratable returns, or must charge costs against landing fees and terminal rents — which triggers airline use agreement scrutiny. The structural result: IoT programs that live in the operational budget are perennially at risk of deferral, while IoT-adjacent physical infrastructure that can be capitalized under AIP categories (conduit, structured wiring in terminals, equipment rooms) gets funded. The divide between fundable and unfundable airport IoT components is drawn by AIP eligibility, not operational logic.

---

## Direct Quotes and Data Points for Strategist Use

**1. On the TSA compliance problem:**
> "Airports are required to implement policies and controls that separate operational technology (OT) systems — airfield lighting, ground vehicle communications, and baggage handling — from corporate IT networks and public-facing systems, maintaining safe OT operation even if the IT network is compromised." — TSA March 2023 cybersecurity directive requirements summary [Source: https://www.dragos.com/blog/emergency-tsa-cybersecurity-directive-for-airports-aircraft-operators-how-to-prepare/]

Any airport whose IoT deployment comingles OT with IT is out of compliance with this requirement today.

**2. On the CBRS spectrum risk:**
> "More than 85% of private 5G networks deployed in U.S. factories by 2032 will rely on CBRS spectrum, and 75% of private 5G networks in use today rely on CBRS." — OnGo Alliance, 2023 [Source: https://ongoalliance.org/cbrs-takes-flight-2023s-soaring-developments-in-3-5-ghz-spectrum-from-potential-to-practice-cbrs-proves-its-promise-in-2023/]

The concentration of private 5G on a single shared spectrum band creates a systemic risk: one federal spectrum policy decision can affect the wireless architecture of every airport that deployed private 5G in the same configuration.

**3. On the PFC cap's 23-year freeze:**
> "In the FAA Reauthorization Act of 2024 (P.L. 118-63), Congress did not raise the PFC cap — the final legislation retained $4.50, though it included streamlining provisions for the PFC application process." — Congressional Research Service summary of FAA Reauth 2024 [Source: https://www.everycrsreport.com/reports/IF12791.html]

Adjusted for inflation, the $4.50 cap set in 2001 is worth approximately $7.85 in 2026 purchasing power. Airports have lost nearly 43% of their per-passenger capital-raising capacity while construction costs have increased 38% since 2014 alone.

**4. On the scale of the capital-needs gap:**
> "Combined funding for airport projects from the infrastructure legislation, the AIP program, and PFCs will come to around $12 billion per year in 2025 and 2026, but annual infrastructure needs at U.S. airports top $30 billion." — ACI-NA 2025 Airport Infrastructure Needs Study [Source: https://airportscouncil.org/intelligence/airport-infrastructure-needs-study/]

In a capital environment where $30B in needs competes against $12B in supply, operational IoT programs without AIP eligibility or visible bond-ratable returns finish last.

**5. On the FAA's forward rulemaking trajectory:**
> "Section 395 [of P.L. 118-63] directs the FAA to convene the Civil Aviation Cybersecurity ARC by May 15, 2025, to develop findings and recommendations on cybersecurity standards for civil aircraft, aircraft ground support information systems, airports, air traffic control mission systems." — CRS IF12791, The 2024 FAA Reauthorization [Source: https://www.congress.gov/crs-product/IF12791]

The ARC's recommendations will become rulemaking. Airports designing IoT architectures today are designing for a regulatory environment they cannot yet read the final text of — but can predict the direction.

---

## The Analyst's Argument

The regulatory and political environment does not make airport IoT impossible. It makes the specific design decisions that create stranded deployments harder to avoid. Three forces reinforce each other:

**The compliance retrofit trap:** TSA's 2023 directive imposed network segmentation requirements on deployed IoT systems that weren't designed for segmentation. The upcoming FAA cybersecurity rulemaking will impose a second compliance pass. Airports with flat-network IoT architectures will face two rounds of forced architectural remediation within a 5-year window — not because their sensors failed, but because the regulatory environment changed around infrastructure that was designed for a simpler compliance world.

**The spectrum concentration risk:** The IoT industry has converged on CBRS private 5G as the preferred enterprise network. Airports that deployed single-technology IoT networks on the assumption that CBRS spectrum would be stable for 15 years are exposed to a political decision they have no standing to influence. Federal spectrum policy is made by the FCC, contested by carriers, occasionally blocked by the FAA, and subject to budget reconciliation riders. Airports sit outside that process.

**The capital structure bias:** The PFC cap, AIP eligibility rules, and bond market dynamics create a capital environment that funds visible physical infrastructure and resists operational software investment. This is not neutral — it is a structural force that consistently pushes airport organizations toward the categories of IoT investment (new terminal conduit, equipment rooms, structured wiring) that are AIP-eligible, and away from the categories (middleware, data architecture, open schema, vendor-neutral integration layers) that make deployments durable. The result is airports that have spent substantial capital on sensor hardware and connectivity infrastructure while systematically underfunding the data and integration layers that determine whether that investment survives three vendor changes.

The strategist should understand this as a systems-level problem: the regulatory and political environment does not just constrain IoT investment, it shapes which IoT investment is institutionally possible. Any architecture recommendation that requires sustained capital allocation to operational software, proprietary-schema migration, or integration-layer maintenance is asking airports to fight uphill against their own capital structure. The durable architecture is not just the one that survives technology change — it is the one that survives the funding cycles, regulatory passes, and spectrum governance disputes that will arrive on a timeline the vendor won't put in their sales deck.

---

*Brief prepared by Regulatory and Political Analyst for Transform Airports AI Council Stage 1 research. Independent of other Stage 1 agents' outputs. All regulatory citations are primary-source where possible.*
