#!/usr/bin/env python

"""
No description.
"""

import sys
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MoeImgNetCrawler(CrawlSpider):
    """No descrition"""

    name = 'moeimg.net'
    allowed_domains = ['moeimg.net']
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    rules = (
        Rule(LinkExtractor(restrict_css='h2 > a'), callback='parse_entry'),
        Rule(LinkExtractor(restrict_css='li.next > a')),
    )

    def start_requests(self):
        """No descrition"""

        url = getattr(self, 'tag', None)
        yield Request(url, dont_filter=True)

    def parse_entry(self, response):
        """No descrition"""
        images = response.css('a > img[src*="/wp-content/uploads/archives"]::attr(src)')

        # Recommend -O images.csv
        for image in images:
            yield {'image': image.get()}


if __name__ == '__main__':
    print(f'Usage: scrapy runspider {sys.argv[0]} [options] -a tag=URL')
