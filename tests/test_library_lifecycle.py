from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cli.library_lifecycle import (
    ConfirmationMismatch,
    DeletePlanExpired,
    DeletePlanForbidden,
    DeletePlanStale,
    LibraryItemNotFound,
    LibraryLifecycle,
    LifecycleSafetyError,
    LifecycleTransactionError,
    MetadataValidationError,
    MutationBlocked,
)


CLIENT_ID = "library_owner_123456789"
OTHER_CLIENT_ID = "library_other_123456789"


def _write(path: Path, content: bytes | str = b"artifact") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        path.write_text(content, encoding="utf-8")
    else:
        path.write_bytes(content)
    return path


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class LibraryLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.service = LibraryLifecycle(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _report_family(self, slug: str = "airport-plan") -> dict[str, Path]:
        prompt = _write(
            self.root / "prompts" / "runs" / f"{slug}.md",
            f"# Run: {slug}\n",
        )
        source = _write(
            self.root / "sources" / "runs" / slug / "source.pdf",
            b"operator source",
        )
        _write(source.with_suffix(".pdf.extracted.md"), "Extracted source\n")

        older = self.root / "runs" / f"2026-08-20-{slug}"
        current = self.root / "runs" / f"2026-08-21-{slug}"
        for archive in (older, current):
            _write(archive / "stage3" / "final-draft.md", "# Final\n")
            _write(archive / "stage4" / f"{slug}.docx", b"archived word")
            _write(archive / "run-prompt.md", prompt.read_bytes())
            _write(
                archive / "run-manifest.json",
                json.dumps({"run": {"slug": slug}}),
            )
        revision = current / "revisions" / "v1"
        _write(revision / "final-draft.md", "# Revised\n")
        _write(revision / "stage4" / f"{slug}-revised-v1.docx", b"revision")

        reports = self.root / "reports"
        word = _write(reports / f"{slug}.docx", b"published word")
        _write(reports / f"{slug}-executive-summary.docx", b"summary")
        _write(reports / f"{slug}.pptx", b"deck")
        _write(reports / f"{slug}.docx.qa.json", "{}\n")
        pointer = _write(
            reports / f"{slug}-release-manifest.json",
            json.dumps({"slug": slug, "status": "current"}),
        )
        _write(
            reports / f"{slug}-deck-release-manifest.json",
            json.dumps({"slug": slug, "status": "current"}),
        )
        revised = f"{slug}-revised-v1"
        _write(reports / f"{revised}.docx", b"published revision")
        _write(
            reports / f"{revised}-release-manifest.json",
            json.dumps({"slug": revised, "status": "current"}),
        )
        final_word = _write(
            self.root / "final" / "Word" / f"{slug}.docx",
            b"legacy final copy",
        )

        # Both conventional and historical/nonconventional bundle names are
        # associated by the internal release slug, not a broad prefix glob.
        canonical = reports / "releases" / f"{slug}-{'a' * 12}"
        _write(
            canonical / "release-manifest.json",
            json.dumps({"slug": slug, "status": "ready"}),
        )
        _write(canonical / f"{slug}.docx", b"bundle word")
        historical = reports / "releases" / "historical-bundle-name"
        _write(
            historical / "release-manifest.json",
            json.dumps({"slug": slug, "status": "ready"}),
        )
        _write(historical / f"{slug}.docx", b"old bundle")
        revision_bundle = reports / "releases" / f"{revised}-{'b' * 12}"
        _write(
            revision_bundle / "release-manifest.json",
            json.dumps({"slug": revised, "status": "ready"}),
        )
        _write(revision_bundle / f"{revised}.docx", b"revision bundle")

        unrelated_slug = f"{slug}-other"
        unrelated = reports / "releases" / f"{unrelated_slug}-{'c' * 12}"
        _write(
            unrelated / "release-manifest.json",
            json.dumps({"slug": unrelated_slug, "status": "ready"}),
        )
        _write(reports / f"{unrelated_slug}.docx", b"do not move")
        _write(
            self.root / "runs" / f"2026-08-21-{unrelated_slug}" / "keep.txt",
            b"keep",
        )

        return {
            "prompt": prompt,
            "source": source,
            "older": older,
            "current": current,
            "word": word,
            "pointer": pointer,
            "canonical": canonical,
            "historical": historical,
            "revision_bundle": revision_bundle,
            "final_word": final_word,
            "unrelated": unrelated,
        }

    def test_metadata_sidecar_does_not_change_evidence_or_release_bytes(self) -> None:
        paths = self._report_family()
        immutable = [
            paths["prompt"],
            paths["current"] / "run-manifest.json",
            paths["word"],
            paths["pointer"],
            paths["canonical"] / "release-manifest.json",
        ]
        before = {path: _digest(path) for path in immutable}

        saved = self.service.update_metadata(
            "report",
            "airport-plan",
            {
                "title": "A clearer airport plan",
                "summary": "The decision, the evidence, and the bounded next step.",
                "tags": ["Capital", "Board", "capital"],
            },
        )

        self.assertEqual(saved["title"], "A clearer airport plan")
        self.assertEqual(saved["tags"], ["Capital", "Board"])
        self.assertEqual(
            self.service.read_metadata("report", "airport-plan"), saved
        )
        self.assertEqual(before, {path: _digest(path) for path in immutable})
        metadata = (
            self.root
            / ".council-state"
            / "library"
            / "metadata"
            / "report"
            / "airport-plan.json"
        )
        self.assertTrue(metadata.is_file())

        summary_only = self.service.update_metadata(
            "scope", "terminal-study", {"summary": "A scoped engagement."}
        )
        self.assertNotIn("title", summary_only)
        self.assertEqual(
            self.service.read_metadata("scope", "terminal-study"),
            summary_only,
        )
        # The sidecar is a partial overlay: applying a summary-only edit to a
        # Library entry must leave the title derived from immutable artifacts.
        derived_display = {"title": "Terminal Study"}
        display_fields = {
            key: value
            for key, value in summary_only.items()
            if key in {"title", "summary", "tags"}
        }
        visible_entry = {**derived_display, **display_fields}
        self.assertEqual(visible_entry["title"], "Terminal Study")
        self.assertEqual(visible_entry["summary"], "A scoped engagement.")

        with self.assertRaises(MetadataValidationError):
            self.service.update_metadata(
                "report", "airport-plan", {"title": "bad\nvalue"}
            )
        with self.assertRaises(MetadataValidationError):
            self.service.update_metadata(
                "report", "airport-plan", {"unexpected": "field"}
            )

    def test_report_inventory_is_whole_family_and_exact_prefix_safe(self) -> None:
        paths = self._report_family()
        self.service.update_metadata(
            "report", "airport-plan", {"title": "Airport plan"}
        )
        self.service.update_metadata(
            "revision",
            "airport-plan-revised-v1",
            {"title": "Airport plan revision"},
        )

        inventory = self.service.inventory(
            "revision", "airport-plan-revised-v1"
        )
        relative = {target.relative_path for target in inventory.targets}

        self.assertEqual(inventory.family_mode, "report")
        self.assertEqual(inventory.family_slug, "airport-plan")
        self.assertEqual(
            inventory.revision_slugs, ("airport-plan-revised-v1",)
        )
        for path in (
            paths["prompt"],
            paths["source"].parent,
            paths["older"],
            paths["current"],
            paths["word"],
            paths["pointer"],
            paths["canonical"],
            paths["historical"],
            paths["revision_bundle"],
            paths["final_word"],
        ):
            self.assertIn(path.relative_to(self.root).as_posix(), relative)

        self.assertNotIn(
            paths["unrelated"].relative_to(self.root).as_posix(), relative
        )
        self.assertNotIn("reports/airport-plan-other.docx", relative)
        self.assertNotIn("runs/2026-08-21-airport-plan-other", relative)
        with self.assertRaises(LibraryItemNotFound):
            self.service.inventory("revision", "airport-plan-revised-v99")

    def test_numbered_legacy_exports_require_hash_or_explicit_ownership(self) -> None:
        paths = self._report_family()
        archived_deck = _write(
            paths["current"] / "stage4" / "airport-plan.pptx",
            b"archived presentation bytes",
        )
        numbered_deck = _write(
            self.root
            / "final"
            / "PowerPoint"
            / "AI Report 101 - Airport Plan.pptx",
            archived_deck.read_bytes(),
        )
        numbered_pdf = _write(
            self.root / "final" / "PDF" / "AI Report 101 - Airport Plan.pdf",
            b"legacy rendered report",
        )
        unrelated_deck = _write(
            self.root
            / "final"
            / "PowerPoint"
            / "AI Report 101 - Airport Plan - working notes.pptx",
            b"different presentation bytes",
        )
        unrelated_pdf = _write(
            self.root
            / "final"
            / "PDF"
            / "AI Report 101 - Airport Plan - source material.pdf",
            b"different pdf bytes",
        )
        ownership = _write(
            self.root
            / ".council-state"
            / "library"
            / "ownership"
            / "report"
            / "airport-plan.json",
            json.dumps(
                {
                    "schema_version": "1.0",
                    "mode": "report",
                    "slug": "airport-plan",
                    "artifacts": [
                        {
                            "path": numbered_pdf.relative_to(self.root).as_posix(),
                            "sha256": _digest(numbered_pdf),
                            "size_bytes": numbered_pdf.stat().st_size,
                        }
                    ],
                }
            ),
        )

        inventory = self.service.inventory("report", "airport-plan")
        relative = {target.relative_path for target in inventory.targets}
        for path in (numbered_deck, numbered_pdf, ownership):
            self.assertIn(path.relative_to(self.root).as_posix(), relative)
        for path in (unrelated_deck, unrelated_pdf):
            self.assertNotIn(path.relative_to(self.root).as_posix(), relative)

        plan = self.service.create_delete_plan(
            "report", "airport-plan", client_id=CLIENT_ID
        )
        self.service.commit_delete(
            plan.plan_id,
            client_id=CLIENT_ID,
            confirmation="airport-plan",
        )
        self.assertFalse(numbered_deck.exists())
        self.assertFalse(numbered_pdf.exists())
        self.assertFalse(ownership.exists())
        self.assertTrue(unrelated_deck.is_file())
        self.assertTrue(unrelated_pdf.is_file())

    def test_builtin_legacy_index_is_exact_and_protects_primer_deck(self) -> None:
        paths = self._report_family()
        archived_deck = _write(
            paths["current"] / "stage4" / "airport-plan.pptx",
            b"shared presentation bytes",
        )
        owned_pdf = _write(
            self.root / "final" / "PDF" / "Board Edition 101.pdf",
            b"reviewed historical pdf",
        )
        owned_deck = _write(
            self.root / "final" / "PowerPoint" / "Board Edition 101.pptx",
            b"reviewed historical deck",
        )
        primer = _write(
            self.root
            / "final"
            / "PowerPoint"
            / "AI Research Council — How It Works.pptx",
            archived_deck.read_bytes(),
        )
        similarly_named = _write(
            self.root / "final" / "PDF" / "Board Edition 101 notes.pdf",
            b"operator material",
        )
        builtins = {
            "airport-plan": (
                (
                    owned_pdf.relative_to(self.root).as_posix(),
                    _digest(owned_pdf),
                    owned_pdf.stat().st_size,
                ),
                (
                    owned_deck.relative_to(self.root).as_posix(),
                    _digest(owned_deck),
                    owned_deck.stat().st_size,
                ),
            )
        }

        with patch(
            "cli.library_lifecycle.BUILTIN_LEGACY_REPORT_OWNERSHIP",
            builtins,
        ):
            inventory = self.service.inventory("report", "airport-plan")
            relative = {target.relative_path for target in inventory.targets}
            self.assertIn(owned_pdf.relative_to(self.root).as_posix(), relative)
            self.assertIn(owned_deck.relative_to(self.root).as_posix(), relative)
            self.assertNotIn(primer.relative_to(self.root).as_posix(), relative)
            self.assertNotIn(
                similarly_named.relative_to(self.root).as_posix(), relative
            )

            plan = self.service.create_delete_plan(
                "report", "airport-plan", client_id=CLIENT_ID
            )
            self.service.commit_delete(
                plan.plan_id,
                client_id=CLIENT_ID,
                confirmation="airport-plan",
            )

        self.assertFalse(owned_pdf.exists())
        self.assertFalse(owned_deck.exists())
        self.assertTrue(primer.is_file())
        self.assertTrue(similarly_named.is_file())

    def test_builtin_legacy_index_blocks_when_tracked_bytes_drift(self) -> None:
        self._report_family()
        tracked = _write(
            self.root / "final" / "PDF" / "Board Edition 101.pdf",
            b"current bytes",
        )
        builtins = {
            "airport-plan": (
                (
                    tracked.relative_to(self.root).as_posix(),
                    hashlib.sha256(b"reviewed bytes").hexdigest(),
                    len(b"reviewed bytes"),
                ),
            )
        }

        with patch(
            "cli.library_lifecycle.BUILTIN_LEGACY_REPORT_OWNERSHIP",
            builtins,
        ):
            with self.assertRaises(LifecycleSafetyError):
                self.service.inventory("report", "airport-plan")

        self.assertEqual(tracked.read_bytes(), b"current bytes")

    def test_shared_legacy_source_waits_until_only_one_mode_claims_it(self) -> None:
        paths = self._report_family()
        scope_package = _write(
            self.root
            / "reports"
            / "scope-airport-plan"
            / "deliverable.docx",
            b"scope deliverable",
        )
        source_dir = paths["source"].parent

        report_inventory = self.service.inventory("report", "airport-plan")
        report_paths = {
            target.relative_path for target in report_inventory.targets
        }
        self.assertNotIn(source_dir.relative_to(self.root).as_posix(), report_paths)

        report_plan = self.service.create_delete_plan(
            "report", "airport-plan", client_id=CLIENT_ID
        )
        self.service.commit_delete(
            report_plan.plan_id,
            client_id=CLIENT_ID,
            confirmation="airport-plan",
        )
        self.assertTrue(paths["source"].is_file())
        self.assertTrue(scope_package.is_file())

        scope_inventory = self.service.inventory("scope", "airport-plan")
        scope_paths = {target.relative_path for target in scope_inventory.targets}
        self.assertIn(source_dir.relative_to(self.root).as_posix(), scope_paths)
        scope_plan = self.service.create_delete_plan(
            "scope", "airport-plan", client_id=CLIENT_ID
        )
        self.service.commit_delete(
            scope_plan.plan_id,
            client_id=CLIENT_ID,
            confirmation="airport-plan",
        )
        self.assertFalse(source_dir.exists())

    def test_plans_are_bound_expiring_confirmed_and_stale_safe(self) -> None:
        self._report_family()
        now = [1_000.0]
        service = LibraryLifecycle(
            self.root, plan_ttl_seconds=10, clock=lambda: now[0]
        )
        plan = service.create_delete_plan(
            "report", "airport-plan", client_id=CLIENT_ID
        )
        self.assertEqual(plan.confirmation, "airport-plan")
        serialized = plan.as_dict()
        expected_groups: dict[str, dict[str, int]] = {}
        for target in serialized["targets"]:
            target_path = Path(target["path"])
            self.assertFalse(target_path.is_absolute())
            self.assertNotIn("..", target_path.parts)
            group = expected_groups.setdefault(
                target["category"],
                {"targets": 0, "files": 0, "bytes": 0, "symlinks": 0},
            )
            group["targets"] += 1
            group["files"] += target["file_count"]
            group["bytes"] += target["total_bytes"]
            group["symlinks"] += target["symlink_count"]
        self.assertEqual(serialized["groups"], expected_groups)
        self.assertEqual(
            serialized["target_count"],
            sum(group["targets"] for group in expected_groups.values()),
        )
        self.assertEqual(
            serialized["file_count"],
            sum(group["files"] for group in expected_groups.values()),
        )
        self.assertEqual(
            serialized["total_bytes"],
            sum(group["bytes"] for group in expected_groups.values()),
        )
        self.assertEqual(
            serialized["symlink_count"],
            sum(group["symlinks"] for group in expected_groups.values()),
        )

        with self.assertRaises(DeletePlanForbidden):
            service.commit_delete(
                plan.plan_id,
                client_id=OTHER_CLIENT_ID,
                confirmation="airport-plan",
            )
        with self.assertRaises(ConfirmationMismatch):
            service.commit_delete(
                plan.plan_id,
                client_id=CLIENT_ID,
                confirmation="wrong",
            )

        _write(self.root / "reports" / "airport-plan.docx", b"changed bytes")
        with self.assertRaises(DeletePlanStale):
            service.commit_delete(
                plan.plan_id,
                client_id=CLIENT_ID,
                confirmation="airport-plan",
            )
        self.assertTrue((self.root / "reports" / "airport-plan.docx").is_file())

        fresh = service.create_delete_plan(
            "report", "airport-plan", client_id=CLIENT_ID
        )
        now[0] += 11
        with self.assertRaises(DeletePlanExpired):
            service.commit_delete(
                fresh.plan_id,
                client_id=CLIENT_ID,
                confirmation="airport-plan",
            )

    def test_permanent_delete_reclaims_entire_verified_family(self) -> None:
        paths = self._report_family()
        plan = self.service.create_delete_plan(
            "report",
            "airport-plan",
            client_id=CLIENT_ID,
            permanent=True,
        )
        targets = [self.root / target.relative_path for target in plan.inventory.targets]

        self.assertTrue(plan.permanent)
        self.assertFalse(plan.as_dict()["recoverable"])
        receipt = self.service.commit_delete(
            plan.plan_id,
            client_id=CLIENT_ID,
            confirmation=plan.confirmation,
        )

        serialized = receipt.as_dict()
        self.assertFalse(serialized["recoverable"])
        self.assertTrue(serialized["permanent"])
        self.assertFalse(serialized["cleanup_pending"])
        self.assertEqual(serialized["reclaimed_bytes"], plan.inventory.total_bytes)
        self.assertTrue(all(not path.exists() for path in targets))
        self.assertTrue(paths["unrelated"].is_dir())
        self.assertFalse(
            (self.service.trash_root / serialized["receipt_id"]).exists()
        )
        self.assertEqual(self.service.recover_pending_transactions(), [])

    def test_interrupted_permanent_cleanup_finishes_on_recovery(self) -> None:
        self._report_family()
        plan = self.service.create_delete_plan(
            "report",
            "airport-plan",
            client_id=CLIENT_ID,
            permanent=True,
        )
        with patch(
            "cli.library_lifecycle.shutil.rmtree",
            side_effect=OSError("simulated busy filesystem"),
        ):
            receipt = self.service.commit_delete(
                plan.plan_id,
                client_id=CLIENT_ID,
                confirmation=plan.confirmation,
            )

        serialized = receipt.as_dict()
        receipt_id = serialized["receipt_id"]
        journal = self.service.purge_journal_root / f"{receipt_id}.json"
        self.assertTrue(serialized["cleanup_pending"])
        self.assertTrue((self.service.trash_root / receipt_id).is_dir())
        self.assertTrue(journal.is_file())
        self.assertEqual(
            self.service.recover_pending_transactions(),
            [receipt_id],
        )
        self.assertFalse((self.service.trash_root / receipt_id).exists())
        self.assertFalse(journal.exists())
        self.assertEqual(self.service.recover_pending_transactions(), [])

    def test_active_and_interrupted_run_guards_block_without_mutation(self) -> None:
        self._report_family()
        with self.assertRaises(MutationBlocked):
            self.service.create_delete_plan(
                "report",
                "airport-plan",
                client_id=CLIENT_ID,
                active_run=True,
            )
        with self.assertRaises(MutationBlocked):
            self.service.create_delete_plan(
                "report",
                "airport-plan",
                client_id=CLIENT_ID,
                interrupted_slug="airport-plan",
            )
        self.assertTrue((self.root / "reports" / "airport-plan.docx").is_file())

    def test_transaction_failure_rolls_back_every_moved_target(self) -> None:
        paths = self._report_family()
        plan = self.service.create_delete_plan(
            "report", "airport-plan", client_id=CLIENT_ID
        )
        real_replace = os.replace
        failed = [False]

        def fail_on_word(source: object, destination: object) -> None:
            source_path = Path(source)
            if (
                source_path.name == "airport-plan.docx"
                and source_path.parent.name == "reports"
                and not failed[0]
            ):
                failed[0] = True
                raise OSError("injected move failure")
            real_replace(source, destination)

        with patch("cli.library_lifecycle.os.replace", side_effect=fail_on_word):
            with self.assertRaises(LifecycleTransactionError):
                self.service.commit_delete(
                    plan.plan_id,
                    client_id=CLIENT_ID,
                    confirmation="airport-plan",
                )

        self.assertTrue(failed[0])
        for path in (
            paths["prompt"],
            paths["source"],
            paths["older"],
            paths["current"],
            paths["word"],
            paths["pointer"],
            paths["canonical"],
        ):
            self.assertTrue(path.exists() or path.is_symlink(), path)
        trash = self.root / ".council-state" / "trash" / "library"
        self.assertFalse(
            any(path.name.startswith(".pending-") for path in trash.iterdir())
        )

    def test_pending_recovery_handles_crash_before_moved_flag_is_written(self) -> None:
        paths = self._report_family()
        plan = self.service.create_delete_plan(
            "report", "airport-plan", client_id=CLIENT_ID
        )
        pending = self.service.trash_root / f".pending-{plan.plan_id}"
        payload = pending / "payload"
        payload.mkdir(parents=True)
        prompt_relative = paths["prompt"].relative_to(self.root)
        trashed_prompt = payload / prompt_relative
        trashed_prompt.parent.mkdir(parents=True)
        os.replace(paths["prompt"], trashed_prompt)
        # Simulate the narrow crash window after the filesystem move but before
        # the journal update: every target still says moved=false.
        self.service._atomic_json(
            pending / "journal.json",
            {
                "schema_version": "1.0",
                "status": "moving",
                "targets": [
                    {**target.as_dict(), "moved": False}
                    for target in plan.inventory.targets
                ],
            },
        )

        recovered = self.service.recover_pending_transactions()

        self.assertEqual(recovered, [pending.name])
        self.assertTrue(paths["prompt"].is_file())
        self.assertFalse(pending.exists())

    def test_pending_recovery_never_follows_a_payload_parent_symlink(self) -> None:
        paths = self._report_family()
        plan = self.service.create_delete_plan(
            "report", "airport-plan", client_id=CLIENT_ID
        )
        prompt_target = next(
            target
            for target in plan.inventory.targets
            if target.relative_path == "prompts/runs/airport-plan.md"
        )
        pending = self.service.trash_root / f".pending-{plan.plan_id}"
        payload = pending / "payload"
        payload.mkdir(parents=True)
        external = self.root / "not-trash"
        external_prompt = _write(
            external / "runs" / "airport-plan.md",
            paths["prompt"].read_bytes(),
        )
        paths["prompt"].unlink()
        (payload / "prompts").symlink_to(external, target_is_directory=True)
        self.service._atomic_json(
            pending / "journal.json",
            {
                "schema_version": "1.0",
                "status": "moving",
                "targets": [{**prompt_target.as_dict(), "moved": True}],
            },
        )

        with self.assertRaises(LifecycleSafetyError):
            self.service.recover_pending_transactions()

        self.assertTrue(external_prompt.is_file())
        self.assertFalse(paths["prompt"].exists())

    def test_partial_restore_recovery_is_deterministic_and_idempotent(self) -> None:
        self._report_family()
        plan = self.service.create_delete_plan(
            "report", "airport-plan", client_id=CLIENT_ID
        )
        original_digest = plan.inventory.digest
        receipt = self.service.commit_delete(
            plan.plan_id,
            client_id=CLIENT_ID,
            confirmation="airport-plan",
        )
        receipt_dir = self.service.repo_root / receipt.trash_path
        payload = receipt_dir / "payload"

        # Simulate a process death after two successful restore moves but before
        # the durable restore receipt was written.
        partially_restored = list(receipt.inventory.targets[:2])
        for target in partially_restored:
            source = payload / Path(target.relative_path)
            destination = self.service.repo_root / Path(target.relative_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(source, destination)
        self.service._atomic_json(
            receipt_dir / "restore-journal.json",
            {
                "schema_version": "1.0",
                "status": "restoring",
                "receipt_id": receipt.receipt_id,
                "targets": [
                    target.as_dict() for target in receipt.inventory.targets
                ],
            },
        )

        first = self.service.recover_pending_transactions()
        self.assertEqual(first, [receipt.receipt_id])
        self.assertEqual(
            self.service.inventory("report", "airport-plan").digest,
            original_digest,
        )
        restore_receipt = json.loads(
            (receipt_dir / "restore-receipt.json").read_text(encoding="utf-8")
        )
        self.assertTrue(restore_receipt["recovered_after_crash"])
        self.assertEqual(
            restore_receipt["target_count"], len(receipt.inventory.targets)
        )

        second = self.service.recover_pending_transactions()
        self.assertEqual(second, [])
        self.assertEqual(
            self.service.inventory("report", "airport-plan").digest,
            original_digest,
        )

    def test_delete_moves_symlink_itself_and_restore_preserves_external_target(self) -> None:
        paths = self._report_family()
        source_dir = paths["source"].parent
        shutil_target = self.root / "outside-source"
        shutil_target.mkdir()
        sentinel = _write(shutil_target / "sentinel.txt", b"outside")
        for child in source_dir.iterdir():
            child.unlink()
        source_dir.rmdir()
        source_dir.symlink_to(shutil_target, target_is_directory=True)

        plan = self.service.create_delete_plan(
            "revision", "airport-plan-revised-v1", client_id=CLIENT_ID
        )
        receipt = self.service.commit_delete(
            plan.plan_id,
            client_id=CLIENT_ID,
            confirmation="airport-plan",
        )

        self.assertFalse(source_dir.exists())
        self.assertTrue(sentinel.is_file())
        self.assertEqual(sentinel.read_bytes(), b"outside")
        self.assertFalse(paths["current"].exists())
        self.assertTrue(paths["unrelated"].is_dir())
        self.assertTrue((self.root / "reports" / "airport-plan-other.docx").is_file())
        self.assertTrue(
            (
                self.root
                / receipt.trash_path
                / "payload"
                / "sources"
                / "runs"
                / "airport-plan"
            ).is_symlink()
        )

        restored = self.service.restore(receipt.receipt_id)
        self.assertGreater(restored.target_count, 0)
        self.assertTrue(source_dir.is_symlink())
        self.assertEqual(source_dir.resolve(), shutil_target.resolve())
        self.assertEqual(sentinel.read_bytes(), b"outside")
        self.assertTrue(paths["current"].is_dir())
        self.assertTrue(paths["word"].is_file())

    def test_scope_inventory_includes_stale_and_verified_retries_only(self) -> None:
        reports = self.root / "reports"
        package = reports / "scope-terminal-study"
        _write(package / "deliverable.docx", b"scope")
        _write(reports / "terminal-study-deliverables.zip", b"zip")
        _write(reports / "scope-terminal-study-package-receipt.json", "{}")
        _write(reports / "scope-terminal-study-package-manifest.json", "{}")
        stale = reports / "scope-terminal-study.stale-20260821T123456123456"
        _write(stale / "old.docx", b"old")
        stale_zip = _write(
            reports
            / "terminal-study-deliverables.zip.stale-20260821T123456123456",
            b"old zip",
        )
        primary = self.root / "runs" / "2026-08-21-scope-terminal-study"
        _write(primary / "archive-receipt.json", json.dumps({"slug": "terminal-study"}))
        retry = self.root / "runs" / "2026-08-21-scope-terminal-study-2"
        _write(retry / "archive-receipt.json", json.dumps({"slug": "terminal-study"}))
        collision = self.root / "runs" / "2026-08-20-scope-terminal-study-2"
        _write(
            collision / "archive-receipt.json",
            json.dumps({"slug": "terminal-study-2"}),
        )
        source = _write(
            self.root / "sources" / "runs" / "terminal-study" / "scope.pdf",
            b"source",
        )

        inventory = self.service.inventory("scope", "terminal-study")
        relative = {target.relative_path for target in inventory.targets}
        for path in (package, stale, stale_zip, primary, retry, source.parent):
            self.assertIn(path.relative_to(self.root).as_posix(), relative)
        self.assertNotIn(collision.relative_to(self.root).as_posix(), relative)

    def test_strengthen_inventory_separates_public_and_source_slugs(self) -> None:
        public = "argument-data-center-risk"
        reports = self.root / "reports"
        argument = _write(reports / f"{public}.md", "Argument\n")
        memo = _write(reports / f"{public}-memo.docx", b"memo")
        pointer = _write(reports / f"{public}-release.json", "{}")
        primary = self.root / "runs" / "2026-08-21-argument-data-center-risk"
        _write(
            primary / "argument-archive.json",
            json.dumps({"slug": "data-center-risk"}),
        )
        retry = self.root / "runs" / "2026-08-21-argument-data-center-risk-2"
        _write(
            retry / "argument-archive.json",
            json.dumps({"slug": "data-center-risk"}),
        )
        collision = self.root / "runs" / "2026-08-20-argument-data-center-risk-2"
        _write(
            collision / "argument-archive.json",
            json.dumps({"slug": "data-center-risk-2"}),
        )
        source = _write(
            self.root / "sources" / "runs" / "data-center-risk" / "input.md",
            "Input\n",
        )

        inventory = self.service.inventory("strengthen", public)
        relative = {target.relative_path for target in inventory.targets}
        self.assertEqual(inventory.family_slug, "data-center-risk")
        self.assertEqual(inventory.public_slug, public)
        for path in (argument, memo, pointer, primary, retry, source.parent):
            self.assertIn(path.relative_to(self.root).as_posix(), relative)
        self.assertNotIn(collision.relative_to(self.root).as_posix(), relative)


if __name__ == "__main__":
    unittest.main()
