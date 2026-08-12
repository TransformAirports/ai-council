# Technology-Scout Brief — Quiet-by-Design Standards for MWAA Terminals

**Author:** technology-scout
**Run:** `quiet-by-design-standards-for-mwaa-terminals-2`
**Date:** 2026-08-10
**Scope:** Independent technology assessment of the stack a MWAA quiet-by-design standard would actually specify — PA architecture, measurement, visual redundancy, mobile channel, assistive listening, and low-stimulation space — separating what is off-the-shelf in 2026 from what still requires bespoke integration, and vendor claims from audited evidence.

---

## 1. What "quiet-by-design" actually is, in technology terms

The public conversation collapses "quiet airport" into "fewer announcements." That framing is wrong on the technology, and it will misprice the standard. A quiet terminal is a coordinated stack of eight technology layers, most of which are governed by international standards that MWAA can point to by number in its Design Manual. Treated in this order, the stack also matches the order of the design decisions:

1. **Room acoustics.** Reverberation time (RT60), background noise (NR/NC), and finish absorption. Nothing downstream survives a reverberant volume with a hard ceiling — steerable arrays and app notifications do not fix a 2.5-second RT60 in a curbside hall. This is a shell-and-core specification.
2. **PA architecture and zoning.** Distributed loudspeaker layout, beam-steerable column arrays (e.g., Renkus-Heinz ICONYX Gen5), and parametric ultrasonic emitters (Holosonics Audio Spotlight) for tight local coverage. Zone granularity — one gate, one hold room, one restroom — is the design variable that determines whether "local announcement" is achievable at all.
3. **Announcement governance and automation.** Scripted announcement engine (turnaround-triggered), rules about what plays where, tenant PA override protocols, and language rotation. This is mostly configuration, not hardware.
4. **Measurement, commissioning, and post-occupancy verification.** Speech Transmission Index per IEC 60268-16 Ed. 5 (STIPA methodology), EN 54-16 voice-alarm intelligibility, continuous LEQ monitoring, occupancy-loaded testing.
5. **Visual information redundancy.** FIDS density and sight-line design, dynamic wayfinding, gate podium displays, changeable-message screens with pictograms, and closed-captioning of any audio content.
6. **Personal / mobile channel.** Airline app push notifications, airport-app geofenced alerts, Bluetooth Low Energy (BLE) beacon fabric, and SMS fallback for passengers not on the airline app.
7. **Assistive listening and accessibility.** Hearing induction loops per IEC 60118-4 at gate counters, ticket counters, and information desks; T-coil compatibility; visual paging systems; multilingual voice synthesis; and pictogram wayfinding.
8. **Low-stimulation and sensory spaces.** Sensory rooms modeled on Pittsburgh's Presley's Place, ATL's Multi-Sensory Room, and quiet zones with acoustic separation.

A useful test for any MWAA standard: does each requirement map to a numbered international standard or a measurable performance threshold, or is it a preference dressed up as a specification? Requirements that fail that test become change orders in construction and lawsuits in tenant negotiations.

## 2. Key findings

- **The domestic baseline document already exists and MWAA does not need to invent it.** ACRP Research Report 175 (2017) is the U.S. reference for airport PA intelligibility. It converges on a signal-to-noise ratio of 10–15 dB(A) and a minimum Speech Transmission Index (STI) of 0.45 for pier-style departure lounges [Source: https://nap.nationalacademies.org/read/24839/chapter/5]. Any MWAA standard that does not cite ACRP 175, IEC 60268-16, and EN 54-16 by number is skipping the easiest evidentiary layer.
- **The most-cited "quiet airport" numbers are self-reported and undocumented.** SFO's frequently repeated "90 minutes of daily announcements removed" and "onsite noise reduced by more than 40%" figures come from SFO's own communication and trade press repetition [Source: https://viewfromthewing.com/san-francisco-airport-removed-90-minutes-of-daily-noise-travelers-say-it-changed-everything/]. I did not find a published measurement methodology, an independent acoustical study, or a peer-reviewed evaluation. Council output should quote the figure but attribute it and flag the vintage.
- **The "silent airport" pioneers optimized for a specific traveler profile that IAD and DCA do not fully share.** London City's silent terminal policy (2008) relies explicitly on smartphone penetration and a homogeneous, largely business-traveler population [Source: https://www.londoncityairport.com/silent-airport-policy]. Helsinki's Silent Airport program (Finavia, 2015) directs passengers to the departure screens, airport website, or mobile app in lieu of general announcements [Source: https://morepremium.com/helsinki-vantaa-to-be-made-a-quiet-airport/]. Copenhagen removes 'Go to gate' and 'Boarding' announcements entirely and pushes passengers to FIDS and the CPH app [Source: https://www.cph.dk/en/practical/gate-information-and-boarding]. IAD's 36%+ international share and heavy connection traffic (airport-context.md §6) means MWAA cannot assume the London City or Helsinki demographic profile.
- **Steerable and parametric PA is mature, competitively supplied, and installed in airports today.** Renkus-Heinz ICONYX steerable column arrays are deployed at LAX and thousands of other venues and support up to eight independently aimable beams per column with 170 ms of onboard DSP delay [Source: https://renkus-heinz.com/products/iconyx-gen5/]. Holosonics Audio Spotlight parametric ultrasonic emitters produce sound columns "10x more isolated than any loudspeaker" and have shipped thousands of units since 2000 [Source: https://www.holosonics.com/]. Neither is exotic; both belong in the MWAA specification catalog.
- **Voice-alarm intelligibility is not optional under any credible fire-life-safety review.** IEC 60268-16 is the STI measurement standard, and STIPA per that standard is required to demonstrate EN 54-16 compliance for voice-alarm systems — with a common threshold of STI ≥ 0.50 for general paging and higher for emergency voice alarm [Source: https://bedrock-elite.com/applications/alarm-paga-testing]. Any "quiet-by-design" spec that reduces PA coverage must preserve the emergency-voice-alarm STI at every point in the terminal or it will fail commissioning.
- **The mobile-notification substitute for PA is real, cheap, and unevenly delivered.** SFO installed roughly 500 BLE beacons for indoor navigation and notifications; Gatwick installed roughly 2,000 across two terminals as part of a £2.5B transformation program, using battery-powered devices to compress install time to three weeks [Source: https://appleinsider.com/articles/17/05/25/uks-gatwick-airport-installs-2000-bluetooth-beacons-for-ar-based-indoor-navigation]. The technology risk is not hardware — it is that airlines control the app that receives the notification. MWAA can specify the beacon fabric but cannot force United, American, and every other carrier to develop consistent geofenced boarding push behavior on top of it.
- **Assistive-listening standards are settled; enforcement is not.** IEC 60118-4:2014 specifies field strength, signal-to-noise, and frequency response requirements for audio-frequency induction loops feeding hearing-aid telecoils [Source: https://webstore.iec.ch/en/publication/798]. The ADA "encourages" hearing loops at counters and information desks. What is missing from most airport design manuals is a specific location list — gate podiums, ticket counters, information desks, security exit counters — and a testing regime.
- **Sensory-friendly space is off-the-shelf as a concept but bespoke as a build.** Pittsburgh's Presley's Place (2019) is a 1,500 sq ft dedicated suite with private relaxation pods, a tactile water wall, and a simulated cabin including jetway and overhead bins [Source: https://nextpittsburgh.com/latest-news/pittsburghs-airport-unveils-presleys-place-the-worlds-most-advanced-sensory-suite-for-special-needs-travelers/]. ATL's Multi-Sensory Room in Concourse F offers a padded crash pit, bubble tubes, tactile panels, and soft lighting [Source: https://outcoast.com/sensory-friendly-u-s-airports-that-reduce-overstimulation-for-the-neurodivergent-traveler/]. Cost data is not publicly disclosed at either airport; treat published figures skeptically.

## 3. Off-the-shelf in 2026 vs. still bespoke

**Off-the-shelf, commodity-priced, multiple vendors:**

- Beam-steerable column-array loudspeakers (Renkus-Heinz ICONYX, Community Steerable, Fulcrum Acoustic).
- Parametric ultrasonic directional emitters (Holosonics, others).
- STIPA measurement instruments and voice-alarm certification services (Bedrock Elite, NTi, Bruel & Kjaer).
- Hearing induction loop amplifiers, mats, and counter loops meeting IEC 60118-4 (Williams AV, Ampetronic, Contacta).
- Airport FIDS platforms and dynamic-signage CMS (SITA, Amadeus, Rockwell Collins/Collins Aerospace, Ultra).
- BLE beacon fabric and indoor-positioning SDKs (Mappedin, Situm, Navigine).
- Automated announcement engines with multi-language TTS (Innovative Business Software, Copenhagen Optimization, Ultra).
- Modular sensory-room kits (bubble tubes, tactile walls, projection systems) from special-education suppliers.

**Still requires bespoke design and integration:**

- Gate-boundary PA zoning that matches specific airline hold-room geometries and does not spill into neighboring gates. This is layout-and-acoustics work, not a product purchase.
- Tenant-versus-tenant audio-level enforcement across airline clubs, concessions, and gate podiums. There is no product for this; it is a lease-and-tenant-agreement problem with technical guardrails.
- Cross-airline push-notification consistency for boarding calls when the passenger holds an airline app that MWAA does not control.
- Commissioning protocols that verify STI at design occupancy loads, not empty terminals. STI degrades sharply as absorption and background noise change with passenger density; empty-terminal certification is a common failure pattern.
- Integration of PA suppression rules with irregular-operations messaging, so that a quiet-zone doctrine does not silence a diversion or an evacuation announcement.
- Retrofit into architecturally protected volumes — at IAD, the Saarinen Main Terminal preservation (airport-context.md §5) constrains what can be added to the ceiling plane. This is bespoke by definition.

## 4. Honest assessment of maturity

The technology is not the constraint. Every layer of the stack above has multiple commercial vendors, at least one international standard, and installed reference sites. The failure modes at peer airports are governance failures, commissioning failures, and demographic-mismatch failures — not hardware failures.

**What is real:**

- STI measurement, EN 54-16 voice-alarm compliance, and IEC 60118-4 hearing-loop testing are mature and enforceable.
- Beam-steering and parametric PA reliably localize sound in the field; both technologies have been shipping for two decades.
- Sensory rooms have three-to-seven years of North American operating experience and are now a recognized ACRP-adjacent design pattern.
- FIDS density and multi-lingual dynamic wayfinding are commodity capabilities from the major airport IT vendors.

**What is hype or unverified:**

- The specific "40% noise reduction / 90 minutes removed" SFO figures. Real directional effect, undocumented measurement.
- "Silent airport" branding at peer airports where the actual policy is "fewer general announcements, gate-area announcements retained, emergency announcements retained." London City, Helsinki, and Copenhagen all preserve gate-area and emergency PA — the branding oversells the change.
- Vendor case studies claiming intelligibility improvements without STIPA data at occupancy load.
- Sensory-room "cost" claims in trade press. There is no public capex or opex data set to benchmark against.

**What MWAA specifically should not adopt without adjustment:**

The London City / Helsinki model of eliminating general and gate-area announcements assumes near-universal smartphone possession, high English literacy, and low-connection-anxiety passengers. IAD's international-connection population and DCA's post-collision irregular-operations exposure both cut against that assumption. The right answer is not to import the branding; it is to import the measurement discipline (STI, RT60, LEQ, ambient noise) and let the operational policy vary by terminal.

## 5. Direct quotes and data points for the strategist

- "Codes and application standards typically recommend a minimum STI of 0.45 or 0.50. STI values range from 0 to 1, with numbers close to 1 achieving high levels of intelligibility." — ACRP Research Report 175 summary, National Academies Press [Source: https://nap.nationalacademies.org/read/24839/chapter/5]
- "A STIPA value of 0.50 or above ('Fair') is typically required for voice alarm systems to comply with EN 54-16, BS 5839-8, and ISO 7240-19." — STIPA measurement guide, Bedrock Elite, citing IEC 60268-16 [Source: https://bedrock-elite.com/applications/alarm-paga-testing]
- "No flight or gate announcements will be made, instead all information will be displayed on screens that are located throughout the lounge and restaurants. In the case of emergency are announcements made." — London City Airport, Silent Airport Policy page [Source: https://www.londoncityairport.com/silent-airport-policy]
- "The scheme has already helped remove over 90 minutes' worth of unnecessary daily noise throughout the airport and reduced overall onsite noise by more than 40%." — Reporting on SFO Quiet Airport program (self-reported figures) [Source: https://viewfromthewing.com/san-francisco-airport-removed-90-minutes-of-daily-noise-travelers-say-it-changed-everything/]
- "Up to eight steerable beams can be individually shaped and aimed from a single column using software-controlled DSP." — Renkus-Heinz ICONYX Gen5 product page [Source: https://renkus-heinz.com/products/iconyx-gen5/]
- Pittsburgh's Presley's Place is a "1,500-square-foot sensory suite" including "private relaxation pods, a bubbling water wall, tactile panels, and a simulated airplane interior… complete with a cabin, seats, overhead bins and a jetway." — NEXTpittsburgh reporting on the July 2019 opening [Source: https://nextpittsburgh.com/latest-news/pittsburghs-airport-unveils-presleys-place-the-worlds-most-advanced-sensory-suite-for-special-needs-travelers/]

## 6. What this brief does not establish

- Actual capital or annual O&M cost for any of the technology layers at IAD or DCA scale. No primary vendor pricing was captured; strategy work should assume order-of-magnitude ranges only.
- Whether the current MWAA Design Manual (2020, seven volumes) already binds STI, RT60, or LEQ thresholds. The airport-context packet flags this as unverified (§10) and it should be checked before Stage 2.
- Independent, audited passenger-experience or accessibility outcomes at the "silent airport" peer set. Trade press and airport press releases repeat each other; the underlying measurement was not located.
- Any MWAA-specific tenant-agreement language on airline club, concession, or gate-podium PA. This is a lease question that a technology brief cannot answer.
- Airline app boarding-notification behavior consistency across United (dominant at IAD) and American (dominant at DCA). This is essential to any "push instead of paging" recommendation and is not documented.

The recommended posture for Stage 2 is: adopt measurement discipline as a mandatory tier (STI, RT60, LEQ, hearing-loop field strength), adopt the design-catalog technologies (steerable/parametric PA, hearing loops, FIDS density, sensory rooms) as recommended tier with airport-specific tuning, and leave announcement-policy prescriptions as context-dependent — because that is where the peer evidence is thinnest and the IAD/DCA demographic split is widest.
