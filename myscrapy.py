"""
myscrapy.py: a wrapper module of Scrapy
"""

from __future__ import annotations
import sys

from scrapy import cmdline  # type: ignore

import click


@click.command()
@click.argument("tag", nargs=1, required=True)
@click.option(
    "-f",
    "--format",
    type=click.Choice(
        ["json", "jsonline", "xml", "csv"],
        case_sensitive=False,
    ),
    default="json",
    help="scraped data format",
)
@click.option(
    "--log/--nolog",
    default=False,
    help="enable logging",
)
@click.help_option(help="show this message and exit")
def main(tag: str, format: str, log: bool) -> None:
    """Crawl a website."""

    command_line = [
        "scrapy",
        "runspider",
        sys.argv[0],
        # Pass `-a TAG`.
        "-a",
        f"tag={tag}",
        # Pass `-o STDOUT:FORMAT`.
        "-o",
        f"-:{format}",
    ]

    if not log:
        command_line.append("--nolog")

    cmdline.execute(command_line)
