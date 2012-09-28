# -*- coding: utf-8 -*-
u"""
Copyright (c) 2012 プレハブ小屋 <yojyo@hotmail.com>
All Rights Reserved.  NO WARRANTY.

Twitter による所定の検索結果を ATOM で購読する OPML ファイルを生成する。
"""

import sys
import urllib
import cgi
import codecs
from jinja2 import Environment

TWITTER_SEARCH_URL = 'http://search.twitter.com/search.atom?'

OPML_TEMPLATE = u'''\
<?xml version="1.0" encoding="utf-8"?>
<opml version="1.0">
  <head>
    <title>RSS Bar</title>
    <dateCreated></dateCreated>
    <dateModified></dateModified>
  </head>
  <body>
  {%- for query in queries %}
    {%- set url=query|makeurl %}
    <outline type="rss" text="{{ query|escape }}" title="{{ query|escape }}" xmlUrl="{{ url }}" htmlUrl="{{ url }}"/>
  {%- endfor %}
  </body>
</opml>
'''

def makeurl(query):
    params = dict(
        q=query.encode('utf-8'),
        rpp=30, 
        result_type='recent',
        show_user='true')
    return cgi.escape(TWITTER_SEARCH_URL + urllib.urlencode(params), True)

def run():
    # TODO: ここをしょっちゅう書き換える必要があるのは面倒。
    queries = (
        u'むこうぶち OR 麻雀破壊神',
        u'"トラブル ウィッチーズ" OR トラブルウィッチーズ',
        # ...
        )

    if not queries:
        return
    
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    env = Environment()
    env.filters['makeurl'] = makeurl
    template = env.from_string(OPML_TEMPLATE)
    print template.render(queries=queries)

if __name__ == '__main__':
    run()
