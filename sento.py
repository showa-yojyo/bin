#!/usr/bin/env python
"""sento.py: List bath houses in KU of Tokyo"""

from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Sequence

from urllib import parse, request

from bs4 import BeautifulSoup, Tag  # type: ignore
import click

__version__ = "1.4"

CSV_HEADER = (
    "名前",
    "位置",
    "アクセス",
    "定休日",
    "コインランドリー",
    "営業時間",
)
SEP = "|"
URL = "http://www.1010.or.jp/map/archives/area/{ku}/page/{page:d}"


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

    click.echo(SEP.join(CSV_HEADER))
    return await asyncio.gather(
        *[scrape(URL.format(ku=ku, page=i + 1)) for i in range(page)]
    )


async def scrape(url) -> None:
    """Scrape the page located in url"""

    soup: BeautifulSoup
    with request.urlopen(url) as html:
        soup = BeautifulSoup(html, "html.parser")

    for j in soup.find_all("div", attrs={"class": "item"}):
        click.echo(SEP.join(parse_item(j)))


@click.command()
@click.argument("ku")
@click.argument("page", type=int)
@click.help_option(help="show this help message and exit")
@click.version_option(__version__, help="show the version and exit")
def main(ku: str, page: int) -> None:
    """List bath houses in KU of Tokyo.

    \b
    Example:
    $ sento 足立区 1
    """

    asyncio.run(fetch(parse.quote(ku), page))


if __name__ == "__main__":
    main()
