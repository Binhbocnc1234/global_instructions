# Extraction Workflow

Use this workflow only after normalizing and validating the complete invocation schema
in `SKILL.md`. Do not collect or redefine user inputs here.

## Contents

- Resolve sources
- Resolve content type
- Run extraction
- Inspect outputs
- Estimate generation cost
- Read large sources efficiently

## Resolve Sources

Expand every file, directory, and glob in normalized `sources`. Keep supported files:

`.pdf`, `.epub`, `.docx`, `.txt`, `.md`, `.markdown`, `.rst`, `.adoc`, `.html`,
`.htm`, `.rtf`, `.mobi`, `.azw`, `.azw3`.

Resolve attached documents to readable local paths before invoking the extractor. Reject
missing paths and empty expansions. Continue past an individual unreadable source only
when at least one valid source remains, and report every skipped source.

## Resolve Content Type

Map normalized `content_type` to `BOOK_TYPE`:

- `technical` -> `technical`
- `text` -> `text`
- `auto` -> inspect representative pages or sections. Choose `technical` when accurate
  preservation of code, tables, formulas, or diagrams matters; otherwise choose `text`.
  If inspection is inconclusive, choose `text` and warn that structural fidelity may be
  limited.

Do not ask the user to classify content after normalization.

## Run Extraction

Find `scripts/extract.py` in this order:

1. The `scripts/` directory beside the active book-to-skill `SKILL.md`
2. `~/.copilot/skills/book-to-skill/scripts/extract.py`
3. `~/.agents/skills/book-to-skill/scripts/extract.py`
4. `~/.claude/skills/book-to-skill/scripts/extract.py`
5. `.github/skills/book-to-skill/scripts/extract.py`
6. `.claude/skills/book-to-skill/scripts/extract.py`
7. `.agents/skills/book-to-skill/scripts/extract.py`
8. `~/.config/agents/skills/book-to-skill/scripts/extract.py`
9. `~/.config/amp/skills/book-to-skill/scripts/extract.py`

Stop with a clear error when the script is unavailable.

Choose `python3`, falling back to `python`. Run:

```text
<python> <extract.py> <sources...> --mode <BOOK_TYPE> --install-missing <install_missing>
```

Show `banner.txt` beside the script when present. The extractor may use these fallbacks:

- Technical PDF: Docling
- Text PDF: `pdftotext`, then `pypdf`, then `pdfminer.six`
- EPUB: `ebooklib`, then standard-library ZIP parsing
- DOCX: `python-docx`, then ZIP/XML parsing
- HTML: `beautifulsoup4`, then standard-library HTML parsing
- RTF: `striprtf`, then regex fallback
- MOBI/AZW: Calibre `ebook-convert`

Honor normalized `install_missing`:

- `yes`: install required optional packages when safe and supported.
- `no`: do not install; use a working fallback or stop.
- `ask`: request permission only when installation would materially improve or unblock
  extraction. This is the documented parameter behavior, not a new input question.

Use `<python> <extract.py> --check` for dependency diagnostics when needed.

## Inspect Outputs

The extractor writes under `<tempdir>/book_skill_work/`:

- `full_text.txt`: combined text with source boundaries
- `metadata.json`: combined and per-source size, format, page, word, and token data
- `raw-source-extract/*.txt`: one stable content-hash extract per source

Read `metadata.json`. Stop if no source succeeded. Keep the temporary workspace until
raw extracts have been preserved successfully by the generation workflow.

## Estimate Generation Cost

Before `full` or `update` generation, report:

- Sources and formats
- Approximate pages or sections, words, and source tokens
- Estimated input, output, and total tokens
- Estimated time
- Files that will be created or updated, including capability guides and `source-map.md`

Calculate:

- Input tokens: `estimated_tokens * 1.3`
- Output tokens: provide a broad planning range based on the number of material
  instructions discovered during structure analysis. Label it as an estimate, never a
  generation limit. If instruction inventory has not completed, state that output size
  cannot yet be estimated reliably.

Do not derive or enforce per-chapter token budgets. Generation ends when all materially
behavior-changing instructions are represented and coverage-audited.

Label monetary prices as dated reference estimates when reporting them. Do not present
stale model prices as current facts.

If normalized `confirm_before_generation` is true, return the estimate and wait once.
Otherwise continue after reporting it. Do not ask for purpose, depth, naming, destination,
or collision behavior here.

## Read Large Sources Efficiently

For sources over approximately 50,000 tokens, treat `full_text.txt` as a queryable corpus:

1. Find chapter headings and line offsets with targeted search.
2. Read only the table of contents and relevant chapter slices.
3. Verify named frameworks with exact searches before including them.
4. Avoid loading the full source repeatedly for each generated chapter.

This keeps generation cost proportional to selected content instead of multiplying the
entire source by the chapter count.
