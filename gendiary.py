# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014 プレハブ小屋 <yojyo@hotmail.com>
# All Rights Reserved.  NO WARRANTY.

"""Generate an HTML document for diary of a month."""

import sys
import codecs
import datetime
from calendar import Calendar
from argparse import ArgumentParser
from jinja2 import Environment

__version__ = '0.0.1'

DIARY_ENCODING = "utf-8"

DIARY_TEMPLATE = """\
{#-
render の引数
-------------
year: 西暦 4 桁整数
month: 月
dates: calendar.Calendar.itermonthdays2(year, month)
-#}

{#- 変数 -#}
{%- set dows = ("Mon","Tue","Wed","Thu","Fri","Sat","Sun") -%}
{%- set monthnames = ("","jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec") -%}
{%- set monname = monthnames[month] -%}

{#- マクロ diary_link

    HTML の上部と下部、パンクズに使う。
-#}
{%- macro diary_link() -%}
<a href="../index.html" title="index">日記</a> &gt;
{{ year }} 年 &gt;
{{ "%02d"|format(month) }} 月
{%- endmacro -%}

{#- ここからテンプレート本体 -#}

<?xml version="1.0" encoding="{{ encoding }}" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja">
<head>
  {% block header %}
  <title>日記 {{ year }}/{{ "%02d"|format(month) }}</title>
  <meta http-equiv="Content-type" content="text/html; charset={{ encoding }}" />
  <meta http-equiv="Content-style-type" content="text/css" />
  <meta name="author" content="showa_yojyo@hotmail.com" />
  <link rel="index" type="text/html" href="http://www.geocities.jp/showa_yojyo/index.html" />
  <link rel="stylesheet" href="../diary.css" type="text/css" />
  <link rel="stylesheet" href="../buf2html.css" type="text/css" />
  {% endblock %}
</head>
<body>
{% block body %}
<p>
{{ diary_link() }}
</p>
<hr />
{{ '<h3 id="diary.%d.%s">%d 年 %02d 月</h3>'|format(year, monname, year, month) }}
{%- for date in dates %}
{%- if date[0] %}
{%- set sectid = 'diary.%d.%s.%d'|format(year, monname, date[0]) %}
{%- set secttitle = '%d/%02d/%02d (%s)'|format(year, month, date[0], dows[date[1]]) %}
<div title="{{ sectid }}">
<h4 id="{{ sectid }}" class="Date">{{ secttitle }}</h4>
<pre class="Diary">

</pre>
</div> <!-- {{ sectid }} -->
{% endif %}
{%- endfor %}
{% endblock %}
<hr />
{% block footer %}
{{ diary_link() }}
<br />
<address>プレハブ小屋管理人<a href="mailto:yojyo@hotmail.com?subject=diary.{{ year }}.{{ "%02d"|format(month) }}">yojyo@hotmail.com</a></address>
{% endblock %}
</body>
</html>
"""

def main(args):
    year = args.year
    month = args.month
    env = Environment(autoescape = False)
    templ = env.from_string(DIARY_TEMPLATE)

    cal = Calendar()

    sys.stdout = codecs.getwriter(DIARY_ENCODING)(sys.stdout)
    sys.stdout.write(templ.render(
        encoding=DIARY_ENCODING,
        year=year,
        month=month,
        dates=cal.itermonthdays2(year, month),
        ))
    sys.stdout.write('\n')

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__, version=__version__)
    today = datetime.date.today()

    parser.add_argument('-y', '--year',
                        type=int,
                        default=today.year,
                        dest='year',
                        help="year of diary (default to today's year)")
    parser.add_argument('-m', '--month',
                        type=int,
                        default=today.month,
                        dest='month',
                        help="month of diary (default to today's month)")

    args = parser.parse_args()
    main(args)
