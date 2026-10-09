# Skill Anatomy

Layout, hard limits, and when to split a skill into multiple files.

## Directory Layout

```text
skill-name/
├── SKILL.md              Required. Frontmatter plus body.
├── agents/
│   └── openai.yaml        Optional. metadata for Codex.
├── references/
│   └── Topic.md            Optional. Loaded only when the task needs it.
├── scripts/
│   └── helper.py            Optional. Executed, not read as instructions.
|   └── validator.py
└── assets/
    └── template.ext           Optional. Copied or adapted into output.
```

Supporting directories go exactly one level deep. Do not nest `references/foo/bar.md`; keep every supporting file directly inside its top-level directory.

## The Three-Level Progressive Disclosure Model

A skill discloses information in three stages, and each stage costs more context than the last:

1. **Name and description.** Always in context, for every skill, on every turn. This is what the agent uses to decide whether to load the skill at all. Keep it short and precise; see [DescriptionWriting](DescriptionWriting.md).
2. **`SKILL.md` body.** Loaded only when the skill triggers. This is where the working instructions live.
3. **Bundled resources** (`references/`, `scripts/`, `assets/`). Read or executed only when the current task actually needs that specific file.

A skill that puts everything in `SKILL.md` wastes context on every trigger, even for tasks that only need one mode. A skill that never uses `references/` for genuinely mode-specific content is usually a sign the skill is doing too much in one file, or doesn't need to be split at all. Match the split to actual task variation, not to file length alone.

## Hard Limits

| Item | Limit |
|---|---|
| `name` | 1 to 64 characters. Lowercase letters, digits, and hyphens only. MUST match the folder name exactly. |
| `description` | At most 1024 characters. |
| Supporting directories | Exactly one level deep. No nested subdirectories under `references/`, `scripts/`, or `assets/`. |
| `SKILL.md` length | At most 250 lines, under this house's file-size rule. |

The wider community norm for `SKILL.md` allows up to 500 lines. This house's stricter 250-line rule wins here; do not use the 500-line figure to justify a longer file.

### Provenance of the Numeric Limits

The 64-character `name` limit and the 1024-character `description` limit come from community consensus, specifically https://github.com/mgechev/skills-best-practices. They have not been confirmed against the normative specification.

The normative specification lives at agentskills.io. It states only that `name` and `description` are required fields; it does not itself state numeric length limits for them. Treat the 64 and 1024 figures as widely followed practice, not as a rule enforced by the spec itself. This distinction matters if a future skill needs to exceed one of these figures: nothing in the normative spec forbids it, but `scripts/validate_skill.py` still enforces the community numbers, because they are a reasonable and widely-followed ceiling.

## When to Split a Skill Into References

Split when `SKILL.md` would exceed 250 lines, or when a section only applies to one mode or one task variant and loading it every time wastes context.

Do not split preemptively. A skill with one mode and under 200 lines does not need a `references/` folder just because other skills have one.

### Worked Example: A Skill That Outgrew One File

A skill named `deploy-app` started as a single `SKILL.md` covering one deployment target. As the user added AWS, GCP, and Azure support, the file grew past 300 lines, most of it provider-specific credentials setup, CLI commands, and troubleshooting that only applied to whichever provider the user picked that day.

The fix was not to compress the prose. It was to recognize three genuinely separate modes and split them out:

```text
deploy-app/
├── SKILL.md
└── references/
    ├── Aws.md
    ├── Gcp.md
    └── Azure.md
```

`SKILL.md` kept the shared workflow and a short routing table: "user picks AWS, read `references/Aws.md`; GCP, read `references/Gcp.md`," and so on. Each reference stayed focused on one provider. The agent now loads only the one reference the task actually needs, and `SKILL.md` dropped back under 150 lines.

The signal that triggered the split was not line count alone. It was that most of the file's length existed to serve a choice the agent makes once per task (which provider), and the other two-thirds of the content was irrelevant to that choice every single time.
