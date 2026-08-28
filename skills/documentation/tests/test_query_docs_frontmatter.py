from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from query_docs_frontmatter import main as query_main


class QueryDocsFrontmatterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.write_doc("Gameplay.md", "gameplay", "Defines gameplay rules.")
        self.write_doc("Technical.md", "technical", "Explains technical boundaries.")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_doc(self, name: str, doc_type: str, description: str) -> None:
        (self.root / name).write_text(
            "---\n"
            f"type: {doc_type}\n"
            "audience: agent\n"
            "status: active\n"
            "language: en\n"
            f"description: {description}\n"
            "---\n",
            encoding="utf-8",
        )

    def run_query(self, *arguments: str) -> tuple[int, str]:
        old_argv = sys.argv
        sys.argv = ["query_docs_frontmatter.py", "--root", str(self.root), *arguments]
        output = StringIO()
        try:
            with redirect_stdout(output):
                result = query_main()
        finally:
            sys.argv = old_argv
        return result, output.getvalue()

    def test_default_output_uses_readable_document_blocks(self) -> None:
        result, output = self.run_query("--audience", "agent")

        self.assertEqual(0, result)
        self.assertEqual(
            "Path: Gameplay.md\n"
            "Type: gameplay\n"
            "Description: Defines gameplay rules.\n\n"
            "Path: Technical.md\n"
            "Type: technical\n"
            "Description: Explains technical boundaries.\n",
            output,
        )

    def test_tsv_format_preserves_machine_readable_output(self) -> None:
        result, output = self.run_query("--format", "tsv", "--type", "gameplay")

        self.assertEqual(0, result)
        self.assertEqual(
            "Path\tType\tAudience\tStatus\tLanguage\tDescription\n"
            "Gameplay.md\tgameplay\tagent\tactive\ten\tDefines gameplay rules.\n",
            output,
        )


if __name__ == "__main__":
    unittest.main()
