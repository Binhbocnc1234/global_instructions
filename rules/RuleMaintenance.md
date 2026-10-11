# RuleMaintenance

Use the shared foundation in [AGENTS.md](../AGENTS.md).

Check links, routing, preserved constraints, unique ownership, and representative routing cases when verifying rule changes.

## Examples in a Rule

When to apply: writing or changing an example inside a global rule or a skill.

A reader understands the example from common knowledge plus the concept the rule teaches. Before writing it, test it: can the reader see why A may cause B without recalling a fact from another field? If not, choose another example.

- An example MUST NOT depend on a project, repository, or session. Global rules load at the start of every request, so the reader has no outside context.
- Prefer a setting from daily life or general computing over a setup sentence such as "we are in a game where ...". Use a setup sentence only when no common setting shows the mechanism, or when the rule is about that setting.

For example, an example about a hidden premise uses "after a system update, the laptop battery drains faster". It needs only an update and a battery. By contrast, "a game froze while an asset import ran" needs three facts from game engines first: what an asset import is, that it competes with the game for CPU and disk, and whether the game's log would record that.

For example, an example about a size that needs a number uses "a larger file takes longer to download", not "a larger texture atlas takes longer to import". Both show size and time, but the second also makes the reader know what a texture atlas is.

It does not fire: [Name a project thing by project symbol](Communication.md#name-a-project-thing-by-project-symbol) opens with "we are inside game project", because that rule is about project symbols, and only a project has them. It also does not fire in a project `AGENTS.md`, whose every reader works in that project.

You can take examples from any source (whether from the session itself or ones you come up with yourself), provided they meet the aforementioned conditions.

Why: a rule is added after an agent makes an error in a real session. For example, a hallucinated fact led to [Evidence Labels](Communication.md#evidence-labels), and uncommon, exam-level English words led to the plain-word rules in [Language](Communication.md#language). Developer-specific terminology belongs in [Developer Vocabulary and Direct Phrasing](DeveloperWriting.md#developer-vocabulary-and-direct-phrasing). The agent that writes the rule is still inside that session, and it builds the example from the session's context (the developer suspects a model habit): an agent working in a game project writes examples about that game's units and grid. Every fact the reader must recall from another field stands between the reader and the point, and the developer learns English and the field at the same time.

## The Why Line

When to apply: writing or changing any rule, including a one-line project rule and an `[Override]`.

Rule may carries a `Why`. It states the reason the rule exists. When the reason is a temporary condition, such as a bug, a missing tool, or a deferred task, the `Why` names that condition, so a reader can tell when the rule becomes obsolete. Rule is solution for "why", and that rule maybe not right solution

For example:
- Bad: `[Override] Tests are executed manually by the developer.`
- Good: `[Override] Tests are executed manually by the developer. Why: UnityMCP runs every test even when the agent selects only some of them. Fixing it is a deferred task.`

The bad form gives no reason, so the next developer or agent cannot tell whether the rule still matters, and may delete it while the bug still exists, or keep it forever after the fix. The good form says what to check: once the UnityMCP task is finished, the override can go.. The reason is also what [Generalize Only as Far as the Evidence Goes](#generalize-only-as-far-as-the-evidence-goes) checks the rule's scope against.

## Generalize Only as Far as the Evidence Goes

When to apply: writing or proposing a rule from an observed mistake or a request.

A rule's scope is a claim that the same failure happens everywhere the rule fires. Pick the narrowest scope that holds every observed case(experienced case by agent memory is accepted). Widen it one level only with evidence for that level:

| Scope | Owner | Evidence needed |
|---|---|---|
| One place in the code | A code comment | The case itself |
| One project | The project `AGENTS.md` or document | The cause lies in this project's code, data, tools, or team |
| One tool used across projects | The skill for that tool | The cause lies in the tool, and the tool behaves the same in every project |
| Any project | A global rule | The cause lies in how the agent works, not in any code, and a second case in a different context can be named without changing the cause |

Before proposing the rule, check it:
- The trigger is something the agent can observe in the conversation or the files, such as a kind of message or a file change. A judgement such as "the agent's fault" or "important" is not a trigger, because the agent decides it differently each time.
- The rule has at least two examples where it fires, from different contexts, and one where it must not fire. An example is a test case: a later reader checks the rule against it, and sees that the rule applies instead of being meaningless. When the second firing example needs invented details to fit, the scope is too wide.
- Each word such as `every`, `any`, `always`, or `never` has the evidence of the widest row.
- When an existing rule already covers the case, extend that rule instead, under [DRY](../AGENTS.md#drydont-repeat-yourself).

For example (a trigger that is too wide). After a session where corrections went unrecorded, an agent proposes: "a developer message that questions a result counts as a correction". A question also comes from a developer who does not know an area, so the rule would record a lesson from every explanation. The narrower trigger: "a question is a correction only when answering it shows the result was wrong."

For example (a scope that is too wide). In a game project, an agent changes six consumers of an effect on the assumption that the effect can hold several instances, and the project's effect system allows only one. A global rule "check the data model before every change" restates good practice and prevents nothing specific. The cause lies in one project's effect system, so the record is a project fact

For example (the right global scope). An agent asks the developer to look at a GUI instead of querying its widget tree. The cause is the agent's habit, and the same habit appears in an editor extension, a web page, and a game, so it is a global rule.

Why: an agent generalizes from one case by default, and a rule that is too wide fires where it does not fit. A wrong rule then costs every session that loads it, while the mistake it came from cost one session.

## Propose a Rule Before Writing It

When to apply: the agent wants to add, change, move, or delete a rule in any owner: a global rule file, a skill, a project `AGENTS.md`, or a project document that states rules.

A rule tells an agent what to do. A fact describes a project or a tool, and [Reusable Knowledge](#reusable-knowledge) records a fact without a proposal. For example, "only Buff and Debuff effects can hold several instances" is a fact; "read an effect's category before changing a consumer of it" is a rule.

Propose in the response: the rule text, the owner under [Which global file owns a rule](../AGENTS.md#rule-ownership), the scope evidence under [Generalize Only as Far as the Evidence Goes](#generalize-only-as-far-as-the-evidence-goes), and the mistake it prevents. Write the rule only after the developer accepts it. A request that names the rule and its decisions authorizes writing it; the diff is then the proposal, and the developer reviews it before the commit.

Why: agents write poor rules(developer experience)

## Reusable Knowledge

When to apply: at the end of every task, before the final response, and whenever [A Correction Is a Trigger](#a-correction-is-a-trigger) fires.

Record a fact where the next reader/session reaches it directly, so that neither of you rediscovers it or opens unrelated files to find it.

Capture only evidence-based facts that would otherwise need rediscovery:

- Put a local invariant or non-obvious reason in a code comment.
- Put a cross-component contract or workflow in its canonical project document.
- Put a recurring agent-process or verification trap in the project's agent instructions when no clearer owner exists.
- Link to the canonical owner instead of duplicating its content.

A fact describes the project or a tool, and the agent records it directly. A rule tells an agent what to do, and the agent proposes it first under [Propose a Rule Before Writing It](#propose-a-rule-before-writing-it).

Do not record obvious behavior, speculation, temporary debugging observations, or stale intermediate conclusions.

### Examples

For example, a test passes alone and fails in a suite because GUT reuses the scene tree between tests, so a node the test creates must be freed in `after_each`. Write the reason on the `free()` call: `# GUT reuses the scene tree between tests, so a node left alive leaks into the next test.` Without it, the next reader deletes a call that looks redundant. This is a local invariant, so a code comment owns it.

For example, you find that a `Resource` loaded from disk is shared by every scene that loads it, so an `Entity` must duplicate its behaviour resource before mutating it. Two systems depend on this and neither owns it, so it is a cross-component contract: it belongs in the project document that owns entity configuration, and the code links to that document.

For example, a `--headless` run rotates `godot.log` and destroys the log the developer was reading. No source file owns the log, and the next agent hits the same trap on the next headless run, so the project `AGENTS.md` owns it.

For example, a new debugging document needs the log path that `AGENTS.md` already records. Link to that section. A second copy of the path is a second thing to update when the snap revision changes, and the copy is the one that will be missed.

Do not record these:

- `# returns the player's health` above `func get_health() -> int`. The code already says it.
- `The bug is probably in the input buffer`, written after the cause turned out to be the state machine. A stale intermediate conclusion sends the next reader down the path you already rejected.
- `This will break when we add multiplayer`, when no multiplayer is planned. That is speculation, under [Reviewing Developer Changes](Execution.md#reviewing-developer-changes).
- `Printed the index here to check the loop bounds`. A temporary debugging observation dies with the session.

## A Correction Is a Trigger

When to apply: the developer undoes, rejects, or redoes a result that an agent produced, in this session or an earlier one, or points out a step the agent skipped. A question is a correction only when answering it shows that the result was wrong. A question that comes from the developer not knowing an area gets an answer, and nothing is recorded.

A correction is the strongest signal that a reusable fact is missing, so it always gets the [Reusable Knowledge](#reusable-knowledge) step, before the fix:

1. Name the cause. For a wrong result, find why it was wrong. For an undo with no stated reason, infer the developer's reason from the profiles in [AGENTS.md](../AGENTS.md#about-developer), or ask when two reasons fit and they lead to different records.
2. Decide whether the cause can recur in a later request of the same kind. A cause tied to this one request (a typo, a misread line, a one-off taste) records nothing.
3. Route a recurring cause by what was missing, then fix.
4. Report the cause and its record on the `Lesson` line of [Final Response Format](Leader.md#final-response-format).

| What was missing | Where it goes |
|---|---|
| A fact about this project | A code comment or the project document that owns it, under [Reusable Knowledge](#reusable-knowledge) |
| A route to a document or step the agent never reached | The fix under [An Unrelated File Opened Is a Routing Defect](Execution.md#an-unrelated-file-opened-is-a-routing-defect) |
| A tool capability, such as a reference search or a channel into a GUI | A proposal for the tool, or for the skill that owns it |
| A fact about a tool or runtime used across projects | The skill that owns that tool, or a new skill |
| A step the agent should take, or a developer preference for later requests | A rule, proposed under [Propose a Rule Before Writing It](#propose-a-rule-before-writing-it), at the scope [Generalize Only as Far as the Evidence Goes](#generalize-only-as-far-as-the-evidence-goes) allows |
| Nothing: the cause cannot recur | Nothing. Fix it and move on. |

For example (an undo with an unstated reason). The developer writes: "I no longer want markdown guides for testing this Entity. Create a scene that demonstrates its features, and the right arrow shows the next feature." Bad: the agent builds the scene and ends the turn. Good: the agent infers the reason from the profiles: the agent executes fast, so a driver scene stages each state in one frame (a Card dragged to a position, many Entities spawned, an Effect applied), while a guide makes the developer click through every setup step by hand. Testing is not specific to this Entity; every later feature is tested the same way. So the agent proposes reusable knowledge for future testing: manual checks in this project are stepped scenes, not guides, with the route recorded where [Capture Visual Evidence for the Developer](Testing.md#capture-visual-evidence-for-the-developer) says a project keeps it.

For example (an oversight). The developer writes: "You forgot to update the testing documentation to reflect the new changes." Bad: the agent updates the document and ends the turn. Good: the agent updates the document, then diagnoses why it was missed. Possible causes: nothing links the changed code to the document (routing), no tool lists what references the changed symbol (no LSP reference search), or no workflow step says that a change to this code also updates its testing document (a missing rule). The agent fixes or proposes a fix for the cause it found.

For example (a question that is not a correction). The developer asks: "Why does this passive remove every Camouflage?" The agent reads the code and the design. When the design requires it, the agent explains and records nothing. When the design gives no reason, the result was wrong, and the question is a correction.

For example (a project fact). The developer says a GUT suite the agent reported as passing never ran. The cause is that `-gtest=` takes a path relative to the project root, and the agent passed a path relative to the test folder, so the runner exited 0 with zero tests. Record in the project's `AGENTS.md` that a GUT result counts as evidence only when the printed test count is nonzero.

For example (a global step). The developer asks why a chat list is empty. The agent reads the session files, the index and the viewer cache, finds all three healthy, and asks for a screenshot. The developer answers that the agent should have a way to inspect the GUI. Nothing about that repository was missing: the agent skipped a step that applies to any project with a GUI, so it became [Query the GUI Before Asking the Developer to Look](Testing.md#query-the-gui-before-asking-the-developer-to-look).

For example (nothing to record). The agent mistypes a path in one sentence and corrects it in the next.

Why: a fix repairs this session, a record repairs every session after it. Without this step the agent fixes each correction separately, and the same cause returns. In one observed session, three corrections that shared one cause were fixed one by one, and the cause was recorded only after the developer named this rule.
