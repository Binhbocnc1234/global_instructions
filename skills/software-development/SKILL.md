---
name: software-development
description: Apply an evidence-led workflow for non-trivial software implementation, refactoring, bug fixing, test design, test execution, verification, documentation synchronization, and scoped Conventional Commits. Use when Codex changes a software project or diagnoses a defect where repository context, testing policy, or delivery discipline matters.
---

# Software Development

Use repository evidence to move from requirements to a verified, documented, and intentionally committed change. Treat project instructions as the authority for technology-specific commands and explicit exceptions.

## 1. Understand the Request

1. Classify the task as explanation, design, implementation, refactoring, or bug fixing.
2. Read applicable agent instructions and the project documentation index when one exists.
3. Inspect only the documents, code, configuration, and tests needed to understand the affected concepts and entry route.
4. Separate direct observations from interpretations. Cite exact files, symbols, logs, commands, or documentation for load-bearing conclusions.
5. Stop when a missing requirement, dependency, artifact, or risky decision would force an important guess. State the blocker and evidence.
6. Decide inexpensive, reversible details locally when they do not change product intent or architecture.

For explanation or design-only requests, do not mutate the project unless the user also requests implementation.

## Resolve Instruction Conflicts

Do not silently choose one of two contradictory project rules.

- If the correct resolution is clear and the task authorizes the necessary edit, correct the canonical owner with the implementation.
- If choosing incorrectly would be expensive to reverse, stop and ask one concise question with a recommendation.
- Do not preserve duplicate rules after establishing a canonical owner; link to that owner instead.

## 2. Plan Proportionally

Create a short sequential plan when the task spans multiple responsibilities, has dependencies, or carries meaningful regression risk. Keep one step active at a time and update the plan when evidence changes it.

- Work dependency-first.
- Keep the requested scope explicit.
- Preserve unrelated and concurrent edits.
- Identify the focused verification method before implementation.

Skip a formal plan for a small, self-contained change whose implementation and verification are obvious.

## 3. Construct the Change

- Implement the smallest complete correction that satisfies the requirement.
- Prefer readable, cohesive code over compression or cleverness.
- Follow the project's typing, architecture, naming, dependency, and file-size rules.
- Use explicit types where the language and project policy require them. Do not hide uncertainty behind dynamic escape types.
- Treat required initialized dependencies as invariants. Fix broken construction or wiring instead of adding silent fallbacks, no-ops, or legacy behavior.
- Do not extract a method merely to label a few statements when keeping them inline makes lifecycle or ordering clearer.
- Comment non-obvious reasons, invariants, units, ordering, external constraints, and deliberate trade-offs. Do not restate the code.
- Make a value's unit or representation explicit in its identifier when omission could cause misuse. Follow the project's naming convention with names such as `duration_seconds`, `DurationSeconds`, or `limit_fraction`.
- Do not opportunistically fix unrelated technical debt. Report it when it blocks the requested work or violates an applicable stop policy.

## 4. Select Valuable Tests

Do not create a permanent automated test merely because production code changed. Add or update one when it has unique detection value and manual verification is expensive, unreliable, or unable to cover the relevant state space.

Good permanent boundaries include:

- deterministic business rules and calculations;
- regressions with a stable observable outcome;
- lifecycle, event, concurrency, persistence, or input behavior that requires exact sequencing;
- stable configuration or wiring contracts with repeated regression risk;
- representative scenarios or controlled seeds for probabilistic systems.

Avoid tests for trivial getters, setters, constructors, passthroughs, temporary implementation details, or presentation whose acceptance is primarily visual or experiential.

When a test verifies a production timing, threshold, or limit, reference the owning production constant. Keep test-only tolerances and timing margins explicitly named.

For evolving systems, assert capabilities and invariants rather than internal scores, ordering, or implementation structure. Change accepted benchmarks only through an intentional product decision.

## Execute Tests by Default

Agents own automated test execution by default. Run the smallest relevant fixture first and expand only when risk or focused failures justify it.

A project may explicitly make test execution developer-owned. Treat that as a local exception: write or update the test, inspect it statically, and hand off the exact method or fixture, setup, and expected evidence without running it.

Leave physical-device checks, performance measurement, usability review, and release approval to the developer unless explicitly delegated.

A result is evidence only when the intended fixture was discovered and a nonzero test count executed. A skipped or silently excluded test script is a failure of evidence, even if the runner exits successfully.

## Verification Selection

| Defect or change | First verification method |
|---|---|
| Deterministic rule, calculation, serialization, or data error | Focused unit or integration regression when it has unique value; otherwise the smallest static or manual check |
| Lifecycle, scene/view flow, coroutine, event, physics, or input error | Runtime integration test reproducing the real hierarchy and required frames, or a focused manual scenario |
| Configuration, dependency, prefab, scene, or resource wiring | Inspect persisted configuration and runtime wiring; add a wiring test only for stable recurring contracts |
| Visual clarity, animation, audio, usability, balance, or comprehension | Focused manual review; automate only an underlying deterministic rule |
| Performance, memory, interruption, or device-specific behavior | Measure the affected scenario in the relevant environment or device |

Test the entry route named in the report. Do not bypass the defective route with a helper or alternate setup.

## 5. Fix Bugs from Evidence

Collect the smallest useful report:

```text
Reproduction steps:
Actual result:
Expected result:
Entry route or screen:
Platform and input:
Paused or suspended state:
Screenshot or recording:
Full error and stack trace:
```

Then:

1. Inspect the cheapest evidence that distinguishes likely defect classes.
2. Classify the defect as deterministic logic, lifecycle/integration, persisted wiring, visual/usability, or device/performance.
3. Capture runtime state only when runtime behavior matters. Do not resume or mutate a paused session without authorization.
4. Write a regression test before the fix when it passes the unique-value test and can reproduce the actual entry route.
5. Apply the smallest correction addressing the cause.
6. Verify the changed artifact and relevant neighboring contracts.
7. Add durable prevention only when the defect class is likely to recur.

If automation is impractical, document a stable manual procedure and why automation is not valuable.

## 6. Verify with Current Evidence

Match checks to changed artifacts:

- Code: static analysis, focused tests, then risk-appropriate regression.
- Documentation: metadata/frontmatter validation, links, and diff inspection.
- Configuration or assets: persisted-text inspection plus the real load path.
- Architecture: dependency direction and module-boundary checks.
- Release work: evidence from the exact release candidate.

Probe uncertain engine, language, file-format, or tool behavior before relying on it. Report measurements in the same turn they were taken, or identify the exact revision that produced them.

Report exact commands or actions, discovered and executed counts, pass/fail counts, skipped artifacts, and relevant warnings. Do not claim runtime, visual, performance, or device success without that evidence.

## 7. Synchronize Reusable Knowledge

Capture only evidence-based facts that would otherwise need rediscovery:

- Put a local invariant or non-obvious reason in a code comment.
- Put a cross-component contract or workflow in its canonical project document.
- Put a recurring agent-process or verification trap in the project's agent instructions when no clearer owner exists.
- Link to the canonical owner instead of duplicating its content.

Do not record obvious behavior, speculation, temporary debugging observations, or stale intermediate conclusions.

## 8. Commit Intentionally

After the feature is complete and its required verification passes:

1. Inspect the worktree and diff.
2. Stage only files belonging to the completed change. Leave unrelated edits unstaged.
3. Run a staged diff check when available.
4. Commit using a focused Conventional Commit message.
5. Verify the resulting commit and remaining worktree state.

Do not omit the commit merely because the worktree is dirty; make a scoped commit. Do not commit when the user or project explicitly forbids it, when required verification failed, or when an approval gate requires stopping before commit.

## 9. Hand Off the Result

Lead with the outcome. Include only sections that add value:

- **Summary:** completed behavior and important design decisions.
- **Verification:** exact evidence and remaining manual ownership.
- **Deferred work:** only work genuinely blocked by an unmade decision or unavailable dependency.
- **Questions:** place last and include only risky decisions that must be answered before continuing.

Do not defer authorized work merely because the user has not repeated “go.” When the request already supplies the decision and scope, complete that work in the same turn.

A blocking question is only for a decision that would be expensive to reverse, such as a large refactor, data migration, or discarded work. Include a recommended option and explain what it costs or protects. Do not continue past an unanswered blocking question.

State inherited failures and unrelated dirty files explicitly without presenting them as failures caused by the change.
