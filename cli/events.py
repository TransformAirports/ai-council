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
    """Per-run event queue + pending-checkpoint registry."""

    def __init__(self) -> None:
        self.queue: asyncio.Queue[dict] = asyncio.Queue()
        self._pending: dict[str, asyncio.Future] = {}
        self.closed = False

    async def emit(self, event_type: str, data: dict) -> None:
        await self.queue.put({"type": event_type, **data})

    async def checkpoint(self, kind: str, payload: dict) -> dict:
        cid = uuid.uuid4().hex
        loop = asyncio.get_event_loop()
        fut: asyncio.Future = loop.create_future()
        self._pending[cid] = fut
        await self.queue.put({"type": "checkpoint", "id": cid, "kind": kind, **payload})
        try:
            return await fut
        finally:
            self._pending.pop(cid, None)

    def resolve(self, cid: str, decision: dict) -> bool:
        fut = self._pending.get(cid)
        if fut is not None and not fut.done():
            fut.set_result(decision)
            return True
        return False

    async def close(self) -> None:
        self.closed = True
        # Wake any waiting consumer.
        await self.queue.put({"type": "stream_end"})
        # Fail any still-pending checkpoints so the pipeline can unwind.
        for fut in list(self._pending.values()):
            if not fut.done():
                fut.set_result({"action": "abort"})
