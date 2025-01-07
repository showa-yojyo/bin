#!/usr/bin/env python

"""
No description.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterator, Mapping, Self

from scrapy import Request  # type: ignore
from scrapy.http import Response  # type: ignore
from scrapy.linkextractors import LinkExtractor  # type: ignore
from scrapy.spiders import CrawlSpider, Rule  # type: ignore

import myscrapy

TARGET_DOMAIN = "moeimg.net"


class MoeImgNetCrawler(CrawlSpider):
    """No description"""

    name = TARGET_DOMAIN
    allowed_domains = [TARGET_DOMAIN]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h2/a"), callback="parse_entry"),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a')),
    )

    def start_requests(self: Self) -> Iterator[Request]:
        """No description"""

        url = f"https://{TARGET_DOMAIN}/tag/{self.tag}"  # type: ignore[attr-defined]
        yield Request(url, dont_filter=True)

    def parse_entry(self: Self, response: Response) -> Iterator[Mapping]:
        """No description"""

        if images := response.xpath(
            '//a/img[contains(@src, "/wp-content/uploads/archives")]/@src'
        ).getall():
            yield {
                "title": response.xpath("//title/text()").get(),
                "url": response.url,
                "images": images,
            }


if __name__ == "__main__":
    myscrapy.main()
