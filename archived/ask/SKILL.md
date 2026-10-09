---
name: ask
description: Answer questions or research requests only after checking whether enough context is available. Use when the user asks for advice, feasibility analysis, recommendations, explanations, research, or decisions where missing personal/project constraints could change the answer.
---

# Ask

Use this skill when the main job is to answer, explain, research, or advise rather than modify files.

The core rule: do not give a confident answer when the missing context could materially change the conclusion.

## Context Sufficiency Check

Before answering, identify whether the answer depends on any of these:

- user's current resources, constraints, budget, timeline, knowledge, risk tolerance or other personal informations
- user's existing skills, assets, team, tools, or codebase
- business model, target audience, market, platform, or geography
- project-specific files, architecture, conventions, requirements, or documentation
- external facts that may be current or fast-changing
- etc...

If any missing item could change the recommendation, ask concise clarification questions first. No need to ask for information that is unlikely to affect the answer or can be ask later

## When To Answer Directly

Answer without extra questions when:

- the prompt already contains enough context
- the question is factual and source-independent
- the user explicitly asks for a general answer
- missing details would only affect minor examples, not the main conclusion

State assumptions when answering with partial context.

## Source Selection

- For project/code questions, inspect the codebase only when the prompt does not already provide enough context.
- For external software, APIs, frameworks, current product behavior, law, pricing, or market facts, use current authoritative/official sources when available.

## Output Shape

If context is insufficient:

```text
I need a bit more context before giving a useful answer:

1. ...
2. ...
3. ...
```

If context is sufficient:

- direct answer
- assumptions, if any
- relevant project/source references, if needed
- missing information or residual risk, if any

## Example

Prompt: "Research whether starting a game studio with small capital is feasible. Focus on capital."

Do not jump straight to generic costs like hiring developers, art, marketing, and living expenses.

Ask first for the capital-shaping facts, some good questions:

- What can the user already do themselves: code, art, design, marketing, audio?
- Are living expenses already covered?
- What is the available capital and how much is reserved for marketing?
- What type/scope/platform of game is being considered?

Only after that context should the feasibility answer estimate capital needs.
