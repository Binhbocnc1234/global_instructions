---
name: book-to-skill
description: "Convert books and documents (PDF, EPUB, DOCX, HTML, Markdown, text, RTF, MOBI/AZW) into structured agent skills."
---

# Book-to-Skill Converter

Transform written knowledge into source-grounded operational guidance. Preserve every
instruction that materially changes agent behavior, while removing narrative and repetition.

## Invocation Contract

Accept YAML-like input or natural language then normalize them into this schema before doing work.

```yaml
mode: full
sources: []
analysis_source: null
skill_name: null
existing_skill: null
content_type: auto
purpose: [apply, mental-models, reference]
depth: auto
destination: auto
destination_path: null
existing_policy: ask
install_missing: ask
confirm_before_generation: true
```

### Mandatory Parameters

| Parameter | Required when | Meaning |
|---|---|---|
| `mode` | Always | `full`: extract and generate a complete skill. `analyze`: extract and return a structured report without creating a skill. `generate`: create a skill from `analysis_source` without extracting documents. `update`: merge new sources into an existing skill. |
| `sources` | `mode` is `full`, `analyze`, or `update` | Non-empty list of readable document paths, directories, glob patterns, or attached files resolved to local paths. Supported extensions: `.pdf`, `.epub`, `.docx`, `.txt`, `.md`, `.markdown`, `.rst`, `.adoc`, `.html`, `.htm`, `.rtf`, `.mobi`, `.azw`, `.azw3`. |
| `analysis_source` | `mode` is `generate` | Prior structured analysis supplied inline or as a readable file path. |
| `skill_name` | `mode` is `update` and `existing_skill` is omitted | Existing skill name or slug that identifies the skill being updated. Outside `update`, optionally sets the generated lowercase hyphenated slug; if omitted, derive `{author-lastname}-{core-concept}`, falling back to the normalized title. |
| `existing_skill` | `mode` is `update` and `skill_name` is omitted | Existing skill directory or discoverable slug that identifies the skill being updated. |

### Optional Parameters and Values

If omitted, these parameters use default values.

| Parameter | Default | Allowed values and behavior |
|---|---|---|
| `content_type` | `auto` | `auto`: inspect representative content; classify as `technical` when code, tables, formulas, or diagrams matter, otherwise `text`. `technical`: use structure-aware extraction such as Docling. `text`: use the fastest prose-oriented extractor. |
| `purpose` | all three values | List containing `apply` (use frameworks during work), `mental-models` (reason in the author's style), and/or `reference` (look up chapters and concepts). It controls emphasis in the generated skill. |
| `depth` | `auto` | `auto`: use `reference` only when `purpose` contains only `reference`; otherwise use `study`. `reference` minimizes explanatory examples; `study` includes useful reasoning and worked examples. Both preserve all materially behavior-changing instructions. |
| `destination` | `auto` | `auto`: select the first existing personal skill root supported by the active host, otherwise create its standard personal root. `project`: use the active host's project-local skill root. `global`: use its standard personal root. `path`: use `destination_path`. |
| `destination_path` | `null` | Required when `destination` is `path`; otherwise ignored. Use an absolute or project-relative skill root under which the generated skill directory is written. |
| `existing_policy` | `ask` | Collision behavior: `ask` requests one decision at collision time; `update` merges; `overwrite` replaces generated files only after explicit authorization; `rename` chooses the next available `-2`, `-3`, etc. suffix. |
| `install_missing` | `ask` | Optional extractor dependency behavior: `ask`, `yes`, or `no`. `no` uses an available fallback or stops when none exists. |
| `confirm_before_generation` | `true` | `true`: show the post-extraction cost estimate and wait once before generating or updating. `false`: report the estimate and continue without pausing. Has no effect in `analyze` mode. |

### Input Examples

Minimal input uses every default:

```text
Use $book-to-skill on C:\Books\ddia.pdf.
```

Complete structured input:

```yaml
mode: full
sources: [C:\Books\ddia.pdf]
analysis_source: null
skill_name: ddia
existing_skill: null
content_type: technical
purpose: [apply, reference]
depth: study
destination: project
destination_path: null
existing_policy: ask
install_missing: ask
confirm_before_generation: true
```

Update input:

```yaml
mode: update
sources: [C:\Books\ddia-second-edition.pdf]
analysis_source: null
skill_name: null
existing_skill: ddia
content_type: technical
purpose: [apply, mental-models, reference]
depth: auto
destination: project
destination_path: null
existing_policy: ask
install_missing: ask
confirm_before_generation: true
```

## Normalize and Validate Once

1. Parse explicit values from the request. Treat legacy positional paths as `sources`;
   treat a final lowercase hyphenated token as `skill_name` only when it is not a
   resolvable source.
2. Apply every documented default.
3. Derive `content_type`, `depth`, `skill_name`, and the destination root where their
   normalized values are `auto` or `null`.
4. Validate allowed values, supported sources, and conditional mandatory parameters.
5. If mandatory information remains unresolved, ask one consolidated question listing
   only those missing fields. Never ask about omitted optional fields with defaults.
6. Keep the normalized configuration fixed for the run unless the user explicitly
   overrides it. Do not reinterpret later replies as new parameters except the cost
   confirmation or an `existing_policy: ask` collision decision.

If no usable input exists, return the schema and identify the missing mandatory fields.

## Mode Routing

- `full`: extract sources, analyze structure, generate all skill files, preserve raw
  extracts locally, and report.
- `analyze`: extract sources and return frameworks, principles, techniques,
  anti-patterns, suggested names, and detected chapters. Do not create skill files.
- `generate`: use `analysis_source`, then generate all skill files without extraction.
- `update`: extract new sources, resolve `existing_skill`, and follow the update workflow
  in [references/generation-spec.md](references/generation-spec.md).

## Execute

### 1. Resolve Destination and Collisions

Use these host roots for `auto`, `project`, and `global`:

| Host | Personal roots in preference order | Project root |
|---|---|---|
| Codex | `~/.agents/skills` | `.agents/skills` |
| GitHub Copilot CLI | `~/.copilot/skills`, `~/.agents/skills` | `.github/skills`, then `.agents/skills` |
| Amp | `~/.agents/skills`, `~/.config/agents/skills`, `~/.config/amp/skills` | `.agents/skills` |
| Claude Code | `~/.claude/skills` | `.claude/skills` |

For `auto`, use the first existing personal root; if none exists, create the first root
listed for the detected host. For `global`, use or create the first personal root. For
`project`, use the first project root. Ask which host is active only if it cannot be
detected and the destination cannot otherwise be resolved.

When the target exists, apply `existing_policy`. Never overwrite silently.

### 2. Extract and Estimate

For modes with `sources`, read and follow
[references/extraction-workflow.md](references/extraction-workflow.md). Use normalized
`content_type` and `install_missing`; do not ask separate content-type or dependency
questions unless the normalized value is `ask`.

After extraction, calculate the cost estimate documented in the extraction workflow.
If `confirm_before_generation` is true for `full` or `update`, pause once. Accept
`proceed`, `analyze`, or `stop`; `analyze` changes only the mode and returns the analysis
report. Do not collect any other schema fields at this point.

### 3. Analyze Structure

Identify title, author, chapters, table of contents, core themes, named frameworks,
principles, techniques, and anti-patterns. For sources over 50,000 tokens, search and
read bounded chapter slices rather than loading or rereading the entire corpus.

For `analyze`, return:

```markdown
## Extraction Report — <Title>
### Author's Core Frameworks
### Key Principles
### Techniques & Methods
### Anti-patterns
### Suggested Skill Name
### Chapters Detected
```

### 4. Generate or Update

Create `<skill-root>/<skill_name>/guides/`, then read
[references/generation-spec.md](references/generation-spec.md) completely and follow
its generation, preservation, cleanup, and update instructions. Pass normalized
`content_type` as `BOOK_TYPE` and normalized `depth` as `DEPTH`.

## Quality Rules

1. Preserve every source instruction whose removal could materially change agent behavior.
2. Compress wording and repetition, never required behavior or verification criteria.
3. Organize generated guides by agent capability, not necessarily by source chapter.
4. Define uncommon, ambiguous, source-specific, or operationally significant terms only.
5. Keep common conventional terms out of the glossary unless their meaning affects action.
6. Audit instruction coverage and preserve guidance-to-source traceability.
7. Front-load generated `SKILL.md` routing and load complete guides on demand.
8. Separate operational guidance from locally retained raw evidence.
9. Never publish copyrighted or private raw extracts without explicit authorization.
