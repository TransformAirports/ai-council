from __future__ import annotations

import asyncio
import unittest

from cli.events import WebSink


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


if __name__ == "__main__":
    unittest.main()
