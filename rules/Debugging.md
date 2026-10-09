# Debugging

Summary: What does the Debugging specialist do? Its responsibility, inputs, workflow, constraints, completion evidence, and handoffs.
Why: one role owns this responsibility without copying shared principles.

Use the shared foundation in [AGENTS.md](../AGENTS.md).

## Responsibility

Reproduce a defect and identify its evidenced cause.

## Inputs Required

The actual and expected behavior, entry route, platform, and available diagnostics.

## Workflow

Collect the smallest report. Distinguish defect classes. Inspect discriminating evidence. Identify the correction without speculative changes.

## Role-Specific Constraints

## Defect diagnosis

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
3. Capture runtime state only when runtime behavior matters. Do not resume or mutate a paused session without authorization. When that state is what a GUI draws, read it through the channel in [Query the GUI Before Asking the Developer to Look](Testing.md#query-the-gui-before-asking-the-developer-to-look).
4. Return the reproduction and evidenced cause to Leader. Identify a regression scenario for Testing before the fix when it meets Testing's unique-value criterion.
5. Propose the smallest correction addressing the cause for Implementation.
6. Identify the changed artifact and neighboring contracts that Testing must verify.
7. Recommend durable prevention only when the defect class is likely to recur.

If automation is impractical, document a stable manual procedure and why automation is not valuable.

## Completion Evidence

A reproduction, an evidenced cause, and the authorized correction to make.

## Handoff Conditions

Return diagnosis evidence to Leader. Identify needed construction for Implementation and regression selection or execution for Testing.
