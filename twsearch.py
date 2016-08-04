#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser
import time

from twitter import TwitterHTTPError

from twmods import EPILOG
from twmods import make_logger
from twmods import output
from twmods.parsers import (parser_full,
                            parser_since_max_ids,
                            parser_include_entities)

from secret import twitter_instance

DESCRIPTION = "A utility script to search Twitter statuses."

USAGE = """
  twsearch.py [--version] [--help]
  twsearch.py [-F | --full] [-g | --geocode <geocode>]
    [--lang <language>] [--locale <locale>]
    [-t | --type {mixed, recent, popular}] [-c | --count <n>]
    [-u | --until <YYYY-MM-DD>]
    [--since-id <status-id>] [--max-id <status-id>]
    [-E | --include-entities]
    <query>
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.3.3'

COUNT_MAX = 100

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(
        description=DESCRIPTION,
        parents=[parser_full(),
                 parser_since_max_ids(),
                 parser_include_entities()],
        epilog=EPILOG,
        usage=USAGE)
    parser.add_argument(
        '--version',
        action='version',
        version=__version__)
    parser.add_argument(
        'q',
        metavar='<query>',
        help='the search query')
    parser.add_argument(
        '-g', '--geocode',
        nargs='?',
        help='locate within a given radius of the given latitude/longitude')
    parser.add_argument(
        '--lang',
        nargs='?',
        help='restrict tweets to the given language, '
             'given by an ISO 639-1 code')
    parser.add_argument(
        '--locale',
        nargs='?',
        help='the language of the query you are sending')
    parser.add_argument(
        '-t', '--type',
        nargs='?',
        choices=('mixed', 'recent', 'popular',),
        dest='result_type',
        help='the language of the query you are sending')
    parser.add_argument(
        '-c', '--count',
        nargs='?',
        type=int,
        choices=range(1, COUNT_MAX + 1),
        metavar='{1..100}',
        help='number of tweets to return per page')
    parser.add_argument(
        '-u', '--until',
        nargs='?',
        metavar='YYYY-MM-DD',
        help='before the given date')

    return parser

def main():
    """The main function.

    Returns:
        None.
    """

    parser = configure()
    args = vars(parser.parse_args())

    logger = make_logger('twsearch')
    twhandler = twitter_instance()
    request = twhandler.search.tweets

    kwargs = {k:args[k] for k in (
        'q',
        'geocode',
        'lang', 'locale',
        'result_type',
        'count',
        'until',
        'since_id', 'max_id',
        'include_entities',)
              if (k in args) and (args[k] is not None)}

    results = None
    if args['full']:
        results = []
        kwargs['count'] = COUNT_MAX
        try:
            while True:
                response = request(**kwargs)
                #metadata = response['search_metadata']
                if 'statuses' in response and response['statuses']:
                    statuses = response['statuses']
                    #max_id = metadata['max_id']
                    since_id = statuses[-1]['id']
                else:
                    logger.info("finished")
                    break

                logger.info('search.tweets params={}'.format(kwargs))
                results.append(response)

                if len(statuses) < kwargs['count']:
                    logger.info("finished")
                    break

                kwargs['max_id'] = since_id - 1
                time.sleep(2)
        except TwitterHTTPError as ex:
            logger.info('{}'.format(ex))
            #raise
    else:
        logger.info('search.tweets params={}'.format(kwargs))
        results = request(**kwargs)

    output(results)

if __name__ == '__main__':
    main()
