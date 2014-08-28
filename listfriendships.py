#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script lists all the followers of a Twitter user.

Examples:
  You must specify the user's screen_name you want to show::

    $ python listfriendships.py list-friends screen_name
    $ python listfriendships.py list-followers screen_name
"""

from secret import twitter_instance
from argparse import ArgumentParser

__version__ = '1.0.0'

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

    # Positional arguments
    parser.add_argument(
        'command',
        choices=[COMMAND_LIST_FRIENDS, COMMAND_LIST_FOLLOWERS,],
        help='Either "{0}" or "{1}".'.format(COMMAND_LIST_FRIENDS, COMMAND_LIST_FOLLOWERS))

    parser.add_argument(
        'screen_name',
        help='The screen name of the target user.')

    return parser

def format_user(user):
    """Return a string that shows user information.

    Args:
        user: An instance of the Twitter API users response object.

    Returns:
        A colon-separated value string.
    """
    return '{screen_name}\t{name}\t{description}\t{url}'.format(**user).replace('\r', '').replace('\n', ' ')

def main(args):
    """The main function.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """

    tw = twitter_instance()
    next_cursor = -1

    cmd = None
    if args.command == COMMAND_LIST_FRIENDS:
        cmd = tw.friends.list
    elif args.command == COMMAND_LIST_FOLLOWERS:
        cmd = tw.followers.list

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

if __name__ == '__main__':
    parser = configure()
    main(parser.parse_args())
