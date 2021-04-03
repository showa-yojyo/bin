#!/usr/bin/env python

"""
No description.
"""

import sys
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class SentoListSpider(CrawlSpider):
    """No descrition"""

    name = 'sentolist'
    allowed_domains = ['www.1010.or.jp']
    start_urls = [
        'https://www.1010.or.jp/map/item/',
        'https://www.1010.or.jp/map/item/page/2']
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2/a[1]'), callback='parse_entry'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="wp-pagenavi"]/a')),
    )

    def parse_entry(self, response):
        """No descrition"""

        yield {
            'id': response.xpath('string(//tr[1]/td)').get().strip(),
            'name': response.xpath('//h2/text()').get().strip(),
            'address': response.xpath('string(//tr[2]/td)').get().strip(),
            'holidays': response.xpath('string(//tr[6]/td)').get().strip(),
            'office_hours': response.xpath('string(//tr[7]/td)').get().strip(),
            'url': response.url,
        }


if __name__ == '__main__':
    print(f'Usage: scrapy runspider {sys.argv[0]}')
