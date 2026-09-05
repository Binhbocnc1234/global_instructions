---
name: skill-creator
description: "Author a new agent skill, or restructure an existing one, in ~/.agents/skills. Use when the user says: create a skill, turn this workflow into a skill, this should be a skill, split a skill that grew too large, or fix a skill that does not trigger. Applies the house rules for layout, frontmatter, description writing, and validation."
---

# Skill Creator

Turn a repeated workflow into a skill the agent can find and follow correctly.

## Decide Whether a Skill Is the Right Container

Answer three questions before creating any file.

1. Does the work repeat? A one-off task does not need a skill.
2. Does an existing skill already own this? Check the skill list before writing anything. Instead of creating a near-duplicate skill, stop execution and propose developer a solution
3. Would a project document serve better? Project-specific facts (a schema, an architecture decision, a naming convention for one codebase) belong in that project's documentation, not in a skill that every project loads.

## Capture Intent

Ask only what changes the result. See the `ask` skill for the sufficiency rule that governs this.

Four questions matter for a skill specifically:

1. What does the skill enable the agent to do that it could not do reliably before?
2. When does it trigger? Name the actual phrases a user would type, not a paraphrase of the capability.
3. What does the output look like? A file, a report, a modified project, a decision?
4. Is the output objectively verifiable? This decides whether a behavior check (see below) is worth running later.

## Choose the Structure

Default: `SKILL.md` alone. Add a directory only when it earns its place.

| Directory | Add it when |
|---|---|
| `scripts/` | The same logic would otherwise be rewritten every run, or deterministic execution matters more than agent judgment. |
| `references/` | Guidance applies only in some modes or tasks, and loading it every time would waste context. |
| `assets/` | A file belongs in the output itself (a template, an image, boilerplate), not in the instructions. |

Layout rules, hard limits, and the progressive-disclosure model live in [SkillAnatomy](references/SkillAnatomy.md). Read it before laying out a skill with more than one file.

## Write the Description

The description is the entire triggering mechanism. The agent chooses a skill from its description alone, before any body text loads. Get this wrong and the skill never fires, or fires on the wrong requests.

Rules:

- State what the skill does and when it applies.
- Name the real trigger phrases, the words a user would actually type.
- Separate the skill from its neighbors with precise verbs, not with a sentence saying what the skill is not.

One worked pair:

- Bad: `description: Helps with documents.` Too vague to route on. Every document request now competes for this skill.
- Good: `description: Extract Word, PDF, PowerPoint, Excel and other documents into agent-readable Markdown. Use when the user attaches or points at a document and wants its contents read, extracted, summarized, or converted to Markdown.` States the capability and the trigger phrases together.

Full guidance, more pairs, and the discovery-check protocol live in [DescriptionWriting](references/DescriptionWriting.md).

## Write the Body

Write in imperative mood, addressed to the agent: "Read the reference," not "You should read" or "I will read."

Use `MUST`, `MUST NOT`, and `STOP` only for constraints where violating them breaks the skill or causes real harm. Sprinkling them on ordinary preferences trains the agent to ignore them.

Keep `SKILL.md` at or below 250 lines. When it would run longer, split by responsibility into `references/`, never by compressing prose or deleting comments.

One canonical owner per rule. If another skill already owns a rule (writing style, Markdown conventions, question-asking sufficiency), link to it instead of restating it. This skill does exactly that for three rules: style is owned by `asd-ste100`, Markdown and document rules by `documentation`, question sufficiency by `ask`.

Write everything in English, regardless of the skill's subject.

## Give Every Non-Obvious Rule an Example

This is a required rule, not advice.

Demonstration, using the script rule from this file:

- Vague version: "Add a script when it helps." The agent cannot tell when "helps" applies, so it either adds none or adds one per skill.
- Same rule with a good/bad pair: "Add a script when the same logic would otherwise be rewritten on every run. Bad: a script wrapping one `git status` call, which the agent can type faster than it can read the script. Good: `scripts/validate_skill.py`, which runs ten structural checks that would otherwise be re-derived and re-typed each time." Now the agent can compare its own case against a real one.

Exception: a rule that is fully self-evident from its own wording does not need an example. `The files always has fewer than 250 lines` or `Always reply in English regardless of prompt's language` needs no example.

## Install Location

Install every skill at `~/.agents/skills/skill-name/`, where `skill-name` is the folder for that particular skill. The folder name MUST match the frontmatter `name`.

Claude reaches this folder through the `~/.claude/skills` symlink. No copy step is needed.

- Git Bash: `/c/Users/binhb/.agents/skills/skill-name/`
- PowerShell: `C:\Users\binhb\.agents\skills\skill-name\`

## Validate Triggering, Then Behavior

Run these two checks in order. Fixing triggering after fixing behavior wastes the behavior check, because a description fix can change what the body needs to say.

### Step 1: Discovery Check

Give an agent the description alone, then two prompts:

1. **The miss.** A realistic request that must trigger the skill, in the phrasing the user would actually type.
2. **The near miss.** An adjacent request that a neighboring skill owns, which tests the boundary between the two descriptions.

Skip the unrelated-domain prompt. An agent does not load a skill whose subject is absent from the request, so that test passes by construction.

A miss on prompt 1, or the wrong skill on prompt 2, means the description needs work. Fix the description before touching the body. This check is cheap. Run it every time, for every skill.

Full protocol, including what each failure mode implies, is in [DescriptionWriting](references/DescriptionWriting.md).

### Step 2: Behavior Check

Run this only when the skill's output is objectively verifiable (see Capture Intent, question 4).

Give one subagent one realistic prompt, the skill, and the raw input. Never give it the expected answer.

This step does not run a baseline comparison, does not repeat runs, and does not aggregate a benchmark. That cost is not justified on this machine. The `skill-creator:skill-creator` plugin already provides the full evaluation loop if that is ever wanted.

### Validator Script

Run the structural validator against the finished skill folder:

```powershell
python .\.agents\skills\skill-creator\scripts\validate_skill.py <path-to-skill-folder>
```

It checks frontmatter, naming, file length, folder depth, and leftover placeholders. It does not check whether the skill makes good decisions; only the two checks above do that.

## Improve an Existing Skill

Rule: precision before addition. Narrow the existing guidance rather than accumulate new files or new rules.

Two anti-patterns to avoid:

- A teaching essay replacing runtime instructions. A skill instructs an agent mid-task; it does not need to explain background theory the agent already knows.
- Adopting another project's conventions wholesale, because they looked reasonable somewhere else. Match this user's house rules instead.

One observed failure justifies one narrow correction, not a new universal rule. If a skill missed a case, fix that case specifically. Do not generalize a single miss into a broad new constraint that will misfire on unrelated cases.
