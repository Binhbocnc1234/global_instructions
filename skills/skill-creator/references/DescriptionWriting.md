# Writing the Description

The description is a routing rule, not documentation for a human reader. The agent reads it, alone, before any other part of the skill loads, and decides whether this request belongs to this skill. Write it in the language a real request would use, not in the language a manual would use.

The failure mode is the miss. A skill that does not load when it should is invisible: the agent answers from its defaults, the user sees a plausible answer, and nothing reports that a skill was skipped. Write every description against that failure.

## What Belongs in a Description

- What the skill does.
- When it applies, in the words a user would actually type.

What does not belong: implementation detail, the full list of supported modes, marketing language, or anything that only matters once the skill has already been loaded. That belongs in the body.

## Good/Bad Pairs

### Pair 1: Unity Test-Writing Skill

- Bad: `description: Helps write tests for Unity projects.`
  Misses. "Helps write tests" does not match how a request actually sounds: "write a test for PlayerController," "add unit tests for the inventory system," "this class has no test coverage." A description built from a paraphrase of the capability, instead of the actual trigger phrases, fails to match real requests.

- Good: `description: Write and run Unity Test Framework tests (EditMode and PlayMode) for C# game code. Use when the user asks to add test coverage, write a unit test for a class or system, or verify behavior with an automated test in a Unity project.`
  Names the concrete framework, both test modes, and the phrases ("add test coverage," "write a unit test") a request would actually contain.

### Pair 2: 2D Sprite Pipeline Skill

- Bad: `description: For working with sprites and images.`
  Misses. A category label carries no trigger phrase. "Fix the pixel-art import settings," "pack these frames into an atlas," and "slice this spritesheet" share almost no vocabulary with "working with sprites and images," so none of them reliably reaches the skill.

- Good: `description: Slice, pack into atlases, and configure import settings for 2D game sprites in Unity. Use when the user asks to set up a sprite sheet, pack a texture atlas, fix pixel-art import settings, or slice a spritesheet into individual frames.`
  States the concrete operations and repeats the phrases a request would contain. Each operation is its own entry point.

### Pair 3: Two Skills Competing for One Request

- Bad: `description: Create, find, and manage agent skills.`
  Collides with `find-skills`, whose job is locating and installing a skill that already exists. A request like "is there a skill for X" now matches two descriptions equally well, and the choice between them is a coin flip.

- Good: `description: Author a new agent skill, or restructure an existing one, in ~/.agents/skills. Use when the user says: create a skill, turn this workflow into a skill, this should be a skill, split a skill that grew too large, or fix a skill that does not trigger.`
  Resolves the collision by scoping the verb. "Author" and "restructure" claim the writing case; the discovery case never matches these phrases, so `find-skills` keeps it without needing an exclusion. Precise verbs separate neighboring skills better than a sentence saying what the skill is not.

## The Discovery Check Protocol

Run this check every time a skill is created or its description changes. It is cheap: one agent turn, no file writes, no side effects.

### Setup

Give a fresh agent instance:

- The skill's `name` and `description` only. Not the body. Not the references.
- Two prompts, run one at a time or listed together and judged individually.

### The Two Prompts

1. **The miss.** A realistic request that should load this skill, in the phrasing a user would actually type, not a paraphrase of the capability. This prompt detects the failure that matters: the skill exists and stays asleep.
2. **The near miss.** A request that sounds adjacent but belongs to a neighboring skill in this user's skill set. It tests the boundary between two descriptions that could each claim the request.

A prompt from a clearly unrelated domain is not worth running. An agent does not load a skill whose subject is absent from the request, so that test passes by construction and buys nothing.

### Reading the Result

- **Prompt 1 does not trigger the skill.** The description is too narrow, or it uses vocabulary the target user would not type. Fix: rewrite the trigger phrases using words pulled from how the user actually asks, not from how the skill's author thinks about the problem internally.
- **Prompt 2 loads the wrong skill of the two.** The two descriptions overlap. Fix: sharpen the verbs and the trigger phrases on both sides until each request has one obvious owner, as in Pair 3 above.
- **Both pass.** The description is ready. Move to the behavior check only if the skill's output is objectively verifiable; otherwise the skill is done.

Fix the description and rerun the same prompts before touching `SKILL.md`'s body. A body fix cannot repair a routing failure; the agent never gets that far.
