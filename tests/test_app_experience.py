from __future__ import annotations

import re
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "cli" / "webapp" / "index.html"
APP_JS = ROOT / "cli" / "webapp" / "app.js"
STYLES = ROOT / "cli" / "webapp" / "styles.css"


class _ShellParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.nav_targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(str(values["id"]))
        if values.get("data-nav"):
            self.nav_targets.append(str(values["data-nav"]))


class AppExperienceContractTests(unittest.TestCase):
    def test_report_setup_offers_one_model_for_every_council_role(self) -> None:
        page = INDEX.read_text(encoding="utf-8")
        script = APP_JS.read_text(encoding="utf-8")
        self.assertIn('name="f-council-model" value="claude-fable-5"', page)
        self.assertIn('name="f-council-model" value="gpt-5.6-sol"', page)
        self.assertIn(
            "Every research lens, writer, reviewer, fact-checker", page
        )
        self.assertIn("council_model: selectedCouncilModel()", script)
        self.assertIn(
            '["Model", escapeHtml(councilModelMeta().label)]', script
        )

    def test_every_navigation_target_has_one_view_and_ids_are_unique(self) -> None:
        parser = _ShellParser()
        parser.feed(INDEX.read_text(encoding="utf-8"))
        duplicates = [name for name, count in Counter(parser.ids).items() if count > 1]
        views = {name.removeprefix("view-") for name in parser.ids if name.startswith("view-")}

        self.assertEqual(duplicates, [])
        self.assertTrue(set(parser.nav_targets).issubset(views))
        self.assertIn("how", views)
        self.assertIn("agents", views)
        self.assertIn("library", views)

    def test_prompt_coach_is_structurally_separate_from_launch(self) -> None:
        script = APP_JS.read_text(encoding="utf-8")
        match = re.search(
            r"async function requestPromptDraft\(\) \{(?P<body>.*?)\n\}\n\nfunction fillTextList",
            script,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        body = match.group("body")
        self.assertIn('fetch("/api/run-prompt/draft"', body)
        self.assertNotIn("startRun(", body)
        self.assertNotIn("launchNew(", body)
        self.assertNotIn("goStep(", body)

    def test_prompt_coach_reviews_every_mutable_field_and_preserves_manual_text(self) -> None:
        script = APP_JS.read_text(encoding="utf-8")
        markup = INDEX.read_text(encoding="utf-8")
        mutable_fields = {
            "title",
            "thesis",
            "operator_context",
            "decision_required",
            "decision_owner",
            "time_horizon",
            "approval_path",
            "success_measure",
            "scope",
            "avoid",
        }
        definitions = re.search(
            r"const PROMPT_FIELD_DEFINITIONS = \[(?P<body>.*?)\n\];",
            script,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(definitions)
        keys = set(re.findall(r'key: "([a-z_]+)"', definitions.group("body")))

        self.assertEqual(keys, mutable_fields)
        self.assertIn('id="coach-preview-fields"', markup)
        self.assertIn("Every active field appears below", markup)
        self.assertIn("state.promptDraftReview.forEach((change) =>", script)
        self.assertIn("fields.appendChild(row)", script)
        self.assertIn("const canApply = Boolean(proposed) && proposed !== before", script)
        self.assertIn("!change.proposed", script)
        self.assertIn("normalizedPromptFieldValue(change, live) !== change.before", script)
        self.assertIn("PROMPT_COACH_TIMEOUT_MS = 105_000", script)
        self.assertIn("gpt-5.6-sol", script)
        self.assertIn("button.disabled = busy || !state.promptCoachOk", script)
        self.assertIn("GPT-5.6 Sol · form only", markup)

    def test_narrative_is_default_and_decision_frame_is_explicit_opt_in(self) -> None:
        script = APP_JS.read_text(encoding="utf-8")
        markup = INDEX.read_text(encoding="utf-8")

        checkbox = re.search(
            r'<input(?P<attrs>[^>]*\bid="f-decision-frame-enabled"[^>]*)>',
            markup,
        )
        self.assertIsNotNone(checkbox)
        self.assertNotIn("checked", checkbox.group("attrs"))
        self.assertIn('id="decision-frame-fields" class="decision-frame-fields hidden" disabled', markup)
        self.assertIn("Add a decision frame", markup)
        self.assertIn("Narrative Feature (1,500–2,000 words)",
                      (ROOT / "cli" / "interactive.py").read_text(encoding="utf-8"))
        self.assertIn('selectedFormat: "article"', script)
        self.assertIn('format.key === "article"', script)
        self.assertIn("decision_frame_enabled: decisionFrameEnabled()", script)
        self.assertIn("!definition.decision || decisionFrameEnabled()", script)
        self.assertIn('includeDecision ? $("#f-decision").value.trim() : ""', script)
        self.assertIn("Lines of inquiry", markup)
        self.assertNotIn("each becomes a research assignment", markup)

    def test_library_edit_and_delete_are_accessible_modal_dialogs(self) -> None:
        script = APP_JS.read_text(encoding="utf-8")
        markup = INDEX.read_text(encoding="utf-8")

        for overlay in ("library-edit-overlay", "library-delete-overlay"):
            opening = re.search(
                rf'<div id="{overlay}"(?P<attrs>[^>]*)>', markup
            )
            self.assertIsNotNone(opening)
            self.assertIn('aria-hidden="true"', opening.group("attrs"))
        self.assertGreaterEqual(markup.count('role="dialog" aria-modal="true"'), 3)
        self.assertIn("function trapLibraryDialogFocus(event)", script)
        self.assertIn("element.inert = true", script)
        self.assertIn("returnFocus?.isConnected", script)
        self.assertIn('e.key === "Escape"', script)

    def test_council_cards_open_complete_accessible_profiles(self) -> None:
        script = APP_JS.read_text(encoding="utf-8")
        markup = INDEX.read_text(encoding="utf-8")
        opening = re.search(
            r'<div id="agent-profile-overlay"(?P<attrs>[^>]*)>', markup
        )
        self.assertIsNotNone(opening)
        self.assertIn('aria-hidden="true"', opening.group("attrs"))
        self.assertIn('role="dialog" aria-modal="true"', markup)
        self.assertIn('aria-labelledby="agent-profile-title"', markup)
        self.assertIn('aria-describedby="agent-profile-description"', markup)
        self.assertIn('const card = document.createElement("button")', script)
        self.assertIn('card.setAttribute("aria-haspopup", "dialog")', script)
        self.assertIn('/profile`, {', script)
        self.assertIn('headers: sourceHeaders()', script)
        self.assertIn('renderMarkdown(', script)
        self.assertIn('openLibraryDialog(overlay, trigger', script)
        self.assertIn('overlay === $("#agent-profile-overlay")', script)

    def test_agent_profile_scroller_and_loading_status_have_separate_accessibility_roles(self) -> None:
        script = APP_JS.read_text(encoding="utf-8")
        markup = INDEX.read_text(encoding="utf-8")
        body = re.search(
            r'<(?P<tag>\w+)(?P<attrs>[^>]*\bid="agent-profile-body"[^>]*)>',
            markup,
        )
        status = re.search(
            r'<(?P<tag>\w+)(?P<attrs>[^>]*\bid="agent-profile-status"[^>]*)>',
            markup,
        )

        self.assertIsNotNone(body)
        self.assertIn('tabindex="0"', body.group("attrs"))
        self.assertNotIn("aria-live", body.group("attrs"))
        self.assertIsNotNone(status)
        self.assertIn('role="status"', status.group("attrs"))
        self.assertIn('aria-live="polite"', status.group("attrs"))
        self.assertIn('$("#agent-profile-status")', script)
        opener = re.search(
            r"async function openAgentProfile\(member, trigger\) \{(?P<body>.*?)"
            r"\n\}\n\nfunction closeAgentProfile",
            script,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(opener)
        self.assertGreaterEqual(opener.group("body").count("status.textContent"), 3)
        self.assertIn('body.setAttribute("aria-busy", "true")', opener.group("body"))
        self.assertIn('body.removeAttribute("aria-busy")', opener.group("body"))

    def test_agent_profile_normalizes_hard_wrapped_markdown_before_rendering(self) -> None:
        script = APP_JS.read_text(encoding="utf-8")
        normalizer = re.search(
            r"function normalizeAgentProfileMarkdown\(markdown\) \{(?P<body>.*?)\n\}",
            script,
            flags=re.DOTALL,
        )

        self.assertIsNotNone(normalizer)
        body = normalizer.group("body")
        self.assertRegex(body, r'\.split\(["\']\\n["\']\)')
        self.assertIn("inFence", body)
        self.assertIn("structural", body)
        self.assertIn("out[out.length - 1]", body)
        self.assertIn(
            "renderMarkdown(normalizeAgentProfileMarkdown(profile), { stripInternal: false })",
            script,
        )

    def test_executive_primer_is_one_controlled_architecture(self) -> None:
        markup = INDEX.read_text(encoding="utf-8")
        match = re.search(
            r"<!-- HOW IT WORKS -->(?P<body>.*?)<!-- AGENT CATALOG -->",
            markup,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        primer = match.group("body")

        self.assertIn("Council operating model", primer)
        self.assertIn("A controlled decision system—not a chatbot.", primer)
        self.assertIn('aria-label="Control plane"', primer)
        self.assertIn("Evidence ledger", primer)
        self.assertIn('aria-label="Three descending argument streams', primer)
        self.assertIn("Code gate", primer)
        self.assertIn("No producing role controls its own gate.", primer)
        self.assertIn('class="how-release-vault"', primer)
        self.assertIn("Immutable release", primer)
        self.assertIn('aria-label="Provenance bus"', primer)

        stages = re.findall(
            r'<article class="how-stage [^"]+" data-stage="([1-4])"',
            primer,
        )
        gates = re.findall(r'class="how-gate" data-gate="([1-2])"', primer)
        self.assertEqual(stages, ["1", "2", "3", "4"])
        self.assertEqual(gates, ["1", "2"])

        summaries = re.findall(r'class="how-stage-summary">([^<]+)</p>', primer)
        self.assertEqual(markup.count('class="how-stage-summary"'), 4)
        self.assertEqual(summaries, [
            "Parallel specialists, separate briefs",
            "Arguments attacked and rewritten",
            "Material claims earn lineage",
            "Rendered packages pass inspection",
        ])
        self.assertTrue(all(3 <= len(re.findall(r"[A-Za-z]+", text)) <= 5 for text in summaries))

    def test_executive_primer_motion_matches_each_stage_concept(self) -> None:
        markup = INDEX.read_text(encoding="utf-8")
        raw_styles = STYLES.read_text(encoding="utf-8")
        styles = re.sub(r"\s+", " ", raw_styles)
        match = re.search(
            r"<!-- HOW IT WORKS -->(?P<body>.*?)<!-- AGENT CATALOG -->",
            markup,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        primer = match.group("body")

        # Eight visible independent workstreams terminate in eight briefs.
        self.assertEqual(primer.count('class="how-inquiry-line"'), 8)
        self.assertEqual(primer.count('class="how-brief-page"'), 8)
        self.assertIn("8 separate brief documents", primer)
        self.assertIn("up to 38 research roles are available", primer)

        # The three role streams retain the challenge / rewrite / challenge /
        # rewrite order in the accessible description.
        self.assertEqual(
            re.findall(r'class="how-debate-line ([^"]+)"', primer),
            ["evidence", "strategist", "executive"],
        )
        debate_label = re.search(
            r'class="how-motion-rig how-debate-rig"[^>]*aria-label="([^"]+)"',
            primer,
        )
        self.assertIsNotNone(debate_label)
        debate_label = debate_label.group(1)
        sequence = (
            "Evidence Prosecutor challenging the draft",
            "Strategist rewriting it",
            "Airport Executive Reviewer challenging the revision",
            "Strategist rewriting again",
        )
        positions = [debate_label.index(step) for step in sequence]
        self.assertEqual(positions, sorted(positions))

        # Verification uses one fast round trip. Production uses one line per
        # Office artifact, with the presentation remaining optional.
        self.assertEqual(primer.count('class="how-fact-scan"'), 1)
        self.assertEqual(
            re.findall(r'class="how-package-line ([^"]+)"', primer),
            ["word", "deck"],
        )
        self.assertIn("optional PPTX", primer)

        for animation in (
            "how-inquiry-descend",
            "how-debate-descend",
            "how-fact-bounce",
            "how-package-shimmy",
        ):
            self.assertIn(f"@keyframes {animation}", raw_styles)

        self.assertIn(
            ".how-inquiry-line, .how-debate-line, .how-package-line { "
            "animation: none !important; stroke-dasharray: none !important; "
            "stroke-dashoffset: 0 !important;",
            styles,
        )
        self.assertIn(
            ".how-brief-page { animation: none !important; opacity: 1 !important; }",
            styles,
        )
        self.assertIn(
            ".how-fact-scan { animation: none !important; opacity: 0.9 !important; "
            "transform: translateY(-34%) !important; }",
            styles,
        )

    def test_executive_primer_has_desktop_presentation_mode(self) -> None:
        styles = re.sub(r"\s+", " ", STYLES.read_text(encoding="utf-8"))
        self.assertIn(
            "@media (min-width: 1180px) and (min-height: 700px)",
            styles,
        )
        self.assertRegex(
            styles,
            r"#view-how \{ max-width: none; width: 100%; height: 100vh; "
            r"margin: 0; padding: 16px 22px; overflow: hidden; display: grid; "
            r"grid-template-rows: auto minmax\(0,1fr\) auto; gap: 8px; \}",
        )
        self.assertIn(
            ".how-architecture { min-height: 0; display: grid; "
            "grid-template-rows: 32px minmax(0,1fr) 33px; }",
            styles,
        )
        self.assertIn(
            ".how-flow-grid { min-height: 0; grid-template-columns:",
            styles,
        )
        self.assertIn("@media (prefers-reduced-motion: reduce)", styles)

    def test_application_defaults_to_a_light_accessible_palette(self) -> None:
        styles = STYLES.read_text(encoding="utf-8")
        self.assertIn("color-scheme: light", styles)
        for token in (
            "--bg: #f7f8fb",
            "--surface: #ffffff",
            "--ink: #141823",
            "--accent: #4f46e5",
            "--green: #137a52",
            "--blue: #2563eb",
            "--red: #c73b4b",
            "--amber: #8a5a14",
        ):
            self.assertIn(token, styles)
        for obsolete in ("#0a0a0c", "#0d0f14", "rgba(12,13,16,0.94)"):
            self.assertNotIn(obsolete, styles)

    def test_permanent_library_delete_copy_is_present(self) -> None:
        markup = INDEX.read_text(encoding="utf-8")
        self.assertIn("GPT-5.6 Sol · form only", markup)
        self.assertIn("Permanent deletion", markup)
        self.assertIn("This action cannot be undone", markup)
        self.assertIn("External originals are never touched", markup)

    def test_library_delete_uses_verified_plan_without_hash_typing(self) -> None:
        markup = INDEX.read_text(encoding="utf-8")
        script = APP_JS.read_text(encoding="utf-8")

        self.assertNotIn("library-delete-confirm", markup)
        self.assertNotIn('$("#library-delete-confirm").oninput', script)
        self.assertNotIn('$("#library-delete-confirm").value', script)
        delete_button = re.search(
            r'<button(?P<attrs>[^>]*\bid="library-delete-go"[^>]*)>',
            markup,
        )
        self.assertIsNotNone(delete_button)
        self.assertRegex(delete_button.group("attrs"), r"(?:^|\s)disabled(?:\s|$)")

        commit = re.search(
            r"async function commitLibraryDelete\(\) \{(?P<body>.*?)"
            r"\n\}\n\nfunction closeLibraryToast",
            script,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(commit)
        self.assertIn(
            "JSON.stringify({ plan_id: plan.plan_id, confirmation: plan.confirmation })",
            commit.group("body"),
        )
        self.assertIn("showLibraryDeletion(receipt)", commit.group("body"))
        self.assertIn("Report permanently deleted", script)

    def test_home_surfaces_a_library_recovery_failure_before_resume(self) -> None:
        script = APP_JS.read_text(encoding="utf-8")
        recovery = script.index("if (data.library_recovery_warning)")
        resume = script.index("else if (data.interrupted)", recovery)

        self.assertLess(recovery, resume)
        self.assertIn("Library recovery needs attention", script[recovery:resume])
        self.assertIn("Read-only browsing remains available", script[recovery:resume])


if __name__ == "__main__":
    unittest.main()
