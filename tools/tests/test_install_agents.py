"""Exercise the installer CLI with isolated source and destination directories."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]


class InstallationWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        (self.source / "tools").mkdir(parents=True)
        (self.source / "rules").mkdir()
        for name in ("install_agents.py", "compile_codex_agents.py"):
            shutil.copyfile(TOOLS / name, self.source / "tools" / name)
        (self.source / "AGENTS.md").write_text("Project brief, not global rules.\n")
        (self.source / "AGENTS.development.md").write_text("# Global rules\n@rules/Example.md\n")
        (self.source / "rules" / "Example.md").write_text("# Example\n@Nested.md\n")
        (self.source / "rules" / "Nested.md").write_text("Rule content.\n")
        skill = self.source / "skills" / "example"
        (skill / "scripts").mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: example\ndescription: Example skill.\n---\n")
        (skill / "scripts" / "run.sh").write_text("#!/bin/sh\nprintf 'example\\n'\n")
        (skill / "scripts" / "run.sh").chmod(0o755)
        (skill / "asset.bin").write_bytes(b"\x00\xff")
        (skill / "scripts" / "__pycache__").mkdir()
        (skill / "scripts" / "__pycache__" / "cached.pyc").write_bytes(b"cache")
        self.destination = self.root / "installed"

    def run_installer(self, *options: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(self.source / "tools" / "install_agents.py"),
             "--destination", str(self.destination), *options],
            cwd=self.root, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_install_check_drift_and_reinstall_remove_stale_and_preserve_unrelated_files(self) -> None:
        source_rule = self.source / "rules" / "Nested.md"
        source_content = (
            "Rule content.\n"
            "[Profile](../AGENTS.development.md#about-developer)\n"
            "[Foundation](../AGENTS.development.md)\n"
            "[Other](Other.md#section)\n"
        )
        source_rule.write_text(source_content)
        self.destination.mkdir()
        untouched = {
            "tools/local.py": "Local tool.\n",
            "skills/.trash/old/SKILL.md": "Trashed by another tool.\n",
            "skills/synced/.marker": "Written by another tool.\n",
            "skills/example/scripts/__pycache__/local.pyc": "Cache.\n",
        }
        stale = ("rules/DestinationOnly.md", "skills/removed/nested/SKILL.md")
        for relative, content in [*untouched.items(), *((name, "Old.\n") for name in stale)]:
            path = self.destination / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        result = self.run_installer("--check", expected=1)
        self.assertFalse((self.destination / "AGENTS.md").exists())
        for relative in stale:
            self.assertIn(relative, result.stderr)
            self.assertTrue((self.destination / relative).exists())
        result = self.run_installer()
        self.assertIn("Updated 6 of 6", result.stdout)
        self.assertFalse((self.destination / "rules/DestinationOnly.md").exists())
        self.assertFalse((self.destination / "skills/removed").exists())
        for relative in ("SKILL.md", "scripts/run.sh", "asset.bin"):
            self.assertEqual(
                (self.destination / "skills/example" / relative).read_bytes(),
                (self.source / "skills/example" / relative).read_bytes(),
            )
        executable = self.destination / "skills/example/scripts/run.sh"
        self.assertEqual(executable.stat().st_mode & 0o777, 0o755)
        self.assertFalse((self.destination / "skills/example/scripts/__pycache__/cached.pyc").exists())
        self.assertEqual((self.destination / "AGENTS.md").read_bytes(),
                         (self.source / "AGENTS.development.md").read_bytes())
        self.assertEqual((self.destination / "rules/Example.md").read_bytes(),
                         (self.source / "rules/Example.md").read_bytes())
        self.assertEqual(
            (self.destination / "rules/Nested.md").read_text(),
            "Rule content.\n"
            "[Profile](../AGENTS.md#about-developer)\n"
            "[Foundation](../AGENTS.md)\n"
            "[Other](Other.md#section)\n",
        )
        self.assertEqual(source_rule.read_text(), source_content)
        self.run_installer("--check")
        changed = self.destination / "rules" / "Nested.md"
        changed.write_text("Changed installed rule.\n")
        result = self.run_installer("--check", expected=1)
        self.assertIn("Nested.md", result.stderr)
        self.assertEqual(changed.read_text(), "Changed installed rule.\n")
        self.run_installer()
        self.run_installer("--check")
        result = self.run_installer()
        self.assertIn("Updated 0 of 6", result.stdout)
        executable.chmod(0o644)
        skill_document = self.destination / "skills/example/SKILL.md"
        skill_document.write_text("Changed skill.\n")
        result = self.run_installer("--check", expected=1)
        self.assertIn("run.sh", result.stderr)
        self.assertIn("SKILL.md", result.stderr)
        self.run_installer()
        self.run_installer("--check")
        self.assertEqual(executable.stat().st_mode & 0o777, 0o755)
        self.assertEqual(skill_document.read_bytes(),
                         (self.source / "skills/example/SKILL.md").read_bytes())
        for relative, content in untouched.items():
            self.assertEqual((self.destination / relative).read_text(), content)
        self.assertFalse((self.destination / "AGENTS.development.md").exists())

    def test_missing_import_fails_before_writing(self) -> None:
        (self.source / "rules" / "Nested.md").unlink()
        result = self.run_installer(expected=1)
        self.assertIn("Cannot read", result.stderr)
        self.assertFalse(self.destination.exists())

    def test_invalid_encoding_fails_before_writing(self) -> None:
        (self.source / "rules" / "Nested.md").write_bytes(b"\xff")
        self.run_installer(expected=1)
        self.assertFalse(self.destination.exists())

    def test_destination_symlink_fails_without_modifying_external_file(self) -> None:
        self.destination.mkdir()
        external = self.root / "external.md"
        external.write_text("External instructions.\n")
        (self.destination / "AGENTS.md").symlink_to(external)
        self.run_installer(expected=1)
        self.assertEqual(external.read_text(), "External instructions.\n")
        self.assertFalse((self.destination / "rules").exists())


if __name__ == "__main__":
    unittest.main()
