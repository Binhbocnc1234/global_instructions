# Authoring Rules

Summary: How do I write the artifact? Source code, Markdown documents, comments

## DRY(don't repeat yourself) 

A behavior, requirement, contract, or rationale has one canonical owner across code, Markdown, and code comments. Do not restate executable behavior in comments or copy implementations into documentation. Comments explain local non-obvious intent, invariants, or trade-offs; documentation owns cross-file policies and design; code and tests own behavior. Other locations link to or briefly identify the canonical source.

Do not add a rule that is a direct consequence or a restatement of a rule that already exists. Add a subordinate rule only when it carries an independent constraint, or prevents a failure that has happened before. Adding an example to an existing rule is not a new rule.

The other half of DRY is about doing the same work twice, not storing the same fact twice. It fires while the agent executes, so [Automate Repeated Work](WorkStyle.md#automate-repeated-work) owns it.

## Describe What Exists, Not What Was Considered

When describing code, architecture, documentation, or any other artifact, describe **the current state directly**.

Do not explain the current design by mentioning alternatives that were considered, rejected, or merely imagined.

Avoid sentences such as:

* "If this were a `List`, lookup would be O(n)."
* "Unlike the naive approach, this does not allocate."
* "We could have used a coroutine here, but..."
* "With a non-strict `SORTED`, the target could occupy multiple positions..."

These sentences make the reader reason about something that does not exist.

Instead, state the property of the current artifact:

* "Dictionary lookup is O(1) on average."
* "The operation performs no allocation."
* "The operation runs synchronously."
* "By Corollary 0, there is at most one match."

## 250 lines rule

Keep source-code and documentation files at or below 250 lines whenever practical.

The 250-line limit is a signal to split responsibilities, not a target to satisfy through compression.

When a file is likely to exceed 250 lines:

1. Do not reduce readability by removing comments, collapsing formatting, shortening meaningful names, combining unrelated logic, or writing denser code.
2. Do not omit necessary information merely to stay below the limit.
3. Identify distinct responsibilities, concepts, sections, or components within the file.
4. Extract those responsibilities into separate, clearly named files.
5. Keep each resulting file cohesive and understandable on its own.
6. Update imports, references, navigation, indexes, or documentation links as needed.

A file may exceed 250 lines only when splitting it would create artificial fragmentation, excessive indirection, or reduce maintainability. In that case, explain why the exception is justified before proceeding.

## Markdown Document Structure

Every `.md` file follows this shape. Frontmatter, where the format needs it, sits above the title.

```markdown
# Name that represents the whole contents

Summary: <the question this file answers>? What the file holds.
Why: the reason the file exists(optional)

## name_1
...
## name_2
...
```

- One `#` title per file. It names the whole contents, not the first section.
- `Summary:` opens with the question the file answers, written as a question and ending in `?`. Use the question word that fits: who, what, when, where, why, how, which. The rest of the line says what the file holds.
- `Why:` is one or two sentences, directly under the summary.
- Every other heading is `##` or deeper.

For example, `Summary: How do I proceed? How the agent decides, executes, and stops.` A reader who does not hold that question skips the file, which is the point.

**Why**: the reader decides whether to keep reading from the title, the summary, and the reason. A file that opens with its first section forces the reader to infer all three.

## Markdown File Naming

- Use PascalCase for Markdown file names: `HowToDocumentation.md`, `Architecture.md`, `DesignPrinciples.md`.
- Every documentation Markdown file name, excluding folders and language prefixes, is unique across the project per language. The validator enforces this to prevent naming collisions.

## Markdown Document Purpose

One file serves one Diataxis purpose.

- Never place an explanation file under a reference folder, or a how-to guide under a tutorial folder. The folder comes from the file's Diataxis classification.
- A single file MUST NOT serve two Diataxis purposes, such as high-level architecture explanation together with dense reference API tables. Split them, for example `Architecture.md` for explanation and `ApiReference.md` for reference, and link one to the other.

## Inline file link

Use concise relative Markdown links, such as `[Layer 2](00-pipeline.md)` or `[details](00-pipeline.md#section-id)`. Do not use `file:///` URLs: they are machine-specific, add unnecessary text, and make links less portable.

- Keep each Markdown link on one line so parsers and VS Code recognize it.
- Do not write absolute or machine-specific paths in documentation.
- `@path` is not a link. It loads the file into the agent's context, so it belongs in an instruction file that the harness reads, such as `AGENTS.md` or a `SKILL.md`. Everywhere else, a reference to another document is a Markdown link.

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

## Editor Tool UI Names

When to apply: making UI, such as game UI, a Godot editor plugin or a Unity editor window.

- Every element the developer can point at shows its name in a tooltip on hover. Drawn items count too, such as a key mark or a playhead.
- The name comes from the tool's UI reference document. That document is canonical. Add a missing element to it in the same change.
- Set the tooltip delay to 1 second if possible
- This rule still apply to game UI but with nuance: Godot editor already have native tooltip in PlayMode, the tooltip shows Node's name when developer click at any Node

Why: Sometime developer want to report bug of an UI element or button, but they cannot remember the names of the UIs, and furthermore, the UIs were largely written by agents.
