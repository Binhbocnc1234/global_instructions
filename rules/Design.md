# Design

Use the shared foundation in [AGENTS.md](../AGENTS.md).

A proposal includes explicit scope, decisions, constraints, acceptance criteria, and unresolved questions.

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

## Identify unknown concepts

Treat names written with capital letters as possible project concepts. Resolve their meaning from the project index and relevant contracts before designing work that depends on them.

Distinguish an existing reference from a requested new concept:

- When an existing concept or contract is required but cannot be found, apply the shared [blocker policy](Execution.md#blocker-detection-and-stop-policy). Do not invent its meaning.
- When the developer requests a new concept, propose its design. Missing design documentation for that new concept is not itself a blocker. Leader obtains approval before construction.
- Use stated behavior and existing contracts to resolve a request. A value intended for later tuning may receive an explicit proposed default.

For example, “Create Exploder with BasicAlien's stats and an explosion within 1.5 Cells” requires resolving BasicAlien and Cell. Propose any unspecified explosion damage and cost for approval.

For example, “Create a boss” requires a proposed design, not an assumption that an existing boss specification must already exist.

By contrast, an ordinary word that names no project concept needs no repository search.
