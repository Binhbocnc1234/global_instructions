"""Read candidate paths and requested blobs without exporting the Git index."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path


def lexical_path(path: Path) -> Path:
    """Normalize without following unstaged working-tree symlinks."""
    return Path(os.path.abspath(path))


class StagedSnapshot:
    def __init__(self, root: Path) -> None:
        self.root = root
        listing = subprocess.run(["git", "-C", str(root), "ls-files", "--stage", "-z"],
                                 check=True, capture_output=True, text=True).stdout
        self.entries: dict[Path, tuple[str, str]] = {}
        self.directories: set[Path] = {root}
        self.cache: dict[Path, str] = {}
        for record in listing.split("\0"):
            if not record:
                continue
            metadata, name = record.split("\t", 1)
            mode, oid, stage = metadata.split()
            if stage != "0":
                raise ValueError(f"Unmerged index entry: {name}")
            path = root / name
            self.entries[path] = (mode, oid)
            self.directories.update(parent for parent in path.parents if parent.is_relative_to(root))

    def exists(self, path: Path) -> bool:
        if path.is_relative_to(self.root):
            return path in self.entries or path in self.directories
        return path.exists()

    def is_file(self, path: Path) -> bool:
        if path.is_relative_to(self.root):
            return path in self.entries and self.entries[path][0] in {"100644", "100755"}
        return path.is_file()

    def read_text(self, path: Path) -> str:
        if not path.is_relative_to(self.root):
            return path.read_text(encoding="utf-8")
        self.prefetch([path])
        return self.cache[path]

    def prefetch(self, paths: list[Path]) -> None:
        pending = list(dict.fromkeys(path for path in paths if path not in self.cache))
        if not pending:
            return
        for path in pending:
            if not self.is_file(path):
                raise ValueError(f"{path.relative_to(self.root)}: staged path is not a regular file")
        # Batch by object ID: one Git process, even when reverse-link discovery reads many documents.
        request = "".join(self.entries[path][1] + "\n" for path in pending).encode("ascii")
        result = subprocess.run(["git", "-C", str(self.root), "cat-file", "--batch"],
                                input=request, check=True, capture_output=True).stdout
        position = 0
        for path in pending:
            end = result.index(b"\n", position)
            oid, kind, size = result[position:end].split()
            if kind != b"blob" or oid.decode("ascii") != self.entries[path][1]:
                raise ValueError(f"Invalid Git blob response for {path}")
            position = end + 1
            length = int(size)
            self.cache[path] = result[position:position + length].decode("utf-8")
            position += length + 1
