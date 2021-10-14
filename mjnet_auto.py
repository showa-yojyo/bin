#!/usr/bin/env python

"""
Sign in MJ.NET and scrape today's result.
"""

from getpass import getpass
import sys
from scrapy import cmdline, Spider, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.shell import inspect_response

MJ_NET_URL = 'https://www.sega-mj.net/mjac_p'
MJ_NET_URL_SIGN_IN = f'{MJ_NET_URL}/mjlogin/login.jsp'
MJ_NET_URL_SIGN_IN_DO = f'{MJ_NET_URL}/login.do'
MJ_NET_URL_SIGN_OUT = f'{MJ_NET_URL}/FwdPage?page=logout'
MJ_NET_URL_TOP_PAGE = f'{MJ_NET_URL}/FwdPage?page=top'
MJ_NET_URL_PLAYER_DATA_PAGE = f'{MJ_NET_URL}/FwdPage?page=playdata&i=0'

# TODO: When XPath upgrades to 2.0, use the function matches() instead of contains().
XPATH_BEST_MAHJONG = "//a[text()[contains(., '倍満') or contains(., '三倍満') or contains(., '役満')]]"

# 一般卓東風戦
GAME_MODE_STANDARD = 'standard'
# プロ卓東風戦
GAME_MODE_PROFESSIONAL = 'professional'

class MjscoreSpider(Spider):
    """MJ.NET"""

    name = 'mjnet'
    allowed_domains = ['www.sega-mj.net']
    start_urls = [MJ_NET_URL_SIGN_IN]

    def parse(self, response, **kwargs):
        """Pass the login page of MJ.NET"""

        return FormRequest.from_response(
            response,
            formdata={
                'uid': getattr(self, 'uid'),
                'password': getattr(self, 'password')},
            callback=self._after_login)

    def _after_login(self, response):
        """Nagivate to the top page"""

        self.logger.info('_after_login')
        self.logger.info(response.url)

        if response.url == MJ_NET_URL_SIGN_IN_DO:
            yield response.follow(MJ_NET_URL_TOP_PAGE, self._top_page)
        else:
            yield response.follow(MJ_NET_URL_SIGN_IN_DO, self._after_login)

    def _top_page(self, response):
        """Navigate to the player data page"""

        yield response.follow(MJ_NET_URL_PLAYER_DATA_PAGE, self._play_data)

    def _play_data(self, response):
        """Navigate to the page 一般卓東風戦 or プロ卓東風戦"""

        ext = LinkExtractor(restrict_text='東風戦')
        links = ext.extract_links(response)
        if len(links) == 1:
            self.logger.info('Something went wrong')
            inspect_response(response, self)
            return

        game_mode = getattr(self, 'game_mode'),
        if game_mode == GAME_MODE_PROFESSIONAL:
            link_index = -1
        else:
            link_index = 0
        yield response.follow(links[link_index].url, self._tompu_games)

    def _tompu_games(self, response):
        """Navigate to the daily record page"""

        ext = LinkExtractor(restrict_text='デイリー戦績')
        links = ext.extract_links(response)
        yield response.follow(links[0].url, self.parse_daily_score)

    def parse_daily_score(self, response):
        """Scraping method"""

        item = {}
        selector = response.selector
        parse_score(selector, item)
        parse_recent_level(selector, item)
        parse_history(selector, item)
        parse_ranks(selector, item)
        parse_stats(selector, item)
        parse_best(selector, item)

        yield item

        if link := response.xpath(XPATH_BEST_MAHJONG).get():
            yield response.follow(link, self.parse_best_mahjong)
        else:
            self.logger.debug('倍満以上なし終了')

    def parse_best_mahjong(self, response):
        """TODO: 跳満以上のアガリがある場合にはリンク先のスクリーンショットを保存する (very hard)
        """
        inspect_response(response, self)
        # 不正なアクセスを検知しました
        #import webbrowser
        #webbrowser.open(response.url)

# 【SCORE】
# 合計SCORE:-197.0
def parse_score(selector, item):
    """Parse 【SCORE】"""

    value = selector.xpath('//font[text() = "【SCORE】"]/following::text()').get()
    item['score'] = value.strip()

    print("【SCORE】")
    print(item['score'])
    print()

# 【最終段位】
# 四人打ち段位:魔神 幻球:7
def parse_recent_level(selector, item):
    """Parse 【最終段位】"""

    value = selector.xpath('//font[text() = "【最終段位】"]/following::text()').get()
    item['recent_level'] = value.strip()

    print("【最終段位】")
    print(item['recent_level'])
    print()

# 【3/9の最新8試合の履歴】
#
# 1st|--------
# 2nd|--*-*---
# 3rd|**---*--
# 4th|---*--**
# old         new
def parse_history(selector, item):
    """Parse 【m/dの最新8試合の履歴】"""

    title = selector.xpath('//font[contains(.,"履歴")]/text()').get().strip()

    values = selector.xpath('//text()[preceding::font[contains(.,"履歴")]][following::font[text()="【順位】"]]').getall()
    item['history'] = '\n'.join(istripped for i in values if (istripped := i.strip())).replace('\nE', 'E')

    print(title)
    print(item['history'])
    print()

# 【順位】
# 1位回数:0(0.00%)
# 2位回数:2(25.00%)
# 3位回数:3(37.50%)
# 4位回数:3(37.50%)
# 平均順位:3.13
#
# プレイ局数:40局
def parse_ranks(selector, item):
    """Parse 【順位】"""

    values = selector.xpath('//font[contains(.,"順位")]/following::text()[position() < 8]').getall()
    item['rank'] = '\n'.join(i.strip() for i in values)

    print("【順位】")
    print(item['rank'])
    print()

# 【打ち筋】
# アガリ率:10.00%(4/40)
# 平均アガリ翻:3.25翻
# 平均アガリ巡目:12.75巡
# 振込み率:20.00%(8/40)
def parse_stats(selector, item):
    """Parse 【打ち筋】"""

    values = selector.xpath('//font[text() = "【打ち筋】"]/following::text()[position() < 5]').getall()
    item['stats'] = '\n'.join(istripped for i in values if (istripped := i.strip()))

    print("【打ち筋】")
    print(item['stats'])
    print()

# 【3/9の最高役】--> //font[contains(.,"最高役")]/following-sibling::text()
# 最高役のデータがありません。最高役は、跳満以上のアガリが対象となります。
def parse_best(selector, item):
    """Parse 【m/dの最高役】"""

    title = selector.xpath('//font[contains(.,"最高役")]/text()').get().strip()

    # TODO: まだよくわからない
    #values = selector.xpath('//font[contains(.,"最高役")]/following-sibling::text()').getall()
    values = selector.xpath('//text()[preceding::font[contains(.,"最高役")]][following::hr]').getall()
    item['best'] = '\n'.join(istripped for i in values if (istripped := i.strip()))

    print(title)
    print(item['best'])
    print()

def main():
    """Receive account information and run spider"""

    game_mode = GAME_MODE_PROFESSIONAL
    if len(sys.argv) == 2 and sys.argv[1] == '--standard':
        game_mode = GAME_MODE_STANDARD

    user_id = input('Enter user id for MJ.NET: ')
    password = getpass('Enter password: ')
    cmdline.execute(f"scrapy runspider {sys.argv[0]} -a uid={user_id} -a password={password} -a game_mode={game_mode}".split())

if __name__ == '__main__':
    main()
