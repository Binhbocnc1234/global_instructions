# Design

Use the shared foundation in [AGENTS.md](../AGENTS.development.md).

Design only resolves missing or ambiguous requirements.

## Requirement elicitation

- Rules and requirements are sometimes ambiguous and contains qualitative adjective. If that is true, agent must clarify the request by suggesting one or some precise requirement to the reader. Do not proceed the task if requirements are not clear.

+ For example, rules: "if task is long, create a plan" is a bad rule. Better rule: "if task is long(agent estimates that the task lasts long than 15 minutes), create a plan"

+ For example, consider the following request: "Is there currently any tool capable of searching the web better than the Google search engine?", agent should replies:

```text
`Better` is ambiguous. Please specify what `better` means in this context. For example, do you mean:

1. Higher semantic relevance — results match the meaning of the query even when they use different words or phrases.
2. Higher recall — the search finds more relevant webpages.
3. Higher precision — a larger proportion of returned webpages are relevant
4. Better ranking — the most relevant webpages appear higher in the results.
```

+ For example, we are in the Unity project and I send a request: "Make the code more clean", agent should replies:

```text
`Clean` is ambiguous. Please specify what `clean` means in this context. For example, do you mean:
1. SOLID principles
2. Explicit typing, do not use `var` in C# code
3. Shorter functions — split any function longer than N lines into smaller units
4. Lower cyclomatic complexity — reduce nesting depth and branch count per function
5. Remove dead code — unused imports, variables, functions, and commented-out blocks
6. Remove duplication — extract repeated logic into shared functions or base classes
7. Consistent naming — apply one convention (PascalCase) to all .cs files
8. Formatter and linter compliance — pass Black/Ruff or dotnet format with zero warnings
9. Better documentation — docstrings/XML comments on every public member
10. Separation of concerns — no I/O, logging, or UI calls inside domain logic
11. Explicit error handling — no bare `except:` or silently swallowed exceptions
12. No magic numbers or hardcoded strings — move them to named constants or ScriptableObject
13. Reduce Singleton — pass dependencies as parameters
```

+ SOLID, Singleton and PascalCase is well-documented concept in the Internet so you don't need to specify what is SOLID.
+ Developer may accept ambiguity if they feel that requirements elicitation is too time-consuming and want some exploration
+ For example, the developer asks for a chat UI with the features of a reference product. A feature table ("slash commands: /archive, /rename") is not yet a UI requirement, because it says what each command does, not how the user finds and confirms it. Clarify each feature's interaction by describing what the reference product shows: after typing "/", a list of commands with descriptions; a recognized command shown in a different color. Why: on 2026-10-23, a desktop frontend passed every behavior check, but its commands worked only for a user who already knew their exact text.

## Identify unknown concepts

Treat names written with capital letters as possible project concepts. Resolve their meaning from the project index and relevant contracts before clarifying requirements that depend on them.

Distinguish an existing reference from a requested new concept:

- When an existing concept or contract is required but cannot be found, apply the shared [blocker policy](Execution.md#blocker-detection-and-stop-policy). Do not invent its meaning.
- When the developer requests a new concept, clarify its required behavior. Missing design documentation for that new concept is not itself a blocker.
- Use stated behavior and existing contracts to resolve a request. A value intended for later tuning may receive an explicit proposed default.

For example, “Create Exploder with BasicAlien's stats and an explosion within 1.5 Cells” requires resolving BasicAlien and Cell. Propose any unspecified explosion damage and cost for approval.

For example, “Create a boss” requires clarifying the required behavior, not an assumption that an existing boss specification must already exist.

By contrast, an ordinary word that names no project concept needs no repository search.

### Test a Reading Against the Request

When to apply: a request names a tool, feature, file, or concept, and the work depends on which one it means.

Before starting that work, list what the name can mean. Search the project's names first, including the tools available in this session, then add the meanings the name has in the field. Test each candidate against every fact the request states about the thing, such as where it exists or what it does.

- One candidate exists: proceed.
- Several exist and one fits every fact: proceed with that one, and name it in the first progress text of the turn, so the developer can stop a wrong reading before the work is done.
- Several fit: ask which one, and state how they differ.
- None fits: apply the [blocker policy](Execution.md#blocker-detection-and-stop-policy) and report the name and the fact that failed.

A stated fact that is false under the chosen reading is evidence against that reading first. MUST NOT report the fact as the developer's mistake while another candidate makes it true.

For example, the developer asks: "Product X has a Task tool, and this app has it too. Does that tool make the agent better?" In the field, "task tool" names both a tool that starts a sub-agent and a tool that keeps a to-do list. Bad: the agent researches sub-agents, finds that this app has no sub-agent tool, and replies that the developer's premise is off. Good: the failed fact sends the agent back to this app's tool list, where a to-do tool makes the sentence true, and its first progress text says it is researching the to-do tool.

For example, one repository holds version 1 and version 2 of an app, and the developer asks why the app behaves a certain way. Both versions fit, so the agent asks which one, or finds that the request's evidence names one, before an explanation rests on either.

By contrast, the developer says "the retry limit in the config file is 3", and the file holds one retry limit, with the value 5. The name has one candidate, so the stated value is what is wrong, and the agent reports the mismatch.

By contrast, "fix the typo in the page header" names one thing with no second meaning, so there is nothing to list.

Why: a meaning recalled from other products feels certain, so the agent does not look for a second one. On 2026-11-06, an agent read "Task tool" as the sub-agent tool and spent a full research turn on it, even though its own search showed the app had no such tool and its tool list held a task-list tool. In an earlier session, the developer asked about an app's old sessions, and had to reply "inspect v2, not v1". Models rarely ask on their own: in [Ambig-SWE](https://arxiv.org/html/2502.13069v3), they almost never interacted without an explicit prompt, and for one model a strongly worded instruction cut missed cases from 44% to 18%.
