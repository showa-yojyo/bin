# -*- coding: utf-8 -*-
"""parsers.py
"""

from abc import ABCMeta
from abc import abstractmethod
from argparse import (ArgumentParser, FileType)

def cache(func):
    instance = None
    def inner():
        nonlocal instance
        if instance:
            return instance

        instance = func()
        return instance
    return inner

# parsers

@cache
def parser_full():
    """Return the parent parser object for --full optional flag."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-F', '--full',
        action='store_true',
        help='retrieve data as much as possible')
    return parser

@cache
def parser_user_single():
    """Return the parent parser object for --user-id and
    --screen_name arguments.
    """

    parser = ArgumentParser(add_help=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-U', '--user-id',
        nargs='?',
        dest='user_id',
        help='the ID of the user for whom to return results')
    group.add_argument(
        '-S', '--screen-name',
        nargs='?',
        dest='screen_name',
        help='the screen name of the user for whom to return results')
    return parser

@cache
def parser_user_multiple():
    """Return the parent parser object for --user-id and
    --screen_name arguments.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-U', '--user-id',
        nargs='*',
        dest='user_id',
        help='the ID of the user for whom to return results')
    parser.add_argument(
        '-S', '--screen-name',
        nargs='*',
        dest='screen_name',
        help='the screen name of the user for whom to return results')
    parser.add_argument(
        '-UF', '--file-user-id',
        type=FileType('r'),
        default=None,
        dest='file_user_id',
        help='a file which lists user IDs')
    parser.add_argument(
        '-SF', '--file-screen-name',
        type=FileType('r'),
        default=None,
        dest='file_screen_name',
        help='a file which lists screen names')
    return parser

@cache
def parser_count_statuses():
    """Return the parent parser object for --count option."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        choices=range(1, 201),
        metavar='{1..200}',
        help='the number of tweets to return per page')
    return parser

@cache
def parser_count_users():
    """Return the parent parser object of the following subcommands:

    * friends/lists
    * followers/lists
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        choices=range(1, 201),
        metavar='{1..200}',
        help='number of users to return per page')
    return parser

@cache
def parser_count_users_many():
    """Return the parent parser object for --count optional argument.

    The following subcommands use this parser:

    * friends/ids
    * followers/ids
    * lists/members
    * lists/subscribers
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        choices=range(1, 5001),
        metavar='{1..5000}',
        help='the number of users to return per page')
    return parser

@cache
def parser_cursor():
    """Return the parent parser object for --cursor optional
    argument.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--cursor',
        type=int,
        nargs='?',
        help='break the results into pages')
    return parser

@cache
def parser_page():
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-p', '--page',
        type=int,
        help='the page of results to retrieve')
    return parser

@cache
def parser_since_max_ids():
    """Return the parent parser object for --since-id and --max-id
    optional arguments.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--since-id',
        dest='since_id',
        type=int,
        nargs='?',
        metavar='<status_id>',
        help='return results with an ID greater than the specified ID')
    parser.add_argument(
        '--max-id',
        dest='max_id',
        type=int,
        nargs='?',
        metavar='<status_id>',
        help='return results with an ID less than or equal to the specified ID')

    return parser

@cache
def parser_include_entities():
    """Return the parent parser object for --include-entities
    optional argument.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-E', '--include-entities',
        action='store_true',
        dest='include_entities',
        help='include entity nodes in tweet objects')
    return parser

@cache
def parser_include_rts():
    """Return the parent parser object for --include-rts optional
    argument.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--include-rts',
        dest='include_rts',
        action='store_true',
        help='show native retweets in the timeline')
    return parser

@cache
def parser_include_user_entities():
    """Return the parent parser object for --include-user-entities
    optional argument.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
            '--include-user-entities',
            dest='include_user_entities',
            action='store_true',
            help='include the user entities node')
    return parser

@cache
def parser_skip_status():
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--skip-status',
        dest='skip_status',
        action='store_true',
        help='exclude statuses from user objects')
    return parser
