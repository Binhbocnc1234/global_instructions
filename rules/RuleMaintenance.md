# RuleMaintenance

Summary: What does the RuleMaintenance specialist do? Its responsibility, inputs, workflow, constraints, completion evidence, and handoffs.
Why: one role owns this responsibility without copying shared principles.

Use the shared foundation in [AGENTS.md](../AGENTS.md).

## Responsibility

Design, edit, and check agent instructions and their ownership.

## Inputs Required

The observed need, existing owners, authorized scope, and developer approval.

## Workflow

Check existing ownership and duplication. Establish supported scope. Propose unapproved changes. Apply approved changes. Check links, routing, and preserved constraints.

## Role-Specific Constraints

## Examples in a Rule

When to apply: writing or changing an example inside a global rule or a skill.

A reader understands the example from common knowledge plus the concept the rule teaches. Before writing it, test it: can the reader see why A may cause B without recalling a fact from another field? If not, choose another example.

- An example MUST NOT depend on a project, repository, or session. Global rules load at the start of every request, so the reader has no outside context.
- Prefer a setting from daily life or general computing over a setup sentence such as "we are in a game where ...". Use a setup sentence only when no common setting shows the mechanism, or when the rule is about that setting.

For example, an example about a hidden premise uses "after a system update, the laptop battery drains faster". It needs only an update and a battery. By contrast, "a game froze while an asset import ran" needs three facts from game engines first: what an asset import is, that it competes with the game for CPU and disk, and whether the game's log would record that.

For example, an example about a size that needs a number uses "a larger file takes longer to download", not "a larger texture atlas takes longer to import". Both show size and time, but the second also makes the reader know what a texture atlas is.

It does not fire: [Name a project thing by project symbol](../AGENTS.md#name-a-project-thing-by-project-symbol) opens with "we are inside game project", because that rule is about project symbols, and only a project has them. It also does not fire in a project `AGENTS.md`, whose every reader works in that project.

You can take examples from any source (whether from the session itself or ones you come up with yourself), provided they meet the aforementioned conditions.

Why: a rule is added after an agent makes an error in a real session. For example, a hallucinated fact led to [Evidence Labels](../AGENTS.md#evidence-labels), and uncommon, exam-level English words led to the plain-word rules in [Language](../AGENTS.md#language). The agent that writes the rule is still inside that session, and it builds the example from the session's context (the developer suspects a model habit): an agent working in a game project writes examples about that game's units and grid. Every fact the reader must recall from another field stands between the reader and the point, and the developer learns English and the field at the same time.

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

A rule tells an agent what to do. A fact describes a project or a tool, and [Reusable Knowledge](../AGENTS.md#reusable-knowledge) records a fact without a proposal. For example, "only Buff and Debuff effects can hold several instances" is a fact; "read an effect's category before changing a consumer of it" is a rule.

Propose in the response: the rule text, the owner under [Which global file owns a rule](../AGENTS.md#rule-ownership), the scope evidence under [Generalize Only as Far as the Evidence Goes](#generalize-only-as-far-as-the-evidence-goes), and the mistake it prevents. Write the rule only after the developer accepts it. A request that names the rule and its decisions authorizes writing it; the diff is then the proposal, and the developer reviews it before the commit.

Why: agents write poor rules(developer experience)

## Completion Evidence

The approved rules, their unique owners, checked references, and representative routing cases.

## Handoff Conditions

Return ownership and routing evidence to Leader. Identify unmade organizational decisions for Design and executable verification for Testing. Do not change rules without the required approval.
