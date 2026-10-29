#!/usr/bin/env python3
"""Select tests for committed changes and execute the same immutable commit.

Run after the last commit: python3 tools/checks.py
For several commits: python3 tools/checks.py --base <commit-before-request>
Unmapped paths select both suites. tools/checks.json owns commands and mappings.
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def git(*arguments: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), *arguments], check=True, stdout=subprocess.PIPE).stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD^", help="exclusive base of the completed request")
    args = parser.parse_args()
    candidate = git("rev-parse", "HEAD").decode().strip()
    config = json.loads(git("show", f"{candidate}:tools/checks.json"))
    checks: dict[str, list[str]] = config["checks"]
    mappings: dict[str, list[str]] = config["paths"]
    changed = git("diff", "--name-only", "--no-renames", "-z", args.base, candidate).decode().split("\0")
    selected: dict[str, list[str]] = {}
    for name in filter(None, changed):
        matches = [pattern for pattern in mappings if name == pattern or (pattern.endswith("/") and name.startswith(pattern))]
        for key in {key for pattern in matches for key in mappings[pattern]} if matches else checks:
            selected.setdefault(key, []).append(f"{name} ({'mapped' if matches else 'unmapped; full suite'})")
    print(f"Candidate: {candidate}", flush=True)
    for key, reasons in selected.items():
        print(f"Selected {key}: {'; '.join(reasons)}", flush=True)
    if not selected:
        print("No executable checks selected: changed paths are explicitly classified as non-executable.")
        return 0
    failures = 0
    with tempfile.TemporaryDirectory(prefix="global-instructions-checks-") as directory:
        snapshot = Path(directory)
        with tarfile.open(fileobj=io.BytesIO(git("archive", candidate))) as archive:
            archive.extractall(snapshot, filter="data")
        for key in sorted(selected):
            command = [sys.executable, *checks[key]]
            print(f"Running {key}: {command}", flush=True)
            result = subprocess.run(command, cwd=snapshot)
            if result.returncode:
                print(f"FAILED {key}: {command} exited {result.returncode}", file=sys.stderr, flush=True)
                failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
