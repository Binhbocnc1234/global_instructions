# Implementation

Use the shared foundation in [AGENTS.md](../AGENTS.md).

## Construction constraints

- Keep each domain invariant owned by the object whose state it constrains. Do not duplicate or query that invariant from a behavior that merely requests a state change. For example, `Knockback` must not check whether a displaced `Entity` position is valid when `Entity` owns team/grid boundaries; it should request displacement through an operation such as `entity.apply_knockback(delta)`, and `Entity` must enforce the invariant by clamping position. Treat the opposite design as misplaced responsibility or domain-invariant leakage: it violates encapsulation and the Tell, Don't Ask principle.
- Use explicit types where the language and project policy require them. Do not hide uncertainty behind dynamic escape types. For example, do not use `var` keyword in C#.
- Fix broken construction or wiring instead of adding silent fallbacks, no-ops, or legacy behavior.
- Do not extract a method merely to label a few statements when keeping them inline makes lifecycle or ordering clearer.
- Make a value's unit or representation explicit in its identifier when omission could cause misuse. Follow the project's naming convention with names such as `duration_seconds`, `DurationSeconds`, or `limit_fraction`.

## Editor Tool UI Names

When to apply: making UI, such as game UI, a Godot editor plugin or a Unity editor window.

- Every element the developer can point at shows its name in a tooltip on hover. Drawn items count too, such as a key mark or a playhead.
- The name comes from the tool's UI reference document. That document is canonical. Add a missing element to it in the same change.
- Set the tooltip delay to 1 second if possible
- This rule still apply to game UI but with nuance: Godot editor already have native tooltip in PlayMode, the tooltip shows Node's name when developer click at any Node

Why: Sometime developer want to report bug of an UI element or button, but they cannot remember the names of the UIs, and furthermore, the UIs were largely written by agents.

## Guard Placement

A guard belongs where the invariant is established, not where it is consumed. Scattering defensive checks across consumers is a programming error, not caution: it hides who actually owns the rule, and it makes an invariant that already holds look uncertain to the next reader.

Before writing any defensive check, name who guarantees the condition:

1. **The producer already guarantees it** — do not re-check. The check is dead code. Instead, state the guarantee at the source (doc comment on the property, method, or event) so consumers can rely on it.
2. **Nothing guarantees it** — fix the producer so it does. Do not compensate in every consumer.
3. **The value crosses a trust boundary** (user input, network payload, file contents, another process) — validate once at the boundary, then treat it as trusted inside.

The clearest smell is an event handler that re-reads the state the event just announced:

```csharp
// WRONG - the notification already means this is true
private void OnGameOver()
{
    if (!BoardUtils.IsGameOver()) return;   // dead code
    Idle();
    enabled = false;
}
```

## Method Extraction

Do not extract a method that is called once merely to label one to five statements. Keep those statements at the call site when seeing them inline makes the lifecycle, dependency, or execution order clearer.

## Required Dependency Policy: No Fallbacks

Treat serialized scene references, required components, initialized gameplay behaviours, and mandated effects as runtime invariants. Access them directly.

- Do not add `null` checks or early returns that silently skip required runtime dependencies.
- Do not mask a missing dependency with a fallback object, default value, warning, legacy behavior, or no-op.
- Let software report its normal runtime error when an invariant is broken so the debugger identifies the offending object and stack trace.
- Fix the scene, serialized data, initialization order, or caller contract that violated the invariant. Do not make the consumer tolerate the defect.
- Do not write required-dependency handling like this:
```gdscript
if dependency != null:
    use_dependency()
else:
    use_legacy_behavior()
```
- Right solution:
```gdscript
use_dependency()
```
That's it. You don't need to check for that error

## Comment rules

- Comment non-obvious reasons, invariants, units, ordering, external constraints, and deliberate trade-offs. Do not restate the code.

## 250 lines rule

Keep source-code and documentation files at or below 250 lines whenever practical.

The 250-line limit is a signal to split responsibilities, not a target to satisfy through compression.
Like the [16 child rule](#16-child-rule), it supports maintenance through meaningful groups. It does not limit the expanded prompt or token count.

When a file is likely to exceed 250 lines:

1. Do not reduce readability by removing comments, collapsing formatting, shortening meaningful names, combining unrelated logic, or writing denser code.
2. Do not omit necessary information merely to stay below the limit.
3. Identify distinct responsibilities, concepts, sections, or components within the file.
4. Extract those responsibilities into separate, clearly named files.
5. Keep each resulting file cohesive and understandable on its own.
6. Update imports, references, navigation, indexes, or documentation links as needed.

A file may exceed 250 lines only when splitting it would create artificial fragmentation, excessive indirection, or reduce maintainability. In that case, explain why the exception is justified before proceeding.

## Automate Repeated Work

This is DRY applied to execution. [DRY](../AGENTS.md#drydont-repeat-yourself) covers the other half: one canonical owner for a fact.

When the same operation runs 3 or more times, build the mechanism that performs it, then run the mechanism. Doing the operation by hand repeats the lookups and the judgement calls with it, and each repetition can go wrong on its own.

For example, the developer asks the agent to migrate every `.prefab` file in a Unity project to `.tscn` in a Godot project. The agent converts all 12 prefabs by hand instead of writing a Python script that converts them. This violates DRY: the agent now looks up Unity YAML syntax once per prefab, and a rule it applies correctly to prefab 3 can be forgotten at prefab 9. The script states the mapping once and applies it 12 times identically.

For example, a change must be checked against 40 scenes. Write one headless script that opens each scene and reports the failures. Opening 40 scenes by hand repeats the same judgement 40 times and produces no record of what was checked.

For example, the same three shell commands run before every commit. They belong in one hook or one script, named once, not retyped per commit.

MAY skip the mechanism when writing it costs more than the work that remains: the operation runs twice, or each case needs a different decision that no rule covers. Say which of the two applies before doing the work by hand.

You will see that many rules above this is a narrow branch of DRY:
- [CorrectionIsATrigger](RuleMaintenance.md#a-correction-is-a-trigger), write a rules so that future mistake won't appear again
- [UnrelatedFileOpened](Execution.md#an-unrelated-file-opened-is-a-routing-defect), better project-scoped AGENTS.md, lower error chance

Why: repeated work hides its own cost. Each manual pass looks small, so the total is never compared against the one-time cost of the mechanism, and the mechanism is also the only artifact that survives the task.

## 16 child rule

When to apply: creating, moving, or splitting a file or folder in a project folder that the developer or an agent browses, such as source, tools, assets, data, or documentation.

A folder holds at most 16 direct children. Only folders the developer or an agent creates count: generated output, git-ignored files, and third-party folders such as `node_modules` or a vendored library do not.

[folder_child_limit.py](../scripts/folder_child_limit.py) checks the rule on a git repository and owns what counts as a child. A project lists its committed third-party folders in that script's settings file, and blocks a new violation by running the script with `--staged` from its pre-commit hook.

Every folder has a meaning: the one thing that all of its children share, such as the feature they implement, the system they belong to, or the owner that edits them. The folder name states that meaning. A reader who knows what they are looking for picks the folder from its name without opening any file inside it.

When a folder would pass 16, look for the groups that already exist among its children and give each group its own subfolder. MUST NOT split only to pass the limit. Numbered parts (`Part1`, `Part2`), alphabetical ranges (`A-M`), and catch-all names (`Misc`, `Common`, `Other`) name no shared meaning, so they are forbidden. When the children share no meaning beyond the parent's, the folder is the exception: report it to the developer with the reason instead of splitting it.

For example, a `UI/` folder holds 25 scripts: 9 for the battle screen, 8 for the shop, and 8 widgets that both screens use. Split it into `Battle/`, `Shop/`, and `Widgets/`. By contrast, `UI1/` and `UI2/` pass the count and tell the reader nothing about which one holds the shop.

Why: the developer and the agent have no reliable memory of where a file lives, so the folder tree is how both find a file without reading many files. A folder with more than 16 children sends the reader back to scanning names one by one, and a folder without a shared meaning sends the reader into every subfolder.
