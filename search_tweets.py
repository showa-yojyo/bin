#!/usr/bin/env python
"""Search the latest tweets in Twitter.

Usage:
    $ search_tweets.py QUERY ...
"""

from argparse import ArgumentParser, Namespace
import sys
from typing import Never, Sequence
from urllib.parse import urlencode
from webbrowser import open_new

__version__ = "1.1"


def parse_args(args: Sequence[str]) -> Namespace:
    """Parse the command line parameters."""

    parser = ArgumentParser(description="Search the latest tweets in Twitter")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("query", nargs="+", help="query string")

    return parser.parse_args(args or ["--help"])


def run(args: Namespace) -> int:
    """The main function."""

    return open_new(
        "https://twitter.com/search?"
        + urlencode({"q": " ".join(args.query), "f": "tweets"})
    )


def main(args: Sequence[str] = sys.argv[1:]) -> Never:
    sys.exit(run(parse_args(args)))


if __name__ == "__main__":
    main()
