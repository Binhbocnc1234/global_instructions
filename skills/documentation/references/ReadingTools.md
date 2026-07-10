# Reading & Validating Documentation Tools

This reference explains how to use the bundled Python scripts located under `scripts/` to search, navigate, inspect, and validate project documentation.

## Purpose & Workflow

Before reading full markdown documents:
1. **Query metadata** using `query_docs_frontmatter.py` to identify candidate documents.
2. **Inspect headings** using `get_markdown_headers.py` to map out sections.
3. **Follow links** using `find_related_docs.py` to traverse prerequisites or related topics.
4. **Validate frontmatter** using `validate_docs_frontmatter.py` after writing or editing documents.

---

## 1. Query Documents by Frontmatter

Use `query_docs_frontmatter.py` to find documents that match metadata filters (e.g., searching for active technical guides meant for developer audience).

```powershell
python .\.agents\skills\documentation\scripts\query_docs_frontmatter.py --audience developer --status active --language en
```

### Available Options

| Option | Description | Example |
|--------|-------------|---------|
| `--type` | Filter by document category | `--type technical` |
| `--audience` | Filter by target audience | `--audience developer` |
| `--status` | Filter by lifecycle status | `--status active` |
| `--language` | Filter by document language code | `--language en` |
| `--description-contains` | Search term within document descriptions | `--description-contains testing` |

---

## 2. Inspect Headings & Line Ranges

Use `get_markdown_headers.py` to list all H1 and H2 headings inside a document alongside their line number ranges. This script ignores headings located inside code blocks.

```powershell
python .\.agents\skills\documentation\scripts\get_markdown_headers.py .\Documentation\en\how-to\style\HowToDocumentation.md
```

### Example Output

```text
Level Header           Range
----- ------           -----
H1    Introduction     [11,25]
H2    YAML Frontmatter [81,126]
```

---

## 3. Find Related Documents (Link Traversal)

Use `find_related_docs.py` to find documents linked directly through the `related_docs` or `prerequisite_docs` fields.

```powershell
python .\.agents\skills\documentation\scripts\find_related_docs.py --id testing --root .\Documentation\en
```

### Output Categories
*   **Outgoing Links:** Other files listed under `related_docs` or `prerequisite_docs` by the selected document.
*   **Incoming Links:** Other files in the project that reference the selected document ID.

---

## 4. Validate Documentation Frontmatter

Use `validate_docs_frontmatter.py` after editing or creating any documentation. It validates all markdown files under a specified directory.

```powershell
# Validate all files under the English documentation root
python .\.agents\skills\documentation\scripts\validate_docs_frontmatter.py --root .\Documentation\en

# Validate only a specific subdirectory
python .\.agents\skills\documentation\scripts\validate_docs_frontmatter.py --root .\Documentation\en\how-to
```

### Validations Performed

*   Checks for start/end delimiters (`---`).
*   Ensures required fields are present: `type`, `audience`, `status`, `language`, `description`.
*   Validates enum constraints (e.g. `type` must be `gameplay` or `technical`; `status` must be `draft`, `active`, or `deprecated`).
*   Ensures `language` matches the folder naming conventions (`en` or `vi`).
*   Checks that links listed under `related_docs` or `prerequisite_docs` actually point to valid markdown files of the same language.
*   Ensures code/test/asset references (`related_code`, `related_tests`, `related_assets`) exist relative to the repository root.
*   Traces requirement IDs in frontmatter `requirements` to ensure they are referenced in the document body.

---

## Error Handling Reference

| Error Scenario | Corrective Action |
|----------------|-------------------|
| "File does not exist" | Verify path spelling and run command from project root directory. |
| Empty result set | Relax metadata filters on `query_docs_frontmatter.py` (e.g., omit `--audience`). |
| Validation failed | Address listed errors (e.g., add missing fields or fix broken paths) before committing. |
| Inaccurate line range | Re-run `get_markdown_headers.py` to obtain fresh line numbers for a modified document. |
