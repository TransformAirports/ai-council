# Run: {{RUN_TITLE}}

<!--
HOW TO USE THIS FILE

1. Copy this file. Rename the copy to something that describes your thesis — e.g.
   `airline-consolidation.md`, `biometric-risk.md`, `cargo-revenue-collapse.md`.
   Keep it short, kebab-case, and in this directory (`prompts/runs/`).
2. Fill in every section below in plain prose. Delete every `{{...}}` placeholder
   and every HTML comment (like this one) as you go.
3. In Claude Code, say: "run <your-filename>" (without the .md). The Council
   handles the rest and drops the final deliverables into `runs/YYYY-MM-DD-<slug>/`
   a few hours later.

GUIDING PRINCIPLE
The sharper the thesis, the sharper the output. "Topics" produce summaries.
Theses produce arguments. This template is for theses.
-->

## Thesis

<!--
One to three sentences, sharp. State the claim you want the Council to
pressure-test. A good thesis is falsifiable and contested. A bad thesis is
a topic.

Good:  "Regional airline consolidation has gone far enough that the next wave
        of mergers will strand infrastructure the industry just built."
Bad:   "An overview of regional airline trends."
-->

{{WRITE YOUR SHARP CLAIM HERE}}

## Audience

<!--
Who is reading this? The tighter you specify, the tighter the prose.
"General aviation readers" produces generic output. Name the people you imagine
reading this and what they already know.
-->

{{AUDIENCE — for example: "Airport executives, capital planners, and policy
readers. Assume sophistication. Assume skepticism. Assume they have read
McKinsey decks and are tired of them."}}

## Tone

<!--
Adjectives and comparisons. What voice do you want? The Strategist defaults to
narrative long-form — think McPhee, Michael Lewis, Gawande, Tracy Kidder. If
that's what you want, just say "the default narrative voice, extra emphasis on
[whatever you want extra of]." If you want something sharper or more analytical,
name it and name a model.

Three usable registers to pick from or blend:

- Narrative long-form (default). "A beautifully written long-form essay, the
  kind of piece a reader finishes not because they had to but because they
  wanted to. Model: McPhee, Lewis, Gawande, Tracy Kidder. Embed the argument
  in story and specific cases. Vary sentence rhythm. Avoid purple prose."
- Analytical sharp. "Direct. Evidence-dense. Intellectually honest about the
  counter-argument. Slightly provocative but not polemical. Model: Matt Levine
  on aviation, not a consultant thought-leadership piece."
- Formal policy. "Measured, precise, unshowy. The voice of a CRS report or a
  serious GAO analysis written by someone who also cared about language. Model:
  the best of the Brookings and Eno Center long-form."

The first report the Council produced used the "analytical sharp" register and
read as technical. If you want something the reader will want to curl up with,
ask for narrative long-form.
-->

{{TONE — write your register here, or say "the default narrative voice" and
any adjustments}}

## Length

{{FINAL DOCUMENT LENGTH — for example: "8,000-10,000 words for the full report;
~1,100-word executive summary. This is a substantive piece, not a blog post."}}

## What this is NOT

<!--
List what the piece should refuse to be. Without this, the Strategist drifts
toward whichever framing is easiest to write.
-->

- {{NOT A — e.g. "a vendor pitch for any specific technology"}}
- {{NOT B — e.g. "a call for zero infrastructure investment"}}
- {{NOT C — e.g. "a polemic that ignores the genuine reasons for the status quo"}}

## What this IS

- {{IS A — the positive framing of the piece}}
- {{IS B — the specific analytical move that makes the piece credible}}
- {{IS C — the demonstration the piece has to pull off}}

## Operator-specific framing (optional)

<!--
If this run should produce observations tied to a specific airport, authority,
or operator (e.g. MWAA's DCA and IAD; Port Authority's JFK/LGA/EWR; an
unnamed peer large hub), name it here and describe the relevant programs,
decisions, or constraints. If the piece is purely industry-wide, delete this
section and the Strategist will produce an "Implications for the hubs this
thesis applies to" section instead.
-->

{{OPERATOR CONTEXT — or delete this section if the run is industry-wide}}

## Success criteria

<!--
How will you know the run produced a document worth sharing? Two or three
crisp criteria. These are for you at the two human checkpoints, not for the
agents. Keep them specific.
-->

- {{CRITERION A — e.g. "A sophisticated reader cannot dismiss the piece in the first 500 words"}}
- {{CRITERION B — e.g. "The counter-case is presented strongly enough that the reader feels the force of it"}}
- {{CRITERION C — e.g. "Every numerical claim traces to a primary source"}}

## Research agent overrides (optional — leave blank for most runs)

<!--
The Council's eight research agents have defaults tuned for the airport
industry. For most airport theses, those defaults work. Use this section only
if a specific agent should focus on something unusual for this run. Leave
blank otherwise.

If this run needs a fundamentally different set of agents, don't override here —
open a PR against `.claude/agents/` with new agents. See
`docs/how-to-propose-an-agent-change.md`.
-->

- **infrastructure-economist:** {{BLANK = USE DEFAULT}}
- **operations-analyst:** {{BLANK = USE DEFAULT}}
- **technology-scout:** {{BLANK = USE DEFAULT}}
- **contrarian:** {{BLANK = USE DEFAULT}}
- **chief-engineer:** {{BLANK = USE DEFAULT}}
- **airline-commercial-strategist:** {{BLANK = USE DEFAULT}}
- **regulatory-political-analyst:** {{BLANK = USE DEFAULT}}
- **aviation-historian:** {{BLANK = USE DEFAULT}}
- **airport-ceo:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED}}
- **airport-coo:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED}}
- **director-of-public-safety:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED}}
- **airport-emergency-management-director:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED}}
- **emergency-management-consultant:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED}}
- **slacker:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED}}
- **virtual-christian:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED}}
- **architectural-historian:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED}}
- **deep-research:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED — requires OPENAI_API_KEY}}
- **virtual-chris:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED}}
- **virtual-pat:** {{BLANK = USE DEFAULT, OR REMOVE LINE IF NOT SEATED}}
