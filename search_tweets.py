#!/usr/bin/env python
"""Search the latest tweets in Twitter.

Usage:
    $ search_tweets.py QUERY ...
"""

from argparse import (ArgumentParser, FileType)
import sys
from urllib.parse import urlencode
from webbrowser import open_new

__version__ = '1.0.0'

def parse_args(args):
    """Parse the command line parameters."""

    parser = ArgumentParser(description='Search the latest tweets in Twitter')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        'query',
        nargs='+',
        help='query string')

    return parser.parse_args(args or ["--help"])

def run(args):
    """The main function."""

    open_new('https://twitter.com/search?' + urlencode(
        {'q': ' '.join(args.query), 'f': 'tweets'}))

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args)))

if __name__ == '__main__':
    main()
