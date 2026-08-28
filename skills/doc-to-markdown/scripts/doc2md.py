"""doc2md - convert documents into agent-readable Markdown.

Wraps Microsoft's MarkItDown (https://github.com/microsoft/markitdown) and
adds support for the pre-2007 binary Office formats, which MarkItDown itself
rejects, by upgrading them through the locally installed Microsoft Office.

Usage:
    doc2md report.docx                 -> report.md next to the source
    doc2md *.doc *.docx -o extracted/  -> all outputs into extracted/
    doc2md notes.doc --stdout          -> Markdown on stdout (UTF-8)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from markitdown import MarkItDown

import legacy_doc
import pdf_tables

EXIT_OK = 0
EXIT_FAILED = 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="doc2md",
        description="Convert documents (.docx/.doc/.pdf/.pptx/.xlsx/...) to Markdown.",
    )
    parser.add_argument("inputs", nargs="+", help="Files to convert.")
    parser.add_argument(
        "-o",
        "--outdir",
        type=Path,
        help="Directory for the .md output. Defaults to each source's own folder.",
    )
    parser.add_argument(
        "--tables",
        action="store_true",
        help=(
            "For PDFs, reconstruct ruled tables into Markdown tables instead of "
            "MarkItDown's flowed-text extraction. Use for timetables and reports."
        ),
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write Markdown to stdout instead of files (single input only).",
    )
    return parser


def convert(path: Path, converter: MarkItDown, tables: bool = False) -> str:
    """Return the Markdown for `path`, upgrading legacy formats when needed."""
    if tables and path.suffix.lower() == ".pdf":
        return pdf_tables.convert(path)
    if legacy_doc.is_legacy(path):
        with legacy_doc.temp_workdir() as workdir:
            upgraded = legacy_doc.upgrade(path, Path(workdir))
            return converter.convert(str(upgraded)).text_content
    return converter.convert(str(path)).text_content


def output_path(source: Path, outdir: Path | None) -> Path:
    folder = outdir if outdir is not None else source.parent
    return folder / (source.stem + ".md")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    sources = [Path(item) for item in args.inputs]

    if args.stdout and len(sources) != 1:
        print("--stdout accepts exactly one input file.", file=sys.stderr)
        return EXIT_FAILED

    if args.outdir is not None:
        args.outdir.mkdir(parents=True, exist_ok=True)

    converter = MarkItDown()
    failures = 0

    for source in sources:
        if not source.is_file():
            print(f"[skip] not a file: {source}", file=sys.stderr)
            failures += 1
            continue
        try:
            markdown = convert(source, converter, tables=args.tables)
        except Exception as error:  # noqa: BLE001 - report, keep going
            print(f"[fail] {source.name}: {error}", file=sys.stderr)
            failures += 1
            continue

        if args.stdout:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stdout.write(markdown)
        else:
            destination = output_path(source, args.outdir)
            destination.write_text(markdown, encoding="utf-8")
            print(f"[ok] {source.name} -> {destination}", file=sys.stderr)

    return EXIT_FAILED if failures else EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
