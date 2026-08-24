"""Run-level model choices for a coherent Council report.

New report runs choose one top-tier model for every research and process
role.  Older run prompts omit this field and retain the historical role-based
routing from ``council.toml`` so their paid artifacts remain safely resumable.
"""
from __future__ import annotations

from dataclasses import dataclass


CLAUDE_FABLE = "claude-fable-5"
GPT_5_6_SOL = "gpt-5.6-sol"
DEFAULT_COUNCIL_MODEL = CLAUDE_FABLE


@dataclass(frozen=True)
class CouncilModel:
    id: str
    label: str
    provider: str
    description: str


COUNCIL_MODELS: tuple[CouncilModel, ...] = (
    CouncilModel(
        id=CLAUDE_FABLE,
        label="Claude Fable 5",
        provider="anthropic",
        description="Narrative judgment and editorial voice",
    ),
    CouncilModel(
        id=GPT_5_6_SOL,
        label="GPT-5.6 Sol",
        provider="openai",
        description="Frontier reasoning on your ChatGPT plan",
    ),
)

_BY_ID = {item.id: item for item in COUNCIL_MODELS}


def council_model(model_id: str | None) -> CouncilModel | None:
    """Resolve one explicit run model; empty means legacy role routing."""

    value = str(model_id or "").strip()
    if not value:
        return None
    try:
        return _BY_ID[value]
    except KeyError as exc:
        choices = ", ".join(item.id for item in COUNCIL_MODELS)
        raise ValueError(
            f"Unknown Council model {value!r}; choose one of: {choices}."
        ) from exc


def council_model_payload() -> list[dict[str, str]]:
    return [
        {
            "id": item.id,
            "label": item.label,
            "provider": item.provider,
            "description": item.description,
        }
        for item in COUNCIL_MODELS
    ]


__all__ = [
    "CLAUDE_FABLE",
    "COUNCIL_MODELS",
    "CouncilModel",
    "DEFAULT_COUNCIL_MODEL",
    "GPT_5_6_SOL",
    "council_model",
    "council_model_payload",
]
