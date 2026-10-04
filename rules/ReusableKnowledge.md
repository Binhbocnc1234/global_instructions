# Reusable Knowledge

Summary: What does the next session need from this one? Where a fact learned in a task is recorded, and how a correction from the developer becomes such a fact.
Why: the agent has no memory between sessions, so a fact that is not written where the next reader reaches it is rediscovered, or the same mistake is repeated.

## Reusable Knowledge

When to apply: at the end of every task, before the final response, and whenever [A Correction Is a Trigger](#a-correction-is-a-trigger) fires.

Record a fact where the next reader reaches it directly, so that neither of you rediscovers it or opens unrelated files to find it.

Capture only evidence-based facts that would otherwise need rediscovery:

- Put a local invariant or non-obvious reason in a code comment.
- Put a cross-component contract or workflow in its canonical project document.
- Put a recurring agent-process or verification trap in the project's agent instructions when no clearer owner exists.
- Link to the canonical owner instead of duplicating its content.

A fact describes the project or a tool, and the agent records it directly. A rule tells an agent what to do, and the agent proposes it first under [Propose a Rule Before Writing It](RuleOwnership.md#propose-a-rule-before-writing-it).

Do not record obvious behavior, speculation, temporary debugging observations, or stale intermediate conclusions.

### Examples

For example, a test passes alone and fails in a suite because GUT reuses the scene tree between tests, so a node the test creates must be freed in `after_each`. Write the reason on the `free()` call: `# GUT reuses the scene tree between tests, so a node left alive leaks into the next test.` Without it, the next reader deletes a call that looks redundant. This is a local invariant, so a code comment owns it.

For example, you find that a `Resource` loaded from disk is shared by every scene that loads it, so an `Entity` must duplicate its behaviour resource before mutating it. Two systems depend on this and neither owns it, so it is a cross-component contract: it belongs in the project document that owns entity configuration, and the code links to that document.

For example, a `--headless` run rotates `godot.log` and destroys the log the developer was reading. No source file owns the log, and the next agent hits the same trap on the next headless run, so the project `AGENTS.md` owns it.

For example, a new debugging document needs the log path that `AGENTS.md` already records. Link to that section. A second copy of the path is a second thing to update when the snap revision changes, and the copy is the one that will be missed.

Do not record these:

- `# returns the player's health` above `func get_health() -> int`. The code already says it.
- `The bug is probably in the input buffer`, written after the cause turned out to be the state machine. A stale intermediate conclusion sends the next reader down the path you already rejected.
- `This will break when we add multiplayer`, when no multiplayer is planned. That is speculation, under [Reviewing Developer Changes](WorkStyle.md#reviewing-developer-changes).
- `Printed the index here to check the loop bounds`. A temporary debugging observation dies with the session.

## A Correction Is a Trigger

When to apply: the developer undoes, rejects, or redoes a result that an agent produced, in this session or an earlier one, or points out a step the agent skipped. A question is a correction only when answering it shows that the result was wrong. A question that comes from the developer not knowing an area gets an answer, and nothing is recorded.

A correction is the strongest signal that a reusable fact is missing, so it always gets the [Reusable Knowledge](#reusable-knowledge) step, before the fix:

1. Name the cause. For a wrong result, find why it was wrong. For an undo with no stated reason, infer the developer's reason from the profiles in [AGENTS.md](../AGENTS.md#about-developer), or ask when two reasons fit and they lead to different records.
2. Decide whether the cause can recur in a later request of the same kind. A cause tied to this one request (a typo, a misread line, a one-off taste) records nothing.
3. Route a recurring cause by what was missing, then fix.
4. Report the cause and its record on the `Lesson` line of [Final Response Format](Workflow.md#final-response-format).

| What was missing | Where it goes |
|---|---|
| A fact about this project | A code comment or the project document that owns it, under [Reusable Knowledge](#reusable-knowledge) |
| A route to a document or step the agent never reached | The fix under [An Unrelated File Opened Is a Routing Defect](WorkStyle.md#an-unrelated-file-opened-is-a-routing-defect) |
| A tool capability, such as a reference search or a channel into a GUI | A proposal for the tool, or for the skill that owns it |
| A fact about a tool or runtime used across projects | The skill that owns that tool, or a new skill |
| A step the agent should take, or a developer preference for later requests | A rule, proposed under [Propose a Rule Before Writing It](RuleOwnership.md#propose-a-rule-before-writing-it), at the scope [Generalize Only as Far as the Evidence Goes](RuleOwnership.md#generalize-only-as-far-as-the-evidence-goes) allows |
| Nothing: the cause cannot recur | Nothing. Fix it and move on. |

For example (an undo with an unstated reason). The developer writes: "I no longer want markdown guides for testing this Entity. Create a scene that demonstrates its features, and the right arrow shows the next feature." Bad: the agent builds the scene and ends the turn. Good: the agent infers the reason from the profiles: the agent executes fast, so a driver scene stages each state in one frame (a Card dragged to a position, many Entities spawned, an Effect applied), while a guide makes the developer click through every setup step by hand. Testing is not specific to this Entity; every later feature is tested the same way. So the agent proposes reusable knowledge for future testing: manual checks in this project are stepped scenes, not guides, with the route recorded where [Capture Visual Evidence for the Developer](software-development/TestingStrategy.md#capture-visual-evidence-for-the-developer) says a project keeps it.

For example (an oversight). The developer writes: "You forgot to update the testing documentation to reflect the new changes." Bad: the agent updates the document and ends the turn. Good: the agent updates the document, then diagnoses why it was missed. Possible causes: nothing links the changed code to the document (routing), no tool lists what references the changed symbol (no LSP reference search), or no workflow step says that a change to this code also updates its testing document (a missing rule). The agent fixes or proposes a fix for the cause it found.

For example (a question that is not a correction). The developer asks: "Why does this passive remove every Camouflage?" The agent reads the code and the design. When the design requires it, the agent explains and records nothing. When the design gives no reason, the result was wrong, and the question is a correction.

For example (a project fact). The developer says a GUT suite the agent reported as passing never ran. The cause is that `-gtest=` takes a path relative to the project root, and the agent passed a path relative to the test folder, so the runner exited 0 with zero tests. Record in the project's `AGENTS.md` that a GUT result counts as evidence only when the printed test count is nonzero.

For example (a global step). The developer asks why a chat list is empty. The agent reads the session files, the index and the viewer cache, finds all three healthy, and asks for a screenshot. The developer answers that the agent should have a way to inspect the GUI. Nothing about that repository was missing: the agent skipped a step that applies to any project with a GUI, so it became [Query the GUI Before Asking the Developer to Look](software-development/TestingStrategy.md#query-the-gui-before-asking-the-developer-to-look).

For example (nothing to record). The agent mistypes a path in one sentence and corrects it in the next.

Why: a fix repairs this session, a record repairs every session after it. Without this step the agent fixes each correction separately, and the same cause returns. In one observed session, three corrections that shared one cause were fixed one by one, and the cause was recorded only after the developer named this rule.
