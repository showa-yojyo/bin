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
XPATH_BEST_MAHJONG = """
//a[contains(text(), '倍満')
 or contains(text(), '三倍満')
 or contains(text(), '役満')]
"""

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
        """Navigate to the page 東風戦プロ卓"""

        ext = LinkExtractor(restrict_text='東風戦')
        links = ext.extract_links(response)
        if len(links) == 1:
            self.logger.info('Something went wrong')
            inspect_response(response, self)
            return

        yield response.follow(links[-1].url, self._tompu_pro)

    def _tompu_pro(self, response):
        """Navigate to the daily record page"""

        ext = LinkExtractor(restrict_text='デイリー戦績')
        links = ext.extract_links(response)
        yield response.follow(links[0].url, self.parse_daily_score)

    def parse_daily_score(self, response):
        """Scraping method"""

        scraped_data = format_data(response.css(
            'body > div > div.contents-wrap > div.common-wrap *::text'))
        print(scraped_data)

        if links := response.xpath(XPATH_BEST_MAHJONG):
            yield response.follow(links[0].url, self.parse_best_mahjong)
        else:
            self.logger.debug('倍満以上なし終了')

    def parse_best_mahjong(self, response):
        """TODO: 跳満以上のアガリがある場合にはリンク先のスクリーンショットを保存する (very hard)
        """
        inspect_response(response, self)
        # 不正なアクセスを検知しました
        #import webbrowser
        #webbrowser.open(response.url)

# 00
# ...
# 14 【SCORE】
# 15 合計SCORE:-197.0
# 16
# 17
# 18 【最終段位】
# 19 四人打ち段位:魔神 幻球:7
# 20
# 21
# 22 【3/9の最新8試合の履歴】
# 23
# 24 1st|--------
# 25 2nd|--*-*---
# 26 3rd|**---*--
# 27 4th|---*--**
# 28 old         new
# 29
# 30
# 31
# 32 【順位】
# 33 1位回数:0(0.00%)
# 34 2位回数:2(25.00%)
# 35 3位回数:3(37.50%)
# 36 4位回数:3(37.50%)
# 37 平均順位:3.13
# 38
# 39 プレイ局数:40局
# 40
# 41
# 42 【打ち筋】
# 43 アガリ率:10.00%(4/40)
# 44 平均アガリ翻:3.25翻
# 45 平均アガリ巡目:12.75巡
# 46 振込み率:20.00%(8/40)
# 47
# 48
# 49 【3/9の最高役】
# 50 最高役のデータがありません。最高役は、跳満以上のアガリが対象となります。
# ...
def format_data(selector_list):
    contents = [s.get().strip() for s in selector_list[:50]]
    bests = [s.get().strip() for s in selector_list[50:] if s.re(r'役満|三倍満|倍満|跳満')]

    if bests:
        last = '\n'.join(f'・{name}' for name in bests)
    else:
        last = '最高役のデータがありません。最高役は、跳満以上のアガリが対象となります。'

    return f'''
{contents[14]}
{contents[15]}

{contents[18]}
{contents[19]}

{contents[22]}

{contents[24]}
{contents[25]}
{contents[26]}
{contents[27]}
{contents[28].replace(chr(0xa0), " ")}

{contents[32]}
{contents[33]}
{contents[34]}
{contents[35]}
{contents[36]}
{contents[37]}

{contents[39]}

{contents[42]}
{contents[43]}
{contents[44]}
{contents[45]}
{contents[46]}

{contents[49]}
{last}
'''

def main():
    """Receive account information and run spider"""

    user_id = input('Enter user id for MJ.NET: ')
    password = getpass('Enter password: ')
    cmdline.execute(f"scrapy runspider {sys.argv[0]} -a uid={user_id} -a password={password}".split())

if __name__ == '__main__':
    main()
