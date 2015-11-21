#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manage multiple users in a specified Twitter list.

Usage:
  listmanager.py [--version] [--help]
  listmanager.py add <owner-screen-name> <slug>
    [-f | --file <filepath>] <screen-name>...
  listmanager.py remove <owner-screen-name> <slug>
    [-f | --file <filepath>] <screen-name>...
  listmanager.py show [-c | --count <n>] <owner-screen-name> <slug>
  listmanager.py memberships [-c | --count <n>] <screen-name>
  listmanager.py ownerships [-c | --count <n>] <screen-name>
"""

from common_twitter import AbstractTwitterManager
from common_twitter import SEP
from common_twitter import format_user
from common_twitter import get_user_csv_format
from argparse import ArgumentParser
from argparse import FileType
import itertools
import sys
import time

__version__ = '1.4.0'

# Available subcommands.
COMMAND_LIST_ADD = 'add'
COMMAND_LIST_REMOVE = 'remove'
COMMAND_LIST_SHOW = 'show'
COMMAND_LIST_MEMBERSHIPS = ('memberships', 'mem')
COMMAND_LIST_OWNERSHIPS = ('ownerships', 'ow')

# GET lists/list - Returns all lists the authenticating or specified user subscribes to, including their own.
# GET lists/statuses - Returns a timeline of tweets authored by members of the specified list.
# GET lists/memberships - ('memberships', 'm')
# GET lists/ownerships - ('ownerships', 'ow')
# GET lists/subscriptions - Obtain a collection of the lists the specified user is subscribed to.

# POST lists/subscribers/create
# GET lists/subscribers - Returns the subscribers of the specified list.
# GET lists/subscribers/show - Check if the specified user is a subscriber of the specified list. 
# POST lists/subscribers/destroy

# POST lists/members/create - n/a
# POST lists/members/create_all - add
# GET lists/members - show
# GET lists/members/show - Check if the specified user is a member of the specified list.
# POST lists/members/destroy - n/a
# POST lists/members/destroy_all - remove

# POST lists/create
# GET lists/show - Returns the specified list.
# POST lists/update
# POST lists/destroy

class TwitterListManager(AbstractTwitterManager):
    """TBW"""

    def __init__(self):
        super().__init__('listmanager')

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that stores the command line
            parameters.
        """

        parser = ArgumentParser(description='Twitter List Manager')
        parser.add_argument('--version', action='version', version=__version__)

        def create_common_parser():
            """Return the common parser to all subcommands."""

            parser = ArgumentParser(add_help=False)
            parser.add_argument(
                'owner_screen_name',
                help='the screen name of the user who owns the list being requested by a slug')

            parser.add_argument(
                'slug',
                help='the slug of the list.')

            return parser

        common_parser = create_common_parser()

        def create_users_parser():
            """Return the common parser object to subcommands `add` and `remove`."""

            parser = ArgumentParser(add_help=False)
            parser.add_argument(
                'screen_name',
                nargs='*',
                help='a list of screen names, up to 100 are allowed in a single request')

            parser.add_argument(
                '-f', '--file',
                type=FileType('r', encoding='utf-8'),
                default=None,
                help='a file which lists screen names to be added or removed')

            return parser

        modify_parser = create_users_parser()

        # Subcommands
        subparsers = parser.add_subparsers(help='commands')

        parser_add = subparsers.add_parser(
            COMMAND_LIST_ADD,
            parents=[common_parser, modify_parser],
            help='add multiple members to a list')

        parser_remove = subparsers.add_parser(
            COMMAND_LIST_REMOVE,
            parents=[common_parser, modify_parser],
            help='remove multiple members from a list')

        parser_list = subparsers.add_parser(
            COMMAND_LIST_SHOW,
            parents=[common_parser],
            help='list the members of the specified list')

        parser_list.add_argument(
            '-c', '--count',
            type=int,
            nargs='?',
            default=20,
            choices=range(1, 5001),
            metavar='{1..5000}',
            help='the number of users to return per page')

        parser_add.set_defaults(func=self._execute_add)
        parser_remove.set_defaults(func=self._execute_remove)
        parser_list.set_defaults(func=self._execute_list)

        def create_parser_ls():
            """Return the parent parser of `ownerships` subcommand."""

            parser = ArgumentParser(add_help=False)
            parser.add_argument(
                'screen_name',
                help='the user for whom to return results for')
            parser.add_argument(
                '-c', '--count',
                type=int,
                nargs='?',
                default=20,
                choices=range(1, 1001),
                metavar='{1..1000}',
                help='the amount of results to return per page')

            return parser

        parser_ls = create_parser_ls()

        parser_mem = subparsers.add_parser(
            COMMAND_LIST_MEMBERSHIPS[0],
            aliases=COMMAND_LIST_MEMBERSHIPS[1:],
            parents=[parser_ls],
            help='lists the specified user has been added to')

        parser_mem.set_defaults(func=self._execute_memberships)

        parser_ow = subparsers.add_parser(
            COMMAND_LIST_OWNERSHIPS[0],
            aliases=COMMAND_LIST_OWNERSHIPS[1:],
            parents=[parser_ls],
            help='list owned by the specified user')

        parser_ow.set_defaults(func=self._execute_ownerships)

        return parser

    def _manage_members(self, request):
        """Add multiple members to a list or remove from a list.

        Args:
            request: Select lists.members.create_all or lists.members.destroy_all.
        """
        logger, args = self.logger, self.args

        # Obtain the target users.
        users = []
        users.extend(args.screen_name)
        if args.file:
            users.extend(line.rstrip() for line in args.file)

        # Note that lists can't have more than 5000 members
        # and you are limited to adding up to 100 members to a list at a time.
        up_to = 15
        for i in range(0, 5000, up_to):
            chunk = itertools.islice(users, i, i + up_to)
            csv = ','.join(chunk)
            if not csv:
                break

            logger.info("[{:04d}]-[{:04d}] Waiting...".format(i, i + up_to))

            # Request.
            request(
                owner_screen_name=args.owner_screen_name,
                slug=args.slug,
                screen_name=csv)

            logger.info("[{:04d}]-[{:04d}] Processed: {}".format(i, i + up_to, csv))
            time.sleep(15)

    def _execute_add(self):
        """Add multiple members to a list."""
        self._manage_members(self.tw.lists.members.create_all)

    def _execute_remove(self):
        """Remove multiple members from a list."""
        self._manage_members(self.tw.lists.members.destroy_all)

    def _execute_list(self):
        """List the members of the specified list."""

        request, logger, args = self.tw.lists.members, self.logger, self.args

        print(get_user_csv_format())

        next_cursor = -1
        while next_cursor != 0:
            # Request.
            response = request(
                owner_screen_name=args.owner_screen_name,
                slug=args.slug,
                count=args.count,
                cursor=next_cursor)

            for user in response['users']:
                print(format_user(user))

            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

    def _show_lists(self, request):
        """Show lists related to the specified user.

        Args:
            request: Select lists.ownerships or lists.memberships.
        """

        request, logger, args = request, self.logger, self.args

        csv_header = (
            'id',
            'slug',
            'full_name',
            'created_at',
            'mode',
            'member_count',
            'subscriber_count',
            'description',)
        csv_format = SEP.join(('{' + i + '}' for i in csv_header))

        print(SEP.join(csv_header))

        next_cursor = -1
        while next_cursor != 0:
            response = request(
                screen_name=args.screen_name,
                count=args.count,
                cursor=next_cursor)

            for i in response['lists']:
                line = csv_format.format(**i)
                print(line.replace('\r', '').replace('\n', ' '))

            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))
            time.sleep(2)

    def _execute_memberships(self):
        """Lists the specified user has been added to."""
        self._show_lists(self.tw.lists.memberships)

    def _execute_ownerships(self):
        """Lists owned by the specified user."""
        self._show_lists(self.tw.lists.ownerships)

def main(params=None):
    """The main function.

    Args:
        params: Raw command line arguments.
    """

    mgr = TwitterListManager()
    mgr.setup(params)
    mgr.execute()

if __name__ == '__main__':
    main()
