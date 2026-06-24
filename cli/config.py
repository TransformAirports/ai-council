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

DEFAULT_MODELS: dict[str, str] = {
    "research": "claude-opus-4-8",
    "synthesis": "claude-opus-4-8",
    "critique": "claude-opus-4-8",
    "editor": "claude-opus-4-8",
    "humanizer": "claude-opus-4-8",
    "factcheck": "claude-opus-4-8",
    "presentation": "claude-opus-4-8",
    # OpenAI's deep-research model. Use `o3-deep-research` for the heavyweight
    # long-horizon sweep (slower, more expensive); switch to
    # `o4-mini-deep-research` from Settings for a faster/cheaper pass.
    "openai_deep_research": "o3-deep-research",
}

MODEL_CHOICES = ["claude-opus-4-8", "claude-sonnet-4-6"]

# Models that are not currently available to this account. When a saved
# council.toml still names one of these (because it was selected before the
# block landed, or because a teammate's config got committed), the loader
# silently substitutes the value below — operators never get a mid-run
# "model not available" error from a stale setting.
BLOCKED_MODELS: dict[str, str] = {
    "claude-fable-5": "claude-opus-4-8",
    # `gpt-5.5-pro-deep-research` was a placeholder ID that never existed in the
    # OpenAI catalog. Real Deep Research models are `o3-deep-research` (heavy)
    # and `o4-mini-deep-research` (light). Auto-rewrite the placeholder.
    "gpt-5.5-pro-deep-research": "o3-deep-research",
}


@dataclass
class Config:
    models: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_MODELS))
    max_turns: int = 80
    default_budget_usd: float = 80.0
    default_format: str = "report"

    def model(self, role: str) -> str:
        return self.models.get(role, DEFAULT_MODELS.get(role, "claude-opus-4-8"))


_cached: Config | None = None


def load_config(path: Path = CONFIG_PATH) -> Config:
    cfg = Config()
    rewrote = False
    if path.is_file():
        try:
            raw = tomllib.loads(path.read_text(encoding="utf-8"))
        except (tomllib.TOMLDecodeError, OSError):
            return cfg
        models = raw.get("models", {})
        if isinstance(models, dict):
            for k, v in models.items():
                if isinstance(v, str) and v.strip():
                    val = v.strip()
                    if val in BLOCKED_MODELS:
                        val = BLOCKED_MODELS[val]
                        rewrote = True
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
    if rewrote and path.is_file():
        _write_config(cfg, path)
    return cfg


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
