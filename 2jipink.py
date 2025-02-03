#!/usr/bin/env python

"""
No description.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Iterator, Mapping, Self

from scrapy.linkextractors import LinkExtractor  # type: ignore[attr-defined]
from scrapy.spiders import CrawlSpider, Rule  # type: ignore[attr-defined]

if TYPE_CHECKING:
    from scrapy import Request
    from scrapy.http import Response  # type: ignore[attr-defined]

import myscrapy

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

    def parse_entry(self: Self, response: Response) -> Iterator[Mapping[str, Any]]:
        """No descrpition"""

        if images := response.xpath(
            '//a[@target="_blank"]/img[contains(@src, "img.2ji.pink")]/@src'
        ).getall():
            yield {
                "title": response.xpath("//title/text()").get(),
                "url": response.url,
                "images": images,
            }


if __name__ == "__main__":
    myscrapy.main()
