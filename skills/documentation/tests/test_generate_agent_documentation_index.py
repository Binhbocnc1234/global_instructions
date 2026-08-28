from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
import tempfile
import unittest


SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from generate_agent_documentation_index import main as generate_main


class GenerateAgentDocumentationIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.output = self.root / "Documentation" / "AgentDocumentationIndex.md"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_doc(self, name: str, audience: str, status: str, language: str, description: str) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            "type: technical\n"
            f"audience: {audience}\n"
            f"status: {status}\n"
            f"language: {language}\n"
            f"description: {description}\n"
            "---\n",
            encoding="utf-8",
        )

    def generate(self) -> int:
        old_argv = sys.argv
        sys.argv = [
            "generate_agent_documentation_index.py",
            "--root",
            str(self.root),
            "--output",
            str(self.output),
        ]
        try:
            with redirect_stdout(StringIO()):
                return generate_main()
        finally:
            sys.argv = old_argv

    def test_index_contains_only_active_english_agent_documents(self) -> None:
        self.write_doc("Guide.md", "agent", "active", "en", "Defines the agent guide.")
        self.write_doc("Draft.md", "agent", "draft", "en", "Defines draft guidance.")
        self.write_doc("Vietnamese.md", "agent", "active", "vi", "Defines Vietnamese guidance.")
        self.write_doc("Developer.md", "developer", "active", "en", "Defines developer guidance.")
        (self.root / "README.md").write_text("No frontmatter", encoding="utf-8")

        self.assertEqual(0, self.generate())

        content = self.output.read_text(encoding="utf-8")
        self.assertIn("| [Guide.md](../Guide.md) | technical | Defines the agent guide. |", content)
        self.assertIn("| [AgentDocumentationIndex.md](AgentDocumentationIndex.md) | technical |", content)
        self.assertNotIn("Draft.md", content)
        self.assertNotIn("Vietnamese.md", content)
        self.assertNotIn("Developer.md", content)
        self.assertNotIn("README.md", content)

    def test_regeneration_keeps_a_single_entry_for_the_index(self) -> None:
        self.write_doc("Guide.md", "agent", "active", "en", "Defines the agent guide.")

        self.assertEqual(0, self.generate())
        self.assertEqual(0, self.generate())

        content = self.output.read_text(encoding="utf-8")
        self.assertEqual(1, content.count("| [AgentDocumentationIndex.md]"))


if __name__ == "__main__":
    unittest.main()
