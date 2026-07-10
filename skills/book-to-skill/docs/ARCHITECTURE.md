# Architecture

book-to-skill has two halves: a **deterministic extractor** (Python) and a
**spec-driven generator** (the agent following `SKILL.md`). The extractor turns any
document into clean text + metadata; the agent turns that into a structured skill.

```
            ┌─────────────────────────── EXTRACTOR (Python, deterministic) ──┐
 documents  │  scripts/extract.py  →  extractor/                              │
 (pdf/epub/ │    ├─ utils.py        CLI parse · multi-source resolve · runner │
  docx/...) │    ├─ config.py       supported extensions · paths · deps map   │
     │      │    ├─ dependencies.py optional-dep probing · --check report     │
     ▼      │    └─ parsers/        pdf · epub · docx · html · rtf · calibre · │
 ───────────│                        text  (best tool first, stdlib fallback) │
            │  output → <tempdir>/book_skill_work/                            │
            │    full_text.txt   (all sources merged, source-marked)          │
            │    metadata.json   (pages, words, tokens, chapters, ToC)        │
            │    raw-source-extract/*.txt (stable per-source raw text)         │
            └────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
            ┌─────────────────────────── GENERATOR (agent, follows SKILL.md) ┐
            │  Step 1.5  ask content type → BOOK_TYPE (technical | text)      │
            │  Step 2/2.5 extract · cost estimate · confirm                   │
            │  Step 2.6  REPL-style probing for large books (grep/sed, no     │
            │            full re-reads)                                        │
            │  Step 3    analyze structure (title, author, chapters, ToC)     │
            │  Step 4    purpose → DEPTH (reference | study)                   │
            │  Step 7    capability guides + behavioral coverage audit        │
            │  Step 8    selective glossary · source map · decision aids      │
            │  Step 9     SKILL.md core + indexes                             │
            │  Step 9.5   preserve raw extracts + sanitized manifest          │
            └────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                <SKILLS_HOME>/<slug>/  ← chosen per host:
                  ~/.copilot/skills/   GitHub Copilot CLI
                  ~/.agents/skills/    Copilot CLI or Amp (cross-agent)
                  ~/.claude/skills/    Claude Code
                  .github|.claude|.agents/skills/  project-local
                  SKILL.md         core rules + capability and topic indexes
                  guides/*.md      complete operational guidance, on demand
                  glossary.md      ambiguous or operationally significant terms
                  source-map.md    guidance-to-source traceability
                  patterns.md      techniques
                  cheatsheet.md    decision rules / trees / trade-offs / tells
                  raw-source-extract/ local-only source text + cache-style .gitignore
```

## Design principles

1. **Separate knowledge from evidence** — polished files contain synthesized
   frameworks and decision rules; raw passages live only in
   `raw-source-extract/` for on-demand verification.
2. **Compile-time over runtime** — pay navigation/structuring once; at query time
   load only the relevant guide. See [PERFORMANCE.md](PERFORMANCE.md).
3. **Behavioral completeness** — omit repetition, not instructions that change
   decisions, actions, constraints, or verification.
4. **On-demand guides** — `SKILL.md` stays small; operational files load only when read.
5. **Front-loaded `SKILL.md`** — most important content first (compaction truncates
   from the end).
6. **Graceful degradation** — every format has a stdlib fallback; one bad source is
   skipped, not fatal.

## Key components

| Path | Responsibility |
|------|----------------|
| `scripts/extract.py` | thin entrypoint wrapper |
| `scripts/extractor/utils.py` | CLI parsing, multi-source resolution, chapter/ToC detection, runner |
| `scripts/extractor/parsers/` | one module per format |
| `scripts/extractor/dependencies.py` | optional-dependency probing + `--check` |
| `tools/discovery_tax.py` | measures token cost vs context-dump / discovery loop |
| `tools/validate_skill.py` | checks a generated SKILL.md against host rules (`--lens claude|copilot|amp`) |
| `SKILL.md` | the generator spec (Steps 0–10 + fold-in workflow) |

## Extending

- **New format** → add `parsers/<fmt>.py`, register its extension in `config.py`,
  wire dependency probing in `dependencies.py`, branch in `utils.extract_single_file`.
- **New generation behavior** → edit the relevant Step in `SKILL.md`; keep it lean
  and back the change with evidence (see CONTRIBUTING.md).
