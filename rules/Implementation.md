# Implementation

How code should look like?

## Some small rules

- Use explicit types where the language and project policy require them. Do not hide uncertainty behind dynamic escape types. For example, do not use `var` keyword in C#.
- Fix broken construction or wiring instead of adding silent fallbacks, no-ops, or legacy behavior.
- Do not extract a method merely to label a few statements when keeping them inline makes lifecycle or ordering clearer.
- Make a value's unit or representation explicit in its identifier when omission could cause misuse. Follow the project's naming convention with names such as `duration_seconds`, `DurationSeconds`, or `limit_fraction`.

## Research Before Building a system

When to apply: adding or replacing a system whose implementation approach is not established by the project, where existing software could supply required capabilities or resolve an unknown integration mechanism.

MUST inspect project code and current dependencies first. If they do not supply the required implementation or reference, search for existing implementations before choosing how to build the system.

Inspect source code or official documentation. Compare reuse, adaptation and a new implementation against required behavior, architectural fit, integration work, verification work, dependency constraints and license. Reuse MAY mean a library, an application extended through an adapter, or a mechanism learned from source. An existing implementation does not by itself establish that adoption requires less work.

For example, a new chat frontend needs session navigation, streamed responses, tool displays and file review. Inspect existing clients and component libraries before implementing those capabilities. Extending an existing application MAY avoid building several of them.

For example, subscription authentication requires a refresh mechanism that the available API documentation does not establish. Inspect a client supporting the same authentication route before inventing the protocol.

By contrast, changing a label, correcting a calculation in an established code path, or adding a field to an existing form does not trigger this rule.

For a boundary case, a candidate application supplies the desired widget but requires replacing session storage, model transport and build tooling. Compare that integration work with a component library or a local implementation; finding an existing application does not require adopting it.

Why: research can avoid rebuilding existing capabilities and reveal protocol constraints before implementation. Limiting the trigger to system choices and unresolved integrations avoids requiring external research for routine local changes.

## Keep Core Behavior Independent of Presentation and Its Host

When to apply: introducing or changing the boundary between application or gameplay behavior and a UI, engine scene, or host process.

MUST identify the behavior's state owner, required lifetime and required execution contexts before choosing the boundary. Derive these from the request and project contracts. Include established needs such as automated verification, simulation, frontend replacement or survival across a host reload; do not invent future requirements.

Presentation and host adapters MUST depend on core-owned operations and contracts. Core behavior MUST NOT require presentation implementations, UI objects or rendered properties to determine its results. Keep mutable state within its owning scope so separate executions do not share state accidentally.

For a new or changed boundary, verification MUST exercise the production core behavior without the presentation or host dependency that the boundary is intended to exclude. Use existing dependency checks to detect prohibited imports. Separate folders or class names alone do not establish independence.

For example, a game AI evaluates possible attacks. Live combat and simulation use the same damage and movement rules, while each battle owns its mutable state. Running the simulation requires no sprites or animation nodes.

For example, a desktop application must support replacing its GUI. Its session operations accept core-owned inputs and produce results or events; a GUI adapter translates between those contracts and widgets.

By contrast, a hover animation belongs in the widget that displays it. This rule does not require moving appearance-only behavior into a domain service.

For a boundary case, a single-process application can satisfy GUI independence through modules and direct calls. Introduce a separate process only when a requirement such as independent lifetime or shared access justifies the communication and lifecycle work.

For a boundary case, engine-provided math and data types may remain in gameplay code when they do not require presentation or scene services. Possible future multiplayer or saving does not require implementing networking, save formats or a plugin system now.

Why: tying core behavior or state to the first presentation or host makes another execution context require changes to that behavior. Explicit dependencies and scoped state preserve reuse without requiring an architecture for hypothetical features.

## Keep spec owned by the object whose state it.

For example, `Knockback` must not check whether a displaced `Entity` position is valid when `Entity` owns team/grid boundaries; it should request displacement through an operation such as `entity.apply_knockback(delta)`, and `Entity` must enforce the invariant by clamping position. Treat the opposite design as misplaced responsibility or domain-invariant leakage: it violates encapsulation and the Tell, Don't Ask principle.

For example, a game rule said that "Boss always have Sanity effect(an effect that make Boss immune to Debuff)". Bad implementation: in every class that inherits from the Boss class (where Boss is an abstract class), the agent calls `AddEffect(new Sanity())`. Good: this rule should be implemented in Boss class

## DRY in implementation

Developer request: "Create a tutorial for Level 1; the tutorial will consist of multiple steps, and at each step, highlight the buttons the player needs to click using a flickering animation."

Bad approach: Implementing the flickering animation logic repeatedly within each tutorial step.

Good approach: Coding a dedicated function or class for the flickering animation, then having the tutorial steps act as consumers of that logic.

Why: This principle also applies to game UI design; ideally, most buttons should share the same style and logic. Violating the DRY principle not only results in bloated code but also breaches an implicit game design requirement: consistency. No one designs a game where every button uses a different style.

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

## Keep the Trace When Code Handles a Failure

When to apply: writing code that catches an error, converts it to a return value, an exit status or a message, or passes it across a boundary such as a process, a tool result, an RPC, or an API that returns only success or failure.

A handled failure MUST stay traceable to its origin: the original error's type and message, its cause chain, its stack, and the operation and input that failed. Put that record where the person who debugs it reads: in the rethrown error (wrap it with `cause`, never replace it), in the log the program writes, or in a file that the message names. A shell script that exits non-zero prints the failing command, its exit status, and the path of any log that holds the details.

When a dependency reduces a failure to a Boolean or a code, call the lower-level operation that raises the real error, or record the dependency's limit where its result is used. MUST NOT retry, guess a cause, or report a generic message instead.

An expected outcome that the caller handles as a normal result, such as a search with no match, is not a failure under this rule.

For example, a save function returns `false` when the disk is full, and the caller reports "Save failed". The reader cannot tell a full disk from a read-only file. Good: the caller uses the save operation that throws, and reports `ENOSPC: no space left on device, write 'notes.txt'` with its stack.

For example, a test script launches a program that exits 1, and the script exits 1 with no output, while the details sit in a report file the script never mentions. Good: the script prints "program exited 1; failures in tmp/run-7/report.json".

The same record serves the agent when the developer reports an error. The agent MUST find the trace itself, in the program's logs, error files and saved records, and MUST NOT ask the developer to supply it. When no record holds the trace, the missing record is a defect under this rule: the agent reports it and fixes the code so the next failure keeps its trace.

For example, the developer reports that an app shows only "RuntimeError". Bad: the agent asks for the full error text. Good: the agent reads the app's log and finds the stack; when the app kept only the type name, the agent says so and makes the app save the message and stack in a file that the notice names.

Why: a failure without its cause makes the reader reproduce it to learn what the error already knew. On 2026-10-20, an editor save API reduced errors to `false`, and a workflow script exited 1 silently with its failures in an unmentioned report; each cost a separate investigation. On 2026-10-27, a chat app showed only `RuntimeError` for a failed turn, so the agent had to infer the cause by counting tool calls in the session record.

## Comment rules

- Comment non-obvious reasons, invariants, units, ordering, external constraints, and deliberate trade-offs. Do not restate the code.

@FileSize.md

## Automate Repeated Work

This is DRY applied to execution. [DRY](../AGENTS.development.md#drydont-repeat-yourself) covers the other half: one canonical owner for a fact.

When the same operation runs 3 or more times, build the mechanism that performs it, then run the mechanism. Doing the operation by hand repeats the lookups and the judgement calls with it, and each repetition can go wrong on its own.

For example, the developer asks the agent to migrate every `.prefab` file in a Unity project to `.tscn` in a Godot project. The agent converts all 12 prefabs by hand instead of writing a Python script that converts them. This violates DRY: the agent now looks up Unity YAML syntax once per prefab, and a rule it applies correctly to prefab 3 can be forgotten at prefab 9. The script states the mapping once and applies it 12 times identically.

For example, a change must be checked against 40 scenes. Write one headless script that opens each scene and reports the failures. Opening 40 scenes by hand repeats the same judgement 40 times and produces no record of what was checked.

For example, the same three shell commands run before every commit. They belong in one hook or one script, named once, not retyped per commit.

MAY skip the mechanism when writing it costs more than the work that remains: the operation runs twice, or each case needs a different decision that no rule covers. Say which of the two applies before doing the work by hand.

You will see that many rules above this is a narrow branch of DRY:
- [Treat Workflow Failures as Improvement Triggers](RuleMaintenance.md#treat-workflow-failures-as-improvement-triggers), write a rules so that future mistake won't appear again
- [An Unrelated File Opened Is Also A Correction](RuleMaintenance.md#an-unrelated-file-opened-is-also-a-correction), better project-scoped AGENTS.md, lower error chance

Why: repeated work hides its own cost. Each manual pass looks small, so the total is never compared against the one-time cost of the mechanism, and the mechanism is also the only artifact that survives the task.

## 16 child rule

When to apply: creating, moving, or splitting a file or folder in a project folder that the developer or an agent browses, such as source, tools, assets, data, or documentation.

A folder holds at most 16 direct children. Only folders the developer or an agent creates count: generated output, git-ignored files, and third-party folders such as `node_modules` or a vendored library do not.

Every folder has a meaning: the one thing that all of its children share, such as the feature they implement, the system they belong to, or the owner that edits them. The folder name states that meaning. A reader who knows what they are looking for picks the folder from its name without opening any file inside it.

When a folder would pass 16, look for the groups that already exist among its children and give each group its own subfolder. MUST NOT split only to pass the limit. Numbered parts (`Part1`, `Part2`), alphabetical ranges (`A-M`), and catch-all names (`Misc`, `Common`, `Other`) name no shared meaning, so they are forbidden. When the children share no meaning beyond the parent's, the folder is the exception: report it to the developer with the reason instead of splitting it.

For example, a `UI/` folder holds 25 scripts: 9 for the battle screen, 8 for the shop, and 8 widgets that both screens use. Split it into `Battle/`, `Shop/`, and `Widgets/`. By contrast, `UI1/` and `UI2/` pass the count and tell the reader nothing about which one holds the shop.

Why: the developer and the agent have no reliable memory of where a file lives, so the folder tree is how both find a file without reading many files. A folder with more than 16 children sends the reader back to scanning names one by one, and a folder without a shared meaning sends the reader into every subfolder.

@SharedChecks.md
