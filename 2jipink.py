#!/usr/bin/env python

"""
No description.
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterator, Mapping, Self

from scrapy import cmdline, Request  # type: ignore
from scrapy.http import Response  # type: ignore
from scrapy.linkextractors import LinkExtractor  # type: ignore
from scrapy.spiders import CrawlSpider, Rule  # type: ignore

import click

TARGET_DOMAIN = "2ji.pink"


class Crawler(CrawlSpider):
    """No descrpition"""

    name = TARGET_DOMAIN
    allowed_domains = [TARGET_DOMAIN]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths='//section/h2[@class="entry-title"]/a'),
            callback="parse_entry",
        ),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="pagination"]/li/a')),
    )

    def start_requests(self: Self) -> Iterator[Request]:
        """No descrpition"""

        url = f"https://{TARGET_DOMAIN}/tag/{self.tag}"  # type: ignore[attr-defined]
        yield Request(url, dont_filter=True)

    def parse_entry(self: Self, response: Response) -> Iterator[Mapping]:
        """No descrpition"""

        if images := response.xpath(
            '//a[@target="_blank"]/img[contains(@src, "img.2ji.pink")]/@src'
        ).getall():
            yield {
                "title": response.xpath("//title/text()").get(),
                "url": response.url,
                "images": images,
            }


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


if __name__ == "__main__":
    main()
