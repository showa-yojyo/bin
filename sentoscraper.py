#!/usr/bin/env python
"""
Usage:
$ sentoscraper.py ID1 ID2 ...

In Cygwin, run this script as follows:
$ getclip
590
591
592
593
594
595
596
597
598
$ getclip | dos2unix | xargs sentoscraper.py --cache-dir D:/home/yojyo/data/sento
"""

import asyncio
import re
import os.path
import sys
from argparse import ArgumentParser
from collections import namedtuple
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup

__version__ = '2'

URL_PATTERN = 'http://www.1010.or.jp/map/item/item-cnt-{id}'

CACHE_DIR = None

class Sento(namedtuple('Sento',
    ['id', 'name', 'address', 'access', 'holidays', 'has_laundry', 'office_hours'])):
    """TODO: docstring"""
    __slots__ = ()
    def __str__(self):
        return '\t'.join(self[:5]) + '\t' + str(self.has_laundry) + '\t' + self[-1]

def parse_args(args):
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='A downloader')
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument(
        'id',
        nargs='+',
        help='numeric ID')

    parser.add_argument(
        '-s', '--semaphore',
        type=int,
        default=3,
        help='the count of the semaphore')

    parser.add_argument(
        '-c', '--cache-dir',
        help='directory in which cache files to be stored')

    return parser.parse_args(args)

async def fetch(args):
    """TODO: docstring"""
    semaphore = asyncio.Semaphore(args.semaphore)

    global CACHE_DIR
    CACHE_DIR = args.cache_dir

    async def scrape_with_semaphore(id):
        with await semaphore:
            return await scrape(id)

    return await asyncio.wait(
        [scrape_with_semaphore(i) for i in args.id])


def make_url(id):
    return URL_PATTERN.format(id=id)

def make_local_path(url):
    return os.path.basename(url) + '.html'

TABLE = str.maketrans('０１２３４５６７８９：−', '0123456789:-')

async def scrape(id):
    """TODO: docstring"""

    url = make_url(id)
    localpath = make_local_path(url)

    global CACHE_DIR
    if CACHE_DIR:
        localpath = os.path.normpath(os.path.join(CACHE_DIR, localpath))

    try:
        with open(localpath, mode='rb') as fin:
            data = fin.read()
    except (IOError, FileNotFoundError):
        with urlopen(url) as fin:
            data = fin.read()
        with open(localpath, mode='wb') as fout:
            fout.write(data)

    def sanitize(text):
        return re.sub(r'\s+', '', text.strip()).translate(TABLE)

    def process_address(text):
        """Remove area code from given address"""
        return sanitize(text[9:])

    bs = BeautifulSoup(data, "lxml")

    sento = Sento(
        id=localpath,
        name=bs.find('h2').text,
        has_laundry=0 if bs.find('a', string="コインランドリー") is None else 1,
        address=process_address(bs.find(string="住所").find_next('td').text),
        access=sanitize(bs.find(string="アクセス").find_next('td').text),
        holidays=sanitize(bs.find(string="休日").find_next('td').text),
        office_hours=sanitize(bs.find(string="営業時間").find_next('td').text))

    return sento

def run(args):
    """The main function"""

    try:
        loop = asyncio.get_event_loop()
        done, pending = loop.run_until_complete(fetch(args))
        for i in sorted(d.result() for d in done):
            print(i)
    finally:
        loop.close()

def main(args=sys.argv[1:]):
    """TODO: docstring"""
    sys.exit(run(parse_args(args)))

if __name__ == '__main__':
    main()
