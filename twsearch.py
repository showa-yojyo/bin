#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Find Twitter tweets.

Usage:
  twsearch.py [--version] [--help]
  twsearch.py [-c | --count <n>]
    [-M | --max-id <status-id>]
    [-N | --max-count <n>]
    <query>
"""

from secret import twitter_instance
from twmods import SEP
from twmods import make_logger
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from itertools import count
import sys
import time

__version__ = '1.1.2'

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """
    parser = ArgumentParser(description='Twitter Tweets Finder')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        'query',
        help='the search query')
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        default=15,
        choices=range(1, 101),
        metavar='{1..100}',
        help='number of tweets to return per page')
    parser.add_argument(
        '-M', '--max-id',
        type=int,
        nargs='?',
        metavar='<status-id>',
        help='the maximum status ID of tweets to search')
    parser.add_argument(
        '-N', '--max-count',
        type=int,
        nargs='?',
        default=100,
        choices=range(1, 1001),
        metavar='{1..1000}',
        help='the maximum number of tweets to search')

    return parser

def main():
    """The main function.

    Returns:
        None.
    """

    parser = configure()
    args = parser.parse_args()

    logger = make_logger('twsearch')
    tw = twitter_instance()

    csv_header = (
        'id',
        'created_at',
        'user[screen_name]',
        'user[description]',
        'text',
        'source',)
    csv_format = SEP.join(('{' + i + '}' for i in csv_header))

    kwargs = dict(
        q=args.query,
        count=args.count,
        include_entities=False)
    if args.max_id:
        kwargs['max_id'] = args.max_id

    # Print CSV header.
    print(SEP.join(csv_header))

    total_statuses = 0

    pcount = args.count
    max_count = args.max_count

    if max_count < pcount:
        max_count = pcount

    for i in count():
        logger.info("[{:03d}] Waiting...".format(i))

        # Request.
        response = tw.search.tweets(**kwargs)
        metadata = response['search_metadata']
        if 'statuses' in response and response['statuses']:
            statuses = response['statuses']
            max_id = metadata['max_id']
            #since_id = metadata['since_id']
            since_id = statuses[-1]['id']
            mcount = metadata['count']
            total_statuses += mcount
        else:
            break

        for j in statuses:
            line = csv_format.format(**j)
            print(line.replace('\r', '').replace('\n', '\\n'))

        logger.info("[{:03d}] Fetched {}-{}.".format(i, max_id, since_id))

        if max_count <= total_statuses:
            logger.info("mcount={} max_count={} total_statuses={}".format(
                mcount, max_count, total_statuses))
            break

        kwargs['max_id'] = since_id - 1
        time.sleep(2)

if __name__ == '__main__':
    main()
