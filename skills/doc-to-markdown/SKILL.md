---
name: doc-to-markdown
description: >
  Extract Word, PDF, PowerPoint, Excel and other documents into agent-readable
  Markdown, including legacy binary .doc/.xls/.ppt files that MarkItDown alone
  cannot open. Use when the user attaches or points at a document and wants its
  contents read, extracted, summarised, or converted to Markdown.
---

# Document to Markdown

Converts documents into Markdown that an agent can read directly. Wraps
Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) and adds the
one thing it cannot do: pre-2007 binary Office formats.

## Preflight

Check the tool is installed before using it:

```bat
doc2md --help
```

If the command is not found, see [Installation](#installation) below. Do not
attempt to parse the document by hand instead.

## Usage

```bat
doc2md report.docx
doc2md lecture.doc slides.pptx -o extracted\
doc2md notes.doc --stdout
```

- Default output is `<name>.md` beside the source file.
- `-o DIR` collects every output into `DIR`, created if missing.
- `--tables` changes PDF handling; see [Table-heavy PDFs](#table-heavy-pdfs).
- `--stdout` prints UTF-8 Markdown; single input only.
- Per-file failures go to stderr and do not stop the batch. Exit code is 1 if
  any file failed, 0 otherwise.

Read the resulting `.md` file rather than piping the whole document into
context when the source is large.

### Never redirect stdout to a file

```bat
doc2md x.docx > x.md   :: WRONG - produces "??I H?C QU?C GIA"
```

The Windows console encoding is cp1252, so redirection mangles non-ASCII text.
The tool writes its own files as UTF-8; use the default output or `-o`.

## Table-heavy PDFs

Pass `--tables` for any PDF whose value is in its tables: timetables, grade
sheets, financial reports, schedules.

Without it the output is silently wrong rather than merely ugly. MarkItDown's
PDF converter classifies each page as form-style or plain text, and when plain
pages dominate it falls back to `pdfminer.high_level.extract_text`. That
fallback emits text in layout order with no row reconstruction, so a wide table
comes out column by column: every value of column 1, then every value of
column 2. Rows cannot be recovered from that output. The heuristic lives in
`markitdown/converters/_pdf_converter.py` and has no CLI override, which is why
this skill bypasses it.

`--tables` asks pdfplumber for the ruled table structure directly and renders
real Markdown tables, one section per page. Pages with no detectable table fall
back to that page's plain text, so cover pages and notes survive.

Measured on a 31-page university timetable: 36,426 lines of unusable column
soup by default, versus 2,412 lines of correct tables with `--tables`.

Keep the default for prose documents. `--tables` is worse for flowing text,
because it segments per page and drops paragraph structure.

## Supported inputs

Native MarkItDown: `.docx`, `.pptx`, `.xlsx`, `.pdf`, `.html`, `.csv`, `.json`,
`.xml`, `.epub`, `.zip`, images, audio.

Legacy bridge, which requires Microsoft Office installed locally:

| Extension | COM application | Upgraded to |
| --- | --- | --- |
| `.doc` | Word.Application | `.docx` |
| `.xls` | Excel.Application | `.xlsx` |
| `.ppt` | PowerPoint.Application | `.pptx` |

PDF table reconstruction uses pdfplumber, which MarkItDown already depends on,
so `--tables` adds no extra dependency.

`scripts/legacy_doc.py` drives Office through PowerShell COM, so there is no
`pywin32` dependency. The upgraded copy is written to a temporary directory and
deleted afterwards; the original file is never modified.

## Installation

The scripts live in this skill; only the MarkItDown dependency needs an
environment. Install it as an isolated uv tool:

```bat
set UV_TOOL_DIR=D:\Apps\uv-tools
set UV_TOOL_BIN_DIR=D:\Apps\uv-bin
uv tool install "markitdown[all]"
```

Then create `D:\Apps\uv-bin\doc2md.cmd`:

```bat
@echo off
"D:\Apps\uv-tools\markitdown\Scripts\python.exe" "%USERPROFILE%\.agents\skills\doc-to-markdown\scripts\doc2md.py" %*
```

Put `D:\Apps\uv-bin` on PATH. If it is not on PATH, call the shim by its full
path, or invoke the script directly with the venv's Python:

```bat
"D:\Apps\uv-tools\markitdown\Scripts\python.exe" "%USERPROFILE%\.agents\skills\doc-to-markdown\scripts\doc2md.py" file.docx
```

On a machine with a different layout, adjust the two paths in the shim; the
scripts themselves contain no hardcoded paths.

## Known limits

- Tables nested inside other tables flatten into a single Markdown cell.
  MarkItDown targets structure and token efficiency, not layout fidelity.
- `--tables` relies on ruled lines. A table drawn with whitespace alignment and
  no borders will not be detected, and the page falls back to plain text.
- Images are not extracted; only alt text survives.
- `.doc` conversion opens a real Office process: several seconds per file, and
  it needs an interactive Windows session. It will not work headless or over
  plain SSH.
- If a conversion fails, report the blocker rather than guessing at the
  document's contents.
