#!/usr/bin/env python

import asyncio
import re
import sys
from argparse import ArgumentParser
from collections import namedtuple
from urllib import request

from bs4 import BeautifulSoup

__version__ = '1.1'

TOP = 'http://www.1010.or.jp/map/item/'
URLS = (
    # 'item-cnt-344', # 改良湯
    # 'item-cnt-345', # 宝来湯
    # 'item-cnt-346', # 広尾湯
    # 'item-cnt-347', # さかえ湯
    # 'item-cnt-350', # 渋谷笹塚温泉 栄湯
    # 'item-cnt-351', # 観音湯
    # 'item-cnt-353', # 第二かねき湯
    # 'item-cnt-354', # 羽衣湯
    # 'item-cnt-355', # 八幡湯
    # 'item-cnt-356', # 仙石湯
    # 'item-cnt-358', # 天神湯
    # 'item-cnt-359', # 健康浴泉
    # 'item-cnt-360', # アクア東中野
    # 'item-cnt-361', # 松本湯
    # 'item-cnt-362', # 千代の湯
    # 'item-cnt-363', # 照の湯
    # 'item-cnt-364', # 高砂湯
    # 'item-cnt-365', # 昭和浴場
    # 'item-cnt-366', # クラブ湯
    # 'item-cnt-367', # 大黒湯
    # 'item-cnt-369', # 清春湯
    # 'item-cnt-370', # 月の湯
    # 'item-cnt-371', # たからゆ
    # 'item-cnt-372', # 昭和湯
    # 'item-cnt-373', # 上越泉
    # 'item-cnt-374', # 大和湯
    # 'item-cnt-375', # 中野寿湯温泉
    # 'item-cnt-376', # 新越泉
    # 'item-cnt-378', # 一の湯
    # 'item-cnt-379', # 江古田湯
    'item-cnt-380', # 弁天湯
    'item-cnt-381', # 香藤湯
    'item-cnt-382', # なみのゆ
    'item-cnt-383', # 小杉湯
    'item-cnt-384', # 玉の湯
    'item-cnt-385', # 天徳泉
    'item-cnt-387', # 杉並湯
    'item-cnt-388', # ゆ家和ごころ 吉の湯
    'item-cnt-390', # 桜湯
    'item-cnt-391', # 藤乃湯
    'item-cnt-392', # 第二宝湯
    'item-cnt-393', # 井草湯
    'item-cnt-394', # 亀の湯
    'item-cnt-395', # 秀の湯
    'item-cnt-396', # 文化湯
    'item-cnt-398', # 天狗湯
    'item-cnt-399', # ＧＯＫＵＲＡＫＵＹＡ
    'item-cnt-400', # 湯の楽代田橋
    'item-cnt-401', # 大黒湯
    'item-cnt-402', # 大和湯
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
        type=int,
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
        [scrape_with_semaphore(TOP + url, f'{url}.html') for url in URLS])

TABLE = str.maketrans('０１２３４５６７８９：−', '0123456789:-')

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
