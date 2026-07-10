from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from validate_docs_frontmatter import main as validate_main


class DocsFrontmatterValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "Documentation" / "en").mkdir(parents=True)
        (self.root / "Assets" / "Scripts" / "Feature").mkdir(parents=True)
        (self.root / "Assets" / "Scripts" / "Tests").mkdir(parents=True)
        (self.root / "Assets" / "Scripts" / "Feature" / "Feature.cs").write_text("public class Feature {}", encoding="utf-8")
        (self.root / "Assets" / "Scripts" / "Tests" / "FeatureTests.cs").write_text("public class FeatureTests {}", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_doc(self, name: str, frontmatter: str, body: str = "") -> Path:
        path = self.root / "Documentation" / "en" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{frontmatter}---\n\n{body}", encoding="utf-8")
        return path

    def validate(self) -> int:
        import sys

        old_argv = sys.argv
        sys.argv = ["validate_docs_frontmatter.py", "--root", str(self.root / "Documentation" / "en")]
        try:
            return validate_main()
        finally:
            sys.argv = old_argv

    def test_typed_frontmatter_with_file_and_folder_paths_passes(self) -> None:
        common = (
            "type: technical\n"
            "audience: [developer, agent]\n"
            "status: active\n"
            "language: en\n"
        )
        self.write_doc(
            "Architecture.md",
            f"{common}description: Defines architecture.\n",
            "| `ARCH-DEP-001` | Runtime files must be owned. |\n",
        )
        self.write_doc(
            "Feature.md",
            f"{common}"
            "description: Explains a feature.\n"
            "prerequisite_docs:\n"
            "  - Architecture.md\n"
            "related_code:\n"
            "  - Assets/Scripts/Feature\n"
            "related_tests:\n"
            "  - Assets/Scripts/Tests/FeatureTests.cs\n"
            "requirements:\n"
            "  - ARCH-DEP-001\n",
        )

        self.assertEqual(0, self.validate())

    def test_generalized_frontmatter_values_pass(self) -> None:
        self.write_doc(
            "Runbook.md",
            "type: process\n"
            "audience: operator\n"
            "status: active\n"
            "language: en\n"
            "description: Defines the release runbook.\n",
        )

        self.assertEqual(0, self.validate())

    def test_legacy_related_field_fails(self) -> None:
        self.write_doc(
            "Feature.md",
            "type: technical\n"
            "audience: agent\n"
            "status: active\n"
            "language: en\n"
            "description: Explains a feature.\n"
            "related:\n"
            "  - missing\n",
        )

        self.assertEqual(2, self.validate())

    def test_duplicate_filenames_fail(self) -> None:
        common = (
            "type: technical\n"
            "audience: developer\n"
            "status: active\n"
            "language: en\n"
        )
        self.write_doc("folder1/Architecture.md", f"{common}description: Doc 1\n")
        self.write_doc("folder2/Architecture.md", f"{common}description: Doc 2\n")

        self.assertEqual(2, self.validate())

    def test_link_matching_by_basename_and_without_extension_passes(self) -> None:
        common = (
            "type: technical\n"
            "audience: developer\n"
            "status: active\n"
            "language: en\n"
        )
        self.write_doc("subfolder/Architecture.md", f"{common}description: Defines architecture.\n")
        self.write_doc(
            "Feature.md",
            f"{common}"
            "description: Explains a feature.\n"
            "prerequisite_docs:\n"
            "  - Architecture\n", # stem only (no extension, no relative folder path)
        )

        self.assertEqual(0, self.validate())

    def test_missing_required_fields_fail(self) -> None:
        self.write_doc(
            "Feature.md",
            "type: technical\n"
            "audience: developer\n"
            "status: active\n"
            "language: en\n"
            # description is missing
        )
        self.assertEqual(2, self.validate())

    def test_invalid_metadata_values_fail(self) -> None:
        common = (
            "audience: developer\n"
            "status: active\n"
            "language: en\n"
            "description: Test\n"
        )
        # Invalid type
        self.write_doc("Feature1.md", f"type: invalid_type\n{common}")
        self.assertEqual(2, self.validate())

    def test_language_path_mismatch_fails(self) -> None:
        self.write_doc(
            "Feature.md",
            "type: technical\n"
            "audience: developer\n"
            "status: active\n"
            "language: vi\n"  # mismatches "en" folder path
            "description: Test\n"
        )
        self.assertEqual(2, self.validate())

    def test_path_validation_failures(self) -> None:
        common = (
            "type: technical\n"
            "audience: developer\n"
            "status: active\n"
            "language: en\n"
            "description: Test\n"
        )
        # Absolute path in related_code
        self.write_doc("Feature1.md", f"{common}related_code:\n  - /absolute/path\n")
        self.assertEqual(2, self.validate())
        
        # Path escaping root
        self.write_doc("Feature2.md", f"{common}related_code:\n  - ../escaped\n")
        self.assertEqual(2, self.validate())

        # Path not found
        self.write_doc("Feature3.md", f"{common}related_code:\n  - Assets/NonExistent\n")
        self.assertEqual(2, self.validate())

    def test_requirement_id_missing_in_body_fails(self) -> None:
        self.write_doc(
            "Feature.md",
            "type: technical\n"
            "audience: developer\n"
            "status: active\n"
            "language: en\n"
            "description: Test\n"
            "requirements:\n"
            "  - MVP-DEV-1234\n",
            "No requirement ID in this body text."
        )
        self.assertEqual(2, self.validate())

    def test_missing_doc_link_fails(self) -> None:
        self.write_doc(
            "Feature.md",
            "type: technical\n"
            "audience: developer\n"
            "status: active\n"
            "language: en\n"
            "description: Test\n"
            "prerequisite_docs:\n"
            "  - NonExistentDoc.md\n",
        )
        self.assertEqual(2, self.validate())

    def test_malformed_frontmatter_fails(self) -> None:
        path = self.root / "Documentation" / "en" / "Feature.md"
        path.write_text("type: technical\nno delimiters here", encoding="utf-8")
        self.assertEqual(2, self.validate())


if __name__ == "__main__":
    unittest.main()
