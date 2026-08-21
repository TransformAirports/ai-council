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
import json
import os
import uuid
from pathlib import Path
from typing import Any

_current_sink: contextvars.ContextVar["WebSink | None"] = contextvars.ContextVar(
    "council_sink", default=None
)

# These records describe how a previous process ended. They belong in the
# durable journal for diagnosis, but replaying them through a newly resumed
# sink would make the browser treat the new stream as already finished.
_HISTORICAL_TERMINAL_EVENTS = frozenset({
    "run_error",
    "run_complete",
    "run_stopped",
    "stream_end",
})


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

    def __init__(
        self,
        journal_path: Path | None = None,
        *,
        append: bool = False,
    ) -> None:
        self._pending: dict[str, asyncio.Future] = {}
        self._condition = asyncio.Condition()
        self._events: list[dict] = []
        self._sequence = 0
        self.journal_path = Path(journal_path) if journal_path is not None else None
        self._archive_journal_path: Path | None = None
        self.journal_errors: list[str] = []
        self.closed = False
        self.run_start_event: dict | None = None
        self.last_stage_event: dict | None = None
        self.pending_checkpoint: dict | None = None
        self.agent_events: dict[str, dict] = {}
        self.quality_events: dict[str, dict] = {}
        self.artifact_events: dict[str, dict] = {}
        if self.journal_path is not None:
            if append:
                self._restore_journal()
            else:
                self._replace_journal(())

    @staticmethod
    def _decode_journal(raw: bytes) -> tuple[list[dict], bool]:
        """Return valid events and whether the on-disk bytes need repair.

        A process can be killed between writing a JSON object and its trailing
        newline. Resume keeps every complete, valid event and discards that
        incomplete tail before appending new records. Malformed complete lines
        are also omitted so one damaged diagnostic never blocks the run.
        """

        events: list[dict] = []
        repair_needed = bool(raw and not raw.endswith(b"\n"))
        for line in raw.splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                repair_needed = True
                continue
            if not isinstance(event, dict):
                repair_needed = True
                continue
            try:
                sequence = int(event.get("seq", 0))
            except (TypeError, ValueError):
                repair_needed = True
                continue
            if sequence <= 0:
                repair_needed = True
                continue
            event["seq"] = sequence
            events.append(event)
        return events, repair_needed

    def _record_journal_error(self, exc: BaseException) -> None:
        # Journaling is diagnostic infrastructure. A full disk or a damaged
        # path must never turn a recoverable model run into a pipeline failure.
        message = f"{type(exc).__name__}: {exc}"
        if not self.journal_errors or self.journal_errors[-1] != message:
            self.journal_errors.append(message)

    def _read_journal(self, path: Path) -> tuple[list[dict], bool]:
        try:
            if path.is_symlink():
                raise OSError(f"Event journal may not be a symlink: {path}")
            if not path.is_file():
                return [], False
            return self._decode_journal(path.read_bytes())
        except OSError as exc:
            self._record_journal_error(exc)
            return [], False

    @staticmethod
    def _encoded_event(event: dict) -> bytes:
        return (
            json.dumps(
                event,
                ensure_ascii=False,
                default=str,
                separators=(",", ":"),
            ).encode("utf-8")
            + b"\n"
        )

    def _replace_journal(self, events: tuple[dict, ...] | list[dict]) -> None:
        path = self.journal_path
        if path is None:
            return
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.is_symlink():
                raise OSError(f"Event journal may not be a symlink: {path}")
            with path.open("wb") as handle:
                for event in events:
                    handle.write(self._encoded_event(event))
                handle.flush()
                os.fsync(handle.fileno())
        except OSError as exc:
            self._record_journal_error(exc)

    def _append_journal(self, path: Path, event: dict) -> None:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.is_symlink():
                raise OSError(f"Event journal may not be a symlink: {path}")
            with path.open("ab") as handle:
                handle.write(self._encoded_event(event))
                handle.flush()
                os.fsync(handle.fileno())
        except OSError as exc:
            self._record_journal_error(exc)

    def _restore_journal(self) -> None:
        assert self.journal_path is not None
        events, repair_needed = self._read_journal(self.journal_path)
        # Keep the complete journal on disk and use every record to continue
        # the monotonic sequence. Only nonterminal history enters the live
        # replay queue: a stale stream_end/run_error/run_complete would cause
        # the resume pump or UI to stop before it sees the resumed run's events.
        self._events.extend(
            event
            for event in events
            if event.get("type") not in _HISTORICAL_TERMINAL_EVENTS
        )
        self._sequence = max(
            (int(event.get("seq", 0)) for event in events),
            default=0,
        )
        for event in events:
            self._track_event(event)
        if repair_needed:
            self._replace_journal(events)

    def _track_event(self, event: dict) -> None:
        event_type = event.get("type")
        if event_type == "run_start":
            self.run_start_event = event
        elif event_type == "stage_start":
            self.last_stage_event = event
        elif event_type in {
            "agent_start",
            "agent_done",
            "agent_error",
            "agent_retry",
            "agent_skipped",
        } and event.get("agent"):
            self.agent_events[str(event["agent"])] = event
        elif event_type in {
            "quality_gate", "artifact_validated", "evidence_update",
            "render_qa",
        }:
            self.quality_events[str(event_type)] = event
            if event_type == "artifact_validated":
                key = str(
                    event.get("path")
                    or event.get("artifact")
                    or event.get("step")
                    or event["seq"]
                )
                self.artifact_events[key] = event

    def bind_journal(self, journal_path: Path, *, append: bool = False) -> None:
        """Attach durable storage after a new run has passed its start gates.

        A browser creates its live sink before the pipeline knows whether the
        operator will clear an interrupted working set. Keeping the sink in
        memory until that decision prevents merely opening a new-run flow from
        truncating the prior run's diagnostic journal.
        """

        target = Path(journal_path)
        if self.journal_path is not None:
            if self.journal_path != target:
                raise RuntimeError("Event sink is already bound to another journal.")
            return
        self.journal_path = target
        if append:
            self._restore_journal()
        else:
            self._replace_journal(self._events)

    def archive_to(
        self,
        journal_path: Path,
        *,
        preserve_existing: bool = False,
    ) -> None:
        """Mirror remaining events into a committed run archive.

        ``archive_run`` commits before the final ``run_complete`` and
        ``stream_end`` events exist. Binding the sink at commit time preserves
        those final events in the dated archive and lets ``close`` remove the
        short-lived tail recreated under ``outputs/`` after archive cleanup.
        """

        target = Path(journal_path)
        existing, _ = self._read_journal(target)
        if preserve_existing and existing:
            # An idempotent cleanup retry must not replace the original run's
            # diagnostics with a newly attached sink's shorter history.
            self._sequence = max(
                self._sequence,
                max(int(event.get("seq", 0)) for event in existing),
            )
        else:
            previous = self.journal_path
            self.journal_path = target
            self._replace_journal(self._events)
            self.journal_path = previous
        self._archive_journal_path = target

    async def emit(self, event_type: str, data: dict) -> None:
        self._sequence += 1
        event = {"type": event_type, "seq": self._sequence, **data}
        self._track_event(event)
        if self.journal_path is not None:
            self._append_journal(self.journal_path, event)
        if (
            self._archive_journal_path is not None
            and self._archive_journal_path != self.journal_path
        ):
            self._append_journal(self._archive_journal_path, event)
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
            if (
                self.journal_path is not None
                and self._archive_journal_path is not None
                and self.journal_path != self._archive_journal_path
            ):
                try:
                    if self.journal_path.is_symlink():
                        raise OSError(
                            f"Event journal may not be a symlink: {self.journal_path}"
                        )
                    if self.journal_path.is_file():
                        self.journal_path.unlink()
                except OSError as exc:
                    self._record_journal_error(exc)
        # Fail any still-pending checkpoints so the pipeline can unwind.
        for fut in list(self._pending.values()):
            if not fut.done():
                fut.set_result({"action": "abort"})
