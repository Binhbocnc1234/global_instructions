# Construct the Change

- Keep each domain invariant owned by the object whose state it constrains. Do not duplicate or query that invariant from a behavior that merely requests a state change. For example, `Knockback` must not check whether a displaced `Entity` position is valid when `Entity` owns team/grid boundaries; it should request displacement through an operation such as `entity.apply_knockback(delta)`, and `Entity` must enforce the invariant by clamping position. Treat the opposite design as misplaced responsibility or domain-invariant leakage: it violates encapsulation and the Tell, Don't Ask principle.
- Use explicit types where the language and project policy require them. Do not hide uncertainty behind dynamic escape types. For example, do not use `var` keyword in C#.
- Fix broken construction or wiring instead of adding silent fallbacks, no-ops, or legacy behavior.
- Do not extract a method merely to label a few statements when keeping them inline makes lifecycle or ordering clearer.
- Make a value's unit or representation explicit in its identifier when omission could cause misuse. Follow the project's naming convention with names such as `duration_seconds`, `DurationSeconds`, or `limit_fraction`.

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


