# Tool Evaluation

Read this when the request is "I need a tool for X", or a comparison between named tools, libraries, or repositories.

The two-engine workflow in `SKILL.md` still applies. This file adds what to do with the compared results.

## Search Order

1. Search for candidates specific to the task before general-purpose alternatives. A sprite-sheet packer beats a general image toolkit for a sprite-sheet task, even when the general toolkit is more popular.
2. Deduplicate mirrors, wrappers, abandoned forks, and several pages of one project.
3. Verify each finalist from its canonical repository and its documentation, not from a listicle that names it.

## What the Two Engines Contribute Here

The engines disagree in a predictable way on tool questions, so read the disagreement instead of merging it away.

- Exa surfaces the project pages and issue threads. It is the better source for what a tool actually does.
- Native search surfaces recent posts, comparisons, and complaints. It is the better source for whether a tool is still alive and who abandoned it.

A candidate that Exa finds and native search never mentions is usually niche, and possibly unmaintained. A candidate that only native search returns, through blog posts, is usually popular but may not fit the specific task. Check both cases against the repository before ranking.

## Ranking Rules

Rank primarily by fit to the user's concrete task. Then documentation quality. Then evidence of maintenance.

GitHub stars are supporting popularity evidence, not proof of quality. MUST NOT invent a star count. The CLI does not return stars. Verify the current count from the repository page, or mark it unavailable.

## Report Format

Return a compact ranked list. Prefer three strong candidates over a long unfiltered list. For each candidate:

- repository name and URL;
- why it fits this concrete task;
- verified star count, or "not verified";
- documentation quality, with the evidence that supports the judgment;
- maintenance or integration risk: last release date, open issue backlog, license, platform support;
- which engine found it.

## Common Failure

Ranking by search score. Exa's `score` measures relevance of the page to the query text. It measures nothing about the software. A tutorial page about a tool can outrank the tool's own repository. Rank from the verified repository, not from the result order.
