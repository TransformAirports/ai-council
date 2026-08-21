# AI Council — Known Issues and Bug Ledger

Compiled 2026-08-12, after the `quiet-by-design-standards-for-mwaa-terminals-2`
run (Aug 6–12). Two sections: what is still broken, and what broke this cycle
and was fixed. Severity reflects cost to a live run, not code elegance.

---

## Open bugs

### 1. Dependency-receipt hash drift — the "it's starting over" bug

**Severity: critical. This caused every full-pipeline restart this week (six).**

Every artifact records a dependency receipt whose payload is digested into a
`sha256`. On resume, `dependency_fingerprint_matches()` rebuilds the payload
and compares digests. For the context step, the recorded digest never matched
the rebuilt one **even when every input file, and the run identity, were
byte-identical** (observed: recorded `5f963a3d…` vs rebuilt `30c5e0ec…` over
the same inputs). The step-start check then quarantined the context outputs
and re-ran the step; new context bytes invalidated every downstream receipt,
and the integrity chain — working as designed — rebuilt the entire run.

- Suspected cause: the digest recorded at write time is computed over a
  slightly different serialization than the one `build_dependency_fingerprint`
  rebuilds (key order, field set, or a rewrite during
  `create_run_manifest(resume=True)`'s artifact merge). Not yet pinned down.
- Evidence: `outputs/context/` in the archived run holds six
  `.partial-*` quarantines, one per resume (Aug 7 ×4, Aug 10, Aug 12).
- Workaround used: recompute each receipt's digest over its own body and
  rewrite the manifest (done manually 2026-08-12 to unblock the archive).
- Fix needed: single canonical serializer used by both writer and verifier;
  a regression test that round-trips a receipt through
  `create_run_manifest(resume=True)` and asserts `dependency_fingerprint_matches`.

### 2. Checkpoint approvals are not persisted

**Severity: high (user-facing friction, no data loss).**

Human checkpoint decisions live only in run memory. Every resume replays
Checkpoint #1 even when the operator already approved it — three times in one
run this week. Fix: record the decision (checkpoint id, action, timestamp,
draft hash it was granted against) as a manifest entry, and skip the replay
when the underlying artifacts are unchanged.

### 3. Resume rebuild drops unknown manifest fields

**Severity: high (destroys audit trail).**

`create_run_manifest(resume=True)` rebuilds the manifest from a fixed field
list. Anything it doesn't know about — including the `resume_rebaselines`
audit history that `cli/resume_repair.py` writes — is silently discarded.
A re-baselined run becomes indistinguishable from an untouched one, which is
exactly what the audit trail exists to prevent. Fix: carry unknown top-level
fields through the rebuild verbatim.

### 4. Format contract enforced only at the very end

**Severity: high (burns full pipeline cycles).**

The run contract said "1,500–2,000-word article, no appendices." The
fact-checker produced a 3,482-word draft with an 1,100-word Decision Card
appendix, and nothing objected until the publication gate — after research,
synthesis, editing, humanizing, and verification were all paid for. The gate
then reported 45–64 blockers, most of them consequences of the oversized claim
load. Fix: cheap word-count/structure checks after the strategist, editor,
humanizer, and fact-checker steps, failing fast with the contract quoted.

### 5. Internal-only sources can back reader-facing claims

**Severity: medium-high.**

The evidence ledger accepts records whose only source is the internal Airport
Context Packet (no URL, not reader-citable). The fact-checker then attaches
them to footnotes, and the gate correctly rejects the pairing — but only at
the end. The DCA 2025 traffic figures were lost from the final report for
exactly this reason. Fix: at curation time, either require an external
source on packet-derived records or mark them `internal_only` so the
fact-checker never cites them.

### 6. Research agents can misquote their sources

**Severity: medium-high (citation integrity).**

A ledger record attributed "771 alarms per bed per day" to a trade-press
article that does not contain that figure; the claim survived research,
curation, and one fact-check pass, and was caught only by manually fetching
the article during operator remediation. Fix: a curation-time spot-check that
fetches a sample of `supporting_excerpt`s and verifies the quoted text (or at
least the load-bearing numbers) actually appears in the cited source.

### 7. Fact-checker's lineage bookkeeping diverges from its own report

**Severity: medium.**

The fact-check *report* documented genuine primary-source verification
(✓ with URLs) for many claims whose lineage records said
`primary_source_checked: false`. The gate reads only the lineage, so
verified work was counted as unverified — 14–20 blockers per cycle from
recording inconsistency alone. Fix: have the fact-checker emit one structured
verification record per claim and generate both the report table and the
lineage from it, so they cannot disagree.

### 8. Model-driven remediation is slow and may not converge

**Severity: medium (cost/time).**

Gate remediation passes ran 40–80 minutes each and one cycle went 64 → 64.
Most blockers are mechanical (binding, renumbering, span alignment) and are
fixable deterministically before spending model time. Fix: a deterministic
pre-remediation pass (rebind lineage, renumber footnotes, align claim spans),
then the model pass only for genuinely substantive blockers.

### 9. No persistent event journal for post-mortems

**Severity: low-medium.**

When a run dies, the only forensic records are the server console log and the
manifest. Sequenced events exist in memory (`WebSink`) but are not written to
disk. Fix: append events to `outputs/run-events.jsonl` as they are emitted.

---

## Fixed this cycle (Aug 7–12)

| # | Bug | Fix | Where |
|---|-----|-----|-------|
| 1 | Resume contract hashed the roster in click order; reordering agents blocked resume | Order-insensitive roster hash | `cli/run_manifest.py` |
| 2 | Resume contract hashed all of `cli/*.py`; editing WebSocket/UI code bricked in-flight runs | Generation/app-shell split (`APP_SHELL_PATHS` denylist) | `cli/run_manifest.py` |
| 3 | Re-baseline moved the run identity without moving dependency receipts, silently condemning completed work to re-runs | `_restamp_dependency_identities` with a bytes-intact guard; audit entry records what moved | `cli/resume_repair.py` |
| 4 | Evidence contract required `source_url` or `source_path`; paywalled standards (NFPA, IEC, ANSI) could never validate, killing runs | Third provenance form `source_citation`, valid only with a locator (`requires_with`) | `cli/orchestrator.py`, `cli/artifacts.py`, `cli/run_manifest.py`, `prompts/research-contract.md` |
| 5 | One professional-judgment record in an evidence file destroyed the agent's entire output | Unsourced records sequester to `<name>.unsourced.jsonl`; all-unsourced and malformed records still fail loudly | `cli/orchestrator.py` |
| 6 | Ledger normalizer dropped `source_citation`, so paywalled-source records passed stage 1 and died at the ledger | Field carried through | `cli/evidence.py` |
| 7 | Lineage binder required the claim to fit inside the marker's sentence; multi-sentence claims could never bind | Containment accepted in both directions | `cli/evidence.py` |
| 8 | CLI session flag (`is_error` + `stop_sequence`, no real error) killed runs mid-write | Complete artifact sets accepted; incomplete work retried once; diagnostics now name the trigger | `cli/orchestrator.py` |
| 9 | Publication gate got exactly one remediation pass; large blocker sets could never converge | Bounded loop, re-gating each pass (`MAX_REMEDIATION_PASSES = 3`) | `cli/orchestrator.py` |
| 10 | Fact-checker wrote footnotes from memory, then attached topical evidence IDs — fabricated citations (a statute footnote backed by a fire-alarm standard) | Instructions: compose the footnote *from* the attached records; contiguous claim spans; three honest options when evidence doesn't match | `.claude/agents/fact-checker.md` |
| 11 | Gate's citation matcher didn't recognize `source_citation`, so paywalled sources read as mismatches | Field added to source candidates | `cli/quality_gate.py` |
| 12 | Changing one agent's instructions blocked resume for the whole run | `--redo-agent`: discard that agent's artifacts (receipts stripped), keep everyone else's | `cli/resume_repair.py` |
| 13 | Release QA rendered the Word report and the deck into the same stem-named folder; the second render clobbered the first and hash verification failed at end of promotion | Render dirs scoped by extension (`<stem>-docx`, `<stem>-pptx`) | `cli/publish.py` |
| 14 | Word visual inspection crashed on machines without LibreOffice (`Word inspection requires one rendered PDF…`) | LibreOffice installed (environmental); consider a preflight check that reports the missing renderer before stage 4 | environment |
| 15 | A crashed browser stranded runs at unapprovable checkpoints ("A run is already in progress") | Sequenced event log, cursor replay, ownership handoff to a live tab | `cli/server.py`, `cli/events.py`, `cli/webapp/app.js` |
| 16 | Professional judgment and evidence rules were implicit | Explicit rules: judgment goes in the brief, never the evidence file; never invent a URL to satisfy a schema | `prompts/research-contract.md`, inline prompts |

---

## Process notes for the next maintainer

- Any edit to generation code (`cli/orchestrator.py`, builders, prompts,
  agent definitions) changes the execution contract; in-flight runs then need
  `python -m cli.resume_repair --apply --accept-code-changes` (or
  `--redo-agent <name>` for instruction changes). Edit transport/UI code
  freely — it no longer blocks resume.
- Never modify `outputs/` or re-baseline while a run is live. Check
  `ps` for `bin/council` and `_bundled/claude` first. Two of this week's
  restarts were caused by exactly this.
- The deterministic finish (release staging, promotion, archive) can be run
  directly from Python when the pipeline is wedged — that is how this run was
  ultimately delivered. The entry points are `stage_release_artifacts`,
  `promote_release` (`cli/publish.py`), and `archive_run` (`cli/archive.py`).
