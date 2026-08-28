"""Convert legacy binary Office files (.doc, .xls, .ppt) to their modern
OOXML equivalents so that markitdown can read them.

MarkItDown only understands OOXML (.docx/.xlsx/.pptx); the pre-2007 binary
formats raise UnsupportedFormatException. This module drives the locally
installed Microsoft Office through COM (via PowerShell, so no pywin32
dependency) to perform the upgrade into a temporary file.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

# Legacy extension -> (COM application ProgID, modern extension, SaveAs format id)
# Format ids come from the Office enums: wdFormatXMLDocument = 12,
# xlOpenXMLWorkbook = 51, ppSaveAsOpenXMLPresentation = 24.
LEGACY_FORMATS = {
    ".doc": ("Word.Application", ".docx", 12),
    ".xls": ("Excel.Application", ".xlsx", 51),
    ".ppt": ("PowerPoint.Application", ".pptx", 24),
}

_WORD_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject Word.Application
$app.Visible = $false
try {
    $doc = $app.Documents.Open('@SRC@', $false, $true)
    $doc.SaveAs2('@DST@', @FMT@)
    $doc.Close($false)
} finally {
    $app.Quit()
}
"""

_EXCEL_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject Excel.Application
$app.Visible = $false
$app.DisplayAlerts = $false
try {
    $book = $app.Workbooks.Open('@SRC@')
    $book.SaveAs('@DST@', @FMT@)
    $book.Close($false)
} finally {
    $app.Quit()
}
"""

_POWERPOINT_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
try {
    $deck = $app.Presentations.Open('@SRC@', $true, $false, $false)
    $deck.SaveAs('@DST@', @FMT@)
    $deck.Close()
} finally {
    $app.Quit()
}
"""

_SCRIPTS = {
    "Word.Application": _WORD_SCRIPT,
    "Excel.Application": _EXCEL_SCRIPT,
    "PowerPoint.Application": _POWERPOINT_SCRIPT,
}


class LegacyConversionError(RuntimeError):
    """Raised when Office could not upgrade a legacy binary file."""


def is_legacy(path: Path) -> bool:
    return path.suffix.lower() in LEGACY_FORMATS


def upgrade(path: Path, workdir: Path) -> Path:
    """Upgrade a legacy binary Office file, returning the new OOXML path.

    `workdir` should be a caller-owned temporary directory; the converted
    file is written there and lives as long as that directory does.
    """
    progid, modern_ext, fmt = LEGACY_FORMATS[path.suffix.lower()]
    source = path.resolve()
    target = (workdir / (source.stem + modern_ext)).resolve()

    script = (
        _SCRIPTS[progid]
        .replace("@SRC@", str(source).replace("'", "''"))
        .replace("@DST@", str(target).replace("'", "''"))
        .replace("@FMT@", str(fmt))
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not target.exists():
        raise LegacyConversionError(
            f"Microsoft Office could not convert {path.name} via {progid}.\n"
            f"{result.stderr.strip()}"
        )
    return target


def temp_workdir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(prefix="doc2md-")
