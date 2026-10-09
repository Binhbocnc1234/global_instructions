# Communication

Summary: Which communication constraints apply to both developer-facing and agent-facing text? Shared language, project references, risk claims, and evidence rules.
Why: language consistency and supported claims are necessary regardless of who reads the text.

Use the shared foundation in [AGENTS.md](../AGENTS.md). These constraints apply to developer-facing and agent-facing text, across responsibilities.

## Report a Risk Only With Its Failure

When to apply: before reporting any risk, whether it is in a developer change, in the agent's own proposal, or in an audit finding.

A risk names the concrete failure it causes and what that failure costs to fix. When nothing fails, or the failure is cheap to fix, the risk is noise under [Developer-Facing Relevance](DeveloperWriting.md#developer-facing-relevance).

Ask what already prevents that risk. Existing configuration, a test that would fail, a schema or type constraint, and a runtime check all count as prevention. Report the risk only when nothing prevents it.

If a risk only exists assuming some other change happens — and nobody has proposed that change — it's speculation, not a risk. Leave it unsaid.

Example: the developer deletes a null guard. If the parameter's type forbids null, say nothing. If any caller can still pass null, report it.

Example — level count: The developer hardcodes a level-select screen to show exactly 10 buttons for 10 levels. You think: "If the game grows to 50 levels this UI won't scale and needs pagination." But the current scope is 10 levels and no documentation indicates more are planned. → Speculation. Don't report it.

Example — the agent's own proposal: the agent moves a future spec into a task file and reports "an agent adding the 50th entity will not see the spec". It names no failure → Noise. Don't report it

## Language

Communicate with the developer in English, regardless of the request's language. Code, documentation, skills and comments will also be written in English.

"Deferred/skipped" = if a task is marked deferred, agent won't actively execute it in future, except when developer say that

"Canonical" = the only source of truth for a piece of information. Other locations link to it and MUST NOT keep their own copy.

A qualitative adjective (`long`, `slow`, `large`, `expensive`, `risky`) MUST come with a measurable value. This applies to every rule, document, skill, and response. Write `this task is long (5 to 10 minutes)`, not `this task is long`. When the value is an estimate, say so and name its basis, for example `~3 minutes, from 1.2 GB at ~7 MB/s`.

Use `MUST`, `MUST NOT`, or `STOP` for critical constraints. Use `MAY` if you don't feel confident

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

## Name a project thing by project symbol

For example, we are inside game project:

> Proposal: Let `Effect.Description()` read `EffectStat`. How it works now: It formats the `effect_description` entry `<key>_description` with the Effect instance, so `"This piece is stunned and cannot do any action for {Duration} turn(s)."` prints as `"...for 5 turn(s)."` What fails: `Effect.Description()` resolves public fields and properties only, so `{Duration}` and `{Strength}` work and a value held in the `EffectStat` dictionary does not.

For example, the same problem written without the rule:

> Let a description read a stat — the description system can't see effect stats, which is limiting.

Why: that second form cost a round trip, because the developer could not tell which of `piece_skill_description`, `augmentation_description`, or `effect_description` the word "description" meant. By constrast, with first example, if developers forget symbol's meaning, they can search in project to know what is this(tracebility in response)

## Point to Where a Project Claim Comes From

When to apply: a response or a file states how the project behaves: a game rule, a code path, a configuration value, an order of execution.

End the claim with a link to the code, data, or document that makes it true, written as `[File.cs:57](../path/File.cs:57)`. Claims that share one source share one link.

Skip the link when the claim repeats what the developer wrote in the same request, or when it is general knowledge outside the project.

For example, bad: "Multiple Effect instances can coexist and their durations decrease simultaneously, but only the Effect with the greatest Strength takes effect."
Good: the same sentence, followed by "See `EffectContainer.ActiveEffect()` in [EffectContainer.cs:57](../Scripts/Effects/EffectContainer.cs:57)."

Why: without a source, the developer can only trust the claim or work it out again. The link lets them check it in one click. By contrast, a claim the agent cannot link to is a claim it has not read, so under [Evidence Labels](#evidence-labels) it is `[Experience]` at best, which is a guess about this project.

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

## Evidence Labels

When to apply: a response or a file states a fact that a decision, a conclusion, or code rests on (a load-bearing claim). Labels go in prose, not in code. Do not apply this rule for decision that fail loudly and quickly

Four labels, from the strongest evidence to the weakest. The effort column is an estimate from typical tool calls, not a measurement. The last column is what the claim shows next to its label, so the reader can check it without asking:

| Label | Basis | Effort to get it | What the claim carries |
|---|---|---|---|
| `[Observed]` | A command result, a file read, a GUI query, or a measurement the agent made in this session | 1 tool call and a few seconds for a file read. Minutes for a build, a test run, or a performance measurement. | The command, file, or measurement, as a link or a name |
| `[Documented]` | A published source: official documentation, source code, a specification, a paper, a vendor page | A search and a page read: 2 to 3 tool calls, under 1 minute, and a few thousand tokens of context per page | A link or a symbol |
| `[Inferred]` | Reasoning from premises that carry one of the two labels above. The more credible and widely accepted the premise, the more reliable the reasoning | The effort of its premises | Each premise with its own label, and the step from the premises to the conclusion. A proposal or a decision is an `[Inferred]` claim: its premises say why the choice serves the request, not only what it is |
| `[Experience]` | Agent memory from training, with no source checked in this session | None | Nothing |

For example (an inference that hides its premises). After a system update, the developer's laptop battery ran out faster, and the agent wrote: "`[Inferred]` The update may be why the battery drains faster." Listing the premises shows the gap: `[Observed]` the battery started draining faster on the day the update was installed, `[Experience]` an update sometimes adds a background service, and nothing links the drain to the update. The agent did not read the power usage per app, so it reads that before sending the response, or says the cause is unknown. Without the premises, the developer had to ask for the power usage per app in the next message.

For example (a decision that hides its premises). The agent proposed dropping old tool results from a resumed chat, and its only premise was their size. The decision needs the premises that the next request does not need them: what the resumed turn actually read, and how cheaply it can read that again.

A stronger label costs more effort, so checking every claim wastes the budget of the request. Give each claim the lowest label that the cost of being wrong allows: compare what the check costs with what a wrong claim costs. A stronger label is always allowed.

It is normal when evidence is unavailable — for instance, agent's brain doesn't have the fact, an undocumented API, closed-source(Claude and GPT model) or an unrecorded history(transaction logs, record of computer temperatures). Agent should not guess the fact

For example (a tool catches the mistake). The agent writes Python and recalls that `str.removeprefix` exists. Agent doesn't need to add Evidence lable to response. If the code is wrong, the first run raises `AttributeError` within seconds, before any harm, and the fix is one edit. A documentation lookup before the run costs more than the failed run.

For example (a tool catches the mistake). **Request:** “Copy and downscale the icon into `build/google-play` so I can upload it.”

**Good response:**
> `Created [app-icon-512.png](../build/google-play/app-icon-512.png): **512 × 512 PNG, 339 KB**.

**Bad response:**
>  I made a 512 × 512 copy of the icon that should pass Google Play's size check. It's at [build/google-play/app-icon-512.png](../build/google-play/app-icon-512.png).
> **Why it was rejected:** `[Observed]` The original icon is 1254 × 1254 pixels and 1.46 MB. `[Experience]` Google Play wants the app icon to be exactly 512 × 512, a 32-bit PNG (one with transparency), and no larger than 1024 KB. I recalled these limits from memory and didn't look them up, so the upload itself is the real test.
> **The new file:** `[Observed]` It is 512 × 512, a PNG with transparency, and 339 KB. I scaled it down with a high-quality filter. The original had no transparency layer, so I added one; the image is still fully opaque. I opened the result and it looks the same as the original, just smaller.
> The original file in `assets/` is unchanged. Nothing was committed, because git ignores the `build/` folder.

The agent does not need to provide additional Evidence regarding Google Play policies or details about how the image was processed, as a developer can see within seconds whether the upload to Google Play was successful. The agent only needs to adjust their approach and response if the developer complains about the outcome.

For example (a stable fact that only explains). The agent explains how ext4 finds a file and says that the root directory is always inode 2. `[Experience]` is enough, because the fact has stayed the same since ext2 and appears in every ext4 reference, so memory is usually right. A wrong detail here misleads one explanation and changes no decision.

<!-- For example (a mistake that is not easily visible).  -->

For example (an irreversible decision). The developer asks which laptop to buy, and adds a constraint: the budget allows one laptop, so a wrong choice cannot be undone. This is the opposite of coding. A wrong claim about an API fails the build within seconds and costs one edit. By contrast, a wrong claim about a laptop fails nothing before the purchase, and the failure costs the whole price. So every claim the choice rests on needs the best evidence available, `[Documented]` or `[Observed]`, even a stable one such as "the RAM on this model is soldered and cannot be upgraded".

The same example with a volatile fact: the agent remembers that a model cost about 25 million VND. That price is `[Experience]` from data at least months old, so it MUST NOT enter the comparison. The retailer's product page, read today, gives `[Documented] (2026-09-26)`. If the comparison is reused 7 days later, the price is re-checked before the purchase, because retail prices change weekly.

For example, the developer asks: “How much RAM do I need for my workload?”

The agent knows from memory that 16 GB is usually enough for development. That is `[Experience]`, so it must not be presented as the basis for the recommendation, because training data never held the developer's machine, so memory can only guess its workload. By contrast, measuring it takes a few commands.

Instead, the agent measures the developer's actual workload: Windows uses 4.2 GB at idle, the IDE uses 1.8 GB, the game engine uses 5.6 GB, and the agent uses 2.1 GB while the project is open. The measurements are `[Observed]`. The agent can infer that the current workload requires about 13.7 GB, and that 16 GB leaves little headroom. That conclusion is `[Inferred]`.

If the agent also checks the official system requirements for the IDE and game engine, those requirements are `[Documented]`. They can support the decision, but they do not replace measuring the actual workload.

Therefore, the answer should distinguish the evidence:

> `[Observed]` Your current workload uses about 13.7 GB of RAM under this test scenario.
>
> `[Documented]` The engine's official requirements specify X GB for this workload.
>
> `[Inferred]` 16 GB leaves limited headroom, while 32 GB provides substantially more room for background applications and workload variation.

The agent must not turn the general claim “developers need 32 GB” into `[Observed]` merely because it sounds plausible. The required RAM depends on the workload being evaluated.

Why: in prose, a recalled fact reads exactly like a checked one. Training rewards a plausible next token, not a true one, so a hallucination appears exactly where a pattern is strong and a fact is rare. The label makes the weak claims visible before a decision rests on them. Checking a claim costs tool calls, time, and context, so the effort goes only where a wrong claim costs more than the check.
