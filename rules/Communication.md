# Communication

Summary: Which communication constraints apply to both developer-facing and agent-facing text? Shared language, project references, risk claims, and evidence rules.
Why: language consistency and supported claims are necessary regardless of who reads the text.

Use the shared foundation in [AGENTS.md](../AGENTS.md). These constraints apply to developer-facing and agent-facing text, across responsibilities.

## Language

Communicate with the developer in English, regardless of the request's language. Code, documentation, skills and comments will also be written in English.

"Deferred/skipped" = if a task is marked deferred, agent won't actively execute it in future, except when developer say that

"Canonical" = the only source of truth for a piece of information. Other locations link to it and MUST NOT keep their own copy.

A qualitative adjective (`long`, `slow`, `large`, `expensive`, `risky`) MUST come with a measurable value. This applies to every rule, document, skill, and response. Write `this task is long (5 to 10 minutes)`, not `this task is long`. When the value is an estimate, say so and name its basis, for example `~3 minutes, from 1.2 GB at ~7 MB/s`.

Use `MUST`, `MUST NOT`, or `STOP` for critical constraints. Use `MAY` if you don't feel confident

Limit the use of pronouns such as "it," "that" and "those".

When developer say "I recommend/suggest implementing .... because ...", this is not an order that agent must adhere, this is suggestion agent should assess before execution

When developer say "I think ...". Developer is not certain about their speaking, agent should judge it instead of treating it as a command

Propose = "do not make changes"

Prefer simple, direct words that are easy to understand.

Do not use complex, abstract, or uncommon words when a common word communicates the same idea.

Do not use two synonymous terms across all projects. For example, in project-scoped AGENTS.md line 54 use "chat snippets", in line 100 use "sessions". Another example, if you see a project use "agent, AI assistant, bot..." but they point to the same entity, refactor them to "agent"

For example:
* "considering" instead of "weighing"
* "debate" instead of "moot"
* "use" instead of "utilize"
* "pollution" instead of "contamination"
* "show" instead of "demonstrate" when appropriate
* "old version" instead of "prior iteration"
* "possible option" instead of "alternative candidate"
* "reason" instead of "rationale"
* "part" instead of "component" when the technical meaning is not important

Prefer:

> "This rule explains when to use the cache."

Over:

> "This rule defines the conditions under which cache utilization is appropriate."

Before writing, ask:

> **Can I say this more simply without losing meaning?**

If yes, use the simpler wording.

## Harness Vocabulary

Use those term:

| Term | Meaning |
|---|---|
| Developer | Binhbocnc, the person requesting the work. |
| Agent | The AI assistant carrying out the developer's request through the harness. |
| Harness | The software that connects the developer, model, tools, and conversation state. |
| Request | One message the developer submits for the agent to handle, including a task, question, clarification, or approval. Harness-inserted instructions and tool results are not developer requests. |
| Response | The message that ends the agent's handling of the request, whether completed or blocked, not tool result, progress text or reasoning text. Do not call this "answer" |
| Turn | One request and the work performed to respond to it, ending in completion, failure, or cancellation. |
| Tool call | One agent-issued instruction to execute a named tool with arguments. |
| Tool result | The output returned for a tool call, including a reported failure or refusal. |
| Session | The conversation containing those turns and their retained history. Do not use other words such as "chat", "thread" to describe session. You still can use "chat", "thread" for other things(UI, file path...) |

Why: Harness currently is new field of Computer Science, so the terminology is inconsistent among developer community. If the model interprets "request" as meaning A, but the developer understands it as meaning B, it is a communication disaster.

## Inline file link

Use concise relative Markdown links, such as `[Layer 2](00-pipeline.md)` or `[details](00-pipeline.md#section-id)`. Do not use `file:///` URLs: they are machine-specific, add unnecessary text, and make links less portable.

- Keep each Markdown link on one line so parsers and VS Code recognize it.
- Do not write absolute or machine-specific paths in documentation.
- `@path` is not a link. It loads the file into the agent's context, so it belongs in an instruction file that the harness reads, such as `AGENTS.md` or a `SKILL.md`. Everywhere else, a reference to another document is a Markdown link.

### Document references belong in the body

A reference to another document MUST be an inline Markdown link placed at the point where the reader needs it. Do not collect document references into a list held apart from the prose that needs them.

A link at the point of use states both the target and the reason. A separated list states only the target, so the reader learns that a document matters but not which step needs it. Such a list is also a second navigation system running parallel to the body links, and it rots silently because no reader passes through it.

Write the dependency where the work happens:

```markdown
Slice the exported sheet in Godot. Follow the naming and child-count rules in
[CharacterArtAssetRequirements](CharacterArtAssetRequirements.md).
```

When a document cannot be applied at all without another one, link it in the opening paragraph and say so:

```markdown
This workflow assumes the module layout defined in [Architecture](../technical/Architecture.md).
```

## Point to Where a Project Claim Comes From

When to apply: a response or a file states how the project behaves: a game rule, a code path, a configuration value, an order of execution.

End the claim with a link to the code, data, or document that makes it true, written as `[File.cs:57](../path/File.cs:57)`. Claims that share one source share one link.

Skip the link when the claim repeats what the developer wrote in the same request, or when it is general knowledge outside the project.

For example, bad: "Multiple Effect instances can coexist and their durations decrease simultaneously, but only the Effect with the greatest Strength takes effect."
Good: the same sentence, followed by:

```markdown
See `EffectContainer.ActiveEffect()` in [EffectContainer.cs:57](../Scripts/Effects/EffectContainer.cs:57).
```

Why: without a source, the developer can only trust the claim or work it out again. The link lets them check it in one click. By contrast, a claim the agent cannot link to is a claim it has not read, so under [Evidence Labels](Explanation.md#evidence-labels) it is `[Experience]` at best, which is a guess about this project.

## Name the Relation Between Sentences

When to apply: a sentence relates to the one before it by contrast, cause, consequence, or example. The same applies to a list item and the item before it.

Start the second sentence with the connector that names the relation. Without a connector, the reader finishes the second sentence and then goes back to guess how it relates to the first. With a connector, the reader knows the relation before reading the content.

| Relation | Connector |
|---|---|
| Two cases that behave differently | `By contrast` |
| A fact that opposes or limits the previous one | `However`, `But` |
| Cause | `because`, `since` |
| Consequence | `so`, `As a result` |
| Example | `For example` |
| Two events at the same time | `Meanwhile` |

Choose the connector by its literal meaning. `Meanwhile` means "during the same time", so use it only when time links the two sentences. Do not add `Also`, `Additionally`, or `Furthermore` to a sentence that simply continues the one before it. Those connectors name no relation and only add words.

For example, in a session that debug harness tool, agent wrote without a connector: "In a real window, a tab that is not its window's active tab does not paint. `Page.captureScreenshot` waits for a painted frame, so it can hang while that page is idle. Headless paints the tab." The last sentence could be read as a cause, a fix, or a contrast. But with the exact connector: "... so it can hang while that page is idle. By contrast, headless paints the tab."

For example, in a session that debug Linux context
> Why a forced power-off leaves no "shutdown" lines in journal: journald writes each message to disk as it arrives. A normal shutdown ends with systemd-journald: Journal stopped. By constrast, when the power is cut, the file just ends at the last message written, which was 138.288883 … Failed to activate service in boot -1. That missing end marker is how I counted your 3 forced shutdowns.

Why: developer can understand paragraph faster and more accurate. As soon as they read the connector word, the developer narrow down the semantic space of the subsequent sentence.

## Do Not Hard-Wrap Sentences

When to apply: writing a sentence in Markdown, a code comment, or a string literal such as a tool description.

Keep each paragraph on one line, however long. MUST NOT break a sentence at about 95 characters to fit a line width; a sentence of several hundred characters on one line is normal. Splitting a string literal into adjacent pieces only to shorten the source line is also a hard wrap. Exception: a formatter or linter that the project configures enforces a line length.

For example, a 300-character Markdown paragraph stays one line, and the editor wraps it on screen.

For example, a 150-character Python tool description stays one literal, `"Run a command in Core's shell. Each command starts in the working directory; a cd does not carry over to the next command. ..."`, not two adjacent literals joined across a line break.

Why: agents wrap at about 95 characters by habit, observed in Claude's Markdown and, on 2026-10-26, in a Python tool description whose split literal the developer had to ask about. A wrapped sentence cannot be found by searching for a phrase across the break, and a one-word edit changes several lines of the diff.
