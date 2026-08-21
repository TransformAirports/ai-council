from __future__ import annotations

import asyncio
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from starlette.requests import Request

import cli.server as server
from cli.prompt_assist import PromptAssistModelError


ORIGIN = "http://127.0.0.1:8723"
CLIENT_ID = "prompt_coach_client_123456"


class _LiveTask:
    def done(self) -> bool:
        return False


class _LockedPromptCoach:
    def locked(self) -> bool:
        return True


class PromptAssistEndpointTests(unittest.TestCase):
    def test_new_run_spec_defaults_to_narrative_and_decision_fields_fail_closed(self) -> None:
        narrative = server._build_spec(
            {
                "title": "The gate that time forgot",
                "thesis": "The gate feels obsolete because its operating assumptions aged faster than its concrete.",
                "scope": ["Follow one aircraft turn from arrival to departure."],
                "decision_owner": "Should not survive",
            }
        )
        opted_in = server._build_spec(
            {
                "title": "A named choice",
                "thesis": "The airport should test the operating model before it builds.",
                "decision_frame_enabled": True,
                "decision_owner": "Chief Operating Officer",
            }
        )

        self.assertEqual(narrative.output_format, "article")
        self.assertFalse(narrative.decision_frame_enabled)
        self.assertEqual(narrative.decision_owner, "")
        self.assertEqual(
            narrative.lines_of_inquiry,
            ["Follow one aircraft turn from arrival to departure."],
        )
        self.assertNotIn(narrative.lines_of_inquiry[0], narrative.success_criteria)
        self.assertTrue(opted_in.decision_frame_enabled)
        self.assertEqual(opted_in.decision_owner, "Chief Operating Officer")

    def setUp(self) -> None:
        self.client = TestClient(
            server.app,
            base_url=ORIGIN,
            client=("127.0.0.1", 51000),
        )
        self.previous_task = server._active_task
        server._active_task = None

    def tearDown(self) -> None:
        server._active_task = self.previous_task
        self.client.close()

    @property
    def headers(self) -> dict[str, str]:
        return {
            "origin": ORIGIN,
            "content-type": "application/json",
            server._SESSION_HEADER: server._SESSION_TOKEN,
            server._CLIENT_HEADER: CLIENT_ID,
        }

    def test_authenticated_request_returns_form_fields_without_starting_a_run(self) -> None:
        result = {
            "draft": {
                "title": "Capacity Before Concrete",
                "thesis": "The airport should prove the constraint before it builds.",
                "scope": ["Measure it", "Compare peers", "Test the counter-case"],
                "avoid": ["Vendor lists"],
                "operator_context": "",
                "decision_required": "Choose whether to fund a pilot.",
                "decision_owner": "",
                "time_horizon": "",
                "approval_path": "",
                "success_measure": "",
                "uncertainties": ["The decision owner was not supplied."],
            },
            "output_format": "report",
            "model": "test-model",
            "cost_usd": 0.12,
            "turns": 1,
            "budget_ceiling_usd": 1.5,
            "started_run": False,
        }
        fake = AsyncMock(return_value=result)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "prompts" / "runs").mkdir(parents=True)
            (root / "outputs").mkdir()
            before = sorted(path.relative_to(root) for path in root.rglob("*"))
            with (
                patch.object(server, "REPO_ROOT", root),
                patch("cli.prompt_assist.generate_prompt_draft", fake),
            ):
                response = self.client.post(
                    "/api/run-prompt/draft",
                    headers=self.headers,
                    json={"brief": "Test the constraint before building."},
                )
            after = sorted(path.relative_to(root) for path in root.rglob("*"))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["started_run"])
        self.assertEqual(server._active_task, None)
        self.assertEqual(before, after)
        kwargs = fake.await_args.kwargs
        self.assertEqual(kwargs["repo_root"], root)
        self.assertEqual(kwargs["model"], "gpt-5.6-sol")
        self.assertNotIn("agents", response.json()["draft"])
        self.assertNotIn("budget", response.json()["draft"])

    def test_authentication_json_size_active_run_and_concurrency_guards(self) -> None:
        forbidden = self.client.post(
            "/api/run-prompt/draft", json={"brief": "A useful question"}
        )
        wrong_type = self.client.post(
            "/api/run-prompt/draft",
            headers={key: value for key, value in self.headers.items() if key != "content-type"},
            content="plain text",
        )
        malformed = self.client.post(
            "/api/run-prompt/draft", headers=self.headers, content=b"{not-json"
        )
        oversized = self.client.post(
            "/api/run-prompt/draft",
            headers=self.headers,
            json={"brief": "x" * (server._PROMPT_ASSIST_MAX_BODY_BYTES + 1)},
        )
        server._active_task = _LiveTask()  # type: ignore[assignment]
        active = self.client.post(
            "/api/run-prompt/draft",
            headers=self.headers,
            json={"brief": "A useful question"},
        )
        server._active_task = None
        with patch.object(server, "_prompt_assist_lock", _LockedPromptCoach()):
            concurrent = self.client.post(
                "/api/run-prompt/draft",
                headers=self.headers,
                json={"brief": "A useful question"},
            )

        self.assertEqual(forbidden.status_code, 403)
        self.assertEqual(wrong_type.status_code, 400)
        self.assertEqual(malformed.status_code, 400)
        self.assertEqual(oversized.status_code, 413)
        self.assertEqual(active.status_code, 409)
        self.assertEqual(concurrent.status_code, 409)

    def test_model_access_failure_is_actionable_in_the_browser(self) -> None:
        message = (
            "This OpenAI API project cannot use gpt-5.6-sol. Enable that model "
            "for the project or use a key from a project with access, then restart "
            "the Council."
        )
        fake = AsyncMock(side_effect=PromptAssistModelError(message))
        with patch("cli.prompt_assist.generate_prompt_draft", fake):
            response = self.client.post(
                "/api/run-prompt/draft",
                headers=self.headers,
                json={"brief": "Test the constraint before building."},
            )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json()["error"], message)
        self.assertEqual(response.json()["code"], "prompt_coach_model_error")

    def test_concurrent_prompt_requests_do_not_queue_a_second_model_call(self) -> None:
        first_body_waiting = threading.Event()
        release_first_body = threading.Event()
        body_counter_lock = threading.Lock()
        body_calls = 0
        responses: dict[str, object] = {}
        failures: list[BaseException] = []
        original_body = Request.body

        result = {
            "draft": {
                "title": "One paid call",
                "thesis": "Concurrent requests must not queue duplicate spend.",
                "scope": ["Observe the request gate"],
                "avoid": [],
                "operator_context": "",
                "decision_required": "",
                "decision_owner": "",
                "time_horizon": "",
                "approval_path": "",
                "success_measure": "",
                "uncertainties": [],
            },
            "started_run": False,
        }
        fake_coach = AsyncMock(return_value=result)

        async def hold_first_body(request: Request) -> bytes:
            nonlocal body_calls
            if request.url.path == "/api/run-prompt/draft":
                with body_counter_lock:
                    body_calls += 1
                    position = body_calls
                if position == 1:
                    first_body_waiting.set()
                    await asyncio.to_thread(release_first_body.wait, 3)
            return await original_body(request)

        def submit(name: str, client: TestClient) -> None:
            try:
                responses[name] = client.post(
                    "/api/run-prompt/draft",
                    headers=self.headers,
                    json={"brief": f"Concurrent request {name}"},
                )
            except BaseException as exc:  # surface worker failures in this test
                failures.append(exc)

        first = threading.Thread(target=submit, args=("first", self.client), daemon=True)
        second = threading.Thread(target=submit, args=("second", self.client), daemon=True)
        with (
            patch.object(server, "_prompt_assist_lock", asyncio.Lock()),
            patch.object(server, "_run_library_lock", asyncio.Lock()),
            patch.object(Request, "body", hold_first_body),
            patch("cli.prompt_assist.generate_prompt_draft", fake_coach),
        ):
            first.start()
            try:
                self.assertTrue(
                    first_body_waiting.wait(2),
                    "first request never reached its deliberately delayed body read",
                )
                second.start()
                second.join(2)
                second_returned_before_release = not second.is_alive()
            finally:
                release_first_body.set()
                first.join(3)
                second.join(3)

        self.assertEqual(failures, [])
        self.assertTrue(
            second_returned_before_release,
            "the competing request queued instead of receiving an immediate 409",
        )
        self.assertFalse(first.is_alive())
        self.assertFalse(second.is_alive())
        self.assertEqual(
            sorted(response.status_code for response in responses.values()),  # type: ignore[union-attr]
            [200, 409],
        )
        self.assertEqual(fake_coach.await_count, 1)
        self.assertEqual(body_calls, 1, "the rejected request should not consume its body")

    def test_prompt_coach_and_pipeline_start_never_overlap(self) -> None:
        coach_entered = threading.Event()
        release_coach = threading.Event()
        pipeline_entered = threading.Event()
        response_box: dict[str, object] = {}

        async def delayed_coach(*args: object, **kwargs: object) -> dict[str, object]:
            coach_entered.set()
            await asyncio.to_thread(release_coach.wait, 3)
            return {
                "draft": {
                    "title": "Gate test",
                    "thesis": "The two paid paths must not overlap.",
                    "scope": ["Observe ordering"],
                    "avoid": [],
                    "operator_context": "",
                    "decision_required": "",
                    "decision_owner": "",
                    "time_horizon": "",
                    "approval_path": "",
                    "success_measure": "",
                    "uncertainties": [],
                },
                "started_run": False,
            }

        async def fake_drive(mode: str, payload: dict, sink: object) -> None:
            pipeline_entered.set()
            await sink.close()  # type: ignore[attr-defined]

        def request_coach(client: TestClient) -> None:
            response_box["response"] = client.post(
                "/api/run-prompt/draft",
                headers=self.headers,
                json={"brief": "Prove the shared start gate."},
            )

        ws_client_id = "pipeline_start_client_123456"
        ws_path = (
            f"/ws?token={server._SESSION_TOKEN}&client_id={ws_client_id}"
        )
        ws_headers = {"origin": ORIGIN, "host": "127.0.0.1:8723"}
        start_message = {
            "type": "start",
            "mode": "new",
            "spec": {},
            "client_id": ws_client_id,
            "session_token": server._SESSION_TOKEN,
        }

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outputs").mkdir()
            with (
                TestClient(server.app, base_url=ORIGIN) as client,
                patch.object(server, "REPO_ROOT", root),
                patch.object(server, "_run_library_lock", asyncio.Lock()),
                patch("cli.prompt_assist.generate_prompt_draft", delayed_coach),
                patch.object(server, "_drive_run", fake_drive),
            ):
                coach_thread = threading.Thread(
                    target=request_coach, args=(client,), daemon=True
                )
                coach_thread.start()
                try:
                    self.assertTrue(coach_entered.wait(2), "coach call did not begin")
                    with client.websocket_connect(ws_path, headers=ws_headers) as socket:
                        socket.send_json(start_message)
                        self.assertFalse(
                            pipeline_entered.wait(0.15),
                            "pipeline entered while the prompt coach still held the shared gate",
                        )
                        release_coach.set()
                        self.assertTrue(
                            pipeline_entered.wait(2),
                            "pipeline did not begin after the prompt coach released the gate",
                        )
                finally:
                    release_coach.set()
                    coach_thread.join(3)
                    self.assertFalse(coach_thread.is_alive())
                    server._active_task = None
                    server._active_sink = None
                    server._active_owner = None

        response = response_box.get("response")
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)  # type: ignore[union-attr]


if __name__ == "__main__":
    unittest.main()
