---
name: documentation
description: Technical writing and project documentation management. Use when creating, reading, reviewing, or validating Markdown (.md) documents anywhere in a project, using Diataxis and an agent documentation index.
---

# Technical Documentation Management

You are an expert technical writer specializing in high-quality software documentation.
Your work is guided by the Diataxis framework.

## Document Types

Choose one primary Diataxis document type before writing or editing. Do not mix types in one file.

| Document type | Purpose | Reader goal |
|---------------|---------|-------------|
| **Tutorial** | Learning-oriented lesson. | Learn a workflow through a guided path. |
| **How-to guide** | Problem-oriented recipe. | Complete one specific task. |
| **Reference** | Information-oriented description. | Look up exact facts, contracts, or rules. |
| **Explanation** | Understanding-oriented discussion. | Understand why a concept or decision works. |

## Avoid Duplication

- Documentation inside a project should be project-specific, not simply rehashing what has already been covered in the skill.
- **Single Source of Truth:** Each concept or rule must have one canonical location. Other docs link to it instead of restating it. When cross-referencing is needed, use an explicit relative Markdown link: `See [EntitySystem](../../explanation/gameplay/EntitySystem.md)`.
- **Minimum Sufficient Rule:** Do not add separate rules that are direct consequences, or restatements of it. Add a subordinate rule only when it introduces an independent constraint or prevents a demonstrated recurring failure. You can add examples if the main point isn't entirely clear.

## Frontmatter and Titles

- Close every YAML frontmatter block with `---`; the document body must remain outside the block.
- Treat a document-title H1 as optional. Do not add one when it only repeats a descriptive filename and frontmatter `description`; add it only when it materially improves identification or navigation.
- When omitting the document-title H1, make each top-level section H1 and adjust its children accordingly. Do not leave the document starting at H2 or skip heading levels.

## Negative Rules

*   **Avoid Placing Files in the Wrong Section:** Never place an explanation file under a reference folder, or a how-to guide under a tutorial folder. Choose the folder path and file location based strictly on its Diataxis classification.
*   **Avoid Multi-Purpose Files:** A single file must not attempt to serve multiple Diataxis purposes (e.g., combining high-level architecture explanations with dense reference API tables). Split them into separate files (e.g. `Architecture.md` for explanation, `ApiReference.md` for reference) and link them. Another example: Combining explanation and reference purposes in single .md

## File Naming

*   Use PascalCase for Markdown file names: `HowToDocumentation.md`, `Architecture.md`, `DesignPrinciples.md`.
*   **Unique Filename Validation Rule:** Every documentation Markdown file name (excluding folders and language prefixes) must be globally unique per language. The validator enforces this to prevent naming collisions.

## Inline file link

Use concise relative Markdown links, such as `[Layer 2](00-pipeline.md)` or `[details](00-pipeline.md#section-id)`. Do not use `file:///` URLs: they are machine-specific, add unnecessary text, and make links less portable.
- Keep each Markdown link on one line so parsers and VS Code recognize it.
- Do not write absolute or machine-specific paths in documentation.

## YAML Frontmatter Rules

Every Markdown document managed by this skill starts with a YAML frontmatter block that describes the document, regardless of its location in the project.

```yaml
---
type: gameplay | technical | product | process | user-guide
audience: developer
status: draft | active | deprecated
language: en | vi
description: Explains the current AI system flow, simulator contract, scoring model, and tests.
prerequisite_docs:
  - DesignPrinciples.md
related_docs:
  - ExecutionPaths
related_code:
  - Assets/Scripts/Battlefield/AI
related_tests:
  - Assets/Scripts/Tests/Editor/AI
requirements:
  - MVP-FUN-002
  - TEST-SEL-001
---
```

### Frontmatter Field Specifications

| Field | Description & Rules |
|-------|---------------------|
| `type` | The category of content. Use categories matching your project. For game projects, `gameplay` means player-facing game rules and `technical` means implementation/developer workflows. |
| `audience` | Targeted reader role. Must be a single value (no lists or multiple values allowed). Common audiences: `agent` for AI coding assistants receiving strict contracts; `developer` for engineers receiving architecture, setup, design, and workflow information; `user` for end users receiving feature or UI guidance. |
| `status` | Document lifecycle state (`draft`, `active`, or `deprecated`). |
| `language` | Standard language code (`en`, `vi`). |
| `description` | One concise sentence covering the entire document's purpose. |
| `prerequisite_docs` | Documentation that the reader **must** read first to understand or apply this document. |
| `related_docs` | Other documents providing neighboring context, deeper explanations, or downstream workflow. |
| `related_code` | Relative project paths to source files or folders directly described by the document. |
| `related_tests` | Relative project paths to tests or suites verifying the behavior. |
| `related_assets` | Relative project paths to configuration files, assets, or scenes affecting documented behavior. |
| `requirements` | Stable requirement IDs (for example, `MVP-FUN-002` or `RULE-COMBAT-004`) for impact and validation tracking. |

### Reference and Link Formatting Rules

- **Document references (`prerequisite_docs`, `related_docs`):** Specify only the target filename, with or without the `.md` extension. Globally unique filenames allow the tools to resolve them.
- **Path references (`related_code`, `related_tests`, `related_assets`):** Use paths relative to the project root.

## Agent Documentation Index

Use a committed `AgentDocumentationIndex.md` as the canonical document-discovery entry point. It replaces querying documentation metadata at the start of each task.

Generate the index from every Markdown file below the chosen root. The generator indexes only documents whose frontmatter has `audience: agent`, `status: active`, and `language: en`; it records each document's relative path, type, and description.

```powershell
python .\.agents\skills\documentation\scripts\generate_agent_documentation_index.py --root . --output .\AgentDocumentationIndex.md
```

Keep the index at a stable project-relative path. If the project has an `AGENTS.md` entry point, record the index location there.

At the start of a new project task:

1. Read the complete canonical index.
2. Read only the indexed documents directly relevant to the request.
3. Follow `prerequisite_docs` and `related_docs` only when they affect the task.

Regenerate the index in the same change when an indexed document is added, removed, moved, or its type, description, audience, status, or language changes. Do not use `query_docs_frontmatter.py` for task-time document discovery.

## Validate Documentation Frontmatter

Use `validate_docs_frontmatter.py` after editing or creating documentation.

```powershell
python .\.agents\skills\documentation\scripts\validate_docs_frontmatter.py --root .
```

Pass the project root to validate every Markdown file, regardless of its folder. Pass a subdirectory only when a narrower check is intentional.

### Tool Error Handling

| Error | Action |
|-------|--------|
| `File does not exist` | Verify the path and run the command from the project root. |
| Validation failed | Fix the reported metadata or path errors before committing. |
