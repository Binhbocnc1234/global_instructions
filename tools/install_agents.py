#!/usr/bin/env python3
"""Install this project's development instructions, rules and skills into ~/.agents/.

Run from any directory: python3 /path/to/global_instructions/tools/install_agents.py
Use --check to compare without writing, or --destination for an isolated install.
The destination's rules/ and skills/ mirror the source: files the source lacks are deleted.
Every other destination folder holds files this installer does not own, such as the Git hooks, and is left alone.
"""
from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

from compile_codex_agents import CompileError, compile_document

SOURCE_ROOT = Path(__file__).resolve().parent.parent
# Another tool writes inside these skills folders, so a file the source lacks is not stale there.
EXTERNALLY_MANAGED_SKILLS: frozenset[str] = frozenset({".trash", "synced"})


def is_bytecode_cache(relative: Path) -> bool:
    return "__pycache__" in relative.parts or relative.suffix in {".pyc", ".pyo"}


def stale_files(destination: Path, installed: set[Path]) -> list[Path]:
    """Return files in the installer-owned folders that the source no longer provides."""
    stale: list[Path] = []
    for owned in (destination / "rules", destination / "skills"):
        for path in sorted(owned.rglob("*")):
            relative = path.relative_to(owned)
            # This installer never writes a symlink or a cache file, so neither can be left over from it.
            if path in installed or path.is_symlink() or not path.is_file() or is_bytecode_cache(relative):
                continue
            if owned.name == "skills" and relative.parts[0] in EXTERNALLY_MANAGED_SKILLS:
                continue
            stale.append(path)
    return stale


def installation_files(destination: Path) -> dict[Path, bytes]:
    source = SOURCE_ROOT / "AGENTS.development.md"
    rules = SOURCE_ROOT / "rules"
    if not rules.is_dir() or rules.is_symlink():
        raise ValueError(f"Required rules directory is missing or is a symlink: {rules}")
    paths = sorted(rules.rglob("*"))
    if not any(path.is_file() for path in paths):
        raise ValueError(f"Required rules directory contains no files: {rules}")
    skills = SOURCE_ROOT / "skills"
    if not skills.is_dir() or skills.is_symlink():
        raise ValueError(f"Required skills directory is missing or is a symlink: {skills}")
    paths.extend(sorted(
        path for path in skills.rglob("*")
        if not is_bytecode_cache(path.relative_to(skills))
    ))
    if not any(path.name == "SKILL.md" for path in paths if skills in path.parents):
        raise ValueError(f"Required skills directory contains no SKILL.md files: {skills}")
    files: dict[Path, bytes] = {}
    for path in [source, *paths]:
        if path.is_symlink():
            raise ValueError(f"Source symlinks are not supported: {path}")
        if path.is_dir():
            continue
        content = path.read_bytes()
        if path.suffix == ".md" and (path == source or rules in path.parents):
            text = content.decode("utf-8")
            if path != source:
                # The source project brief differs from the installed global document.
                text = text.replace(
                    "](../AGENTS.development.md", "](../AGENTS.md"
                )
            content = text.encode("utf-8")
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
        skill_modes: dict[Path, int] = {
            path: (SOURCE_ROOT / path.relative_to(destination)).stat().st_mode & 0o777
            for path in files if path.relative_to(destination).parts[0] == "skills"
        }
        changed: list[Path] = [
            path for path, content in files.items()
            if not path.is_file() or path.read_bytes() != content
            or (path in skill_modes and path.stat().st_mode & 0o777 != skill_modes[path])
        ]
        stale: list[Path] = stale_files(destination, set(files))
        if args.check:
            for path in changed:
                print(f"Missing or changed: {path}", file=sys.stderr)
            for path in stale:
                print(f"Stale: {path}", file=sys.stderr)
            if changed or stale:
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
                mode = skill_modes.get(path, path.stat().st_mode & 0o777 if path.exists() else 0o644)
                temporary.chmod(mode)
                temporary.replace(path)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
            print(f"Installed: {path}")
        for path in stale:
            path.unlink()
            for parent in path.parents:
                if parent in (destination / "rules", destination / "skills") or any(parent.iterdir()):
                    break
                parent.rmdir()
            print(f"Removed: {path}")
        print(f"Updated {len(changed)} of {len(files)} instruction files and removed {len(stale)} stale files in {destination}")
        return 0
    except (CompileError, OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
