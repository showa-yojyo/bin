#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""View the most recent tweets of a user.

Examples:
  $ usertimeline.py <screen_name>
"""

from secret import twitter_instance
from secret import format_tweet
from secret import get_tweet_csv_format
from argparse import ArgumentParser
import sys
import time

__version__ = '1.0.0'

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
        help='the number of tweets to try and retrieve')

    parser.add_argument(
        '-m', '--max_id',
        type=int,
        nargs='?',
        default=0,
        help='results with an ID less than or equal to the specified ID')

    return parser.parse_args()

def main(args):
    """The main function.

    Args:
      args: Command line parameters.

    Returns:
      None.
    """

    tw = twitter_instance()

    kwargs = dict(
        screen_name=args.screen_name,
        count=args.count,
        include_rts=False,
        include_entities=False,
        exclude_replies=True,)

    if args.max_id != 0:
        kwargs['max_id'] = args.max_id

    print(get_tweet_csv_format())

    for i in range(5):
        if i != 0:
            time.sleep(2)

        print("{}: Wait...".format(i), file=sys.stderr, flush=True)
        response = tw.statuses.user_timeline(**kwargs)

        for j in response:
            print(format_tweet(j))

        min_id = None
        if len(response):
            min_id = response[-1]['id']

        if min_id:
            kwargs['max_id'] = min_id - 1
            print("{} (min_id={}): OK.".format(i, min_id),
                  file=sys.stderr, flush=True)

        #if response[-1]['created_at'][-4:] < '2014':
        #    print("Loop break.", file=sys.stderr, flush=True)
        #    break

        #if len(response) < args.count:
        #    break

if __name__ == '__main__':
    main(configure())
