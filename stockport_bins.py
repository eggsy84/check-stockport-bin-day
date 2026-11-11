#!/usr/bin/env python3
"""
Stockport Council Live Bin Collection Lookup
Fetches live bin collection dates directly from Stockport Council:
https://myaccount.stockport.gov.uk/bin-collections/show/<UPRN>
"""

import argparse
from datetime import datetime, date
import json
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser


DAYS_OF_WEEK = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)

BIN_COLORS = ("Black bin", "Blue bin", "Brown bin", "Green bin")


class StockportBinHTMLParser(HTMLParser):
    """Lightweight, zero-dependency HTML parser for Stockport Council bin page."""

    def __init__(self):
        super().__init__()
        self.text_blocks = []
        self._current = []
        self._skip_tags = {"script", "style", "noscript"}
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip_depth += 1
        elif tag in {"div", "li", "h1", "h2", "h3", "h4", "p", "br", "tr"}:
            self._flush()

    def handle_endtag(self, tag):
        if tag in self._skip_tags and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag in {"div", "li", "h1", "h2", "h3", "h4", "p", "tr"}:
            self._flush()

    def handle_data(self, data):
        if self._skip_depth == 0:
            cleaned = " ".join(data.split())
            if cleaned:
                self._current.append(cleaned)

    def _flush(self):
        if self._current:
            line = " ".join(self._current).strip()
            if line:
                self.text_blocks.append(line)
            self._current = []

    def close(self):
        super().close()
        self._flush()


def parse_uk_date(text: str) -> date | None:
    """
    Parse dates like 'Friday, 13 November 2026' or '13 November 2026'.
    """
    # Match patterns like: (Friday, )?13 November 2026
    pattern = re.compile(
        r"(?:(?:" + "|".join(DAYS_OF_WEEK) + r"),?\s+)?"
        r"(\d{1,2}\s+[A-Za-z]+\s+\d{4})",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if not match:
        return None
    date_part = match.group(1)
    for fmt in ("%d %B %Y", "%d %b %Y"):
        try:
            return datetime.strptime(date_part, fmt).date()
        except ValueError:
            continue
    return None


def fetch_stockport_bins(uprn: str) -> list[dict]:
    """
    Fetch and parse live bin collections from Stockport Council for a given UPRN.
    """
    uprn = str(uprn).strip().rstrip("/").split("/")[-1]
    if not uprn.isdigit():
        raise ValueError(
            f"Invalid UPRN '{uprn}'. Expected numeric UPRN from "
            "https://myaccount.stockport.gov.uk/bin-collections/show/<UPRN>"
        )

    url = f"https://myaccount.stockport.gov.uk/bin-collections/show/{uprn}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml",
        },
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    parser = StockportBinHTMLParser()
    parser.feed(html)
    parser.close()

    blocks = parser.text_blocks
    results = []
    seen_bins = set()

    for i, block in enumerate(blocks):
        matched_bin = None
        for bin_name in BIN_COLORS:
            if block.lower().startswith(bin_name.lower()):
                matched_bin = bin_name
                break

        if matched_bin and matched_bin not in seen_bins:
            # Look in the current block and the next few blocks for a date
            search_window = " | ".join(blocks[i : i + 4])
            collection_date = parse_uk_date(search_window)
            if collection_date:
                seen_bins.add(matched_bin)
                results.append(
                    {
                        "bin": matched_bin,
                        "date": collection_date.isoformat(),
                        "day_of_week": collection_date.strftime("%A"),
                        "formatted_date": collection_date.strftime("%A, %d %B %Y"),
                        "days_until": (collection_date - date.today()).days,
                    }
                )

    results.sort(key=lambda x: x["date"])
    return results


def summarize_next_collection(collections: list[dict]) -> dict:
    """
    Identify the immediate next collection day and which bin(s) to put out.
    """
    if not collections:
        return {
            "found": False,
            "message": "No upcoming bin collections found on the Stockport Council page.",
            "collections": [],
        }

    # Filter to today or future collections (fallback to all if none)
    upcoming = [c for c in collections if c["days_until"] >= 0] or collections
    next_date = upcoming[0]["date"]
    next_bins = [c["bin"] for c in upcoming if c["date"] == next_date]
    days_until = upcoming[0]["days_until"]
    formatted_date = upcoming[0]["formatted_date"]

    if days_until == 0:
        when_str = f"TODAY ({formatted_date})"
    elif days_until == 1:
        when_str = f"TOMORROW ({formatted_date})"
    else:
        when_str = f"on {formatted_date} (in {days_until} days)"

    bins_joined = " and ".join(
        [", ".join(next_bins[:-1]), next_bins[-1]]
        if len(next_bins) > 2
        else next_bins
    )

    message = f"Your next collection is {when_str}. Put out your: {bins_joined}."
    return {
        "found": True,
        "next_date": next_date,
        "formatted_date": formatted_date,
        "days_until": days_until,
        "bins_to_put_out": next_bins,
        "message": message,
        "all_collections": collections,
    }


def main():
    arg_parser = argparse.ArgumentParser(
        description="Live lookup of Stockport Council bin collection schedule."
    )
    arg_parser.add_argument(
        "--uprn",
        default=os.environ.get("STOCKPORT_UPRN", ""),
        help="Your Stockport UPRN (or full collection URL).",
    )
    arg_parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON.",
    )
    args = arg_parser.parse_args()

    if not args.uprn:
        print(
            "Error: Please provide your Stockport UPRN via --uprn <UPRN> "
            "or set the STOCKPORT_UPRN environment variable.\n"
            "Find your UPRN at: https://www.stockport.gov.uk/find-your-collection-day",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        collections = fetch_stockport_bins(args.uprn)
        summary = summarize_next_collection(collections)
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print(summary["message"])
            if summary["all_collections"]:
                print("\nFull upcoming schedule:")
                for item in summary["all_collections"]:
                    print(f"  - {item['bin']}: {item['formatted_date']}")
    except Exception as exc:
        print(f"Failed to fetch bin collection schedule: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
