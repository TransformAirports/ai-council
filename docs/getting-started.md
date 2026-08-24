# Get the AI Council running

This guide takes a new operator from an empty machine to the browser app and a
first report. The Council runs locally on macOS or Linux. Each new report uses
one selected model for the full pipeline: Claude Fable 5 or GPT-5.6 Sol.

## 1. Install the four system prerequisites

You need:

- Python 3.11 or newer
- At least one report provider: Claude Code signed in for Fable 5, or Codex
  signed in with ChatGPT for GPT-5.6 Sol
- LibreOffice, which renders Word and PowerPoint packages during QA
- Poppler, which renders PDFs during visual inspection

### macOS

With [Homebrew](https://brew.sh/) installed:

```bash
brew install python@3.12 poppler
brew install --cask libreoffice
curl -fsSL https://claude.ai/install.sh | bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
claude auth login
codex login
```

If `python3 --version` still names an older system Python, follow Homebrew's
printed PATH instruction before continuing.

### Ubuntu or Debian

```bash
sudo apt update
sudo apt install git python3 python3-venv libreoffice poppler-utils
curl -fsSL https://claude.ai/install.sh | bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
claude auth login
codex login
```

Confirm that `python3 --version` is 3.11 or newer. On an older distribution,
install a supported Python before continuing.

The Council deliberately uses the saved Claude and ChatGPT subscription
sessions. It does not read provider API keys from `.env` or use them for model
execution.

## 2. Clone the Council

```bash
git clone https://github.com/TransformAirports/ai-council.git
cd ai-council
```

The first `./council` command creates a private `.venv` in this folder and
installs the Python package. Do not use `sudo` and do not activate the virtual
environment manually.

## 3. Sign in to the subscriptions you use

No `.env` file or API key is required for new reports:

```bash
claude auth login
codex login
claude auth status
codex login status
```

Claude Fable uses the Claude Code subscription session. GPT-5.6 Sol, Prompt
Coach, and Deep Research use the ChatGPT subscription session through
`codex exec`. The Council explicitly removes provider API-key environment
variables from every model subprocess so a report cannot silently fall back
to API billing.

## 4. Run the doctor before spending anything

```bash
./council --doctor
```

The doctor makes no model call and changes no report files. It checks the
Python version, at least one configured report provider, LibreOffice, Poppler,
Python packages, writable work folders, free disk space, and model routing.
Every blocking result includes a command or concrete next step.

Do not start a report until all required checks pass.

## 5. Open the app

```bash
./council
```

The app opens at `http://127.0.0.1:8723`. Leave the terminal window running.
The server listens only on the local machine and gives each browser tab a
session credential for state-changing actions.

For a first demonstration:

1. Open **How it works** for the four-stage primer.
2. Open **Meet the Council** to browse all agent descriptions without starting
   a report.
3. Choose **New Research Report**.
4. Give the AI Prompt Coach a rough idea, apply its draft, and revise the fields.
5. Choose a small, relevant research roster. Keep both human checkpoints on.
6. Choose Claude Fable 5 or GPT-5.6 Sol for the entire report, confirm the
   subscription route, and set the optional execution guardrail before launch.

The prompt coach is a separate, one-call GPT-5.6 Sol form assistant using the
same ChatGPT subscription login. It has a 4,000-token output contract. It cannot choose agents, change the report budget,
request a deck, disable checkpoints, create a run file, or launch the Council.

## What a full run does

A report is not a single chat response. The Council builds current airport
context, runs independent researchers in parallel, curates an evidence ledger,
tests several narrative frames, writes and attacks the argument twice, verifies
material claims against sources, pauses for two human decisions, builds Office
packages, renders every page and slide, and promotes a hash-verified release.

Time and cost depend on the number of agents, source volume, selected model,
and whether a deck is included. The app shows a planning range before launch.
Fable receives a bounded per-call allocation; GPT usage is calculated from API
token receipts and the guardrail is checked between calls.
Treat the estimate as a planning range, not a quote.

## If a run stops

Do not clear `outputs/` and do not start over. Relaunch:

```bash
./council
```

The home screen shows **Resume** when validated work is present. A resume
rechecks the run identity, source bytes, agent charters, dependency receipts,
and completed artifacts; it skips only work that still matches. Browser
disconnects also reconnect to the durable run event journal.

Technical details are written to `logs/last-error.log`. The browser's live
event history is written to `outputs/run-events.jsonl` during an active run and
is copied into the archive on completion.

## Where the work goes

| Path | Purpose |
|---|---|
| `prompts/runs/` | Human-readable run prompts |
| `sources/runs/<slug>/` | Council-owned copies of supplied source material |
| `outputs/` | Resumable active-run workspace |
| `runs/YYYY-MM-DD-<slug>/` | Complete evidence, draft, QA, and production archive |
| `reports/` | Current distribution-ready Word and PowerPoint files |
| `.council-state/trash/` | Recoverable Library removals |

Library title, summary, and tag edits are stored outside immutable report
packages. **Move to Trash** withdraws the entire report family—including all
revisions, Council-owned source copies, prompt, archive, convenience packages,
QA, and historical release bundles—only after showing the exact inventory. It
does not delete an external original source file.

## Common setup failures

### `LibreOffice (soffice) is not installed`

Install LibreOffice, close and reopen the terminal, then rerun
`./council --doctor`. On macOS, opening LibreOffice once can clear the operating
system's first-launch prompt before a long run reaches production.

### `Poppler (pdftoppm) is not installed`

Install `poppler` on macOS or `poppler-utils` on Ubuntu. `pdftoppm` must be on
the shell PATH used to launch `./council`.

### Claude is not signed in

```bash
claude auth login
claude auth status
./council --doctor
```

If a corporate proxy or managed model gateway is involved, configure Claude
Code first and confirm `claude auth status` in the same terminal.

You can instead select GPT-5.6 Sol after running `codex login` and restarting
the Council. A GPT-selected report never falls back to Claude or API-key billing.

### The browser did not open

Open `http://127.0.0.1:8723` manually. For SSH or a machine without a browser,
use `./council --terminal`; report checkpoints still require an interactive
operator unless `--no-review` was explicitly selected.

### A report reached the budget ceiling

Completed, validated artifacts remain in `outputs/`. Resume with a new ceiling
only after reviewing the run's current spend and remaining work. A ceiling of
zero permits no model calls.

## Updating and validating a local checkout

Before pulling changes, allow any active report to finish or stop cleanly. Then:

```bash
git pull --ff-only
./council --doctor
```

Developers changing Council behavior should also run the repository test and
render checks documented in `README.md`. Agent definitions are edited in
`.claude/agents/`; `.codex/agents/` is generated and should not be hand-edited.
