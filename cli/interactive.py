"""Interactive prompt flow for assembling a Council run.

Collects everything the existing `prompts/runs/_template.md` expects, plus a
multi-select of which research agents to include on the Council for this run.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import questionary
from rich.console import Console
from rich.panel import Panel
from slugify import slugify

from cli.agents import Agent, research_agents

console = Console()


TONE_REGISTERS: dict[str, str] = {
    "Narrative long-form (default)": (
        "A beautifully written long-form essay, the kind of piece a reader finishes "
        "not because they had to but because they wanted to. Model: McPhee, Lewis, "
        "Gawande, Tracy Kidder. Embed the argument in story and specific cases. "
        "Vary sentence rhythm. Avoid purple prose."
    ),
    "Analytical sharp": (
        "Direct. Evidence-dense. Intellectually honest about the counter-argument. "
        "Slightly provocative but not polemical. Model: Matt Levine on aviation, "
        "not a consultant thought-leadership piece."
    ),
    "Formal policy": (
        "Measured, precise, unshowy. The voice of a CRS report or a serious GAO "
        "analysis written by someone who also cared about language. Model: the "
        "best of the Brookings and Eno Center long-form."
    ),
}


@dataclass
class RunSpec:
    title: str
    slug: str
    thesis: str
    audience: str
    tone: str
    length: str
    is_not: list[str] = field(default_factory=list)
    is_yes: list[str] = field(default_factory=list)
    operator_context: str = ""
    success_criteria: list[str] = field(default_factory=list)
    selected_research_agents: list[str] = field(default_factory=list)
    agent_overrides: dict[str, str] = field(default_factory=dict)


def _ask(text: str, multiline: bool = False, default: str = "") -> str:
    if multiline:
        result = questionary.text(
            text + "  (press Esc then Enter to submit)",
            multiline=True,
            default=default,
        ).ask()
    else:
        result = questionary.text(text, default=default).ask()
    if result is None:
        raise KeyboardInterrupt
    return result.strip()


def _ask_list(text: str, min_items: int = 1) -> list[str]:
    items: list[str] = []
    console.print(f"[dim]{text} Enter blank line to finish.[/dim]")
    n = 1
    while True:
        line = questionary.text(f"  {n}.").ask()
        if line is None:
            raise KeyboardInterrupt
        line = line.strip()
        if not line:
            if len(items) >= min_items:
                return items
            console.print(f"[yellow]Need at least {min_items} entry.[/yellow]")
            continue
        items.append(line)
        n += 1


def collect_run_spec(all_agents: list[Agent]) -> RunSpec:
    console.print(
        Panel.fit(
            "[bold]Transform Airports AI Council[/bold]\n"
            "Let's assemble a new run. Sharp thesis in, sharp report out.",
            border_style="cyan",
        )
    )

    title = _ask("Run title (short headline)")
    default_slug = slugify(title)
    slug = _ask("Slug for filenames (kebab-case)", default=default_slug)
    slug = slugify(slug) or default_slug

    console.print()
    console.print("[bold]Thesis[/bold] — one to three sentences, sharp, falsifiable.")
    thesis = _ask("Thesis", multiline=True)

    console.print()
    console.print("[bold]Audience[/bold] — name the readers and what they already know.")
    audience = _ask(
        "Audience",
        multiline=True,
        default=(
            "Airport executives, capital planners, and policy readers. "
            "Assume sophistication, skepticism, and that they have read McKinsey decks."
        ),
    )

    console.print()
    tone_choice = questionary.select(
        "Tone register:",
        choices=list(TONE_REGISTERS.keys()) + ["Custom"],
    ).ask()
    if tone_choice is None:
        raise KeyboardInterrupt
    if tone_choice == "Custom":
        tone = _ask("Describe the voice you want", multiline=True)
    else:
        tone = TONE_REGISTERS[tone_choice]

    console.print()
    length = _ask(
        "Length",
        default="8,000–10,000 words for the full report; ~1,100-word executive summary.",
    )

    console.print()
    console.print("[bold]What this is NOT[/bold]")
    is_not = _ask_list("List what the piece should refuse to be (2–4 entries).", min_items=2)

    console.print()
    console.print("[bold]What this IS[/bold]")
    is_yes = _ask_list("List the positive framing (2–4 entries).", min_items=2)

    console.print()
    operator_context = _ask(
        "Operator context (optional — airport/authority specifics). Blank for industry-wide.",
        multiline=True,
    )

    console.print()
    console.print("[bold]Success criteria[/bold]")
    success_criteria = _ask_list("How you'll know the run produced something worth sharing (2–3).", min_items=2)

    console.print()
    console.print("[bold]Council composition[/bold] — pick which research agents sit on this run.")
    research = research_agents(all_agents)
    choices = [
        questionary.Choice(
            title=f"{a.display_name} — {a.description.splitlines()[0][:90]}",
            value=a.name,
            checked=True,
        )
        for a in research
    ]
    selected = questionary.checkbox(
        "Space to toggle, Enter to confirm:",
        choices=choices,
    ).ask()
    if selected is None:
        raise KeyboardInterrupt
    if not selected:
        console.print("[yellow]At least one research agent is required.[/yellow]")
        return collect_run_spec(all_agents)

    overrides: dict[str, str] = {}
    if questionary.confirm(
        "Any agent-specific focus overrides for this run?", default=False
    ).ask():
        for name in selected:
            override = _ask(f"  Override for {name} (blank = default)")
            if override:
                overrides[name] = override

    return RunSpec(
        title=title,
        slug=slug,
        thesis=thesis,
        audience=audience,
        tone=tone,
        length=length,
        is_not=is_not,
        is_yes=is_yes,
        operator_context=operator_context,
        success_criteria=success_criteria,
        selected_research_agents=selected,
        agent_overrides=overrides,
    )


def confirm_spec(spec: RunSpec) -> bool:
    console.print()
    console.print(
        Panel(
            f"[bold]{spec.title}[/bold]\n"
            f"[dim]slug:[/dim] {spec.slug}\n\n"
            f"[bold]Thesis[/bold]\n{spec.thesis}\n\n"
            f"[bold]Council ({len(spec.selected_research_agents)} research agents)[/bold]\n"
            + "\n".join(f"  • {n}" for n in spec.selected_research_agents),
            border_style="green",
            title="Ready to run",
        )
    )
    return bool(
        questionary.confirm(
            "Write run file and start the Council?", default=True
        ).ask()
    )
