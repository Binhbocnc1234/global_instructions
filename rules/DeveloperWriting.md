# DeveloperWriting

Summary: How must developer-facing text select information and wording? Relevance and vocabulary rules for replies and files, under Explanation.
Why: the developer needs the same presentation choices in a reply and a document.

These rules belong to [Explanation](Explanation.md). Apply the shared constraints in [Communication](Communication.md) too. A file's primary reader determines its presentation; another reader may still use the same canonical file.

## Developer-Facing Relevance

When to apply: writing a reply or file whose primary reader is the developer.

Noise is content whose reading and follow-up cost exceeds the value it gives the developer.

In a reply, lead with the answer or completed outcome after the Vocabulary and Task type lines of [Final Reply Format](Leader.md#final-reply-format). A file follows its applicable document structure.

Include information that answers the request, supports the conclusion, explains a necessary limitation, or enables the next required action.

Examples are valuable when they make an abstract point concrete. Keep an example when it shows an application, boundary, or consequence that the explanation alone does not make clear.

MUST NOT repeat the same information through prose, bullets, pseudocode, a trace, and a closing summary. Each representation must add something the reader needs.

When delivering a document in a reply, link to it. Do not repeat its contents unless the developer requests a summary or needs a specific finding immediately.

End a reply with a question only when its answer blocks the requested work. Do not offer additional work merely to give the reply an ending.

Before sending, remove sentences whose deletion preserves the answer, necessary evidence, useful examples, limitations, and required actions.

For example — explanation:
Request: "What does rounding to whole percentages mean?"
Good: "The displayed value changes in 1-percentage-point steps. For example, 49.2% and 49.4% both display as 49%."
The example stays because it shows the precision the display hides.

For example — document delivery:
Request: "Record this finding in the project."
Good: `Recorded the finding and its measurement limits in [MeasurementResults](MeasurementResults.md). Committed as abc1234.`
Noise: repeating the document's table of contents, recounting the edits, explain why agent create new file and offering to implement another feature.

Why: the developer needs enough information to understand and act. Unnecessary content costs reading time without adding understanding.

Do not defer authorized work merely because the developer has not repeated "go". When the request already supplies the decision and the scope, finish that work in the same turn.

For example, the developer decides to rename a word that has two meanings, then asks whether another project needs the same change. The agent finds the word there too, in the labels of the app's buttons, and already has a recommended new name. The goal decides the change, and only the name is open, so the agent renames the labels with its recommendation in the same turn and names that choice in the reply. If the developer prefers another name, reverting one commit is enough. By contrast, when the options change what the product does, such as removing the buttons instead of renaming them, the decision is unmade and the agent asks first.

Some other examples:

**Example 1:**

**Request:** “I remember this project store the game icon to somewhere. Find it.”

**Good reply:**
> The active game icon is `assets/UI/Shared/Source/icon.png`.

**Bad reply:**
> The game icon is `assets/UI/Shared/Source/icon.png`. It is 1254 × 1254 pixels. `project.godot` references it through `config/icon`. The Android presets have empty launcher-icon settings. There are also older drafts in `RawAssets/other/`, generated icons under `android/build/res/`, and an unused default `icon.svg`.

---

**Example 2:**

**Request:** “Make the black divider wider. Don’t adjust it yourself; give me the constant to change.”

**Good reply:**
> `[Observed]` Increase `SEGMENT_DIVIDER_WIDTH_PIXELS` in `HealthBar.gd:13`.

**Bad reply:**
> The constant is `SEGMENT_DIVIDER_WIDTH_PIXELS`, currently `1.0`.
> ```gdscript
> const SEGMENT_DIVIDER_WIDTH_PIXELS: float = 1.0
> ```
> Each divider stays centred on its health boundary. The bar is 83.2 pixels wide, so at 2000 health each segment is approximately 4.2 pixels wide. Try 1.5–2.0. You can also change `SEGMENT_DIVIDER_COLOR`, declared immediately below it.

---

**Example 3:**

**Request:** “Proceed with the remaining verification.”

**Good reply:**
> `[Observed]` The editor type check passed. The packaged build remains unverified. The execution log is `tmp/typecheck-07/typecheck.log`.

**Bad reply:**
> Verification passed. See `chatInputCompletions.ts`.

The source file does not establish which check ran or whether the packaged build was verified.

---

**Example 4:**

**Request:** “Continue fixing the .NET dialog and DotRush activation.”

**Good reply:**
> The fixes are saved but need activation. Log out and back in, then run `Developer: Reload Window` in MonkeyVsAlien.

**Bad reply:**
> Fixed. The .NET environment variables are now in `~/.profile`, and DotRush’s identifier is stored under `extensionsIdentifiers/disabled` in the workspace state.

The bad reply omits the actions needed before the developer sees the fix.

The same relevance rule applies to reviews and risk reports:

For example: If developer request agent to review project, and you find that project is already good(following coding practices, documentation and developer's rules) Agent should say "There is no problem" instead of specify noise problem.

This is also apply when review a skill

For example: a small dead code that changes nothing at runtime. "`Entity.cs` declares a field that no code read it" True, and worth nothing: the property costs no behaviour, no memory, and no confusion until someone edits that class.

For example: "The variable `users` could be renamed to `userList`". If no project rules require it, it's just noise

For example: A game mechanism that is not broken. "ActionManager.AfterActionResolve skips a dead listener with a bare continue; add a Debug.Log there." Nothing malfunctions, and anyone debugging that path is already reading the loop. The developer spends time on a proposal that prevents no failure.

Repays — a silent fallback. "`public GameObject prefab` is not assigned but the code supress the error instead of letting error happen" or "using `var` in C#". It violates rules and you can fix it without developer permission

Repays — developer secret commited to Github, or a security risk

## Developer Vocabulary and Direct Phrasing

When to apply: writing a reply or file whose primary reader is the developer.

Use the [developer profile](../AGENTS.development.md#about-developer) to select vocabulary, detail, and examples. This does not change the shared evidence requirements.

Prefer the standard term of the field over jargon borrowed from another field. For dependencies, write `depends on` and `depended on by`, not `outgoing` and `incoming`, because `outgoing` has several unrelated meanings.

Prefer `Open Unity Editor`, `Click Run All`, and `Result: all tests pass` over conversational sequencing such as `First you need to` or `Then you should`.

Why: standard terms support lookup, while direct phrasing lets the developer identify the action or result.
