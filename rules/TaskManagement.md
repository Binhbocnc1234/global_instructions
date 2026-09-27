# Task Management Rules

Summary: How does work survive past this request? The `delivery/` folder, the request budget, and the task file format.
Why: a closed laptop must not lose the state of work that takes more than one request. Developer cannot remember remaining tasks reliably

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
