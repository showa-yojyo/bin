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

TARGET_DOMAIN = "hnalady.com"


class HNaLadyCrawler(CrawlSpider):
    """No descrpition"""

    name = TARGET_DOMAIN
    allowed_domains = [TARGET_DOMAIN]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths='(//div[@id="main-right"]/div[@class="page_navi"]/p[@class="page_next"]/a)[1]'
            )
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths='//h3/a[contains(@title, "このエントリーの固定リンク")]'
            ),
            callback="parse_entry",
        ),
    )

    def start_requests(self) -> Iterator[Request]:
        """No descrpition"""

        url = f"https://{TARGET_DOMAIN}/blog-category-{self.tag}.html"  # type: ignore[attr-defined]
        yield Request(url, dont_filter=True)

    def parse_entry(self, response: Response) -> Iterator[Mapping[str, object]]:
        """No descrpition"""

        if images := response.xpath('//div[@id="more"]/a/img/@src').getall():
            yield {
                "title": response.xpath("//title/text()").get(),
                "url": response.url,
                "images": images,
            }


if __name__ == "__main__":
    myscrapy.main()
