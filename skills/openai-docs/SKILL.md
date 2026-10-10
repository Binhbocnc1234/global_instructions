---
name: openai-docs
description: Find official OpenAI documentation for Codex setup, troubleshooting, models, skills, settings, OpenAI APIs, and ChatGPT Work. Use for questions about Codex itself or model selection and migration, not generic software work.
---

# OpenAI Docs

Use the maintained [bundled OpenAI Docs instructions](../../../.codex/skills/.system/openai-docs/SKILL.md) for topic routing and supporting references. Read that entrypoint before the documentation lookup; resolve its relative references against its own directory.

Use the shared [web-search skill](../web-search/SKILL.md) for official-domain search and page retrieval. It owns the Exa workflow and search failure handling. Restrict sources to the official domains accepted by the bundled instructions.

This entrypoint makes the same documentation workflow discoverable by one-harness and Codex Desktop without copying the bundled reference library. The bundled entrypoint is disabled in Desktop's catalog to avoid duplicate skill choices; its files remain installed as this skill's dependency.
