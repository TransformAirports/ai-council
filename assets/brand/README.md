# Transform Airports Council design system

This folder is the single source of truth for reader-facing Council artifacts.
`design-system.json` contains the tokens that Word and PowerPoint production
must follow. `visual-brief.schema.json` defines the planning contract between
the final fact-checked argument and presentation production.

## Output modes

### Board decision (`board_decision`)

- 8-12 slides.
- Built to support a speaker and secure a decision.
- One claim per slide, low text density, one signature visual.
- Close on the exact approval, direction, or next step required.

### Executive briefing (`executive_briefing`)

- 12-18 slides.
- Built to be presented or read without a technical appendix.
- Includes the counter-case, implementation sequence, and a sources slide.

### Technical read-ahead (`technical_read_ahead`)

- 15-25 slides.
- Evidence-dense reference material.
- Calculations, assumptions, data definitions, primary-source excerpts, and
  sensitivity cases belong here rather than on board slides.
- Appendix typography may be smaller than the main deck but never below 12 pt;
  sources never below 9 pt.

## Visual standard

Use visuals to explain evidence, not to decorate empty space. Preferred forms
are airport-specific maps, annotated terminal or airfield plans, throughput and
cost charts, passenger or baggage flows, implementation timelines, and direct
excerpts from authoritative source material.

Every deck must have one signature visual: the image, map, chart, or diagram an
executive can recall and redraw after the meeting. Every quantitative visual
must name the unit, denominator, time period, and source. The visual brief binds
the signature exhibit to one exact slide; the deck names its primary exhibit
with the reserved `SIGNATURE VISUAL —` shape prefix so QA can verify placement.

## Reader-facing hygiene

Final artifacts never expose filenames, agent names, internal stage labels,
legacy `[Source: ...]` tags, prompt language, or unresolved production notes.
Run `python -m cli.presentation_qa <deck.pptx>` for structural checks. Client
release also requires a mode-specific render, full-size review of every slide,
montage review, and a passing hash-bound visual-inspection receipt. Word
artifacts are checked through `cli.publishing_quality.qa_docx`, rendered page
by page, inspected individually and as a montage, and released only with a
passing hash-bound page-inspection receipt.
