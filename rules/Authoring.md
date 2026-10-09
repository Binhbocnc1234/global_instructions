# Authoring

Summary: What does the Authoring specialist do? Its responsibility, inputs, workflow, constraints, completion evidence, and responsibility transitions.
Why: one role owns this responsibility without copying shared principles.

Use the shared foundation in [AGENTS.md](../AGENTS.md).

## Responsibility

Create or maintain non-rule documentation.

## Inputs Required

The reader, their question, canonical sources, and the project documentation index.

## Workflow

Check whether documentation is needed. Choose its kind. Write what code cannot show. Update descriptions and regenerate the index.

## Role-Specific Constraints

## Markdown Document Kind

When to apply: creating a documentation file, or adding a section to one.

A file has one main kind: the question its reader holds when opening it. The kind decides how the file is written, not which folder it goes in. The folder comes from the topic the file serves, under [16 child rule](Implementation.md#16-child-rule).

| Kind | Reader's question | Holds |
|---|---|---|
| How-to | How do I do this task? | Ordered steps for one kind of work, and the stop conditions met during them |
| Rules | What must hold, or what is the exact value? | Rules and contracts, each with its reason next to it, and lookup tables |
| Explanation | Why is it shaped this way? | Architecture, product vision, and the premise behind a design |

- The main kind is the kind that most of the file's sections answer. A section of another kind stays when the reader needs it at that point: the reason next to a rule, the command that runs a rule's check, a stop condition inside a step.
- A decision record's main kind is Rules: its Decision section states what must hold, and its Why section is the reason next to it.
- When a group of sections of another kind is read by a request that does not need the rest of the file, split that group into its own file and link to it.
- A project MAY add kinds for material these three do not cover, such as lessons or task records, and names them in its `AGENTS.md`.

For example, a document holds three rules for how the save file is written, each with its reason, and the command that checks them. Its main kind is rules, and the reasons and the command stay in it.

For example, a migration guide holds nine fidelity rules and seven slice steps. A code review reads the rules without the steps, so the rules move into their own rules file and the guide links to it.

Why: a rule and its reason are read together. A layout that files the rule and its reason under two different kinds makes the reader open two files to apply one rule, and after [Documentation Audit](#documentation-audit) most documents that remain are rules with their reasons.

## Documentation Audit

Condition for the document to exist: Very simple, the documentation must contain information that is difficult to find in the code or is not present in the code at all. The description field will clearly show that.

Typically, the following common scenarios arise:

| Sentence | Where it goes |
|---|---|
| **Reason** that no code shows. A product goal counts: the audience and the intended experience are the reason behind every design that serves them | An ADR, the project's product-vision document for a product goal, or a code comment when only one file is affected |
| **Principle** that every instance of a kind must follow and that no code or lint checks. For example, the art style every character image follows | Its document, or the project `AGENTS.md` when almost every request needs it |
| **Future spec**, still planned and not built | A task in `delivery/deferred/`, under [Task Management](Leader.md#task-management). A reason attached to it stays in a document. |
| **Flow** that no call chain from one entry point shows: it crosses a process or repository boundary, runs through a callback or event that another component fires later, or its source is out of reach (an LLM, an operating system kernel) | Pseudocode under [Explaining a Technique](Explanation.md#explaining-a-technique), in the document that owns the design. Name the real files and functions, so a reader can check the pseudocode against the code. |

**Delete** (no link replaces it; name the symbol directly instead):
- Anything code or data shows, including "feature X is not used". A flow counts as shown when a reader can follow it from one function by go-to-definition, however many files it spans.
- Dead design.
- A copy of another document.
- Rule IDs that no code or test uses.
- Task steps and status. Open steps move to a task file.

For example, a rules document lists every module with its folder and layer, copied from the manifest that the boundary lint reads. The manifest holds the list, so the table is deleted. The reason one layer exists stays, because no manifest shows it.

Why: a document that restates code drifts from it without any check failing, and every reader pays to open it. A document that holds only what code cannot say stays true, and stays short enough to read.

## Documentation Index

When to apply: adding, removing, moving, renaming, or re-describing a document in a project that has an index.

A documentation index is one committed file that lists every qualifying document with its relative path and a one-sentence description. It is the canonical entry point for document discovery, so that a reader never opens a document just to learn what it holds. [Route Through the Documentation Index](Execution.md#route-through-the-documentation-index) owns the reading half.

- The index is generated output. Never edit it by hand.
- Regenerate it in the same change that adds, removes, moves, renames, or re-describes an indexed document. A change that leaves the index stale is incomplete.
- Each entry's description answers the same question as the document's `Summary:` line, under [Markdown Document Structure](../AGENTS.md#markdown-document-structure). A description that does not let a reader decide whether to open the document is a defect in the description, not in the reader.
- A document that states rules names them in its description. `Records the decision to ...` describes an event, so a reader who is about to act skips it. Write `Rules for which values go in a data file and which stay as constants in code, with the reasons` instead.
- The project's `AGENTS.md` records the index path, the command that regenerates it, which documents qualify, and where their descriptions come from. Those are project decisions, and no global rule fixes them.

For example, `MonkeyVsAlien` generates its index from the `description` and `status` frontmatter fields of every document under `Documentation/`, and its `AGENTS.md` records both the index path and the generator command.

A project that holds more than 10 documents and has no index has no routing. Propose one instead of reading the folder tree; [An Unrelated File Opened Is a Routing Defect](Execution.md#an-unrelated-file-opened-is-a-routing-defect) says when that proposal is due.

## Completion Evidence

The document, its canonical references, and an updated generated index where applicable.

## Responsibility Transitions

Return documents and reference checks to Leader. Identify instruction changes for RuleMaintenance. Use Explanation only when the developer requests explanation. Learning materials activate the learning-material skill.
