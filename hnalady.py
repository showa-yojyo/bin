#!/usr/bin/env python

"""
No description.
"""

import sys
from scrapy import cmdline, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

TARGET_DOMAIN = 'hnalady.com'

class HNaLadyCrawler(CrawlSpider):
    """No descrition"""

    name = TARGET_DOMAIN
    allowed_domains = [TARGET_DOMAIN]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths='(//div[@id="main-right"]/div[@class="page_navi"]/p[@class="page_next"]/a)[1]')),
        Rule(LinkExtractor(restrict_xpaths='//h3/a[contains(@title, "このエントリーの固定リンク")]'), callback='parse_entry'),
    )

    def start_requests(self):
        """No descrition"""

        url = self.tag
        yield Request(url, dont_filter=True)

    def parse_entry(self, response):
        """No descrition"""
        images = response.xpath('//div[@id="more"]/a/img/@src')

        # Recommend -O images.csv
        for image in images:
            yield {'image': image.get() for image in images}


if __name__ == '__main__':
    #cmdline.execute(f"scrapy runspider {sys.argv[0]} -a tag={sys.argv[1]} -O images.csv".split())
    command_line = ["scrapy", "runspider"]
    command_line.extend(sys.argv)
    cmdline.execute(command_line)
