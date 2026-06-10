"""Interactive prompt flow for assembling a Council run — simplified.

Three required prompts: title, thesis, council preset. Two optional ones:
scope and avoid. Audience, tone, length use sensible defaults the operator can
override by editing the generated run file. The five-preset council picker
replaces the prior agent-by-agent checkbox.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

import questionary
from rich.console import Console
from rich.panel import Panel
from slugify import slugify

from cli.agents import Agent, research_agents

console = Console()


# ----------------------------------------------------------------------------
# Defaults — used when the user does not explicitly override them. All of
# these end up written into the run file and the operator can edit them by
# hand before launch.
# ----------------------------------------------------------------------------

DEFAULT_AUDIENCE = (
    "Airport executives, capital planners, and policy readers. Assume "
    "sophistication, skepticism, and that they have read McKinsey decks "
    "and are tired of them."
)

DEFAULT_TONE = (
    "Analytical sharp. Direct. Evidence-dense. Intellectually honest about "
    "the counter-argument. Slightly provocative but not polemical. Model: "
    "Matt Levine on aviation, not a consultant thought-leadership piece."
)

DEFAULT_LENGTH = (
    "4,000–6,000 words for the full research report; ~1,100-word executive summary."
)

# Output formats the operator can pick from. The chosen string is written into
# the run file's Length section, which the Strategist and Editor read. The
# format KEY also travels through the run file so the publisher can style the
# polished document appropriately (see FORMAT_KEYS and cli/publish.py).
OUTPUT_FORMATS: dict[str, str] = {
    "Full Research Report (4,000–6,000 words)": (
        "4,000–6,000 words for the full research report; ~1,100-word executive summary."
    ),
    "Long-Form Article (1,500–2,000 words)": (
        "A 1,500–2,000-word long-form article — one continuous argument, no appendices; "
        "~400-word executive summary."
    ),
    "Brief (700–1,000 words)": (
        "A 700–1,000-word brief: the thesis, the three strongest pieces of evidence, "
        "the counter-case in one paragraph, and the bottom line. No executive summary."
    ),
    "Concise recommendations": (
        "A concise set of numbered, actionable recommendations (400–700 words total), "
        "each with a one-sentence evidentiary basis, preceded by a single framing "
        "paragraph. No executive summary."
    ),
}

# Stable keys for each format label — written into the run file and read by
# the publisher to pick the right document treatment.
FORMAT_KEYS: dict[str, str] = {
    "Full Research Report (4,000–6,000 words)": "report",
    "Long-Form Article (1,500–2,000 words)": "article",
    "Brief (700–1,000 words)": "brief",
    "Concise recommendations": "recommendations",
}

DEFAULT_IS_YES = [
    "A sharp, evidence-driven argument that earns its conclusions",
    "An honest steelman of the strongest counter-case",
]

DEFAULT_IS_NOT = [
    "A vendor pitch for any specific platform or product",
    "A polemic that ignores the genuine reasons for the status quo",
]

DEFAULT_SUCCESS_CRITERIA = [
    "A sophisticated reader cannot dismiss the piece in the first 500 words",
    "Every numerical claim traces to a primary source or analyst construction",
]


# ----------------------------------------------------------------------------
# Council presets.
# ----------------------------------------------------------------------------

# Audit-tuned default council. Each agent in this list returned at least 2.8
# citations per 1,000 brief words across the first four archived runs (see
# `council --audit` for current scores). The agents dropped from the prior
# "Default Eight" roster — chief-engineer, aviation-historian, and
# regulatory-political-analyst — wrote substantial briefs but the Strategist
# rarely surfaced their content. Re-run the audit periodically and update this
# list as the data evolves; this is meant to be tuned, not frozen.
PRESET_DEFAULT: tuple[str, ...] = (
    "technology-scout",              # 14.0 cites / 1k brief words
    "contrarian",                    # 13.1
    "airport-ceo",                   # 9.8
    "airport-coo",                   # 8.3
    "infrastructure-economist",      # 5.5
    "operations-analyst",            # 4.9
    "airline-commercial-strategist", # 2.8
)

PRESET_OPERATIONAL: tuple[str, ...] = (
    "operations-analyst",
    "chief-engineer",
    "technology-scout",
    "airport-coo",
    "director-of-public-safety",
    "airport-emergency-management-director",
)

PRESET_STRATEGIC: tuple[str, ...] = (
    "airport-ceo",
    "airport-coo",
    "regulatory-political-analyst",
    "airline-commercial-strategist",
    "infrastructure-economist",
    "aviation-historian",
)

AGENT_GROUPS: list[tuple[str, list[str]]] = [
    ("Economics & Industry", [
        "infrastructure-economist",
        "airline-commercial-strategist",
        "aviation-historian",
        "contrarian",
    ]),
    ("Operations & Engineering", [
        "operations-analyst",
        "chief-engineer",
        "technology-scout",
        "architectural-historian",
    ]),
    ("Executive Leadership", [
        "airport-ceo",
        "airport-coo",
        "regulatory-political-analyst",
    ]),
    ("Public Safety & Emergency Management", [
        "director-of-public-safety",
        "airport-emergency-management-director",
        "emergency-management-consultant",
    ]),
    ("Out-of-the-Box Thinkers", [
        "slacker",
        "virtual-christian",
        "virtual-chris",
        "virtual-pat",
    ]),
    ("Extended Research", [
        "deep-research",
    ]),
]


# ----------------------------------------------------------------------------
# RunSpec — same shape the orchestrator and run-file writer expect.
# ----------------------------------------------------------------------------

@dataclass
class RunSpec:
    title: str
    slug: str
    thesis: str
    audience: str = DEFAULT_AUDIENCE
    tone: str = DEFAULT_TONE
    length: str = DEFAULT_LENGTH
    is_not: list[str] = field(default_factory=list)
    is_yes: list[str] = field(default_factory=list)
    operator_context: str = ""
    success_criteria: list[str] = field(default_factory=list)
    selected_research_agents: list[str] = field(default_factory=list)
    agent_overrides: dict[str, str] = field(default_factory=dict)
    want_pptx: bool = False
    output_format: str = "report"  # report | article | brief | recommendations


# ----------------------------------------------------------------------------
# Input helpers.
# ----------------------------------------------------------------------------

def _ask(text: str, default: str = "") -> str:
    result = questionary.text(text, default=default).ask()
    if result is None:
        raise KeyboardInterrupt
    return result.strip()


def _ask_multiline(label: str, optional: bool = False) -> str:
    hint = " (paste OK; press Esc then Enter to submit"
    if optional:
        hint += "; leave empty to skip"
    hint += ")"
    result = questionary.text(label + hint, multiline=True).ask()
    if result is None:
        raise KeyboardInterrupt
    return result.strip()


def _parse_bullets(text: str) -> list[str]:
    """Turn a pasted block into a list of items.

    Strips common bullet markers (-, *, •, ·) and `1.`/`1)` number prefixes.
    Drops blank lines. Each non-empty line becomes one item. If the user
    pasted prose with no bullets, the whole block becomes a single item.
    """
    if not text:
        return []
    items: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        line = re.sub(r"^[-*•·]\s*", "", line)
        line = re.sub(r"^\d+[.)]\s*", "", line)
        if line:
            items.append(line)
    return items


def _apply_preset(preset: str, research: list[Agent]) -> list[str]:
    available = {a.name for a in research}
    if preset.startswith("All"):
        # "All" means all Claude-native lenses. Provider-gated agents (the
        # OpenAI Deep Research lens needs OPENAI_API_KEY) are opt-in via Custom
        # so a missing key never breaks the default path.
        return [a.name for a in research if a.provider == "anthropic"]
    if preset.startswith("Default"):
        return [n for n in PRESET_DEFAULT if n in available]
    if preset.startswith("Operational"):
        return [n for n in PRESET_OPERATIONAL if n in available]
    if preset.startswith("Strategic"):
        return [n for n in PRESET_STRATEGIC if n in available]
    return [a.name for a in research]


def _custom_council_picker(research: list[Agent]) -> list[str]:
    """Grouped checkbox UI for picking individual agents."""
    by_name = {a.name: a for a in research}
    choices: list = []
    for group_label, names in AGENT_GROUPS:
        choices.append(questionary.Separator(f"── {group_label} ──"))
        for name in names:
            agent = by_name.get(name)
            if agent is None:
                continue
            short = agent.description.splitlines()[0].strip()
            if len(short) > 80:
                short = short[:77] + "..."
            gated = agent.provider != "anthropic"
            title = f"{agent.display_name} — {short}"
            if gated:
                title = f"{agent.display_name} (requires OPENAI_API_KEY) — {short}"
            choices.append(
                questionary.Choice(
                    title=title,
                    value=name,
                    checked=not gated,
                )
            )
    selected = questionary.checkbox(
        "Space to toggle, Enter to confirm:",
        choices=choices,
    ).ask()
    if selected is None:
        raise KeyboardInterrupt
    return selected


# ----------------------------------------------------------------------------
# Main entry point.
# ----------------------------------------------------------------------------

def choose_mode() -> str:
    """Top-level mode select. Returns 'new' or 'revise'."""
    answer = questionary.select(
        "What would you like to do?",
        choices=[
            "Create a new report",
            "Revise an existing report",
        ],
    ).ask()
    if answer is None:
        raise KeyboardInterrupt
    return "revise" if answer.startswith("Revise") else "new"


def collect_run_spec(all_agents: list[Agent]) -> RunSpec:
    console.print(
        Panel.fit(
            "[bold]Transform Airports AI Council[/bold]\n"
            "Three prompts plus a council pick. Sharp thesis in, sharp report out.",
            border_style="cyan",
        )
    )

    # 1. Title
    title = _ask("Run title (short headline)")
    if not title:
        raise RuntimeError("A title is required.")
    slug = slugify(title)

    # 2. Thesis
    console.print()
    console.print("[bold]Thesis[/bold] — one to three sentences, sharp and falsifiable.")
    thesis = _ask_multiline("Thesis")
    if not thesis:
        raise RuntimeError("A thesis is required.")

    # 3. Scope (optional)
    console.print()
    console.print(
        "[bold]Scope[/bold] — what should the council address? "
        "Paste a bulleted list, or leave empty to let the council scope itself."
    )
    scope_text = _ask_multiline("Scope", optional=True)
    scope_items = _parse_bullets(scope_text)

    # 4. Avoid (optional)
    console.print()
    console.print(
        "[bold]Avoid[/bold] — what should this piece refuse to be? "
        "Paste a list, or leave empty for the standard guardrails."
    )
    avoid_text = _ask_multiline("Avoid", optional=True)
    avoid_items = _parse_bullets(avoid_text)

    # 5. Output format
    console.print()
    format_choice = questionary.select(
        "Output format:",
        choices=list(OUTPUT_FORMATS.keys()),
    ).ask()
    if format_choice is None:
        raise KeyboardInterrupt
    length = OUTPUT_FORMATS[format_choice]
    output_format = FORMAT_KEYS[format_choice]

    # 6. Council preset
    console.print()
    research = research_agents(all_agents)
    standard_count = len([a for a in research if a.provider == "anthropic"])
    default_count = len([n for n in PRESET_DEFAULT if n in {a.name for a in research}])
    preset_options = [
        f"All standard lenses ({standard_count} agents)",
        f"Default {default_count} (audit-tuned contributors)",
        "Operational focus (Ops, Engineering, COO, Public Safety, EM)",
        "Strategic focus (CEO, COO, Regulatory, Commercial, Econ, History)",
        "Custom — pick from grouped checklist (includes Deep Research)",
    ]
    preset_choice = questionary.select(
        "Council composition:",
        choices=preset_options,
    ).ask()
    if preset_choice is None:
        raise KeyboardInterrupt
    if preset_choice.startswith("Custom"):
        selected = _custom_council_picker(research)
    else:
        selected = _apply_preset(preset_choice, research)
    if not selected:
        console.print("[yellow]At least one research agent is required. Starting over.[/yellow]")
        return collect_run_spec(all_agents)

    # 7. Companion PowerPoint
    console.print()
    want_pptx = bool(
        questionary.confirm(
            "Also generate a companion executive PowerPoint?", default=False
        ).ask()
    )

    # Map the simplified inputs onto the run-file structure the strategist,
    # red-team, editor, and fact-checker already know how to read.
    is_yes = (
        [scope_items[0]] + DEFAULT_IS_YES
        if scope_items
        else DEFAULT_IS_YES.copy()
    )
    is_not = avoid_items if avoid_items else DEFAULT_IS_NOT.copy()
    success_criteria = scope_items if scope_items else DEFAULT_SUCCESS_CRITERIA.copy()

    return RunSpec(
        title=title,
        slug=slug,
        thesis=thesis,
        audience=DEFAULT_AUDIENCE,
        tone=DEFAULT_TONE,
        length=length,
        is_not=is_not,
        is_yes=is_yes,
        operator_context="",
        success_criteria=success_criteria,
        selected_research_agents=selected,
        agent_overrides={},
        want_pptx=want_pptx,
        output_format=output_format,
    )


def confirm_spec(spec: RunSpec) -> bool:
    console.print()
    thesis_preview = (
        spec.thesis if len(spec.thesis) <= 280 else spec.thesis[:280] + "…"
    )
    council_preview = ", ".join(spec.selected_research_agents[:8])
    if len(spec.selected_research_agents) > 8:
        council_preview += f", +{len(spec.selected_research_agents) - 8} more"
    console.print(
        Panel(
            f"[bold]{spec.title}[/bold]\n"
            f"[dim]slug:[/dim] {spec.slug}\n\n"
            f"[bold]Thesis[/bold]\n{thesis_preview}\n\n"
            f"[bold]Council ({len(spec.selected_research_agents)} agents)[/bold]\n"
            f"{council_preview}",
            border_style="green",
            title="Ready to run",
        )
    )
    return bool(
        questionary.confirm(
            "Write run file and start the Council?", default=True
        ).ask()
    )
