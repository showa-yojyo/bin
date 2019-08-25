#!/usr/bin/env python
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

    $ gendiary.py --year=2014 --month=9

"""

import sys
import datetime
from calendar import Calendar
from argparse import ArgumentParser
from jinja2 import Environment

__version__ = '2.1.0'

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
{%- set mymail = "yojyo@hotmail.com" -%}
{%- set myurl = "../index.html" -%}

{#- Macro diary_link

    Use for header, footer and crumbs.
-#}
{%- macro diary_link() -%}
  <nav>
    <a href="../index.html" title="index">日記</a> &gt;
    {{ year }} 年 &gt;
    {{ "%02d"|format(month) }} 月
  </nav>
{%- endmacro -%}

{#- Here is the template body. -#}

<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="author" content="{{ mymail }}" />
  <title>日記 {{ year }}/{{ "%02d"|format(month) }}</title>
  <link rel="index" href="{{ myurl }}" />
  <link rel="stylesheet" href="../diary-html5.css" />
</head>
<body>
  <header>
    {{ diary_link() }}
    {{ '<h1 id="diary.%d.%s">%d 年 %02d 月</h3>'|format(year, monname, year, month) }}
  </header>

  <section>
{%- for date in dates %}
{%- if date[0] %}
{%- set article_id = 'diary.%d.%s.%d'|format(year, monname, date[0]) %}
{%- set datetime_repr = '%d-%02d-%02d'|format(year, month, date[0]) %}
{%- set article_time = '%d/%02d/%02d (%s)'|format(year, month, date[0], dows[date[1]]) %}
    <article id="{{ article_id }}">
      <header>
        <time datetime="{{ datetime_repr }}">{{ article_time }}</time>
      </header>
      <pre class="Diary">

      </pre>
    </article> <!-- {{ article_id }} -->
{% endif %}
{%- endfor %}
  </section>

  <footer>
    {{ diary_link() }}
    <address>プレハブ小屋管理人<a href="mailto:{{ mymail }}?subject=diary.{{ year }}.{{ "%02d"|format(month) }}">{{ mymail }}</a></address>
  </footer>
</body>
</html>
"""

def parse_args(args):
    """Parse the command line parameters."""

    parser = ArgumentParser(
        description='Diary Template Generator',
        epilog='Mail bug reports and suggestions to <yojyo@hotmail.com>',
        add_help=False)
    # Startup:
    startup_group = parser.add_argument_group('Startup')
    startup_group.add_argument(
        '-V', '--version',
        action='version',
        version=__version__)
    startup_group.add_argument(
        '-h', '--help',
        action='help',
        help='print this help')

    today = datetime.date.today()

    # Calendar:
    calendar_group = parser.add_argument_group('Calendar')
    calendar_group.add_argument(
        '-y', '--year',
        type=int,
        default=today.year,
        help="the year of diary (default to today's year)")
    calendar_group.add_argument(
        '-m', '--month',
        type=int,
        default=today.month,
        help="the month number of diary (default to today's month)")

    return parser.parse_args(args)

def main(args=sys.argv[1:]):
    """The main function."""
    sys.exit(run(parse_args(args)))

def run(args):
    """The main function."""

    year = args.year
    month = args.month
    print(
        Environment(autoescape=False).from_string(DIARY_TEMPLATE).render(
            year=year,
            month=month,
            dates=Calendar().itermonthdays2(year, month)))

if __name__ == "__main__":
    main()
