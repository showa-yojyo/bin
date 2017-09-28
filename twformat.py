#!/usr/bin/env python
"""twformat.py: prototype

Usage:
  twformat.py [--version] [--help]
  twformat.py [-L | --logmode] [FILE]...
"""

from argparse import (ArgumentParser, FileType)
from json import load
import sys

__version__ = '0.0.0'

def parse_args(args):
    """Parse the command line parameters."""

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        'files',
        nargs='*',
        default=sys.stdin,
        type=FileType('r', encoding='utf-8'),
        help='JSON files to format')
    parser.add_argument(
        '-L', '--logmode',
        action='store_true',
        help='enable log mode')

    return parser.parse_args(args=args or ('--help',))

# users/search
# lists/members
CSV_HEADER = (
    'id',
    'screen_name',
    'name',
    'protected',
    'lang',
    'location',
    'friends_count',
    'followers_count',
    'description',
    'url',
    'status[text]',
    'status[source]',)

# statuses/user_timeline --trim-user -X
CSV_HEADER_LOG = (
    'id',
    'created_at',
    'text',)

def run(args):
    """TBW"""

    if args.logmode:
        fmt = '\t'.join(('{' + i + '}' for i in CSV_HEADER_LOG))
    else:
        csv_format = '\t'.join(('{' + i + '}' for i in CSV_HEADER))
        csv_format_w = '\t'.join(('{' + i + '}' for i in CSV_HEADER[:-2]))

    for fp in args.files:
        json_obj = load(fp)
        for i in json_obj:
            if not args.logmode:
                if 'status' in i:
                    fmt = csv_format
                else:
                    fmt = csv_format_w
            print(fmt.format(**i).replace('\r', '').replace('\n', '\\n'))

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args)))

if __name__ == '__main__':
    main()
