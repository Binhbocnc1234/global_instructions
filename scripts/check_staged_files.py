#!/usr/bin/env python3
"""Check staged source character counts and local Markdown links.

.agent-checks.json may set source_extensions (replaces defaults), exclude (repository-relative directories), and line_exceptions (path -> reason; the existing key now excepts character counts).
Markdown is always subject to the character limit unless excluded or excepted.
Count Unicode code points in decoded UTF-8, including whitespace and newlines, without newline normalization. Exactly LIMIT_CHARACTERS passes.
Character counts cover changed, nondeleted staged files. A commit fails only for a file it puts over the limit; a file already over it in HEAD (under its old name, for a rename) is reported as a warning.
Unlike folder_child_limit.py, growth of such a file does not fail: every edit grows a file, even a link rewrite, so failing it would block every edit until the file is split. Link checks also cover incoming links to removed paths or changed Markdown targets. Repository content is read on demand from the index, never exported or read from the working tree.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

from check_markdown_links import check
from staged_snapshot import StagedSnapshot, lexical_path

LIMIT_CHARACTERS = 18_000
MARKDOWN = {".md", ".markdown"}
SOURCE = {".py", ".cs", ".gd", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".sh", ".bash", ".c", ".h", ".cpp", ".hpp", ".cc", ".java", ".go", ".rs", ".rb", ".swift", ".kt", ".lua", ".vue", ".svelte"}


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(["git", "-C", str(root), *arguments], check=True, capture_output=True, text=True).stdout


def head_characters(root: Path, name: str) -> int | None:
    """Character count of `name` in HEAD, or None when HEAD lacks it."""
    result = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{name}"], capture_output=True)
    return len(result.stdout.decode("utf-8")) if result.returncode == 0 else None


def relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and value != "."


def settings(snapshot: StagedSnapshot) -> tuple[set[str], list[str], dict[str, str]]:
    path = snapshot.root / ".agent-checks.json"
    data = json.loads(snapshot.read_text(path)) if snapshot.exists(path) else {}
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
    return {extension.lower() for extension in extensions} | MARKDOWN, [folder.rstrip("/") for folder in excluded], exceptions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="explicit full-project audit of all indexed source/Markdown files")
    args = parser.parse_args()
    try:
        root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").strip())
        changed = [name for name in git(root, "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "-z").split("\0") if name]
        # Renamed paths map to their HEAD name, so a moved file keeps the size it had before this commit.
        status = git(root, "diff", "--cached", "--name-status", "-M", "--diff-filter=ACMRT", "-z").split("\0")
        head_names: dict[str, str] = {}
        index = 0
        while index < len(status) and status[index]:
            if status[index].startswith(("R", "C")):
                head_names[status[index + 2]] = status[index + 1]; index += 3
            else:
                head_names[status[index + 1]] = status[index + 1]; index += 2
        snapshot = StagedSnapshot(root)
        extensions, excluded, exceptions = settings(snapshot)
        eligible = {path for path in snapshot.entries if not any(
            path.relative_to(root).as_posix() == folder or path.relative_to(root).as_posix().startswith(folder + "/")
            for folder in excluded)}
        candidates = eligible if args.all else {root / name for name in changed} & eligible
        selected = sorted(path for path in candidates if path.suffix.lower() in extensions)
        snapshot.prefetch(selected)
        errors = 0
        for path in selected:
            name = path.relative_to(root).as_posix()
            count = len(snapshot.read_text(path))
            if count > LIMIT_CHARACTERS and name not in exceptions:
                before = None if args.all else head_characters(root, head_names.get(name, name))
                if before is not None and before > LIMIT_CHARACTERS:
                    print(f"warning: {name}: {count} characters, already over the {LIMIT_CHARACTERS} limit before this commit; split by responsibility")
                    continue
                print(f"{name}: {count} characters, limit {LIMIT_CHARACTERS}; split by responsibility or record a reason in .agent-checks.json")
                errors += 1
        print(f"Checked {len(selected)} staged source/Markdown files for the {LIMIT_CHARACTERS}-character limit.")
        markdown = [path for path in selected if path.suffix.lower() in MARKDOWN]
        callbacks = dict(read_text=snapshot.read_text, exists=snapshot.exists,
                         is_file=snapshot.is_file, resolve=lexical_path)
        if markdown:
            errors += check(markdown, **callbacks)
        # --no-renames exposes old names as deletions, including directory links.
        removed = {root / name for name in git(root, "diff", "--cached", "--no-renames", "--name-only", "--diff-filter=D", "-z").split("\0") if name}
        affected = removed | {root / name for name in changed if Path(name).suffix.lower() in MARKDOWN}
        if removed:
            affected.update(parent for path in removed for parent in path.parents
                            if parent.is_relative_to(root) and not snapshot.exists(parent))
        if affected:
            incoming = sorted(path for path in eligible if path.suffix.lower() in MARKDOWN and path not in markdown)
            snapshot.prefetch(incoming)
            if incoming:
                errors += check(incoming, only_targets=affected, **callbacks)
        return 1 if errors else 0
    except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Staged check error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
