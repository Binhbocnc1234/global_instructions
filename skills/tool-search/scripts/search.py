"""Command-line wrapper for token-efficient Exa web searches."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Sequence

from exa_py import Exa
from exa_py.api import Result


SEARCH_TYPES = (
    "auto",
    "fast",
    "instant",
    "deep-lite",
    "deep",
    "deep-reasoning",
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search the web with Exa.")
    parser.add_argument("query", help="Natural-language search query")
    parser.add_argument(
        "--type",
        choices=SEARCH_TYPES,
        default="auto",
        dest="search_type",
        help="Search strategy (default: auto)",
    )
    parser.add_argument(
        "--num-results",
        type=int,
        default=15,
        help="Number of results, from 1 to 100 (default: 10)",
    )
    parser.add_argument(
        "--include-domain",
        action="append",
        default=[],
        help="Only search this domain; repeat to add domains",
    )
    parser.add_argument(
        "--exclude-domain",
        action="append",
        default=[],
        help="Exclude this domain; repeat to add domains",
    )
    args = parser.parse_args(argv)
    if not 1 <= args.num_results <= 100:
        parser.error("--num-results must be between 1 and 100")
    return args


def require_api_key() -> str:
    api_key = os.environ.get("EXA_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "EXA_API_KEY is not set. Restart the terminal after configuring it. If you're coding agent, you should terminate the task and ask user to configure EXA_API_KEY")
    return api_key


def serialize_result(result: Result) -> dict[str, object]:
    return {
        "title": result.title,
        "url": result.url,
        "score": result.score,
        "published_date": result.published_date,
        "author": result.author,
        "highlights": result.highlights or [],
    }


def search(args: argparse.Namespace) -> list[dict[str, object]]:
    client = Exa(api_key=require_api_key())
    response = client.search(
        args.query,
        type=args.search_type,
        num_results=args.num_results,
        include_domains=args.include_domain or None,
        exclude_domains=args.exclude_domain or None,
        contents={"highlights": True},
    )
    return [serialize_result(result) for result in response.results]


def main(argv: Sequence[str] | None = None) -> int:
    try:
        results = search(parse_args(argv))
    except Exception as error:
        print(f"Exa search failed: {error}", file=sys.stderr)
        return 1

    # ASCII JSON remains readable and works in legacy Windows cp1252 consoles.
    print(json.dumps(results, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
