from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cli.sources import (
    SourcePathError,
    attach_sources,
    discover_dropzone,
)


class SourceBoundaryTests(unittest.TestCase):
    def test_browser_staging_is_not_part_of_the_global_dropzone(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dropzone = root / "sources"
            staged = dropzone / ".browser-uploads" / "client" / "report"
            staged.mkdir(parents=True)
            (staged / "private.md").write_text(
                "selected only for one browser run", encoding="utf-8"
            )
            visible = dropzone / "terminal-source.md"
            visible.write_text("legacy terminal source", encoding="utf-8")

            self.assertEqual(discover_dropzone(dropzone), [visible])

    def test_dropzone_discovery_and_attachment_reject_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dropzone = root / "sources"
            dropzone.mkdir()
            outside = root / "outside.md"
            outside.write_text("not approved", encoding="utf-8")
            linked = dropzone / "linked.md"
            linked.symlink_to(outside)

            self.assertEqual(discover_dropzone(dropzone), [])
            with self.assertRaisesRegex(SourcePathError, "symlink"):
                attach_sources("secure-run", [linked], root / "outputs")

            self.assertTrue(outside.is_file())
            self.assertFalse(
                (dropzone / "runs" / "secure-run" / "linked.md").exists()
            )

    def test_symlinked_directory_cannot_escape_the_dropzone(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dropzone = root / "sources"
            external_root = root / "external"
            dropzone.mkdir()
            external_root.mkdir()
            external = external_root / "airport.md"
            external.write_text("external evidence", encoding="utf-8")
            linked_dir = dropzone / "linked-directory"
            linked_dir.symlink_to(external_root, target_is_directory=True)

            self.assertEqual(discover_dropzone(dropzone), [])
            with self.assertRaisesRegex(
                SourcePathError, "outside the approved drop zone"
            ):
                attach_sources(
                    "secure-run",
                    [linked_dir / "airport.md"],
                    root / "outputs",
                )

    def test_external_sources_require_opt_in_and_an_approved_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sources").mkdir()
            external_root = root / "operator-files"
            external_root.mkdir()
            external = external_root / "airport.md"
            external.write_text("operator evidence", encoding="utf-8")
            outputs = root / "outputs"

            with self.assertRaisesRegex(SourcePathError, "explicit opt-in"):
                attach_sources("secure-run", [external], outputs)
            with self.assertRaisesRegex(SourcePathError, "approved external root"):
                attach_sources(
                    "secure-run",
                    [external],
                    outputs,
                    allow_external=True,
                )

            attached = attach_sources(
                "secure-run",
                [external],
                outputs,
                allow_external=True,
                approved_external_roots=[external_root],
            )
            expected = (
                root / "sources" / "runs" / "secure-run" / "airport.md"
            )
            self.assertEqual(attached[0].original, expected)
            self.assertEqual(expected.read_text(encoding="utf-8"), "operator evidence")
            # Explicit external attachment copies rather than removing an
            # operator-owned file outside the Council workspace.
            self.assertTrue(external.is_file())

    def test_source_library_slug_cannot_escape_runs_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dropzone = root / "sources"
            dropzone.mkdir()
            source = dropzone / "airport.md"
            source.write_text("evidence", encoding="utf-8")

            with self.assertRaisesRegex(SourcePathError, "Unsafe"):
                attach_sources("../escape", [source], root / "outputs")


if __name__ == "__main__":
    unittest.main()
