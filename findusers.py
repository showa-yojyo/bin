#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Find Twitter users.

Usage:
  findusers.py [--version] [--help]
  findusers.py [-p | --page-range <begin>[:<end>]]
    [-c | --count <n>]
    <query>
"""

from secret import twitter_instance
from twmods import SEP
from twmods import USER_COLUMN_HEADER
from twmods import make_logger
from argparse import ArgumentParser
from argparse import ArgumentTypeError
import re
import sys
import time

__version__ = '1.2.3'

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
        metavar='<begin>[:<end>]',
        help='the page ranges of results to retrieve')
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        default=20,
        choices=range(1, 51),
        metavar='{1..50}',
        help='the number of potential user results to retrieve per page')

    return parser

def main():
    """The main function.

    Returns:
        None.
    """

    parser = configure()
    args = parser.parse_args()

    logger = make_logger('findusers')
    tw = twitter_instance()

    csv_header = USER_COLUMN_HEADER + ('status[text]', 'status[source]',)
    csv_format = SEP.join(('{' + i + '}' for i in csv_header))

    print(SEP.join(csv_header))

    # Only the first 1,000 matching results are available.
    for i in args.page_range:
        logger.info("[{:03d}] Waiting...".format(i))

        response = tw.users.search(
            q=args.query,
            page=i,
            count=args.count,
            include_entities=False)

        logger.info("[{:03d}] OK:".format(i))
        for j in response:
            if 'status' in j:
                line = csv_format.format(**j)
                print(line.replace('\r', '').replace('\n', '\\n'))

        time.sleep(2)

if __name__ == '__main__':
    main()
