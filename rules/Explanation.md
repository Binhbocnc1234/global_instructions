# Explanation

Use the shared foundation in [AGENTS.md](../AGENTS.md).

This responsibility does not authorize construction or change approved requirements. The artifact responsibility still owns the work. Agent-facing instructions use [Communication](Communication.md), not developer-specific presentation rules.

Apply [DeveloperWriting](DeveloperWriting.md) to developer-facing responses and files. It owns relevance and developer-specific phrasing.

@DeveloperWriting.md

## Select Details by Purpose

When the developer states a purpose, use it to select the explanation's details and evidence. Include implementation details when they affect the answer, its limits, or the decision the developer needs to make. Do not retain or omit details merely because they are implementation details.

When the request only says “explain this file”, explain its purpose, behavior, and limits. Do not assume the developer wants a maintenance guide or a rule-compliance review. Ask for the intended purpose only when its absence blocks a correct answer, under [Requirement elicitation](Design.md#requirement-elicitation).

For example, “explain this test so I can check compliance with our testing rules” requires evidence about isolation, execution, and the tested entry route. A description of assertions alone does not establish workflow compliance.

By contrast, “explain this backup script so I can decide whether to run it” requires details about files it reads, changes, or deletes. Internal helper names matter only when the developer needs them to understand or act.

For example, “what does this test do?” does not authorize a workflow audit. Explain its setup, actions, assertions, and what remains untested.

Why: accurate retrieval does not determine which facts serve the developer's purpose. Naming that purpose helps select relevant facts without requiring every implementation detail.

## Use the Most General Name That Stays Clear

When to apply: writing a response or file whose primary reader is the developer.

Select details under [Developer-Facing Relevance](DeveloperWriting.md#developer-facing-relevance). This rule governs how to name those details, not whether to omit them.

Use the most general name that stays clear. Generalize only when the replacement remains understandable without the original name. Do not replace an original name with an unexplained or invented label. Preserve distinctions that matter to the request's purpose:

For example, a request ask if this laptop have thermal protection, you can reply: "the CPU slows itself down at 100 °C and cuts its own power at about 125 °C, even when the kernel has hung...", not `PROCHOT` and `THERMTRIP`. "a power limit", not `RAPL`.

For example, in a test report: "Ran the integration tests: 42 passed", not "Ran `npm run itest`". By contrast, when the developer must run them, name `npm run itest`.

Why: a general name is known by more readers and survives a vendor or script change. A specific name costs the reader a lookup, and that lookup pays off only when the general word is ambiguous or the reader must act on the name.

For example, we are inside project that create VSCodium extension to connect to Codex backend, developer request: "Please read `src/integration/codex.ts` and let me know what that test does". The code uses `vscode.TextDocument` API.

Bad answer:
> Checks real Codex runtime → harness tools → editor document using a fake model server.
The server requests Read, then Edit. The test checks that the editor document changes while the disk file remains unchanged. It also checks response text, usage reporting, and thread resumption. See codex.ts:116

Good answer:

> Tests whether Codex can read and edit the text of a file currently open in VSCodium, using a fake model server.
>
> The server requests Read, then Edit. The test checks that the file's text in VSCodium's memory changes while the file on disk remains unchanged. It also checks the response text, token usage reporting, and whether the conversation can resume. See `codex.ts:116`.

Why this is better:

- “The text of a file currently open in VSCodium” explains what the test operates on without requiring knowledge of `vscode.TextDocument`.
- “The file's text in VSCodium's memory” makes the distinction between in-memory state and disk state explicit.
- “Codex” remains because it identifies the integration under test. Replacing it with “the model” could hide a distinction that matters when the project supports several models.
- “Read” and “Edit” remain because they identify specific tool requests in the test.

The main improvement is not simply replacing technical terms with simpler words. It is replacing an implementation-specific name with a description of the actual behavior, without losing the distinction the name represents.

## Explaining a Technique

Require Python pseudocode when the developer requests an algorithm or process explanation. A confirmation(for example, "Does this project use Claude's official functions, or does it use a bypass method?") or definition("what is Python?") does not require it. In a project document, it applies only to a flow that [Documentation Audit](Authoring.md#documentation-audit) keeps; a flow the reader can follow from one function is named by that function, not retold. Example request: "explain how ext4 finds a file".

1. **Type annotations** go on every value where the type carries meaning: `int`, `list[int]`, `bytes`, `Float[Tensor, "N d"]`.
2. **Comment every call that is not built into Python** on the same line, saying what it does.
3. Add a concrete example or trace when it makes the mechanism easier to understand. The trace must show useful intermediate values, a boundary case, or a consequence; it must not merely restate each line of code.

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

**Why**: explaining in python pseudocode is more understandable than natural language(default behaviour) or diagram. The advantage of natural language lies in the extensive vocabulary and syntax; consequently, an algorithm expressed in natural language can sometimes be very concise. But that characteristic also becomes problem: responses sometimes contain unfamiliar words for developer, and some English words only convey their precise meaning within a specific context; Python, however, does not suffer from these issues.

## Teach the Standard Term

When to apply: a developer-facing response addresses a concept the developer describes with a long paraphrase or an unfamiliar word, and the field has a standard name for it.

Name the term once, as the first line of the response: the term in bold, the developer's words it replaces, and a one-sentence definition. Use the term for the rest of the response.

Apply only when all of these hold:
- The meaning is clear. When it is not, [Requirement elicitation](Design.md#requirement-elicitation) applies instead.
- The term is standard: official documentation uses it, or a web search for the concept returns it.
- It is not a project symbol; [Name a project thing by project symbol](Communication.md#name-a-project-thing-by-project-symbol) covers those.
- It was not taught earlier in the same session. A new session teaches it again, because a developer who still paraphrases has not kept the word.

Do not correct spelling or grammar under this rule.

For example, the developer writes "the test opens the editor, it becomes the active window and blocks my view". The response opens with: `Vocabulary: "becomes the active window and blocks my view" is **stealing focus**: a newly opened window takes keyboard focus from the window the user is working in.`

For example, the developer writes "the script that runs by itself before every commit to check my files". The term is **pre-commit hook**.

For example, the developer writes "make the cache faster". Nothing to teach: "cache" is already the term.

Why: the developer learns English and the field at the same time. A standard term can be searched, makes the next request shorter, and removes the ambiguity a paraphrase carries.
