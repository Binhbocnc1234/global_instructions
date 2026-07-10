#!/usr/bin/env python3
"""Preserve extracted source text inside a generated book skill."""

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path


LOCAL_GITIGNORE = """# Raw source extracts are local-only and may contain copyrighted or private content.
# Ignore everything in this directory except this rule, matching local cache folders.
*
!.gitignore
"""


def sanitized_run(metadata: dict) -> dict:
    sources = []
    for source in metadata.get("sources", []):
        sources.append(
            {
                key: source.get(key)
                for key in (
                    "filename",
                    "format",
                    "extraction_method",
                    "pages",
                    "pages_label",
                    "chars",
                    "words",
                    "estimated_tokens",
                    "raw_extract_file",
                )
            }
        )
    run = {
        "extraction_mode": metadata.get("extraction_mode"),
        "total_sources": metadata.get("total_sources", len(sources)),
        "pages": metadata.get("pages"),
        "words": metadata.get("words"),
        "estimated_tokens": metadata.get("estimated_tokens"),
        "sources": sources,
    }
    encoded = json.dumps(run, sort_keys=True, ensure_ascii=False).encode("utf-8")
    run["id"] = hashlib.sha256(encoded).hexdigest()[:12]
    return run


def preserve(workdir: Path, skill_dir: Path) -> Path:
    source_dir = workdir / "raw-source-extract"
    metadata_path = workdir / "metadata.json"
    if not source_dir.is_dir() or not metadata_path.is_file():
        raise FileNotFoundError("extraction output is incomplete; run extract.py first")

    target_dir = skill_dir / "raw-source-extract"
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / ".gitignore").write_text(LOCAL_GITIGNORE, encoding="utf-8")
    for source in source_dir.glob("*.txt"):
        shutil.copy2(source, target_dir / source.name)

    run = sanitized_run(json.loads(metadata_path.read_text(encoding="utf-8")))
    manifest_path = target_dir / "manifest.json"
    manifest = {"version": 1, "runs": []}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    runs = {item["id"]: item for item in manifest.get("runs", [])}
    runs[run["id"]] = run
    manifest["runs"] = [runs[key] for key in sorted(runs)]
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return target_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", required=True, type=Path)
    parser.add_argument(
        "--workdir",
        type=Path,
        default=Path(
            os.environ.get(
                "BOOK_SKILL_WORKDIR",
                Path(tempfile.gettempdir()) / "book_skill_work",
            )
        ),
    )
    args = parser.parse_args()
    target = preserve(args.workdir, args.skill_dir)
    print(f"Preserved raw source extracts -> {target}")


if __name__ == "__main__":
    main()
