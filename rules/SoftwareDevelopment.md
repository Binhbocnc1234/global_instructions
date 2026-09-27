# Software Development

Summary: the workflow that turns a software request into a verified, documented, intentionally committed change. Use repository evidence to move from requirements to a verified, documented, and intentionally committed change. Project instructions are the authority for technology-specific commands and for explicit exceptions to anything below.

Why: skipping the evidence and verification steps costs nothing now and everything after the change ships, so the workflow is loaded in every session instead of waiting to be recalled.

## Understand the Request

Classify the task as explanation, design, implementation, migration(for example: convert Unity game project to Godot project), or bug fixing. One request may carry several tasks; classify each.

Stop when a missing requirement, dependency, artifact, or risky decision would force an important guess. State the blocker and its evidence.

There are usually 4 types of tasks: Design, Implement(Create), Explain, Bug-fixing. Design is about how a requirement(inside request) should work and be structured before fully implementing it. Implement, on the other hand, is about converting Design to playable game

When the task is about Design or Explain, you don't need to follow instruction from section 2(Planning) onwards and do not mutate the project

## Identify unknown concepts

Words written in capital letters are very likely project concepts. You should search related information about it instead of guessing

Example 1: `Implement an Card, summon an Entity named Exploder. It has the same stats as BasicAlien and the ability to explode upon death, dealing damage in a radius of 1.5 Cells.` You need to understand: What is an Entity? What is BasicAlien? What is a Cell? What is Card? The request already describe Design about Exploder. The request doesn't mention the damage dealt upon explosion and the cost, but you can ignore that and set a number you think is appropriate, as this number can be easily adjusted.

Example 2: `Implement an Entity named Exploder`. Stop immediately because you cannot find any design documentation related to `Exploder`

Example 1: `Design UI for Collection scene` Collection is capitalized, so you need to find out what Collection does in my project. If my project doesn't have documentation about that, you must stop. When developer says `design`, you shouldn't make changes for project

## Load Task-Specific Guidance

| Before you | Apply |
|---|---|
| Write or refactor production code | @software-development/ConstructionGuidance.md |
| Select, write, or execute tests | @software-development/TestingStrategy.md |
| Diagnose or fix a bug | @software-development/Debugging.md |
| Commit to a non-functional target, or judge whether evidence proves a quality claim | the `software-quality` skill |

The rows above import the first three files, so they are already in context. Apply the matching one before acting, not after: a refinement read afterwards only tells you what to redo. The `software-quality` skill loads on demand, because most requests name no non-functional target.

## Reusable Knowledge

Record a fact where the next reader reaches it directly, so that neither of you rediscovers it or opens unrelated files to find it.

Capture only evidence-based facts that would otherwise need rediscovery:

- Put a local invariant or non-obvious reason in a code comment.
- Put a cross-component contract or workflow in its canonical project document.
- Put a recurring agent-process or verification trap in the project's agent instructions when no clearer owner exists.
- Link to the canonical owner instead of duplicating its content.

Do not record obvious behavior, speculation, temporary debugging observations, or stale intermediate conclusions.

### Examples

For example, a test passes alone and fails in a suite because GUT reuses the scene tree between tests, so a node the test creates must be freed in `after_each`. Write the reason on the `free()` call: `# GUT reuses the scene tree between tests, so a node left alive leaks into the next test.` Without it, the next reader deletes a call that looks redundant. This is a local invariant, so a code comment owns it.

For example, you find that a `Resource` loaded from disk is shared by every scene that loads it, so an `Entity` must duplicate its behaviour resource before mutating it. Two systems depend on this and neither owns it, so it is a cross-component contract: it belongs in the project document that owns entity configuration, and the code links to that document.

For example, a `--headless` run rotates `godot.log` and destroys the log the developer was reading. No source file owns the log, and the next agent hits the same trap on the next headless run, so the project `AGENTS.md` owns it.

For example, a new debugging document needs the log path that `AGENTS.md` already records. Link to that section. A second copy of the path is a second thing to update when the snap revision changes, and the copy is the one that will be missed.

Do not record these:

- `# returns the player's health` above `func get_health() -> int`. The code already says it.
- `The bug is probably in the input buffer`, written after the cause turned out to be the state machine. A stale intermediate conclusion sends the next reader down the path you already rejected.
- `This will break when we add multiplayer`, when no multiplayer is planned. That is speculation, under [Reviewing Developer Changes](WorkStyle.md#reviewing-developer-changes).
- `Printed the index here to check the loop bounds`. A temporary debugging observation dies with the session.

## Commit

Commit after you complete the request(bug-fixing/implementation/migration) and its required verification passes.

Agent-performed verification is sufficient evidence for committing. Manual or developer verification, visual review, Play Mode confirmation, physical-device checks, usability review, and release approval may remain outstanding; report them as post-commit verification or approval rather than withholding the commit solely for their absence.

1. Inspect the worktree and the diff.
2. Stage only files belonging to the completed change. Leave unrelated edits unstaged. The developer may have staged files of their own, and a plain `git commit` records everything in the index. Commit with `git commit -- <paths>`, or first confirm that `git diff --cached --stat` lists only your files.
3. Run a staged diff check when available.
4. Commit using a focused Conventional Commit message. Apply Commit Scope and Commit Message. The message is a header line only, with no description body.
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

Write the scope as the affected component, taken from the project vocabulary, such as an assembly, a module, or a system name. Omit the scope when the change has no single owner.

Write the subject in the imperative mood, and name the resulting behavior instead of the activity: `fix(input): keep jump buffered across a frame drop`, not `fixed some input stuff`.

MUST NOT write a description body. The commit is the header line and nothing else. Reasoning, evidence, trade-offs, and consequences belong in the response to the developer, who is reading them right now, not in a commit message nobody opens again. A change that feels too large to fit in one header line is two commits, not one commit with an essay attached; apply Commit Scope instead of writing a body.

The single exception is `revert`, whose body carries `This reverts commit <sha>.` and nothing more.