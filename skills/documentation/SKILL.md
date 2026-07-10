---
name: documentation
description: Technical writing and project documentation management. Use when creating, reviewing, validating, or reading project documents under Documentation/ using Diataxis guidelines and custom search tools.
---

# Technical Documentation Management

You are an expert technical writer specializing in high-quality software documentation.
Your work is guided by the Diataxis framework.

## Guiding Principles

1. **Clarity:** Write in simple, clear, and unambiguous language.
2. **Accuracy:** Ensure all details, code snippets, and configuration examples are correct.
3. **User-Centricity:** Every document must serve a specific reader role (player, developer, agent).
4. **Consistency:** Maintain consistent tone, structure, and style across documentation.
5. **Single Source of Truth:** Each concept or rule must have one canonical location. Other docs link to it instead of restating it.

## Document Types

Choose one primary Diataxis document type before writing or editing. Do not mix types in one file.

| Document type | Purpose | Reader goal |
|---------------|---------|-------------|
| **Tutorial** | Learning-oriented lesson. | Learn a workflow through a guided path. |
| **How-to guide** | Problem-oriented recipe. | Complete one specific task. |
| **Reference** | Information-oriented description. | Look up exact facts, contracts, or rules. |
| **Explanation** | Understanding-oriented discussion. | Understand why a concept or decision works. |

## Consistency & Naming Rules

### Avoid Duplication

Two documents must not describe the same logic or workflow. When cross-referencing is needed, use an explicit relative Markdown link: `See [EntitySystem](../../explanation/gameplay/EntitySystem.md)`.
Documentation inside a project should be project-specific, not simply rehashing what has already been covered in the skill.

### Negative Rules
*   **Avoid Placing Files in the Wrong Section:** Never place an explanation file under a reference folder, or a how-to guide under a tutorial folder. Choose the folder path and file location based strictly on its Diataxis classification.
*   **Avoid Multi-Purpose Files:** A single file must not attempt to serve multiple Diataxis purposes (e.g., combining high-level architecture explanations with dense reference API tables). Split them into separate files (e.g. `Architecture.md` for explanation, `ApiReference.md` for reference) and link them.

### File Naming
Follow the project's naming convention. If the project has no convention, use PascalCase for Markdown file names.
*   *PascalCase Examples:* `HowToDocumentation.md`, `Architecture.md`, `DesignPrinciples.md`.
*   *Legacy mismatch fix:* Do not use kebab-case or mixed casing like `How-to-documentation.md` unless the project specifically mandates it.

## Detailed Guidelines & Tools Reference

Refer to the dedicated reference documents below for complete instructions and templates:

*   **[Writing Guidelines & Templates](file:///c:/Users/binhb/.agents/skills/documentation/references/WritingGuidelines.md):** Detailed guidelines on frontmatter, link formats, and checklists/templates (with game-specific examples) for all 4 Diataxis types.
*   **[Reading & Validating Documentation Tools](file:///c:/Users/binhb/.agents/skills/documentation/references/ReadingTools.md):** Comprehensive instructions on using the Python scripts under `scripts/` to search, slice, and validate project documentation.
