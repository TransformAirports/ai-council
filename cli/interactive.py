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
from cli.council_models import COUNCIL_MODELS, DEFAULT_COUNCIL_MODEL

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
    "Fascinating, vivid, and argument-led. Open with a concrete scene, case, "
    "or surprise that earns the reader's attention, then let the evidence "
    "change how they see the subject. Write with the clarity and momentum of "
    "an excellent magazine feature, not a consulting assignment or technical paper."
)

DEFAULT_LENGTH = (
    "A 1,500–2,000-word narrative feature — one continuous argument, no appendices "
    "or decision-card catalog."
)

# Output formats the operator can pick from. The chosen string is written into
# the run file's Length section, which the Strategist and Editor read. The
# format KEY also travels through the run file so the publisher can style the
# polished document appropriately (see FORMAT_KEYS and cli/publish.py).
OUTPUT_FORMATS: dict[str, str] = {
    "Narrative Feature (1,500–2,000 words)": (
        "A 1,500–2,000-word narrative feature — one continuous argument, no appendices "
        "or separate executive summary. Make it fascinating, specific, and enjoyable "
        "to read while preserving the evidence trail."
    ),
    "Full Research Report (4,000–6,000 words)": (
        "4,000–6,000 words for the full research report; ~600-word executive summary."
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
    "Narrative Feature (1,500–2,000 words)": "article",
    "Full Research Report (4,000–6,000 words)": "report",
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

# Balanced airport council. This is a deliberate coverage preset—not a ranking
# inferred from mentions in past final drafts. Evidence-lineage telemetry can
# inform future changes once enough comparable, human-scored runs exist.
PRESET_DEFAULT: tuple[str, ...] = (
    "technology-scout",
    "quantitative-analyst",
    "contrarian",
    "airport-ceo",
    "airport-coo",
    "infrastructure-economist",
    "operations-analyst",
    "airline-commercial-strategist",
)

PRESET_OPERATIONAL: tuple[str, ...] = (
    "operations-analyst",
    "quantitative-analyst",
    "chief-engineer",
    "technology-scout",
    "airport-coo",
    "director-of-public-safety",
    "airport-emergency-management-director",
)

PRESET_STRATEGIC: tuple[str, ...] = (
    "airport-ceo",
    "quantitative-analyst",
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
        "quantitative-analyst",
        "chief-engineer",
        "technology-scout",
        "architectural-historian",
    ]),
    ("Executive Leadership", [
        "airport-ceo",
        "airport-coo",
        "airport-procurement-expert",
        "regulatory-political-analyst",
    ]),
    ("Public Safety & Emergency Management", [
        "director-of-public-safety",
        "airport-emergency-management-director",
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
    # Supplemental personas (Council of High Intelligence). Listed last and
    # never part of the "All standard lenses" preset — seat them deliberately.
    ("Supplemental — Council of High Intelligence", [
        "council-ada",
        "council-aristotle",
        "council-aurelius",
        "council-feynman",
        "council-kahneman",
        "council-karpathy",
        "council-lao-tzu",
        "council-machiavelli",
        "council-meadows",
        "council-munger",
        "council-musashi",
        "council-rams",
        "council-socrates",
        "council-sun-tzu",
        "council-sutskever",
        "council-taleb",
        "council-torvalds",
        "council-watts",
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
    lines_of_inquiry: list[str] = field(default_factory=list)
    is_not: list[str] = field(default_factory=list)
    is_yes: list[str] = field(default_factory=list)
    operator_context: str = ""
    decision_frame_enabled: bool = False
    decision_required: str = ""
    decision_owner: str = ""
    time_horizon: str = ""
    approval_path: str = ""
    success_measure: str = ""
    success_criteria: list[str] = field(default_factory=list)
    selected_research_agents: list[str] = field(default_factory=list)
    agent_overrides: dict[str, str] = field(default_factory=dict)
    want_pptx: bool = False
    deck_mode: str = "executive_briefing"
    output_format: str = "article"  # report | article | brief | recommendations
    source_paths: list[str] = field(default_factory=list)  # readable paths for sources
    # Empty is reserved for legacy prompts that used role-by-role routing.
    council_model: str = ""


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
        # "All standard" = core airport-domain lenses. The long-horizon Deep
        # Research seat and supplemental personas remain deliberate Custom
        # opt-ins, so an unexpectedly huge run never happens by accident.
        return [
            a.name for a in research
            if a.provider == "anthropic" and not a.is_supplemental
        ]
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
            if len(short) > 100:
                short = short[:97] + "..."
            title = f"{agent.display_name} — {short}"
            choices.append(
                questionary.Choice(
                    title=title,
                    value=name,
                    # Supplemental personas are opt-in so Custom starts from
                    # the standard roster. The run-level model applies later.
                    checked=not agent.is_supplemental,
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

    # 6. One coherent model for the complete report pipeline.
    console.print()
    model_labels = {
        f"{item.label} — {item.description}": item.id
        for item in COUNCIL_MODELS
    }
    selected_model_label = questionary.select(
        "Council model (used by every report role):",
        choices=list(model_labels),
        default=next(
            label
            for label, model_id in model_labels.items()
            if model_id == DEFAULT_COUNCIL_MODEL
        ),
    ).ask()
    if selected_model_label is None:
        raise KeyboardInterrupt
    selected_council_model = model_labels[selected_model_label]

    # 7. Council preset
    console.print()
    research = research_agents(all_agents)
    standard_count = len([
        a for a in research if a.provider == "anthropic" and not a.is_supplemental
    ])
    default_count = len([n for n in PRESET_DEFAULT if n in {a.name for a in research}])
    preset_options = [
        f"All standard lenses ({standard_count} agents)",
        f"Balanced {default_count} (evidence, operations, commercial, opposition)",
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

    # The companion-deck choice lives on the pre-flight screen (one place to
    # adjust everything) rather than as another question here.
    want_pptx = False

    # Map the simplified inputs onto the run-file structure the strategist,
    # red-team, editor, and fact-checker already know how to read.
    is_yes = DEFAULT_IS_YES.copy()
    is_not = avoid_items if avoid_items else DEFAULT_IS_NOT.copy()
    success_criteria = DEFAULT_SUCCESS_CRITERIA.copy()

    return RunSpec(
        title=title,
        slug=slug,
        thesis=thesis,
        audience=DEFAULT_AUDIENCE,
        tone=DEFAULT_TONE,
        length=length,
        lines_of_inquiry=scope_items,
        is_not=is_not,
        is_yes=is_yes,
        operator_context="",
        success_criteria=success_criteria,
        selected_research_agents=selected,
        agent_overrides={},
        want_pptx=want_pptx,
        output_format=output_format,
        council_model=selected_council_model,
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
            f"[bold]Model[/bold]\n{spec.council_model or 'legacy role routing'}\n\n"
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
