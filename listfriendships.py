#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""List friends or followers of a specified Twitter user.

Usage:
  listfriendships.py [--version] [--help]
  listfriendships.py <command> [-c | --count <n>] <screen-name>
"""

from common_twitter import AbstractTwitterManager
from common_twitter import format_user
from common_twitter import get_user_csv_format
from argparse import ArgumentParser
import sys

__version__ = '1.3.2'

# Available subcommands.
# names[0] and names[1:] are the official name and aliases, respectively.
COMMAND_LIST_FRIENDS = ['list-friends', 'friends', 'fr']
COMMAND_LIST_FOLLOWERS = ['list-followers', 'followers', 'fl']

class TwitterFollowerManager(AbstractTwitterManager):
    """TBW"""

    def __init__(self):
        super().__init__('listfriendships')

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that stores the command line
            parameters.
        """

        parser = ArgumentParser(description='Twitter Followers Viewer')
        parser.add_argument('--version', action='version', version=__version__)

        subparsers = parser.add_subparsers(help='commands')

        common_parser = ArgumentParser(add_help=False)
        common_parser.add_argument(
            'screen_name',
            help='the screen name of the target user')
        common_parser.add_argument(
            '-c', '--count',
            type=int,
            nargs='?',
            default=20,
            choices=range(1, 201),
            metavar='{1..200}',
            help='number of users to return per page')

        parser_friends = subparsers.add_parser(
            COMMAND_LIST_FRIENDS[0],
            aliases=COMMAND_LIST_FRIENDS[1:],
            parents=[common_parser],
            help='list all of the users the specified user is following')

        parser_follows = subparsers.add_parser(
            COMMAND_LIST_FOLLOWERS[0],
            aliases=COMMAND_LIST_FOLLOWERS[1:],
            parents=[common_parser],
            help='list all of the users following the specified user')

        parser_friends.set_defaults(func=self._execute_list_friends)
        parser_follows.set_defaults(func=self._execute_list_followers)

        return parser

    def _execute_list_friends(self):
        """List all of the users the specified user is following."""
        self._list_common(self.tw.friends.list)

    def _execute_list_followers(self):
        """List all of the users following the specified user."""
        self._list_common(self.tw.followers.list)

    def _list_common(self, request):
        """The common procedure of friends/list and followers/list.

        Args:
            request: A PTT request method for Twitter API.
        """

        logger, args = self.logger, self.args

        # Print CSV header.
        print(get_user_csv_format())

        next_cursor = -1
        while next_cursor != 0:
            # Request.
            users = request(
                screen_name=args.screen_name,
                cursor=next_cursor,
                count=args.count,
                skip_status=True,
                include_user_entities=False,)

            for user in users['users']:
                print(format_user(user))

            next_cursor = users['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

def main(params=None):
    """The main function.

    Args:
        params: Raw command line arguments.
    """

    mgr = TwitterFollowerManager()
    mgr.setup(params)
    mgr.execute()

if __name__ == '__main__':
    main()
