"""Command-line wrapper that reads known URLs through the Exa /contents endpoint."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from exa_py import Exa

from search import require_api_key


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read page contents with Exa.")
    parser.add_argument("urls", nargs="+", help="One or more page URLs")
    parser.add_argument(
        "--max-characters",
        type=int,
        default=20000,
        help="Maximum text characters per page (default: 20000)",
    )
    parser.add_argument(
        "--max-age-hours",
        type=int,
        default=None,
        help="Crawl fresh when the cached page is older; 0 always crawls fresh",
    )
    args = parser.parse_args(argv)
    if args.max_characters < 1:
        parser.error("--max-characters must be positive")
    return args


def fetch(args: argparse.Namespace) -> dict[str, object]:
    client = Exa(api_key=require_api_key())
    response = client.get_contents(
        args.urls,
        text={"max_characters": args.max_characters},
        max_age_hours=args.max_age_hours,
    )
    pages = [
        {
            "title": result.title,
            "url": result.url,
            "published_date": result.published_date,
            "text": result.text,
        }
        for result in response.results
    ]
    # Exa reports a URL it could not read in statuses, not as an exception.
    failures = [
        {"url": status.id, "status": status.status, "source": status.source}
        for status in response.statuses or []
        if status.status != "success"
    ]
    return {"pages": pages, "failures": failures}


def main(argv: Sequence[str] | None = None) -> int:
    try:
        output = fetch(parse_args(argv))
    except Exception as error:
        print(f"Exa contents failed: {error}", file=sys.stderr)
        return 1

    # ASCII JSON remains readable and works in legacy Windows cp1252 consoles.
    print(json.dumps(output, indent=2, ensure_ascii=True))
    return 0 if not output["failures"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
