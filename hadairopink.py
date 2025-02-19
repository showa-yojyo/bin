#!/usr/bin/env python

"""
No description.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterator, Mapping

from scrapy.linkextractors import LinkExtractor  # type: ignore[attr-defined]
from scrapy.spiders import CrawlSpider, Rule  # type: ignore[attr-defined]

if TYPE_CHECKING:
    from scrapy import Request
    from scrapy.http import Response  # type: ignore[attr-defined]

import myscrapy

TARGET_DOMAIN = "hadairopink.com"

XPATH_IMAGE_SRC = (
    '//div[@class="kizi"]//a/img[contains(@src, "/wp-content/uploads/")]/@src'
)
XPATH_PAGINATION = '/html/body//div[@class="pagination"]/a[@data-wpel-link="internal"]'
XPATH_ENTRY = '/html/body//h3[@class="entry-title-ac"]/a'


class Crawler(CrawlSpider):
    """No description"""

    name = TARGET_DOMAIN
    allowed_domains = [TARGET_DOMAIN]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths=XPATH_ENTRY), callback="parse_entry"),
        Rule(LinkExtractor(restrict_xpaths=XPATH_PAGINATION)),
    )

    def start_requests(self) -> Iterator[Request]:
        """No description"""

        url = f"https://{TARGET_DOMAIN}/category/{self.tag}"  # type: ignore[attr-defined]
        yield Request(url, dont_filter=True)

    def parse_entry(self, response: Response) -> Iterator[Mapping[str, object]]:
        """No description"""

        if images := response.xpath(XPATH_IMAGE_SRC).getall():
            yield {
                "title": response.xpath("//title/text()").get(),
                "url": response.url,
                "images": images,
            }


if __name__ == "__main__":
    myscrapy.main()
