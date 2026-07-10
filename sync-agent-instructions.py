#!/usr/bin/env python3
r"""Sync shared global agent instructions to tool-specific global files.

Default source:
  ~/.agents/AGENTS.md

Default targets:
  ~/.codex/AGENTS.md
  ~/.gemini/GEMINI.md

How to use: 
    python "$env:USERPROFILE\.agents\sync-agent-instructions.py"
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import shutil
import sys

HOME = Path.home()
DEFAULT_SOURCE = HOME / ".agents" / "AGENTS.md"
TARGETS = {
    "codex": HOME / ".codex" / "AGENTS.md",
    "gemini": HOME / ".gemini" / "GEMINI.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync ~/.agents/AGENTS.md to Codex and Gemini global instruction files."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Canonical instruction file to copy from. Default: ~/.agents/AGENTS.md",
    )
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=["all", *TARGETS.keys()],
        default=["all"],
        help="Targets to sync. Default: all",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create .bak timestamp backups before overwriting changed targets.",
    )
    return parser.parse_args()


def selected_targets(names: list[str]) -> dict[str, Path]:
    if "all" in names:
        return TARGETS
    return {name: TARGETS[name] for name in names}


def backup_path(target: Path) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return target.with_name(f"{target.name}.bak-{stamp}")


def sync_file(source: Path, target: Path, dry_run: bool, backup: bool) -> str:
    source_text = source.read_text(encoding="utf-8")
    target_text = None
    if target.exists():
        target_text = target.read_text(encoding="utf-8")

    if target_text == source_text:
        return f"unchanged {target}"

    if dry_run:
        action = "create" if target_text is None else "update"
        return f"would {action} {target}"

    target.parent.mkdir(parents=True, exist_ok=True)
    if backup and target.exists():
        shutil.copy2(target, backup_path(target))
    target.write_text(source_text, encoding="utf-8", newline="\n")
    action = "created" if target_text is None else "updated"
    return f"{action} {target}"


def main() -> int:
    args = parse_args()
    source = args.source.expanduser().resolve()
    if not source.exists():
        print(f"source not found: {source}", file=sys.stderr)
        return 1

    for name, target in selected_targets(args.targets).items():
        result = sync_file(
            source=source,
            target=target.expanduser(),
            dry_run=args.dry_run,
            backup=not args.no_backup,
        )
        print(f"{name}: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
