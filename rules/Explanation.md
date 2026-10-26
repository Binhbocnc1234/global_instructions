# Explanation

Use the shared foundation in [AGENTS.md](../AGENTS.md).

Apply [DeveloperWriting](DeveloperWriting.md) to developer-facing replies and files. It owns relevance and developer-specific phrasing.

@DeveloperWriting.md

## Convention

When the request only says “explain this file”, explain its purpose, behavior, and limits. Do not assume the developer wants implementation details, a maintenance guide or a rule-compliance review. Ask for the intended purpose only when its absence blocks a correct answer, under [Requirement elicitation](Design.md#requirement-elicitation).

## Use the Most General Name That Stays Clear

When to apply: writing a reply or file whose primary reader is the developer.

Select details under [Developer-Facing Relevance](DeveloperWriting.md#developer-facing-relevance). This rule governs how to name those details, not whether to omit them.

Use the most general name that stays clear. Generalize only when the replacement remains understandable without the original name. Do not replace an original name with an unexplained or invented label. Preserve distinctions that matter to the request's purpose:

For example, a request ask if this laptop have thermal protection, you can reply: "the CPU slows itself down at 100 °C and cuts its own power at about 125 °C, even when the kernel has hung...", not `PROCHOT` and `THERMTRIP`. "a power limit", not `RAPL`.

For example, in a test report: "Ran the integration tests: 42 passed", not "Ran `npm run itest`". By contrast, when the developer must run them, name `npm run itest`.

Why: a general name is known by more readers and survives a vendor or script change. A specific name costs the reader a lookup, and that lookup pays off only when the general word is ambiguous or the reader must act on the name.

For example, we are inside project that create VSCodium extension to connect to Codex backend, developer request: "Please read `src/integration/codex.ts` and let me know what that test does". The code uses `vscode.TextDocument` API.

Bad answer:
> Checks real Codex runtime → harness tools → editor document using a fake model server.
The server requests Read, then Edit. The test checks that the editor document changes while the disk file remains unchanged. It also checks response text, usage reporting, and thread resumption.

Good answer:

> Tests whether Codex can read and edit the text of a file currently open in VSCodium, using a fake model server.
>
> The server requests Read, then Edit. The test checks that the file's text in VSCodium's memory changes while the file on disk remains unchanged. It also checks the response text, token usage reporting, and whether the conversation can resume.

Why this is better:

- “The text of a file currently open in VSCodium” explains what the test operates on without requiring knowledge of `vscode.TextDocument`.
- “The file's text in VSCodium's memory” makes the distinction between in-memory state and disk state explicit.
- “Codex” remains because it identifies the integration under test. Replacing it with “the model” could hide a distinction that matters when the project supports several models.
- “Read” and “Edit” remain because they identify specific tool requests in the test.

The main improvement is not simply replacing technical terms with simpler words. It is replacing an implementation-specific name with a description of the actual behavior, without losing the distinction the name represents.

## Explaining a Technique

Require Python pseudocode when the developer requests an algorithm or process explanation. A confirmation(for example, "Does this project use Claude's official functions, or does it use a bypass method?") or definition("what is Python?") does not require it. In a project document, it applies only to a flow that [Documentation Audit](Authoring.md#documentation-audit) keeps; a flow the reader can follow from one function is named by that function, not retold.

1. **Type annotations** go on every value where the type carries meaning: `int`, `list[int]`, `bytes`, `Float[Tensor, "N d"]`.
2. **Comment every call that is not built into Python** on the same line, saying what it does.
3. Add a concrete trace. The trace must show useful intermediate values, a boundary case, or a consequence; it must not merely restate each line of code.

Example request: "explain how ext4 finds a file".

```python
ROOT_INODE: int = 2 # ext4 always stores "/" in inode 2

def lookup(path: str, sb: Superblock) -> int: # sb: filesystem header read at mount time
    """Return the inode number of an absolute path."""
    ino: int = ROOT_INODE
    for name in path.strip("/").split("/"):
        entries: dict[str, int] = read_dir(ino, sb) # read_dir: parse the directory's data blocks into name -> inode
        ino = entries[name] # KeyError here is "No such file or directory"
    return ino

def inode_position(ino: int, sb: Superblock) -> tuple[int, int]:
    group: int = (ino - 1) // sb.inodes_per_group # which block group holds the inode
    index: int = (ino - 1) % sb.inodes_per_group # slot inside that group's inode table
    return group, index
```

Trace for `/home/a.txt` with `inodes_per_group = 8192` (example values): `ino = 2` → `read_dir(2)` finds `home -> 131073` → `inode_position(131073)` = `(16, 0)`, so the `home` directory is in group 16, slot 0 → `read_dir(131073)` finds `a.txt -> 131080` → return `131080`.

**Why**: explaining in python pseudocode is more understandable than natural language(default behaviour) or diagram. The advantage of natural language lies in the extensive vocabulary and syntax; consequently, an algorithm expressed in natural language can sometimes be very concise. But that characteristic also becomes problem: replies sometimes contain unfamiliar words for developer, and some English words only convey their precise meaning within a specific context; Python, however, does not suffer from these issues.

## Teach the Standard Term

When to apply: a developer-facing reply addresses a concept the developer describes with a long paraphrase or an unfamiliar word, and the field has a standard name for it.

Name the term once, as the first line of the reply: the term in bold, the developer's words it replaces, and a one-sentence definition. Use the term for the rest of the reply.

Apply only when all of these hold:
- The meaning is clear. When it is not, [Requirement elicitation](Design.md#requirement-elicitation) applies instead.
- The term is standard: official documentation uses it, or a web search for the concept returns it.
- It is not a project symbol.
- It was not taught earlier in the same session. A new session teaches it again, because a developer who still paraphrases has not kept the word.

Do not correct spelling or grammar under this rule.

For example, the developer writes "the test opens the editor, it becomes the active window and blocks my view". The reply opens with: `Vocabulary: "becomes the active window and blocks my view" is **stealing focus**: a newly opened window takes keyboard focus from the window the user is working in.`

For example, the developer writes "the script that runs by itself before every commit to check my files". The term is **pre-commit hook**.

For example, the developer writes "make the cache faster". Nothing to teach: "cache" is already the term.

Why: the developer learns English and the field at the same time. A standard term can be searched, makes the next request shorter, and removes the ambiguity a paraphrase carries.


## Evidence Labels

When to apply: a reply or a file states a claim that a decision, a conclusion, or code rests on (a load-bearing claim). Do not apply this rule to decisions whose mistakes fail loudly and quickly.

Four labels, from the strongest evidence to the weakest. The effort column is an estimate from typical tool calls, not a measurement. The last column is what the claim carries after its label, so the reader can check it without asking:

| Label | Basis | Effort to get it | What the claim carries |
|---|---|---|---|
| `[Observed]` | A command result, a GUI query, or a measurement the agent made in this session | 1 tool call and a few seconds for a file read. Minutes for a build, a test run, or a performance measurement. | The command, file, or measurement, as a link or a name |
| `[Documented]` | A published source: official documentation, source code, a specification, a paper, a vendor page | A search and a page read: 2 to 3 tool calls, under 1 minute, and a few thousand tokens of context per page | A link or a symbol |
| `[Inferred]` | Reasoning from premises that carry one of the two labels above. The more credible and widely accepted the premise, the more reliable the reasoning | The effort of its premises | Each premise with its own label, and the step from the premises to the conclusion. A proposal or a decision is an `[Inferred]` claim: its premises say why the choice serves the request, not only what it is |
| `[Experience]` | Agent memory from training, with no source checked in this session | None | Nothing |


MUST place the appropriate evidence label immediately before each claim covered by this rule, even when the claim names a command, cites a source, or explains its reasoning. Labels go in prose, not in code.

If you write "[Observed]" without providing supporting evidence, the developer will implicitly understand that it refers to information from the session. For example, "[Observed] The test run reports 42 passed"

Claims that share one source share one link and one label. For example: "[Documented]: Claim 1, Claim 2,...See this link: ...."

For example, request in game project: "How Effect system in this game work?"

```markdown
[Documented] Multiple Effect instances can coexist and their durations decrease simultaneously, but only the Effect with the greatest Strength takes effect. See `EffectContainer.ActiveEffect()` in [EffectContainer.cs:57](Scripts/Effects/EffectContainer.cs:57).
```

For example (an inference that hides its premises). After a system update, the developer's laptop battery ran out faster, and the agent wrote: "`[Inferred]` The update may be why the battery drains faster." Listing the premises shows the gap: `[Observed]` the battery started draining faster on the day the update was installed, `[Experience]` an update sometimes adds a background service, and nothing links the drain to the update. The agent did not read the power usage per app, so it reads that before sending the reply, or says the cause is unknown. Without the premises, the developer had to ask for the power usage per app in the next message.

For example (a decision that hides its premises). The agent proposed dropping old tool results from a resumed chat, and its only premise was their size. The decision needs the premises that the next request does not need them: what the resumed turn actually read, and how cheaply it can read that again.

A stronger label costs more effort, so checking every claim wastes the budget of the request. Give each claim the lowest label that the cost of being wrong allows: compare what the check costs with what a wrong claim costs. A stronger label is always allowed.

It is normal when evidence is unavailable — for instance, agent's brain doesn't have the fact, an undocumented API, closed-source(Claude and GPT model) or an unrecorded history(transaction logs, record of computer temperatures). Agent should not guess the fact

For example (a tool catches the mistake). The agent writes Python and recalls that `str.removeprefix` exists. This falls under the exception for mistakes that fail loudly and quickly: if the method is unavailable, the first run raises `AttributeError` within seconds, before any harm, and the fix is one edit. The reply does not need an evidence label for this decision.

For example (a tool catches the mistake). **Request:** “Copy and downscale the icon into `build/google-play` so I can upload it.”

**Good reply (hypothetical output):**
```markdown
[Observed] Created [app-icon-512.png](../build/google-play/app-icon-512.png): **512 × 512 PNG, 339 KB**.
```

**Bad reply (unnecessary detail, even with labels before the claims):**
```markdown
[Observed] I made a 512 × 512 copy at [app-icon-512.png](../build/google-play/app-icon-512.png).
[Observed] The original icon is 1254 × 1254 pixels and 1.46 MB.
[Observed] The new file is 512 × 512 pixels, a PNG with transparency, and 339 KB.
[Observed] I scaled the image down with a high-quality filter.
[Observed] The original had no transparency layer, so I added one; the image is still fully opaque.
[Observed] The original file in `assets/` is unchanged.
[Observed] Nothing was committed, because git ignores the `build/` folder.
```

The agent does not need to provide additional Evidence regarding Google Play policies or details about how the image was processed, as a developer can see within seconds whether the upload to Google Play was successful. The agent only needs to adjust their approach and reply if the developer complains about the outcome.

For example (a stable fact that only explains). Developer want to learn about how ext4 filesystem work,the explanation can say: "`[Experience]` ext4 stores the root directory in inode 2." Memory is enough here because a wrong detail misleads one explanation and changes no decision.

For example (an irreversible decision). The developer asks which laptop to buy, and adds a constraint: the budget allows one laptop, so a wrong choice cannot be undone. This is the opposite of coding. A wrong claim about an API fails the build within seconds and costs one edit. By contrast, a wrong claim about a laptop fails nothing before the purchase, and the failure costs the whole price. So every claim the choice rests on needs the best evidence available, `[Documented]` or `[Observed]`. For example, after checking the manufacturer's specification, write: "`[Documented]` The RAM on this model is soldered and cannot be upgraded," followed by the specification link.

The same example with a volatile fact: "`[Experience]` I remember this model costing about 25 million VND." This unverified price MUST NOT enter the comparison. By contrast, after reading the retailer's product page, write: "`[Documented]` The retailer lists this model at 25 million VND, checked on 2026-09-26," followed by the product-page link. If the comparison is reused 7 days later, re-check the price before the purchase.

For example, the developer asks: “How much RAM do I need for my workload?”

The reply can use the following format; the log path, requirement value, and example URLs stand for the evidence collected:

```markdown
[Observed] During ordinary work, RAM use was 4.2 GB for Windows, 1.8 GB for the IDE, 5.6 GB for the engine, 2.1 GB for the agent, 2.6 GB for a browser with 10 tabs, and 1.2 GB for a chat app and a music player, 17.5 GB in total. See `tmp/ram-measurements.txt`.
[Observed] During a build, the engine rose to 10 GB, so the total peaked at 22 GB.
[Documented] The game requirements specify 16 GB is minimum, 32GB for smooth experience. See [game requirements](https://example.com/requirements).
[Experience] When RAM is full, Windows moves memory pages to the paging file on disk, and reading them back is slower than reading RAM.
[Inferred] With 16 GB, even ordinary work does not fit, so Windows pages to disk all day, and builds and games slow down further. By constrast, With 32 GB, the build peak leaves 32 - 22 = 10 GB, so no measured situation pages to disk.
[Inferred] Free RAM helps only when a workload uses it, so the reason for 32 GB is the largest measured case
```

The agent must not turn the general claim “developers need 32 GB” into `[Observed]` merely because it sounds plausible. The required RAM depends on the workload being evaluated.

Why: in prose, a recalled fact reads exactly like a checked one. Training rewards a plausible next token, not a true one, so a hallucination appears exactly where a pattern is strong and a fact is rare. The label makes the weak claims visible before a decision rests on them. Checking a claim costs tool calls, time, and context, so the effort goes only where a wrong claim costs more than the check.