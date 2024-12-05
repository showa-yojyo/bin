#!/usr/bin/env python

"""
No description.
"""

import sys
from typing import Iterator, Mapping, Self

from scrapy import cmdline, Request  # type: ignore
from scarpy.http import Response  # type: ignore
from scrapy.linkextractors import LinkExtractor  # type: ignore
from scrapy.spiders import CrawlSpider, Rule  # type: ignore

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

        url = self.tag
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
    # cmdline.execute(f"scrapy runspider {sys.argv[0]} -a tag={sys.argv[1]} -O images.csv".split())
    command_line = ["scrapy", "runspider"]
    command_line.extend(sys.argv)
    cmdline.execute(command_line)
