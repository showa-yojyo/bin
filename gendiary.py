#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""gendiary.py: Generate a blank diary for a month.

Usage:
  $ gendiary.py [--help] [--version]
  $ gendiary.py [-y | --year <YYYY>] [-m | --month <MM>]
    [-o | --output <FILE>]

Examples:
  You can generate diary template of the current month with no arguments::

    $ gendiary.py

  With --year and --month options, you can generate diary templates of
  any months in any years, e.g.::

    $ genduary.py --year=2014 --month=9

  With --output option, the result will be written to specified file.

    $ gendiary.py --year=2015 --month=12 --output=~/diary/12.html

"""

import sys
import datetime
from calendar import Calendar
from argparse import ArgumentParser, FileType
from jinja2 import Environment

__version__ = '1.2.1'

DIARY_TEMPLATE = """\
{#-
Args:
    year: A year.
    month: A month number (1, 2, ..., 12).
    dates: calendar.Calendar.itermonthdays2(year, month)
-#}

{#- Constants -#}
{%- set dows = ("Mon","Tue","Wed","Thu","Fri","Sat","Sun") -%}
{%- set monthnames = ("","jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec") -%}
{%- set monname = monthnames[month] -%}
{%- set mymail = "showa_yojyo@hotmail.com" -%}
{%- set myurl = "http://www.geocities.jp/showa_yojyo/" -%}

{#- Macro diary_link

    Use for header, footer and crumbs.
-#}
{%- macro diary_link() -%}
<a href="../index.html" title="index">日記</a> &gt;
{{ year }} 年 &gt;
{{ "%02d"|format(month) }} 月
{%- endmacro -%}

{#- Here is the template body. -#}

<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja">
<head>
  <title>日記 {{ year }}/{{ "%02d"|format(month) }}</title>
  <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
  <meta http-equiv="Content-style-type" content="text/css" />
  <meta name="author" content="{{ mymail }}" />
  <link rel="index" type="text/html" href="{{ myurl }}" />
  <link rel="stylesheet" href="../diary.css" type="text/css" />
  <link rel="stylesheet" href="../buf2html.css" type="text/css" />
</head>
<body>
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
<hr />
{{ diary_link() }}
<br />
<address>プレハブ小屋管理人<a href="mailto:{{ mymail }}?subject=diary.{{ year }}.{{ "%02d"|format(month) }}">{{ mymail }}</a></address>
</body>
</html>
"""

# pylint: disable=too-few-public-methods
class MyFileType(FileType):
    """Unfortunately, argparse.FileType does not accept newline
    parameter.
    """

    def __call__(self, path):
        if path == ':':
            return super.__call__(self, path)

        try:
            return open(path, self._mode, self._bufsize,
                        self._encoding, self._errors, newline='\n')
        finally:
            pass

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='Diary Template Generator')
    parser.add_argument('--version', action='version', version=__version__)

    today = datetime.date.today()

    # Optional arguments.
    parser.add_argument(
        '-y', '--year',
        type=int,
        default=today.year,
        help="specify the year of diary (default to today's year)")

    parser.add_argument(
        '-m', '--month',
        type=int,
        default=today.month,
        help="specify the month number of diary (default to today's month)")

    parser.add_argument(
        '-o', '--output',
        type=MyFileType('w', encoding='utf-8'),
        default=sys.stdout,
        metavar='FILE',
        help='write result to FILE instead of standard output')

    return parser

def main():
    """The main function."""

    args = configure().parse_args()

    year = args.year
    month = args.month
    output = args.output

    output.write(
        Environment(autoescape=False).from_string(DIARY_TEMPLATE).render(
            year=year,
            month=month,
            dates=Calendar().itermonthdays2(year, month)))
    output.write('\n')

if __name__ == "__main__":
    main()
