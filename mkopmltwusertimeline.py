# -*- coding: utf-8 -*-
u"""
Copyright (c) 2012 プレハブ小屋 <yojyo@hotmail.com>
All Rights Reserved.  NO WARRANTY.

Twitter の user_timeline を ATOM で購読する OPML ファイルを生成する。
"""

import urllib
import cgi
from jinja2 import Environment

TWITTER_API_URL = 'https://api.twitter.com/1/statuses/user_timeline.atom?'

OPML_TEMPLATE = u'''\
<?xml version="1.0" encoding="utf-8"?>
<opml version="1.0">
  <head>
    <title>RSS Bar</title>
    <dateCreated></dateCreated>
    <dateModified></dateModified>
  </head>
  <body>
  {%- for screen_name in screen_names %}
    {%- set url=screen_name|makeurl %}
    <outline type="rss" text="{{ screen_name }}" title="{{ screen_name }}" xmlUrl="{{ url }}" htmlUrl="{{ url }}"/>
  {%- endfor %}
  </body>
</opml>
'''

def makeurl(screen_name):
    doseq = dict(
        screen_name=screen_name,
        count=30,
        include_rts='true',
        )
    return cgi.escape(TWITTER_API_URL + urllib.urlencode(doseq))

def run():
    # TODO: ここをしょっちゅう書き換える必要があるのは面倒。
    screen_names = (
        'showa_yojyo',
        # ...
        )
    if not screen_names:
        return

    env = Environment()
    env.filters['makeurl'] = makeurl
    template = env.from_string(OPML_TEMPLATE)
    print template.render(screen_names=screen_names)

if __name__ == '__main__':
    run()
