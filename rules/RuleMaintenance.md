# RuleMaintenance

Use the shared foundation in [AGENTS.md](../AGENTS.development.md).

When to apply: reviewing, proposing, creating, or changing agent rules.

Most rules are added from agent mistake, and that mistake lead to consequences. Some rules come from developer preferences, or for the sake of consistency. For example, if we don't have a rule requiring Markdown filenames to be in PascalCase, the agent will name files arbitrarily; consistency makes reading the data faster.

Recommended structure of a rule:

```markdown
## Rule name

Write instructions here

For example, ...

For example, ...

Why:...
```

Most rules follow that structure; examples may be unnecessary if a rule is so straightforward that applying it requires almostly no reasoning.

When writing or editing rules, write for both agent and developer. The reason is developer must be able to judge whether the instruction solves the observed problem without weakening its meaning for the agent.

## Workflow

Why --> Examples --> Abstract instructions

Before writing the wording, check whether the reader can perform the required action using the rule and its explicit references. MUST NOT assume the reader has the author's session context or knows where an unnamed prerequisite is documented.

When an instruction requires a particular format, MUST provide the details needed to construct a valid input, or link to the canonical reference that provides them. An example MUST show the format when the format is what the reader needs to learn; explaining only the example's purpose is not enough.

For example, “put excluded directories under `exclude`” leaves the reader to guess the value type. Showing `"exclude": ["vendor/library", "addons/AnimationPanel"]` establishes that the value is an array of path strings. The instruction must still explain path matching or point to its canonical reference.

By contrast, “Open the file” does not need an explanation of files. A missing prerequisite is knowledge needed to carry out this instruction, not every fact related to its topic.

Why: the author can mentally fill in omitted details and mistake that understanding for a usable instruction. Checking the reader's required action exposes those omissions before the rule is written.

Place a rule by what triggers it, not only by its topic. When two owners seem to fit, identify when the agent must act and choose the owner responsible for that action.

For example, deciding who runs a check belongs to execution responsibilities; deciding what the check must verify belongs to testing.

Why: one topic can involve several responsibilities. The trigger identifies which responsibility owns the required action.

## Choose Global Rules or Skills

When to apply: choosing where to store a rule whose cross-project scope is already established under [Generalize from Why Line](#generalize-from-why-line).

- If more than half of requests need the rule, keep it in the global instructions.
- If half or fewer of requests need the rule, keep it in the global instructions when the complete rule, including examples and its reason, is 30 lines or shorter.
- If half or fewer of requests need the rule and the complete rule exceeds 30 lines, put it in a skill.
- Place a global rule in its existing responsibility owner. Do not shorten a rule merely to meet the 30-line cutoff.
- Base frequency on available request history or an explicit developer expectation. If neither establishes which side of half applies, ask the developer before choosing.

For example, a language rule needed in every reply stays global regardless of its length. A document-conversion workflow needed in one request out of ten belongs in a skill when its complete instructions exceed 30 lines. By contrast, a rule that applies only to one project is outside this choice.

Why: these cutoffs are developer-selected placement criteria. Global rules are loaded even when unused; a skill adds a description and an activation step. Keep instructions global when frequent use or a length of at most 30 lines makes that trade-off worthwhile.

## Use Project AGENTS.md as a Temporary Owner

When to apply: a project-scoped rule is needed, but its canonical owner within the project is not yet clear.

The project `AGENTS.md` MAY temporarily own the rule. Mark the placement as temporary and state which ownership decision remains unresolved.

Once the canonical owner is established, move the rule there. If automation fully enforces the rule, remove the duplicate instruction. Leave a link in the project `AGENTS.md` only when needed for routing.

For example, an asset-naming rule may temporarily live in the project `AGENTS.md` while the project decides which document owns asset requirements. Once that owner is chosen, move the rule there. By contrast, do not use temporary placement when an existing document already owns asset requirements.

Why: a needed rule must remain discoverable while ownership is unresolved, without turning temporary placement into a second canonical copy.

## Treat Workflow Failures as Improvement Triggers

When to apply: the developer undoes, rejects, or redoes a result that an agent produced, in this session or an earlier one, or points out a step the agent skipped. A question that comes from the developer not knowing an area gets an answer, and nothing is recorded.

For example (an undo with an unstated reason). The developer writes: "I no longer want markdown guides for testing this Entity. Create a scene that demonstrates its features, and the right arrow shows the next feature." Bad: the agent builds the scene and ends the turn. Good: the agent infers the reason from the profiles: the agent executes fast, so a driver scene stages each state in one frame (a Card dragged to a position, many Entities spawned, an Effect applied), while a guide makes the developer click through every setup step by hand. Testing is not specific to this Entity; every later feature is tested the same way. So the agent records reusable knowledge for future testing: manual checks in this project are stepped scenes, not guides, with the route recorded where [Capture Visual Evidence for the Developer](Testing.md#capture-visual-evidence-for-the-developer) says a project keeps it.

For example (an oversight). The developer writes: "You forgot to update the testing documentation to reflect the new changes." Bad: the agent updates the document and ends the turn. Good: the agent updates the document, then diagnoses why it was missed. Possible causes: nothing links the changed code to the document (routing), no tool lists what references the changed symbol (no LSP reference search), or no workflow step says that a change to this code also updates its testing document (a missing rule). The agent fixes the cause it found.

For example (a question that is not a correction). The developer asks: "Why does this passive remove every Camouflage?" The agent reads the code and the design. When the design requires it, the agent explains and records nothing. When the design gives no reason, the result was wrong, and the question is a correction.

For example (a project fact). The developer says a GUT suite the agent reported as passing never ran. The cause is that `-gtest=` takes a path relative to the project root, and the agent passed a path relative to the test folder, so the runner exited 0 with zero tests. Record in the project's `AGENTS.md` that a GUT result counts as evidence only when the printed test count is nonzero.

For example (a global step). The developer asks why a session list UI is empty. The agent reads the session files, the index and the viewer cache, finds all three healthy, report that agent cannot reproduce the issue and asks for a screenshot. The developer answers that the agent should have a way to inspect the GUI. Nothing about that repository was missing: the agent skipped a step that applies to any project with a GUI, so it became [Query the GUI Before Asking the Developer to Look](Testing.md#query-the-gui-before-asking-the-developer-to-look).

For example (nothing to record). The agent mistypes a path in one sentence then corrects it in the next and this only happen with probality under 5%

For example (nothing to record). Initially, the developer wanted to limit each harness turn to a maximum of 15 minutes, but later changed the requirement to a token budget limit. There is no lesson to be learned here; both requests were simply directives, and the agent was not required to evaluate the underlying reasons for the requests.

For example, a bug appear, this is maybe a testing activity defect: test is too weak for detecting the bug. After fixing the bug, agent should take notice on current testing rules

Why: a fix repairs this session, a record repairs every session after it. Without this step the agent fixes each correction separately, and the same cause returns. In one observed session, three corrections that shared one cause were fixed one by one, and the cause was recorded only after the developer named this rule.

### An Unrelated File Opened Is Also A Correction

When to apply: you read a file, and it held nothing the task needed.

Two causes produce that read: the agent chose badly, or the project routes badly. The second cause can be fixed more easily with a rule. A routing defect is one of:

- The project has no documentation index, so the only way to learn what a document holds was to open it.
- The index entry's description does not describe the document, or it is stale.
- The document mixes kinds, so one sentence cannot describe it. See [Markdown Document Kind](Authoring.md#markdown-document-kind).
- project-scoped `AGENTS.md` or a document links to a file that was renamed, moved, split, or deleted.

For example, a task about the build pipeline ends with the agent opening six files under `tools/` because no document names which one runs first. Nothing is stale; the routing simply does not exist. The fix is an entry in `AGENTS.md` naming the entry point.

## The Why Line

Rule may carries a `Why`. It states the reason the rule exists. When the reason is a temporary condition, such as a bug, a missing tool, or a deferred task, the `Why` names that condition, so a reader can tell when the rule becomes obsolete. Rule is solution for "why", and that rule maybe not right solution

For example:
- Bad: `[Override] Tests are executed manually by the developer.`
- Good: `[Override] Tests are executed manually by the developer. Why: UnityMCP runs every test even when the agent selects only some of them. Fixing it is a deferred task.`

The bad form gives no reason, so the next developer or agent cannot tell whether the rule still matters, and may delete it while the bug still exists, or keep it forever after the fix. The good form says what to check: once the UnityMCP task is finished, the override can go.

## Generalize from Why Line

Start with the cause of the observed failure, or the reason stated in [The Why Line](#the-why-line). Choose the narrowest scope in which that cause or reason applies.

Evidence MUST support both the cause or reason and the proposed scope. Similar outcomes alone do not establish a shared cause. A `Why` line states the reason; it does not prove it.

Use the following table to choose the owner and check the evidence needed for that scope:

| Scope | Owner | Evidence needed |
|---|---|---|
| One place in the code | A code comment | The case itself |
| One project | The project `AGENTS.md` or document | The cause lies in this project's code, data, tools, or team |
| One tool used across projects | The skill for that tool | The cause lies in the tool, and the tool behaves the same in every project |
| Any project | A global rule | The cause lies in how the agent works, not in any code, and a second case in a different context can be named without changing the cause |

Before writing the rule, check it:
- The trigger is something the agent can observe in the conversation or the files, such as a kind of message or a file change. A judgement such as "the agent's fault" or "important" is not a trigger, because the agent decides it differently each time.
- The trigger identifies the conditions where the cause or reason applies, not merely a similar outcome.
- Include an example where the rule applies and one where it does not. For a rule that applies across contexts, include at least two applicable examples from different contexts, supported by evidence of the same cause or reason. A rule confined to one place does not require a second context. Invented examples MAY illustrate a rule, but MUST NOT count as evidence for widening its scope.
- Each word such as `every`, `any`, `always`, or `never` MUST be supported by evidence for the scope it claims.
- When an existing rule already covers the case, extend that rule instead, under [DRY](../AGENTS.development.md#drydont-repeat-yourself).

For example (a trigger that is too wide). After a session where corrections went unrecorded, an agent proposes: "a developer message that questions a result counts as a correction". A question also comes from a developer who does not know an area, so the rule would record a lesson from every explanation. The narrower trigger: "a question is a correction only when answering it shows the result was wrong."

For example (a scope that is too wide). In a game project, an agent changes six consumers of an effect on the assumption that the effect can hold several instances, and the project's effect system allows only one. A global rule "check the data model before every change" restates good practice and prevents nothing specific. The cause lies in one project's effect system, so the record is a project fact

For example (the right global scope). An agent asks the developer to look at a GUI for visual testing instead of querying its widget tree. The cause is the agent's habit, and the same habit appears in an editor extension, a web page, and a game, so it is a global rule, with some adoption in each project

Why: an agent generalizes from one case by default, and a rule that is too wide fires where it does not fit. A wrong rule then costs every session that loads it, while the mistake it came from cost one session.

## Examples in a Rule

When to apply: writing or revising an example in an agent instruction.

A reader understands the example from common knowledge plus the concept the rule teaches. Before writing it, test it: can the reader understand the rule recalling a fact from another field? If not, choose another example.

- An example MUST NOT depend on a project, repository, specific vendor or session. Global rules load at the start of every request, so the reader has no outside context.
- Prefer a setting from daily life or general computing over a setup sentence such as "we are in a game where ...". Use a setup sentence only when no common setting shows the mechanism, or when the rule is about that setting.
- An example MUST include the context needed to understand why the rule applies: the relevant situation or request, the condition that affects the choice, and the action or result that illustrates the rule.
- When an example comes from a project, repository, vendor, or session, explain the necessary facts within the example or choose a self-contained setting.
- Include only context that changes how the reader interprets or applies the rule. Common knowledge does not need an explanation.

For example, an example about a hidden premise uses "after a system update, the laptop battery drains faster". It needs only an update and a battery. By contrast, "a game froze while an asset import ran" needs three facts from game engines first: what an asset import is, that it competes with the game for CPU and disk, and whether the game's log would record that.

For example, an example about a size that needs a number uses "a larger file takes longer to download", not "a larger texture atlas takes longer to import". Both show size and time, but the second also makes the reader know what a texture atlas is.

You can take examples from any source (whether from the session itself or ones you come up with yourself), provided they meet the aforementioned conditions.

For example, a rule distinguishes a requested outcome from an implementation step. “Changing the converter is not a second outcome” leaves the reader to guess what was requested. Instead, write: “The developer wants exported documents to open in another application with text and images preserved. Propose that result; changing the converter is a possible way to achieve it, not a separate outcome.”

By contrast, “A download contains 100 MB and the connection transfers 10 MB per second, so the transfer takes about 10 seconds, excluding overhead” already supplies the facts needed to illustrate a time estimate. The example needs no project history or explanation of what a download is.

Whether an example supports a rule's scope is governed by [Generalize from Why Line](#generalize-from-why-line).

Why: an author remembers the omitted situation and can mistake a fragment for a complete example. Supplying the facts that affect the choice lets a reader understand and judge the example without the author's session context.

