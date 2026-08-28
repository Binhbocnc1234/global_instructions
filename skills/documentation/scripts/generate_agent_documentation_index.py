from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

from docs_tool_lib import MarkdownDoc, load_docs, value_list


INDEX_DESCRIPTION = "Lists every active English agent document for task-scoped documentation discovery."


def is_indexed_document(document: MarkdownDoc) -> bool:
    frontmatter = document.frontmatter
    return (
        "agent" in value_list(frontmatter.get("audience"))
        and str(frontmatter.get("status", "")).strip() == "active"
        and str(frontmatter.get("language", "")).strip() == "en"
    )


def relative_link(source: Path, target: Path) -> str:
    relative_path = os.path.relpath(target, source.parent).replace("\\", "/")
    return f"[{target.name}]({relative_path})"


def escape_table_cell(value: str) -> str:
    return " ".join(value.splitlines()).replace("|", "\\|")


def build_index(root: Path, output: Path) -> str:
    output = output.resolve()
    documents = [
        document
        for document in load_docs(root)
        if document.path.resolve() != output and is_indexed_document(document)
    ]
    documents.append(
        MarkdownDoc(
            path=output,
            frontmatter={"type": "technical", "description": INDEX_DESCRIPTION},
        )
    )
    documents.sort(key=lambda document: str(document.path.relative_to(root)).lower())

    lines = [
        "---",
        "type: technical",
        "audience: agent",
        "status: active",
        "language: en",
        f"description: {INDEX_DESCRIPTION}",
        "---",
        "",
        "# Registry contract",
        "",
        "Use this file as the canonical discovery index for active English Markdown documents intended for agents.",
        "Read the complete index before selecting documents relevant to a task. Do not run a discovery query at task time.",
        "",
        "Regenerate this index in the same change when an indexed document is added, removed, or its path, type, description, audience, status, or language changes.",
        "",
        "# Document index",
        "",
        "| Document | Type | Description |",
        "|---|---|---|",
    ]
    for document in documents:
        frontmatter = document.frontmatter
        lines.append(
            "| "
            f"{relative_link(output, document.path)} | "
            f"{escape_table_cell(str(frontmatter.get('type', '')))} | "
            f"{escape_table_cell(str(frontmatter.get('description', '')))} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Generate the canonical index of active English Markdown documents for agents."
    )
    parser.add_argument("--root", default=".", help="Project root to scan for Markdown files.")
    parser.add_argument(
        "--output",
        required=True,
        help="Path of the AgentDocumentationIndex.md file to create or replace.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    if not root.is_dir():
        print(f"Markdown root not found: {root}")
        return 1

    try:
        output.relative_to(root)
    except ValueError:
        print(f"Output path must be inside the Markdown root: {output}")
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_index(root, output), encoding="utf-8")
    print(f"Generated agent documentation index: {output}")
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
