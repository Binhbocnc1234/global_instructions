---
name: exploration
description: Rapidly explore a codebase to answer where things live, how existing behavior works, what patterns can be reused, or what files are relevant before planning or implementation. Use when the user asks to investigate, find, inspect, understand project structure, locate symbols/usages, or gather implementation context.
---

# Exploration

Use this skill for fast, targeted codebase analysis. The output should be useful context, not a full implementation plan.

## Workflow

1. Start from project guidance.
   - Read root markdown or instruction files that describe structure, conventions, or modules.
   - Follow any active `AGENTS.md` rules.

2. Search broad to narrow.
   - Use file listing/glob search to discover relevant areas.
   - Use text search or symbol/usages search for specific names and patterns.
   - Read full files only after the likely relevant paths are known.

3. Recover from stale paths.
   - If a referenced file is missing, assume it may have moved.
   - Search by filename, class/type/function name, or distinctive text before asking the user.

4. Bias for speed.
   - Parallelize independent reads/searches when possible.
   - Stop once there is enough evidence to answer the user or unblock the next step.
   - Avoid exhaustive sweeps unless the user explicitly asks for exhaustive research.

5. Report findings directly.
   - Include clickable file references when available.
   - Name specific symbols, functions, types, patterns, and analogous implementations.
   - Separate confirmed facts from assumptions.
   - Mention blockers or missing context only when they affect the answer.

## Output Shape

Prefer a concise structure:

- Answer or finding summary.
- Relevant files/symbols.
- Reusable patterns or analogous implementations.
- Risks, blockers, or next steps if needed.

Do not modify files while using this skill unless the user explicitly switches from exploration to implementation.
