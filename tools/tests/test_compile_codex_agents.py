"""Verify import expansion and safe installation using test-owned sources."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "compile_codex_agents.py"
SPEC = importlib.util.spec_from_file_location("compile_codex_agents", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CompileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "shared" / "AGENTS.md"
        self.output = self.root / "codex" / "AGENTS.md"

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--source", str(self.source),
             "--output", str(self.output), *arguments],
            capture_output=True, text=True,
        )

    def test_nested_imports_relative_paths_order_and_duplicates(self) -> None:
        self.write("shared/AGENTS.md", "# Root\n@rules/WorkStyle.md\n@rules/Communication.md\n")
        self.write("shared/rules/WorkStyle.md", "# Work\n@nested/Detail.md\n")
        self.write("shared/rules/nested/Detail.md", "# Detail\n@../Communication.md\n")
        self.write("shared/rules/Communication.md", "# Communication\n")
        compiled = MODULE.compile_document(self.source, self.output)
        self.assertEqual(compiled.count("# Communication\n"), 1)
        self.assertLess(compiled.index("# Work\n"), compiled.index("# Detail\n"))
        self.assertLess(compiled.index("# Detail\n"), compiled.index("# Communication\n"))
        self.assertNotIn("@rules/", compiled)

    def test_table_imports_expand_after_table_and_links_rebase(self) -> None:
        self.write("shared/AGENTS.md", "| Before | Apply |\n|---|---|\n| Write | @rules/Work.md |\n\nAfter\n")
        self.write("shared/rules/Work.md", "# Work\nSee [details](../docs/Detail.md#section).\n")
        compiled = MODULE.compile_document(self.source, self.output)
        self.assertIn("| Write | [Work](<../shared/rules/Work.md>) |", compiled)
        self.assertIn("[details](../shared/docs/Detail.md#section)", compiled)
        self.assertLess(compiled.index("| Write |"), compiled.index("# Work\n"))
        self.assertLess(compiled.index("# Work\n"), compiled.index("After\n"))

    def test_code_examples_and_external_links_remain_literal(self) -> None:
        literal = (
            "`@missing.md` and ``@also-missing.md``\n"
            "```markdown\n@missing.md\n[example](example.md)\n```\n"
            "~~~\n@missing.md\n~~~\n"
            "[web](https://example.com) and [anchor](#section)\n"
        )
        self.write("shared/AGENTS.md", literal)
        self.assertIn(literal, MODULE.compile_document(self.source, self.output))

    def test_inline_import_at_eof_without_a_newline(self) -> None:
        self.write("shared/AGENTS.md", "Apply @rules/Work.md")
        self.write("shared/rules/Work.md", "# Work\nBody\n")
        compiled = MODULE.compile_document(self.source, self.output)
        self.assertIn("[Work](<../shared/rules/Work.md>)\n# Work\n", compiled)

    def test_links_with_code_in_labels_rebase_but_inline_examples_do_not(self) -> None:
        self.write("shared/AGENTS.md", "[Use `tmp/`](rules/Work.md#scratch) and `[example](example.md)`\n")
        compiled = MODULE.compile_document(self.source, self.output)
        self.assertIn("[Use `tmp/`](../shared/rules/Work.md#scratch)", compiled)
        self.assertIn("`[example](example.md)`", compiled)

    def test_cycle_reports_chain_even_for_an_already_seen_source(self) -> None:
        self.write("shared/AGENTS.md", "@rules/Work.md\n")
        self.write("shared/rules/Work.md", "@../AGENTS.md\n")
        with self.assertRaisesRegex(MODULE.CompileError, "Circular import:.*AGENTS.md.*Work.md.*AGENTS.md"):
            MODULE.compile_document(self.source, self.output)

    def test_missing_import_does_not_overwrite_existing_output(self) -> None:
        self.write("shared/AGENTS.md", "@missing.md\n")
        self.write("codex/AGENTS.md", "Existing instructions\n")
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing.md", result.stderr)
        self.assertEqual(self.output.read_text(), "Existing instructions\n")

    def test_output_cannot_overwrite_an_imported_source(self) -> None:
        self.write("shared/AGENTS.md", "@../codex/AGENTS.md\n")
        self.write("codex/AGENTS.md", "Source instructions\n")
        self.assertEqual(self.run_cli().returncode, 1)
        self.assertEqual(self.output.read_text(), "Source instructions\n")

    def test_install_and_check_detect_changed_source_without_writing(self) -> None:
        self.write("shared/AGENTS.md", "# Original\n")
        self.assertEqual(self.run_cli().returncode, 0)
        installed = self.output.read_text()
        self.assertEqual(self.run_cli("--check").returncode, 0)
        self.source.write_text("# Changed\n")
        self.assertEqual(self.run_cli("--check").returncode, 1)
        self.assertEqual(self.output.read_text(), installed)


if __name__ == "__main__":
    unittest.main()
