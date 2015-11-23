#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""List friends or followers of a specified Twitter user.

Usage:
  listfriendships.py [--version] [--help]
  listfriendships.py <command> [-c | --count <n>] <screen-name>
"""

from common_twitter import AbstractTwitterCommand
from common_twitter import AbstractTwitterManager
from common_twitter import format_user
from common_twitter import get_user_csv_format
from argparse import ArgumentParser

__version__ = '1.3.4'

# Available subcommands.
# names[0] and names[1:] are the official name and aliases, respectively.
COMMAND_LIST_FRIENDS = ['list-friends', 'friends', 'fr']
COMMAND_LIST_FOLLOWERS = ['list-followers', 'followers', 'fo']

class TwitterFollowerManager(AbstractTwitterManager):
    """This class handles commands about a Twitter followers."""

    def __init__(self):
        super().__init__(
            'listfriendships',
            (CommandFriends(self),
             CommandFollowers(self),))
        self._common_parser = None

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that stores the command line
            parameters.
        """

        parser = ArgumentParser(description='Twitter Followers Viewer')
        parser.add_argument('--version', action='version', version=__version__)
        return parser

    def common_parser(self):
        """Return the parent parser object of the following subcommands:

        * friends
        * followers
        """

        if self._common_parser:
            return self._common_parser

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

        self._common_parser = common_parser
        return common_parser

    def request_friends(self):
        """List all of the users the specified user is following."""
        self._list_common(self.tw.friends.list)

    def request_followers(self):
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

class CommandFriends(AbstractTwitterCommand):
    """List all of the users the specified user is following."""

    def create_parser(self, subparsers):
        common_parser = self.manager.common_parser()
        parser_friends = subparsers.add_parser(
            COMMAND_LIST_FRIENDS[0],
            aliases=COMMAND_LIST_FRIENDS[1:],
            parents=[common_parser],
            help='list all of the users the specified user is following')
        return parser_friends

    def __call__(self):
        self.manager.request_friends()

class CommandFollowers(AbstractTwitterCommand):
    """List all of the users following the specified user."""

    def create_parser(self, subparsers):
        common_parser = self.manager.common_parser()
        parser_follows = subparsers.add_parser(
            COMMAND_LIST_FOLLOWERS[0],
            aliases=COMMAND_LIST_FOLLOWERS[1:],
            parents=[common_parser],
            help='list all of the users following the specified user')
        return parser_follows

    def __call__(self):
        self.manager.request_followers()

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterFollowerManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
