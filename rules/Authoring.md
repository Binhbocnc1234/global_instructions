# Authoring Rules

Summary: How do I write the artifact? Source code, Markdown documents, comments

## DRY(don't repeat yourself) 

A behavior, requirement, contract, or rationale has one canonical owner across code, Markdown, and code comments. Do not restate executable behavior in comments or copy implementations into documentation. Comments explain local non-obvious intent, invariants, or trade-offs; documentation owns cross-file policies and design; code and tests own behavior. Other locations link to or briefly identify the canonical source.

For example, a highlight effect already flickers a UI button, and a request adds a game character as a second thing to highlight. The agent writes a second function with the same timing and colour for the character. Now two functions own one effect, and a change to the flicker speed must be made twice. Instead, generalise the existing mechanism so that it accepts both kinds of target, and delete the copy.

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

## Markdown Document Kind

When to apply: creating a documentation file, choosing its folder, or adding a section to one.

A file has one main kind: the question its reader holds when opening it. The folder comes from that kind.

| Kind | Reader's question | Holds |
|---|---|---|
| How-to | How do I do this task? | Ordered steps for one kind of work, and the stop conditions met during them |
| Reference | What must hold, or what is the exact value? | Rules and contracts, each with its reason next to it, and lookup tables |
| Explanation | Why is it shaped this way? | Decisions, architecture, product vision, and the premise behind a design |

- The main kind is the kind that most of the file's sections answer. A section of another kind stays when the reader needs it at that point: the reason next to a rule, the command that runs a rule's check, a stop condition inside a step.
- When the main kind differs from the folder's kind, move the file.
- When a group of sections of another kind is read by a request that does not need the rest of the file, split that group into its own file and link to it.
- A project MAY add kinds for material these three do not cover, such as lessons or task records, and names them in its `AGENTS.md`.

For example, a document holds three rules for how the save file is written, each with its reason, and the command that checks them. Its main kind is reference, and the reasons and the command stay in it.

For example, a migration guide holds nine fidelity rules and seven slice steps. A code review reads the rules without the steps, so the rules move into their own reference file and the guide links to it.

Why: a rule and its reason are read together. A framework that files the rule under reference and its reason under explanation makes the reader open two files to apply one rule, and after [Documentation Audit](#documentation-audit) most documents that remain are rules with their reasons.

## Documentation Audit

When to apply: auditing a document, or deciding whether a sentence belongs in one.

**Use case.** Name at least one realistic request, from the developer or an agent, that needs the document and that code, data or a task file cannot answer. When there is none, delete the whole document. The document's description states why it exists, so a later audit starts from it.

A sentence stays when that request needs it. The common reasons it is needed, and where the sentence goes:

| Sentence | Where it goes |
|---|---|
| **Reason** that no code shows. A product goal counts: the audience and the intended experience are the reason behind every design that serves them | An ADR, the project's product-vision document for a product goal, or a code comment when only one file is affected |
| **Principle** that every instance of a kind must follow and that no code or lint checks. For example, the art style every character image follows | Its document, or the project `AGENTS.md` when almost every request needs it |
| **Future spec**, still planned and not built | A task in `delivery/deferred/`, under [Task Management](TaskManagement.md#task-management). A reason attached to it stays in a document. |
| **Flow** that no call chain from one entry point shows: it crosses a process or repository boundary, runs through a callback or event that another component fires later, or its source is out of reach (an LLM, an operating system kernel) | Pseudocode under [Explaining a Technique](Communication.md#explaining-a-technique), in the document that owns the design. Name the real files and functions, so a reader can check the pseudocode against the code. |

**Delete** (no link replaces it; name the symbol directly instead):
- Anything code or data shows, including "feature X is not used". A flow counts as shown when a reader can follow it from one function by go-to-definition, however many files it spans.
- Dead design.
- A copy of another document.
- Rule IDs that no code or test uses.
- Task steps and status. Open steps move to a task file.

For example, a reference document lists every module with its folder and layer, copied from the manifest that the boundary lint reads. The manifest holds the list, so the table is deleted. The reason one layer exists stays, because no manifest shows it.

Why: a document that restates code drifts from it without any check failing, and every reader pays to open it. A document that holds only what code cannot say stays true, and stays short enough to read.

## Documentation Index

When to apply: adding, removing, moving, renaming, or re-describing a document in a project that has an index.

A documentation index is one committed file that lists every qualifying document with its relative path and a one-sentence description. It is the canonical entry point for document discovery, so that a reader never opens a document just to learn what it holds. [Route Through the Documentation Index](WorkStyle.md#route-through-the-documentation-index) owns the reading half.

- The index is generated output. Never edit it by hand.
- Regenerate it in the same change that adds, removes, moves, renames, or re-describes an indexed document. A change that leaves the index stale is incomplete.
- Each entry's description answers the same question as the document's `Summary:` line, under [Markdown Document Structure](#markdown-document-structure). A description that does not let a reader decide whether to open the document is a defect in the description, not in the reader.
- The project's `AGENTS.md` records the index path, the command that regenerates it, which documents qualify, and where their descriptions come from. Those are project decisions, and no global rule fixes them.

For example, `MonkeyVsAlien` generates its index from the `description` and `status` frontmatter fields of every document under `Documentation/`, and its `AGENTS.md` records both the index path and the generator command.

A project that holds more than 10 documents and has no index has no routing. Propose one instead of reading the folder tree; [An Unrelated File Opened Is a Routing Defect](WorkStyle.md#an-unrelated-file-opened-is-a-routing-defect) says when that proposal is due.

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
