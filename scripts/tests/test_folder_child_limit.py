"""Tests for folder_child_limit.py. Each test builds its own git repository, so live projects never affect them."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "folder_child_limit.py"
LIMIT = 16
GIT_IDENTITY = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


class FolderChildLimitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.git("init", "--quiet")

    def tearDown(self) -> None:
        self.directory.cleanup()

    def git(self, *arguments: str) -> None:
        subprocess.run(["git", *arguments], cwd=self.root, check=True, env={**os.environ, **GIT_IDENTITY})

    def write(self, folder: str, count: int, suffix: str = ".txt") -> None:
        (self.root / folder).mkdir(parents=True, exist_ok=True)
        for index in range(count):
            (self.root / folder / f"file{index}{suffix}").write_text("")

    def run_check(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPT), *arguments], cwd=self.root, capture_output=True, text=True)

    def test_folder_over_the_limit_is_reported(self) -> None:
        self.write("src", LIMIT + 1)
        self.write("docs", LIMIT)
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"src: {LIMIT + 1} children", result.stdout)
        self.assertNotIn("docs:", result.stdout)

    def test_ignored_third_party_and_sidecar_paths_do_not_count(self) -> None:
        (self.root / ".gitignore").write_text("node_modules/\n")
        self.write("node_modules", LIMIT + 1)
        self.write("vendor/lib", LIMIT + 1)
        self.write("assets", LIMIT)
        self.write("assets", LIMIT, suffix=".txt.meta")
        (self.root / ".folder-child-limit.json").write_text(json.dumps({"third_party": ["vendor/lib"], "sidecar_suffixes": [".meta"]}))
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_staged_blocks_only_an_added_or_grown_violation(self) -> None:
        self.write("old", LIMIT + 1)
        self.git("add", "-A")
        self.git("commit", "--quiet", "-m", "backlog")
        self.assertEqual(self.run_check("--staged").returncode, 0)

        self.write("new", LIMIT + 1)
        self.git("add", "-A")
        result = self.run_check("--staged")
        self.assertEqual(result.returncode, 1)
        self.assertIn("new:", result.stdout)
        self.assertNotIn("old:", result.stdout)

        self.git("reset", "--quiet")
        (self.root / "old" / "extra.txt").write_text("")
        self.git("add", "old/extra.txt")
        self.assertIn("old:", self.run_check("--staged").stdout)

    def test_unknown_settings_key_fails(self) -> None:
        (self.root / ".folder-child-limit.json").write_text(json.dumps({"thirdparty": ["vendor"]}))
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown keys", result.stderr)


if __name__ == "__main__":
    unittest.main()
