"""
Extract raw text and images from lecture slide PDFs.

Usage:
    python extract_pdf.py <pdf_path> [--pages 1,3,5-10] [--images-dir DIR]

Examples:
    python extract_pdf.py "Slides/Lecture-08.pdf"
    python extract_pdf.py "Slides/Lecture-08.pdf" --images-dir extracted_slides/images
    python extract_pdf.py "Slides/Lecture-08.pdf" --pages 5-12

Output:
    Text is printed to stdout as Markdown. Redirect to a file to save:
        python extract_pdf.py "Slides/Lecture.pdf" --images-dir out/img > out/lecture.md

    When --images-dir is provided, embedded images are saved there and
    referenced in the Markdown output via ![](path) syntax.

Dependencies:
    pip install pymupdf
"""

import argparse
import sys
import io
from pathlib import Path

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF is required. Install it with: pip install pymupdf")
    sys.exit(1)


def parse_page_ranges(page_str: str, max_page: int) -> list[int]:
    """Parse a page range string like '1,3,5-10' into 0-indexed page numbers."""
    pages = []
    for part in page_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = max(1, int(start))
            end = min(max_page, int(end))
            pages.extend(range(start - 1, end))
        else:
            p = int(part)
            if 1 <= p <= max_page:
                pages.append(p - 1)
    return sorted(set(pages))


# Map PyMuPDF CSNAME to file extension
_EXT_MAP = {
    "png": "png",
    "jpeg": "jpg",
    "jpg": "jpg",
    "jpx": "jp2",
    "jbig2": "jbig2",
    "bmp": "bmp",
    "tiff": "tiff",
}


def save_image(doc: fitz.Document, xref: int, images_dir: Path,
               pdf_stem: str, page_num: int, img_idx: int) -> str | None:
    """Extract one image by xref and save it. Returns the path to the saved file or None."""
    try:
        img = doc.extract_image(xref)
    except Exception:
        return None

    if not img or not img.get("image"):
        return None

    ext = _EXT_MAP.get(img.get("ext", ""), img.get("ext", "png"))
    filename = f"{pdf_stem}_p{page_num + 1}_img{img_idx + 1}.{ext}"
    filepath = images_dir / filename
    filepath.write_bytes(img["image"])
    return str(filepath)


def extract_text(pdf_path: str, pages: list[int] | None = None,
                 images_dir: Path | None = None, output_path: Path | None = None) -> None:
    """Extract text (and optionally images) from a PDF, printing or writing Markdown."""
    import contextlib

    doc = fitz.open(pdf_path)
    total = len(doc)
    pdf_stem = Path(pdf_path).stem

    if pages is None:
        pages = list(range(total))

    if images_dir:
        images_dir.mkdir(parents=True, exist_ok=True)

    out_file = None
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        out_file = open(output_path, "w", encoding="utf-8")
        out_dest = out_file
    else:
        out_dest = sys.stdout

    with contextlib.redirect_stdout(out_dest):
        print(f"# Slide: {Path(pdf_path).name}\n")

        for page_num in pages:
            if page_num >= total:
                continue
            page = doc[page_num]
            text = page.get_text("text").strip()

            print(f"## Page {page_num + 1}\n")
            if text:
                print(text)
            else:
                print("[This page contains only images, no extractable text]")

            # Handle images
            image_list = page.get_images(full=True)
            if image_list and images_dir:
                for idx, img_info in enumerate(image_list):
                    xref = img_info[0]
                    saved_path = save_image(doc, xref, images_dir,
                                            pdf_stem, page_num, idx)
                    if saved_path:
                        img_path = Path(saved_path)
                        # Compute relative path if output_path is specified
                        if output_path:
                            try:
                                display_path = img_path.resolve().relative_to(output_path.parent.resolve()).as_posix()
                            except ValueError:
                                display_path = img_path.as_posix()
                        else:
                            display_path = img_path.as_posix()
                        print(f"\n![Page {page_num + 1} image {idx + 1}]({display_path})")
            elif image_list:
                print(f"\n[{len(image_list)} embedded image(s) — "
                      f"use --images-dir to extract them]")

            print("\n\n---\n")

    if out_file:
        out_file.close()
    doc.close()


def main():
    parser = argparse.ArgumentParser(
        description="Extract text and images from PDF slides")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--pages",
        help="Pages to extract, e.g. 1,3,5-10. Default: all pages",
        default=None,
    )
    parser.add_argument(
        "--images-dir",
        help="Directory to save extracted images. "
             "If omitted, images are noted but not saved.",
        default=None,
    )
    parser.add_argument(
        "--output", "-o",
        help="Path to the output Markdown file. If omitted, prints to stdout.",
        default=None,
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}")
        sys.exit(1)

    # Determine page list
    page_list = None
    if args.pages:
        doc = fitz.open(str(pdf_path))
        page_list = parse_page_ranges(args.pages, len(doc))
        doc.close()

    img_dir = Path(args.images_dir) if args.images_dir else None
    out_path = Path(args.output) if args.output else None
    extract_text(str(pdf_path), page_list, img_dir, out_path)


if __name__ == "__main__":
    main()
