"""Installer integration tests; all writes stay in temporary directories."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/install-opencode-skills.py"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        (self.repo / "scripts").mkdir(parents=True)
        (self.repo / ".agents").mkdir()
        shutil.copy2(SCRIPT, self.repo / "scripts" / SCRIPT.name)
        self.source = self.repo / "skills/engineering/example"
        self.source.mkdir(parents=True)
        (self.source / "SKILL.md").write_text("---\nname: example\ndescription: Test\n---\nOriginal\n")
        (self.source / "references").mkdir()
        (self.source / "references/guide.md").write_text("Supporting file\n")
        self.manifest = self.repo / ".agents/opencode-skills.txt"
        self.manifest.write_text("skills/engineering/example\n")
        self.destination = self.root / "installed"
        self.state = self.root / "state"

    def run_installer(self, *args, success=True):
        result = subprocess.run(
            [sys.executable, str(self.repo / "scripts" / SCRIPT.name),
             "--destination", str(self.destination), "--state-dir", str(self.state), *args],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def test_preview_does_not_write(self):
        result = self.run_installer()
        self.assertIn("Preview only", result.stdout)
        self.assertFalse(self.destination.exists())
        self.assertFalse(self.state.exists())

    def test_installs_supporting_files_and_is_idempotent(self):
        self.run_installer("--apply")
        self.assertEqual((self.destination / "example/references/guide.md").read_text(), "Supporting file\n")
        result = self.run_installer("--apply")
        self.assertIn("0 changed files", result.stdout)
        self.assertEqual(list(self.state.glob("backup-*")), [])

    def test_local_changes_refused_before_any_write(self):
        self.run_installer("--apply")
        local = self.destination / "example/SKILL.md"
        local.write_text("My local edit\n")
        (self.source / "references/guide.md").write_text("Upstream change\n")
        self.run_installer("--apply", success=False)
        self.assertEqual(local.read_text(), "My local edit\n")
        self.assertEqual((self.destination / "example/references/guide.md").read_text(), "Supporting file\n")
        self.assertEqual(list(self.state.glob("backup-*")), [])

    def test_adoption_requires_consent_and_backs_up(self):
        target = self.destination / "example"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("Previously installed\n")
        (target / "personal.txt").write_text("Keep extra files\n")
        unrelated = self.destination / "other-skill"
        unrelated.mkdir()
        (unrelated / "SKILL.md").write_text("Unrelated\n")
        (self.destination / ".venv").mkdir()
        (self.destination / "node_modules").mkdir()
        self.run_installer("--apply", success=False)
        self.run_installer("--apply", "--accept-local-changes")
        backups = list(self.state.glob("backup-*/example/SKILL.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), "Previously installed\n")
        self.assertEqual((target / "personal.txt").read_text(), "Keep extra files\n")
        self.assertEqual((unrelated / "SKILL.md").read_text(), "Unrelated\n")
        self.assertTrue((self.destination / ".venv").is_dir())
        self.assertTrue((self.destination / "node_modules").is_dir())

    def test_upstream_update_is_backed_up_without_extra_consent(self):
        self.run_installer("--apply")
        original = (self.source / "SKILL.md").read_text()
        (self.source / "SKILL.md").write_text("Updated upstream\n")
        self.run_installer("--apply")
        self.assertEqual((self.destination / "example/SKILL.md").read_text(), "Updated upstream\n")
        self.assertEqual(next(self.state.glob("backup-*/example/SKILL.md")).read_text(), original)

    def test_missing_selected_skill_prevents_writes(self):
        self.manifest.write_text(self.manifest.read_text() + "skills/engineering/missing\n")
        self.run_installer("--apply", success=False)
        self.assertFalse(self.destination.exists())

    def test_new_upstream_skill_not_installed(self):
        unselected = self.source.parent / "unselected"
        unselected.mkdir()
        (unselected / "SKILL.md").write_text("Not selected\n")
        self.run_installer("--apply")
        self.assertFalse((self.destination / "unselected").exists())

    def test_duplicate_ids_refused(self):
        self.manifest.write_text(self.manifest.read_text() * 2)
        self.run_installer("--apply", success=False)
        self.assertFalse(self.destination.exists())

    def test_symlink_skill_destination_refused(self):
        self.destination.mkdir()
        (self.destination / "example").symlink_to(self.source, target_is_directory=True)
        result = self.run_installer("--apply", "--accept-local-changes", success=False)
        self.assertIn("real directory", result.stderr)
        self.assertTrue((self.destination / "example").is_symlink())

    def test_symlink_parent_refused(self):
        target = self.destination / "example"
        target.mkdir(parents=True)
        outside = self.root / "outside"
        outside.mkdir()
        (target / "references").symlink_to(outside, target_is_directory=True)
        self.run_installer("--apply", success=False)
        self.assertEqual(list(outside.iterdir()), [])

    def test_file_at_skill_destination_refused(self):
        self.destination.mkdir()
        (self.destination / "example").write_text("Not a directory\n")
        self.run_installer("--apply", success=False)
        self.assertEqual((self.destination / "example").read_text(), "Not a directory\n")

    def test_manifest_cannot_escape_skills(self):
        self.manifest.write_text(".agents\n")
        self.run_installer("--apply", success=False)
        self.assertFalse(self.destination.exists())

    def test_old_selection_never_deletes_installed_skills(self):
        self.run_installer("--apply")
        second = self.source.parent / "second"
        second.mkdir()
        (second / "SKILL.md").write_text("Second skill\n")
        self.manifest.write_text("skills/engineering/second\n")
        self.run_installer("--apply")
        self.assertTrue((self.destination / "example/SKILL.md").is_file())
        self.assertTrue((self.destination / "second/SKILL.md").is_file())

    def test_state_tracks_installed_hashes(self):
        self.run_installer("--apply")
        saved = json.loads(next(self.state.glob("*.json")).read_text())
        self.assertEqual(saved["destination"], str(self.destination))
        self.assertEqual(len(saved["files"]), 2)


if __name__ == "__main__":
    unittest.main()
