#!/usr/bin/env python

"""
Example:
$ ./sentocrawler.py -f json
"""

from __future__ import annotations
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterator, Mapping, Self

from scrapy import cmdline
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

if TYPE_CHECKING:
    from scrapy.http import Response

import click


class SentoListSpider(CrawlSpider):
    """No description"""

    name = "sentolist"
    allowed_domains = ("www.1010.or.jp",)
    start_urls = [
        "https://www.1010.or.jp/map/item/",
        "https://www.1010.or.jp/map/item/page/2",
    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h2/a[1]"), callback="parse_entry"),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="wp-pagenavi"]/a')),
    )

    def parse_entry(self: Self, response: Response) -> Iterator[Mapping]:
        """No descrpition"""

        def safe_xpath(xpath: str) -> str:
            sel_list = response.xpath(xpath)
            if text := sel_list.get():
                return text.strip()
            return ""

        yield {
            "id": safe_xpath("string(//tr[1]/td)"),
            "name": safe_xpath("//h2/text()"),
            "address": safe_xpath("string(//tr[2]/td)"),
            "holidays": safe_xpath("string(//tr[6]/td)"),
            "office_hours": safe_xpath("string(//tr[7]/td)"),
            "url": response.url,
        }


@click.command()
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
def main(format: str, log: bool) -> None:
    """A scraping tool for Tokyo Sento."""

    command_line = [
        "scrapy",
        "runspider",
        sys.argv[0],
        "-o",
        f"-:{format}",
    ]

    if not log:
        command_line.append("--nolog")

    cmdline.execute(command_line)


if __name__ == "__main__":
    main()
