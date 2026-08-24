"""Operator configuration — council.toml at the repo root.

Everything an operator might reasonably want to change without editing Python
lives here: model assignments per role, turn budgets, the default cost
ceiling, and the default output format. The file is optional; missing keys
fall back to the defaults below. The Settings menu reads and writes it.
"""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "council.toml"

# Research and synthesis use Anthropic's rolling Opus alias. It selects the
# newest Opus available to the account and will pick up Opus 5.0 when Anthropic
# exposes that model through Claude Code. The editorial tier — the agents
# that work AFTER the research briefs land (Red Team critique, Editor,
# Humanizer, presentation) — runs on Fable 5 for stronger critique and
# editorial performance. The Fact-checker uses a fresh Sonnet context so the
# final source check is not performed by the Opus writer or the Fable polisher.
DEFAULT_MODELS: dict[str, str] = {
    "context": "opus",
    "research": "opus",
    # Strengthen an argument is a bounded memo workflow. Sonnet handles its
    # focused research wave faster; Opus remains the single argument writer.
    "argument_research": "claude-sonnet-4-6",
    "curation": "opus",
    "creative": "claude-fable-5",
    "synthesis": "opus",
    "argument_synthesis": "opus",
    "critique": "claude-fable-5",
    "executive_review": "opus",
    "editor": "claude-fable-5",
    "humanizer": "claude-fable-5",
    "factcheck": "claude-sonnet-4-6",
    "art_direction": "claude-fable-5",
    "presentation": "claude-fable-5",
    # The mixed-Council Deep Research seat runs through the operator's saved
    # ChatGPT subscription login, never API-key billing.
    "openai_deep_research": "gpt-5.6-sol",
}

MODEL_CHOICES = ["opus", "claude-fable-5", "claude-sonnet-4-6"]

# The ChatGPT-backed Deep Research role is pinned to the same supported Sol
# model used by coherent GPT reports.
OPENAI_DR_CHOICES = ["gpt-5.6-sol"]


def choices_for_role(role: str) -> list[str]:
    return OPENAI_DR_CHOICES if role == "openai_deep_research" else MODEL_CHOICES

# Models that are not currently available. When a saved council.toml names one
# (selected before a block landed, or committed by a teammate), the loader
# silently substitutes the replacement — operators never get a mid-run
# "model not available" error from a stale setting.
# claude-fable-5 was blocked here from 2026-06-10 to 2026-06-24; it is
# available again and back in the defaults above.
BLOCKED_MODELS: dict[str, str] = {
    # This literal model ID is not currently exposed by Claude Code. The Opus
    # alias is the supported forward-compatible route to the latest Opus.
    "claude-opus-5-0": "opus",
    # Historical API-only Deep Research IDs now route to the subscription-
    # authenticated GPT-5.6 Sol seat.
    "gpt-5.5-pro-deep-research": "gpt-5.6-sol",
    "o3-deep-research": "gpt-5.6-sol",
    "o4-mini-deep-research": "gpt-5.6-sol",
}


@dataclass
class Config:
    models: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_MODELS))
    max_turns: int = 80
    default_budget_usd: float = 80.0
    default_format: str = "report"

    def model(self, role: str) -> str:
        return self.models.get(role, DEFAULT_MODELS.get(role, "opus"))


@dataclass(frozen=True)
class BlockedModelSelection:
    """A saved model choice that normal configuration loading will replace."""

    role: str
    configured: str
    replacement: str


@dataclass(frozen=True)
class ConfigInspection:
    """Read-only configuration result with defects preserved for diagnostics."""

    config: Config
    parse_error: str | None = None
    blocked_models: tuple[BlockedModelSelection, ...] = ()


_cached: Config | None = None


def _inspect_config(path: Path, *, persist_rewrites: bool) -> ConfigInspection:
    cfg = Config()
    blocked_models: list[BlockedModelSelection] = []
    if path.is_file():
        try:
            raw = tomllib.loads(path.read_text(encoding="utf-8"))
        except (tomllib.TOMLDecodeError, OSError, UnicodeError) as exc:
            return ConfigInspection(cfg, parse_error=str(exc))
        models = raw.get("models", {})
        if isinstance(models, dict):
            for k, v in models.items():
                if isinstance(v, str) and v.strip():
                    val = v.strip()
                    if val in BLOCKED_MODELS:
                        blocked_models.append(
                            BlockedModelSelection(
                                role=str(k),
                                configured=val,
                                replacement=BLOCKED_MODELS[val],
                            )
                        )
                        val = BLOCKED_MODELS[val]
                    cfg.models[k] = val
        run = raw.get("run", {})
        if isinstance(run, dict):
            if isinstance(run.get("max_turns"), int) and run["max_turns"] > 0:
                cfg.max_turns = run["max_turns"]
            if isinstance(run.get("default_budget_usd"), (int, float)) and run["default_budget_usd"] >= 0:
                cfg.default_budget_usd = float(run["default_budget_usd"])
            if run.get("default_format") in ("report", "article", "brief", "recommendations"):
                cfg.default_format = run["default_format"]
    # Persist the substitution so the next inspection shows clean values.
    # The save path itself calls reload_config(), so guard against recursion.
    if blocked_models and persist_rewrites and path.is_file():
        _write_config(cfg, path)
    return ConfigInspection(cfg, blocked_models=tuple(blocked_models))


def inspect_config(path: Path = CONFIG_PATH) -> ConfigInspection:
    """Parse *path* without writing it and retain errors for ``--doctor``.

    Normal Council loading intentionally repairs known stale model IDs.  A
    diagnostic command must not do that behind the operator's back, so this
    separate path reports the pending substitutions while returning the
    resolved in-memory configuration.
    """

    return _inspect_config(path, persist_rewrites=False)


def load_config(path: Path = CONFIG_PATH, *, persist_rewrites: bool = True) -> Config:
    """Load configuration, preserving the historical auto-rewrite by default."""

    return _inspect_config(path, persist_rewrites=persist_rewrites).config


def _write_config(cfg: Config, path: Path) -> None:
    """Internal writer that does NOT touch the module-level cache."""
    lines = ["# Council operator configuration — edited via Settings in ./council", ""]
    lines.append("[models]")
    for k, v in cfg.models.items():
        lines.append(f'{k} = "{v}"')
    lines += [
        "",
        "[run]",
        f"max_turns = {cfg.max_turns}",
        f"default_budget_usd = {cfg.default_budget_usd:g}",
        f'default_format = "{cfg.default_format}"',
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def get_config() -> Config:
    global _cached
    if _cached is None:
        _cached = load_config()
    return _cached


def reload_config() -> Config:
    global _cached
    _cached = load_config()
    return _cached


def save_config(cfg: Config, path: Path = CONFIG_PATH) -> Path:
    _write_config(cfg, path)
    reload_config()
    return path
