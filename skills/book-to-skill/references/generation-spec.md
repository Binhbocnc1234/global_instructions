# Generation and Update Specification

Read this file completely for Full Conversion, Generate from Prior Analysis, or
Update/Fold-in.

## Contents

- Step 7: Generate source-grounded guidance
- Step 8: Generate supporting files
- Step 9: Generate the master `SKILL.md`
- Step 9.5: Preserve raw source extracts
- Step 10: Clean temporary workspace and report
- Update/Fold-in workflow

## Step 7 — Generate source-grounded guidance

### Governing rule: behavioral completeness

Do not impose a token minimum, maximum, item count, or chapter-size class on generated
guidance. Include every source-grounded instruction whose removal could materially change
the agent's decision, action, output, constraint handling, or validation. Compress wording;
never compress away required behavior.

Omit narrative, repetition, motivational prose, and examples that add no new operational
information. Preserve all material:

- triggers and applicability conditions;
- required context and prerequisites;
- procedures, algorithms, and ordered steps;
- decision rules, trade-offs, thresholds, and defaults;
- constraints, prohibitions, exceptions, and safety warnings;
- failure modes and corrective actions;
- verification and acceptance criteria;
- source-specific definitions required to execute the guidance correctly.

The stopping condition is semantic, not numeric: guidance is complete only when removing
any remaining source instruction would not materially affect agent behavior.

Use `DEPTH` only to control supporting explanation and worked examples. Never let
`DEPTH=reference` remove a material instruction, exception, constraint, or verification
rule.

### Organize by capability

Use the source chapter structure to discover content, but organize generated files by the
capability or task the agent must perform. A guide may combine material from several source
chapters; one source chapter may produce several guides.

Before writing, inventory all material instructions in the relevant source sections. For
each inventory item, record its destination guide and source locator. Do not silently drop
an item. Split a guide when it contains independently loadable tasks, not to satisfy a token
limit.

Create `$SKILLS_HOME/<skill_name>/guides/<capability-slug>.md`:

```markdown
# <Capability or Task>

## Use When
<Conditions that trigger this guidance.>

## Required Context
<Information and prerequisites the agent must obtain before acting.>

## Instructions
1. <Concrete action.>
2. <Concrete action.>

## Decision Rules
- If <condition>, do <action> because <reason>.

## Constraints
- <Rule, prohibition, exception, threshold, or default.>

## Failure Modes
- **<Symptom>** — Cause: <cause>. Correction: <action>.

## Verification
- <Observable evidence that the result is correct.>

## Required Terms
- [<Term>](../glossary.md#term) — <why its precise meaning matters here>.

## Source Locators
- <Source name>, Chapter/Section/Page <locator>.
```

Omit empty sections. Include code, formulas, tables, or worked examples only when they
change execution or verification. Define a required term inline when the agent cannot
follow the instruction safely without it; otherwise link to `glossary.md`.

### Coverage audit

After writing all guides, compare them against the instruction inventory. Every material
item must be represented in a guide. If an item is intentionally excluded as non-operational
context, record that decision in the working analysis; do not add it merely to appear
complete. Re-read ambiguous source slices before finalizing.

## Step 8 — Generate supporting files

### `glossary.md`

Include a term only when at least one condition applies:

- it is uncommon, domain-specific, an acronym, or not broadly standardized;
- it has multiple accepted meanings or is commonly confused with another term;
- the author redefines, narrows, or extends its conventional meaning;
- its exact definition changes how an instruction is executed;
- it names a source-specific framework, classification, threshold, or artifact;
- misunderstanding it could produce a materially incorrect result.

Do not include a broadly understood term when the source uses its conventional meaning and
defining it would not change agent behavior. Do not rely solely on an assumption that a
model was trained on a term; evaluate ambiguity and behavioral impact.

Format entries as:

```markdown
## <Term>
**Meaning**: <precise source-grounded definition>.
**Operational significance**: <how this meaning affects behavior>.
**Source**: <chapter/section/page>.
```

### `source-map.md`

Map every generated guide to its source evidence:

```markdown
| Guidance | Source locators |
|---|---|
| [Perform verification](guides/perform-verification.md) | Ch 4 §§4.2–4.6 |
```

Use stable section or page locators when extraction provides them. This file preserves
traceability when guide organization differs from book organization.

### `patterns.md`

Collect reusable techniques, algorithms, and design patterns without duplicating complete
guide instructions. For each pattern record when to use it, its essential mechanism,
trade-offs, and links to the guides that operationalize it.

### `cheatsheet.md`

Capture the author's decision logic as compact decision rules, trees, trade-off matrices,
thresholds, defaults, and diagnostic smells. Avoid definitions already in the glossary and
procedures already in guides. Keep it concise by removing duplication, not by imposing a
token cap.

## Step 9 — Generate the master SKILL.md

Keep the master file compact because it is always loaded when the generated skill triggers.
Put routing and the highest-value decision rules first; move complete operational guidance
to `guides/`.

```markdown
---
name: <skill_name>
description: "Source-grounded operational guidance from <Title> by <Author>. Use when <key capabilities and triggers>."
---

# <Title>

## How to Use This Skill

- Route task questions through the Capability Index.
- Read every guide relevant to the requested task before answering or acting.
- Read linked glossary entries when a guide requires an exact term.
- Use `source-map.md` and targeted raw extracts to verify ambiguous or precise claims.
- State when the retained guidance is insufficient; do not fill source-specific gaps from
  general model knowledge without clearly labeling that distinction.

## Core Decision Rules

<Only cross-cutting rules needed for routing or most tasks.>

## Capability Index

| Capability | Use when | Guide |
|---|---|---|
| <Capability> | <Trigger> | [guide](guides/<slug>.md) |

## Topic Index

- **<Topic>** → [<guide>](guides/<slug>.md)

## Supporting Files

- [glossary.md](glossary.md) — uncommon, ambiguous, or operationally significant terms
- [patterns.md](patterns.md) — reusable techniques and trade-offs
- [cheatsheet.md](cheatsheet.md) — compact decision aids
- [source-map.md](source-map.md) — guidance-to-source traceability
- `raw-source-extract/manifest.json` — local retained-source inventory

## Scope and Limits

This skill contains source-grounded operational guidance, not a complete reproduction of
the source. Verify ambiguity against retained extracts and identify unsupported gaps.
```

Ensure every guide appears in the Capability Index and every important query term routes to
at least one guide.

## Step 9.5 — Preserve raw source extracts

Run:

```bash
PRESERVE_SCRIPT="$(dirname "$SCRIPT_PATH")/preserve_raw_extract.py"
"$PYTHON_BIN" "$PRESERVE_SCRIPT" \
  --workdir "${BOOK_SKILL_WORKDIR:-$(python -c 'import tempfile; print(tempfile.gettempdir())')/book_skill_work}" \
  --skill-dir "$SKILLS_HOME/<skill_name>"
```

This creates or updates `raw-source-extract/` with content-hashed source text,
`manifest.json`, and a cache-style `.gitignore`. Treat raw extracts as secondary evidence.
Search and read only the relevant slice; never load them wholesale.

Raw extracts may contain copyrighted or private material. Never force-add, publish, or
package them without explicit authorization and the necessary rights.

## Step 10 — Clean temporary workspace and report

Delete only the temporary extraction workspace after raw preservation succeeds. Report the
generated `SKILL.md`, guides, glossary, patterns, cheatsheet, source map, and retained raw
sources. Report actual sizes as observations, not compliance targets.

## Update/Fold-in Workflow

1. Read the existing `SKILL.md`, all affected guides, supporting files, and source map.
2. Inventory every material instruction in the new sources.
3. Merge each instruction into the capability guide it changes; create a new guide when no
   existing capability fits. Never overwrite silently or discard conflicting guidance.
4. Reconcile conflicts by preserving source attribution and stating version or context
   differences.
5. Update selective glossary entries, patterns, decision aids, capability/topic indexes,
   and source locators.
6. Run the coverage audit against both existing and new instruction inventories.
7. Preserve new raw extracts, clean temporary output, and report changed guides and sources.
