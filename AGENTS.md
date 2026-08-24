# Repo guidance for Codex

This is the **Transform Airports AI Council** — a multi-model system that
produces executive-grade airport decision packages. A run assembles current
airport context, launches a configurable independent research swarm, curates a
structured evidence ledger, tests several creative frames, passes the draft
through evidence and airport-executive adversaries, verifies primary sources,
and produces visually inspected Word and PowerPoint artifacts. Four public
stages. Two human checkpoints. See `README.md`.

## Treat this repo like a Codex app

The user writes a run-prompt markdown file in `prompts/runs/` and then triggers a run by telling you the filename. Everything else — research, synthesis, adversarial revision, polish, fact-checking, Word document generation, archiving — is your job.

### When the user says "run <filename>"

If the user says anything that looks like:

- `run airline-consolidation`
- `run prompts/runs/biometric-risk.md`
- `let's run the cargo-revenue file`
- `kick off <name>`
- `execute <name>`

...treat it as a trigger to start a full Council run on that file.

1. Resolve the filename to a path in `prompts/runs/` (add `.md` if missing; accept with or without the directory prefix).
2. Read the file. If any `{{...}}` placeholders remain or required sections are missing/empty, stop and tell the user what's unfilled. Do not proceed with a half-written run prompt.
3. Confirm you understood: "Running `<slug>`. Thesis: <1-sentence paraphrase>.
   Decision: <decision/owner or research gap>. The app will show the current
   cost range and budget ceiling. Ready?"
4. On confirmation, execute the canonical pipeline defined in [`prompts/orchestration.md`](prompts/orchestration.md) through `./council --run <path>`. You already have the run file path and the slug. The user does not need to paste anything further.

### When the user asks for a new run but has no file yet

If they describe a thesis in conversation without pointing to a file (e.g. "let's do a new run on cargo revenue"), follow [`prompts/start-a-run.md`](prompts/start-a-run.md) — it walks you through gathering the thesis, writing the run file for them, and kicking off the run. This is the conversational path for users who don't want to edit files themselves.

### After a run completes

After Stage 4 (executive packet generated and validated), automatically:

1. Independently QA and hash-bind the exact Stage 4 Office packages in
   `outputs/release/`, reserve the dated archive path, then promote an
   immutable release bundle and its atomic current pointer to `reports/`.
2. Atomically copy the full contents of `outputs/`, the exact run prompt, and
   supplied source bytes to `runs/YYYY-MM-DD-<slug>/` using today's date.
3. Write a short `retrospective.md` in that folder (what worked, what didn't,
   which agent file behaviors to watch in the next run).
4. Clear `outputs/` only after release and archive promotion succeed; cleanup
   must remain safe to retry after an interrupted commit.
5. Tell the user the archive path and a one-line summary of the deliverables.

Do NOT require the user to do the archiving themselves. The archive and clean-up is part of the run.

## Tone rules — apply to every deliverable the Council produces, and to your own prose about the Council

- No buzzwords: "absolutely," "leverage," "synergy," "holistic," "best-in-class," "paradigm shift," "ecosystem" (unless literal), "game-changer," "mission-critical" (unless genuinely so), "in today's rapidly evolving landscape."
- No vague quantifiers ("many," "often," "increasingly") when a specific number exists.
- Short paragraphs. Active voice. Specific examples over abstractions.
- Write for sophisticated, skeptical peer readers — airport executives, planners, and policy leaders.

## What the user should NEVER have to do

- Check out a git branch to run a new thesis
- Copy or edit `orchestration.md`
- Paste the pipeline sequence into Codex
- Manually archive outputs to `runs/`
- Clear `outputs/` between runs
- Remember slug conventions or date formats

Branches are only needed when proposing Council behavior changes. The
human-edited source of truth is `.claude/agents/`; `.codex/agents/` is a
generated native-Codex mirror. See
[`docs/how-to-propose-an-agent-change.md`](docs/how-to-propose-an-agent-change.md).

## Key files

- [`prompts/runs/_template.md`](prompts/runs/_template.md) — the template the user copies and renames
- [`prompts/orchestration.md`](prompts/orchestration.md) — the canonical Council v2 operating contract (you read this; the user does not)
- [`prompts/start-a-run.md`](prompts/start-a-run.md) — conversational entry point for users who want to dictate a thesis instead of writing a file
- [`.claude/agents/`](.claude/agents/) — versioned agent definitions
- [`.codex/agents/`](.codex/agents/) — generated Codex-native mirrors
- [`prompts/research-contract.md`](prompts/research-contract.md) — structured
  evidence contract
- [`runs/2026-04-17-infrastructure-vs-intelligence/`](runs/2026-04-17-infrastructure-vs-intelligence/) — first run's complete archive; use as a reference for what a good run looks like end-to-end

## Cursor Cloud specific instructions

This is a Python 3.11+ CLI + FastAPI web app. Setup, run, and test commands are
documented in [`README.md`](README.md) and [`docs/getting-started.md`](docs/getting-started.md);
the notes below are only the non-obvious cloud caveats.

- **Model runs need an interactive subscription login that cannot be scripted.**
  Any real report/scope/argument run (and the doctor's "Report model provider"
  check, and the web app's launch button) requires `claude auth login` (Claude
  Fable 5) or `codex login` (GPT-5.6 Sol / Prompt Coach). The Council uses those
  saved CLI subscription sessions, never provider API keys — API-key env vars are
  deliberately stripped from model subprocesses, so setting `ANTHROPIC_API_KEY`
  etc. does nothing. Without a login you can still exercise everything that makes
  no model call: `./council --doctor`, the full test suite, the web app UI
  (Meet the Council, How it works, the framing wizard through the review/launch
  screen with its assembled roster + budget), and the code-only doc builders in
  `scripts/`.
- **Virtualenv:** dependencies live in `.venv/` (gitignored). Run tools via
  `.venv/bin/...` or the `./council` wrapper; never activate manually or use
  `sudo`. The `./council` wrapper only auto-installs when `.venv/bin/council` is
  missing — it does NOT reinstall after `pyproject.toml` changes, so re-run
  `.venv/bin/pip install -e .` (the startup update script already does this).
- **Tests:** run `.venv/bin/python -m pytest tests/ -q` (357+ tests, ~5s). The
  suite is mostly `unittest`-style; `tests/test_reattach.py` is the one module
  that imports `pytest`, so `pytest` must be installed (the update script installs
  it). `python -m unittest discover -s tests -v` also works but errors on that
  one module.
- **Web app:** `./council` starts uvicorn on `http://127.0.0.1:8723` in the
  foreground (blocking) and tries to open a browser (harmless/no-op when headless).
  For scripted/headless use, run `.venv/bin/python -c "from cli.server import serve; serve(open_browser=False)"` under tmux/background. State-changing API
  routes require a same-origin session token from `/api/meta`; loopback-only.
- **System renderers:** LibreOffice (`soffice`) and Poppler (`pdftoppm`) are
  required for the stage-4 rendered Word/PPTX QA and are checked by the doctor.
  They are installed in the base environment (not via the update script).
