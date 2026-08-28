from __future__ import annotations

import argparse
from pathlib import Path
import sys

from docs_tool_lib import load_docs, value_list


Row = tuple[str, str, str, str, str, str]


def field_matches(value: object, expected: str | None) -> bool:
    if not expected:
        return True
    return expected in value_list(value)


def print_readable(rows: list[Row]) -> None:
    for index, row in enumerate(rows):
        path, doc_type, _, _, _, description = row
        if index > 0:
            print()
        print(f"Path: {path}")
        print(f"Type: {doc_type}")
        print(f"Description: {description}")


def print_tsv(rows: list[Row]) -> None:
    print("Path\tType\tAudience\tStatus\tLanguage\tDescription")
    for row in rows:
        print("\t".join(row))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Query markdown documents by YAML frontmatter.")
    parser.add_argument("--root", default=".", help="Markdown root.")
    parser.add_argument("--type")
    parser.add_argument("--audience")
    parser.add_argument("--status")
    parser.add_argument("--language")
    parser.add_argument("--description-contains")
    parser.add_argument(
        "--format",
        choices=("readable", "tsv"),
        default="readable",
        help="Output format. Defaults to readable document blocks.",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Markdown root not found: {root}")
        return 1

    rows = []
    for doc in load_docs(root):
        frontmatter = doc.frontmatter
        if not field_matches(frontmatter.get("type"), args.type):
            continue
        if not field_matches(frontmatter.get("audience"), args.audience):
            continue
        if not field_matches(frontmatter.get("status"), args.status):
            continue
        if not field_matches(frontmatter.get("language"), args.language):
            continue
        description = str(frontmatter.get("description", ""))
        if args.description_contains and args.description_contains.lower() not in description.lower():
            continue

        rows.append((
            str(doc.path.relative_to(root)),
            str(frontmatter.get("type", "")),
            ", ".join(value_list(frontmatter.get("audience"))),
            str(frontmatter.get("status", "")),
            str(frontmatter.get("language", "")),
            description,
        ))

    if args.format == "tsv":
        print_tsv(rows)
    else:
        print_readable(rows)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
