#!/usr/bin/env python
"""sento.py: List bath houses in KU of Tokyo
"""
import asyncio
import sys
from argparse import ArgumentParser
from urllib import parse, request

from bs4 import BeautifulSoup

__version__ = '1.2'

URL = 'http://www.1010.or.jp/map/archives/area/{ku}/page/{page:d}'

def parse_args(args):
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='List bath houses in KU of Tokyo')
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument(
        'ku',
        metavar='KU',
        default='北区',
        help='ku (ward) in which bath houses to be searched'
    )
    parser.add_argument(
        'page',
        default=1,
        type=int,
        help='the number of pages to be searched')

    return parser.parse_args(args or ["--help"])

def parse_item(item):
    """Return name, location, holiday and office hours"""

    def get_column_value(item, propname):
        return item.find(string=propname).find_next('td').text.strip()

    def has_laundry(item):
        return bool(item.find(string='コインランドリー'))

    info = item.find('div', class_='info')

    name = info.h2.a.text
    location = 'TODO'
    access = get_column_value(item, 'アクセス')
    holidays = get_column_value(item, '休日')
    laundry = '1' if has_laundry(item) else '0'
    office_hours = get_column_value(item, '営業時間')

    return [name, location, access, holidays, laundry, office_hours]

async def fetch(ku, page):
    """Fetch all the data"""
    return await asyncio.wait(
        [scrape(URL.format(ku=ku, page=i + 1)) for i in range(page)])

async def scrape(url):
    """Scrape the page located in url"""
    with request.urlopen(url) as html:
        soup = BeautifulSoup(html, "html.parser")

    items = soup.findAll('div', attrs={'class': 'item'})
    for j in items:
        print('|'.join(parse_item(j)))

def run(args):
    """The main function"""

    print('|'.join(('名前', '位置', 'アクセス', '定休日', 'コインランドリー', '営業時間')))

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fetch(
            parse.quote(args.ku), args.page))
    finally:
        loop.close()

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args)))

if __name__ == '__main__':
    main()
