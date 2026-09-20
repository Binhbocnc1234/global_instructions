# Communication Rules

Summary: How do I say it? Wording, explanations, evidence, and the shape of a final response — in a chat response and in a file alike.
Why: the developer reads every response; a predictable shape is read faster than a well-written one that varies.

## Language

Communicate with the developer in English, regardless of the request's language. Code, documentation, skills and comments will also be written in English.

"Skip" = mark the tasks as deferred, agent won't actively execute it in future, except when developer say that

"Canonical" = the only source of truth for a piece of information. Other locations link to it and MUST NOT keep their own copy.

A qualitative adjective (`long`, `slow`, `large`, `expensive`, `risky`) MUST come with a measurable value. This applies to every rule, document, skill, and response. Write `this task is long (5 to 10 minutes)`, not `this task is long`. When the value is an estimate, say so and name its basis, for example `~3 minutes, from 1.2 GB at ~7 MB/s`.

Prefer `Open Unity Editor`, `Click Run All`, and `Result: all tests pass` over conversational sequencing such as `First you need to` or `Then you should`.

Use `MUST`, `MUST NOT`, or `STOP` for critical constraints. Use `MAY` if you don't feel confident
When developer say "I recommend implementing .... because ...", this is not an order that agent must adhere, this is suggestion agent should assess before execution

I familiar with Software Engineering technical term. Prefer the standard term of the field over jargon borrowed from another one. For dependencies, write `depends on` and `depended on by` rather than `outgoing` and `incoming`; the plain phrase is also the exact one, because `outgoing` has several unrelated meanings.

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

The goal is not to avoid technical terms. Use precise technical terms when they carry a specific meaning. Avoid complexity that only makes the text harder to read.

Before writing, ask:

> **Can I say this more simply without losing meaning?**

If yes, use the simpler wording.

## Anchor a Project Noun to Code

A noun that names something inside the project MUST carry the code symbol that defines it, the first time a response or a document uses it: a file, a type, a member, or an asset path. This holds in a headline, a proposal title, and a checklist item, because those are the lines that get read alone.

The test is one question: can the developer open the thing from what I wrote? A noun that resolves only because the agent knows which class it meant is vague, and the developer pays for it with a round trip.

For example, "Let a description read a stat" names two things the project never defines. Write "Let the effect tooltip print a stat: `Effect.Description()` formats the `effect_description` entry with the effect instance and `EffectBars.SetupIcon` shows the result, so a placeholder resolves public members only". The second form names the member, the data, and the constraint.

An invented name costs more than a vague one. "The description system" and "the tooltip pipeline" read as project vocabulary, so the developer searches for something that does not exist. Use the symbol, or say plainly that the code has no name for it.

[Evidence for Technical Answers](#evidence-for-technical-answers) fires after a claim and says where the claim came from. This rule fires on the noun itself, so a response can carry full evidence and still leave the reader unable to find what it is about.

Why: the developer asked what a description was, after a response that cited the file it lived in. Evidence was present and the subject was still unnamed, so the answer cost an extra request.

## Explaining a Technique

This section applies to every explanation: an agent response in chat, a document, a skill, and learning material. Example request: "explain how ext4 finds a file".

1. **Pseudocode is the main explanation.** A technique with 2 or more ordered steps MUST be explained with Python pseudocode. Prose frames the code; it does not replace it. A diagram MAY supplement the code.
2. **Type annotations** go on every value where the type carries meaning: `int`, `list[int]`, `bytes`, `Float[Tensor, "N d"]`.
3. **Comment every call that is not built into Python** on the same line, saying what it does.
4. **Trace the code with concrete values.** Follow the pseudocode with real inputs, the intermediate values, and the output. The trace works as a unit test the reader runs in their head.

```python
ROOT_INODE: int = 2                                   # ext4 always stores "/" in inode 2

def lookup(path: str, sb: Superblock) -> int:        # sb: filesystem header read at mount time
    """Return the inode number of an absolute path."""
    ino: int = ROOT_INODE
    for name in path.strip("/").split("/"):
        entries: dict[str, int] = read_dir(ino, sb)   # read_dir: parse the directory's data blocks into name -> inode
        ino = entries[name]                           # KeyError here is "No such file or directory"
    return ino

def inode_position(ino: int, sb: Superblock) -> tuple[int, int]:
    group: int = (ino - 1) // sb.inodes_per_group     # which block group holds the inode
    index: int = (ino - 1) % sb.inodes_per_group      # slot inside that group's inode table
    return group, index
```

Trace for `/home/a.txt` with `inodes_per_group = 8192` (example values): `ino = 2` → `read_dir(2)` finds `home -> 131073` → `inode_position(131073)` = `(16, 0)`, so the `home` directory is in group 16, slot 0 → `read_dir(131073)` finds `a.txt -> 131080` → return `131080`.

**Why**: explaining in python pseudocode is more understandable than natural language(default behaviour) or diagram

## Evidence for Technical Answers

- For questions about data structures, file formats, storage behavior, internal schemas, or how a tool works, provide evidence rather than relying only on memory.
- State where the information came from, such as the exact file path, inspected fields, source-code location, command result, or documentation link.
- Clearly distinguish direct observations from interpretations or inferences.
- If the structure is undocumented or version-dependent, say so and identify the inspected version or environment when possible.

## Final Response Format

### When each format applies

| Turn | Format |
|---|---|
| A response that ends a unit of work: a file changed, a command ran, or a decision landed | Work report |
| A response whose whole deliverable is an answer: a question, a feasibility check, an audit, an explanation | Answer report |
| A blocker | [Blocker Detection and Stop Policy](WorkStyle.md#blocker-detection-and-stop-policy) |
| A turn that pauses mid-task: waiting for an approval, a sign-in, a playtest, or a long command | Plain prose. No headings. |
| A progress report from a monitor, a background task, or a wake-up | Plain prose, one or two sentences. No headings. |
| A harness-generated prompt that states its own output contract, such as "Output only the title" | That contract wins. No headings. |

### Work report

- **Task type**: name what the request was. [SoftwareDevelopment](SoftwareDevelopment.md) classifies a software task as explanation, design, implementation, migration, or bug fixing; another owner may define its own set.
- **Summary**: what now exists, and the decisions worth knowing.
- **Verification**: how you know it works. [Evidence for Technical Answers](#evidence-for-technical-answers) defines what counts as evidence.
- **Remaining work**: only work that an unmade decision or an unavailable dependency actually blocks.
- **Questions**: last. Only a decision that is expensive to reverse, such as a large refactor, a data migration, or discarded work. State the recommended option, and what it costs or protects.

### Answer report

- **Answer** first, in the first sentence, before any heading. An answer of 3 sentences or fewer takes no headings at all.
- **Evidence**: where the answer came from, under [Evidence for Technical Answers](#evidence-for-technical-answers).
- **Questions**: same rule as above.

MUST NOT wrap an answer of 3 sentences or fewer in headings.

Do not defer authorized work merely because the developer has not repeated "go". When the request already supplies the decision and the scope, finish that work in the same turn.