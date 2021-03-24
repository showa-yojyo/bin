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
        Rule(LinkExtractor(restrict_css='h2 > a'), callback='parse_entry'),
        Rule(LinkExtractor(restrict_css='li.next > a')),
    )

    def start_requests(self):
        """No descrition"""

        url = self.tag
        yield Request(url, dont_filter=True)

    def parse_entry(self, response):
        """No descrition"""
        images = response.css('a > img[src*="/wp-content/uploads/archives"]::attr(src)')

        # Recommend -O images.csv
        for image in images:
            yield {'image': image.get()}


if __name__ == '__main__':
    #cmdline.execute(f"scrapy runspider {sys.argv[0]} -a tag={sys.argv[1]} -O images.csv".split())
    command_line = ["scrapy", "runspider"]
    command_line.extend(sys.argv)
    cmdline.execute(command_line)
