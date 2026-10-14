#!/usr/bin/env python3
"""Install this project's development instructions and rules into ~/.agents/.

Run from any directory: python3 /path/to/global_instructions/tools/install_agents.py
Use --check to compare without writing, or --destination for an isolated install.
Other destination files are neither updated nor deleted.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

from compile_codex_agents import CompileError, compile_document

SOURCE_ROOT = Path(__file__).resolve().parent.parent


def installation_files(destination: Path) -> dict[Path, bytes]:
    source = SOURCE_ROOT / "AGENTS.development.md"
    rules = SOURCE_ROOT / "rules"
    if not rules.is_dir() or rules.is_symlink():
        raise ValueError(f"Required rules directory is missing or is a symlink: {rules}")
    paths = sorted(rules.rglob("*"))
    if not any(path.is_file() for path in paths):
        raise ValueError(f"Required rules directory contains no files: {rules}")
    files: dict[Path, bytes] = {}
    for path in [source, *paths]:
        if path.is_symlink():
            raise ValueError(f"Source symlinks are not supported: {path}")
        if path.is_dir():
            continue
        content = path.read_bytes()
        if path.suffix == ".md":
            content.decode("utf-8")
        relative = Path("AGENTS.md") if path == source else path.relative_to(SOURCE_ROOT)
        target = destination / relative
        # Replacing a destination symlink could change how another tool loads rules.
        if any(parent.is_symlink() for parent in [target, *target.parents]):
            raise ValueError(f"Destination symlinks are not supported: {target}")
        if target.exists() and not target.is_file():
            raise ValueError(f"Destination is not a regular file: {target}")
        files[target] = content
    # Reuse the import parser to catch missing files and cycles before any writes.
    # The expanded document is only validation; installation preserves @ imports.
    compile_document(source, destination / "AGENTS.md")
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=Path("~/.agents"))
    parser.add_argument("--check", action="store_true", help="exit 1 when files are missing or changed")
    args = parser.parse_args()
    destination = Path(os.path.abspath(args.destination.expanduser()))
    try:
        if destination == SOURCE_ROOT or SOURCE_ROOT in destination.parents:
            raise ValueError("Destination must be outside the source project")
        files = installation_files(destination)
        changed: list[Path] = [
            path for path, content in files.items()
            if not path.is_file() or path.read_bytes() != content
        ]
        if args.check:
            for path in changed:
                print(f"Missing or changed: {path}", file=sys.stderr)
            if changed:
                return 1
            print(f"Up to date: {len(files)} instruction files in {destination}")
            return 0
        for path in changed:
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary: Path | None = None
            try:
                with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
                    temporary = Path(handle.name)
                    handle.write(files[path])
                temporary.chmod(path.stat().st_mode & 0o777 if path.exists() else 0o644)
                temporary.replace(path)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
            print(f"Installed: {path}")
        print(f"Updated {len(changed)} of {len(files)} instruction files in {destination}")
        return 0
    except (CompileError, OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
