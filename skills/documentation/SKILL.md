---
name: documentation
description: Technical writing and project documentation management. Use when creating, reading, reviewing, or validating Markdown (.md) documents anywhere
---

# Technical Documentation Management

You are an expert technical writer specializing in high-quality software documentation.

Documentation(.md and only .md files) is treated like law, everyone must adhere to it. However, since the documentation themselves aren't necessarily optimal, if you wish to do something that deviates from the documentation, you must update the documentation to align with current need.

## Avoid Duplication

- Documentation inside a project should be project-specific, not simply rehashing what has already been covered in the skill.
- **Single Source of Truth:** Each concept or rule must have one canonical location. Other docs link to it instead of restating it. When cross-referencing is needed, use an explicit relative Markdown link: `See [EntitySystem](../../explanation/gameplay/EntitySystem.md)`.
- **Minimum Sufficient Rule:** Do not add separate rules that are direct consequences, or restatements of it. Add a subordinate rule only when it introduces an independent constraint or prevents a demonstrated recurring failure. You can add examples if the main point isn't entirely clear.

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

### Document references belong in the body

A reference to another document MUST be an inline Markdown link placed at the point where the reader needs it. Do not collect document references into a list held apart from the prose that needs them.

A link at the point of use states both the target and the reason. A separated list states only the target, so the reader learns that a document matters but not which step needs it. Such a list is also a second navigation system running parallel to the body links, and it rots silently because no reader passes through it.

Write the dependency where the work happens:

```markdown
Slice the exported sheet in Godot. Follow the naming and child-count rules in
[CharacterArtAssetRequirements](CharacterArtAssetRequirements.md).
```

When a document cannot be applied at all without another one, link it in the opening paragraph and say so:

```markdown
This workflow assumes the module layout defined in [Architecture](../technical/Architecture.md).
```