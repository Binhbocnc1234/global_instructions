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
        self.destination = self.root / "installed"

    def run_installer(self, *options: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(self.source / "tools" / "install_agents.py"),
             "--destination", str(self.destination), *options],
            cwd=self.root, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_install_check_drift_and_reinstall_preserve_unrelated_files(self) -> None:
        self.destination.mkdir()
        untouched = {
            "rules/DestinationOnly.md": "Local-only rule.\n",
            "skills/Example.md": "Installed skill.\n",
            "tools/local.py": "Local tool.\n",
        }
        for relative, content in untouched.items():
            path = self.destination / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.run_installer("--check", expected=1)
        self.assertFalse((self.destination / "AGENTS.md").exists())
        result = self.run_installer()
        self.assertIn("Updated 3 of 3", result.stdout)
        self.assertEqual((self.destination / "AGENTS.md").read_bytes(),
                         (self.source / "AGENTS.development.md").read_bytes())
        for relative in ("rules/Example.md", "rules/Nested.md"):
            self.assertEqual((self.destination / relative).read_bytes(),
                             (self.source / relative).read_bytes())
        self.run_installer("--check")
        changed = self.destination / "rules" / "Nested.md"
        changed.write_text("Changed installed rule.\n")
        result = self.run_installer("--check", expected=1)
        self.assertIn("Nested.md", result.stderr)
        self.assertEqual(changed.read_text(), "Changed installed rule.\n")
        self.run_installer()
        self.run_installer("--check")
        result = self.run_installer()
        self.assertIn("Updated 0 of 3", result.stdout)
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
