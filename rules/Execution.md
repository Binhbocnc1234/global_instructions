# Execution

Summary: How must an agent execute work? Shared retrieval, tool-use, workspace, and stop constraints.
Why: these constraints apply across specialist responsibilities.

Use the shared foundation in [AGENTS.md](../AGENTS.md).

## Reuse File Content Already in Context

When to apply: before a tool call that would read file content already available in the active context.

- MUST reuse the available content when you expect the file to be unchanged.
- MUST NOT repeat the read merely for reassurance or to refresh your memory.
- MAY read again when an edit, a generating command, or a developer message gives a reason to expect changed content.
- MAY read content that the earlier result omitted or that is no longer available in the active context.

Why: repeated reads of unchanged content consume tool calls and context without adding evidence.

## Scratch Files Go in `tmp/`

When to apply: the agent writes a file that serves only the current task, such as a probe, a driver scene, a one-off check or conversion script, a log, or an intermediate output.

- Put it in `tmp/<topic>/` at the project root. Git MUST ignore `tmp/`. When the project does not ignore it yet, add `/tmp/` to `.gitignore` in the same change.
- MUST NOT put it in a harness scratchpad, even when the harness names one. Use a scratchpad only when the task has no project root.
- MUST NOT write it at the project root, or inside a folder that holds source, assets, data, tests or documentation. No file outside `tmp/` references a file inside it.
- A check worth running again is not scratch. Move it into the project's tools or tests, where it gets a name and an owner.

For example, a Godot script that loads every model scene and prints duplicate node names needs `res://` paths, so it goes in `tmp/model-probes/AllModelsCheck.gd`, not in `probe_all_models_tmp.gd` at the project root.

Why: a scratch file at the root appears in the editor and in `git status` next to the developer's own untracked work, so the developer cannot tell whether it is safe to delete, and git cannot restore it after deletion. Inside an ignored `tmp/`, the folder name says the file is disposable and git never offers it for a commit. A harness scratchpad is a feature of one harness: another harness or model has none, and the path is per session, outside the project, so the developer and the next session cannot find the file. `tmp/` is the same path for every harness and every model.

## Route Through the Documentation Index

When to apply: at the start of every task in a project that carries documentation.

1. Read the project's documentation index in full. The project `AGENTS.md` records its path.
2. Open only the indexed documents whose description matches the request.
3. Follow an inline link out of those documents only when the link affects the task.

MUST NOT list a documentation folder, grep it for a keyword, or open a document to learn what it holds. Each of those searches for a document that the index already names, and each one costs context that the task needs. [Documentation Index](Authoring.md#documentation-index) owns generating and updating the index.

Why: the index costs one read and names every document. Discovering the same set by opening files costs one read per candidate, and the candidates that turn out to be irrelevant stay in context for the rest of the session.

## An Unrelated File Opened Is a Routing Defect

When to apply: you read a file, and it held nothing the task needed.

Two causes produce that read: the agent chose badly, or the project routes badly. Treat the second as the cause, because it is the one that can be fixed. A routing defect is one of:

- The project has no documentation index, so the only way to learn what a document holds was to open it.
- The index entry's description does not describe the document, or it is stale.
- The document mixes kinds, so one sentence cannot describe it. See [Markdown Document Kind](Authoring.md#markdown-document-kind).
- `AGENTS.md` or a document links to a file that was renamed, moved, split, or deleted.

Report it in the same response as the work: name the file you opened, what you expected it to hold, and which defect above sent you there. Then propose the fix, and record it under [Reusable Knowledge](RuleMaintenance.md#reusable-knowledge).

For example, a task about card cost ends with the agent reading `Documentation/en/rules/technical/EntityStats.md`, which holds no cost rule. The index describes it as "Entity reference", a description that fits four documents. The fix is one sentence in that document's `description` frontmatter field naming what it holds, followed by regenerating the index.

For example, a task about the build pipeline ends with the agent opening six files under `tools/` because no document names which one runs first. Nothing is stale; the routing simply does not exist. The fix is an entry in `AGENTS.md` naming the entry point.

## Reviewing Developer Changes

Developers often edit files without explicitly telling you in request, so if you see unusual changes (e.g. removing a feature, removing a seemingly unnecessary null check) in the git diff, it's because of the developer.

A change the developer made is deliberate. Read it to understand the current state. Do not undo it, reformat it, report on it, or fold it into a change of your own — unless the task specifically asks you to do one of these.

A risk you see in a change is reported under [Report a Risk Only With Its Failure](Communication.md#report-a-risk-only-with-its-failure).

## Handle long-running task

A command has no total time limit. Its limit is silence: when it goes 2 minutes without a meaningful response or signal, stop it and find the cause before running it again.

A meaningful signal is output that shows progress or a state change: a build step, a test result, a line the program logs. A loop that repeats the same check, or prints only "waiting", gives none. So a wait loop prints each new state it reads, and its end condition is tested once against the current state before the loop starts.

For example, a script waits for a chat turn to end by polling for a "Cancel" button. The button is also present when no turn runs, so the loop never ends early and polls silently until its limit. Testing the condition once on the idle chat shows the defect in seconds.

Why: a total limit stops a long build that is still working, and lets a stuck loop run until the limit ends it. Silence tells the two apart.

### Confirm the kill landed

`kill <pid>` on the pid a shell reports often hits a wrapper shell, not the program. The program keeps running, keeps holding its lock, its API quota or its port, and the next attempt fails for a reason that looks unrelated.

After any kill, confirm by name — `pgrep -a <name>` — not by checking that the pid is gone. A process in `D` state ignores `SIGTERM`; escalate to `kill -9`.

`pkill -f <pattern>` and `pgrep -f <pattern>` also match the shell that runs them, because the pattern appears in that shell's own command line. `pkill -f` then kills the agent's own tool shell (exit 144), and `pgrep -f` counts itself as a process still alive. Write the pattern so it cannot match itself: `pkill -f '[b]rave-probe'` matches `brave-probe` but not the text `[b]rave-probe`.

## Blocker Detection and Stop Policy

When working on a task the developer requested, you must continuously check whether the current project state matches the assumptions/prerequisites required to complete the task.

A **blocker** is an issue that prevents the requested task from being completed correctly and cannot be repaired within the authorized scope using available access. Examples include, but are not limited to:

* A required file, referenced class, function, module, asset, dependency, or configuration file is missing and cannot be restored or installed within the authorized scope.
* The documentation contradicts the actual project structure.
* Continuing would require guessing important project details.
* The task cannot be completed without developer clarification or project correction.
* Some skills have input schema/Invocation Contracts. If the request violates that schema, it needs to be stopped, the error pointed out, and the developer asked to correct it.
* The developer's request contradicts the project's canonical documentation (such as skills, project-level documentation, or project-level skills), as developers are human and might not remember everything.
* A task in the developer's request depends on task A, and task A is not finished yet. For example, the request says "Create test for assembly MvA.Bullet". But that assembly is not exist/not have enough resource for testing, then you should say this is blocker

Missing tools or dependencies and failures with an evidenced, repairable cause are prerequisite work. MUST repair them recursively within the authorized scope, verify the repair, then return to the original task. For example, install a missing Python runtime needed by the task, or install missing OpenSSL development files required by an approved build. MUST NOT substitute a workaround that leaves the failed mechanism broken. A repair that requires unavailable credentials, additional approval, an unmade product decision, or access the agent lacks remains a blocker.

Why: handing repairable prerequisite work to the developer interrupts the task and transfers work the agent can perform itself.

If you detect a blocker after assessing whether its cause can be repaired, you must **stop immediately**. Do not continue implementing, modifying, refactoring, or generating code based on assumptions.

Instead, report the blocker to the developer clearly using this format:

1. **Blocker found**

   * Briefly describe what prevents the task from being completed.

2. **Evidence**

   * Show the specific file, documentation line, reference, command result, or project fact that proves the blocker exists.

3. **Why this blocks the task**

   * Explain why continuing would be unsafe, incorrect, or likely to produce broken work.

4. **Recommended next action**

   * Suggest what the developer should fix, provide, rename, restore, or clarify before the task can continue.

Do not silently work around blockers unless the developer explicitly allows you to make assumptions.

For example:

The file `Architecture.md` references `AISystem.cs`, but no file named `AISystem.cs` exists in the project. Because the requested task depends on modifying or understanding that system, continuing would require guessing the intended file or architecture. Please confirm whether `AISystem.cs` was renamed, deleted, or not yet created.

For example: Harness tool is not working for some unknown reason. You should stop the task and tell developer about that bug

For example: the task's own file marks a contract that the change depends on as pending, such as a shared policy that differs between the current branch and a branch about to be merged. Changing code before that contract is settled builds on a guess, and the merge can make every such change redundant. Stop and ask which contract applies.

### No Fallback

When to apply: a harness tool, script, or mechanism the task relies on fails

Action: MUST repair the cause and retry the original mechanism when the repair is within the authorized scope and available access. MUST NOT bypass the failed mechanism. When the cause cannot be repaired, apply Blocker Detection and Stop Policy.

For example, the Read tool fails, and the agent writes the file with a Python one-liner instead. The task looks done, the defect stays, and every later session pays for it again. This is the execution half of the coding rule [No Fallbacks](Implementation.md#required-dependency-policy-no-fallbacks).

A route the harness allows in general is still a workaround when the agent takes it because a dedicated tool failed. For example, Claude Code in auto mode allows reading and editing files through the shell instead of Read, Edit, and Write. That permission covers a choice made before the first call. It does not cover switching after the Read tool returned an error.

1. Record the failure: the tool, its input, and the full error text.
2. Repair the evidenced cause within the authorized scope, then retry and verify the original mechanism before resuming dependent work.
3. When the repair requires separate work that the developer has authorized delegating, hand it to a separate session with the record from step 1.
4. When the repair cannot proceed with available access or authority, report it with the format in [Blocker Detection and Stop Policy](#blocker-detection-and-stop-policy). Continue only work that does not need the broken mechanism.

Why: a workaround hides the failure from the only reader who can fix it. The developer sees a finished task and never learns that a tool is broken, so the next task hits the same failure.

## The Agent Does What It Does Better

When to apply: a step of the task could be done by the agent or handed to the developer, such as a setup, a check, a test, a lookup, or a repeated action.

Compare the step with the strengths and weaknesses in [About developer](../AGENTS.md#about-developer) and [About agent](../AGENTS.md#about-agent). When the agent does the step better, the agent does it, and MUST NOT hand the developer instructions for it. Hand over only the part that needs a developer strength: sight or taste, a product decision, a credential or an approval, or a physical device. When the agent cannot do the step yet but a tool would let it (a driver script, a debugging protocol, an editor API), build or find the tool under [Automate Repeated Work](Implementation.md#automate-repeated-work).

These rules apply this one to particular steps: [Agent Tests Logic, Developer Judges Visuals](Testing.md#agent-tests-logic-developer-judges-visuals), [Query the GUI Before Asking the Developer to Look](Testing.md#query-the-gui-before-asking-the-developer-to-look), and [Capture Visual Evidence for the Developer](Testing.md#capture-visual-evidence-for-the-developer).

For example, a chat extension must be checked: "Claude answers, and the Read tool runs". Bad: "Open VSCodium, open the chat panel, and type a prompt." Good: the agent launches the editor with a debugging port, types the prompt and reads the answer through the DevTools Protocol, then asks the developer only whether the panel looks right.

For example, a new game unit must be playtested. Bad: a markdown guide that tells the developer to drag a card to a cell, spawn five enemies, and apply an effect before each check. Good: a driver scene that stages each state in one frame, so the developer only watches and presses one key for the next state.

For example (the developer's part). Whether an attack animation feels heavy enough needs taste, so the agent hands that judgement to the developer, together with a capture of the animation.

Why: the agent executes setups and checks in seconds, while the developer clicks through them one by one. By contrast, the developer sees the screen and judges feel, which the agent cannot. Giving each step to the stronger side makes the whole task faster and frees the developer for the part only they can do.

## Ask Before Taking the Developer's Machine

When to apply: before an action that shows a window on the developer's screen, takes keyboard or mouse focus, or holds the laptop busy for more than 30 seconds (a headful browser or editor, GUI automation, a build over 3 minutes).

Say what appears or happens, for how long, and whether typing is safe during it. Wait for a yes. Prefer a headless or off-screen route first, and use the visible one only when the headless route cannot prove the behavior; name that reason when asking.

Why: The developer and the agent can operate concurrently. However, if the developer accidentally clicks or types into the active window you have open, it could cause errors.
