# -*- coding: utf-8 -*-
"""lists.py: Implementation of class AbstractTwitterListsCommand
and its subclasses.
"""

from .. import AbstractTwitterCommand
from .. import cache
from .. import (parser_user_single,
                parser_user_multiple,
                parser_count_statuses,
                parser_count_users_many,
                parser_cursor,
                parser_since_max_ids,
                parser_include_entities,
                parser_include_rts,
                parser_skip_status)
from argparse import ArgumentParser

# Available subcommands.
LISTS_STATUSES = ('lists/statuses', 'statuses', 'stat', 'st')
LISTS_MEMBERS_CREATE_ALL = ('lists/members/create_all', 'add')
LISTS_MEMBERS_DESTROY_ALL = ('lists/members/destroy_all', 'remove')
LISTS_MEMBERS = ('lists/members', 'show')
LISTS_SUBSCRIBERS = ('lists/subscribers', 'subscribers', 'sb')
LISTS_SUBSCRIBERS_CREATE = ('lists/subscribers/create', 'subscribe', 'subscr')
LISTS_SUBSCRIBERS_DESTROY = ('lists/subscribers/destroy', 'unsubscribe', 'unsubscr')
LISTS_MEMBERSHIPS = ('lists/memberships', 'memberships', 'mem')
LISTS_OWNERSHIPS = ('lists/ownerships', 'ownerships', 'ow')
LISTS_SUBSCRIPTIONS = ('lists/subscriptions', 'subscriptions', 'sp')
LISTS_CREATE = ('lists/create', 'create')
LISTS_SHOW = ('lists/show', 'describe', 'desc')
LISTS_UPDATE = ('lists/update', 'update', 'up')
LISTS_DESTROY = ('lists/destroy', 'destroy', 'del')

# GET lists/list - ALMOST EQUIVALENT to ownerships + subscriptions
# GET lists/subscribers/show - Check if the specified user is a subscriber of the specified list. 
# POST lists/members/create - n/a
# GET lists/members/show - Check if the specified user is a member of the specified list.
# POST lists/members/destroy - n/a

class AbstractTwitterListsCommand(AbstractTwitterCommand):
    pass

class Statuses(AbstractTwitterListsCommand):
    """Show a timeline of tweets of the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_STATUSES[0],
            aliases=LISTS_STATUSES[1:],
            parents=[parser_listspec(),
                     parser_since_max_ids(),
                     parser_count_statuses(),
                     parser_include_entities(),
                     parser_include_rts()],
            help=self.__doc__)

        return parser

    def __call__(self):
        self.manager.request_lists_statuses()

class MembersCreateAll(AbstractTwitterListsCommand):
    """Add multiple members to a list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_MEMBERS_CREATE_ALL[0],
            aliases=LISTS_MEMBERS_CREATE_ALL[1:],
            parents=[parser_listspec(),
                     parser_user_multiple()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_lists_members_create_all()

class MembersDestroyAll(AbstractTwitterListsCommand):
    """Remove multiple members from a list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_MEMBERS_DESTROY_ALL[0],
            aliases=LISTS_MEMBERS_DESTROY_ALL[1:],
            parents=[parser_listspec(),
                     parser_user_multiple()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_lists_members_destroy_all()

class Members(AbstractTwitterListsCommand):
    """List the members of the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_MEMBERS[0],
            aliases=LISTS_MEMBERS[1:],
            parents=[parser_listspec(),
                     parser_count_users_many(), # 20, 5000
                     parser_cursor(),
                     parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_lists_members()

class SubscribersCreate(AbstractTwitterListsCommand):
    """Subscribe the authenticated user to the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_SUBSCRIBERS_CREATE[0],
            aliases=LISTS_SUBSCRIBERS_CREATE[1:],
            parents=[parser_listspec()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_lists_subscribers_create()

class SubscribersDestroy(AbstractTwitterListsCommand):
    """Unsubscribe the authenticated user to the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_SUBSCRIBERS_DESTROY[0],
            aliases=LISTS_SUBSCRIBERS_DESTROY[1:],
            parents=[parser_listspec()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_lists_subscribers_destroy()

class Subscribers(AbstractTwitterListsCommand):
    """List the subscribers of the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_SUBSCRIBERS[0],
            aliases=LISTS_SUBSCRIBERS[1:],
            parents=[parser_listspec(),
                     parser_count_users_many(), # 20, 5000
                     parser_cursor(),
                     parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_lists_subscribers()

class Memberships(AbstractTwitterListsCommand):
    """List lists the specified user has been added to."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_MEMBERSHIPS[0],
            aliases=LISTS_MEMBERSHIPS[1:],
            parents=[parser_user_single(),
                     parser_count_lists(), # 20, 1000
                     parser_cursor()],
            help=self.__doc__)
        parser.add_argument(
            '--filter-to-owned-lists',
            dest='filter_to_owned_lists',
            action='store_true',
            help='print just lists the authenticating user owns')
        return parser

    def __call__(self):
        self.manager.request_lists_memberships()

class Ownerships(AbstractTwitterListsCommand):
    """List lists owned by the specified user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_OWNERSHIPS[0],
            aliases=LISTS_OWNERSHIPS[1:],
            parents=[parser_user_single(),
                     parser_count_lists(), # 20, 1000
                     parser_cursor()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_lists_ownerships()

class Subscriptions(AbstractTwitterListsCommand):
    """List lists the specified user is subscribed to."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_SUBSCRIPTIONS[0],
            aliases=LISTS_SUBSCRIPTIONS[1:],
            parents=[parser_user_single(),
                     parser_count_lists(), # 20, 1000
                     parser_cursor()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_lists_subscriptions()

class Create(AbstractTwitterListsCommand):
    """Create a new list for the authenticated user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_CREATE[0],
            aliases=LISTS_CREATE[1:],
            parents=[parser_prop()],
            help=self.__doc__)
        parser.add_argument(
            'name',
            help='the name for the list')
        return parser

    def __call__(self):
        self.manager.request_lists_create()

class Show(AbstractTwitterListsCommand):
    """Show the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_SHOW[0],
            aliases=LISTS_SHOW[1:],
            parents=[parser_listspec()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_lists_show()

class Update(AbstractTwitterListsCommand):
    """Update the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_UPDATE[0],
            aliases=LISTS_UPDATE[1:],
            parents=[parser_listspec(),
                     parser_prop()],
            help=self.__doc__)
        parser.add_argument(
            '--name',
            nargs='?',
            help='the name for the list')
        return parser

    def __call__(self):
        self.manager.request_lists_update(self)

class Destroy(AbstractTwitterListsCommand):
    """Delete the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            LISTS_DESTROY[0],
            aliases=LISTS_DESTROY[1:],
            parents=[parser_listspec()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_lists_destroy(self)

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterListsCommand.__subclasses__()]

@cache
def parser_listspec():
    """(list_id | (slug (owner_id | owner_screen_name)))

        return {k:v[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',)
                if (k in args) and (args[k] is not None)}
    """

    parser = ArgumentParser(add_help=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-l', '--list-id',
        dest='list_id',
        metavar='<list_id>',
        help='the numerical id of the list')
    group.add_argument(
        '-s', '--slug',
        dest='slug',
        metavar='<slug>',
        help='the slug of the list')

    # TODO: required only if <slug> is supplied
    owner = parser.add_mutually_exclusive_group(required=False)
    owner.add_argument(
        '-OI', '--owner-id',
        metavar='<owner_id>',
        help='the user ID of the user who owns the list being requested by a slug')
    owner.add_argument(
        '-OS', '--owner-screen-name',
        metavar='<owner_screen_name>',
        help='the screen name of the user who owns the list being requested by a slug')

    return parser

@cache
def parser_count_lists():
    """Return the parent parser object of the following subcommands:

    * lists/ownerships
    * lists/memberships
    * lists/subscriptions
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        choices=range(1, 1001),
        metavar='{1..1000}',
        help='the amount of results to return per page')
    return parser

@cache
def parser_prop():
    """Return the parent parser object of the following subcommands:

    * create
    * update
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-m', '--mode',
        nargs='?',
        choices=('public', 'private'),
        metavar='<public | private>',
        help='public or private')
    parser.add_argument(
        '-d', '--description',
        nargs='?',
        help='the description to give the list')
    return parser
