#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Find Twitter tweets.

Usage:
  findtweets.py [--version] [--help]
  findtweets.py [-c | --count <n>]
                [-M | --max-id <status-id>]
                [-N | --max-count <n>]
                <query>
"""

from secret import twitter_instance
from secret import SEP
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from itertools import count
import sys
import time

__version__ = '1.0.0'

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

    tw = twitter_instance()

    csv_header = (
        'id',
        'created_at',
        'user[screen_name]',
        'user[description]',
        'text',
        'source',)
    csv_format = SEP.join(('{' + i + '}' for i in csv_header))

    print(SEP.join(csv_header))

    kwargs = dict(
        q=args.query,
        count=args.count,
        include_entities=False)
    if args.max_id:
        kwargs['max_id'] = args.max_id

    total_statuses = 0
    pcount = kwargs['count']
    max_count = args.max_count

    if max_count < pcount:
        max_count = pcount

    for i in count():
        print("{}: Wait...".format(i), file=sys.stderr, flush=True)

        # Request.
        response = tw.search.tweets(**kwargs)

        metadata = response['search_metadata']
        max_id = metadata['max_id']
        #since_id = metadata['since_id']
        if 'statuses' in response and response['statuses']:
            statuses = response['statuses']
            since_id = statuses[-1]['id']
        else:
            break

        for j in statuses:
            line = csv_format.format(**j)
            print(line.replace('\r', '').replace('\n', ' '))

        print("{} ({} to {}): OK.".format(i, max_id, since_id),
              file=sys.stderr, flush=True)

        mcount = metadata['count']
        total_statuses += mcount
        if mcount < pcount or max_count <= total_statuses:
            break

        kwargs['max_id'] = since_id - 1
        time.sleep(2)

if __name__ == '__main__':
    main()
