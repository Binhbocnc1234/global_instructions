---
name: agent-improvement
description: Review completed agent work and propose durable updates to instructions, skills, documentation, hooks, or automations when a reusable lesson was found. Use when the user asks for a retrospective or durable agent workflow update.
---

# Agent Retrospective

Use this skill to turn repeated workflow friction into durable guidance.

## Workflow

1. Identify the trigger.
   - The user explicitly requested a retrospective.
   - Completed work exposed a recurring mistake, missing instruction, unclear workflow, or reusable process.

2. Separate one-off context from durable lessons.
   - One-off context stays in the current answer.
   - Durable lessons must be concrete, reusable, and likely to help future tasks.

3. Choose one destination.
   - Global behavior: `~/.agents/AGENTS.md`.
   - Project behavior: the closest project `AGENTS.md`.
   - Repeatable workflow: a skill under `~/.agents/skills` or repo `.codex/skills`.
   - Project knowledge: checked-in documentation.
   - Mechanical enforcement: hook, linter, test, or automation.

4. Propose before changing durable state unless the user already asked for the edit.
   - State what happened.
   - State the reusable lesson.
   - State the proposed destination.
   - Explain why that destination fits the scope.

## Guardrails

- Do not edit global instructions, memories, hooks, automations, or skills without explicit user approval or a direct user request.
- Do not create rules from weak evidence.
- Do not store secrets, private credentials, or sensitive personal data in instructions or skills.
- Do not override project-specific instructions.
