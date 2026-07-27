"""Event plumbing between the orchestrator and the web UI.

The orchestrator is a long-running async pipeline. The web server needs two
things from it: a live stream of progress events (agent started, agent
finished, stage changed, cost ticked), and a way to pause for the two human
checkpoints and resume when the browser sends a decision.

A `WebSink` is created per run by the server. The orchestrator reads the
active sink from a contextvar (set at run start), so deep functions like
`_run_agent` can emit without threading the sink through every signature.
When no sink is active (headless flag use), `emit()` is a no-op and
checkpoints fall back to the terminal.
"""
from __future__ import annotations

import asyncio
import contextvars
import uuid
from typing import Any

_current_sink: contextvars.ContextVar["WebSink | None"] = contextvars.ContextVar(
    "council_sink", default=None
)


def set_sink(sink: "WebSink | None") -> None:
    _current_sink.set(sink)


def get_sink() -> "WebSink | None":
    return _current_sink.get()


async def emit(event_type: str, **data: Any) -> None:
    """Push a progress event to the active web sink, if any."""
    sink = _current_sink.get()
    if sink is not None:
        await sink.emit(event_type, data)


async def request_checkpoint(kind: str, payload: dict) -> dict | None:
    """Block until the browser resolves a checkpoint. None if no web sink."""
    sink = _current_sink.get()
    if sink is None:
        return None
    return await sink.checkpoint(kind, payload)


class WebSink:
    """Per-run sequenced event log plus pending-checkpoint registry."""

    def __init__(self) -> None:
        self._pending: dict[str, asyncio.Future] = {}
        self._condition = asyncio.Condition()
        self._events: list[dict] = []
        self._sequence = 0
        self.closed = False
        self.run_start_event: dict | None = None
        self.last_stage_event: dict | None = None
        self.pending_checkpoint: dict | None = None
        self.agent_events: dict[str, dict] = {}
        self.quality_events: dict[str, dict] = {}
        self.artifact_events: dict[str, dict] = {}

    async def emit(self, event_type: str, data: dict) -> None:
        self._sequence += 1
        event = {"type": event_type, "seq": self._sequence, **data}
        if event_type == "run_start":
            self.run_start_event = event
        elif event_type == "stage_start":
            self.last_stage_event = event
        elif event_type in {
            "agent_start",
            "agent_done",
            "agent_error",
            "agent_skipped",
        } and event.get("agent"):
            self.agent_events[str(event["agent"])] = event
        elif event_type in {
            "quality_gate", "artifact_validated", "evidence_update",
            "render_qa",
        }:
            self.quality_events[event_type] = event
            if event_type == "artifact_validated":
                key = str(
                    event.get("path")
                    or event.get("artifact")
                    or event.get("step")
                    or event["seq"]
                )
                self.artifact_events[key] = event
        async with self._condition:
            self._events.append(event)
            self._condition.notify_all()

    async def checkpoint(self, kind: str, payload: dict) -> dict:
        cid = uuid.uuid4().hex
        loop = asyncio.get_event_loop()
        fut: asyncio.Future = loop.create_future()
        self._pending[cid] = fut
        await self.emit(
            "checkpoint",
            {"id": cid, "kind": kind, **payload},
        )
        self.pending_checkpoint = self._events[-1]
        try:
            return await fut
        finally:
            self._pending.pop(cid, None)
            self.pending_checkpoint = None

    def resolve(self, cid: str, decision: dict) -> bool:
        fut = self._pending.get(cid)
        if fut is not None and not fut.done():
            fut.set_result(decision)
            return True
        return False

    def events_after(self, sequence: int = 0) -> list[dict]:
        """Return each event exactly once after a caller-owned cursor."""

        return [
            event for event in self._events
            if int(event.get("seq", 0)) > sequence
        ]

    async def wait_after(self, sequence: int = 0) -> list[dict]:
        async with self._condition:
            await self._condition.wait_for(
                lambda: bool(self.events_after(sequence)) or self.closed
            )
            return self.events_after(sequence)

    def snapshot(self) -> list[dict]:
        """Backward-compatible full replay; sequence IDs make it deduplicable."""

        return self.events_after(0)

    async def close(self) -> None:
        if not self.closed:
            await self.emit("stream_end", {})
            self.closed = True
            async with self._condition:
                self._condition.notify_all()
        # Fail any still-pending checkpoints so the pipeline can unwind.
        for fut in list(self._pending.values()):
            if not fut.done():
                fut.set_result({"action": "abort"})
