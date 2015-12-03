#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Show the most recent tweets of a user.

Usage:
  usertimeline.py [--version] [--help]
  usertimeline.py [-c | --count <n>]
    [-M | --max-id <status-id>]
    [-N | --max-count <n>]
    <screen-name>
"""

from secret import twitter_instance
from twmods import format_tweet
from twmods import get_tweet_csv_format
from twmods import make_logger
from argparse import ArgumentParser
from itertools import count
import sys
import time

__version__ = '1.2.1'

def configure():
    """Parse the command line parameters."""

    parser = ArgumentParser(description='Timeline Viewer')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        'screen_name',
        help='the screen name of the user for whom to return results for')
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        default=20,
        choices=range(1, 201),
        metavar='{1..200}',
        help='number of tweets to return per page')
    parser.add_argument(
        '-M', '--max_id',
        type=int,
        nargs='?',
        default=0,
        metavar='<status-id>',
        help='results with an ID less than or equal to the specified ID')
    parser.add_argument(
        '-N', '--max-count',
        type=int,
        nargs='?',
        default=100,
        choices=range(1, 10001),
        metavar='{1..10000}',
        help='the maximum number of tweets to show')

    return parser.parse_args()

def main(args):
    """The main function.

    Args:
      args: Command line parameters.

    Returns:
      None.
    """

    logger = make_logger('usertimeline')
    tw = twitter_instance()

    kwargs = dict(
        screen_name=args.screen_name,
        count=args.count,
        include_rts=False,
        include_entities=False,
        exclude_replies=True,)

    if args.max_id:
        kwargs['max_id'] = args.max_id

    # Print CSV header.
    print(get_tweet_csv_format())

    total_statuses = 0

    pcount = args.count
    max_count = args.max_count
    if max_count < pcount:
        max_count = pcount

    for i in count():
        logger.info("[{:03d}] Waiting...".format(i))

        # Request.
        response = tw.statuses.user_timeline(**kwargs)
        if response:
            max_id = response[0]['id']
            min_id = response[-1]['id']
            mcount = len(response)
            total_statuses += mcount
        else:
            break

        for j in response:
            print(format_tweet(j))

        logger.info("[{:03d}] min_id={} Fetched.".format(i, min_id))

        if max_count <= total_statuses:
            logger.info("mcount={} max_count={} total_statuses={}".format(
                mcount, max_count, total_statuses))
            break

        kwargs['max_id'] = min_id - 1
        time.sleep(2)

if __name__ == '__main__':
    main(configure())
