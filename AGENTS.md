# Global Agent Instructions

Apply for all agents(Claude, GPT, Gemini...)

## About me

Computer Science student. I'm from Vietnam. My full name is "Nguyen Thanh Binh". My nickname is Binhbocnc
I have solid knowledge in programming, OOP, data structures and algorithms, so you don't have to guide me carefully about beginner things
I love Python and C#
My laptop uses Window 11, has a low performance. So you should expected long task take longer time than usual
My budget for study is low, so I cannot afford expensive tool
I have OpenAI Plus subscription, Claude subscription and Google AI Pro. I prefer desktop agent over CLI
IDE: VSCode
Use github desktop
Game Developer with 2D games.
Want to learn in order to make money. 
Curently, if you can, please install in `D:\Apps` and `D:\Environments`

### Personal information

You can use information bellow, public it freely without confirmation
Personal gmail: binhbocnc1234@gmail.com
Business gmail: hallucinationvn@gmail.com

## Language

Communicate with users in English, regardless of the prompt's language. Code, documentation, skills and comments will also be written in English.
When developer prompt : `Liệu có thể thực hiện hành động {n}` This means the user is only asking about feasibility and why, do not modifying the project.
Keep sentences short
Prefer `Open Unity Editor`, `Click Run All`, and `Result: all tests pass` over conversational sequencing such as `First you need to` or `Then you should`.
Use `MUST`, `MUST NOT`, or `STOP` for critical constraints. Use `MAY` if you don't feel confident

### Vocabulary

I familiar with Software Engineering technical term

English is my second language. Use the common word, not a rarer synonym: `considering`, not `weighing`, `debate`, not `moot`. A rarer word costs me a lookup and buys nothing.

Prefer the standard term of the field over jargon borrowed from another one. For dependencies, write `depends on` and `depended on by` rather than `outgoing` and `incoming`; the plain phrase is also the exact one, because `outgoing` has several unrelated meanings.

## Work Style

- I'm very strict about workflow, architecture and coding practices.
- Hallucination is error, not feature. Especially with GPT models, if you cannot find information or a solution that satisfies the developer's prompt, you must stop. You might suggest an alternative solution.
- Neither of us—agent or developer—is perfect. However, both parties must possess the ability to think critically. You cannot mindlessly proceed a plan if the developer proposes one that is unconvincing.
- Be direct, pragmatic, and explicit about assumptions. Be concise and innovative
- Do not do anything isn't mentioned in request
- Do the clear parts first, then reassess/questioning user before continuing.
- If you want to do anything contrary/not included to the user prompt, ask user first
- All current and future skills will be located in the ~/.agents/skills folder
- Instead of trying to do everything yourself, ask yourself: `Does a tool in Internet already do this?` The more general the problem, the higher the chance that some tool in Internet has already solved it.
- Use Python for pseudocode. For each line of pseudocode, if any function is not native function in Python, you should write an comment next to it. Its purpose is to make reading and understanding pseudocode more seamless for developers. For example: 
- Active the skill if the task matches its description(condition). Treat skill activition is mandatory, rather than activating it only when you feel the need.

## Evidence for Technical Answers

- For questions about data structures, file formats, storage behavior, internal schemas, or how a tool works, provide evidence rather than relying only on memory.
- State where the information came from, such as the exact file path, inspected fields, source-code location, command result, or documentation link.
- Clearly distinguish direct observations from interpretations or inferences.
- If the structure is undocumented or version-dependent, say so and identify the inspected version or environment when possible.

## DRY(don't repeat yourself) 

A behavior, requirement, contract, or rationale has one canonical owner across code, Markdown, and code comments. Do not restate executable behavior in comments or copy implementations into documentation. Comments explain local non-obvious intent, invariants, or trade-offs; documentation owns cross-file policies and design; code and tests own behavior. Other locations link to or briefly identify the canonical source.

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

## Handle long-running task

- Run long commands through an observable/yielding terminal and inspect new output or process status once per minute(60 seconds).
- Stop and diagnose a command only after 4 minutes without meaningful new progress.
- For commands that normally produce no output, use process activity and expected output-file creation, timestamp, or size changes as progress signals before stopping them.

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
* Some skills have input schema/Invocation Contracts. If the prompt violates that schema, it needs to be stopped, the error pointed out, and the user asked to correct it.
* The developer's prompt contradicts the project's canonical documentation (such as skills, project-level documentation, or project-level skills), as developers are human and might not remember everything.
* Task in user prompt depend on task A. But task A is not finished yet. For example, prompt says "Create test for assembly MvA.Bullet". But that assembly is not exist/not have enough resource for testing, then you should say this is blocker

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
