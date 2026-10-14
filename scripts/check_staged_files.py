#!/usr/bin/env python3
"""Check staged source line counts and local Markdown links.

.agent-checks.json may set source_extensions (replaces defaults), exclude
(repository-relative directories), and line_exceptions (path -> reason).
Markdown is always subject to the line limit unless excluded or excepted.
Only changed, nondeleted staged files are checked. Targets inside the project
are read from a temporary index snapshot, not from the working tree.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

from check_markdown_links import check

LIMIT = 250
MARKDOWN = {".md", ".markdown"}
SOURCE = {".py", ".cs", ".gd", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".sh", ".bash", ".c", ".h", ".cpp", ".hpp", ".cc", ".java", ".go", ".rs", ".rb", ".swift", ".kt", ".lua", ".vue", ".svelte"}


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(["git", "-C", str(root), *arguments], check=True, capture_output=True, text=True).stdout


def relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and value != "."


def settings(snapshot: Path) -> tuple[set[str], list[str], dict[str, str]]:
    path = snapshot / ".agent-checks.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if not isinstance(data, dict) or set(data) - {"source_extensions", "exclude", "line_exceptions"}:
        raise ValueError(".agent-checks.json: expected source_extensions, exclude, line_exceptions only")
    extensions = data.get("source_extensions", sorted(SOURCE))
    excluded = data.get("exclude", [])
    exceptions = data.get("line_exceptions", {})
    if not isinstance(extensions, list) or any(not isinstance(x, str) or not x.startswith(".") or len(x) < 2 for x in extensions):
        raise ValueError("source_extensions must be a list of dotted extensions")
    if not isinstance(excluded, list) or any(not isinstance(x, str) or not relative_path(x) for x in excluded):
        raise ValueError("exclude must contain repository-relative directory paths")
    if not isinstance(exceptions, dict) or any(not relative_path(x) or not isinstance(reason, str) or not reason.strip() for x, reason in exceptions.items()):
        raise ValueError("line_exceptions must map repository-relative paths to nonempty reasons")
    return {extension.lower() for extension in extensions} | MARKDOWN, excluded, exceptions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").strip())
        changed = [name for name in git(root, "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "-z").split("\0") if name]
        with tempfile.TemporaryDirectory(prefix="agent-precommit-") as directory:
            snapshot = Path(directory)
            git(root, "checkout-index", "--all", f"--prefix={snapshot}{os.sep}")
            extensions, excluded, exceptions = settings(snapshot)
            errors = 0
            markdown: list[Path] = []
            checked = 0
            for name in changed:
                if any(name == folder.rstrip("/") or name.startswith(folder.rstrip("/") + "/") for folder in excluded):
                    continue
                path = snapshot / name
                if path.suffix.lower() not in extensions:
                    continue
                if path.is_symlink():
                    raise ValueError(f"{name}: staged source/Markdown symlinks cannot be checked safely")
                if not path.is_file():
                    continue
                checked += 1
                count = len(path.read_text(encoding="utf-8").splitlines())
                if count > LIMIT and name not in exceptions:
                    print(f"{name}: {count} lines, limit {LIMIT}; split by responsibility or record a reason in .agent-checks.json")
                    errors += 1
                if path.suffix.lower() in MARKDOWN:
                    markdown.append(path)
            print(f"Checked {checked} staged source/Markdown files for the {LIMIT}-line limit.")
            # Keep diagnostic paths project-relative after removing the snapshot.
            previous = Path.cwd()
            try:
                os.chdir(snapshot)
                if markdown:
                    errors += check([path.relative_to(snapshot) for path in markdown])
            finally:
                os.chdir(previous)
            return 1 if errors else 0
    except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Staged check error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
