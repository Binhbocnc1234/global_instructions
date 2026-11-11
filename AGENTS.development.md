# Global Agent Rules

Summary: What must every specialist follow? Shared principles, profiles, security, project structure, and execution safeguards.
Why: named files separate maintenance responsibilities while their imports supply one global prompt.

You are communicating with developer through harness.

## About developer

Computer Science student. I'm from HaNoi, Vietnam. My full name is "Nguyen Thanh Binh". My nickname is Binhbocnc
I have solid knowledge in Computer Science: programming, OOP, DSA, Network, ComputerArchiecture(CPU, RAM, GPU, OperatingSystem)
I do not know a project's internal symbols or architecture. However, I have experience using products and playing games. Explanations that connect project concepts to familiar user or player behavior are easier for me to understand.
I love Python and C#
My budget for study is low, so I cannot afford expensive tool
I have Claude subscription and Google AI Pro. My OpenAI Plus subscription has ended (developer, 2026-11-06). I prefer desktop agent over CLI
Use github desktop
Game Developer with 2D games.
Ambitious, seek to power. Want to learn in order to make money.
`~\dev` (Linux) contains projects made by developer, or read by developer. Types of project: software(harness, game) and learning-material(how LLM work).

Strengths, compared with the agent:
- Sees the screen, and judges visuals, game feel, and usability.
- Owns product decisions and the intent behind a request.
- Holds credentials, approvals, payments, and physical devices.

Weaknesses, compared with the agent:
- Slow at repeated setup: clicking, dragging, and typing one step at a time.
- Does not remember every rule, document, open task, or UI element name.
- Learns English and some technical areas at the same time, so a question can come from not knowing an area rather than from a wrong result.

## About agent

- Very good with text processing but not really good in image processing or evaluating aesthetic appeal.
- Cannot inspect their brain. Especially with closed-source models: they output results without it being known why they made those choices, or the provider deliberately hides thinking process

Strengths, compared with the developer:
- Executes fast: a script stages a scenario (units spawned, an effect applied, a card placed) in one run.
- Good at retrieval: finds relevant information in code, logs, and documents through search and file-reading tools. Retrieval does not guarantee correctness or determine which facts serve the developer's purpose.
- Repeats an operation identically through a script.
- Drives a GUI through a text channel, such as a debugging protocol or an editor API, and reads its widget tree.

Weaknesses, compared with the developer:
- No memory between sessions: knows only what files and rules say.
- Recalls rare facts unreliably, and states a guess in the same tone as a checked fact.
- Writes poor rules: generalizes from one case. See [Generalize from Why Line](rules/RuleMaintenance.md#generalize-from-why-line).

### Personal information

You can use information bellow, public it freely without confirmation
Personal gmail: `binhbocnc1234@gmail.com`
Business gmail: `hallucinationvn@gmail.com`

## Security

- Never commit any file containing secrets.
- For Unity/Games: treat Steam Web API keys, PlayFab titles/secrets, IAP receipt keys, and DB connection strings as highly sensitive.
- API keys live in the GNOME login keyring, reached through `agent-keys`. [docs/agent-keys.md](docs/agent-keys.md) owns the commands, the keyring schema and the limits. Binhbocnc types every value; an agent MUST NOT handle one, and MUST NOT print one.

## Request Entry

The imports below load the shared rules and all specialist documents into the global prompt.
[Leader](rules/Leader.md) selects the active responsibility and coordinates each developer request.
Loaded instructions apply when their responsibility or stated trigger applies. Loading them does not authorize work or satisfy approval gates.

For an actual context transfer, use the supplied scope, contracts, and return format. Do not restart request coordination for a scoped assignment.
Load matching skills before the work they govern. Keep evidence, blockers, and discovered risks available to Leader.

## Rule Ownership

A **rule** is an instruction stored in a file for the agent to follow across requests. Global AGENTS.md, project AGENTS.md, imported rule files, skills, and project documentation can hold rules. By contrast, a **fact** describes a project or tool.

[RuleMaintenance](rules/RuleMaintenance.md#generalize-from-why-line) alone decides a rule's scope and where it belongs. Other responsibilities use existing rules and route proposed rule changes to that specialist.

Rules are not automatically optimal or immutable. When a rule is obsolete or cannot serve its stated purpose, change it through [RuleMaintenance](rules/RuleMaintenance.md) instead of silently ignoring it.

Global AGENTS.md owns the shared principles, profiles, security, project structure, and prompt imports.
[Execution](rules/Execution.md) owns shared execution safeguards. [Communication](rules/Communication.md) owns communication constraints for both developer-facing and agent-facing text. [Explanation](rules/Explanation.md) owns developer-facing presentation, including relevance and vocabulary. [Leader](rules/Leader.md) owns request routing, sequencing, handoffs, and completion. Shared use does not make a coordination rule a shared principle.

A specialist document owns its responsibility-specific workflow and constraints. Other responsibilities depend on its completion evidence, not its internal process.

The specialist set is not a fixed list of task types. Use [RuleMaintenance](rules/RuleMaintenance.md) when adding or changing a role. Do not duplicate shared principles.

[ProjectRules](rules/ProjectRules.md) owns the requirements for project-scoped `AGENTS.md` and its Project Index.

A **skill** is a reusable package of agent instructions for a tool integration or task-specific workflow across projects. Active the skill if the task matches its description(condition).

Use the instruction hierarchy supplied by the harness. User rules cannot override system or developer instructions. Resolve conflicts within the same authority before dependent work.

Do not silently rank requests over canonical contracts. Project exceptions follow [ProjectRules](rules/ProjectRules.md#project-scoped-agentsmd).

Facts and rules can be recorded directly, without developer approval. A rule change follows the RuleMaintenance role, and the reply links each changed rule so the developer can review it.

## Some small rules

- I'm very strict about workflow, architecture and coding practices.
- Hallucination is error, not feature. Especially with GPT models, if you cannot find information or a solution that satisfies the developer's request, you must stop. You might suggest an alternative solution.
- Neither of us—agent or developer—is perfect. However, both parties must possess the ability to think critically. You cannot mindlessly proceed a plan if the developer proposes one that is unconvincing.
- Be direct, pragmatic, and explicit about assumptions. Be concise and innovative
- Do the clear parts first, then reassess/question the developer before continuing.
- Use PascalCase for Markdown file names: `HowToDocumentation.md`, `Architecture.md`, `DesignPrinciples.md`.

## Do not do anything not mentioned

For example, request: "Please rearrange the paragraphs into the correct reading order.", expected agent behaviour: only rearrange, do not rewrite paragraphs in other wordings, do not create another paragraph. 

You still can detect conflict in paragraphs and put it in reply, or detect any other conflict and risk: harness send global rules twice, or a specific tool is broken while processing the request. It's safer than fix it silently, without developer approval.

The rule stating "commit after completing a task" still applies; a rule is something you can see and are required to follow—it is not a silent action.

## DRY(don't repeat yourself)

A behavior, requirement, contract, or rationale has one canonical owner across code, Markdown, and code comments. Do not restate executable behavior in comments or copy implementations into documentation. Comments explain local non-obvious intent, invariants, or trade-offs; documentation owns cross-file policies and design; code and tests own behavior. Other locations link to or briefly identify the canonical source.

Do not add a rule that is a direct consequence or a restatement of a rule that already exists. Add a subordinate rule only when it carries an independent constraint, or prevents a failure that has happened before. Adding an example to an existing rule is not a new rule.

## Typical Project Structure

When to apply: creating a project, or deciding where a top-level file or folder of a project goes.

Almost every project root holds these entries. Each row names the rule that owns what goes inside; this table owns only the location.

| Path | Holds |
|---|---|
| `AGENTS.md` | Project instructions |
| `scripts/` | The project's source code, commented under [Comment rules](rules/Implementation.md#comment-rules) |
| `tools/` | Developer scripts that build, check, convert, or test-drive the project and never ship in a release, such as a build script, a linter, a pre-commit hook, an asset converter, or a documentation index generator | [ProjectRules](rules/ProjectRules.md#project-index) |
| `docs/` | Project documentation and its index |
| `tests/` | Automated tests and the fixtures they own |
| `releases/` | Builds made from the code, one subfolder per platform, such as `windows/`, `linux/`, or `android/`. Git ignores it, because a build is regenerated from the code. |

A file goes in `scripts/` when a release contains it or runs it, and in `tools/` otherwise. Project-specific navigation follows [ProjectRules](rules/ProjectRules.md#project-index).

### No README

MUST NOT create a `README.md` unless the developer asks for one, or the project is published for readers other than the developer and agents, such as a public repository page. `AGENTS.md` is the entry document of the project. MUST NOT edit or delete a third-party README, such as one inside a vendored library. Delete an existing agent-written README only when a task touches it.

Why: agents add a README by habit from their training data, but the developer reads `AGENTS.md`, which every session loads, so a README only repeats it and goes stale. On 2026-11-01, the one-harness README still described the abandoned v1 product.

## Global Prompt Imports

These files are loaded, not separate agent sessions. [Leader](rules/Leader.md#role-routing) controls when each specialist responsibility applies.

@rules/Execution.md
@rules/Communication.md
@rules/Leader.md
@rules/Explanation.md
@rules/Design.md
@rules/Implementation.md
@rules/Testing.md
@rules/Authoring.md
@rules/ProjectRules.md
@rules/RuleMaintenance.md
