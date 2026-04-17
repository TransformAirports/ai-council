# Methodology

This file documents how the Council produces its outputs. It is the source of truth for the methodology appendix that must appear in every published document.

## Why a methodology disclosure

An executive-grade piece produced with AI assistance is only credible if the reader understands how it was made. Hiding the method invites suspicion; disclosing it cleanly disarms the objection. The methodology appendix is not a disclaimer. It is a statement of process.

## The canonical appendix

Paste this into every final document. Fill the bracketed fields before publishing.

> **Methodology**
>
> This document was produced by a multi-agent AI system operated by [name / role]. The system consisted of eight specialized agents running on Anthropic's Claude platform:
>
> - **Four research agents** — Infrastructure Economist, Operations Analyst, Technology Scout, and Contrarian — that independently gathered evidence without reading each other's work.
> - **A Strategist** that synthesized the four briefs into a single argumentative draft.
> - **A Red Team** agent that attacked the Strategist's drafts across multiple revision rounds.
> - **An Editor** that tightened the final prose without adding new content or claims.
> - **A Fact-checker** that verified every numerical and attributed claim against the research briefs. Unverifiable claims were removed or flagged for human review.
>
> Total agent runtime: [X] hours. Human review occurred at two checkpoints: after the third Strategist draft and after the Fact-checker's report. Agent definitions are maintained as versioned markdown files in a private repository and are edited only by human reviewers via pull request — agents do not modify themselves or each other.
>
> The final text was reviewed and approved by [name] before release. AI-assisted production does not reduce human accountability for the arguments and claims in this document.

## Principles behind the design

**Independent research beats coordinated research.** The four Stage 1 agents do not share a context. They cannot see each other's briefs. This forces genuine variance in the evidence pool. A pipeline in which agents share drafts tends to converge early and lose the friction that produces a good final argument.

**Steelmanning is mandatory.** The Contrarian agent is not a token skeptic. Its job is to make the strongest possible case against the thesis. If the Strategist can beat the Contrarian only by ignoring it, the thesis is not ready to publish.

**Adversarial revision is the engine.** The Strategist writes. The Red Team attacks. The Strategist revises. The Red Team attacks again. Each round strips away a layer of unsupported claim or weak rhetoric. Two rounds is enough to catch most problems without exhausting the argument.

**Fact-checking has veto power.** Every number in the final document must trace to a Stage 1 brief. If a claim cannot be traced, it either gets cut or gets marked for human review. No exceptions.

**Version control is the improvement loop.** Agents get better through edits to their markdown files, reviewed and merged by humans. Agents never modify themselves. Agents never modify each other. This sounds slow; it is the only way to keep the system accountable across many runs.

**The final human review is load-bearing.** AI output is 85%. The last 15% is the judgment of the person whose name goes on the document. The Council is a tool for drafting quickly and arguing rigorously. It is not a tool for replacing that judgment.

## What this methodology is not

- Not an evaluation framework for AI output quality. We do not score agents. We observe their behavior across runs and edit their prompts.
- Not a guarantee of correctness. The Fact-checker catches numerical mismatches against the briefs. It does not catch errors in the briefs themselves. Primary source review is the reader's responsibility.
- Not a substitute for a subject-matter author. The Council amplifies a human's argument. It does not replace one.
