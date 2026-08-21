from __future__ import annotations

import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cli.events import WebSink, set_sink


class WebSinkTests(unittest.TestCase):
    def test_replay_is_sequenced_and_quality_types_do_not_overwrite(self) -> None:
        async def scenario() -> None:
            sink = WebSink()
            await sink.emit("artifact_validated", {"path": "a.md", "valid": True})
            await sink.emit("evidence_update", {"record_count": 4})
            await sink.emit("quality_gate", {"passed": True})

            replay = sink.events_after(0)
            self.assertEqual([event["seq"] for event in replay], [1, 2, 3])
            self.assertEqual(
                {event["type"] for event in replay},
                {"artifact_validated", "evidence_update", "quality_gate"},
            )
            self.assertEqual(
                {event["type"] for event in sink.events_after(1)},
                {"evidence_update", "quality_gate"},
            )
            self.assertEqual(len(sink.artifact_events), 1)
            self.assertEqual(len(sink.quality_events), 3)

            waiter = asyncio.create_task(sink.wait_after(3))
            await sink.emit("render_qa", {"status": "complete"})
            latest = await waiter
            self.assertEqual([event["seq"] for event in latest], [4])

            await sink.emit(
                "agent_start", {"agent": "alpha", "display": "Alpha"}
            )
            await sink.emit(
                "agent_error",
                {"agent": "alpha", "message": "artifact contract failed"},
            )
            self.assertEqual(
                sink.agent_events["alpha"]["type"], "agent_error"
            )
            await sink.close()

        asyncio.run(scenario())

    def test_resume_repairs_truncated_tail_and_continues_sequence(self) -> None:
        async def scenario(root: Path) -> None:
            journal = root / "outputs" / "run-events.jsonl"
            journal.parent.mkdir(parents=True)
            journal.write_bytes(
                b'{"type":"run_start","seq":1,"slug":"alpha"}\n'
                b'{"type":"stage_start","seq":2,"stage":1}\n'
                b'{"type":"agent_start","seq":'
            )

            sink = WebSink(journal, append=True)
            self.assertEqual(
                [event["seq"] for event in sink.snapshot()],
                [1, 2],
            )
            self.assertEqual(sink.last_stage_event["stage"], 1)
            await sink.emit("agent_start", {"agent": "alpha"})

            restored = [
                json.loads(line)
                for line in journal.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                [event["seq"] for event in restored],
                [1, 2, 3],
            )
            self.assertEqual(sink.agent_events["alpha"]["seq"], 3)

        with tempfile.TemporaryDirectory() as tmp:
            asyncio.run(scenario(Path(tmp)))

    def test_resume_keeps_terminal_history_on_disk_without_replaying_it(self) -> None:
        async def scenario(root: Path) -> None:
            journal = root / "outputs" / "run-events.jsonl"
            journal.parent.mkdir(parents=True)
            historical = [
                {"type": "run_start", "seq": 1, "slug": "alpha"},
                {"type": "stage_start", "seq": 2, "stage": 3},
                {"type": "run_error", "seq": 3, "message": "interrupted"},
                {"type": "run_complete", "seq": 4, "slug": "alpha"},
                {"type": "stream_end", "seq": 5},
            ]
            journal.write_text(
                "".join(json.dumps(event) + "\n" for event in historical),
                encoding="utf-8",
            )

            sink = WebSink(journal, append=True)
            self.assertEqual(
                [event["type"] for event in sink.snapshot()],
                ["run_start", "stage_start"],
            )
            self.assertEqual(sink.last_stage_event["stage"], 3)

            # A resume client already caught up to the old journal should wait
            # for the resumed run instead of receiving the old stream_end.
            waiter = asyncio.create_task(sink.wait_after(5))
            await asyncio.sleep(0)
            self.assertFalse(waiter.done())
            await sink.emit("stage_start", {"stage": 4})
            resumed = await waiter
            self.assertEqual(
                [(event["type"], event["seq"]) for event in resumed],
                [("stage_start", 6)],
            )

            persisted = [
                json.loads(line)
                for line in journal.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                [(event["type"], event["seq"]) for event in persisted],
                [
                    ("run_start", 1),
                    ("stage_start", 2),
                    ("run_error", 3),
                    ("run_complete", 4),
                    ("stream_end", 5),
                    ("stage_start", 6),
                ],
            )

        with tempfile.TemporaryDirectory() as tmp:
            asyncio.run(scenario(Path(tmp)))

    def test_new_journal_truncates_prior_run(self) -> None:
        async def scenario(root: Path) -> None:
            journal = root / "run-events.jsonl"
            journal.write_text(
                '{"type":"old","seq":19}\n', encoding="utf-8"
            )
            sink = WebSink(journal)
            await sink.emit("run_start", {"slug": "new"})
            event = json.loads(journal.read_text(encoding="utf-8"))
            self.assertEqual(event["seq"], 1)
            self.assertEqual(event["slug"], "new")

        with tempfile.TemporaryDirectory() as tmp:
            asyncio.run(scenario(Path(tmp)))

    def test_lazy_new_journal_preserves_old_run_until_start_is_accepted(self) -> None:
        async def scenario(root: Path) -> None:
            journal = root / "run-events.jsonl"
            old = '{"type":"run_error","seq":8,"message":"old run"}\n'
            journal.write_text(old, encoding="utf-8")
            sink = WebSink()
            await sink.emit(
                "checkpoint",
                {"kind": "output_cleanup", "id": "review-clear"},
            )
            self.assertEqual(journal.read_text(encoding="utf-8"), old)

            sink.bind_journal(journal)
            persisted = [
                json.loads(line)
                for line in journal.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                [(event["type"], event["seq"]) for event in persisted],
                [("checkpoint", 1)],
            )

        with tempfile.TemporaryDirectory() as tmp:
            asyncio.run(scenario(Path(tmp)))

    def test_journal_failure_does_not_stop_event_stream(self) -> None:
        async def scenario(root: Path) -> None:
            blocked_parent = root / "not-a-directory"
            blocked_parent.write_text("blocked", encoding="utf-8")
            sink = WebSink(blocked_parent / "run-events.jsonl")
            await sink.emit("run_start", {"slug": "still-runs"})
            self.assertEqual(sink.snapshot()[0]["slug"], "still-runs")
            self.assertTrue(sink.journal_errors)

        with tempfile.TemporaryDirectory() as tmp:
            asyncio.run(scenario(Path(tmp)))

    def test_archive_mirror_receives_final_events_and_cleans_output_tail(self) -> None:
        async def scenario(root: Path) -> None:
            journal = root / "outputs" / "run-events.jsonl"
            archived = root / "runs" / "run" / "run-events.jsonl"
            sink = WebSink(journal)
            await sink.emit("run_start", {"slug": "alpha"})
            sink.archive_to(archived)

            # Archive cleanup occurs before the final two events in the real
            # pipeline. Recreate that order here.
            journal.unlink()
            await sink.emit("run_complete", {"archive": str(archived.parent)})
            await sink.close()

            events = [
                json.loads(line)
                for line in archived.read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(
                [event["type"] for event in events],
                ["run_start", "run_complete", "stream_end"],
            )
            self.assertFalse(journal.exists())

        with tempfile.TemporaryDirectory() as tmp:
            asyncio.run(scenario(Path(tmp)))

    def test_server_error_is_redacted_and_names_diagnostic_log(self) -> None:
        async def scenario(root: Path) -> None:
            from cli import server

            journal = root / "outputs" / "run-events.jsonl"
            sink = WebSink(journal)
            secret = "council-secret-value"
            with (
                patch.object(server, "REPO_ROOT", root),
                patch.object(
                    server,
                    "_coerce_budget",
                    side_effect=ValueError(f"bad credential {secret}"),
                ),
                patch.dict(os.environ, {"COUNCIL_TEST_TOKEN": secret}),
            ):
                await server._drive_run("new", {}, sink)
            set_sink(None)

            diagnostic = root / "logs" / "last-error.log"
            self.assertTrue(diagnostic.is_file())
            self.assertNotIn(secret, diagnostic.read_text(encoding="utf-8"))
            events = [
                json.loads(line)
                for line in journal.read_text(encoding="utf-8").splitlines()
            ]
            error = next(event for event in events if event["type"] == "run_error")
            self.assertNotIn(secret, json.dumps(error))
            self.assertEqual(error["diagnostic_log"], "logs/last-error.log")
            self.assertIn("Technical details: logs/last-error.log", error["message"])
            self.assertEqual(events[-1]["type"], "stream_end")

        with tempfile.TemporaryDirectory() as tmp:
            asyncio.run(scenario(Path(tmp)))


if __name__ == "__main__":
    unittest.main()
