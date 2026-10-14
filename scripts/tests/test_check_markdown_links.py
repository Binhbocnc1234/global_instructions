"""Exercise the global checker through its command-line entry point."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check_markdown_links.py"


class CheckMarkdownLinksTests(unittest.TestCase):
    def run_checker(self, cwd: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(SCRIPT), *arguments], cwd=cwd, capture_output=True, text=True)

    def test_explicit_directory_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Target.md").write_text("# Hello, World!\n# Hello, World!\n# `Code`\nSetext\n======\n<a id=\"custom\"></a>\n", encoding="utf-8")
            (root / "asset (1).png").write_bytes(b"fixture")
            source = root / "Source.md"
            source.write_text(
                "# Local\n[local](#local)\n[heading](Target.md#hello-world)\n"
                "[duplicate](Target.md#hello-world-1)\n[code](Target.md#code)\n"
                "[setext](Target.md#setext)\n[html](Target.md#custom)\n"
                "![image](<asset (1).png>)\n![balanced](asset%20(1).png)\n"
                "[full][target]\n[target][]\n[target]\n"
                "[target]: Target.md#hello-world \"title\"\n@Target.md\n"
                "[web](https://example.invalid/no-page)\n[mail](mailto:test@example.invalid)\n"
                "`[missing](No.md)`\n```markdown\n[missing](No.md)\n@No.md\n```\n"
                "<!-- [missing](No.md) -->\n    [missing](No.md)\n", encoding="utf-8")
            result = self.run_checker(root, ".")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Checked 2 Markdown files; 0 errors.", result.stdout)
            self.assertNotIn("skipped", result.stdout.lower())
            source.write_text(source.read_text() + "[missing](No.md)\n[anchor](Target.md#absent)\n@No.md\n[x][undefined]\n", encoding="utf-8")
            result = self.run_checker(root, "Source.md")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("4 errors", result.stdout)
            self.assertIn("Source.md:24: No.md: target does not exist", result.stdout)
            self.assertIn("heading anchor does not exist", result.stdout)
            self.assertIn("undefined reference label", result.stdout)

    def test_git_default_from_another_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "Source.md").write_text("# Source\n[here](#source)\n", encoding="utf-8")
            (root / "Untracked.md").write_text("[broken](No.md)\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "Source.md"], check=True)
            nested = root / "nested"
            nested.mkdir()
            result = self.run_checker(nested)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Checked 1 Markdown files", result.stdout)
            (root / "Source.md").unlink()
            result = self.run_checker(root)
            self.assertEqual(result.returncode, 1)
            self.assertIn("checking error", result.stderr)

    def test_bad_inputs_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for arguments in ((), ("missing.md",), (".",)):
                result = self.run_checker(root, *arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
