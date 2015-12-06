#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""twformat.py: prototype

Usage:
  twformat.py [--version] [--help]
  twformat.py [FILE]...
"""

__version__ = '0.0.0'

import sys
from argparse import ArgumentParser
from argparse import FileType
from json import load

def make_parser():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        'files',
        nargs='*',
        default=sys.stdin,
        type=FileType('r', encoding='utf-8'),
        help='JSON files to format')

    return parser

def format_json(inputs):
    # users/search
    # lists/members
    csv_header = (
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
    csv_format = '\t'.join(('{' + i + '}' for i in csv_header))
    csv_format_w = '\t'.join(('{' + i + '}' for i in csv_header[:-2]))

    for fp in inputs:
        json_obj = load(fp)
        for i in json_obj:
            if 'status' in i:
                fmt = csv_format
            else:
                fmt = csv_format_w
            print(fmt.format(**i).replace('\r', '').replace('\n', '\\n'))

def main(params=sys.argv[1:]):
    parser = make_parser()
    args = parser.parse_args(params)
    format_json(args.files)

if __name__ == '__main__':
    main()
