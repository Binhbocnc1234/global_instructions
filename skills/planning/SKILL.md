---
name: planning
description: Create or revise a concise implementation plan for non-trivial work after researching the codebase. Use when the user asks for a plan, roadmap, design, phase breakdown, plan revision, or when a task is complex enough that implementation should be aligned before edits.
---

# Planning

Use this skill to create or revise an actionable implementation plan. Planning is separate from implementation unless the user explicitly asks to proceed after the plan.

## When To Plan

Plan before implementation when the task has any of these traits:

- touches multiple files or systems
- creates new files, APIs, or architecture
- changes public behavior, interfaces, tests, or documentation contracts
- requires choosing between designs
- has unclear scope, risks, or dependencies

Simple mechanical edits do not need a formal plan.

## Workflow

1. Discovery.
   - Use targeted exploration to understand current structure.
   - Find analogous existing implementations and conventions to reuse.
   - Identify affected files and verification commands.

2. Alignment.
   - Surface major ambiguities, contradictions, or risky assumptions.
   - Ask the user only when a reasonable assumption would be risky or business logic is unclear.
   - State important scope boundaries.

3. Design.
   - Group work into phases when phases are independently verifiable.
   - Keep each step concrete enough for implementation.
   - Reference specific files, symbols, APIs, or patterns.
   - Include verification for each phase or for the whole plan.

4. Refinement.
   - Check the plan for internal conflicts.
   - Remove unnecessary steps and overly broad refactors.
   - Keep the plan scannable.

## Plan Template

Use this shape when a written plan is useful:

```md
# [Plan Name]

## TL;DR
[Brief summary.]

## Current Status
- Codebase status:
- Current architecture:
- Reason for change:

## Scope
- In scope:
- Out of scope:

## Phase 1: [Name]
Objective: [What this phase accomplishes.]

### Step: [Name]
- Description:
- Affected files:
- Reference patterns:
- Dependencies:

Verification:

## Risks / Open Questions
- [Only if any.]
```

## Revising Existing Plans

When revising a plan:

1. Read the current plan and relevant source files.
2. Accept implementation feedback objectively.
3. Identify the issue, evidence, impacted steps, and correction.
4. Update the smallest necessary part of the plan if the user asked for an edit.
5. Summarize what changed.

## Guardrails

- Do not implement while using this skill unless the user explicitly asks to proceed.
- Do not create a plan file unless the user asks for a saved plan or the project workflow requires one.
- Do not over-plan simple one-file mechanical edits.
- Keep plans in English unless the user requests another language.
