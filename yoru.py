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

TARGET_DOMAIN = "eromanga-yoru.com"


class EromangaYoruSpider(CrawlSpider):
    """No description"""

    name = TARGET_DOMAIN
    allowed_domains = [TARGET_DOMAIN]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    rules = (
        # a[@title="個別記事ページへ"]
        Rule(
            LinkExtractor(restrict_xpaths='//header[@class="article-header"]/div/a'),
            callback="parse_article",
        ),
        # »
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="nextpostslink"])[1]')),
    )

    def start_requests(self) -> Iterator[Request]:
        """No description"""

        url = f"https://{TARGET_DOMAIN}/tag/{self.tag}"  # type: ignore[attr-defined]
        yield Request(url, dont_filter=True)

    def parse_article(self, response: Response) -> Iterator[Mapping[str, object]]:
        """No description"""

        post_url = response.url
        images = response.xpath('//img[contains(@class, "size-full")]/@src').getall()
        yield {
            "article": post_url,
            "images": images,
        }


if __name__ == "__main__":
    myscrapy.main()
