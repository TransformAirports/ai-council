from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from cli.artifacts import contract_for_path, validate_artifact
from cli.orchestrator import _required_outputs_match_manifest
from cli.run_manifest import build_dependency_fingerprint, update_artifact
from cli.scope import (
    SCOPE_EXECUTION_FILES,
    _archive_scope_run,
    _assert_scope_outputs_current,
    _file_sha256,
    _prepare_scope_state,
    _promote_scope_package,
    _scope_archive_matches,
    _scope_dependency_declaration,
    _scope_package_matches,
    _scope_step_contract_path,
    _write_scope_step_contract,
    parse_plan,
    run_scope_pipeline,
)


class ScopeIntegrityTests(unittest.TestCase):
    def _repo(self, root: Path) -> tuple[Path, Path, Path]:
        repo = root / "repo"
        base = repo / "outputs" / "scope" / "airport-study"
        base.mkdir(parents=True)
        for relative in SCOPE_EXECUTION_FILES:
            path = repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"execution contract: {relative}\n", encoding="utf-8")
        agent = repo / ".claude" / "agents" / "scope-builder.md"
        agent.parent.mkdir(parents=True)
        agent.write_text("builder charter v1\n", encoding="utf-8")
        source = repo / "sources" / "runs" / "airport-study" / "scope.md"
        source.parent.mkdir(parents=True)
        source.write_text("airport scope v1\n", encoding="utf-8")
        return repo, base, agent

    def _record_resumable_output(
        self,
        *,
        state: Path,
        base: Path,
        contract_path: Path,
        output: Path,
    ) -> tuple[str, ...]:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            " ".join(["airport"] * 260),
            encoding="utf-8",
        )
        declaration = _scope_dependency_declaration(contract_path, base)
        update_artifact(
            state,
            output,
            validate_artifact(output, contract_for_path(output)),
            artifact_id="scope/test",
            producer="scope-builder",
            dependencies=build_dependency_fingerprint(state, declaration),
        )
        return declaration

    def test_step_receipt_invalidates_source_notes_and_agent_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, base, agent = self._repo(Path(tmp))
            state = _prepare_scope_state(
                base=base, slug="airport-study", title="Airport Study"
            )
            source = repo / "sources" / "runs" / "airport-study" / "scope.md"
            output = base / "research" / "R1-brief.md"

            contract = _write_scope_step_contract(
                repo_root=repo,
                base=base,
                step_id="research-R1",
                model="research-model",
                agent_path=agent,
                input_paths=[source],
                virtual_inputs={"notes": "original"},
            )
            declaration = self._record_resumable_output(
                state=state,
                base=base,
                contract_path=contract,
                output=output,
            )
            outputs = ((output, contract_for_path(output)),)
            self.assertTrue(
                _required_outputs_match_manifest(
                    outputs, state, declaration
                )
            )

            source.write_text("airport scope v2\n", encoding="utf-8")
            with self.assertRaisesRegex(
                RuntimeError, "upstream bytes changed"
            ):
                _assert_scope_outputs_current(
                    repo_root=repo,
                    base=base,
                    state_path=state,
                    outputs=[output],
                )
            _write_scope_step_contract(
                repo_root=repo,
                base=base,
                step_id="research-R1",
                model="research-model",
                agent_path=agent,
                input_paths=[source],
                virtual_inputs={"notes": "original"},
            )
            self.assertFalse(
                _required_outputs_match_manifest(
                    outputs, state, declaration
                )
            )

            declaration = self._record_resumable_output(
                state=state,
                base=base,
                contract_path=contract,
                output=output,
            )
            _write_scope_step_contract(
                repo_root=repo,
                base=base,
                step_id="research-R1",
                model="research-model",
                agent_path=agent,
                input_paths=[source],
                virtual_inputs={"notes": "changed"},
            )
            self.assertFalse(
                _required_outputs_match_manifest(
                    outputs, state, declaration
                )
            )

            declaration = self._record_resumable_output(
                state=state,
                base=base,
                contract_path=contract,
                output=output,
            )
            agent.write_text("builder charter v2\n", encoding="utf-8")
            _write_scope_step_contract(
                repo_root=repo,
                base=base,
                step_id="research-R1",
                model="research-model",
                agent_path=agent,
                input_paths=[source],
                virtual_inputs={"notes": "changed"},
            )
            self.assertFalse(
                _required_outputs_match_manifest(
                    outputs, state, declaration
                )
            )

    def test_builder_contract_binds_plan_research_and_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, base, agent = self._repo(Path(tmp))
            plan = base / "plan.json"
            brief = base / "research" / "R1-brief.md"
            dependency = base / "deliverables" / "outline.docx"
            for path, text in (
                (plan, '{"plan":"v1"}\n'),
                (brief, "research v1\n"),
                (dependency, "dependency v1\n"),
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")

            def receipt() -> str:
                return _file_sha256(
                    _write_scope_step_contract(
                        repo_root=repo,
                        base=base,
                        step_id="build-D2",
                        model="editor-model",
                        agent_path=agent,
                        input_paths=[plan, brief, dependency],
                        virtual_inputs={"deliverable": {"id": "D2"}},
                    )
                )

            initial = receipt()
            plan.write_text('{"plan":"v2"}\n', encoding="utf-8")
            after_plan = receipt()
            brief.write_text("research v2\n", encoding="utf-8")
            after_research = receipt()
            dependency.write_text("dependency v2\n", encoding="utf-8")
            after_dependency = receipt()
            self.assertEqual(
                len({initial, after_plan, after_research, after_dependency}), 4
            )

    def test_package_and_archive_reject_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, base, _ = self._repo(Path(tmp))
            plan = parse_plan(
                json.dumps(
                    {
                        "engagement": "Airport Study",
                        "summary": "Prepare one decision package.",
                        "research_questions": [],
                        "deliverables": [
                            {
                                "id": "D1",
                                "title": "Decision package",
                                "kind": "docx",
                                "filename": "decision-package.docx",
                                "instructions": "Build the package.",
                            }
                        ],
                        "gaps": [],
                    }
                )
            )
            plan_path = base / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            (base / "plan.md").write_text("plan markdown\n", encoding="utf-8")
            qa = base / "qa-report.md"
            qa.write_text("READY FOR CLIENT REVIEW\n", encoding="utf-8")
            deliverable = base / "deliverables" / "decision-package.docx"
            deliverable.parent.mkdir(parents=True)
            deliverable.write_bytes(b"version one")
            ordered = list(plan["deliverables"])
            built = {"D1": deliverable}

            package_dir, zip_path, receipt = _promote_scope_package(
                repo_root=repo,
                base=base,
                slug="airport-study",
                plan=plan,
                ordered=ordered,
                built=built,
                qa_path=qa,
            )
            contract = _scope_step_contract_path(base, "package")
            self.assertTrue(
                _scope_package_matches(
                    receipt_path=receipt,
                    package_dir=package_dir,
                    zip_path=zip_path,
                    contract_sha256=_file_sha256(contract),
                )
            )

            deliverable.write_bytes(b"version two")
            _promote_scope_package(
                repo_root=repo,
                base=base,
                slug="airport-study",
                plan=plan,
                ordered=ordered,
                built=built,
                qa_path=qa,
            )
            self.assertEqual(
                (package_dir / "decision-package.docx").read_bytes(),
                b"version two",
            )
            (package_dir / "rogue.txt").write_text("not receipted", encoding="utf-8")
            self.assertFalse(
                _scope_package_matches(
                    receipt_path=receipt,
                    package_dir=package_dir,
                    zip_path=zip_path,
                    contract_sha256=_file_sha256(contract),
                )
            )
            (package_dir / "rogue.txt").unlink()

            archive = _archive_scope_run(
                repo_root=repo,
                base=base,
                slug="airport-study",
                title="Airport Study",
                deliverable_count=1,
                total_cost=12.34,
                package_receipt=receipt,
            )
            receipt_hash = _file_sha256(receipt)
            self.assertTrue(
                _scope_archive_matches(
                    archive, package_receipt_sha256=receipt_hash
                )
            )
            (archive / "plan.md").write_text("tampered\n", encoding="utf-8")
            self.assertFalse(
                _scope_archive_matches(
                    archive, package_receipt_sha256=receipt_hash
                )
            )
            replacement = _archive_scope_run(
                repo_root=repo,
                base=base,
                slug="airport-study",
                title="Airport Study",
                deliverable_count=1,
                total_cost=12.34,
                package_receipt=receipt,
            )
            self.assertNotEqual(replacement, archive)
            self.assertTrue(
                _scope_archive_matches(
                    replacement, package_receipt_sha256=receipt_hash
                )
            )

    def test_pipeline_wires_step_scoped_inputs_through_every_paid_stage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo, _, _ = self._repo(Path(tmp))
            agent_names = (
                "scope-planner",
                "scope-researcher",
                "scope-builder",
                "scope-qa",
            )
            agents = []
            for name in agent_names:
                path = repo / ".claude" / "agents" / f"{name}.md"
                path.write_text(f"{name} charter\n", encoding="utf-8")
                agents.append(SimpleNamespace(name=name, path=path))

            captured: dict[str, dict] = {}

            async def fake_run_agent(**kwargs):
                label = kwargs["step_label"]
                contract_path = (
                    kwargs["manifest_path"].parent
                    / kwargs["dependency_inputs"][0]
                )
                captured[label] = json.loads(
                    contract_path.read_text(encoding="utf-8")
                )
                output = kwargs["output_path"]
                output.parent.mkdir(parents=True, exist_ok=True)
                if label == "scope/plan":
                    output.write_text(
                        json.dumps(
                            {
                                "engagement": "Airport Study",
                                "summary": "Airport decision support.",
                                "client_context": "US airport authority",
                                "research_questions": [
                                    {
                                        "id": "R1",
                                        "topic": "FAA",
                                        "questions": "What applies?",
                                    }
                                ],
                                "deliverables": [
                                    {
                                        "id": "D1",
                                        "title": "Outline",
                                        "kind": "docx",
                                        "filename": "outline.docx",
                                        "depends_on": [],
                                        "instructions": "Build an outline.",
                                    },
                                    {
                                        "id": "D2",
                                        "title": "Board deck",
                                        "kind": "pptx",
                                        "filename": "board-deck.pptx",
                                        "depends_on": ["D1"],
                                        "instructions": "Build a board deck.",
                                    },
                                ],
                                "gaps": [],
                            }
                        ),
                        encoding="utf-8",
                    )
                elif label.startswith("scope/build-"):
                    member = (
                        "word/document.xml"
                        if output.suffix == ".docx"
                        else "ppt/presentation.xml"
                    )
                    with zipfile.ZipFile(output, "w") as office:
                        office.writestr("[Content_Types].xml", "<Types/>")
                        office.writestr(member, "<document/>")
                else:
                    output.write_text(
                        " ".join([label] * 300), encoding="utf-8"
                    )
                update_artifact(
                    kwargs["manifest_path"],
                    output,
                    validate_artifact(output, contract_for_path(output)),
                    artifact_id=kwargs["artifact_id"],
                    producer=kwargs["agent"].name,
                    dependencies=build_dependency_fingerprint(
                        kwargs["manifest_path"], kwargs["dependency_inputs"]
                    ),
                )
                return {"skipped": False}

            with (
                patch("cli.scope.load_all_agents", return_value=agents),
                patch("cli.scope._model", side_effect=lambda role: f"{role}-model"),
                patch("cli.scope._run_agent", side_effect=fake_run_agent),
                patch("cli.scope.emit", new=AsyncMock()),
                patch("cli.scope._notify_done"),
            ):
                result = asyncio.run(
                    run_scope_pipeline(
                        title="Airport Study",
                        notes="Board-ready output",
                        repo_root=repo,
                        auto_approve=True,
                    )
                )

            self.assertTrue(result.completed)
            self.assertEqual(
                set(captured),
                {
                    "scope/plan",
                    "scope/research-R1",
                    "scope/build-D1",
                    "scope/build-D2",
                    "scope/qa",
                },
            )

            def paths(step: str) -> set[str]:
                return {
                    item["path"] for item in captured[step]["files"]
                }

            source = "sources/runs/airport-study/scope.md"
            plan = "outputs/scope/airport-study/plan.json"
            brief = "outputs/scope/airport-study/research/R1-brief.md"
            d1 = "outputs/scope/airport-study/deliverables/outline.docx"
            d2 = "outputs/scope/airport-study/deliverables/board-deck.pptx"
            self.assertIn(source, paths("scope/plan"))
            self.assertTrue({source, plan} <= paths("scope/research-R1"))
            self.assertTrue(
                {source, plan, brief} <= paths("scope/build-D1")
            )
            self.assertTrue(
                {source, plan, brief, d1} <= paths("scope/build-D2")
            )
            self.assertTrue(
                {source, plan, d1, d2}
                <= paths("scope/qa")
            )
            package_contract = next(
                (
                    result.archive_path / "_state" / "inputs"
                ).glob("package-*.json")
            )
            package_files = {
                item["path"]
                for item in json.loads(
                    package_contract.read_text(encoding="utf-8")
                )["files"]
            }
            self.assertTrue({plan, d1, d2} <= package_files)

    def test_plan_rejects_colliding_or_unsafe_output_paths(self) -> None:
        base = {
            "research_questions": [],
            "deliverables": [
                {
                    "id": "D1",
                    "title": "One",
                    "kind": "docx",
                    "filename": "one.docx",
                    "instructions": "Build one.",
                },
                {
                    "id": "D2",
                    "title": "Two",
                    "kind": "docx",
                    "filename": "one.docx",
                    "instructions": "Build two.",
                },
            ],
        }
        with self.assertRaisesRegex(ValueError, "duplicate deliverable filename"):
            parse_plan(json.dumps(base))
        base["deliverables"][1]["filename"] = "../two.docx"
        with self.assertRaisesRegex(ValueError, "unsafe deliverable filename"):
            parse_plan(json.dumps(base))


if __name__ == "__main__":
    unittest.main()
