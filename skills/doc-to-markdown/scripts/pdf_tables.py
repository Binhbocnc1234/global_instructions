"""Table-aware PDF extraction.

MarkItDown's PDF converter decides per document whether pages look like forms
or plain text, and for plain-text documents it falls back to
`pdfminer.high_level.extract_text`. That fallback emits text in layout order
with no row reconstruction, so a wide data table comes out column by column:
every value of the first column, then every value of the second, and so on.
Rows are unrecoverable.

This module bypasses that heuristic and asks pdfplumber directly for the ruled
table structure, emitting real Markdown tables. Use it for PDFs whose value is
in their tables; the default MarkItDown path remains better for prose.
"""

from __future__ import annotations

from pathlib import Path

import pdfplumber


def _clean(cell: object) -> str:
    """Flatten one cell into something safe inside a Markdown table row."""
    if cell is None:
        return ""
    text = str(cell).replace("\r", " ").replace("\n", " ")
    text = text.replace("|", "\\|")
    return " ".join(text.split())


def _render_table(rows: list[list[object]]) -> str:
    """Render one extracted table as a Markdown table.

    The first row is treated as the header. Rows are padded to the widest row
    so the table stays well-formed even when pdfplumber reports ragged output.
    """
    cleaned = [[_clean(cell) for cell in row] for row in rows if row]
    if not cleaned:
        return ""

    width = max(len(row) for row in cleaned)
    padded = [row + [""] * (width - len(row)) for row in cleaned]

    header, *body = padded
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * width) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in body)
    return "\n".join(lines)


def convert(path: Path) -> str:
    """Return Markdown for `path`, preferring ruled tables over flowed text.

    Pages with no detectable table fall back to that page's plain text, so
    cover pages and notes are not lost.
    """
    chunks: list[str] = []

    with pdfplumber.open(str(path)) as pdf:
        for number, page in enumerate(pdf.pages, start=1):
            chunks.append(f"## Page {number}")

            tables = page.extract_tables()
            if tables:
                for table in tables:
                    rendered = _render_table(table)
                    if rendered:
                        chunks.append(rendered)
                continue

            text = page.extract_text()
            if text and text.strip():
                chunks.append(text.strip())

    return "\n\n".join(chunks).strip() + "\n"
