#!/usr/bin/env python3
"""Check local Markdown links and @ imports without changing files.

Run from any Git project: python3 ~/.agents/scripts/check_markdown_links.py
Or supply files/directories explicitly (Git is then unnecessary).
Uses GitHub-style heading anchors; external URLs are ignored.
Checks single-line Markdown links/reference definitions and @ imports.
Raw HTML links and multiline link syntax are outside this checker's scope.
Explicit directories are scanned recursively, including untracked files.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
DEFINITION = re.compile(r"^ {0,3}\[([^\]]+)\]:\s*(.*)$")
IMPORT = re.compile(r"(?<![\w@])@([^\s`|<>\[\]()]+\.md)(?=$|[\s|.,;:)])")
LABEL = re.compile(r"!?\[((?:[^\[\]\\]|\\.|\[[^\[\]]*\])*)\]")
INLINE_CODE = re.compile(r"(`+)(?!`)(.*?)\1(?!`)")


def visible_lines(text: str) -> list[str]:
    """Preserve line numbers and columns while hiding literal examples/comments."""
    text = re.sub(r"<!--[\s\S]*?-->", lambda m: re.sub(r"[^\n]", " ", m[0]), text)
    lines: list[str] = []
    fence = ""
    for line in text.splitlines():
        marker = FENCE.match(line)
        if fence:
            lines.append(" " * len(line))
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                if not line[marker.end():].strip():
                    fence = ""
        elif marker:
            fence = marker[1]
            lines.append(" " * len(line))
        elif line.startswith(("    ", "\t")):
            lines.append(" " * len(line))
        else:
            lines.append(INLINE_CODE.sub(lambda m: " " * len(m[0]), line))
    return lines


def destination(text: str, start: int = 0) -> tuple[str, int] | None:
    """Read an angle-bracket or balanced bare link destination."""
    pos = start
    while pos < len(text) and text[pos].isspace():
        pos += 1
    begin = pos
    if pos < len(text) and text[pos] == "<":
        end = text.find(">", pos + 1)
        return None if end < 0 else (text[pos + 1:end], end + 1)
    depth = 0
    while pos < len(text):
        char = text[pos]
        if char == "\\" and pos + 1 < len(text):
            pos += 2
            continue
        if char.isspace() or (char == ")" and depth == 0):
            break
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        pos += 1
    return (text[begin:pos], pos) if depth == 0 else None


def reference_key(label: str) -> str:
    return " ".join(label.split()).casefold()


def links(lines: list[str]) -> list[tuple[int, str]]:
    definitions: dict[str, str] = {}
    found: list[tuple[int, str]] = []
    for number, line in enumerate(lines, 1):
        definition = DEFINITION.match(line)
        if definition:
            parsed = destination(definition[2])
            if parsed:
                definitions.setdefault(reference_key(definition[1]), parsed[0])
                found.append((number, parsed[0]))
    for number, line in enumerate(lines, 1):
        if DEFINITION.match(line):
            continue
        consumed = 0
        for match in LABEL.finditer(line):
            if match.start() < consumed:
                continue
            end = match.end()
            if line[end:end + 1] == "(":
                parsed = destination(line, end + 1)
                if parsed:
                    target, finish = parsed
                    # A destination may be followed by a quoted title.
                    tail = re.match(r"\s*(?:\"[^\"]*\"|'[^']*'|\([^)]*\))?\s*\)", line[finish:])
                    if tail:
                        found.append((number, target))
                        consumed = finish + tail.end()
            else:
                reference = re.match(r"\[([^\]]*)\]", line[end:])
                key = reference_key(reference[1] or match[1]) if reference else reference_key(match[1])
                if reference:
                    consumed = end + reference.end()
                if key in definitions:
                    # Definitions themselves already carry the target check.
                    continue
                if reference:
                    found.append((number, "!undefined-reference:" + key))
        found.extend((number, match[1]) for match in IMPORT.finditer(line))
    return found


def anchors(text: str) -> set[str]:
    # Inline code is part of a heading's displayed text, unlike literal links.
    text = INLINE_CODE.sub(lambda m: m[2], text)
    lines = visible_lines(text)
    result: set[str] = set()
    counts: dict[str, int] = {}
    for index, line in enumerate(lines):
        result.update(re.findall(r"\b(?:id|name)\s*=\s*[\"']([^\"']+)[\"']", line))
        heading = re.match(r"^ {0,3}#{1,6}(?:\s+|$)(.*)$", line)
        title: str | None = None
        if heading:
            title = re.sub(r"\s+#+\s*$", "", heading[1])
        elif index + 1 < len(lines) and line.strip() and re.fullmatch(r" {0,3}(?:=+|-+)\s*", lines[index + 1]):
            title = line.strip()
        if title is None:
            continue
        title = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", title)
        title = re.sub(r"<[^>]*>", "", title).strip().lower()
        slug = "".join(char for char in title if char.isalnum() or char in "_- ").replace(" ", "-")
        count = counts.get(slug, 0)
        candidate = slug if count == 0 else f"{slug}-{count}"
        while candidate in result:
            count += 1
            candidate = f"{slug}-{count}"
        counts[slug] = count + 1
        result.add(candidate)
    return result


def check(files: list[Path]) -> int:
    errors = 0
    cache: dict[Path, set[str]] = {}
    for source in files:
        try:
            text = source.read_text(encoding="utf-8")
            for number, target in links(visible_lines(text)):
                reason = ""
                if target.startswith("!undefined-reference:"):
                    reason = "undefined reference label"
                else:
                    target = re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])", r"\1", target)
                    url = urlsplit(target)
                    if url.scheme or url.netloc:
                        continue
                    local = Path(unquote(url.path)).expanduser()
                    path = (source.parent / local).resolve() if url.path else source.resolve()
                    if not path.exists():
                        reason = "target does not exist"
                    elif url.fragment:
                        if not path.is_file() or path.suffix.lower() not in (".md", ".markdown"):
                            reason = "cannot validate an anchor in a non-Markdown target"
                        else:
                            if path not in cache:
                                cache[path] = anchors(path.read_text(encoding="utf-8"))
                            if unquote(url.fragment) not in cache[path]:
                                reason = "heading anchor does not exist"
                if reason:
                    print(f"{source}:{number}: {target}: {reason}")
                    errors += 1
        except (OSError, UnicodeError, ValueError) as error:
            print(f"{source}: checking error: {error}", file=sys.stderr)
            errors += 1
    print(f"Checked {len(files)} Markdown files; {errors} errors.")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Markdown files or directories")
    args = parser.parse_args()
    try:
        files: set[Path] = set()
        if args.paths:
            for path in args.paths:
                if not path.exists():
                    raise ValueError(f"Input does not exist: {path}")
                candidates = path.rglob("*") if path.is_dir() else [path]
                for candidate in candidates:
                    if candidate.is_file() and candidate.suffix.lower() in (".md", ".markdown"):
                        files.add(candidate.resolve())
                    elif not path.is_dir():
                        raise ValueError(f"Input is not Markdown: {path}")
        else:
            root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
            tracked = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True, text=True, check=True).stdout
            files = {Path(root) / name for name in tracked.split("\0") if name and Path(name).suffix.lower() in (".md", ".markdown")}
        if not files:
            raise ValueError("No Markdown files found")
        return check(sorted(files))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
