"""Exercise committed-change selection and snapshot isolation through the CLI.

The selected commands are scripted stand-ins; selection and Git export use the production runner.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RUNNER = Path(__file__).resolve().parents[1] / "checks.py"


class CheckSelectionTests(unittest.TestCase):
    def test_selection_uses_committed_paths_configuration_and_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
            env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="Test", GIT_AUTHOR_EMAIL="test@example.invalid", GIT_COMMITTER_NAME="Test", GIT_COMMITTER_EMAIL="test@example.invalid")

            def command(*arguments: str) -> subprocess.CompletedProcess[str]:
                result = subprocess.run(arguments, cwd=root, env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return result

            command("git", "init", "-q")
            command("git", "config", "core.hooksPath", str(root / "no-hooks"))
            (root / "tools").mkdir()
            shutil.copy2(RUNNER, root / "tools/checks.py")
            config = {
                "checks": {key: ["-c", f"from pathlib import Path; print('{key.upper()}:' + Path('Behavior.txt').read_text())"] for key in ("tools", "scripts")},
                "paths": {"Behavior.txt": ["tools"], "DirectTest.py": ["scripts"], "Notes.md": []},
            }
            (root / "tools/checks.json").write_text(json.dumps(config))
            (root / "Behavior.txt").write_text("base")
            (root / "DirectTest.py").write_text("pass\n")
            (root / "Notes.md").write_text("# Base\n")
            command("git", "add", ".")
            command("git", "commit", "-qm", "test: base")
            base = command("git", "rev-parse", "HEAD").stdout.strip()
            (root / "Behavior.txt").write_text("candidate")
            command("git", "add", "Behavior.txt")
            command("git", "commit", "-qm", "test: candidate")
            (root / "Behavior.txt").write_text("unstaged")
            (root / "tools/checks.json").write_text("invalid unstaged configuration")
            result = command(sys.executable, "tools/checks.py")
            self.assertIn("Selected tools: Behavior.txt (mapped)", result.stdout)
            self.assertIn("TOOLS:candidate", result.stdout)
            self.assertNotIn("Selected scripts:", result.stdout)
            self.assertNotIn("TOOLS:unstaged", result.stdout)
            (root / "tools/checks.json").write_text(json.dumps(config))
            (root / "Notes.md").write_text("# Updated\n")
            command("git", "add", "Notes.md")
            command("git", "commit", "-qm", "test: documentation")
            self.assertIn("No executable checks selected", command(sys.executable, "tools/checks.py").stdout)
            self.assertIn("TOOLS:candidate", command(sys.executable, "tools/checks.py", "--base", base).stdout)
            (root / "DirectTest.py").write_text("print('changed')\n")
            command("git", "add", "DirectTest.py")
            command("git", "commit", "-qm", "test: direct test")
            result = command(sys.executable, "tools/checks.py")
            self.assertIn("Selected scripts:", result.stdout)
            self.assertNotIn("Selected tools:", result.stdout)
            for path in ("Unmapped.py", "tools/checks.json", "tools/checks.py"):
                target = root / path
                target.write_text(target.read_text() + "\n" if target.exists() else "pass\n")
                command("git", "add", path)
                command("git", "commit", "-qm", "test: unmapped dependency")
                result = command(sys.executable, "tools/checks.py")
                self.assertIn("Selected tools:", result.stdout)
                self.assertIn("Selected scripts:", result.stdout)
                self.assertIn("unmapped; full suite", result.stdout)
            config["checks"]["tools"] = ["-c", "raise RuntimeError('selected command failed')"]
            (root / "tools/checks.json").write_text(json.dumps(config))
            command("git", "add", "tools/checks.json")
            command("git", "commit", "-qm", "test: failed check")
            result = subprocess.run([sys.executable, "tools/checks.py"], cwd=root, env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("RuntimeError: selected command failed", result.stderr)
            self.assertIn("FAILED tools:", result.stderr)
            self.assertIn("SCRIPTS:candidate", result.stdout)


if __name__ == "__main__":
    unittest.main()
