---
name: tool-search
description: Search the current web with Exa and evaluate tools, libraries, repositories, documentation, or other technical resources. Use when a user asks to find a tool for a task, compare current software options, research niche or changing technical information, or retrieve source-backed web results through the project Exa integration.
---

# Tool Search

Use the bundled CLI for repeatable, token-efficient Exa searches. Treat its JSON as retrieval evidence, not a finished answer.

## Preflight

1. Run commands from the repository root.
2. Confirm Python can import `exa_py`.
3. Confirm `EXA_API_KEY` exists without printing its value.
4. If the package or key is missing, stop and tell the user exactly what must be configured. Never read keys from project files or include them in logs.

```powershell
python -c "import exa_py"
if ($env:EXA_API_KEY) { "EXA_API_KEY configured" } else { "EXA_API_KEY missing" }
```

## Search Workflow

1. Convert the request into a specific query containing the task, environment, and important constraints.
2. Start with `type=auto`, 5-10 results, and highlights.
3. Use domain filters only when authoritative or repository-specific sources are required.
4. Inspect the returned URLs and highlights. Run narrower follow-up searches when evidence is incomplete.
5. Answer from the retrieved evidence, link the supporting sources, and distinguish verified facts from inference.

```powershell
python .agents/skills/tool-search/scripts/search.py "<query>" --num-results 15
```

Useful variants:

```powershell
# Focus on GitHub repositories
python .agents/skills/tool-search/scripts/search.py "<task> open source repository" --include-domain github.com

# Use deeper retrieval for difficult comparisons
python .agents/skills/tool-search/scripts/search.py "<comparison query>" --type deep --num-results 15

# Exclude a low-value domain
python .agents/skills/tool-search/scripts/search.py "<query>" --exclude-domain example.com
```

Repeat `--include-domain` or `--exclude-domain` to pass multiple domains. Read `references/exa-api.md` before changing the script, using advanced SDK features, or troubleshooting API parameters.

## Tool and Repository Evaluation

For requests such as "I need a tool for X":

1. Search for task-specific candidates before general-purpose alternatives.
2. Deduplicate mirrors, wrappers, abandoned forks, and multiple pages for the same project.
3. Verify each finalist using its canonical repository and documentation.
4. Rank primarily by project fit, then documentation quality and maintenance evidence. Treat GitHub stars as supporting popularity evidence, not proof of quality.
5. Never invent star counts. The CLI does not return stars; verify current counts separately or mark them unavailable.

Return a compact ranked list containing:

- repository and URL;
- why it fits the user's concrete task;
- verified GitHub stars when available;
- documentation quality with evidence;
- maintenance or integration risks.

Prefer three strong candidates over a long unfiltered list.

## Search Type Selection

- `auto`: default balance of relevance and speed.
- `fast` or `instant`: simple lookups where latency matters.
- `deep-lite`: moderate comparison or synthesis.
- `deep`: difficult research across multiple sources.
- `deep-reasoning`: reserve for genuinely complex multi-step research because it is slower.

## Failure Handling

- Missing key: ask the user to configure `EXA_API_KEY` and restart the agent process.
- Import failure: report that `exa-py==2.14.0` is required; do not silently install packages.
- Weak results: make the query more specific, remove unnecessary filters, then try `deep`.
- API mismatch: consult Exa's official documentation linked in `references/exa-api.md` and report stale local guidance.
- Search failure: report the error without exposing environment variables, headers, or request secrets.

## Boundaries

- Do not use Exa when authoritative project-local context already answers the question.
- Do not present highlights as complete page contents.
- Do not claim the CLI performs structured synthesis, GitHub metadata retrieval, or documentation scoring; those require agent analysis or future script support.
- Do not modify code or install software merely because search results recommend it unless the user requested that action.
