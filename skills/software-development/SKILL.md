---
name: software-development
description: Deterministic workflow for software development, including games. Use it for every request involve software — explanation, design, implementation, migration, refactor, or bug fix. Apply it even when the user only asks "how does X work?", "could we do Y?", or "fix this bug", and even when the change looks like a one-liner, because the cost of skipping the evidence and verification steps lands after the change ships.
---

# Software Development

Use repository evidence to move from requirements to a verified, documented, and intentionally committed change. Project instructions are the authority for technology-specific commands and for explicit exceptions to anything below.

## Understand the Request

1. Classify the task as explanation, design, implementation, migration(for example: convert Unity game project to Godot project), or bug fixing. One request may carry several tasks; classify each.
2. Read the project documentation index when one exists.
3. Inspect only the documents, code, configuration, and tests needed to understand the affected concepts and the entry route.
4. Separate direct observations from interpretations. Cite exact files, symbols, logs, commands, or documentation for load-bearing conclusions.
5. Stop when a missing requirement, dependency, artifact, or risky decision would force an important guess. State the blocker and its evidence.
6. Decide inexpensive, reversible details locally when they do not change product intent or architecture.

For explanation or design-only requests, do not mutate the project unless the user also requests implementation.

## Load Task-Specific Guidance

Read the matching reference before acting, not after. Each one carries refinements this file deliberately omits, and a refinement read afterwards only tells you what to redo.

| Before you | Read |
|---|---|
| Write or refactor production code | [ConstructionGuidance](references/ConstructionGuidance.md) |
| Select, write, or execute tests | [TestingStrategy](references/TestingStrategy.md) |
| Diagnose or fix a bug | [Debugging](references/Debugging.md) |
| Commit to a non-functional target. Read this document if the request mentions non-functional targets or qualities to be achieved. | [SoftwareQuality](references/SoftwareQuality.md) |

### Binding Documents

A project's process document constrains the result. It is not reference material. Reading a document for an answer and reading it to be bound by it are different acts.

- When a project names a process document, read it whole and read it yourself before planning. A subagent's summary does not count: a summary keeps the general principle and drops the refinement that forbids what you were already going to do.
- Before calling a unit of work done, restate that document's constraints as a checklist and answer each one against what you actually produced. Put the checklist in the report.
- A constraint with no evidence beside it means the work is not done.

## Plan Proportionally

Create a short sequential plan when the task spans multiple responsibilities, has dependencies, or carries meaningful regression risk. Keep one step active at a time, and update the plan when evidence changes it.

- Work dependency-first.
- Keep the requested scope explicit.
- Preserve unrelated and concurrent edits.
- Identify the focused verification method before implementation.

Skip a formal plan for a small, self-contained change whose implementation and verification are obvious.

## Verify with Current Evidence

Match checks to changed artifacts:

- Code: static analysis, focused tests, then risk-appropriate regression.
- Documentation: metadata/frontmatter validation, links, and diff inspection.
- Configuration or assets: persisted-text inspection plus the real load path.
- Architecture: dependency direction and module-boundary checks.
- Release work: evidence from the exact release candidate.

Probe uncertain engine, language, file-format, or tool behavior before relying on it. Report measurements in the same turn they were taken, or identify the exact revision that produced them.

Report exact commands or actions, discovered and executed counts, pass/fail counts, skipped artifacts, and relevant warnings. Do not claim runtime, visual, performance, or device success without that evidence.

## Synchronize Reusable Knowledge

Record a fact where the next reader reaches it directly, so that neither of you rediscovers it or opens unrelated files to find it.

Capture only evidence-based facts that would otherwise need rediscovery:

- Put a local invariant or non-obvious reason in a code comment.
- Put a cross-component contract or workflow in its canonical project document.
- Put a recurring agent-process or verification trap in the project's agent instructions when no clearer owner exists.
- Link to the canonical owner instead of duplicating its content.

Do not record obvious behavior, speculation, temporary debugging observations, or stale intermediate conclusions.

## Commit

Commit after you complete the request(bug-fixing/implementation/migration) and its required verification passes.

Agent-performed verification is sufficient evidence for committing. Manual or developer verification, visual review, Play Mode confirmation, physical-device checks, usability review, and release approval may remain outstanding; report them as post-commit verification or approval rather than withholding the commit solely for their absence.

1. Inspect the worktree and the diff.
2. Stage only files belonging to the completed change. Leave unrelated edits unstaged.
3. Run a staged diff check when available.
4. Commit using a focused Conventional Commit message. Apply Commit Scope, Commit Message, you don't need description for commit.
5. Verify the resulting commit and the remaining worktree state.

Do not omit the commit merely because the worktree is dirty; make a scoped commit. Do not commit when the user or the project explicitly forbids it, when agent-required verification failed, when the change is incomplete, or when an explicit approval gate requires stopping before commit. A requirement for later developer or manual verification is not such a gate.

### Commit Scope

One commit carries one reason to change. The file count is a consequence of that rule, not a limit to respect.

Write the subject line before you stage. A subject that needs "and", or that joins unrelated items with a comma, proves that the work is two commits.

- Good: `refactor: rename PlayerController to Player`. Twenty files is correct here, because one rename produced all twenty.
- Bad: `fix: fix jump bug and update UI and format code`. Three files for three reasons. Make three commits.

Keep in one commit the files that are only correct together: a fix and its regression test, a model and its migration, a rename and every call site, a manifest and its lock file.

Split a mechanical change from a behavioral one. A rename, a move, or a formatting pass goes in its own commit, because a logic change hidden inside a large mechanical diff escapes review. Split a refactor from the feature that follows it: first the refactor with behavior unchanged, then the new behavior on the clean base.

Do not add an unrelated fix, a formatting change, generated build output, or commented-out code to a commit that has another purpose.

### Commit Message

Write the header as `<type>(<scope>): <subject>`.

Use one of these types. The Conventional Commits specification defines only `feat` and `fix`; the rest come from the Angular convention that the specification cites, and that `@commitlint/config-conventional` enforces.

| Type | Use it when the commit |
|---|---|
| `feat` | Adds a capability that a user or a calling module can observe. |
| `fix` | Corrects wrong behavior. |
| `refactor` | Changes structure and keeps behavior. Covers a rename, a move, and an extraction. |
| `perf` | Improves speed or memory and keeps behavior. |
| `test` | Adds or corrects tests only, with no production source change. |
| `docs` | Changes documentation or comments only. |
| `build` | Changes the build system, the packaging, or a dependency. Examples: `.csproj`, Unity `manifest.json`, `package.json`. |
| `ci` | Changes continuous integration configuration or its scripts. |
| `chore` | Changes repository maintenance files that ship nothing. Examples: `.gitignore`, an editor or linter configuration. |
| `revert` | Reverts an earlier commit. Write `This reverts commit <sha>.` in the description. |

There is no rule about 
Write the scope as the affected component, taken from the project vocabulary, such as an assembly, a module, or a system name. Omit the scope when the change has no single owner.

Write the subject in the imperative mood, and name the resulting behavior instead of the activity: `fix(input): keep jump buffered across a frame drop`, not `fixed some input stuff`.


<!-- ## Final response format

When the task is complete, respond to the user using these sections:

- **Task type:** Explanation / Design / Implementation / Migration / Bug fixing
- **Summary:** completed behavior and important design decisions.
- **Verification:** exact evidence and remaining manual ownership.
- **Deferred work:** only work genuinely blocked by an unmade decision or an unavailable dependency.
- **Questions:** place last, and include only risky decisions that must be answered before continuing.

Do not defer authorized work merely because the user has not repeated "go." When the request already supplies the decision and the scope, complete that work in the same turn.

A blocking question is only for a decision that would be expensive to reverse, such as a large refactor, a data migration, or discarded work. Include a recommended option, and state what it costs or protects. Do not continue past an unanswered blocking question.

State inherited failures and unrelated dirty files explicitly, without presenting them as failures caused by the change.

### Example

```text
## Task type:

## Summary

## Verification

## Deferred work

## Questions -->