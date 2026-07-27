# Methodology

This file is the source of truth for the Council's public methodology
disclosure. The run manifest supplies the actual roster, models, artifacts, and
quality results for each report.

## Public disclosure

> **How this report was produced**
>
> This document was produced by the Transform Airports AI Research Council, a
> multi-agent analytical system operated with human review. The Council does
> not ask one model to research, write, and approve its own answer.
>
> The named airport's current governance, financial, capital, airline,
> regulatory, and operating context was assembled first from operator-supplied
> files and authoritative public records. A run-specific group of research
> agents then investigated the thesis independently. They could read the shared
> context packet but not one another's work.
>
> Each researcher produced both an analytical brief and structured evidence
> records. A research editor deduplicated those records, ranked the
> load-bearing evidence, preserved disagreement, and identified gaps. A
> Creative Director proposed several truthful narrative approaches before the
> Strategist selected and wrote the argument.
>
> The draft passed through two different adversarial reviews. An Evidence
> Prosecutor tested sources, numbers, causality, and counterevidence. An Airport
> Executive Reviewer tested decision clarity, governance, finance, airline
> response, procurement, delivery, and operating feasibility. The Strategist
> revised after each.
>
> An Editor tightened the work and a Humanizer refined its voice without
> changing facts. A source verifier then checked load-bearing claims against the
> evidence ledger and underlying primary sources, removed or qualified
> unsupported claims, and created a machine-readable claim-to-source lineage
> record.
>
> Before publication, deterministic quality gates checked citations, internal
> provenance leakage, unresolved placeholders, footnote integrity, and other
> release defects. When a presentation was requested, an Art Director defined
> the visual argument. Every final slide was rendered and inspected at full
> size, then the complete deck was inspected as a montage for narrative rhythm.
> A SHA-256-bound inspection receipt records the exact deck, visual brief,
> slide renders, montage, canonical signature slide, resolved findings, and
> inspector attestation. Every Word page was likewise rendered, inspected at
> full size and in sequence, and bound to its own inspection receipt.
>
> Human review occurred after adversarial synthesis and after source
> verification. The report's run archive preserves its roster, research,
> evidence ledger, drafts, critiques, verification log, quality results, and
> model-cost record. AI-assisted production does not reduce the named human
> reviewer's responsibility for what is released.

## Design principles

### Independent research prevents early convergence

Researchers share the question and the airport context packet, not one
another's conclusions. This preserves genuinely different lines of inquiry.
The evidence curator reconciles them only after the swarm finishes.

### Evidence is a typed artifact

A research brief is analysis, not proof. Source-bearing findings live in an
evidence ledger with stable IDs, source metadata, dates, units, denominators,
caveats, and confidence. The final claim-lineage file records which evidence
supports each load-bearing claim and what the verifier did with it. For a
retained claim, the lineage must match the exact sentence or table row, its
adjacent footnote marker, the exact reader-facing citation, an evidence-ledger
record for that same source, and the final document hash. Unsupported claims
can remain in the audit record only when marked as excluded from the final
draft.

### Counterevidence is part of the record

The Contrarian research lens and the Evidence Prosecutor preserve the strongest
case against the thesis. Disagreement is not averaged away. A conclusion is
stronger when the reader can see the conditions under which it would fail.

### Creativity enters before the prose hardens

The Creative Director proposes three narrative spines: board-ready,
counterintuitive, and operational. Each must cite the same evidence ledger.
This gives the work a chance to surprise without giving it permission to
invent.

### Airport recommendations must be assignable

Material recommendations identify an owner, approval route, first 90-day
action, cost order of magnitude, funding source, dependencies, leading
indicator, failure mode, stop condition, and the evidence that would change the
recommendation. Missing operator facts remain named gaps.

### Verification is independent and source-facing

The final verifier reviews the reader-facing draft after editing. A brief can
locate a source but cannot certify its own interpretation. When a brief and the
underlying source disagree, the source wins.

Every generated artifact carries a dependency receipt for the exact upstream
files its prompt and agent charter permit it to read. Glob membership, bytes,
and the stable run identity are hash-bound. The run identity also fingerprints
the local orchestration code, research contract, agent charters, and brand
rules. Resume therefore fails closed when an upstream artifact or Council
version changes; it does not join old synthesis to newly generated research.
Publication-gate remediation reads immutable snapshots and writes separate
outputs before promotion, preserving a checkable before-and-after chain.

### Publishing is a quality-controlled stage

Word and PowerPoint files are treated as professional products. Internal agent
names and stage labels cannot appear in reader-facing text. Decks use
evidence-bearing visuals, readable sources, mode-specific slide and typography
limits, and a rendered visual QA loop. Conversion alone is not inspection:
PowerPoint release requires a passing receipt bound to every full-size slide
render, the narrative montage, and the visual brief's exact signature slide.
Word release requires a second inspector to review every full-size page plus
the page-sequence montage and attest a receipt bound to the exact DOCX, PDF,
and page renders. Missing render tools are a release error, not a warning.
The exact Office packages that pass QA are copied into a SHA-256-bound release
bundle and independently rendered once more. Distribution uses an immutable,
hash-named bundle plus a compact current-release manifest replaced only after
the full bundle is ready. The UI advertises only files whose package and QA
hashes still match that manifest. Only a complete release is archived and
marked finished; the system does not rebuild approved documents from Markdown
after review.

### Human judgment remains load-bearing

The Council records optional human scores for originality, airport specificity,
decision usefulness, writing, and visual quality. Those signals help improve
the system; they do not transfer accountability from the person or institution
that publishes the work.

## Limitations

- Public records may omit confidential airline, security, labor, commercial,
  or procurement information.
- A source can be authentic and still be incomplete, outdated, or methodically
  weak.
- Primary-source verification reduces factual risk; it does not guarantee that
  an inference or recommendation is correct.
- Model behavior and web access can change. Each run's manifest records what
  actually executed.
- The Council produces decision-quality drafts. Subject-matter, legal,
  security, financial, and executive review remain necessary where the stakes
  require them.
