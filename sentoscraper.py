#!/usr/bin/env python
"""
Usage:
$ sentoscraper.py ID1 ID2 ...

Example:
$ seq 590 598 | xargs sentoscraper.py --cache-dir "$XDG_CACHE_HOME/sento"
item-cnt-590.html       さくら湯 [板橋区]       板橋区板橋3-39-12       都営三田線「板橋区役所前」駅下車、徒歩5分   月曜、木曜      0       15:30-21:00
item-cnt-591.html       金松湯 [板橋区] 板橋区大山東町55-3      東武東上線「大山」駅下車、徒歩2分   火曜    0       15:30-23:30
item-cnt-592.html       第二富士見湯 [板橋区]   板橋区幸町20-5  東武東上線「大山」駅下車、徒歩7分   土曜    0       16:00-24:00日曜、祝日は15時から営業
"""

import asyncio
import re
import os.path
import sys
from argparse import ArgumentParser, Namespace
from collections import namedtuple
from typing import Never, Self, Sequence
from urllib.request import urlopen
from bs4 import BeautifulSoup

__version__ = "2.0.1"

URL_PATTERN = "http://www.1010.or.jp/map/item/item-cnt-{id}"

CACHE_DIR = None


class Sento(
    namedtuple(
        "Sento",
        ["id", "name", "address", "access", "holidays", "has_laundry", "office_hours"],
    )
):
    """TODO: docstring"""

    __slots__ = ()

    def __str__(self: Self) -> str:
        return "\t".join(self[:5]) + "\t" + str(self.has_laundry) + "\t" + self[-1]


def parse_args(args: Sequence[str]) -> Namespace:
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description="A downloader")
    parser.add_argument("--version", action="version", version=__version__)

    parser.add_argument("id", nargs="+", help="numeric ID")

    parser.add_argument(
        "-s", "--semaphore", type=int, default=3, help="the count of the semaphore"
    )

    parser.add_argument(
        "-c", "--cache-dir", help="directory in which cache files to be stored"
    )

    return parser.parse_args(args)


async def fetch(args: Namespace):
    """TODO: docstring"""
    semaphore = asyncio.Semaphore(args.semaphore)

    global CACHE_DIR
    CACHE_DIR = args.cache_dir

    async def scrape_with_semaphore(id: str):
        async with semaphore:
            return await scrape(id)

    return await asyncio.gather(*[scrape_with_semaphore(i) for i in args.id])


def make_url(id: str) -> str:
    return URL_PATTERN.format(id=id)


def make_local_path(url: str) -> str:
    return os.path.basename(url) + ".html"


TABLE = str.maketrans("０１２３４５６７８９：−", "0123456789:-")


async def scrape(id: str) -> Sento:
    """TODO: docstring"""

    url = make_url(id)
    localpath = make_local_path(url)

    global CACHE_DIR
    if CACHE_DIR:
        localpath = os.path.normpath(os.path.join(CACHE_DIR, localpath))

    try:
        with open(localpath, mode="rb") as fin:
            data = fin.read()
    except (IOError, FileNotFoundError):
        with urlopen(url) as fin:
            data = fin.read()
        with open(localpath, mode="wb") as fout:
            fout.write(data)

    def sanitize(text: str) -> str:
        return re.sub(r"\s+", "", text.strip()).translate(TABLE)

    def process_address(text: str) -> str:
        """Remove area code from given address"""
        return sanitize(text[9:])

    bs = BeautifulSoup(data, "lxml")

    def get_name_from_heading() -> str:
        if heading := bs.find("h2"):
            return heading.text
        raise ValueError()

    def has_laundry() -> bool:
        return bool(bs.find("a", string="コインランドリー"))

    def get_column_value(propname: str):
        tag = bs.find(string=propname)
        if not tag:
            raise ValueError()
        column = tag.find_next("td")
        if not column:
            raise ValueError()
        return column.text

    sento = Sento(
        id=localpath,
        name=get_name_from_heading(),
        has_laundry=1 if has_laundry() else 0,
        address=process_address(get_column_value("住所")),
        access=sanitize(get_column_value("アクセス")),
        holidays=sanitize(get_column_value("休日")),
        office_hours=sanitize(get_column_value("営業時間")),
    )

    return sento


def run(args: Namespace) -> int:
    """The main function"""

    try:
        loop = asyncio.new_event_loop()
        results = loop.run_until_complete(fetch(args))
        for i in sorted(results):
            print(i)
    finally:
        loop.close()

    return 0


def main(args: Sequence[str] = sys.argv[1:]) -> Never:
    """TODO: docstring"""
    sys.exit(run(parse_args(args)))


if __name__ == "__main__":
    main()
