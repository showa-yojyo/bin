#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Find Twitter users.

Examples:
  $ findusers.py <query> --page=0:5
"""

from secret import twitter_instance
from secret import format_user
from secret import get_user_csv_format
from argparse import ArgumentParser
from argparse import ArgumentTypeError
import re
import sys
import time

__version__ = '1.0.0'

def parse_page_range(text):
    """Parse a range of numbers in the form of M, M:N, or M:.

    http://stackoverflow.com/questions/6512280/
    Accept a range of numbers in the form of 0-5 using Python's argparse?

    Args:
      text (str): A text that represents a range of numbers.

    Returns:
      (range): A range instance.
    """
    m = re.match(r'(\d+)(?::(\d+))?$', text)
    if not m:
        raise ArgumentTypeError(
            '"{}" is not a range of number.'
            'Expected forms like 0-5 or 2.'.format(text))

    start = m.group(1)
    end = m.group(2) or start
    return range(int(start,10), int(end,10)+1)

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """
    parser = ArgumentParser(description='Twitter Users Finder')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        'query',
        help='the search query to run against people search')
    parser.add_argument(
        '-p', '--page-range',
        type=parse_page_range,
        nargs='?',
        default=range(1),
        help='the page ranges of results to retrieve')
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        default=20,
        choices=range(1, 21),
        help='the number of potential user results to retrieve per page')

    return parser

def main():
    """The main function.

    Returns:
        None.
    """

    parser = configure()
    args = parser.parse_args()

    tw = twitter_instance()

    print(get_user_csv_format())

    # Only the first 1,000 matching results are available.
    for i in args.page_range:

        if i != 0:
            time.sleep(2)

        print("{}: Wait...".format(i), file=sys.stderr, flush=True)

        response = tw.users.search(
            q=args.query,
            page=i,
            count=args.count,
            include_entities=False)

        print("{}: OK:".format(i), file=sys.stderr, flush=True)
        for j in response:
            print(format_user(j))

if __name__ == '__main__':
    main()
