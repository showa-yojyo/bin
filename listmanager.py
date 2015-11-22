#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manage multiple users in a specified Twitter list.

Usage:
  listmanager.py [--version] [--help]
  listmanager.py statuses [-c | --count <n>]
    [-M | --max-id <status-id>] [-N | --max-count <n>]
    <owner-screen-name> <slug>
  listmanager.py add <owner-screen-name> <slug>
    [-f | --file <filepath>] <screen-name>...
  listmanager.py remove <owner-screen-name> <slug>
    [-f | --file <filepath>] <screen-name>...
  listmanager.py show [-c | --count <n>] <owner-screen-name> <slug>
  listmanager.py subscribers [-c | --count <n>] <owner-screen-name> <slug>
  listmanager.py memberships [-c | --count <n>] <screen-name>
  listmanager.py ownerships [-c | --count <n>] <screen-name>
  listmanager.py subscriptions [-c | --count <n>] <screen-name>
"""

from common_twitter import AbstractTwitterManager
from common_twitter import SEP
from common_twitter import format_tweet
from common_twitter import format_user
from common_twitter import get_tweet_csv_format
from common_twitter import get_user_csv_format
from argparse import ArgumentParser
from argparse import FileType
from itertools import count
from itertools import islice
import sys
import time

__version__ = '1.5.0'

# Available subcommands.
COMMAND_LIST_STATUSES = ('statuses', 'stat', 'st')
COMMAND_LIST_ADD = 'add'
COMMAND_LIST_REMOVE = 'remove'
COMMAND_LIST_SHOW = 'show'
COMMAND_LIST_SUBSCRIBERS = ('subscribers', 'sb')
COMMAND_LIST_MEMBERSHIPS = ('memberships', 'mem')
COMMAND_LIST_OWNERSHIPS = ('ownerships', 'ow')
COMMAND_LIST_SUBSCRIPTIONS = ('subscriptions', 'sp')

# GET lists/list - ALMOST EQUIVALENT to ownerships + subscriptions
# GET lists/statuses - ('statuses', 'stat', 'st')
# GET lists/memberships - ('memberships', 'm')
# GET lists/ownerships - ('ownerships', 'ow')
# GET lists/subscriptions - ('subscriptions', 'sp')

# POST lists/subscribers/create
# GET lists/subscribers - ('subscribers', 'sb')
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

        # Subcommands
        subparsers = parser.add_subparsers(help='commands')

        # Basic arguments.
        def create_parser_slug():
            """Return a parser which parses arguments owner_screen_name and slug."""

            parser = ArgumentParser(add_help=False)
            parser.add_argument(
                'owner_screen_name',
                help='the screen name of the user who owns the list being requested by a slug')
            parser.add_argument(
                'slug',
                help='the slug of the list.')

            return parser

        parser_slug = create_parser_slug()

        parser_st = subparsers.add_parser(
            COMMAND_LIST_STATUSES[0],
            aliases=COMMAND_LIST_STATUSES[1:],
            parents=[parser_slug],
            help='show a timeline of tweets of the specified list')
        parser_st.add_argument(
            '-c', '--count',
            type=int,
            nargs='?',
            default=20,
            choices=range(1, 201),
            metavar='{1..200}',
            help='number of tweets to return per page')
        parser_st.add_argument(
            '-M', '--max_id',
            type=int,
            nargs='?',
            metavar='<status-id>',
            help='results with an ID less than or equal to the specified ID')
        parser_st.add_argument(
            '-N', '--max-count',
            type=int,
            nargs='?',
            default=100,
            choices=range(1, 10001),
            metavar='{1..10000}',
            help='the maximum number of tweets to show')
        parser_st.set_defaults(func=self._execute_statuses)

        def create_parser_users_batch():
            """Return the parent parser object of the following subcommands:

            * add
            * remove
            """

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

        parser_users_batch = create_parser_users_batch()

        parser_add = subparsers.add_parser(
            COMMAND_LIST_ADD,
            parents=[parser_slug, parser_users_batch],
            help='add multiple members to a list')
        parser_add.set_defaults(func=self._execute_add)

        parser_remove = subparsers.add_parser(
            COMMAND_LIST_REMOVE,
            parents=[parser_slug, parser_users_batch],
            help='remove multiple members from a list')
        parser_remove.set_defaults(func=self._execute_remove)

        def create_parser_users():
            """Return the parent parser object of the following subcommands:

            * show
            * subscribers
            """

            parser = ArgumentParser(add_help=False)
            parser.add_argument(
                '-c', '--count',
                type=int,
                nargs='?',
                default=20,
                choices=range(1, 5001),
                metavar='{1..5000}',
                help='the number of users to return per page')

            return parser

        parser_users = create_parser_users()

        parser_list = subparsers.add_parser(
            COMMAND_LIST_SHOW,
            parents=[parser_slug, parser_users],
            help='list members of the specified list')
        parser_list.set_defaults(func=self._execute_list)

        parser_sb = subparsers.add_parser(
            COMMAND_LIST_SUBSCRIBERS[0],
            aliases=COMMAND_LIST_SUBSCRIBERS[1:],
            parents=[parser_slug, parser_users],
            help='list subscribers of the specified list')
        parser_sb.set_defaults(func=self._execute_subscribers)

        def create_parser_ls():
            """Return the parent parser object of the following subcommands:

            * ownerships
            * memberships
            * subscriptions
            """

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
            help='list lists the specified user has been added to')
        parser_mem.set_defaults(func=self._execute_memberships)

        parser_ow = subparsers.add_parser(
            COMMAND_LIST_OWNERSHIPS[0],
            aliases=COMMAND_LIST_OWNERSHIPS[1:],
            parents=[parser_ls],
            help='list lists owned by the specified user')
        parser_ow.set_defaults(func=self._execute_ownerships)

        parser_sp = subparsers.add_parser(
            COMMAND_LIST_SUBSCRIPTIONS[0],
            aliases=COMMAND_LIST_SUBSCRIPTIONS[1:],
            parents=[parser_ls],
            help='list lists the specified user is subscribed to')
        parser_sp.set_defaults(func=self._execute_subscriptions)

        return parser

    def _execute_statuses(self):
        """Show a timeline of tweets of the specified list."""

        request, logger, args = self.tw.lists.statuses, self.logger, self.args

        kwargs = dict(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug,
            count=args.count,
            include_rts=False,
            include_entities=False,)

        if args.max_id:
            kwargs['max_id'] = args.max_id

        csv_header = (
            'created_at',
            'user[screen_name]',
            'user[name]',
            #'source',
            'favorited',
            'retweet_count',
            'text',)
        csv_format = SEP.join(('{' + i + '}' for i in csv_header))

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
            response = request(**kwargs)
            if response:
                max_id = response[0]['id']
                min_id = response[-1]['id']
                mcount = len(response)
                total_statuses += mcount
            else:
                break

            for j in response:
                line = csv_format.format(**j)
                print(line.replace('\r', '').replace('\n', '\\n'))

            logger.info("[{:03d}] min_id={} Fetched.".format(i, min_id))

            if max_count <= total_statuses:
                logger.info("mcount={} max_count={} total_statuses={}".format(
                    mcount, max_count, total_statuses))
                break

            kwargs['max_id'] = min_id - 1

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
            chunk = islice(users, i, i + up_to)
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

    def _show_users(self, request):
        """Show users related tp the specified list.

        Args:
            request: Select lists.members or lists.subscribers.
        """

        logger, args = self.logger, self.args

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

    def _execute_list(self):
        """List the members of the specified list."""
        self._show_users(self.tw.lists.members)

    def _execute_subscribers(self):
        """List the subscribers of the specified list."""
        self._show_users(self.tw.lists.subscribers)

    def _show_lists(self, request):
        """Show lists related to the specified user.

        Args:
            request: Select lists.ownerships, lists.memberships, etc.
        """

        logger, args = self.logger, self.args

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

    def _execute_memberships(self):
        """List lists the specified user has been added to."""
        self._show_lists(self.tw.lists.memberships)

    def _execute_ownerships(self):
        """List lists owned by the specified user."""
        self._show_lists(self.tw.lists.ownerships)

    def _execute_subscriptions(self):
        """List lists the specified user is subscribed to."""
        self._show_lists(self.tw.lists.subscriptions)

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
