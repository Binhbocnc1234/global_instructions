"""Exercise installed hooks through real commits with isolated global config."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

INSTALLER = Path(__file__).resolve().parents[1] / "install_global_hooks.py"


class GlobalHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.base = Path(self.directory.name)
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.env.update(HOME=str(self.base), GIT_CONFIG_GLOBAL=str(self.base / ".gitconfig"), GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="Test", GIT_AUTHOR_EMAIL="test@example.invalid", GIT_COMMITTER_NAME="Test", GIT_COMMITTER_EMAIL="test@example.invalid")
        self.root = self.repository("existing")
        self.destination = self.base / ".agents"
        result = self.command(self.base, sys.executable, str(INSTALLER), "--destination", str(self.destination))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def command(self, cwd: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(arguments, cwd=cwd, env=self.env, capture_output=True, text=True)

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return self.command(self.root, "git", *arguments)

    def repository(self, name: str) -> Path:
        path = self.base / name
        path.mkdir()
        result = self.command(path, "git", "init", "-q")
        self.assertEqual(result.returncode, 0, result.stderr)
        return path

    def write(self, name: str, text: str) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def stage(self, *paths: str) -> None:
        result = self.git("add", "--", *paths)
        self.assertEqual(result.returncode, 0, result.stderr)

    def commit(self, succeeds: bool) -> subprocess.CompletedProcess[str]:
        result = self.git("commit", "-q", "-m", "test: verify hooks")
        if succeeds:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def test_existing_and_new_repositories(self) -> None:
        for name in ("existing", "new"):
            self.root = self.base / name if name == "existing" else self.repository(name)
            self.write("Source.py", "pass\n" * 251)
            self.stage("Source.py")
            result = self.commit(False)
            self.assertIn("251 lines", result.stdout + result.stderr)
            self.write("Source.py", "pass\n" * 250)
            self.stage("Source.py")
            self.commit(True)

    def test_index_links_not_worktree_links(self) -> None:
        self.write("Source.md", "[link](Target.md#staged)\n")
        self.write("Target.md", "# Staged\n")
        self.stage("Source.md", "Target.md")
        self.write("Source.md", "[broken](Missing.md)\n")
        self.write("Target.md", "# Unstaged\n")
        self.commit(True)
        self.stage("Source.md")
        result = self.commit(False)
        self.assertIn("Missing.md: target does not exist", result.stdout + result.stderr)
        self.write("Source.md", "[link](Target.md#unstaged)\n")
        self.stage("Source.md")
        result = self.commit(False)
        self.assertIn("heading anchor does not exist", result.stdout + result.stderr)

    def test_staged_exceptions_exclusions_and_custom_extensions(self) -> None:
        self.write("Main.custom", "line\n" * 251)
        self.write("Long.md", "paragraph\n" * 251)
        self.write("vendor/Example.md", "[bad](Missing.md)\n")
        config = {"source_extensions": [".custom"], "exclude": ["vendor"], "line_exceptions": {"Main.custom": "One generated protocol table", "Long.md": "One cohesive reference table"}}
        self.write(".agent-checks.json", json.dumps(config))
        self.stage(".")
        self.write(".agent-checks.json", "invalid json")
        self.commit(True)
        config["line_exceptions"]["Long.md"] = ""
        self.write(".agent-checks.json", json.dumps(config))
        self.stage(".agent-checks.json")
        self.assertIn("nonempty reasons", self.commit(False).stderr)

    def test_folder_limit_uses_staged_config(self) -> None:
        for index in range(17):
            self.write(f"vendor/lib/file{index}.txt", "")
        self.stage("vendor")
        result = self.commit(False)
        self.assertIn("17 children", result.stdout + result.stderr)
        self.write(".folder-child-limit.json", json.dumps({"third_party": ["vendor/lib"]}))
        self.stage(".folder-child-limit.json")
        self.write(".folder-child-limit.json", "{}")
        self.commit(True)
        self.write("new/file.txt", "")
        self.stage("new")
        self.commit(True)

    def test_local_hook_preserved_and_mutations_checked(self) -> None:
        local = self.root / ".git/hooks/pre-commit"
        local.write_text("#!/bin/sh\necho ran > local-marker\nexit 7\n", encoding="utf-8")
        local.chmod(0o755)
        self.write("Source.py", "pass\n")
        self.stage("Source.py")
        self.commit(False)
        self.assertTrue((self.root / "local-marker").exists())
        local.write_text("#!/bin/sh\nyes pass | head -n 251 > Source.py\ngit add Source.py\n", encoding="utf-8")
        result = self.commit(False)
        self.assertIn("251 lines", result.stdout + result.stderr)
        local.write_text("#!/bin/sh\necho ran > local-marker\n", encoding="utf-8")
        self.write("Source.py", "pass\n")
        self.stage("Source.py")
        self.commit(True)

    def test_installer_rejects_other_global_hook(self) -> None:
        result = self.git("config", "--global", "core.hooksPath", str(self.base / "other-hooks"))
        self.assertEqual(result.returncode, 0)
        result = self.command(self.base, sys.executable, str(INSTALLER), "--destination", str(self.destination))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("different global core.hooksPath", result.stderr)


if __name__ == "__main__":
    unittest.main()
