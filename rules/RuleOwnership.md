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
| `TaskManagement.md` | when work spans more than one request |
| `SoftwareDevelopment.md` | while the agent works a software request: understanding it, constructing, testing, debugging, or committing |
| `RuleOwnership.md` | when a rule is added, moved, or split |

When two files match, the text is two rules wearing one name. Split it, put each half under its own trigger, and link one to the other. DRY was split this way: [DRY](Authoring.md#drydont-repeat-yourself) fires when writing a file, [Automate Repeated Work](WorkStyle.md#automate-repeated-work) fires when doing the work.

`TaskManagement.md` stays global although it is 61 lines and few requests need it. The developer decided this: a task file that is not loaded is a task file that is never written.

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

The "Why" section explains the reason for adding this instruction. The phrase "For example" is an application of a well-known technique: few-shot prompting.

### Negative rules

- Never put a rule in the wrong owner. For example, a UnityMCP skill should not put in a Unity project since UnityMCP skill will be used by many project
- Never rank a request over documentation over global rules; a conflict is a defect to resolve. If you want project rules to override the global AGENTS.md or Skills, use `[Override]` tag. For example: "[Override] This project does not limit the number of lines in the file(in global AGENTS.md, it's hard capped at 250 lines)"
- A global rule and examples inside that should never rely on a project, repository, or session. This is bad behaviour of agent, in a old session, agent found a reusable rule, but it wrote an example that depend on context of that session. Remember, Global AGENTS.md is automatically added in very first of every request, so it should be understandable without outside context