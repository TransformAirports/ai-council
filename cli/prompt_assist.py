"""Bounded AI assistance for drafting a Council run prompt.

This module deliberately sits outside the report orchestrator.  It turns rough
operator input into structured wizard fields, but it cannot create a run file,
select agents, change a budget, or launch a report.  The model receives no
tools, MCP servers, project settings, or skills.
"""
from __future__ import annotations

import json
import math
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Awaitable, Callable


REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_COACH_PATH = REPO_ROOT / "prompts" / "prompt-coach.md"

PROMPT_ASSIST_MAX_TURNS = 1
PROMPT_ASSIST_MAX_BUDGET_USD = 1.50
PROMPT_ASSIST_MAX_INPUT_CHARS = 20_000
PROMPT_ASSIST_MAX_OUTPUT_TOKENS = 4_000
PROMPT_ASSIST_MODEL = "gpt-5.6-sol"
PROMPT_ASSIST_REASONING_EFFORT = "medium"
# Current promotional GPT-5.6 Sol token prices through at least 2026-11-21.
# Cost is labeled as an estimate because OpenAI may change pricing independently
# of this local app. https://developers.openai.com/api/docs/models/gpt-5.6-sol
PROMPT_ASSIST_INPUT_USD_PER_MILLION = 4.0
PROMPT_ASSIST_OUTPUT_USD_PER_MILLION = 20.0

ALLOWED_OUTPUT_FORMATS = frozenset(
    {"report", "article", "brief", "recommendations"}
)

# These are the only wizard fields a model may draft.  Deliberately absent:
# agents, provider choices, presentation settings, review controls, and budget.
TEXT_FIELD_LIMITS: dict[str, int] = {
    "title": 160,
    "thesis": 2_000,
    "operator_context": 4_000,
    "decision_required": 1_000,
    "decision_owner": 300,
    "time_horizon": 300,
    "approval_path": 1_000,
    "success_measure": 1_000,
}
LIST_FIELD_LIMITS: dict[str, tuple[int, int, int]] = {
    # field: (minimum model output items, maximum items, maximum item length)
    "scope": (3, 10, 600),
    "avoid": (1, 6, 400),
    "uncertainties": (0, 8, 500),
}

REQUEST_FIELDS = frozenset(
    {"brief", "current", "output_format", "decision_frame_enabled"}
)
CURRENT_FIELDS = frozenset({*TEXT_FIELD_LIMITS, "scope", "avoid"})
DRAFT_FIELDS = frozenset({*TEXT_FIELD_LIMITS, *LIST_FIELD_LIMITS})
DECISION_FIELDS = frozenset(
    {"decision_required", "decision_owner", "time_horizon", "approval_path", "success_measure"}
)


PROMPT_DRAFT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "title": {"type": "string", "minLength": 3, "maxLength": 160},
        "thesis": {"type": "string", "minLength": 20, "maxLength": 2_000},
        "scope": {
            "type": "array",
            "minItems": 3,
            "maxItems": 10,
            "items": {"type": "string", "minLength": 1, "maxLength": 600},
        },
        "avoid": {
            "type": "array",
            "minItems": 1,
            "maxItems": 6,
            "items": {"type": "string", "minLength": 1, "maxLength": 400},
        },
        "operator_context": {"type": "string", "maxLength": 4_000},
        "decision_required": {"type": "string", "maxLength": 1_000},
        "decision_owner": {"type": "string", "maxLength": 300},
        "time_horizon": {"type": "string", "maxLength": 300},
        "approval_path": {"type": "string", "maxLength": 1_000},
        "success_measure": {"type": "string", "maxLength": 1_000},
        "uncertainties": {
            "type": "array",
            "maxItems": 8,
            "items": {"type": "string", "minLength": 1, "maxLength": 500},
        },
    },
    "required": sorted(DRAFT_FIELDS),
}


class PromptAssistError(RuntimeError):
    """Base class for prompt-coach failures safe for an API boundary."""


class PromptAssistValidationError(PromptAssistError):
    """The request or structured model response did not match the contract."""


class PromptAssistModelError(PromptAssistError):
    """The bounded model call ended without a usable structured response."""


@dataclass(frozen=True)
class PromptAssistRequest:
    brief: str
    current: dict[str, str | list[str]]
    output_format: str
    decision_frame_enabled: bool


@dataclass(frozen=True)
class PromptAssistResult:
    draft: dict[str, str | list[str]]
    output_format: str
    model: str
    cost_usd: float
    turns: int
    decision_frame_enabled: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "draft": self.draft,
            # Echo the validated operator selection; the model cannot change it.
            "output_format": self.output_format,
            "decision_frame_enabled": self.decision_frame_enabled,
            "model": self.model,
            "cost_usd": self.cost_usd,
            "cost_is_estimate": True,
            "turns": self.turns,
            "budget_ceiling_usd": PROMPT_ASSIST_MAX_BUDGET_USD,
            "provider": "openai",
            "started_run": False,
        }


ResponseFunction = Callable[..., Awaitable[object]]


def _unknown_fields(value: dict[str, object], allowed: frozenset[str]) -> list[str]:
    return sorted(str(key) for key in value if key not in allowed)


def _normalise_text(value: object, *, field: str, maximum: int) -> str:
    if not isinstance(value, str):
        raise PromptAssistValidationError(f"{field} must be text.")
    if any(ord(character) < 32 and character not in "\t\r\n" for character in value):
        raise PromptAssistValidationError(f"{field} contains unsupported control characters.")
    text = re.sub(r"\s+", " ", value).strip()
    if len(text) > maximum:
        raise PromptAssistValidationError(
            f"{field} exceeds its {maximum:,}-character limit."
        )
    return text


def _normalise_list(
    value: object,
    *,
    field: str,
    minimum: int,
    maximum_items: int,
    maximum_item_length: int,
) -> list[str]:
    if not isinstance(value, list):
        raise PromptAssistValidationError(f"{field} must be a list of text items.")
    if len(value) > maximum_items:
        raise PromptAssistValidationError(
            f"{field} may contain no more than {maximum_items} items."
        )
    cleaned: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value, start=1):
        text = _normalise_text(
            item,
            field=f"{field}[{index}]",
            maximum=maximum_item_length,
        )
        text = re.sub(r"^(?:[-*\u2022]\s+)", "", text).strip()
        if not text:
            continue
        identity = text.casefold()
        if identity in seen:
            continue
        seen.add(identity)
        cleaned.append(text)
    if len(cleaned) < minimum:
        raise PromptAssistValidationError(
            f"{field} must contain at least {minimum} distinct item"
            f"{'s' if minimum != 1 else ''}."
        )
    return cleaned


def normalise_prompt_assist_request(payload: object) -> PromptAssistRequest:
    """Validate browser input before any model call is possible."""

    if not isinstance(payload, dict):
        raise PromptAssistValidationError("Prompt-assist input must be a JSON object.")
    unknown = _unknown_fields(payload, REQUEST_FIELDS)
    if unknown:
        raise PromptAssistValidationError(
            "Unknown prompt-assist field(s): " + ", ".join(unknown)
        )

    brief = _normalise_text(
        payload.get("brief", ""), field="brief", maximum=12_000
    )
    output_format_raw = payload.get("output_format", "article")
    if not isinstance(output_format_raw, str):
        raise PromptAssistValidationError("output_format must be text.")
    output_format = output_format_raw.strip().lower() or "article"
    if output_format not in ALLOWED_OUTPUT_FORMATS:
        raise PromptAssistValidationError(
            "output_format must be report, article, brief, or recommendations."
        )
    decision_frame_enabled = payload.get("decision_frame_enabled", False)
    if not isinstance(decision_frame_enabled, bool):
        raise PromptAssistValidationError("decision_frame_enabled must be true or false.")

    raw_current = payload.get("current", {})
    if not isinstance(raw_current, dict):
        raise PromptAssistValidationError("current must be a JSON object.")
    unknown_current = _unknown_fields(raw_current, CURRENT_FIELDS)
    if unknown_current:
        raise PromptAssistValidationError(
            "Unknown current prompt field(s): " + ", ".join(unknown_current)
        )

    current: dict[str, str | list[str]] = {}
    for field, maximum in TEXT_FIELD_LIMITS.items():
        current[field] = _normalise_text(
            raw_current.get(field, ""), field=f"current.{field}", maximum=maximum
        )
        if not decision_frame_enabled and field in DECISION_FIELDS:
            current[field] = ""
    for field in ("scope", "avoid"):
        _, maximum_items, maximum_item_length = LIST_FIELD_LIMITS[field]
        current[field] = _normalise_list(
            raw_current.get(field, []),
            field=f"current.{field}",
            minimum=0,
            maximum_items=maximum_items,
            maximum_item_length=maximum_item_length,
        )

    meaningful_current = any(
        bool(value) for value in current.values()
    )
    if not brief and not meaningful_current:
        raise PromptAssistValidationError(
            "Describe the report idea or provide at least one current prompt field."
        )

    total_characters = len(brief) + len(output_format)
    for value in current.values():
        if isinstance(value, list):
            total_characters += sum(len(item) for item in value)
        else:
            total_characters += len(value)
    if total_characters > PROMPT_ASSIST_MAX_INPUT_CHARS:
        raise PromptAssistValidationError(
            f"Prompt-assist input exceeds the {PROMPT_ASSIST_MAX_INPUT_CHARS:,}-character limit."
        )

    return PromptAssistRequest(
        brief=brief,
        current=current,
        output_format=output_format,
        decision_frame_enabled=decision_frame_enabled,
    )


def normalise_prompt_draft(
    value: object, *, decision_frame_enabled: bool = True
) -> dict[str, str | list[str]]:
    """Fail closed if structured model output exceeds the writable field set."""

    if not isinstance(value, dict):
        raise PromptAssistValidationError(
            "The prompt coach returned no structured draft."
        )
    unknown = _unknown_fields(value, DRAFT_FIELDS)
    missing = sorted(DRAFT_FIELDS.difference(value))
    if unknown or missing:
        details: list[str] = []
        if unknown:
            details.append("unknown fields: " + ", ".join(unknown))
        if missing:
            details.append("missing fields: " + ", ".join(missing))
        raise PromptAssistValidationError(
            "The prompt coach returned an invalid field set (" + "; ".join(details) + ")."
        )

    draft: dict[str, str | list[str]] = {}
    for field, maximum in TEXT_FIELD_LIMITS.items():
        draft[field] = _normalise_text(
            value[field], field=field, maximum=maximum
        )
        if not decision_frame_enabled and field in DECISION_FIELDS:
            draft[field] = ""
    if len(str(draft["title"])) < 3:
        raise PromptAssistValidationError("title must contain at least 3 characters.")
    if len(str(draft["thesis"])) < 20:
        raise PromptAssistValidationError("thesis must contain at least 20 characters.")

    for field, (minimum, maximum_items, maximum_item_length) in LIST_FIELD_LIMITS.items():
        draft[field] = _normalise_list(
            value[field],
            field=field,
            minimum=minimum,
            maximum_items=maximum_items,
            maximum_item_length=maximum_item_length,
        )
    return draft


def _load_system_prompt(path: Path) -> str:
    try:
        prompt = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise PromptAssistModelError("The prompt-coach instructions are unavailable.") from exc
    if not prompt:
        raise PromptAssistModelError("The prompt-coach instructions are empty.")
    return prompt


def _operator_prompt(request: PromptAssistRequest) -> str:
    # JSON encoding makes the boundary visible and preserves supplied text as
    # data.  The system prompt separately instructs the model never to execute
    # instructions found inside this untrusted block.
    data = {
        "brief": request.brief,
        "current": request.current,
        "output_format": request.output_format,
        "decision_frame_enabled": request.decision_frame_enabled,
    }
    return (
        "Draft the allowed run-prompt fields from the untrusted operator data "
        "below. Return only the structured response required by your schema.\n\n"
        "<untrusted_operator_data>\n"
        + json.dumps(data, ensure_ascii=False, sort_keys=True)
        + "\n</untrusted_operator_data>"
    )


def _safe_provider_failure_message(
    *, status: int | None = None, detail: object = ""
) -> str:
    """Map provider failures to actionable text without echoing raw secrets."""

    folded = str(detail or "").casefold()
    if status == 401 or "incorrect api key" in folded:
        return (
            "OpenAI rejected OPENAI_API_KEY. Replace it in .env with an active "
            "OpenAI API key, then restart the Council."
        )
    if status in {403, 404} or "model_not_found" in folded:
        return (
            "This OpenAI API project cannot use gpt-5.6-sol. Enable that model "
            "for the project or use a key from a project with access, then restart "
            "the Council."
        )
    if status == 429 or "rate limit" in folded:
        return "OpenAI is rate-limiting this request. Wait briefly and try again."
    if isinstance(status, int) and status >= 500:
        return "OpenAI returned a temporary service error. Try the prompt coach again."
    return "GPT-5.6 Sol could not complete the bounded Prompt Coach call."


def _estimated_openai_cost(response: object) -> float:
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "input_tokens", 0) or 0
    output_tokens = getattr(usage, "output_tokens", 0) or 0
    if (
        not isinstance(input_tokens, int)
        or isinstance(input_tokens, bool)
        or input_tokens < 0
        or not isinstance(output_tokens, int)
        or isinstance(output_tokens, bool)
        or output_tokens < 0
    ):
        raise PromptAssistModelError(
            "The prompt coach returned invalid OpenAI usage metadata."
        )
    return round(
        (
            input_tokens * PROMPT_ASSIST_INPUT_USD_PER_MILLION
            + output_tokens * PROMPT_ASSIST_OUTPUT_USD_PER_MILLION
        )
        / 1_000_000,
        6,
    )


async def generate_prompt_draft(
    payload: object,
    *,
    model: str | None = None,
    repo_root: Path = REPO_ROOT,
    prompt_path: Path = PROMPT_COACH_PATH,
    response_fn: ResponseFunction | None = None,
) -> dict[str, object]:
    """Return bounded, structured wizard fields without starting a Council run.

    ``response_fn`` is injectable so unit and server tests never need a real
    model call. The function performs no writes and does not import the
    orchestrator.
    """

    request = normalise_prompt_assist_request(payload)
    if model is not None and not isinstance(model, str):
        raise PromptAssistModelError("The configured Prompt Coach model must be text.")
    model_id = model.strip() if isinstance(model, str) else PROMPT_ASSIST_MODEL
    if not isinstance(model_id, str) or not model_id.strip():
        raise PromptAssistModelError("No OpenAI Prompt Coach model is configured.")
    model_id = model_id.strip()
    _ = repo_root  # Deliberately accepted for compatibility; the call cannot write.
    call = response_fn
    client = None
    try:
        if call is None:
            if not os.environ.get("OPENAI_API_KEY"):
                raise PromptAssistModelError(
                    "Prompt Coach requires OPENAI_API_KEY in .env. Add the key "
                    "and restart the Council."
                )
            from openai import AsyncOpenAI

            client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"], timeout=60.0)
            call = client.responses.create
        response = await call(
            model=model_id,
            instructions=_load_system_prompt(prompt_path),
            input=_operator_prompt(request),
            reasoning={"effort": PROMPT_ASSIST_REASONING_EFFORT},
            max_output_tokens=PROMPT_ASSIST_MAX_OUTPUT_TOKENS,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "council_prompt_draft",
                    "schema": PROMPT_DRAFT_SCHEMA,
                    "strict": True,
                },
                "verbosity": "low",
            },
            tools=[],
            store=False,
        )
    except PromptAssistError:
        raise
    except Exception as exc:  # noqa: BLE001 - provider details stay behind the API
        status = getattr(exc, "status_code", None)
        if not isinstance(status, int):
            status = getattr(exc, "status", None)
        raise PromptAssistModelError(
            _safe_provider_failure_message(
                status=status if isinstance(status, int) else None,
                detail=exc,
            )
        ) from exc
    finally:
        if client is not None:
            await client.close()

    if response is None:
        raise PromptAssistModelError(
            "The prompt coach ended without an OpenAI response."
        )
    status = str(getattr(response, "status", "") or "").casefold()
    if status != "completed" or getattr(response, "error", None) is not None:
        raise PromptAssistModelError(
            "GPT-5.6 Sol did not complete the Prompt Coach response. Try again."
        )
    output_items = getattr(response, "output", ()) or ()
    if any(
        str(getattr(item, "type", "") or "").casefold().endswith("_call")
        for item in output_items
    ):
        raise PromptAssistModelError(
            "The prompt coach attempted an action it is not allowed to perform."
        )
    output_text = getattr(response, "output_text", None)
    if not isinstance(output_text, str) or not output_text.strip():
        raise PromptAssistModelError(
            "GPT-5.6 Sol returned no structured Prompt Coach draft."
        )
    try:
        structured = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise PromptAssistModelError(
            "GPT-5.6 Sol returned a Prompt Coach draft that could not be decoded."
        ) from exc
    try:
        draft = normalise_prompt_draft(
            structured,
            decision_frame_enabled=request.decision_frame_enabled,
        )
    except PromptAssistValidationError as exc:
        raise PromptAssistModelError(
            "GPT-5.6 Sol returned a draft that did not match the Council form."
        ) from exc

    cost = _estimated_openai_cost(response)
    if not math.isfinite(cost) or cost < 0:
        raise PromptAssistModelError("The prompt coach returned invalid usage metadata.")
    if cost > PROMPT_ASSIST_MAX_BUDGET_USD + 1e-6:
        raise PromptAssistModelError("The prompt coach exceeded its fixed cost ceiling.")
    return PromptAssistResult(
        draft=draft,
        output_format=request.output_format,
        model=model_id,
        cost_usd=cost,
        turns=PROMPT_ASSIST_MAX_TURNS,
        decision_frame_enabled=request.decision_frame_enabled,
    ).to_dict()


__all__ = [
    "ALLOWED_OUTPUT_FORMATS",
    "DECISION_FIELDS",
    "PROMPT_ASSIST_MAX_BUDGET_USD",
    "PROMPT_ASSIST_MAX_INPUT_CHARS",
    "PROMPT_ASSIST_MAX_OUTPUT_TOKENS",
    "PROMPT_ASSIST_MAX_TURNS",
    "PROMPT_ASSIST_MODEL",
    "PROMPT_DRAFT_SCHEMA",
    "PromptAssistError",
    "PromptAssistModelError",
    "PromptAssistValidationError",
    "generate_prompt_draft",
    "normalise_prompt_assist_request",
    "normalise_prompt_draft",
]
