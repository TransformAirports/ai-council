"""A long run must survive the browser that started it.

Runs take hours. Browsers crash, laptops sleep, tabs get closed. The server
keeps a sequenced event log so a returning tab can rejoin, and control must
pass to a live tab when the original one is gone — otherwise the run stalls
forever at a checkpoint nobody is allowed to approve.
"""
from __future__ import annotations

import asyncio
import json
import uuid

import pytest
from fastapi.testclient import TestClient

import cli.server as server


def _client_id() -> str:
    return uuid.uuid4().hex + uuid.uuid4().hex[:8]


# The origin guard only trusts loopback, and requires Origin to match Host
# exactly. TestClient defaults to the host "testserver", so both are set here.
HEADERS = {"origin": "http://127.0.0.1", "host": "127.0.0.1"}


def _url(client_id: str) -> str:
    return f"/ws?token={server._SESSION_TOKEN}&client_id={client_id}"


def _auth(client_id: str, payload: dict) -> dict:
    return {**payload, "client_id": client_id, "session_token": server._SESSION_TOKEN}


@pytest.fixture(autouse=True)
def _stub_run(monkeypatch, tmp_path):
    """A fake run: emits progress, then blocks on a checkpoint like a real one."""

    async def fake_drive(mode, payload, sink):
        server.set_sink(sink)
        try:
            await sink.emit("run_start", {"slug": "t", "title": "Test Run", "agents": []})
            await sink.emit("stage_start", {"stage": 1, "label": "Research"})
            decision = await sink.checkpoint(
                "stage2", {"title": "CP", "documents": [], "actions": ["continue", "abort"]}
            )
            await sink.emit("run_complete", {"slug": "t", "title": "Test Run",
                                             "total": 1.0, "decision": decision["action"]})
        finally:
            await sink.close()

    monkeypatch.setattr(server, "_drive_run", fake_drive)
    monkeypatch.setattr(server, "REPO_ROOT", tmp_path)
    server._active_sink = None
    server._active_owner = None
    server._active_task = None
    server._live_clients.clear()
    yield
    server._active_task = None
    server._active_sink = None
    server._active_owner = None
    server._live_clients.clear()


def _drain_until(ws, wanted: str, budget: int = 25) -> dict:
    for _ in range(budget):
        event = ws.receive_json()
        if event.get("type") == wanted:
            return event
    raise AssertionError(f"never received {wanted!r}")


def test_control_passes_to_a_live_tab_when_the_owner_crashes():
    starter, rescuer = _client_id(), _client_id()
    with TestClient(server.app) as client:
        # The tab that starts the run owns it.
        with client.websocket_connect(_url(starter), headers=HEADERS) as ws:
            ws.send_json(_auth(starter, {"type": "start", "mode": "new", "spec": {}}))
            status = _drain_until(ws, "control_status")
            assert status["controls"] is True
            checkpoint = _drain_until(ws, "checkpoint")
            assert checkpoint["id"]
        # Socket closed without resolving the checkpoint — the browser crashed.

        # A new tab (new session id, as sessionStorage did not survive) rejoins.
        with client.websocket_connect(_url(rescuer), headers=HEADERS) as ws2:
            ws2.send_json(_auth(rescuer, {"type": "attach"}))
            status2 = _drain_until(ws2, "control_status")
            assert status2["controls"] is True, "a dead tab must not keep control"

            # The pending checkpoint is replayed so the operator can act on it.
            replayed = _drain_until(ws2, "checkpoint")
            assert replayed["id"] == checkpoint["id"]

            # And approving it actually moves the run forward.
            ws2.send_json(_auth(rescuer, {"type": "checkpoint",
                                          "id": replayed["id"], "action": "continue"}))
            done = _drain_until(ws2, "run_complete")
            assert done["decision"] == "continue"


def test_a_second_live_tab_observes_and_cannot_approve():
    owner, observer = _client_id(), _client_id()
    with TestClient(server.app) as client:
        with client.websocket_connect(_url(owner), headers=HEADERS) as ws:
            ws.send_json(_auth(owner, {"type": "start", "mode": "new", "spec": {}}))
            _drain_until(ws, "control_status")
            checkpoint = _drain_until(ws, "checkpoint")

            # Owner still connected: the second tab watches, it does not steal.
            with client.websocket_connect(_url(observer), headers=HEADERS) as ws2:
                ws2.send_json(_auth(observer, {"type": "attach"}))
                status = _drain_until(ws2, "control_status")
                assert status["controls"] is False
                ws2.send_json(_auth(observer, {"type": "checkpoint",
                                               "id": checkpoint["id"], "action": "abort"}))
                refusal = _drain_until(ws2, "control_error")
                assert "observing" in refusal["message"]

            # The owner's approval is the one that counts.
            ws.send_json(_auth(owner, {"type": "checkpoint",
                                       "id": checkpoint["id"], "action": "continue"}))
            done = _drain_until(ws, "run_complete")
            assert done["decision"] == "continue"


def test_reattach_with_a_cursor_replays_only_what_was_missed():
    starter, rescuer = _client_id(), _client_id()
    with TestClient(server.app) as client:
        with client.websocket_connect(_url(starter), headers=HEADERS) as ws:
            ws.send_json(_auth(starter, {"type": "start", "mode": "new", "spec": {}}))
            _drain_until(ws, "control_status")
            first = _drain_until(ws, "run_start")
            cursor = first["seq"]

        with client.websocket_connect(_url(rescuer), headers=HEADERS) as ws2:
            ws2.send_json(_auth(rescuer, {"type": "attach", "after": cursor}))
            _drain_until(ws2, "control_status")
            seen = [ws2.receive_json() for _ in range(2)]
            seqs = [e["seq"] for e in seen]
            assert all(s > cursor for s in seqs), "already-rendered events were resent"
            assert [e["type"] for e in seen] == ["stage_start", "checkpoint"]
