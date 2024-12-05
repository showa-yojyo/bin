#!/usr/bin/env python
"""sento.py: List bath houses in KU of Tokyo"""

import asyncio
import sys
from argparse import ArgumentParser, Namespace
from typing import Never, Sequence
from urllib import parse, request

from bs4 import BeautifulSoup, Tag  # type: ignore

__version__ = "1.3.1"

URL = "http://www.1010.or.jp/map/archives/area/{ku}/page/{page:d}"


def parse_args(args: Sequence[str]) -> Namespace:
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description="List bath houses in KU of Tokyo")
    parser.add_argument("--version", action="version", version=__version__)

    parser.add_argument(
        "ku",
        metavar="KU",
        default="北区",
        help="ku (ward) in which bath houses to be searched",
    )
    parser.add_argument(
        "page", default=1, type=int, help="the number of pages to be searched"
    )

    return parser.parse_args(args or ["--help"])


def parse_item(item: Tag) -> Sequence[str]:
    """Return name, location, holiday and office hours"""

    def get_column_value(item: Tag, propname: str) -> str:
        prop = item.find(string=propname)
        if prop:
            column = prop.find_next("td")
            if isinstance(column, Tag):
                return column.text.strip()
        raise ValueError()

    def has_laundry(item: Tag) -> bool:
        return bool(item.find(string="コインランドリー"))

    info = item.find("div", class_="info")
    if isinstance(info, Tag):
        if a := info.select_one("div[class=info]>h2>a"):
            name: str = a.text

    location: str = "TODO"
    access: str = get_column_value(item, "アクセス")
    holidays: str = get_column_value(item, "休日")
    laundry: str = "1" if has_laundry(item) else "0"
    office_hours: str = get_column_value(item, "営業時間")

    return [name, location, access, holidays, laundry, office_hours]


async def fetch(ku: str, page: int):
    """Fetch all the data"""
    return await asyncio.gather(
        *[scrape(URL.format(ku=ku, page=i + 1)) for i in range(page)]
    )


async def scrape(url) -> None:
    """Scrape the page located in url"""

    soup: BeautifulSoup
    with request.urlopen(url) as html:
        soup = BeautifulSoup(html, "html.parser")

    for j in soup.find_all("div", attrs={"class": "item"}):
        print("|".join(parse_item(j)))


def run(args: Namespace) -> int:
    """The main function"""

    print(
        "|".join(("名前", "位置", "アクセス", "定休日", "コインランドリー", "営業時間"))
    )

    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(fetch(parse.quote(args.ku), args.page))
    finally:
        loop.close()

    return 0


def main(args: Sequence[str] = sys.argv[1:]) -> Never:
    sys.exit(run(parse_args(args)))


if __name__ == "__main__":
    main()
