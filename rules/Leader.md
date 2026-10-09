# Leader

Summary: How does an agent complete a developer request? Request coordination, specialist routing, the Design approval checkpoint, handoffs, task state, and completion.
Why: one agent performs the active specialist responsibility. Leader controls the sequence, not each responsibility's internal methods.

Use the shared foundation in [AGENTS.md](../AGENTS.md).

## Responsibility

Coordinate the requested outcome from intake through completion. The developer does not need to name a task type or select specialists.

## Inputs Required

The request, project instructions, current artifacts, existing approvals, and any task record.

## Workflow

1. Identify the requested outcome and existing approvals. Read the project documentation index under [documentation routing](Execution.md#route-through-the-documentation-index).
2. Select the needed responsibilities under [Role Routing](#role-routing). For a defect, request Debugging evidence before designing its correction.
3. For a change that needs a design, request Design's proposal. Resolve blocking questions before asking for approval.
4. Present the design and its acceptance criteria. STOP for developer approval before construction. Existing explicit approval of that design satisfies this checkpoint.
5. After approval, dispatch the required construction work. Use Implementation, Authoring, or RuleMaintenance according to the artifact.
6. Request Testing for executable behavior. Use the artifact specialist's completion checks for documents and rules.
7. Route failed checks to the responsible specialist. Repeat the affected checks after correction. Do not request routine approval for these transitions.
8. Assess [Reusable Knowledge](RuleMaintenance.md#reusable-knowledge). Update the task record. Apply [Commit](#commit) when required. Report the result under [Final Response Format](#final-response-format).

Design approval is the only routine human checkpoint. A request that only asks for explanation or review does not enter the construction workflow.

For example, “Create a boss for game ABC” routes to Design for project concepts, behavior, integration, and acceptance criteria. After approval, Leader coordinates construction and verification.

For example, “Add an export command” follows the same approval flow. By contrast, “Explain the export command” routes to Explanation without construction.

## Scope and Exceptional Stops

Required supporting work belongs to the requested outcome, even when the developer did not list every step. It does not authorize unrelated changes.

Report discovered risks under [Report a Risk Only With Its Failure](Communication.md#report-a-risk-only-with-its-failure). Do not suppress a finding because the developer did not request a risk review.

After Design approval, continue automatically within the approved scope. Return to Design when new evidence requires changing the approved requirements or acceptance criteria. Obtain approval for that change.

The following exceptional stops remain in force:

- [Blockers and failed mechanisms](Execution.md#blocker-detection-and-stop-policy).
- [Credentials and security boundaries](../AGENTS.md#security).
- [Taking control of the developer's machine](Execution.md#ask-before-taking-the-developers-machine).
- Other explicit approval requirements in the applicable instructions.

Developer-only visual judgment and release approval remain post-completion checks unless an explicit gate prevents completion. Do not claim that the agent supplied those approvals.

## Role Routing

Classify responsibilities, not the whole request under one fixed task type. All specialist instructions are loaded through the global prompt imports. Apply the instructions for the active responsibility.

| Responsibility | Specialist | Output |
|---|---|---|
| Present developer-facing responses and files, including requested explanations | [Explanation](Explanation.md) | Text selected and worded for the developer |
| Resolve requirements and propose a solution | [Design](Design.md) | A proposal and acceptance criteria |
| Construct or migrate code, assets, folders, or execution tools | [Implementation](Implementation.md) | Artifacts and construction evidence |
| Diagnose a defect | [Debugging](Debugging.md) | Reproduction, cause, and correction to consider |
| Select and execute verification | [Testing](Testing.md) | Results and evidence limits |
| Create or maintain non-rule documents | [Authoring](Authoring.md) | Documents and reference checks |
| Maintain agent instructions | [RuleMaintenance](RuleMaintenance.md) | Rules, ownership, and routing checks |

Explanation governs the presentation of every developer-facing response and file, including completion reports. Apply its rules within the active artifact responsibility, not as a separate final stage. Agent-facing text uses Communication.

Why: presentation depends on the reader, while construction and verification depend on the artifact.

Review is a non-mutating mode of the artifact specialist. Use Implementation for code, Testing for tests, Authoring for documents, RuleMaintenance for instructions, and Design for proposals. Report supported findings or state that none qualifies. Do not modify an artifact unless authorized.

A responsibility uses the preceding work's outputs and contracts. Its internal rules apply only to that responsibility. Testing behavior does not activate construction rules such as folder-child limits.

These are responsibilities within one session, not separate agents. Keep one active responsibility at a time. A role change does not require a handoff report.

Subagent delegation remains deferred under task `SubagentEscalation`. Use the single-session workflow until the developer approves escalation after an observed failure.
Why: the available evidence does not establish a benefit for the developer's workload.

For an actual transfer to another session or a continuation without the previous context, use the [handoff contract](#handoff-contract). Do not create a session merely to change roles.

A missing responsibility does not justify creating a generic specialist with no independent guidance. Route proposed role changes to RuleMaintenance.

## Completion Evidence

The approved outcome, specialist results, verification limits, task state, and commit result when required.

## Responsibility Transitions

Use the active specialist's completion evidence to select the next responsibility. Preserve scope, approvals, results, discovered risks, and blockers in the existing task context. Do not restate them in a separate report for each role change.

## Handoff Contract

Use these fields only when task context transfers to another session or a continuation that cannot access the previous conversation.
A handoff MUST NOT expand the authorized scope. Supply the shared rules and applicable specialist and project instructions when the receiver does not already have them.

```text
Goal:
Authorized scope:
Decisions and constraints:
Artifacts and changes:
Evidence:
Open questions or blockers:
Requested next responsibility:
Remaining request budget:
Required return format:
```

Name the receiving responsibility. Distinguish verified results from assumptions. Preserve pending approvals and evidence limits. Authorized parallel sessions must use independent scopes.

## Task Management

A project MAY contain a `delivery/` folder at its root. It is the canonical source for tasks that last longer than one request.

- `delivery/unfinished/` holds a task in progress: at least one `- [ ]` item.
- `delivery/deferred/` holds a task the developer deferred as a whole. It is not started or it is paused; its items keep their `- [ ]` and `- [x]` state.
- `delivery/finished/` holds a task whose items are all `- [x]`.
- A task is never partly deferred. To defer part of a task, split that part into its own task in `delivery/deferred/`.
- 1 task = 1 Markdown file. The file name is the task ID: PascalCase, unique across all three folders.
- Checkboxes decide between `unfinished/` and `finished/`: move the file in the same change that ticks its last item or reopens one. The developer's decision decides `deferred/`: move the file in the same change that defers or resumes it.
- Refer to a task by its ID, never by its file path, because the file moves between folders.
- A task file MUST NOT own anything that outlives its task. A durable contract, rule, or workflow belongs in project documentation, and the task file links to it.

### Request Budget

One request has a budget of 15 minutes of agent work. The budget lets the developer check the result and correct it before work continues. In Claude Code, the hook [request_budget.py](../scripts/request_budget.py) enforces it.

Create a task file only when you estimate that the work does not fit one request budget. Work that needs the developer between steps (an approval, a playtest, a reboot, a physical device) never fits, because each approval ends a request. The number of items does not decide it: a mechanical change over many files can fit.

Also create a task file when the budget ends a request with work left, so the work survives a closed laptop.

Also create a task file for a future spec: planned work that no code implements yet, whatever its size. Its Why states the trigger that starts the work, and it stays in `delivery/deferred/` until the trigger fires. The spec lives only until the code exists, so it does not break the rule that a task file owns nothing that outlives it.

| Request | Task file | Reason |
|---|---|---|
| "Add this rule to AGENTS.md: kill a command after 2 minutes without output" | No | One edit, checked by reading the diff |
| "Rename 30 documentation files to PascalCase and fix their links" | No | Mechanical, a few minutes |
| "Fix the crash when the player dies during a pause" | No | One bug and one regression test |
| "Is the `cooldown` field redundant?" | No | A question |
| "Migrate this game from Unity to Godot" | Yes | Many systems, and the developer playtests each slice |
| "Install Linux beside Windows and restore my tools" | Yes | Reboots, firmware checks, and long installs |
| "Sync 20 GB of files to cloud storage and verify them" | Yes | Waits hours on an outside process |
| "Build an editor plugin in six steps, each checked by hand" | Yes | The developer approves every step |
| "Fix this bug", and the budget ends before the fix is verified | Yes | The budget ended with work left |

### Task File Format

```markdown
## Why
Plain paragraphs: the reason, the criteria, and the decisions of the task.

## Step 1: Import the prefabs
Plain paragraphs MAY record decisions and evidence.
- [x] #1 Convert the prefab files
- [ ] #2 Run the unit tests
- [ ] #3 Manual testing: open each prefab in the editor

## Step 2: Migrate the scenes
- [x] #1 Convert the scene files
- [ ] #2 Manual testing: play level 1-1
```

- A step is a `##` section titled `Step <n>: <name>` that holds checkboxes. A `##` section without checkboxes holds context.
- MUST NOT use `###` or deeper headings in a task file.
- `Step <n>` is the step ID inside its file. Number new steps after the last one and never renumber, because chat and other files refer to these IDs. Item numbers restart at `#1` in each step. One item is one line.
- An item is `- [ ]` or `- [x]`. There is no deferred item; see `delivery/deferred/`.
- Size a step to fit one request budget, and end it with its testing items.
- Refer to an item as `<TaskName> Step <n>#<m>`, e.g. `GodotPrefabMigration Step 1#3`. Omit the task ID when the conversation already names the task.
- When a task file would exceed 250 lines, split it into sibling task files that share an ID prefix, e.g. `GodotMigrationPrefabs` and `GodotMigrationScenes`. Create every sibling at once, so work not started yet stays visible. No parent file.

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

## Final Response Format

- **Vocabulary**: first, only when Explanation is active and [Teach the Standard Term](Explanation.md#teach-the-standard-term) applies.
- **Task type**: name the responsibilities Leader selected for the request.
- **Answer**: only a requested explanation needs this. For an implementation, do not list the changes: the git diff already shows them.
- **Lesson**: only when the request handled a correction. Name the cause and where it was recorded or proposed, or why nothing was recorded.
- **Remaining work**: only work that an unmade decision or an unavailable dependency actually blocks.
- **Questions**: last, and only when an unmade decision blocks the requested work. State the recommended option, and what it costs or protects. An offer of work the request did not name is noise under [Developer-Facing Relevance](DeveloperWriting.md#developer-facing-relevance). For example, the request asks why the chat shows an image under a command's output, and the cause is a feature of the editor that works as designed. Do not end with "Do you want these images removed?", because the developer did not say the images were unwanted.

Use the shared scope and evidence rules for every response. Explanation governs developer-facing presentation. Apply its technique rules when the developer requests an algorithm or process explanation.

Why: a fixed order lets the developer find the answer, the lesson, and the open questions in the same place in every response. The Task type line also shows the developer how the agent read the request, so a wrong reading is caught before the work is checked.
