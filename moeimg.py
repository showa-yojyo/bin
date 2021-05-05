#!/usr/bin/env python

"""
No description.
"""

import sys
from scrapy import cmdline, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

TARGET_DOMAIN = 'moeimg.net'

class MoeImgNetCrawler(CrawlSpider):
    """No descrition"""

    name = TARGET_DOMAIN
    allowed_domains = [TARGET_DOMAIN]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2/a'), callback='parse_entry'),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a')),
    )

    def start_requests(self):
        """No descrition"""

        url = self.tag
        yield Request(url, dont_filter=True)

    def parse_entry(self, response):
        """No descrition"""

        if images := response.xpath('//a/img[contains(@src, "/wp-content/uploads/archives")]/@src').getall():
            yield {
                'title': response.xpath('//title/text()').get(),
                'url': response.url,
                'images': images}


if __name__ == '__main__':
    #cmdline.execute(f"scrapy runspider {sys.argv[0]} -a tag={sys.argv[1]} -O images.csv".split())
    command_line = ["scrapy", "runspider"]
    command_line.extend(sys.argv)
    cmdline.execute(command_line)
