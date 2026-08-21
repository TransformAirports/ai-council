# Get the AI Council running

This guide takes a new operator from an empty machine to the browser app and a
first report. The Council runs locally on macOS or Linux. A normal report uses
Claude; the optional Deep Research seat also uses OpenAI.

## 1. Install the four system prerequisites

You need:

- Python 3.11 or newer
- Claude Code, signed in to a Claude subscription or configured with an
  Anthropic API key
- LibreOffice, which renders Word and PowerPoint packages during QA
- Poppler, which renders PDFs during visual inspection

### macOS

With [Homebrew](https://brew.sh/) installed:

```bash
brew install python@3.12 poppler
brew install --cask libreoffice
curl -fsSL https://claude.ai/install.sh | bash
claude auth login
```

If `python3 --version` still names an older system Python, follow Homebrew's
printed PATH instruction before continuing.

### Ubuntu or Debian

```bash
sudo apt update
sudo apt install git python3 python3-venv libreoffice poppler-utils
curl -fsSL https://claude.ai/install.sh | bash
claude auth login
```

Confirm that `python3 --version` is 3.11 or newer. On an older distribution,
install a supported Python before continuing.

Claude Code also supports pay-as-you-go authentication. Instead of subscription
login, place `ANTHROPIC_API_KEY` in the Council's `.env` file in step 3. Never
commit that file.

## 2. Clone the Council

```bash
git clone https://github.com/TransformAirports/ai-council.git
cd ai-council
```

The first `./council` command creates a private `.venv` in this folder and
installs the Python package. Do not use `sudo` and do not activate the virtual
environment manually.

## 3. Configure only the credentials you need

Claude subscription login requires no `.env` file. Create one for Claude
API-key billing, the GPT-5.6 Sol Prompt Coach, or the optional OpenAI Deep
Research seat:

```bash
cp .env.example .env
```

Then edit `.env` and uncomment the relevant line:

```text
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
```

`ANTHROPIC_API_KEY` moves Claude usage to pay-as-you-go API billing.
`OPENAI_API_KEY` runs the Prompt Coach through GPT-5.6 Sol and is also used when
**Deep Research** is seated. OpenAI cost is separate from the Claude report
budget ceiling shown in the app.

## 4. Run the doctor before spending anything

```bash
./council --doctor
```

The doctor makes no model call and changes no report files. It checks the
Python version, Claude CLI and authentication, LibreOffice, Poppler, Python
packages, writable work folders, free disk space, and resolved model routing.
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
6. Review the cost range and set a firm Claude budget ceiling before launch.

The prompt coach is a separate, one-call GPT-5.6 Sol form assistant with a
conservative $1.50 local ceiling and a 4,000-token output cap. The app shows its
estimated OpenAI API cost. It cannot choose agents, change the report budget,
request a deck, disable checkpoints, create a run file, or launch the Council.

## What a full run does

A report is not a single chat response. The Council builds current airport
context, runs independent researchers in parallel, curates an evidence ledger,
tests several narrative frames, writes and attacks the argument twice, verifies
material claims against sources, pauses for two human decisions, builds Office
packages, renders every page and slide, and promotes a hash-verified release.

Time and cost depend on the number of agents, source volume, selected models,
and whether a deck or Deep Research is included. The app shows a calibrated
range before launch and enforces the Claude ceiling between bounded calls.
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

### The browser did not open

Open `http://127.0.0.1:8723` manually. For SSH or a machine without a browser,
use `./council --terminal`; report checkpoints still require an interactive
operator unless `--no-review` was explicitly selected.

### A report reached the budget ceiling

Completed, validated artifacts remain in `outputs/`. Resume with a new ceiling
only after reviewing the run's current spend and remaining work. A ceiling of
zero permits no Claude calls.

## Updating and validating a local checkout

Before pulling changes, allow any active report to finish or stop cleanly. Then:

```bash
git pull --ff-only
./council --doctor
```

Developers changing Council behavior should also run the repository test and
render checks documented in `README.md`. Agent definitions are edited in
`.claude/agents/`; `.codex/agents/` is generated and should not be hand-edited.
