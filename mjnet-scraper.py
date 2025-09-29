#!/usr/bin/env python

"""
Sign in MJ.NET and scrape today's result.
"""

from __future__ import annotations

import os
import pathlib
import sys
from string import Template
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import MutableMapping

import click
import yaml  # type: ignore[import-untyped]
from scrapy import FormRequest, Spider, cmdline
from scrapy.http import TextResponse  # type: ignore[attr-defined]
from scrapy.linkextractors import LinkExtractor  # type: ignore[attr-defined]
from scrapy.shell import inspect_response

if TYPE_CHECKING:
    from scrapy.http import Response  # type: ignore[attr-defined]
    from scrapy.selector import Selector  # type: ignore[attr-defined]

__version__ = "2.1.1"

APP_NAME = "mjnet-scraper"

DEFAULT_CREDENTIALS_PATH = (
    f"$XDG_CONFIG_HOME/{APP_NAME}/{APP_NAME}.yaml",
    f"$HOME/.config/{APP_NAME}/{APP_NAME}.yaml",
    f"$HOME/.{APP_NAME}/{APP_NAME}.yaml",
    f"$HOME/{APP_NAME}.yaml",
)

HEADING_COLOR = "bright_green"

MJ_NET_URL = "https://www.sega-mj.net/mjac_p"
MJ_NET_URL_SIGN_IN = f"{MJ_NET_URL}/mjlogin/login.jsp"
MJ_NET_URL_SIGN_IN_DO = f"{MJ_NET_URL}/login.do"
MJ_NET_URL_SIGN_OUT = f"{MJ_NET_URL}/FwdPage?page=logout"
MJ_NET_URL_TOP_PAGE = f"{MJ_NET_URL}/FwdPage?page=top"
MJ_NET_URL_PLAYER_DATA_PAGE = f"{MJ_NET_URL}/FwdPage?page=playdata&i=0"

# TODO: When XPath upgrades to 2.0, use the function matches() instead of contains().
XPATH_BEST_MAHJONG = (
    "//a[text()[contains(., '倍満') or contains(., '三倍満') or contains(., '役満')]]"
)

# 一般卓東風戦
GAME_MODE_STANDARD = "standard"
# プロ卓東風戦
GAME_MODE_PROFESSIONAL = "professional"


class MJScoreSpider(Spider):
    """MJ.NET"""

    name = APP_NAME
    allowed_domains = ["www.sega-mj.net"]
    start_urls = [MJ_NET_URL_SIGN_IN]

    def parse(self, response: Response, **_kwargs: object) -> object:
        """Pass the login page of MJ.NET"""

        assert isinstance(response, TextResponse)

        return FormRequest.from_response(
            response,
            formdata={
                "uid": getattr(self, "uid"),
                "password": getattr(self, "password"),
            },
            callback=self._after_login,
        )

    def _after_login(
        self,
        response: Response,
        *_args: object,
        **_kwargs: object,
    ) -> object:
        """Nagivate to the top page"""

        self.logger.info("_after_login")
        self.logger.info(response.url)

        if response.url == MJ_NET_URL_SIGN_IN_DO:
            yield response.follow(
                MJ_NET_URL_TOP_PAGE,
                self._top_page,  # type: ignore[arg-type]
            )
        else:
            yield response.follow(
                MJ_NET_URL_SIGN_IN_DO,
                self._after_login,  # type: ignore[arg-type]
            )

    def _top_page(
        self,
        response: Response,
        *_args: object,
        **_kwargs: object,
    ) -> object:
        """Navigate to the player data page"""

        yield response.follow(
            MJ_NET_URL_PLAYER_DATA_PAGE,
            self._play_data,  # type: ignore[arg-type]
        )

    def _play_data(
        self,
        response: Response,
        *_args: object,
        **_kwargs: object,
    ) -> object:
        """Navigate to the page 一般卓東風戦 or プロ卓東風戦"""

        assert isinstance(response, TextResponse)

        ext = LinkExtractor(restrict_text="東風戦")
        links = ext.extract_links(response)
        if len(links) == 1:
            self.logger.info("Something went wrong")
            inspect_response(response, self)
            return

        link_index = -1 if getattr(self, "game_mode") == GAME_MODE_PROFESSIONAL else 0
        yield response.follow(
            links[link_index].url,
            self._tompu_games,  # type: ignore[arg-type]
        )

    def _tompu_games(
        self,
        response: Response,
        *_args: object,
        **_kwargs: object,
    ) -> object:
        """Navigate to the daily record page"""

        if isinstance(response, TextResponse):
            ext = LinkExtractor(restrict_text="デイリー戦績")
            links = ext.extract_links(response)
            yield response.follow(
                links[0].url,
                self.parse_daily_score,  # type: ignore[arg-type]
            )

    def parse_daily_score(
        self,
        response: Response,
        *_args: object,
        **_kwargs: object,
    ) -> object:
        """Scraping method"""

        assert isinstance(response, TextResponse)

        item: MutableMapping[str, str] = {}
        selector: Selector = response.selector
        parse_score(selector, item)
        parse_recent_level(selector, item)
        parse_history(selector, item)
        parse_ranks(selector, item)
        parse_stats(selector, item)
        parse_best(selector, item)

        yield item


# 【SCORE】
# 合計SCORE:-197.0
def parse_score(selector: Selector, item: MutableMapping[str, str]) -> None:
    """Parse 【SCORE】"""

    value = selector.xpath('//font[text() = "【SCORE】"]/following::text()').get()
    item["score"] = value.strip() if value else ""

    click.secho("【SCORE】", fg=HEADING_COLOR)
    click.echo(item["score"])
    click.echo()


# 【最終段位】
# 四人打ち段位:魔神 幻球:7
def parse_recent_level(selector: Selector, item: MutableMapping[str, str]) -> None:
    """Parse 【最終段位】"""

    value = selector.xpath('//font[text() = "【最終段位】"]/following::text()').get()
    item["recent_level"] = value.strip() if value else ""

    click.secho("【最終段位】", fg=HEADING_COLOR)
    click.echo(item["recent_level"])
    click.echo()


# 【3/9の最新8試合の履歴】
#
# 1st|--------
# 2nd|--*-*---
# 3rd|**---*--
# 4th|---*--**
# old         new
def parse_history(selector: Selector, item: MutableMapping[str, str]) -> None:
    """Parse 【m/dの最新8試合の履歴】"""

    xp = selector.xpath('//font[contains(.,"履歴")]/text()').get()
    title = xp.strip() if xp else ""

    values = selector.xpath(
        '//text()[preceding::font[contains(.,"履歴")]][following::font[text()="【順位】"]]'
    ).getall()
    item["history"] = "\n".join(
        istripped for i in values if (istripped := i.strip())
    ).replace("\nE", "E")

    click.secho(title, fg=HEADING_COLOR)
    click.echo(item["history"])
    click.echo()


# 【順位】
# 1位回数:0(0.00%)
# 2位回数:2(25.00%)
# 3位回数:3(37.50%)
# 4位回数:3(37.50%)
# 平均順位:3.13
#
# プレイ局数:40局
def parse_ranks(selector: Selector, item: MutableMapping[str, str]) -> None:
    """Parse 【順位】"""

    values = selector.xpath(
        '//font[contains(.,"順位")]/following::text()[position() < 8]'
    ).getall()
    item["rank"] = "\n".join(i.strip() for i in values)

    click.secho("【順位】", fg=HEADING_COLOR)
    click.echo(item["rank"])
    click.echo()


# 【打ち筋】
# アガリ率:10.00%(4/40)
# 平均アガリ翻:3.25翻
# 平均アガリ巡目:12.75巡
# 振込み率:20.00%(8/40)
def parse_stats(selector: Selector, item: MutableMapping[str, str]) -> None:
    """Parse 【打ち筋】"""

    values = selector.xpath(
        '//font[text() = "【打ち筋】"]/following::text()[position() < 5]'
    ).getall()
    item["stats"] = "\n".join(istripped for i in values if (istripped := i.strip()))

    click.secho("【打ち筋】", fg=HEADING_COLOR)
    click.echo(item["stats"])
    click.echo()


# 【3/9の最高役】--> //font[contains(.,"最高役")]/following-sibling::text()
# 最高役のデータがありません。最高役は、跳満以上のアガリが対象となります。
def parse_best(selector: Selector, item: MutableMapping[str, str]) -> None:
    """Parse 【m/dの最高役】"""

    xp = selector.xpath('//font[contains(.,"最高役")]/text()').get()
    title = xp.strip() if xp else ""

    # TODO: まだよくわからない
    # values = selector.xpath('//font[contains(.,"最高役")]/following-sibling::text()').getall()
    values = selector.xpath(
        '//text()[preceding::font[contains(.,"最高役")]][following::hr]'
    ).getall()
    item["best"] = "\n".join(
        istripped for i in values if (istripped := i.strip())
    ).replace("・\n", "・")

    click.secho(title, fg=HEADING_COLOR)
    click.echo(item["best"])
    click.echo()


def configure(
    ctx: click.Context,
    param: click.Parameter,
    value: object,
) -> object:
    """Try to read the ID and password."""

    if value:
        assert isinstance(value, pathlib.Path)
        with value.open(mode="r") as fin:
            ctx.default_map = yaml.safe_load(fin)
        return value

    for p in DEFAULT_CREDENTIALS_PATH:
        try:
            with pathlib.Path(Template(p).substitute(os.environ)).open(mode="r") as fin:
                ctx.default_map = yaml.safe_load(fin)
                return value
        except OSError:
            pass

    return value


@click.command()
@click.help_option(
    help="display this message and exit",
)
@click.version_option(
    __version__,
    help="output version information and exit",
)
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, path_type=pathlib.Path),
    default=None,
    metavar="PATH",
    callback=configure,
    is_eager=True,
    expose_value=False,
    help="path to config file",
)
@click.option(
    "-u",
    "--user",
    prompt=True,
    prompt_required=False,
    hide_input=False,
    metavar="NAME",
    help="your user name for MJ.NET account",
)
@click.password_option(
    prompt_required=False,
    metavar="PASSWORD",
    help="your password for MJ.NET account",
)
@click.option(
    "-g",
    "--game-mode",
    type=click.Choice(
        (
            "professional",
            "standard",
        ),
        case_sensitive=False,
    ),
    default="professional",
    help="which mode to scrape プロ卓東風 or 一般卓東風",
)
def main(user: str, password: str, game_mode: str) -> None:
    """Sign in MJ.NET and scrape my stats of last games."""

    command = [
        "scrapy",
        "runspider",
        sys.argv[0],
        "-a",
        f"uid={user}",
        "-a",
        f"password={password}",
        "-a",
        f"game_mode={game_mode}",
        "--nolog",
    ]

    cmdline.execute(command)


if __name__ == "__main__":
    main()
