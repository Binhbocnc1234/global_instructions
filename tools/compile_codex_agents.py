#!/usr/bin/env python3
"""Expand shared @path.md imports into Codex's global AGENTS.md.

Run: python3 ~/.agents/tools/compile_codex_agents.py
Use --source and --output to compile other instruction files, or --check to
verify that the output matches the sources without writing it.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

IMPORT = re.compile(r"(?<![\w@])@(?P<path>[^\s`|<>\[\]()]+\.md)(?=$|[\s|.,;:)])")
INLINE_CODE = re.compile(r"(`+).*?\1")
LINK = re.compile(r"(!?\[[^\]\n]*\]\()(?P<target><[^>\n]+>|[^\s)]+)(?P<suffix>[^)\n]*\))")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


class CompileError(Exception):
    """A source cannot be expanded safely."""


class Compiler:
    def __init__(self, output: Path) -> None:
        self.output = output.expanduser().resolve()
        self.included: set[Path] = set()
        self.active: list[Path] = []

    def rebase_link(self, match: re.Match[str], source: Path) -> str:
        target = match["target"].strip("<>")
        if target.startswith(("#", "/", "//")) or SCHEME.match(target):
            return match[0]
        path, separator, fragment = target.partition("#")
        resolved = Path(path).expanduser()
        if not resolved.is_absolute():
            resolved = source.parent / resolved
        relative = Path(os.path.relpath(resolved, self.output.parent)).as_posix()
        rebased = relative + separator + fragment
        if match["target"].startswith("<") or " " in rebased:
            rebased = f"<{rebased}>"
        return match[1] + rebased + match["suffix"]

    def expand(self, source: Path) -> str:
        source = source.expanduser().resolve()
        if source == self.output:
            raise CompileError(f"Output is also a source file: {source}")
        if source in self.active:
            chain = " -> ".join(str(path) for path in [*self.active, source])
            raise CompileError(f"Circular import: {chain}")
        if source in self.included:
            return ""
        try:
            content = source.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            chain = " -> ".join(str(path) for path in [*self.active, source])
            raise CompileError(f"Cannot read {chain}: {error}") from error
        self.active.append(source)
        self.included.add(source)
        lines: list[str] = []
        pending: list[str] = []
        fence: str = ""
        for line in content.splitlines(keepends=True):
            marker = FENCE.match(line)
            if fence:
                lines.append(line)
                if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence):
                    if not line[marker.end():].strip():
                        fence = ""
                continue
            if marker:
                fence = marker[1]
                lines.append(line)
                continue
            if not line.strip():
                lines.append(line)
                lines.extend(pending)
                pending.clear()
                continue
            directive = IMPORT.fullmatch(line.strip())
            if directive:
                imported = Path(directive["path"]).expanduser()
                lines.append(self.expand(source.parent / imported))
                continue

            def replace_import(match: re.Match[str]) -> str:
                imported = (source.parent / Path(match["path"]).expanduser()).resolve()
                expanded = self.expand(imported)
                if expanded:
                    pending.append(expanded)
                relative = Path(os.path.relpath(imported, self.output.parent)).as_posix()
                return f"[{imported.stem}](<{relative}>)"

            # Literal examples stay literal; inline imports follow their paragraph
            # or table so a whole Markdown document never lands inside a cell.
            code_ranges = [(code.start(), code.end()) for code in INLINE_CODE.finditer(line)]
            line = LINK.sub(
                lambda match: match[0] if any(start <= match.start() < end for start, end in code_ranges)
                else self.rebase_link(match, source),
                line,
            )
            cursor = 0
            parts: list[str] = []
            for code in INLINE_CODE.finditer(line):
                prose = line[cursor:code.start()]
                parts.extend((IMPORT.sub(replace_import, prose), code[0]))
                cursor = code.end()
            prose = line[cursor:]
            parts.append(IMPORT.sub(replace_import, prose))
            lines.append("".join(parts))
        if pending and lines and not lines[-1].endswith("\n"):
            lines.append("\n")
        lines.extend(pending)
        self.active.pop()
        return "".join(lines).rstrip() + "\n\n"


def compile_document(source: Path, output: Path) -> str:
    compiler = Compiler(output)
    body = compiler.expand(source)
    relative = Path(os.path.relpath(source.expanduser().resolve(), compiler.output.parent)).as_posix()
    return (
        "<!-- Generated by ~/.agents/tools/compile_codex_agents.py.\n"
        f"Source: {relative}. Edit the shared sources, then rerun the compiler. -->\n\n"
        + body.rstrip() + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("~/.agents/AGENTS.md"))
    parser.add_argument("--output", type=Path, default=Path("~/.codex/AGENTS.md"))
    parser.add_argument("--check", action="store_true", help="exit 1 if output is missing or stale")
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    temporary: Path | None = None
    try:
        # Finish every import before touching the installed instructions.
        compiled = compile_document(args.source, output)
        if args.check:
            if not output.is_file() or output.read_text(encoding="utf-8") != compiled:
                print(f"Missing or stale: {output}", file=sys.stderr)
                return 1
            print(f"Up to date: {output}")
            return 0
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(compiled)
        if output.exists():
            temporary.chmod(output.stat().st_mode & 0o777)
        temporary.replace(output)
        print(f"Compiled {output} ({len(compiled.encode('utf-8'))} bytes)")
        return 0
    except (CompileError, OSError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
