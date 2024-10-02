#!/usr/bin/env python

"""
No description.
"""

import sys
from typing import Iterator, Mapping, Self
from scrapy import cmdline, Request # type: ignore
from scarpy.http import Response # type: ignore
from scrapy.linkextractors import LinkExtractor # type: ignore
from scrapy.spiders import CrawlSpider, Rule # type: ignore

TARGET_DOMAIN = 'eromanga-yoru.com'

class EromangaYoruSpider(CrawlSpider):
    """No description"""

    name = TARGET_DOMAIN
    allowed_domains = [TARGET_DOMAIN]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    rules = (
        # a[@title="個別記事ページへ"]
        Rule(LinkExtractor(restrict_xpaths='//header[@class="article-header"]/div/a'), callback='parse_article'),
        # »
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="nextpostslink"])[1]')),
    )

    def start_requests(self: Self) -> Iterator[Request]:
        """No description"""

        url = self.tag
        yield Request(url, dont_filter=True)

    def parse_article(self: Self, response: Response) -> Iterator[Mapping]:
        """No description"""

        post_url = response.url
        images = response.xpath(
            '//img[contains(@class, "size-full")]/@src').getall()
        yield {
            'article': post_url,
            'images': images,}

if __name__ == '__main__':
    #cmdline.execute(f"scrapy runspider {sys.argv[0]} -a tag={sys.argv[1]} -O images.jl".split())
    command_line = ["scrapy", "runspider"]
    command_line.extend(sys.argv)
    cmdline.execute(command_line)
