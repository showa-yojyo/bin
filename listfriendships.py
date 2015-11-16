#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""List friends or followers of a specified Twitter user.

Usage:
  listfriendships.py list-friends <screen-name>
  listfriendships.py list-followers <screen-name>
"""

from secret import twitter_instance
from common_twitter import format_user
from common_twitter import get_user_csv_format
from common_twitter import make_logger
from argparse import ArgumentParser
import sys

__version__ = '1.2.0'

# Available subcommands.
COMMAND_LIST_FRIENDS = 'list-friends'
COMMAND_LIST_FOLLOWERS = 'list-followers'

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='Twitter Followers Viewer')
    parser.add_argument('--version', action='version', version=__version__)

    subparsers = parser.add_subparsers(help='commands')

    parser_friends = subparsers.add_parser(
        COMMAND_LIST_FRIENDS,
        help='list all of the users the specified user is following')

    parser_follows = subparsers.add_parser(
        COMMAND_LIST_FOLLOWERS,
        help='list all of the users following the specified user')

    for i in (parser_friends, parser_follows):
        i.add_argument(
            'screen_name',
            help='the screen name of the target user')

    parser_friends.set_defaults(func=execute_list_friends)
    parser_follows.set_defaults(func=execute_list_followers)

    return parser

def execute_list_friends(args):
    """List all of the users the specified user is following.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """

    list_common(args, args.tw.friends.list)

def execute_list_followers(args):
    """List all of the users following the specified user.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """

    list_common(args, args.tw.followers.list)

def list_common(args, cmd):
    """The common procedure of friends/list and followers/list.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.
        cmd: A PTT request method for Twitter API.

    Returns:
        None.
    """

    logger = make_logger('listfriendships')
    print(get_user_csv_format())

    next_cursor = -1
    while next_cursor != 0:
        friends = cmd(
            screen_name=args.screen_name,
            cursor=next_cursor,
            count=200,
            skip_status=True,
            include_user_entities=False,)

        for user in friends['users']:
            print(format_user(user))

        next_cursor = friends['next_cursor']
        logger.info('next_cursor: {}'.format(next_cursor))

def main(args):
    """The main function.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """

    args.tw = twitter_instance()
    args.func(args)

if __name__ == '__main__':
    parser = configure()
    main(parser.parse_args())
