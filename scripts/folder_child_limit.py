#!/usr/bin/env python3
"""Check the 16 child rule from ~/.agents/rules/Implementation.md on the git repository that holds the working directory.

  folder_child_limit.py           report every folder over the limit in the working tree
  folder_child_limit.py --staged  pre-commit mode: report only a folder that the index puts over the limit,
                                  or one already over it in HEAD that the index grows, so an existing
                                  backlog does not block unrelated commits

Exit code 1 when a folder is reported, 0 otherwise.

Only folders the developer or an agent creates count. Git-ignored paths (node_modules, build output) are not
listed by git, so they never count. A project lists the rest in `.folder-child-limit.json` at its root:

  {"third_party": ["vendor/somelib"], "sidecar_suffixes": [".meta"]}

- `third_party`: committed folders that hold third-party code. Each counts as one child of its parent,
  and nothing inside it is inspected.
- `sidecar_suffixes`: files an engine writes beside the file they describe, such as Unity `.meta` or
  Godot `.uid` and `.import`. They are not counted.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

LIMIT = 16
SETTINGS_FILE = ".folder-child-limit.json"
SETTINGS_KEYS = {"third_party", "sidecar_suffixes"}


def git(root: Path, *arguments: str) -> list[str]:
    result = subprocess.run(["git", "-C", str(root), *arguments], capture_output=True, text=True, check=True)
    # -z output separates paths with NUL, so a path with spaces or non-ASCII characters arrives unquoted.
    return [path for path in result.stdout.split("\0") if path]


def load_settings(root: Path) -> tuple[frozenset[str], tuple[str, ...]]:
    path: Path = root / SETTINGS_FILE
    if not path.exists():
        return frozenset(), ()
    settings: dict = json.loads(path.read_text())
    unknown: set[str] = set(settings) - SETTINGS_KEYS
    if unknown:
        raise SystemExit(f"{SETTINGS_FILE}: unknown keys {sorted(unknown)}; allowed keys are {sorted(SETTINGS_KEYS)}")
    third_party = frozenset(folder.strip("/") for folder in settings.get("third_party", []))
    return third_party, tuple(settings.get("sidecar_suffixes", []))


def child_counts(paths: list[str], third_party: frozenset[str], sidecar_suffixes: tuple[str, ...]) -> dict[str, int]:
    """Map each folder ('.' is the repository root) to the number of its direct children."""
    tree: dict[str, set[str]] = {}
    for path in paths:
        parts: tuple[str, ...] = PurePosixPath(path).parts
        if parts[-1].endswith(sidecar_suffixes):
            continue
        for depth in range(len(parts)):
            tree.setdefault("/".join(parts[:depth]) or ".", set()).add(parts[depth])
            if "/".join(parts[: depth + 1]) in third_party:
                break
    return {folder: len(children) for folder, children in tree.items()}


def working_tree_paths(root: Path) -> list[str]:
    deleted: set[str] = set(git(root, "ls-files", "-z", "--deleted"))
    listed: list[str] = git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    return [path for path in listed if path not in deleted]


def has_head(root: Path) -> bool:
    return subprocess.run(["git", "-C", str(root), "rev-parse", "--verify", "--quiet", "HEAD"], capture_output=True).returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the 16 child rule on the current git repository.")
    parser.add_argument("--staged", action="store_true", help="pre-commit mode: report only what the index adds or grows")
    staged: bool = parser.parse_args().staged

    root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel")[0].strip())
    third_party, sidecar_suffixes = load_settings(root)
    if staged:
        counts: dict[str, int] = child_counts(git(root, "ls-files", "-z", "--cached"), third_party, sidecar_suffixes)
        committed_paths: list[str] = git(root, "ls-tree", "-r", "-z", "--name-only", "HEAD") if has_head(root) else []
        committed: dict[str, int] = child_counts(committed_paths, third_party, sidecar_suffixes)
        over: list[str] = [folder for folder, count in counts.items() if count > LIMIT and count > committed.get(folder, 0)]
    else:
        counts = child_counts(working_tree_paths(root), third_party, sidecar_suffixes)
        over = [folder for folder, count in counts.items() if count > LIMIT]

    for folder in sorted(over):
        print(f"{folder}: {counts[folder]} children, limit {LIMIT}")
    if over:
        print("Split each folder by a shared meaning, under the 16 child rule in ~/.agents/rules/Implementation.md.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
