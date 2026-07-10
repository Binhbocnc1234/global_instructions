---
name: slides-to-exam-prep
description: >
  Convert lecture slide PDFs into structured exam preparation materials.
  Extracts raw text and images from PDF slides, then synthesizes comprehensive
  study notes in Markdown format. Use when the user wants to create exam
  review documents from their lecture slides.
---

# Slides to Exam Preparation Materials

This skill converts lecture slide PDFs into high-quality, structured exam
preparation notes in Markdown format.

## Overview

The workflow has two phases:

1. **Extract** — Run `extract_pdf.py` to pull raw text and images from slide
   PDFs into `extracted_slides/`.
2. **Synthesize** — Read the extracted content and compose exam-ready study
   notes in Markdown.

---

## Phase 1: Extract raw content from slides

### Tool

The extraction script is at `scripts/extract_pdf.py` (relative to this skill
directory). Copy it to the project's `tools/` directory if not already there.

### Dependency

The script requires `PyMuPDF`. Install if missing:

```
pip install pymupdf
```

### Usage

**Text + images** (images saved to a directory and referenced in the Markdown with correct relative paths):

```bash
python tools/extract_pdf.py "Slides/lecture-name.pdf" \
    --images-dir extracted_slides/images \
    --output extracted_slides/lecture-name.md
```

- **Input**: One or more `.pdf` files from the `Slides/` directory.
- **Output**: One `.md` file per PDF in `extracted_slides/`, plus an `images/`
  subdirectory containing extracted images when `--images-dir` is used.
- Use `--pages` to extract specific page ranges:
  `python tools/extract_pdf.py "Slides/file.pdf" --pages 5-20 --output out.md`

### Batch extraction

When multiple PDFs need extracting, write a small loop:

```python
import subprocess, pathlib

slides_dir = pathlib.Path("Slides")
out_dir = pathlib.Path("extracted_slides")
img_dir = out_dir / "images"
out_dir.mkdir(exist_ok=True)

for pdf in slides_dir.glob("*.pdf"):
    out_file = out_dir / (pdf.stem + ".md")
    subprocess.run(
        ["python", "tools/extract_pdf.py", str(pdf),
         "--images-dir", str(img_dir),
         "--output", str(out_file)],
        check=True
    )
    print(f"Extracted: {pdf.name} -> {out_file.name}")
```

---

## Phase 2: Synthesize exam preparation materials

### Step 1 — Read project-level quality rules

Quality criteria:

1. **Language**: Vietnamese. Use English or bilingual for specialized terms not
   common in Vietnamese (e.g., "Agent", "Markov Decision Process").
2. **Completeness**: Every concept in the slides must appear in the notes. The
   notes must be self-contained — a student should be able to bring them into
   the exam room as a complete reference.
3. **Clarity**: Every concepts should be explained. If a concept is hard to understand, include a example. The example needs to be practical, perhaps an exercise for students to review for an exam.
4. **No external references**: Never write "According to slide N" or
   "See lecture N". The student will not have the slides in the exam room.
5. **No redundancy**: Do not include concept that is not in the slides.
   Slides define the exam scope.
6. **Exercise**: Exercise that likely appear in exams. Maybe you can get them in slides. Also provide answer
7. **Exam-focused Content (Relevance)**: Do not include introductory, historical, or non-examinable details (e.g., history of the Internet, general slides about computers, or execution runtime measurements like DFS running time with $n = 1000$ or $n = 10^6$ which are merely for illustrative/performance comparison). Focus strictly on conceptual understanding, formulas, algorithms, and worked exam-like exercises.

### Step 2 — Human Gate: Chunking Multiple Lectures (Long Tasks)

Since agents can struggle with long-running tasks, writing notes for too many lectures at once can lead to context/output truncation and lost detail. To prevent this:

- If you need to write notes for multiple lectures (e.g., more than 2 lectures) or if the slides are very long:
  1. **Select a subset**: Choose only the first 1 or 2 lectures.
  2. **Generate notes**: Compose the Markdown notes for only this subset.
  3. **Human Gate**: Stop execution, present the completed subset to the user, and ask for confirmation/approval before proceeding with the remaining lectures.

### Step 3 — Write Markdown study notes

Read each extracted Markdown file, understand the full content, then compose
structured study notes.

**Formatting rules:**

- Each `.md` file MUST be under 300 lines. If a topic exceeds this, split it
  into multiple files (e.g., `08-ml-basics.md`, `08-ml-algorithms.md`).
- Use `$...$` for inline math and `$$...$$` for display math. Markdown
  renderers (VS Code, GitHub) handle these natively.
- Use standard/popular Markdown elements: headings, bold, bullet lists, numbered
  lists, tables, code blocks.
- Because the slides provided by the teacher were of very poor quality, some text that should have been saved as text was saved as images instead. You need to read the images, extract text so that you do not miss any important details.
- When a slide contains an important diagram or figure, include the extracted
  image via `![description](path/to/image.jpg)` syntax. For example: Alpha-beta pruning graph or Neural network graph.

**Math example:**

```markdown
The Bellman optimality equation:

$$
V^*(s) = \max_a \sum_{s'} T(s, a, s') \left[ R(s, a, s') + \gamma V^*(s') \right]
$$
```

### Step 4 — Verify

- Confirm every file is under 250 lines.
- Confirm all slide topics are covered (cross-check extracted slide headings
  against the final notes).
- Do a final pass to ensure no "According to slide N" references remain.
- Verify all math expressions render correctly (check `$` delimiters are
  balanced).
- Verify image references point to existing files.
- Ensure no historical or irrelevant runtime comparison details (e.g., DFS with $n = 1000$) are included.

---

## Checklist before reporting completion

- [ ] All slide PDFs extracted to `extracted_slides/`.
- [ ] Images extracted (if slides contain diagrams/figures).
- [ ] Every concept from the slides is present in the notes.
- [ ] Content is in Vietnamese with bilingual specialized terms.
- [ ] No external references ("slide N", "lecture N").
- [ ] Excluded historical/irrelevant details (e.g., internet history, specific performance benchmarks like DFS runtime for $n=1000$).
- [ ] Concepts are explained clearly, not copied mechanically from slides.
- [ ] Hard concepts have worked examples.
- [ ] Every file is under 250 lines.
- [ ] Math expressions use `$...$` / `$$...$$` and render correctly.
- [ ] Image references are valid.
- [ ] Applied human gate for multiple/long lecture tasks, processing them in small batches.
