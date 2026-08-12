from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from cli.artifacts import ArtifactContract, validate_artifact
from cli.run_manifest import (
    APP_SHELL_PATHS,
    ResumeContractMismatch,
    generation_contract_records,
    create_run_manifest,
    update_artifact,
)


class ManifestContractTests(unittest.TestCase):
    @staticmethod
    def _source_spec(path: Path) -> SimpleNamespace:
        return SimpleNamespace(
            slug="test",
            title="Test",
            thesis="Test thesis",
            selected_research_agents=[],
            agent_overrides={},
            output_format="brief",
            want_pptx=False,
            source_paths=[str(path)],
        )

    def test_manifest_rejects_source_paths_outside_the_run_library(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = root / "outputs"
            outputs.mkdir()
            run_file = root / "prompts" / "runs" / "test.md"
            run_file.parent.mkdir(parents=True)
            run_file.write_text("# Run: Test", encoding="utf-8")
            external = root / "operator-secret.md"
            external.write_text("not attached", encoding="utf-8")

            with self.assertRaisesRegex(
                ResumeContractMismatch,
                "inside sources/runs/test",
            ):
                create_run_manifest(
                    spec=self._source_spec(external),
                    run_file=run_file,
                    outputs_dir=outputs,
                    all_agents=[],
                )

    def test_manifest_rejects_symlinks_inside_the_run_library(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = root / "outputs"
            outputs.mkdir()
            run_file = root / "prompts" / "runs" / "test.md"
            run_file.parent.mkdir(parents=True)
            run_file.write_text("# Run: Test", encoding="utf-8")
            library = root / "sources" / "runs" / "test"
            library.mkdir(parents=True)
            real = library / "real.md"
            real.write_text("approved", encoding="utf-8")
            linked = library / "linked.md"
            linked.symlink_to(real)

            with self.assertRaisesRegex(
                ResumeContractMismatch,
                "symlink",
            ):
                create_run_manifest(
                    spec=self._source_spec(linked),
                    run_file=run_file,
                    outputs_dir=outputs,
                    all_agents=[],
                )

    def test_manifest_fingerprints_agents_models_and_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = root / "outputs"
            outputs.mkdir()
            run_file = root / "prompts" / "runs" / "test.md"
            run_file.parent.mkdir(parents=True)
            run_file.write_text("# Run: Test", encoding="utf-8")
            research_prompt = root / "alpha.md"
            process_prompt = root / "strategist.md"
            research_prompt.write_text("research charter", encoding="utf-8")
            process_prompt.write_text("strategy charter", encoding="utf-8")
            agents = [
                SimpleNamespace(
                    name="alpha",
                    display_name="Alpha",
                    provider="anthropic",
                    model_override=None,
                    path=research_prompt,
                ),
                SimpleNamespace(
                    name="strategist",
                    display_name="Strategist",
                    provider="anthropic",
                    model_override=None,
                    path=process_prompt,
                ),
            ]
            spec = SimpleNamespace(
                slug="test",
                title="Test",
                thesis="Test thesis",
                selected_research_agents=["alpha"],
                agent_overrides={},
                output_format="brief",
                want_pptx=False,
                source_paths=[],
                decision_required="Choose a path",
                decision_owner="CEO",
            )
            step = SimpleNamespace(
                id="strategist-v1",
                phase="synthesis",
                agent="strategist",
                model_role="synthesis",
                inputs=("stage1/*-brief.md",),
                output="stage2/strategist-draft-v1.md",
                quality_gate="typed_artifact",
            )
            path = create_run_manifest(
                spec=spec,
                run_file=run_file,
                outputs_dir=outputs,
                all_agents=agents,
                pipeline_steps=[step],
                model_assignments={
                    "research": "research-model",
                    "synthesis": "synthesis-model",
                },
            )
            payload = json.loads(path.read_text())
            selected = payload["selected_research_agents"][0]
            self.assertEqual(selected["model_id"], "research-model")
            self.assertEqual(len(selected["prompt_sha256"]), 64)
            self.assertEqual(
                payload["pipeline"]["steps"][0]["model_id"], "synthesis-model"
            )
            visual = next(
                artifact
                for artifact in payload["artifacts"]
                if artifact["id"] == "stage4/visual-brief"
            )
            self.assertEqual(visual["status"], "skipped")
            artifact_ids = {artifact["id"] for artifact in payload["artifacts"]}
            self.assertIn("stage3/editor-notes", artifact_ids)
            self.assertIn("stage4/word-report", artifact_ids)
            self.assertIn("stage4/executive-summary", artifact_ids)

            output = outputs / "stage2" / "strategist-draft-v1.md"
            output.parent.mkdir(parents=True)
            output.write_text(" ".join(["draft"] * 30), encoding="utf-8")
            validation = validate_artifact(
                output, ArtifactContract("markdown", min_words=20)
            )
            update_artifact(path, output, validation)
            refreshed = json.loads(path.read_text())
            artifact = next(
                item
                for item in refreshed["artifacts"]
                if item["path"] == "stage2/strategist-draft-v1.md"
            )
            self.assertEqual(artifact["status"], "complete")
            self.assertEqual(len(artifact["sha256"]), 64)

            # An unchanged executable contract may resume and retain artifact
            # completion metadata.
            resumed = create_run_manifest(
                spec=spec,
                run_file=run_file,
                outputs_dir=outputs,
                all_agents=agents,
                resume=True,
                pipeline_steps=[step],
                model_assignments={
                    "research": "research-model",
                    "synthesis": "synthesis-model",
                },
            )
            resumed_payload = json.loads(resumed.read_text())
            self.assertEqual(
                resumed_payload["run"]["resume_identity_sha256"],
                payload["run"]["resume_identity_sha256"],
            )

            # The same slug with changed agent instructions must not silently
            # reuse paid work.
            research_prompt.write_text(
                "changed research charter", encoding="utf-8"
            )
            with self.assertRaises(ResumeContractMismatch):
                create_run_manifest(
                    spec=spec,
                    run_file=run_file,
                    outputs_dir=outputs,
                    all_agents=agents,
                    resume=True,
                    pipeline_steps=[step],
                    model_assignments={
                        "research": "research-model",
                        "synthesis": "synthesis-model",
                    },
                )

    def test_resume_rejects_changed_local_execution_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = root / "outputs"
            outputs.mkdir()
            run_file = root / "prompts" / "runs" / "test.md"
            run_file.parent.mkdir(parents=True)
            run_file.write_text("# Run: Test", encoding="utf-8")
            research_contract = root / "prompts" / "research-contract.md"
            research_contract.write_text(
                "Evidence contract version one", encoding="utf-8"
            )
            spec = SimpleNamespace(
                slug="test",
                title="Test",
                thesis="Test thesis",
                selected_research_agents=[],
                agent_overrides={},
                output_format="brief",
                want_pptx=False,
                source_paths=[],
            )
            create_run_manifest(
                spec=spec,
                run_file=run_file,
                outputs_dir=outputs,
                all_agents=[],
            )

            research_contract.write_text(
                "Evidence contract version two", encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ResumeContractMismatch,
                "code, prompts, or design rules changed",
            ):
                create_run_manifest(
                    spec=spec,
                    run_file=run_file,
                    outputs_dir=outputs,
                    all_agents=[],
                    resume=True,
                )


if __name__ == "__main__":
    unittest.main()


class ExecutionContractScopeTests(unittest.TestCase):
    """The resume tripwire must fire on generation code, not on the app shell.

    Hashing every cli/*.py meant a WebSocket reconnect fix or a terminal menu
    tweak invalidated whatever run was mid-flight — the contract refused
    resumes over code that cannot touch a single byte of a deliverable.
    """

    @staticmethod
    def _records(*paths: str) -> list[dict[str, object]]:
        return [{"path": p, "sha256": "a" * 64, "size_bytes": 1} for p in paths]

    def test_app_shell_modules_are_excluded_from_the_binding_contract(self) -> None:
        kept = generation_contract_records(
            self._records("cli/orchestrator.py", "cli/server.py", "cli/menu.py")
        )
        self.assertEqual([r["path"] for r in kept], ["cli/orchestrator.py"])

    def test_generation_modules_stay_in_the_binding_contract(self) -> None:
        generation = (
            "cli/orchestrator.py",
            "cli/agents.py",
            "cli/docx_builder.py",
            "cli/publish.py",
            "cli/quality_gate.py",
            "cli/run_manifest.py",
            "prompts/orchestration.md",
            "CLAUDE.md",
        )
        kept = {r["path"] for r in generation_contract_records(self._records(*generation))}
        self.assertEqual(kept, set(generation))

    def test_new_cli_modules_are_blocking_until_declared_inert(self) -> None:
        # A denylist, so forgetting to classify a new module yields a loud
        # false refusal rather than a silently corrupt resume.
        kept = generation_contract_records(self._records("cli/brand_new_stage.py"))
        self.assertEqual(len(kept), 1)

    def test_every_declared_shell_path_actually_exists(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for relative in sorted(APP_SHELL_PATHS):
            with self.subTest(path=relative):
                self.assertTrue(
                    (root / relative).is_file(),
                    f"{relative} is declared inert but is not in the repo; a stale "
                    "entry silently narrows the contract",
                )
