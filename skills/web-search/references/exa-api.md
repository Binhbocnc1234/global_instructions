# Exa API Reference

Use this reference only for advanced searches, script changes, or troubleshooting. Exa's official documentation is authoritative when behavior differs:

- [Search API guide for coding agents](https://docs.exa.ai/reference/search-api-guide-for-coding-agents)
- [Python and TypeScript SDK cheat sheet](https://docs.exa.ai/sdks/cheat-sheet)
- [Exa documentation](https://docs.exa.ai/)

## Bundled CLI Contract

`scripts/search.py` uses `exa-py==2.14.0` and reads `EXA_API_KEY` from the environment. It calls `Exa.search` with:

- a positional natural-language query;
- `type`, defaulting to `auto`;
- `num_results`, defaulting to 15;
- optional included and excluded domains;
- `contents={"highlights": True}`.

It emits a JSON array containing `title`, `url`, `score`, `published_date`, `author`, and `highlights`. It writes failures to stderr and returns a nonzero exit code.

`scripts/fetch.py` calls `Exa.get_contents` with:

- one or more positional URLs;
- `text={"max_characters": N}`, where `--max-characters` defaults to 20000;
- `max_age_hours`, only when `--max-age-hours` is set.

It emits a JSON object with `pages` (`title`, `url`, `published_date`, `text`) and `failures` (`url`, `status`, `source`). Exa reports an unreadable URL in `statuses`, not as an exception. The script returns exit code 2 when `failures` is not empty, and 1 when the request fails.

## Supported `search.py` Options

| Option | Purpose |
|---|---|
| `--type` | Choose `auto`, `fast`, `instant`, `deep-lite`, `deep`, or `deep-reasoning` |
| `--num-results` | Request 1-100 results |
| `--include-domain` | Restrict results to a domain; repeatable |
| `--exclude-domain` | Exclude a domain; repeatable |

## SDK Features Not Exposed by the CLI

Use the Python SDK directly, or extend the script with tests, when the task requires:

- structured synthesis through `system_prompt` and `output_schema`;
- extra deep-search queries through `additional_queries`;
- full page text or summaries instead of highlights;
- publication or crawl date filters;
- content freshness controls;
- `/contents` summaries, subpages, and link extras;
- `/answer` for question-first grounded responses.

Keep highlights as the default for agent workflows because they constrain token usage. Set a maximum character count whenever requesting full text.

## Parameter Rules

- Nest `text`, `summary`, and `highlights` inside `contents` for `/search`.
- Use snake_case in the Python SDK and camelCase in raw JSON.
- Use `include_domains` and `exclude_domains`; `includeUrls` and `excludeUrls` are not valid replacements.
- Avoid deprecated options such as `useAutoprompt`, `numSentences`, `highlightsPerUrl`, `tokensNum`, and `livecrawl: "always"`.
- Use current official documentation before adding freshness or structured-output parameters because these interfaces can change.

## Result Interpretation

- `score` can be absent; do not build ranking logic that assumes it always exists.
- Highlights are query-relevant excerpts, not full-document verification.
- Search relevance does not establish software quality, maintenance, security, license compatibility, or GitHub popularity. Verify those properties from canonical sources.
