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

    $ genduary.py --year=2014 --month=9

  With --output option, the result will be written to specified file.

    $ gendiary.py --year=2015 --month=12 --output=~/diary/2015/12.html

"""

import sys
import datetime
from calendar import Calendar
from argparse import ArgumentParser, FileType
from jinja2 import Environment

__version__ = '2.0.0'

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

# pylint: disable=too-few-public-methods
class MyFileType(FileType):
    """Unfortunately, argparse.FileType does not accept newline
    parameter.
    """

    def __call__(self, path):
        if path == ':':
            return super.__call__(self, path)

        return open(path, self._mode, self._bufsize,
                    self._encoding, self._errors, newline='\n')

def parse_args(args):
    """Parse the command line parameters."""

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

    return parser.parse_args(args)

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args)))

def run(args):
    """The main function."""

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
