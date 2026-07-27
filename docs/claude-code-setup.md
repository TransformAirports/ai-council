# Council setup and operating reference

This repository is the Transform Airports AI Council: a multi-agent system for
airport-industry research, adversarial analysis, and executive publishing.
The web app is the normal operating surface. Codex can also create, launch,
resume, revise, publish, and audit runs from the repository.

## Operating principles

1. **Frame a decision.** A contested thesis plus an owner, horizon, approval
   path, and success measure produces a usable answer.
2. **Protect research independence.** Swarm researchers do not read one
   another’s briefs before evidence curation.
3. **Preserve disagreement.** The Curator reconciles duplicates, not legitimate
   conflicts in evidence or professional judgment.
4. **Separate review jobs.** Evidence integrity and airport executability are
   different failure modes and receive different adversarial reviewers.
5. **Verify the underlying source.** An internal brief is provenance, not
   reader-facing authority.
6. **Make release mechanical.** Typed artifact validation, lineage checks, copy
   linting, Office-package inspection, and rendered visual QA complement model
   judgment.
7. **Keep humans accountable.** Two checkpoints and final human approval remain
   part of the method.

## Install and launch

Requirements:

- macOS or Linux
- Python 3.11 or newer
- Claude access or an `ANTHROPIC_API_KEY`
- Optional `OPENAI_API_KEY` for the Deep Research lens

From the repository root:

```bash
./council
```

The launcher creates `.venv`, installs dependencies, and opens the browser app.
Copy `.env.example` to `.env` for local credentials. The file is ignored by
Git, and shell environment variables take precedence.

Useful headless commands:

```bash
./council --run prompts/runs/<name>.md --budget 80
./council --terminal
./council --dry-run
./council --resume [SLUG]
./council --revise [SLUG]
./council --publish [SLUG]
./council --pptx
./council --audit
```

`--run` first performs a no-model-call preflight. It rejects unresolved
placeholders, unsafe paths, duplicate or unknown agent names, missing sources,
and incomplete required sections. `--dry-run` creates a new run file; it
cannot be combined with `--run`. A zero budget permits no Claude calls. The
optional OpenAI Deep Research lens is billed separately from that ceiling.

## Architecture

```text
Run prompt + supplied sources
            │
            ▼
Airport context ──► parallel research swarm
                           │
                           ▼
                  structured evidence ledger
                           │
                           ▼
Creative frame ──► Strategist draft
                           │
                  Evidence Prosecutor
                           │
                    Strategist revision
                           │
                Airport Executive Reviewer
                           │
                    Strategist revision
                           │
                    Human checkpoint 1
                           │
              Editor ─► Humanizer ─► Source Verifier
                           │
                 lineage + publication gate
                           │
                    Human checkpoint 2
                           │
          Art direction ─► Word / PowerPoint production
                           │
                   structural + render QA
                           │
                 archive + publish + audit
```

The executable pipeline lives in `cli/orchestrator.py`. The operator contract
lives in [`prompts/orchestration.md`](../prompts/orchestration.md). Agent
behavior is defined in `.claude/agents/`. `.codex/agents/` is generated from
that source with:

```bash
.venv/bin/python scripts/sync_codex_agents.py
```

Do not edit generated Codex mirrors by hand.

## Contracts and provenance

Each run creates a versioned manifest containing selected agents, process
agents, model assignments, prompt hashes, stage state, artifact paths, and
validation results. Research agents emit both a brief and JSONL evidence
records. The evidence ledger gives each record a stable ID and carries source
type, source URL, dates, claim, limitations, and agent provenance.

The final verification pass writes claim lineage. Audit attribution follows
those IDs; it never infers contribution by searching prose for an agent’s
display name.

Interrupted runs resume only from artifacts that pass their contract. Budget
ceilings are enforced between model calls.

## Model routing

`council.toml` maps roles—not individual hard-coded stages—to models:

- context
- research
- curation
- creative framing
- synthesis
- evidence critique
- executive review
- editing
- humanization
- source verification
- art direction
- presentation

This is multi-model orchestration: the system assigns each kind of reasoning to
the configured model instead of assuming one model is best at every job. The
manifest records what actually ran.

## Source material

Put PDFs, Word documents, PowerPoints, spreadsheets, or text files in
`sources/` before launch. The source-ingestion layer converts supported
material for agent reading and archives the originals with the run. Prompts
must distinguish:

- facts supplied by the operator,
- claims found in public sources,
- reproducible calculations,
- and analyst judgment.

Never fabricate authority-specific data to fill a gap.

## Repository map

| Path | Purpose |
|---|---|
| `.claude/agents/` | Human-maintained agent definitions |
| `.codex/agents/` | Generated Codex-native mirrors |
| `assets/brand/` | Brand tokens, visual-contract schema, and production assets |
| `cli/` | Orchestrator, contracts, evidence, evaluation, publishing, and web app |
| `prompts/runs/` | One decision frame per Council run |
| `prompts/research-contract.md` | Required brief and evidence-record contract |
| `outputs/` | Temporary active-run artifacts |
| `runs/` | Complete immutable run archives |
| `reports/` | Distribution-ready Word and PowerPoint files |
| `tests/` | Deterministic contract and regression tests |
| `council.toml` | Models, budgets, and defaults |

## Validation before merging a Council change

```bash
.venv/bin/python -m compileall -q cli scripts tests
.venv/bin/python -m unittest discover -s tests -v
node --check cli/webapp/app.js
git diff --check
```

If agent definitions changed, sync the Codex mirrors and rerun the tests.
Publishing changes also require a scratch document or deck build followed by
rendered visual inspection.

## Governance

Agents never edit themselves or one another. Change behavior through reviewed
edits to `.claude/agents/`; see
[`how-to-propose-an-agent-change.md`](how-to-propose-an-agent-change.md).
Finished documents disclose AI assistance and retain named human
accountability. The complete method is in [`methodology.md`](methodology.md).
