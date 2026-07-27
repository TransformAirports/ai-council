from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cli.interactive import RunSpec
from cli.runfile import (
    parse_run_file,
    render_run_file,
    resolve_run_file,
    validate_run_file,
)


class RunFileV2Tests(unittest.TestCase):
    def test_decision_frame_and_deck_mode_round_trip(self) -> None:
        spec = RunSpec(
            title="Peak-hour checkpoint decision",
            slug="peak-hour-checkpoint-decision",
            thesis="The airport should pilot a new operating model before building.",
            operator_context="Example Airport, Terminal A.",
            decision_required="Authorize a 90-day pilot",
            decision_owner="Chief Operating Officer",
            time_horizon="Before the FY28 budget decision",
            approval_path="TSA, airport police, airlines, procurement",
            success_measure="Higher throughput without more incidents",
            success_criteria=["Every load-bearing claim traces to a source"],
            selected_research_agents=[
                "operations-analyst",
                "quantitative-analyst",
                "contrarian",
            ],
            want_pptx=True,
            deck_mode="board_decision",
        )
        text = render_run_file(spec)
        self.assertIn("## Decision frame", text)
        self.assertIn("## Presentation mode", text)
        self.assertIn("quantitative-analyst", text)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / f"{spec.slug}.md").write_text(text, encoding="utf-8")
            parsed = parse_run_file(spec.slug, runs_dir=root)

        self.assertEqual(parsed.decision_required, spec.decision_required)
        self.assertEqual(parsed.decision_owner, spec.decision_owner)
        self.assertEqual(parsed.time_horizon, spec.time_horizon)
        self.assertEqual(parsed.approval_path, spec.approval_path)
        self.assertEqual(parsed.success_measure, spec.success_measure)
        self.assertTrue(parsed.want_pptx)
        self.assertEqual(parsed.deck_mode, "board_decision")
        self.assertEqual(parsed.selected_research_agents, spec.selected_research_agents)

    def test_legacy_run_defaults_to_no_deck_and_empty_decision(self) -> None:
        legacy = """# Run: Legacy

## Thesis

Legacy thesis.

## Audience

Executives.

## Tone

Direct.

## Length

4,000 words.

## Success criteria

- Supported.

## Research agent overrides

- **operations-analyst:** (default)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "legacy.md").write_text(legacy, encoding="utf-8")
            parsed = parse_run_file("legacy", runs_dir=root)

        self.assertFalse(parsed.want_pptx)
        self.assertEqual(parsed.deck_mode, "board_decision")
        self.assertEqual(parsed.decision_required, "")
        self.assertEqual(parsed.selected_research_agents, ["operations-analyst"])

    def test_template_hint_suffixes_are_machine_readable(self) -> None:
        text = """# Run: Hint headings

## Thesis

A contested claim.

## Audience

Airport executives.

## Tone

Direct.

## Length

1,000 words.

## Output format

brief

## What this is NOT

- A survey.

## What this IS

- A decision brief.

## Operator-specific framing (optional)

Example Airport.

## Decision frame (recommended)

- **Decision required:** Authorize a pilot

## Presentation mode (optional)

board_decision

## Success criteria

- The decision is explicit.

## Research agent overrides (optional — leave blank for most runs)

- **operations-analyst:** (default)
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "hint-headings.md"
            path.write_text(text, encoding="utf-8")
            parsed = parse_run_file("hint-headings", runs_dir=root)
            errors = validate_run_file(path)

        self.assertEqual(errors, [])
        self.assertEqual(parsed.operator_context, "Example Airport.")
        self.assertEqual(parsed.decision_required, "Authorize a pilot")
        self.assertTrue(parsed.want_pptx)
        self.assertEqual(parsed.selected_research_agents, ["operations-analyst"])

    def test_resolve_and_validate_reject_unready_or_outside_run(self) -> None:
        spec = RunSpec(
            title="Ready",
            slug="ready",
            thesis="A contested claim.",
            audience="Airport executives.",
            tone="Direct.",
            length="1,000 words.",
            output_format="brief",
            is_not=["A survey."],
            is_yes=["A decision brief."],
            success_criteria=["The decision is explicit."],
            selected_research_agents=["operations-analyst"],
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ready = root / "ready.md"
            ready.write_text(render_run_file(spec), encoding="utf-8")
            self.assertEqual(resolve_run_file("ready", runs_dir=root), ready.resolve())
            self.assertEqual(validate_run_file(ready), [])

            unready = root / "unready.md"
            unready.write_text("# Run: {{TITLE}}\n", encoding="utf-8")
            self.assertTrue(validate_run_file(unready))

            outside = root.parent / "outside-council-run.md"
            outside.write_text(render_run_file(spec), encoding="utf-8")
            try:
                with self.assertRaises(ValueError):
                    resolve_run_file(outside, runs_dir=root)
            finally:
                outside.unlink(missing_ok=True)

    def test_preflight_rejects_multiline_placeholder_and_comment_only_section(self) -> None:
        spec = RunSpec(
            title="Ready",
            slug="ready",
            thesis="A contested claim.",
            audience="Airport executives.",
            tone="Direct.",
            length="1,000 words.",
            output_format="brief",
            is_not=["A survey."],
            is_yes=["A decision brief."],
            success_criteria=["The decision is explicit."],
            selected_research_agents=["operations-analyst"],
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "ready.md"
            text = render_run_file(spec).replace(
                "A contested claim.",
                "{{A contested\nmultiline claim}}",
            ).replace(
                "Airport executives.",
                "<!-- audience will be added later -->",
            )
            path.write_text(text, encoding="utf-8")
            errors = validate_run_file(path)

        self.assertTrue(any("placeholders" in error for error in errors))
        self.assertTrue(any("Audience" in error for error in errors))

    def test_preflight_rejects_duplicate_unknown_and_malformed_agents(self) -> None:
        spec = RunSpec(
            title="Roster safety",
            slug="roster-safety",
            thesis="A contested claim.",
            audience="Airport executives.",
            tone="Direct.",
            length="1,000 words.",
            output_format="brief",
            is_not=["A survey."],
            is_yes=["A decision brief."],
            success_criteria=["The decision is explicit."],
            selected_research_agents=["operations-analyst"],
        )
        base = render_run_file(spec)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            duplicate = root / "duplicate.md"
            duplicate.write_text(
                base.replace(
                    "- **operations-analyst:** (default)",
                    "- **operations-analyst:** (default)\n"
                    "- **operations-analyst:** focus on queues",
                ),
                encoding="utf-8",
            )
            duplicate_errors = validate_run_file(duplicate)
            self.assertTrue(any("duplicate" in error for error in duplicate_errors))
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                parse_run_file("duplicate", runs_dir=root)

            unknown = root / "unknown.md"
            unknown.write_text(
                base.replace(
                    "operations-analyst",
                    "operation-analyst",
                ),
                encoding="utf-8",
            )
            unknown_errors = validate_run_file(unknown)
            self.assertTrue(any("unknown" in error for error in unknown_errors))
            with self.assertRaisesRegex(ValueError, "Unknown"):
                parse_run_file("unknown", runs_dir=root)

            malformed = root / "malformed.md"
            malformed.write_text(
                base.replace(
                    "- **operations-analyst:** (default)",
                    "- **operations-analyst** (default)",
                ),
                encoding="utf-8",
            )
            malformed_errors = validate_run_file(malformed)
            self.assertTrue(any("malformed" in error for error in malformed_errors))

    def test_parse_run_file_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "runs"
            root.mkdir()
            outside = root.parent / "outside.md"
            outside.write_text("# Run: Outside\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_run_file("../outside", runs_dir=root)


if __name__ == "__main__":
    unittest.main()
