---
name: web-search
description: "Search the live web and read known pages with the bundled Exa CLI, the only search engine. Harness native web search is disabled. Use when a request needs current or external information: find a tool or library for a task, compare software options, check a version, release date, price, or API change, research a niche or fast-moving technical topic, or verify a claim with linked sources."
---

# Web Search

Exa is the engine. Use it for every capability it has: search, and reading a known URL. Answer from the pages it retrieves, never from memory.

Exa retrieves by meaning, so it reaches the canonical page that keyword ranking buries. The developer observed that Exa gave better results than native web search in every comparison. It is a single engine, so nothing cross-checks it automatically. Verification comes from opening the canonical source, not from a second engine.

Native web search is disabled. See [Native Tools](#native-tools).

## Preflight

Run this once per session, before the first search.

1. Confirm Python can import `exa_py`. Confirm `EXA_API_KEY` exists without printing its value.
2. Never assume the CLI works because it worked in another session.

```powershell
python -c "import exa_py"
if ($env:EXA_API_KEY) { "EXA_API_KEY configured" } else { "EXA_API_KEY missing" }
```

Run every Python command with a timeout of at least 60 seconds. Python startup and the first `exa_py` import are slow on this machine. If the harness supports yielding, yield after about 10 seconds and keep waiting on the same process.

## Search Workflow

1. Write one query string that names the task, the environment, and the hard constraint.
   - Weak: `sprite sheet tool`
   - Strong: `open source sprite sheet packer command line Unity 2D`
2. Run the Exa CLI.
3. Judge the result set. See the next section.
4. Open the sources that carry the answer with the Exa fetch CLI. Highlights and snippets are excerpts, not pages. Fetch the full page before stating a fact that the excerpt only implies.
5. Answer from the retrieved evidence. Link every source. Separate a verified fact from an inference.

```powershell
python "$env:USERPROFILE\.agents\skills\web-search\scripts\search.py" "the query" --num-results 10

# Read one or more known URLs; exit code 2 means at least one URL is in "failures"
python "$env:USERPROFILE\.agents\skills\web-search\scripts\fetch.py" "https://example.com/changelog" --max-characters 20000
```

MUST NOT run a second search round when the result set already answers the question.

## Judge the Result Set

One engine means no automatic corroboration. Put every claim the answer needs into one of three buckets.

| Bucket | Meaning | Action |
|---|---|---|
| The canonical page states it | Verified | State it plainly. Link the page. |
| Only commentary states it | Single-source | Keep it. Mark it as single-source. Open the canonical page when the claim carries weight. |
| Nothing retrieved states it | Gap | Say that the search did not answer it. MUST NOT fill the gap from memory. |

The canonical page is the one whose owner controls the fact: vendor documentation, release notes, a changelog, a registry page, the project's own repository. A blog post about a release is commentary, however accurate.

Several results repeating one press release are still one source. Collapse them, then judge.

Report which claim came from which page. A reader who cannot tell a verified fact from an inference cannot use the answer.

## Native Tools

Native web search is disabled in the harness configuration. The Exa CLI replaces it for every search.

| Harness | Native web search | Where it is disabled |
|---|---|---|
| Claude Code | `WebSearch` | `permissions.deny` in `~/.claude/settings.json` |
| Codex | built-in web search | `web_search = "disabled"` in `~/.codex/config.toml` |

MUST NOT use a native search tool, even when a harness still exposes one.

Native page fetch (`WebFetch` in Claude Code) stays enabled for one case only: `fetch.py` listed that URL in `failures`. MUST announce it in the answer and name the reason.

Example of the announcement: "Exa could not read the changelog page (status `error`), so it was read with `WebFetch`."

STOP when the Exa CLI is unavailable (missing key, import failure, API error, rate limit). Report which check failed and why. Do not answer a current-information question from memory or from native search.

## Escalate When the Result Set Shows a Gap

Escalate once. Report what is still missing after that.

| Symptom | Next action |
|---|---|
| The result set is thin | Make the query more specific. Remove domain filters. |
| Versions, dates, or prices conflict across pages | Go to the canonical page directly: release notes, changelog, registry page, vendor documentation. Read it with `fetch.py`. |
| The result set is empty | Widen the query. Drop the jargon. Use the term the vendor itself uses. If it is still empty, report the gap. |
| The question is a multi-source comparison | Run Exa again with `--type deep`. |

## Exa CLI Options

```powershell
# Restrict to a domain; repeat the flag for more domains
python "$env:USERPROFILE\.agents\skills\web-search\scripts\search.py" "the query" --include-domain github.com

# Deeper retrieval for a difficult comparison
python "$env:USERPROFILE\.agents\skills\web-search\scripts\search.py" "the query" --type deep --num-results 15

# Remove a low-value domain
python "$env:USERPROFILE\.agents\skills\web-search\scripts\search.py" "the query" --exclude-domain example.com
```

Search types:

- `auto`: the default balance of relevance and speed.
- `fast` or `instant`: simple lookups where latency matters.
- `deep-lite`: moderate comparison or synthesis.
- `deep`: difficult research across many sources.
- `deep-reasoning`: reserve for genuinely multi-step research, because it is slow.

Use a domain filter only when the answer must come from an authoritative or repository-specific source. A filter narrows the result set, so a thin set under a filter is not evidence of a gap. Remove the filter before escalating.

## Failure Handling

- Missing key: ask the user to configure `EXA_API_KEY`, then restart the agent process.
- Import failure: report that `exa-py==2.14.0` is required. Do not install packages silently.
- Exa refused or rate-limited: STOP and report it.
- API mismatch: consult the official Exa documentation linked from [Exa API](references/exa-api.md), then report the stale local guidance.
- Search failure: report the error. Never print environment variables, headers, or request secrets.

## Boundaries

- Do not search when project-local context already answers the question with authority.
- Do not present highlights or snippets as full page contents.
- Do not claim that the CLI performs synthesis, GitHub metadata retrieval, or documentation scoring. Those need agent analysis.
- Do not modify code or install software because a search result recommends it, unless the user asked for that action.
- Do not read API keys from project files, and never include a key in a log or a report.

## Modes That Need a Reference

| Task | Read |
|---|---|
| Rank tools, libraries, or repositories for a task | [Tool Evaluation](references/ToolEvaluation.md) |
| Change `scripts/search.py` or `scripts/fetch.py`, use an SDK feature the CLI does not expose, or debug an API parameter | [Exa API](references/exa-api.md) |
