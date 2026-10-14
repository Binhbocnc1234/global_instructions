#!/usr/bin/env python3
"""Install shared checks in ~/.agents and enable Git's global pre-commit hook.

Run: python3 tools/install_global_hooks.py
Use --destination for an isolated installation (still updates global Git config).
Refuses to replace a different global core.hooksPath.
Repository-specific core.hooksPath overrides this global setting.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["hooks/pre-commit", "scripts/check_staged_files.py", "scripts/check_markdown_links.py", "scripts/folder_child_limit.py"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=Path("~/.agents"))
    args = parser.parse_args()
    try:
        destination = args.destination.expanduser().resolve()
        hooks = destination / "hooks"
        existing = subprocess.run(["git", "config", "--global", "--get-all", "core.hooksPath"], capture_output=True, text=True)
        if existing.returncode not in (0, 1):
            raise ValueError(existing.stderr.strip())
        values = existing.stdout.splitlines()
        if values and (len(values) != 1 or Path(values[0]).expanduser().resolve() != hooks):
            raise ValueError(f"A different global core.hooksPath already exists: {values}")
        contents = {name: (ROOT / ("tools/" + name if name.startswith("hooks/") else name)).read_bytes() for name in FILES}
        for name, content in contents.items():
            target = destination / name
            if any(path.is_symlink() for path in [target, *target.parents]):
                raise ValueError(f"Installation symlinks are not supported: {target}")
            if target.exists() and not target.is_file():
                raise ValueError(f"Not a regular file: {target}")
        for name, content in contents.items():
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary: Path | None = None
            try:
                with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as handle:
                    temporary = Path(handle.name)
                    handle.write(content)
                temporary.chmod(0o755)
                temporary.replace(target)
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
            print(f"Installed: {target}")
        subprocess.run(["git", "config", "--global", "core.hooksPath", str(hooks)], check=True)
        configured = subprocess.run(["git", "config", "--global", "--get", "core.hooksPath"], capture_output=True, text=True, check=True).stdout.strip()
        if configured != str(hooks) or not os.access(hooks / "pre-commit", os.X_OK):
            raise ValueError("Global hook activation verification failed")
        print(f"Enabled global hooks: {configured}")
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
