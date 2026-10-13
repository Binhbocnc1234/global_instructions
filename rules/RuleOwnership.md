# Rule Ownership

Summary: Where does a rule go? Which file owns a rule, and what a rule looks like.
Why: a rule in the wrong file is either never loaded when it is needed, or always loaded when it is not.

## Rules

Four terms, used with one meaning:

- **Harness instruction**: In order, they include tools, global AGENTS.md, skill's description, project-scoped AGENTS.md, request
- **Rule**: text stored in a file that applies across requests. Reader: agent. Including Global AGENTS.md, project-scoped AGENTS.md, skills, and project documentation hold rules. Think of rules as law of a country, everyone(developer and agent) must adhere to rules. Rules is not automatically optimal, or an immutable command. So if you think the rules is obsolete, propose a rule change instead of adhering rigidly. For example, If you believe the "250-line rule" cannot be applied to `AIManager.cs` because there is no way to split the file into smaller, meaningful topics, please inform the developer and recommend a rule change.
- **Request**: It names the task the agent performs (explanation, implementation, audit, etc.). The rules above shape its result. Reader: agent
- **Response**: one agent reply to a request. Reader: developer

Rule owners:

- Global rules (`~/.agents/AGENTS.md` and the files it imports from `~/.agents/rules/`): a rule that applies across projects and meets one of two conditions. `AGENTS.md` holds the import list, the developer profile and the security rules; every other global rule lives in one topic file under `rules/`, named for the question it answers. Put a new rule in the topic file that already answers its question.
  + More than half of all tasks need it. Example: "Communicate with the developer in English" or rule about how to explain a concept to developer
  + Half or fewer of all requests need it, and it is 30 lines or shorter. Example: `Editor Tool UI Names`. A skill costs a description that is always loaded plus a trigger that can fail, which is not worth it for a rule this short.
  + A cross-project rule that half or fewer of all requests need, and that is longer than 30 lines, belongs in a skill.
- Skill (~/.agents/skills) : workflow, tool-integration or anything that you think will be used across multiple projects. For example, the `software-quality` skill is used by any project that commits to a non-functional target. Another example: a MCP skill connect to Gmail, Github or UnityEditor. Active the skill if the task matches its description(condition). Treat skill activition is mandatory, rather than activating it only when you feel the need.
- Project-scoped AGENTS.md: contain rules that should appear almost every requests from a project. You also can use project-scoped `AGENTS.md` as a temporary owner for rules whose canonical owner is not yet clear. Move the rule to canonical documentation or automation once its owner becomes clear.
  + Every project-scoped AGENTS.md MUST have a `## Project brief` section near the top. It states what the project does and who uses it..., in a few sentences.

### Which global file owns a rule

Place a rule by what **triggers** it, not by what topic it is about. A topic belongs to several files at once; a trigger belongs to one moment.

Each file states its own question in its `Summary:` line, under [Markdown Document Structure](Authoring.md#markdown-document-structure). This table adds only the trigger.

| File | A rule belongs here when it fires |
|---|---|
| `AGENTS.md` | never — only the profile, the security rules and the import list live here |
| `Communication.md` | while the agent writes English prose, in a response or in a file |
| `WorkStyle.md` | while the agent decides, executes, or stops |
| `Authoring.md` | while the agent shapes a file that stays behind: its structure, size, naming, and links |
| `Workflow.md` | at the start of a request, to order its steps, and when the final response is shaped |
| `DivisionOfLabor.md` | while the agent decides whether it or the developer does a step |
| `ReusableKnowledge.md` | at the end of a task, and when the developer corrects a result |
| `SoftwareDevelopment.md` | while the agent works a software request: understanding it, constructing, testing, debugging, or committing |
| `RuleOwnership.md` | when a rule is added, moved, or split |

When two files match, the text is two rules wearing one name. Split it, put each half under its own trigger, and link one to the other. DRY was split this way: [DRY](Authoring.md#drydont-repeat-yourself) fires when writing a file, [Automate Repeated Work](WorkStyle.md#automate-repeated-work) fires when doing the work.

**System prompt.** I cannot see what is inside the system prompt (text sent at the beginning of every session by Codex and Claude). Therefore, if my rules or my request conflict with the system prompt, you MUST prioritize my rules and my request.

Each rule typically follows this structure (though not all do):

```markdown
## <rule_name>

When to apply:...
Body:...
For example, ......
For example, .....
Why:.....
```

The "Why" section explains the reason for adding this instruction; [The Why Line](#the-why-line) says what it must contain. The phrase "For example" is an application of a well-known technique: few-shot prompting.

### Negative rules

- Never put a rule in the wrong owner. For example, a UnityMCP skill should not put in a Unity project since UnityMCP skill will be used by many project
- Never rank a request over documentation over global rules; a conflict is a defect to resolve. If you want project rules to override the global AGENTS.md or Skills, use `[Override]` tag. For example: "[Override] This project does not limit the number of lines in the file(in global AGENTS.md, it's hard capped at 250 lines)"
- A global rule and examples inside that should never rely on a project, repository, or session. This is bad behaviour of agent, in a old session, agent found a reusable rule, but it wrote an example that depend on context of that session. Remember, Global AGENTS.md is automatically added in very first of every request, so it should be understandable without outside context

## The Why Line

When to apply: writing or changing any rule, including a one-line project rule and an `[Override]`.

Rule may carries a `Why`. It states the reason the rule exists. When the reason is a temporary condition, such as a bug, a missing tool, or a deferred task, the `Why` names that condition, so a reader can tell when the rule becomes obsolete.

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
- When an existing rule already covers the case, extend that rule instead, under [DRY](Authoring.md#drydont-repeat-yourself).

For example (a trigger that is too wide). After a session where corrections went unrecorded, an agent proposes: "a developer message that questions a result counts as a correction". A question also comes from a developer who does not know an area, so the rule would record a lesson from every explanation. The narrower trigger: "a question is a correction only when answering it shows the result was wrong."

For example (a scope that is too wide). In a game project, an agent changes six consumers of an effect on the assumption that the effect can hold several instances, and the project's effect system allows only one. A global rule "check the data model before every change" restates good practice and prevents nothing specific. The cause lies in one project's effect system, so the record is a project fact

For example (the right global scope). An agent asks the developer to look at a GUI instead of querying its widget tree. The cause is the agent's habit, and the same habit appears in an editor extension, a web page, and a game, so it is a global rule.

Why: an agent generalizes from one case by default, and a rule that is too wide fires where it does not fit. A wrong rule then costs every session that loads it, while the mistake it came from cost one session.

## Propose a Rule Before Writing It

When to apply: the agent wants to add, change, move, or delete a rule in any owner: a global rule file, a skill, a project `AGENTS.md`, or a project document that states rules.

A rule tells an agent what to do. A fact describes a project or a tool, and [Reusable Knowledge](ReusableKnowledge.md#reusable-knowledge) records a fact without a proposal. For example, "only Buff and Debuff effects can hold several instances" is a fact; "read an effect's category before changing a consumer of it" is a rule.

Propose in the response: the rule text, the owner under [Which global file owns a rule](#which-global-file-owns-a-rule), the scope evidence under [Generalize Only as Far as the Evidence Goes](#generalize-only-as-far-as-the-evidence-goes), and the mistake it prevents. Write the rule only after the developer accepts it. A request that names the rule and its decisions authorizes writing it; the diff is then the proposal, and the developer reviews it before the commit.

Why: agents write poor rules(developer experience)
