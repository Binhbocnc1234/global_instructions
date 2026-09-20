---
name: how-to-comment-in-csharp
description: Rules for writing C# comments and XML doc comments - which tags are allowed, and what a comment must say. Use when writing or editing any comment or /// block in a .cs file, reviewing comments, or when a class, method, property, event, or exception type is added and needs documenting.
---

# How to Comment in C#

A comment earns its place by carrying information the code cannot. Restating the signature in English is noise that rots as soon as the code changes.

**Goal: a doc comment must read as plain prose in raw text.** Both the developer and the agent read these as raw `.cs` files far more often than as rendered IDE tooltips, so the tag set is kept small on purpose. If a comment is hard to read with the tags still visible, it has too many tags.

## Allowed tags

Only these five. Anything else is out of scope for this project.

| Tag | Use for | Example |
|---|---|---|
| `<summary>` | The one required block on every documented member. | `/// <summary>...</summary>` |
| `<para>` | A new paragraph inside a summary. This is the line/paragraph break. | `/// <para>Second point.</para>` |
| `<c>` | A short code word inline: a symbol that does not resolve as a `cref`, a literal, a keyword. | `<c>runInBackground</c>` |
| `<see cref="X"/>` | A reference to a type or member that the compiler can resolve. | `<see cref="GameOverException"/>` |
| `<list>` | Two or more conditions, steps, or rules that must be read as separate items. | see below |

### `<see cref>` vs `<c>`

Prefer `<see cref>`. It renders as a clickable link in the IDE and the compiler warns (CS1574) when the target is renamed or deleted, so the comment cannot quietly go stale. `<c>` is plain text and has neither property.

Use `<c>` only when a `cref` will not resolve from the file's namespace and `using` directives, and adding a `using` purely for a comment is not worth it. Naming the symbol in prose without any tag is also fine when it reads better.

### `<list>` shape

```csharp
/// <list type="number">
/// <item>the first cause to arrive wins;</item>
/// <item>the queue is cancelled before anyone is notified.</item>
/// </list>
```

Use `type="number"` for ordered steps or rules, `type="bullet"` for unordered points.

`<list>` is the noisiest allowed tag in raw text, so reach for it last. Two items belong in a sentence joined by "and". Use `<list>` only from three items up, and only when they must be scanned separately rather than read as a flowing sentence.

## Not allowed

* **`<br>` / `<br/>`** - not a C# documentation tag. The documented set is `<c>`, `<code>`, `<example>`, `<exception>`, `<include>`, `<inheritdoc>`, `<list>`, `<para>`, `<param>`, `<paramref>`, `<permission>`, `<remarks>`, `<returns>`, `<see>`, `<seealso>`, `<summary>`, `<typeparam>`, `<typeparamref>`, `<value>` (Microsoft, "Recommended XML tags for C# documentation comments"). Visual Studio and Rider happen to render `<br/>` in tooltips because they process some HTML, but other doc pipelines are not required to. **Use `<para>` to break text.**
* **`<param>` and `<returns>`** - banned. They restate the signature, which the reader already has one line below, and they turn a three-line comment into a wall of tags that is painful to read as raw text. If a parameter or a return value carries a constraint the type does not express - a unit, an allowed range, what `null` means - say it in `<summary>` as a normal sentence: "Positions are board indices, not ranks." Never re-open the argument list in tag form.
* `<exception>`, `<value>`, `<typeparam>`, `<remarks>`, `<seealso>` - same reason. Anything worth saying goes in `<summary>`, in prose.
* `<code>` blocks - a doc comment is not the place for a sample. If callers need one, write a test.
* Raw HTML of any kind, including `<b>` and `<br>`, and markdown syntax such as `**bold**` or backticks. Doc comments are XML, and both wreck raw-text readability.

## What a summary must say

**Lead with why the member exists, not what it is.** The name and signature already say what it is. A summary that starts "Gets or sets..." or "Handles..." has said nothing.

Concretely, a summary should carry at least one of:

* the reason the member exists at all - the problem it solves, or what would break without it;
* an invariant callers can rely on, stated at the source so consumers never re-check it;
* a constraint on how it may be used, and the consequence of getting it wrong;
* a non-obvious ordering, lifetime, or threading requirement;
* why the obvious simpler approach was not taken.

If none of those apply, write no comment. A member whose name fully explains it is well named.

### Example

```csharp
/// <summary>
/// One-way latch: false until the match ends, then true for the rest of the match.
/// The setter drops a repeated assignment, so PropertyChanged fires exactly once and only ever announces true.
/// Subscribers must not re-read this to confirm the notification.
/// </summary>
public bool IsGameOver { get; private set; }
```

That comment gives the reader an invariant plus a rule. Compare the version that says nothing:

```csharp
/// <summary>
/// Gets a value indicating whether the game is over.
/// </summary>
```

## Style

* One blank-free `<summary>` block directly above the member, no blank line between them.
* **Do not hard-wrap a sentence.** One sentence goes on one `///` line however long it runs; a sentence of two hundred characters is normal. Breaking a sentence across lines to hit a column limit makes it unsearchable with grep and turns a one-word edit into a multi-line diff.
* A paragraph of several sentences becomes several `///` lines, one per sentence. Editors soft-wrap; the file should not.
* Plain sentences, sentence case, full stops. No shouting.
* An ALL-CAPS lead-in is reserved for a standing warning that must not be missed - `NOT MAINTAINED`, `DO NOT CALL FROM`. Never use one for ordinary explanation.
* Write for the next reader, not for a spec document. "so the socket never closes" beats "to ensure proper resource lifecycle management".

## Inline `//` comments

Use them for a decision, never for a translation of the next line.

```csharp
// WRONG - says what the line already says

// Lock the cursor
Cursor.lockState = CursorLockMode.Locked;

// RIGHT - explains a gameplay or engine constraint that the code alone cannot show
// Keep the cursor locked while aiming so losing focus for one frame cannot
// turn the next mouse movement into an accidental camera jump.
if (isAiming)
{
    Cursor.lockState = CursorLockMode.Locked;
}
```

## Checklist before finishing a comment

1. Does it use only `<summary>`, `<para>`, `<c>`, `<see cref>`, `<list>`? No `<param>`, no `<returns>`, no exceptions to this.
2. Read it as raw text with the tags visible. Does it still read as prose?
3. Does the first sentence explain why the member exists, rather than restating its name?
4. Could a reader delete the comment and lose nothing? Then delete it.
5. Does every `<see cref>` resolve, so a rename will be caught?
6. Would this still be true after a plausible refactor, or does it pin down today's line numbers and call order unnecessarily?
