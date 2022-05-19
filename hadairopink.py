#!/usr/bin/env python

"""
No description.
"""

import sys
from scrapy import cmdline, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

TARGET_DOMAIN = 'hadairopink.com'

XPATH_IMAGE_SRC = '//div[@class="kizi"]//a/img[contains(@src, "/wp-content/uploads/")]/@src'
XPATH_PAGINATION = '/html/body//div[@class="pagination"]/a[@data-wpel-link="internal"]'
XPATH_ENTRY = '/html/body//h3[@class="entry-title-ac"]/a'

class Crawler(CrawlSpider):
    """No descrition"""

    name = TARGET_DOMAIN
    allowed_domains = [TARGET_DOMAIN]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths=XPATH_ENTRY), callback='parse_entry'),
        Rule(LinkExtractor(restrict_xpaths=XPATH_PAGINATION)),
    )

    def start_requests(self):
        """No descrition"""

        url = self.tag
        yield Request(url, dont_filter=True)

    def parse_entry(self, response):
        """No descrition"""

        if images := response.xpath(XPATH_IMAGE_SRC).getall():
            yield {
                'title': response.xpath('//title/text()').get(),
                'url': response.url,
                'images': images}


if __name__ == '__main__':
    #cmdline.execute(f"scrapy runspider {sys.argv[0]} -a tag={sys.argv[1]} -O images.csv".split())
    command_line = ["scrapy", "runspider"]
    command_line.extend(sys.argv)
    cmdline.execute(command_line)
