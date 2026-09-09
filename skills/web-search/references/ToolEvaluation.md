# Tool Evaluation

Read this when the request is "I need a tool for X", or a comparison between named tools, libraries, or repositories.

The Exa-first workflow in `SKILL.md` still applies. This file adds what to do with the retrieved results.

## Search Order

1. Search for candidates specific to the task before general-purpose alternatives. A sprite-sheet packer beats a general image toolkit for a sprite-sheet task, even when the general toolkit is more popular.
2. Deduplicate mirrors, wrappers, abandoned forks, and several pages of one project.
3. Verify each finalist from its canonical repository and its documentation, not from a listicle that names it.

## Check Liveness at the Repository

Exa surfaces project pages and issue threads, so it answers what a tool does. It ranks by meaning, not by recency, so it does not answer whether a tool is still alive. A dead project with excellent documentation ranks well.

Get liveness from the repository page itself, never from result ordering:

- date of the last release, and of the last commit to the default branch;
- open issue and pull request backlog, and whether a maintainer replies in the recent ones;
- an archived-repository banner, or a README pointing at a successor project.

A candidate that Exa ranks first and that has no commit in two years is a documentation win, not a tool recommendation.

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
- the page that verified each of the claims above.

Name the engine only when native search supplied a candidate, because that fallback must be announced. See [Fall Back to Native Search](../SKILL.md#fall-back-to-native-search).

## Common Failure

Ranking by search score. Exa's `score` measures relevance of the page to the query text. It measures nothing about the software. A tutorial page about a tool can outrank the tool's own repository. Rank from the verified repository, not from the result order.
