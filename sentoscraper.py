#!/usr/bin/env python

import asyncio
import sys
from argparse import ArgumentParser
from collections import namedtuple
from urllib import request

from bs4 import BeautifulSoup

__version__ = '1.0'

TOP = 'http://www.1010.or.jp/map/item/'
URLS = (
    'item-cnt-251', # 興和浴場
    'item-cnt-253', # 湯パーク松島
    'item-cnt-254', # 千代の湯
    'item-cnt-255', # 大黒湯（休業中）
    'item-cnt-256', # 金町湯
    'item-cnt-257', # 栄湯
    'item-cnt-258', # 富士の湯
    'item-cnt-259', # ゆートピア２１
    'item-cnt-260', # 第一日立湯
    'item-cnt-261', # 日の出湯
    'item-cnt-262', # 日の出湯
    'item-cnt-266', # 富士の湯
    'item-cnt-267', # 寿湯
    'item-cnt-268', # 吉の湯
    'item-cnt-269', # 美吉湯
    'item-cnt-270', # さつき湯
    'item-cnt-271', # 草津湯
    'item-cnt-272', # 久の湯
    'item-cnt-273', # 第四富士の湯
    'item-cnt-274', # 橘湯
    'item-cnt-237', # 竹の湯
    'item-cnt-240', # アクアガーデン栄湯
    'item-cnt-241', # 寿湯
    'item-cnt-242', # 富の湯
    'item-cnt-244', # 成弘湯
    'item-cnt-245', # アクアドルフィンランド
    'item-cnt-246', # 喜久の湯
    'item-cnt-247', # 末広湯
#    'item-cnt-479', # 八幡湯
#    'item-cnt-480', # 駒の湯
#    'item-cnt-481', # 栄湯
#    'item-cnt-482', # 弘善湯
#    'item-cnt-483', # ノザワランド（休業中）
#    'item-cnt-485', # 天狗湯
#    'item-cnt-486', # 富士見湯
#    'item-cnt-487', # 千代の湯
#    'item-cnt-488', # 世田谷温泉 四季の湯
#    'item-cnt-489', # 鶴の湯
#    'item-cnt-490', # 石川湯
#    'item-cnt-491', # 宇田川湯
#    'item-cnt-492', # 松原湯
#    'item-cnt-493', # 月見湯温泉
#    'item-cnt-494', # 山崎湯
#    'item-cnt-495', # 新寿湯
#    'item-cnt-497', # 北沢湯
#    'item-cnt-498', # 松の湯（休業中）
#    'item-cnt-499', # 増穂湯
#    'item-cnt-500', # 丸正浴場
#    'item-cnt-501', # えの木湯（休業中）
#    'item-cnt-502', # 湯パークレビランド
#    'item-cnt-503', # そしがや温泉２１
#    'item-cnt-504', # 塩の湯（休業中）
#    'item-cnt-505', # 給田湯
#    'item-cnt-506', # つばめ湯（休業中）
#    'item-cnt-507', # 松の湯
#    'item-cnt-509', # 藤の湯
#    'item-cnt-510', # 栗の湯（休業中）
#    'item-cnt-511', # 栄湯
    )

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
        '-s', '--semaphore',
        default=3,
        help='the count of the semaphore'
    )

    return parser.parse_args(args)

async def fetch(args):
    """TODO: docstring"""
    semaphore = asyncio.Semaphore(args.semaphore)

    async def scrape_with_semaphore(url, localpath):
        with await semaphore:
            return await scrape(url, localpath)

    return await asyncio.wait(
        [scrape_with_semaphore(TOP + url, '{}.html'.format(url)) for url in URLS])

async def scrape(url, localpath):
    """TODO: docstring"""
    try:
        with open(localpath, mode='rb') as fin:
            data = fin.read()
    except (IOError, FileNotFoundError):
        with request.urlopen(url) as fin:
            data = fin.read()
        with open(localpath, mode='wb') as fout:
            fout.write(data)

    def sanitize(text):
        return text.replace('\t', ' ').strip()

    bs = BeautifulSoup(data, "html.parser")
    sento = Sento(
        id=localpath,
        name=bs.find('h2').text,
        has_laundry=0 if bs.find('a', string="コインランドリー") is None else 1,
        address=sanitize(bs.find(string="住所").find_next('td').text),
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
