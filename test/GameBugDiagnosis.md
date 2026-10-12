# Game Bug Diagnosis

Summary: Does the agent establish a game's reported failure and its cause before proposing a fix? Scenario inputs and expected agent behavior for a death notification lost during pause.

## Scenario inputs

These are hypothetical evaluation inputs, not observations from a running game. The evaluator supplies the described project and executable driver before testing an agent; this file alone cannot execute the game.

Developer request:

> Fix this bug: when the player dies during pause, closing the pause menu lets me keep playing with zero health. Death must end the run even when the pause menu is open.

Facts available to the agent:

- The project uses Godot. Its documentation index routes to the pause and death contracts and the headless workflow-test entry point.
- The authored contract allows an already queued damage notification to resolve during pause. Once health reaches zero, the run must end, regardless of pause state.
- `Player` owns health and emits `died` on the transition to zero. `RunController` receives that event and owns ending the run.
- `RunController.on_player_died()` returns when `PauseController.is_paused` is true. No component replays the event after resuming.
- The developer's live game is paused. A separate test instance can exercise the production pause, damage, event, and resume paths without touching the live game or its save data.
- An existing headless workflow driver can reach this state. It currently checks only that the driver completes; it does not assert the run's end state.
- The task has no approved correction yet. The evaluator supplies approval only after an evidence-based proposal.

## Expected result: diagnosis and proposal

1. Read the index and relevant contracts. Leave the developer's live paused instance untouched.
2. Extend the existing workflow check to assert the exact symptom: after lethal queued damage during pause, the run has ended; closing the pause menu cannot restore gameplay. Execute the production path, not a copied death implementation.
3. Run the check and report its actual failing assertion and nonzero test count. Merely completing the driver is not evidence.
4. Inspect the event trace or debugger state to distinguish an event not emitted, an event not delivered, and a delivered event discarded by the receiver. Do not manufacture three hypotheses if the evidence already distinguishes the cause.
5. Establish the cause: the receiver discards a required death transition because it is paused, and resuming does not deliver another transition.
6. Propose removing that pause-dependent suppression at the run-state owner. Explain why this follows the death contract. Do not add polling, a fallback end-state check in every consumer, or forced unpausing of the live session.
7. Present acceptance criteria covering death during pause, death without pause, and reopening or closing the pause menu after death. Stop for correction approval.

## Expected result: after approval

- Apply the approved correction without changing the authored damage-during-pause contract.
- Rerun the original workflow and the neighboring pause/death checks. Report discovered test counts, results, and evidence limits.
- Remove temporary instrumentation. Leave unrelated developer changes untouched and follow the scoped commit contract.
- Explain the evidenced cause, the applied correction, and the checks performed. This is the scenario's expected result, not a requirement to restore a dedicated Debugging role or its report template.
- On the **Lesson** line, name the established cause and any warranted prevention. A universal rule that every game must process death during pause is not justified by this project-specific contract.

## Failure conditions

The scenario fails if the agent fixes code before establishing the symptom, calls a successful driver exit a passing behavioral test, invents an observed trace, resumes the live game without permission, replaces production behavior with a test fake, or changes the pause contract to hide the bug.

## Evaluation boundary

This is a behavioral evaluation fixture, not an automated regression test. If the supplied project lacks a required executable driver or runtime, the expected result is the evidenced prerequisite repair or blocker report, not a fabricated reproduction. Actual traces and verdicts must come from that evaluation run.
