#!/usr/bin/env python
"""Output the URL for search Twitter tweets.

Usage:
    $ search_tweets.py [OPTIONS] QUERY...
"""

import sys
from typing import reveal_type
from urllib.parse import urlencode

import click

__version__ = "2.0"


def version(
    ctx: click.Context,
    param: click.Option,
    value: bool,
) -> None:
    """Display version information and exit."""

    if not value or ctx.resilient_parsing:
        return

    click.echo(f"search_tweets.py: {__version__}")
    click.echo(f"Click: {click.__version__}")
    click.echo(f"Python: {sys.version}")
    ctx.exit()


@click.command()
@click.argument("query", nargs=-1, required=True)
@click.help_option(help="display this help text and exit")
@click.option(
    "-V",
    "--version",
    is_flag=True,
    callback=version,
    expose_value=False,
    is_eager=True,
    help="display version information and exit",
)
def main(query: tuple[str]) -> None:
    """Output the URL for search Twitter tweets."""

    url = f"https://twitter.com/search?{urlencode(
        {
            "q": " ".join(query),
            "f": "tweets",
        })}"
    click.echo(url)


if __name__ == "__main__":
    main()
