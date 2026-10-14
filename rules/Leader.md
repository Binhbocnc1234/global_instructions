# Leader

Summary: How does an agent complete a developer request? Request coordination, specialist routing, the Design approval checkpoint, handoffs, and completion.
Why: one agent performs the active specialist responsibility. Leader controls the sequence, not each responsibility's internal methods.

Use the shared foundation in [AGENTS.md](../AGENTS.md).

## Responsibility

Coordinate the requested outcome from intake through completion. The developer does not need to name a task type or select specialists.

## Inputs Required

The request, project instructions, current artifacts, and existing approvals.

## Workflow

1. Identify the requested outcome and existing approvals. Read the project documentation index under [documentation routing](Execution.md#route-through-the-documentation-index).
2. Select the needed responsibilities under [Role Routing](#role-routing).
3. For a change that needs a design, request Design's proposal. Resolve blocking questions before asking for approval.
4. Present the design and its acceptance criteria. STOP for developer approval before construction. Existing explicit approval of that design satisfies this checkpoint.
5. After approval, dispatch the required construction work. Use Implementation, Authoring, or RuleMaintenance according to the artifact.
6. Request Testing for executable behavior. Use the artifact specialist's completion checks for documents and rules.
7. Route failed checks to the responsible specialist. Repeat the affected checks after correction. Do not request routine approval for these transitions.
8. Assess [Reusable Knowledge](RuleMaintenance.md#reusable-knowledge). Apply [Commit](#commit) when required. Report the result under [Final Response Format](#final-response-format).

Design approval is the only routine human checkpoint. A request that only asks for explanation or review does not enter the construction workflow.

For example, “Create a boss for game ABC” routes to Design for project concepts, behavior, integration, and acceptance criteria. After approval, Leader coordinates construction and verification.

For example, “Add an export command” follows the same approval flow. By contrast, “Explain the export command” routes to Explanation without construction.

## Scope and Exceptional Stops

Required supporting work belongs to the requested outcome, even when the developer did not list every step. It does not authorize unrelated changes.

Report discovered risks under [Report a Risk Only With Its Failure](Communication.md#report-a-risk-only-with-its-failure). Do not suppress a finding because the developer did not request a risk review.

After Design approval, continue automatically within the approved scope. Return to Design when new evidence requires changing the approved requirements or acceptance criteria. Obtain approval for that change.

The following exceptional stops remain in force:

- [Blockers and failed mechanisms](Execution.md#blocker-detection-and-stop-policy).
- [Credentials and security boundaries](../AGENTS.md).
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
| Select and execute verification | [Testing](Testing.md) | Results and evidence limits |
| Create or maintain non-rule documents | [Authoring](Authoring.md) | Documents and reference checks |
| Maintain agent instructions | [RuleMaintenance](RuleMaintenance.md) | Rules, ownership, and routing checks |

Explanation governs the presentation of every developer-facing response and file, including completion reports. Apply its rules within the active artifact responsibility, not as a separate final stage. Agent-facing text uses Communication.

Why: presentation depends on the reader, while construction and verification depend on the artifact.

Review is a non-mutating mode of the artifact specialist. Use Implementation for code, Testing for tests, Authoring for documents, RuleMaintenance for instructions, and Design for proposals. Report supported findings or state that none qualifies. Do not modify an artifact unless authorized.

A responsibility uses the preceding work's outputs and contracts. Its internal rules apply only to that responsibility. Testing behavior does not activate construction rules such as folder-child limits.

These are responsibilities within one session, not separate agents. Keep one active responsibility at a time. A role change does not require a handoff report.

Use the single-session workflow until the developer approves subagent escalation after an observed failure.
Why: the available evidence does not establish a benefit for the developer's workload.

For an actual transfer to another session or a continuation without the previous context, use the [handoff contract](#handoff-contract). Do not create a session merely to change roles.

A missing responsibility does not justify creating a generic specialist with no independent guidance. Route proposed role changes to RuleMaintenance.

## Completion Evidence

The approved outcome, specialist results, verification limits, and commit result when required.

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

## Request Budget

The harness owns request-cost accounting, reminders, and the work cutoff. The agent MUST NOT estimate or track elapsed time to enforce the request budget. After the harness announces the cost cutoff, the agent MUST write only the final response and MUST NOT request further tools. Continuing work requires a new developer message.
Why: the harness uses the approved cost allowance to require human review before further autonomous work, without depending on the agent's own estimates.

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
