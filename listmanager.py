#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manage a Twitter list.

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
  listmanager.py subscribe <owner-screen-name> <slug>
  listmanager.py unsubscribe <owner-screen-name> <slug>
  listmanager.py subscribers [-c | --count <n>] <owner-screen-name> <slug>
  listmanager.py memberships [-c | --count <n>] <screen-name>
  listmanager.py ownerships [-c | --count <n>] <screen-name>
  listmanager.py subscriptions [-c | --count <n>] <screen-name>
  listmanager.py create [-m | --mode <public | private>]
    [-d | --desc <DESC>] <name>
  listmanager.py describe <owner-screen-name> <slug>
  listmanager.py update [-m | --mode <public | private>]
    [-d | --desc <DESC>] [--name <NAME>] <owner_screen_name> <slug>
  listmanager.py destroy <owner_screen_name> <slug>
"""

from common_twitter import AbstractTwitterCommand
from common_twitter import AbstractTwitterManager
from common_twitter import SEP
from common_twitter import format_list
from common_twitter import format_user
from common_twitter import get_list_csv_format
from common_twitter import get_user_csv_format
from argparse import ArgumentParser
from argparse import FileType
from itertools import count
from itertools import islice
import time

__version__ = '1.7.0'

# Available subcommands.
COMMAND_LIST_STATUSES = ('statuses', 'stat', 'st')
COMMAND_LIST_ADD = 'add'
COMMAND_LIST_REMOVE = 'remove'
COMMAND_LIST_SHOW = 'show'
COMMAND_LIST_SUBSCRIBERS = ('subscribers', 'sb')
COMMAND_LIST_SUBSCRIBE = ('subscribe', 'subscr')
COMMAND_LIST_UNSUBSCRIBE = ('unsubscribe', 'unsubscr')
COMMAND_LIST_MEMBERSHIPS = ('memberships', 'mem')
COMMAND_LIST_OWNERSHIPS = ('ownerships', 'ow')
COMMAND_LIST_SUBSCRIPTIONS = ('subscriptions', 'sp')
COMMAND_LIST_CREATE = 'create'
COMMAND_LIST_DESCRIBE = ('describe', 'desc')
COMMAND_LIST_UPDATE = ('update', 'up')
COMMAND_LIST_DESTROY = ('destroy', 'del')

# GET lists/list - ALMOST EQUIVALENT to ownerships + subscriptions
# GET lists/statuses - ('statuses', 'stat', 'st')
# GET lists/memberships - ('memberships', 'm')
# GET lists/ownerships - ('ownerships', 'ow')
# GET lists/subscriptions - ('subscriptions', 'sp')

# POST lists/subscribers/create - ('subscribe', 'subscr')
# GET lists/subscribers - ('subscribers', 'sb')
# GET lists/subscribers/show - Check if the specified user is a subscriber of the specified list. 
# POST lists/subscribers/destroy - ('unscribe', 'unsubscr')

# POST lists/members/create - n/a
# POST lists/members/create_all - add
# GET lists/members - show
# GET lists/members/show - Check if the specified user is a member of the specified list.
# POST lists/members/destroy - n/a
# POST lists/members/destroy_all - remove

# POST lists/create - 'create'
# GET lists/show - ('describe', 'desc')
# POST lists/update - ('update', 'up')
# POST lists/destroy - ('destroy', 'del')

class TwitterListManager(AbstractTwitterManager):
    """This class handles commands about a Twitter list."""

    def __init__(self):
        super().__init__(
            'listmanager',
            (CommandListStatuses(self),
             CommandListAdd(self),
             CommandListRemove(self),
             CommandListShow(self),
             CommandListSubscribers(self),
             CommandListSubscribe(self),
             CommandListUnsubscribe(self),
             CommandListMemberships(self),
             CommandListOwnerships(self),
             CommandListSubscriptions(self),
             CommandListCreate(self),
             CommandListDescribe(self),
             CommandListUpdate(self),
             CommandListDelete(self),))

        self._parser_slug = None
        self._parser_users_batch = None
        self._parser_users = None
        self._parser_ls = None
        self._parser_prop = None

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the command line
            parameters.
        """

        parser = ArgumentParser(description='Twitter List Manager')
        parser.add_argument('--version', action='version', version=__version__)
        return parser

    def parser_slug(self):
        """Return a parser which parses arguments owner_screen_name and slug."""

        if self._parser_slug:
            return self._parser_slug

        parser = ArgumentParser(add_help=False)
        parser.add_argument(
            'owner_screen_name',
            help='the screen name of the user who owns the list being requested by a slug')
        parser.add_argument(
            'slug',
            help='the slug of the list.')

        self._parser_slug = parser
        return parser

    def parser_users_batch(self):
        """Return the parent parser object of the following subcommands:

        * add
        * remove
        """

        if self._parser_users_batch:
            return self._parser_users_batch

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

        self._parser_users_batch = parser
        return parser

    def parser_users(self):
        """Return the parent parser object of the following subcommands:

        * show
        * subscribers
        """

        if self._parser_users:
            return self._parser_users

        parser = ArgumentParser(add_help=False)
        parser.add_argument(
            '-c', '--count',
            type=int,
            nargs='?',
            default=20,
            choices=range(1, 5001),
            metavar='{1..5000}',
            help='the number of users to return per page')

        self._parser_users = parser
        return parser

    def parser_ls(self):
        """Return the parent parser object of the following subcommands:

        * ownerships
        * memberships
        * subscriptions
        """

        if self._parser_ls:
            return self._parser_ls

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

        self._parser_ls = parser
        return parser

    def parser_list_property(self):
        """Return the parent parser object of the following subcommands:

        * create
        * update
        """

        if self._parser_prop:
            return self._parser_prop

        parser = ArgumentParser(add_help=False)
        parser.add_argument(
            '-m', '--mode',
            nargs='?',
            choices=('public', 'private'),
            metavar='<public | private>',
            help='public or private')
        parser.add_argument(
            '-d', '--desc',
            nargs='?',
            help='the description to give the list')

        self._parser_prop = parser
        return parser

    def request_statuses(self):
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
        print(SEP.join(csv_header))

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

    def request_add(self):
        """Add multiple members to a list."""
        self._manage_members(self.tw.lists.members.create_all)

    def request_remove(self):
        """Remove multiple members from a list."""
        self._manage_members(self.tw.lists.members.destroy_all)

    def request_members(self):
        """List the members of the specified list."""
        self._show_users(self.tw.lists.members)

    def request_subscribers(self):
        """List the subscribers of the specified list."""
        self._show_users(self.tw.lists.subscribers)

    def request_subscribe(self):
        """Subscribe the authenticated user to the specified list."""

        args = self.args
        self.tw.lists.subscribe(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug)
        self.logger.info("Subscribed to {owner_screen_name}/{slug}.".format(**vars(args)))

    def request_unsubscribe(self):
        """Unsubscribe the authenticated user to the specified list."""

        args = self.args
        self.tw.lists.unsubscribe(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug)
        self.logger.info("Unsubscribed from {owner_screen_name}/{slug}.".format(**vars(args)))

    def request_memberships(self):
        """List lists the specified user has been added to."""
        self._show_lists(self.tw.lists.memberships)

    def request_ownerships(self):
        """List lists owned by the specified user."""
        self._show_lists(self.tw.lists.ownerships)

    def request_subscriptions(self):
        """List lists the specified user is subscribed to."""
        self._show_lists(self.tw.lists.subscriptions)

    def request_create(self):
        """Create a new list for the authenticated user."""

        logger, args = self.logger, self.args

        kwargs = dict(name=args.name)
        if args.mode:
            kwargs['mode'] = args.mode
        if args.desc:
            kwargs['description'] = args.desc

        self.tw.lists.create(**kwargs)
        logger.info("List {} is created.".format(args.name))

    def request_describe(self):
        """Show the specified list."""

        args = self.args
        response = self.tw.lists.show(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug)

        print(get_list_csv_format())
        print(format_list(response))

    def request_update(self):
        """Update the specified list."""

        logger, args = self.logger, self.args

        kwargs = dict(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug)
        if args.name:
            kwargs['name'] = args.name
        if args.mode:
            kwargs['mode'] = args.mode
        if args.desc:
            kwargs['description'] = args.desc

        self.tw.lists.update(**kwargs)
        logger.info("List {} is updated.".format(args.slug))

    def request_delete(self):
        """Delete the specified list."""

        logger, args = self.logger, self.args
        self.tw.lists.destroy(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug)
        logger.info("List {} is deleted.".format(args.slug))

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

    def _show_lists(self, request):
        """Show lists related to the specified user.

        Args:
            request: Select lists.ownerships, lists.memberships, etc.
        """

        logger, args = self.logger, self.args

        print(get_list_csv_format())

        next_cursor = -1
        while next_cursor != 0:
            response = request(
                screen_name=args.screen_name,
                count=args.count,
                cursor=next_cursor)

            for i in response['lists']:
                print(format_list(i))

            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

class CommandListStatuses(AbstractTwitterCommand):
    """Show a timeline of tweets of the specified list."""

    def create_parser(self, subparsers):
        parser_slug = self.manager.parser_slug()
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
        return parser_st

    def __call__(self):
        self.manager.request_statuses()

class CommandListAdd(AbstractTwitterCommand):
    """Add multiple members to a list."""

    def create_parser(self, subparsers):
        mgr = self.manager
        parser_slug = mgr.parser_slug()
        parser_users_batch = mgr.parser_users_batch()
        parser_add = subparsers.add_parser(
            COMMAND_LIST_ADD,
            parents=[parser_slug, parser_users_batch],
            help='add multiple members to a list')
        return parser_add

    def __call__(self):
        self.manager.request_add()

class CommandListRemove(AbstractTwitterCommand):
    """Remove multiple members from a list."""

    def create_parser(self, subparsers):
        mgr = self.manager
        parser_slug = mgr.parser_slug()
        parser_users_batch = mgr.parser_users_batch()
        parser_remove = subparsers.add_parser(
            COMMAND_LIST_REMOVE,
            parents=[parser_slug, parser_users_batch],
            help='remove multiple members from a list')
        return parser_remove

    def __call__(self):
        self.manager.request_remove()

class CommandListShow(AbstractTwitterCommand):
    """List the members of the specified list."""

    def create_parser(self, subparsers):
        mgr = self.manager
        parser_slug = mgr.parser_slug()
        parser_users = mgr.parser_users()
        parser_list = subparsers.add_parser(
            COMMAND_LIST_SHOW,
            parents=[parser_slug, parser_users],
            help='list members of the specified list')
        return parser_list

    def __call__(self):
        self.manager.request_members()

class CommandListSubscribe(AbstractTwitterCommand):
    """Subscribe the authenticated user to the specified list."""

    def create_parser(self, subparsers):
        parser_slug = self.manager.parser_slug()
        parser = subparsers.add_parser(
            COMMAND_LIST_SUBSCRIBE[0],
            aliases=COMMAND_LIST_SUBSCRIBE[1:],
            parents=[parser_slug],
            help='subscribe you to the specified list')
        return parser

    def __call__(self):
        self.manager.request_subscribe()

class CommandListUnsubscribe(AbstractTwitterCommand):
    """Unsubscribe the authenticated user to the specified list."""

    def create_parser(self, subparsers):
        parser_slug = self.manager.parser_slug()
        parser = subparsers.add_parser(
            COMMAND_LIST_UNSUBSCRIBE[0],
            aliases=COMMAND_LIST_UNSUBSCRIBE[1:],
            parents=[parser_slug],
            help='unsubscribe you to the specified list')
        return parser

    def __call__(self):
        self.manager.request_unsubscribe()

class CommandListSubscribers(AbstractTwitterCommand):
    """List the subscribers of the specified list."""

    def create_parser(self, subparsers):
        mgr = self.manager
        parser_slug = mgr.parser_slug()
        parser_users = mgr.parser_users()
        parser_sb = subparsers.add_parser(
            COMMAND_LIST_SUBSCRIBERS[0],
            aliases=COMMAND_LIST_SUBSCRIBERS[1:],
            parents=[parser_slug, parser_users],
            help='list subscribers of the specified list')
        return parser_sb

    def __call__(self):
        self.manager.request_subscribers()

class CommandListMemberships(AbstractTwitterCommand):
    """List lists the specified user has been added to."""

    def create_parser(self, subparsers):
        parser_ls = self.manager.parser_ls()
        parser_mem = subparsers.add_parser(
            COMMAND_LIST_MEMBERSHIPS[0],
            aliases=COMMAND_LIST_MEMBERSHIPS[1:],
            parents=[parser_ls],
            help='list lists the specified user has been added to')
        return parser_mem

    def __call__(self):
        self.manager.request_memberships()

class CommandListOwnerships(AbstractTwitterCommand):
    """List lists owned by the specified user."""

    def create_parser(self, subparsers):
        parser_ls = self.manager.parser_ls()
        parser_ow = subparsers.add_parser(
            COMMAND_LIST_OWNERSHIPS[0],
            aliases=COMMAND_LIST_OWNERSHIPS[1:],
            parents=[parser_ls],
            help='list lists owned by the specified user')
        return parser_ow

    def __call__(self):
        self.manager.request_ownerships()

class CommandListSubscriptions(AbstractTwitterCommand):
    """List lists the specified user is subscribed to."""

    def create_parser(self, subparsers):
        parser_ls = self.manager.parser_ls()
        parser_sp = subparsers.add_parser(
            COMMAND_LIST_SUBSCRIPTIONS[0],
            aliases=COMMAND_LIST_SUBSCRIPTIONS[1:],
            parents=[parser_ls],
            help='list lists the specified user is subscribed to')
        return parser_sp

    def __call__(self):
        self.manager.request_subscriptions()

class CommandListCreate(AbstractTwitterCommand):
    """Create a new list for the authenticated user."""

    def create_parser(self, subparsers):
        mgr = self.manager
        parser_prop = mgr.parser_list_property()
        parser_create = subparsers.add_parser(
            COMMAND_LIST_CREATE,
            parents=[parser_prop],
            help='create a new list')
        parser_create.add_argument(
            'name',
            help='the name for the list')
        return parser_create

    def __call__(self):
        self.manager.request_create()

class CommandListDescribe(AbstractTwitterCommand):
    """Show the specified list."""

    def create_parser(self, subparsers):
        parser_slug = self.manager.parser_slug()
        parser = subparsers.add_parser(
            COMMAND_LIST_DESCRIBE[0],
            aliases=COMMAND_LIST_DESCRIBE[1:],
            parents=[parser_slug],
            help='show the specified list')
        return parser

    def __call__(self):
        self.manager.request_describe()

class CommandListUpdate(AbstractTwitterCommand):
    """Update the specified list."""

    def create_parser(self, subparsers):
        mgr = self.manager
        parser_slug = mgr.parser_slug()
        parser_prop = mgr.parser_list_property()

        parser_update = subparsers.add_parser(
            COMMAND_LIST_UPDATE[0],
            aliases=COMMAND_LIST_UPDATE[1:],
            parents=[parser_slug, parser_prop],
            help='update the specified list')
        parser_update.add_argument(
            '--name',
            nargs='?',
            help='the name for the list')

        return parser_update

    def __call__(self):
        self.manager.request_update(self)

class CommandListDelete(AbstractTwitterCommand):
    """Delete the specified list."""

    def create_parser(self, subparsers):
        parser_slug = self.manager.parser_slug()

        parser_del = subparsers.add_parser(
            COMMAND_LIST_DESTROY[0],
            aliases=COMMAND_LIST_DESTROY[1:],
            parents=[parser_slug],
            help='delete the specified list')

        return parser_del

    def __call__(self):
        self.manager.request_delete(self)

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterListManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
