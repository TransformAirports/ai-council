# Writing effective run prompts

How to frame a Title, Thesis, Scope, and Avoid so the Council produces its best work.

The Council amplifies whatever you give it. A sharp thesis gives the research
swarm something worth deciding; a vague one produces a polite industry
summary. This guide is how to get the framing right.

**The one rule that governs everything: topics produce summaries. Theses produce arguments.** "An overview of airport IoT trends" is a topic. "Most airport IoT deployments are stranded within five years — not because the sensors fail, but because the surrounding decisions were made for a pilot and never re-made for scale" is a thesis. The first gives the Council nothing to test. The second gives the Contrarian something to attack, the Fact-checker something to verify, and the Strategist something to defend or concede.

---

## What each field actually does

These aren't just form fields. Each one is wired into the pipeline differently, and knowing where your words land tells you how to write them.

| Field | Where it goes |
|---|---|
| **Title** | Becomes the slug, the archive folder name, the report's cover page, and the library card. |
| **Thesis** | Read by every research agent before they search, by the Strategist before every draft, by the Red Team before every critique. It is the single most-read sentence in the run. |
| **Scope** | Each line becomes a success criterion the run is judged against, and research agents treat the list as their assignment sheet. What you don't list, they may not cover. |
| **Avoid** | Each line becomes a "what this is NOT" constraint. The Red Team attacks drafts that drift toward these; the Editor cuts in their direction. |
| **Decision frame** | Grounds the research in an owner, approval path, time horizon, and measurable outcome. The Airport Executive Reviewer uses it to reject recommendations that cannot be assigned or approved. |
| **Presentation mode** | Chooses a board decision deck, executive briefing, or technical read-ahead. The Art Director adjusts narrative density and visual treatment accordingly. |

---

## Title

One short headline. It names the folder, the file, and the cover — so write it for the person finding this report in the library eight months from now.

- **Name the subject and the angle**, not just the subject. "Baggage Handling" says what it's about; "BHS Governance and the IAD Capital Program" says what it argues and where it lands.
- **Keep it under ~8 words.** The slug auto-derives from it; a title like "Evaluate Arguments for Stand Alone Emergency Managements" produces a filename you'll be typing into terminals for years.
- Don't put the whole thesis in the title. That's what the thesis is for.

---

## Thesis

One to three sentences. This is where the run is won or lost.

### The anatomy of a strong thesis

The best theses this Council has run share four parts:

1. **A falsifiable claim.** Someone informed could disagree. If nobody could reasonably argue the other side, the Contrarian has no job and the report reads as a press release.
2. **A mechanism.** Not just *what* is true but *why*. The "not because X, but because Y" construction is the workhorse: *"…stranded within 5 years — not because the sensors fail, but because the surrounding decisions were made for a pilot and never re-made for scale."* The mechanism gives every agent a causal chain to test rather than a mood to affirm.
3. **Named anchors.** Real airports, real years, real systems. *"DEN '95, HKG '98, T5 '08, BER '20"* in the BHS thesis told the Aviation Historian exactly which case studies form the spine — and dared the Contrarian to find a counterexample.
4. **A reframe of the question.** The strongest closers tell the Council what the *actual* question is: *"The future-proofing question is not 'what's the best sensor' but 'what's the architecture that survives three vendor changes, two network upgrades, and one CIO turnover.'"* This is what separates a report readers finish from one they skim.

### Before and after

Weak (a topic):
> Airport IoT is an important and growing area. This report will examine best practices for IoT deployments.

Strong (a thesis — from a real run):
> Most airport IoT deployments are stranded within 5 years — not because the sensors fail, but because the surrounding decisions (network, data ownership, integration path, vendor lock) were made for a pilot and never re-made for scale. The future-proofing question is not "what's the best sensor" but "what's the architecture that survives three vendor changes, two network upgrades, and one CIO turnover."

Notice what the strong version does: a specific claim (stranded within 5 years), a mechanism (pilot-scale decisions), named failure vectors (network, data ownership, integration, vendor lock), and a reframe. Every research agent can start work immediately, from a different angle, without asking what you meant.

### Tests to apply before you launch

- **The dinner-party test.** Could someone at the table say "I don't think that's true"? If not, it's not a thesis.
- **The verb test.** Does it contain a claim verb — *fails, outperforms, should be, will strand, is the wrong* — or only survey verbs — *examines, explores, considers*? Survey verbs mean you've written a topic.
- **The number test.** Is there at least one specific quantity or date an agent could check? "Within 5 years." "Since 1995." "The last 25 years." Specifics are handles for the Fact-checker; vagueness is unfalsifiable by construction.
- **The two-sided test.** Can you state the strongest opposing position in one sentence? If you can't, the Contrarian can't either, and the report will lack the counter-case that makes it credible.

### If the thesis is about your own operation

Say so, and be concrete. The Saarinen and BHS runs both named MWAA, IAD, and the live capital program — which is why their recommendations landed as actionable moves instead of industry commentary. The Council writes with more nerve when it knows whose decision it is informing.

---

## Scope

Optional — but the difference between a report that covers what you needed and one that covers what the Strategist found interesting. One item per line; each becomes both a research assignment and a success criterion.

### Writing scope items that work

**Give each item a question and a standard, not just a noun.** Compare:

Weak:
> - Network technology
> - Vendor management

Strong (from the IoT run):
> - Network layer durability: LoRaWAN vs. cellular IoT (LTE-M, NB-IoT) vs. private 5G vs. Wi-Fi 6E for airport sensor applications. What survives a 10-year horizon and what's already obsolescing?
> - Vendor strategy: what separates IoT programs that maintain optionality from those that quietly become single-vendor by year 3? Procurement patterns, contract structures, and exit-cost transparency.

The strong versions name the alternatives to compare, the horizon to judge against, and the evidence that would settle the question. An agent handed the weak version writes a survey; handed the strong version, it runs a comparison and returns a verdict.

**Patterns that consistently produce good sections:**

- **The failure taxonomy:** *"Catalog 6–10 major deployments that became orphaned or got ripped out, and identify the specific architectural decision that doomed each."* Bounded count, named deliverable, causal demand.
- **The named-benchmark question:** *"How do high performers (FRA, AMS, ATL) actually scale EBS, and what does under-sized EBS cost in operational flexibility?"* Naming the comparators tells agents exactly where to dig.
- **The hidden-number question:** *"The 95% rule and what it hides: stated read rates vs. real-world performance after 2–3 years."* Points agents at the gap between spec and reality — where the interesting findings live.
- **The decision-framework demand:** *"When does processing belong on-sensor, on-gateway, on-prem, or in cloud? Decision framework, not preferences."* The last three words prevent an opinion piece.
- **The "what actually happens" question:** *"What pattern do high-performing programs actually use, and why does it differ from what enterprise IT recommends?"* The word *actually* licenses agents to contradict conventional wisdom — which several are built to do.

**Calibration:** five to eight items is the sweet spot. Fewer than four and the Strategist scopes the piece itself (fine, but you lose control). More than ten and the report goes wide instead of deep — a kitchen-sink scope produces a survey wearing a thesis as a hat.

If the run should inform a specific decision, make the last scope item say so — the BHS run's final item named the IAD capital program and the specific new-build opportunities on the table, and the report's entire recommendations section grew from that one line.

---

## Avoid

Optional, short, and more powerful than it looks. Each line is a guardrail the Red Team enforces and the Editor cuts toward. Without it, the Strategist drifts toward whichever framing is easiest to write.

**Name the failure modes this particular thesis invites.** Every topic has a gravitational pull toward some lazy version of itself. Technology theses drift toward vendor brochures. Preparedness theses drift toward fear. Capital-program theses drift toward boosterism. Write the Avoid list by asking: *if this report went wrong, what would it sound like?*

From real runs:
> - Marketing-grade "digital twin" narratives. Vendor capability lists. Anything that ends with "deploy a platform."
> - Promises about AI/computer-vision sortation that haven't proven out at scale. RFID-as-silver-bullet narratives.
> - A polemic that ignores the genuine reasons for the status quo.

Three properties make these work: they're **specific** (not "avoid bias" but "RFID-as-silver-bullet narratives"), they're **recognizable** (an agent can tell when a draft is doing it), and they **preempt the likely failure** rather than a hypothetical one.

Two or four lines is plenty. A ten-line Avoid list reads as anxiety and constrains the argument into blandness — the report also needs room to surprise you.

---

## Decision frame

This section is optional in the form and load-bearing in the output. It tells
the Council which decision the research is meant to improve.

Fill what you know:

- **Decision required:** the choice, authorization, or posture the work should
  enable.
- **Decision owner:** the executive, board, program, or operating owner who can
  act.
- **Time horizon:** the budget cycle, agreement window, project milestone, or
  operating deadline.
- **Approval path:** board, airline majority-in-interest, FAA, TSA, procurement,
  labor, host jurisdiction, or another dependency.
- **Success measure:** the observable condition that would show the decision
  worked.

Unknowns are acceptable. Write "research and state explicitly" rather than
guessing. The airport context packet and executive review will try to close the
gap and will preserve it as a named dependency if public evidence cannot.

A useful decision frame:

> **Decision required:** Whether to pilot a non-sterile visitor-access program
> at one terminal before the FY28 checkpoint expansion.
>
> **Decision owner:** COO, with CEO and TSA concurrence.
>
> **Time horizon:** Pilot decision within 90 days; operating test before the
> holiday peak.
>
> **Approval path:** TSA security plan amendment, airport police, airlines,
> concessions, and terminal operations.
>
> **Success measure:** Visitor demand served without reducing passenger
> throughput or increasing checkpoint incidents.

This is more useful than "provide recommendations." It gives the Council
something it can assign, sequence, and test.

---

## A worked example, annotated

The strongest run prompt this Council has executed, with the moves labeled:

> **Thesis:** Most airport IoT deployments are stranded within 5 years *(falsifiable claim with a number)* — not because the sensors fail, but because the surrounding decisions (network, data ownership, integration path, vendor lock) were made for a pilot and never re-made for scale *(mechanism, with the failure vectors named)*. The future-proofing question is not "what's the best sensor" but "what's the architecture that survives three vendor changes, two network upgrades, and one CIO turnover." *(the reframe — the sentence the whole report exists to defend)*
>
> **Scope:** seven items, each with named alternatives (LoRaWAN vs. LTE-M vs. private 5G), named benchmarks (FRA, AMS, ATL), bounded deliverables (catalog 6–10 deployments), and time horizons (10-year, year-3, 2–3 years of operation). One item anchors the run to the operator's live capital decision.
>
> **Avoid:** three lines naming the exact lazy versions this topic invites — vendor advocacy, unproven-tech promises, platform-pitch endings.

The report that came back compared architectures instead of describing them, returned verdicts instead of considerations, and closed with moves the operator could take to a program meeting. That is the framing doing its work.

---

## Pre-launch checklist

Thirty seconds before you hit Convene:

- [ ] Could an informed person disagree with the thesis? (If not: sharpen until they could.)
- [ ] Does the thesis contain a mechanism — a *because*?
- [ ] Is there at least one number, date, or named case an agent can check?
- [ ] Does each scope item name what to compare, where to look, or what would settle it?
- [ ] Is there a scope item tying the run to the decision you actually face?
- [ ] Does the decision frame identify an owner, horizon, and approval path—or
      mark them as research gaps?
- [ ] Does the Avoid list name this topic's specific lazy failure modes?
- [ ] Is the title short enough to live in a filename?

Three or more unchecked: spend five more minutes on the framing. It's the highest-leverage five minutes in the entire run — everything downstream, across every agent and every stage, inherits it.
