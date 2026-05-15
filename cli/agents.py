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
    "director-of-public-safety",
    "airport-emergency-management-director",
    "emergency-management-consultant",
    "slacker",
    "virtual-christian",
)

PROCESS_AGENT_NAMES: tuple[str, ...] = (
    "strategist",
    "red-team",
    "editor",
    "fact-checker",
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

    @property
    def is_research(self) -> bool:
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
    )


def load_all_agents(agents_dir: Path = AGENTS_DIR) -> list[Agent]:
    if not agents_dir.is_dir():
        raise FileNotFoundError(f"Agents directory not found: {agents_dir}")
    agents = [load_agent(p) for p in sorted(agents_dir.glob("*.md"))]
    return sorted(agents, key=lambda a: (not a.is_research, a.order, a.name))


def research_agents(agents: Iterable[Agent]) -> list[Agent]:
    return [a for a in agents if a.is_research]


def process_agents(agents: Iterable[Agent]) -> dict[str, Agent]:
    return {a.name: a for a in agents if a.is_process}
