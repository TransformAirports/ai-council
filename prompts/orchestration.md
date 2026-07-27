# Orchestration — Transform Airports AI Council

This is the canonical operating contract for a report run. The user triggers it
with `run <filename>`. The executable implementation is
`cli/orchestrator.py`; this document explains how Codex or Claude should launch,
monitor, and hand off that implementation. Do not reconstruct the pipeline by
manually invoking a fixed roster of agents.

## Resolve and validate the run

1. Resolve the name inside `prompts/runs/`, accepting the directory prefix and
   `.md` as optional.
2. Run the deterministic prompt preflight. It must reject unresolved
   `{{...}}` tokens, missing required sections, an invalid output or deck mode,
   a missing supplied source, and an empty research roster.
3. Read the prompt and confirm the thesis, decision frame, selected research
   lenses, requested deliverables, and configured budget with the user. Make
   clear that this is a paid, multi-model run. Do not quote a fixed time or cost
   for every roster.
4. After confirmation, launch the exact file:

   ```bash
   ./council --run prompts/runs/<slug>.md
   ```

   Keep the process attached and monitor it. Use `--no-review` only when the
   user explicitly authorizes an autonomous run. Use `--budget USD` when the
   user specifies a ceiling.

The command is responsible for authentication checks, model routing, typed
artifact validation, budget enforcement, checkpoint state, resume behavior,
publishing, archiving, and cleanup. If it stops, preserve `outputs/` and resume
with `./council --resume <slug>`. Reuse a completed artifact only when its
validated bytes, declared upstream dependency receipt, run identity, and
fingerprinted Council code/prompt/design contract still match; otherwise
quarantine and regenerate it.

## Public stage 1 — context, parallel research, and curation

1. Create `outputs/run-manifest.json`. It records the decision frame, selected
   research and process agents, actual models, prompt hashes, contracts,
   artifacts, dependency receipts, Council execution-contract fingerprints,
   and stage state.
2. Invoke the Airport Context Builder. It writes:
   - `outputs/context/airport-context.md`
   - `outputs/context/context-sources.jsonl`
3. Invoke every selected research agent as an independent **parallel research
   swarm**. The roster comes from the manifest; never assume a fixed number or
   filename list. A researcher may read the run prompt, shared context, and
   supplied sources, but not another researcher’s output.
4. Each researcher writes:
   - `outputs/stage1/<agent>-brief.md`
   - `outputs/stage1/<agent>-evidence.jsonl`
5. Build and normalize `outputs/evidence-ledger.jsonl`. Evidence IDs must be
   unique across the run and trace to source and researcher provenance.
6. Invoke the Evidence Curator. It deduplicates evidence, preserves genuine
   conflict, ranks load-bearing records, closes only focused gaps, and writes
   `outputs/stage1/evidence-map.md`.

The stage fails when a required brief or typed artifact is missing or invalid.
Missing optional structured evidence is visible as a telemetry gap; it is not
silently treated as success.

## Public stage 2 — creative framing and adversarial synthesis

Run the declared sequence from the manifest:

1. Creative Director → `outputs/stage2/narrative-options.md`
2. Strategist v1 → `outputs/stage2/strategist-draft-v1.md`
3. Evidence Prosecutor → `outputs/stage2/red-team-critique-v1.md`
4. Strategist v2 → `outputs/stage2/strategist-draft-v2.md`
5. Airport Executive Reviewer →
   `outputs/stage2/red-team-critique-v2.md`
6. Strategist v3 → `outputs/stage2/strategist-draft-v3.md`

The first reviewer prosecutes source use, arithmetic, causality, stale data,
missing counterevidence, and unsupported narrative. The second reviewer tests
airport executability: authority, board and airline response, finance,
procurement, regulation, staffing, delivery, peak-hour operations, measures,
and stop conditions. These are different jobs and neither substitutes for the
other.

### Human checkpoint 1

Present v3 and both specialized critiques. Summarize what changed, which
findings were answered or defended, and what weaknesses remain. Ask the user to
score any of originality, airport specificity, decision usefulness, and
writing on the 1–5 rubric. Persist the scores as structured evaluation data.

Do not continue without approval unless the run was explicitly launched with
`--no-review`. A requested redo resumes from the smallest affected synthesis
step.

## Public stage 3 — edit, verify, and release gate

1. Editor → `outputs/stage3/edited-draft.md`
2. Humanizer → `outputs/stage3/humanized-draft.md`
3. Source Verifier writes:
   - `outputs/stage3/fact-check-report.md`
   - `outputs/stage3/final-draft.md`
   - `outputs/claim-lineage.jsonl`
4. Deterministic publication gate → `outputs/quality-gate.json`

The Source Verifier checks the reader-facing claim against the underlying
source, not merely an internal brief. Canonical lineage statuses are
`verified`, `qualified`, `corrected`, `removed`, and `unverified`. An
`unverified` claim may remain in the verification record only when it was
excluded from the final draft. The reader-facing draft cannot contain an
`[UNVERIFIED]` release tag.

Every retained lineage record must also contain the exact claim text, the
`footnote_id` placed immediately after that claim, a `citation` exactly equal
to the reader-facing footnote definition, evidence IDs that identify that
same source, `retained: true`, and `primary_source_checked: true`. Excluded
records use `retained: false`. The orchestrator binds the record to the exact
final-draft hash only after those relationships match.

The publication gate blocks unresolved placeholders, leaked internal paths or
brief labels, broken footnotes, invalid lineage, and unsupported numeric
claims. A failed gate is a remediation event, not a publishable result.

### Human checkpoint 2

Present the final draft, fact-check report, claim-lineage coverage, and release
gate result. Persist optional writing, airport-specificity, and
decision-usefulness scores. Do not begin production without approval unless
the user explicitly disabled checkpoints.

## Public stage 4 — art direction, Office production, and visual QA

1. Invoke the Art Director for every full report or article and for every
   requested presentation. It writes
   `outputs/stage4/visual-brief.json` using the brand visual contract.
2. Build the Word executive packet from the verified draft, methodology,
   evidence, and visual brief.
3. If requested, build `outputs/stage4/<slug>.pptx` in `board_decision`,
   `executive_briefing`, or `technical_read_ahead` mode.
4. Reopen every Office package and validate its structure. Render pages and
   slides, then inspect overflow, clipping, density, source readability,
   hierarchy, accessibility, and internal-content leakage. Inspect every slide
   individually at full size and inspect a montage for narrative rhythm.
   PowerPoint production is incomplete until a passing inspection receipt is
   bound to the exact deck, visual brief, canonical signature slide, slide
   renders, and montage hashes. Word production is incomplete until an
   independent inspector has reviewed every full-size page and the sequence
   montage and passed a receipt bound to the exact DOCX, PDF, and page hashes.
5. Record structural and rendered QA artifacts in the run manifest. A required
   document, presentation, inspection receipt, or QA report left pending or
   invalid means production is not complete. Missing render tooling is
   release-blocking.

Reader-facing citations name regulations, datasets, reports, official
documents, and other underlying sources. They never name agents, stages, or
research briefs. Visuals that contain data cite evidence IDs internally and
reader-facing sources in the finished artifact.

## Completion, publishing, and archive

A run is complete only after every required manifest artifact and release gate
passes.

1. Copy the exact Stage 4 Office packages into `outputs/release/`, render and
   inspect them independently, and bind each package and QA sidecar to SHA-256
   in `release-manifest.json`.
2. Revalidate every required run-manifest artifact against its current bytes.
3. Reserve the dated archive destination before changing distribution files.
4. Promote the release as an immutable, hash-named bundle under
   `reports/releases/`; replace the compact current-release manifest last and
   keep top-level filenames only as convenience copies. Never rebuild an
   approved Office package from Markdown during publishing.
5. Atomically archive the complete active-run state to
   `runs/YYYY-MM-DD-<slug>/`, including the exact run prompt, context, supplied
   sources, manifests, evidence, lineage, human reviews, drafts, critiques,
   verification, release bundle, Office files, QA, cost, and retrospective.
6. Clear the temporary `outputs/` state only after the archive has been
   promoted into place, then report the archive path, published files, actual
   Claude cost, separately billed provider use, and any material limitation.

If publishing fails, surface the failure and leave the run resumable. Do not
emit a successful `run_complete` event or mark the run complete merely because
research and writing finished.

## Rules throughout the run

- Use the manifest roster and paths; never hard-code a researcher count.
- Respect role-based model assignments in `council.toml`.
- Keep research independent until curation.
- Treat briefs as analysis and the evidence ledger as provenance; cite the
  underlying source to the reader.
- Preserve counterevidence and distinguish observation, inference,
  calculation, and professional judgment.
- Do not invent airport authority, agreement terms, funding, cost, traffic,
  approval, security, or operating facts.
- Material recommendations identify an owner, decision, approval route, first
  action, horizon, measure, failure mode, stop condition, and evidence that
  would change the recommendation.
- Short paragraphs. Active voice. Specific examples. No banned consultant
  language from `AGENTS.md` or `CLAUDE.md`.
- Agents never edit their own or another agent’s definition. Behavior changes
  are reviewed changes to `.claude/agents/`, followed by generated Codex mirror
  synchronization.
