from __future__ import annotations

import argparse
from pathlib import Path
import sys

from docs_tool_lib import (
    DOC_LINK_FIELDS,
    PATH_FIELDS,
    VALID_AUDIENCES,
    VALID_LANGUAGES,
    VALID_STATUSES,
    VALID_TYPES,
    collect_requirement_ids,
    infer_language_from_path,
    iter_markdown_docs,
    load_docs,
    parse_frontmatter,
    related_target_exists,
    value_list,
)


REQUIRED_FIELDS = ("type", "audience", "status", "language", "description")
LEGACY_FIELDS = ("related", "code")


def find_project_root(root: Path) -> Path:
    search_path = root.resolve()
    if search_path.is_file():
        search_path = search_path.parent

    for candidate in (search_path, *search_path.parents):
        if candidate.name == "Documentation":
            return candidate.parent

    return Path.cwd().resolve()


def validate_paths(
    field: str,
    values: object,
    project_root: Path,
    issues: list[tuple[str, str, str]],
    relative_path: str,
) -> None:
    project_root = project_root.resolve()

    for raw_path in value_list(values):
        path = Path(raw_path)
        if path.is_absolute():
            issues.append((relative_path, field, f"path '{raw_path}' must be relative to the project root"))
            continue

        candidate = (project_root / path).resolve()
        try:
            candidate.relative_to(project_root)
        except ValueError:
            issues.append((relative_path, field, f"path '{raw_path}' escapes the project root"))
            continue

        if not candidate.exists():
            issues.append((relative_path, field, f"path '{raw_path}' was not found from project root"))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Validate markdown YAML frontmatter.")
    parser.add_argument("--root", default=".", help="Markdown root or subdirectory.")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Markdown root not found: {root}")
        return 1

    all_docs = load_docs(root)
    project_root = find_project_root(root)
    requirement_ids = collect_requirement_ids(root)
    issues: list[tuple[str, str, str]] = []

    by_language_and_name: dict[tuple[str, str], list[Path]] = {}
    for path in iter_markdown_docs(root):
        lang = infer_language_from_path(path) or "unknown"
        filename = path.name.lower()
        by_language_and_name.setdefault((lang, filename), []).append(path)

    for (lang, filename), paths in by_language_and_name.items():
        if len(paths) > 1:
            for p in paths:
                relative_path = str(p.relative_to(root))
                other_paths = [str(o.relative_to(root)) for o in paths if o != p]
                issues.append((relative_path, "filename", f"duplicate filename '{p.name}' found in language '{lang}'; other occurrences: {', '.join(other_paths)}"))

    for path in iter_markdown_docs(root):
        frontmatter, error = parse_frontmatter(path)
        relative_path = str(path.relative_to(root))
        if error or frontmatter is None:
            issues.append((relative_path, "frontmatter", error or "invalid frontmatter"))
            continue

        for field in REQUIRED_FIELDS:
            value = frontmatter.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                issues.append((relative_path, field, "missing required field"))

        for field in LEGACY_FIELDS:
            if field in frontmatter:
                issues.append((relative_path, field, f"use typed traceability fields instead of '{field}'"))

        doc_type = str(frontmatter.get("type", ""))
        if doc_type and doc_type not in VALID_TYPES:
            issues.append((relative_path, "type", f"invalid value '{doc_type}'"))

        audience_vals = value_list(frontmatter.get("audience"))
        if len(audience_vals) > 1:
            issues.append((relative_path, "audience", f"only a single audience is allowed, found: {', '.join(audience_vals)}"))
        elif len(audience_vals) == 1:
            audience = audience_vals[0]
            if audience not in VALID_AUDIENCES:
                issues.append((relative_path, "audience", f"invalid value '{audience}'"))

        status = str(frontmatter.get("status", ""))
        if status and status not in VALID_STATUSES:
            issues.append((relative_path, "status", f"invalid value '{status}'"))

        language = str(frontmatter.get("language", ""))
        if language and language not in VALID_LANGUAGES:
            issues.append((relative_path, "language", f"invalid value '{language}'"))

        inferred_language = infer_language_from_path(path)
        if language and inferred_language and language != inferred_language:
            issues.append((relative_path, "language", f"value '{language}' does not match path language '{inferred_language}'"))

        source_doc = next((doc for doc in all_docs if doc.path == path), None)
        if source_doc and language in VALID_LANGUAGES:
            for field in DOC_LINK_FIELDS:
                for target in value_list(frontmatter.get(field)):
                    if target and not related_target_exists(target, source_doc, all_docs):
                        issues.append((relative_path, field, f"target '{target}' was not found in language '{language}'"))

        for field in PATH_FIELDS:
            validate_paths(field, frontmatter.get(field), project_root, issues, relative_path)

        for requirement_id in value_list(frontmatter.get("requirements")):
            if requirement_id not in requirement_ids:
                issues.append((relative_path, "requirements", f"id '{requirement_id}' was not found in documentation body text"))

    if issues:
        print("Path\tField\tIssue")
        for path, field, issue in sorted(issues):
            print(f"{path}\t{field}\t{issue}")
        return 2

    print(f"All markdown frontmatter is valid under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
