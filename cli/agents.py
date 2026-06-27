"""Load Council agent definitions from .claude/agents/*.md.

Each agent file has YAML frontmatter (name, description, tools, display_name,
order) and a markdown body that is used as the agent's system prompt. The CLI
uses the metadata for selection UI and the body for execution.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import frontmatter

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"

RESEARCH_AGENT_NAMES: tuple[str, ...] = (
    "infrastructure-economist",
    "operations-analyst",
    "technology-scout",
    "contrarian",
    "chief-engineer",
    "airline-commercial-strategist",
    "regulatory-political-analyst",
    "aviation-historian",
    "airport-ceo",
    "airport-coo",
    "airport-procurement-expert",
    "director-of-public-safety",
    "airport-emergency-management-director",
    "slacker",
    "virtual-christian",
    "architectural-historian",
    "deep-research",
    "virtual-chris",
    "virtual-pat",
)

PROCESS_AGENT_NAMES: tuple[str, ...] = (
    "strategist",
    "red-team",
    "editor",
    "humanizer",
    "fact-checker",
    "presentation-designer",
)

# Supplemental agents — the Council of High Intelligence personas, imported and
# adapted from github.com/0xNyk/council-of-high-intelligence. They are seatable
# research lenses, but kept distinct from the airport-domain roster: opt-in via
# the Custom picker only, never pulled into the "All standard lenses" preset.
SUPPLEMENTAL_AGENT_NAMES: tuple[str, ...] = (
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
)


@dataclass(frozen=True)
class Agent:
    name: str
    display_name: str
    description: str
    tools: tuple[str, ...]
    order: int
    system_prompt: str
    path: Path
    provider: str = "anthropic"        # "anthropic" (Claude SDK) or "openai"
    model_override: str | None = None  # per-agent model from frontmatter

    @property
    def is_research(self) -> bool:
        # Supplemental agents are research-type too (seatable Stage 1 lenses).
        return self.name in RESEARCH_AGENT_NAMES or self.name in SUPPLEMENTAL_AGENT_NAMES

    @property
    def is_supplemental(self) -> bool:
        return self.name in SUPPLEMENTAL_AGENT_NAMES

    @property
    def is_standard_research(self) -> bool:
        return self.name in RESEARCH_AGENT_NAMES

    @property
    def is_process(self) -> bool:
        return self.name in PROCESS_AGENT_NAMES


def _parse_tools(raw: object) -> tuple[str, ...]:
    if raw is None:
        return ()
    if isinstance(raw, list):
        return tuple(str(t).strip() for t in raw if str(t).strip())
    if isinstance(raw, str):
        return tuple(t.strip() for t in raw.split(",") if t.strip())
    return ()


def load_agent(path: Path) -> Agent:
    post = frontmatter.load(path)
    meta = post.metadata
    name = str(meta.get("name") or path.stem).strip()
    return Agent(
        name=name,
        display_name=str(meta.get("display_name") or name).strip(),
        description=str(meta.get("description") or "").strip(),
        tools=_parse_tools(meta.get("tools")),
        order=int(meta.get("order") or 999),
        system_prompt=post.content.strip(),
        path=path,
        provider=str(meta.get("provider") or "anthropic").strip().lower(),
        model_override=(str(meta["model"]).strip() if meta.get("model") else None),
    )


def load_all_agents(agents_dir: Path = AGENTS_DIR) -> list[Agent]:
    if not agents_dir.is_dir():
        raise FileNotFoundError(f"Agents directory not found: {agents_dir}")
    agents = [load_agent(p) for p in sorted(agents_dir.glob("*.md"))]
    return sorted(agents, key=lambda a: (not a.is_research, a.order, a.name))


def research_agents(agents: Iterable[Agent]) -> list[Agent]:
    return [a for a in agents if a.is_research]


def standard_research_agents(agents: Iterable[Agent]) -> list[Agent]:
    """Core airport-domain research lenses, excluding supplemental personas."""
    return [a for a in agents if a.is_standard_research]


def supplemental_agents(agents: Iterable[Agent]) -> list[Agent]:
    return [a for a in agents if a.is_supplemental]


def process_agents(agents: Iterable[Agent]) -> dict[str, Agent]:
    return {a.name: a for a in agents if a.is_process}
