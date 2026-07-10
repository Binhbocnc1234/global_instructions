import json
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from preserve_raw_extract import preserve


def test_preserve_raw_extract_merges_and_sanitizes(tmp_path):
    workdir = tmp_path / "work"
    raw_dir = workdir / "raw-source-extract"
    raw_dir.mkdir(parents=True)
    (raw_dir / "book-abc.txt").write_text("raw text", encoding="utf-8")
    metadata = {
        "source_file": "/private/path/book.pdf",
        "extraction_mode": "text",
        "total_sources": 1,
        "pages": 10,
        "words": 100,
        "estimated_tokens": 133,
        "sources": [
            {
                "source_file": "/private/path/book.pdf",
                "filename": "book.pdf",
                "format": "pdf",
                "extraction_method": "test",
                "pages": 10,
                "pages_label": "pages",
                "chars": 500,
                "words": 100,
                "estimated_tokens": 133,
                "raw_extract_file": "book-abc.txt",
            }
        ],
    }
    (workdir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

    target = preserve(workdir, tmp_path / "skill")
    preserve(workdir, tmp_path / "skill")

    assert (target / "book-abc.txt").read_text(encoding="utf-8") == "raw text"
    assert (target / ".gitignore").read_text(encoding="utf-8").endswith(
        "*\n!.gitignore\n"
    )
    manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["runs"]) == 1
    assert "source_file" not in json.dumps(manifest)
