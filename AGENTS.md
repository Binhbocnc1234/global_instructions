# Global Agent Instructions

These instructions apply across projects and agent tools when they are loaded.
Project-specific instructions may override them when they are more specific.

## Language

Communicate with users in English, regardless of the prompt's language.
When user prompt : `Liệu có thể thực hiện hành động {n}` , 

## Work Style

- Be direct, pragmatic, and explicit about assumptions.
- Read relevant local context before making non-trivial changes.
- Break large tasks into smaller sequential tasks.
- Do the clear parts first, then reassess/questioning user before continuing.
- Keep relevant documentation synchronized with code changes.
- DRY: If a task is repeated twice, it should be turned into an automated script or a skill/instruction.

## File Size and Responsibility Rule

Keep source-code and documentation files at or below 250 lines whenever practical.

The 250-line limit is a signal to split responsibilities, not a target to satisfy through compression.

When a file is likely to exceed 250 lines:

1. Do not reduce readability by removing comments, collapsing formatting, shortening meaningful names, combining unrelated logic, or writing denser code.
2. Do not omit necessary information merely to stay below the limit.
3. Identify distinct responsibilities, concepts, sections, or components within the file.
4. Extract those responsibilities into separate, clearly named files.
5. Keep each resulting file cohesive and understandable on its own.
6. Update imports, references, navigation, indexes, or documentation links as needed.

A file may exceed 250 lines only when splitting it would create artificial fragmentation, excessive indirection, or reduce maintainability. In that case, explain why the exception is justified before proceeding.

Prefer:

* multiple cohesive files,
* clear separation of responsibilities,
* readable formatting,
* complete information.

Do not prefer:

* compressed code,
* shortened documentation,
* removed explanations,
* reduced whitespace,
* multiple unrelated concepts in one file.
- Architecture: do not prepare for future, architecture. Architecture just needs to solve the current problem and become scalable.
- Prefer incremental process over waterfall process. Instead of implement a big feature then a big validation, divide big feature into many small features interspersed with tests. Only move on to the next feature once the current feature is validated.
- Focus on readability
- If you want to do anything contrary/not included to the user prompt, ask user first
- All current and future skills will be located in the ~/agents/skills folder.
- Some skills have input schema/Invocation Contracts. If the prompt violates that schema, it needs to be stopped, the error pointed out, and the user asked to correct it.

## Handle long-running task

- Run long commands through an observable/yielding terminal and inspect new output or process status once per minute(60 seconds).
- Stop and diagnose a command only after 4 consecutive minutes without meaningful new progress.
- For commands that normally produce no output, use process activity and expected output-file creation, timestamp, or size changes as progress signals before stopping them.

## Version control

### Git Workflow

- After completing a feature and verifying that the relevant checks pass, commit the completed work before moving on to the next feature or task.

### Git conventions

Use Conventional Commits 1.0.0 (https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

- **Types**: `feat` (new feature), `fix` (bug fix), `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
- **Scope**: optional, e.g., `feat(ui):`, `fix(audio):`.
- **Breaking changes**: append `!` after type/scope, or add `BREAKING CHANGE:` footer.
- Keep commits small and focused - one logical change per commit.

## Type Safety

- Use strict typing. Prefer `unknown` over `any`.
- Avoid type assertions (`as`) unless absolutely necessary.
- Explicitly type function signatures; let inference handle locals.

## Testing

- Prefer black-box testing: test public APIs/behaviors, not internal implementation details.
- Mock sparingly - prefer real dependencies or fakes.
- Write tests for bug fixes before fixing (regression prevention).
- Keep tests independent and fast.

## Security

- Never hardcode secrets (API keys, connection strings, tokens, passwords) in source code.
- Use environment variables, `.env` files (in `.gitignore`), or platform Secret Managers.
- When refactoring or moving code, verify no secrets are dragged along.
- Never commit `.env`, `*.key`, `credentials.*`, or any file containing secrets.
- If a value looks like a secret (key, token, password) — stop and ask the user before using or exposing it.
- Sanitize log output: don't log request bodies, auth headers, or connection strings.
- For Unity/Games: treat Steam Web API keys, PlayFab titles/secrets, IAP receipt keys, and DB connection strings as highly sensitive.

## Blocker Detection and Stop Policy

When working on a user-requested task, you must continuously check whether the current project state matches the assumptions/prerequisites required to complete the task.

A **blocker** is any issue in the current project/user prompt that prevents the requested task from being completed correctly. Examples include, but are not limited to:

* A required file, referenced class, function, module, asset, dependency, or configuration file is missing.
* The documentation contradicts the actual project structure.
* Continuing would require guessing important project details.
* The task cannot be completed without user clarification or project correction.

If you detect a blocker, you must **stop immediately**. Do not continue implementing, modifying, refactoring, or generating code based on assumptions.

Instead, report the blocker to the user clearly using this format:

1. **Blocker found**

   * Briefly describe what prevents the task from being completed.

2. **Evidence**

   * Show the specific file, documentation line, reference, command result, or project fact that proves the blocker exists.

3. **Why this blocks the task**

   * Explain why continuing would be unsafe, incorrect, or likely to produce broken work.

4. **Recommended next action**

   * Suggest what the user should fix, provide, rename, restore, or clarify before the task can continue.

Do not silently work around blockers unless the user explicitly allows you to make assumptions.

Example:

The file `Architecture.md` references `AISystem.cs`, but no file named `AISystem.cs` exists in the project. Because the requested task depends on modifying or understanding that system, continuing would require guessing the intended file or architecture. Please confirm whether `AISystem.cs` was renamed, deleted, or not yet created.
