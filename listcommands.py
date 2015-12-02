# -*- coding: utf-8 -*-
"""listcommands.py
"""
__version__ = '1.8.1'

from common_twitter import AbstractTwitterCommand
from common_twitter import parser_user_single
from argparse import ArgumentParser
from argparse import FileType

# Available subcommands.
COMMAND_LISTS_STATUSES = ('lists-statuses', 'statuses', 'stat', 'st')
COMMAND_LISTS_MEMBERS_CREATE_ALL = ('lists-members-create_all', 'add')
COMMAND_LISTS_MEMBERS_DESTROY_ALL = ('lists-members-destroy_all', 'remove')
COMMAND_LISTS_MEMBERS = ('lists-members', 'show')
COMMAND_LISTS_SUBSCRIBERS = ('lists-subscribers', 'subscribers', 'sb')
COMMAND_LISTS_SUBSCRIBERS_CREATE = ('lists-subscribers-create', 'subscribe', 'subscr')
COMMAND_LISTS_SUBSCRIBERS_DESTROY = ('lists-subscribers-destroy', 'unsubscribe', 'unsubscr')
COMMAND_LISTS_MEMBERSHIPS = ('lists-memberships', 'memberships', 'mem')
COMMAND_LISTS_OWNERSHIPS = ('lists-ownerships', 'ownerships', 'ow')
COMMAND_LISTS_SUBSCRIPTIONS = ('lists-subscriptions', 'subscriptions', 'sp')
COMMAND_LISTS_CREATE = ('lists-create', 'create')
COMMAND_LISTS_SHOW = ('lists-show', 'describe', 'desc')
COMMAND_LISTS_UPDATE = ('lists-update', 'update', 'up')
COMMAND_LISTS_DESTROY = ('lists-destroy', 'destroy', 'del')

# GET lists/list - ALMOST EQUIVALENT to ownerships + subscriptions
# GET lists/subscribers/show - Check if the specified user is a subscriber of the specified list. 
# POST lists/members/create - n/a
# GET lists/members/show - Check if the specified user is a member of the specified list.
# POST lists/members/destroy - n/a

class CommandListsStatuses(AbstractTwitterCommand):
    """Show a timeline of tweets of the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_STATUSES[0],
            aliases=COMMAND_LISTS_STATUSES[1:],
            parents=[parser_listspec()],
            help='show a timeline of tweets of the specified list')
        parser.add_argument(
            '-c', '--count',
            type=int,
            nargs='?',
            default=20,
            choices=range(1, 201),
            metavar='{1..200}',
            help='number of tweets to return per page')
        parser.add_argument(
            '-M', '--max_id',
            type=int,
            nargs='?',
            metavar='<status-id>',
            help='results with an ID less than or equal to the specified ID')
        parser.add_argument(
            '-N', '--max-count',
            type=int,
            nargs='?',
            default=100,
            choices=range(1, 10001),
            metavar='{1..10000}',
            help='the maximum number of tweets to show')
        return parser

    def __call__(self):
        self.manager.request_lists_statuses()

class CommandListsMembersCreateAll(AbstractTwitterCommand):
    """Add multiple members to a list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_MEMBERS_CREATE_ALL[0],
            aliases=COMMAND_LISTS_MEMBERS_CREATE_ALL[1:],
            parents=[parser_listspec(), parser_users_batch()],
            help='add multiple members to a list')
        return parser

    def __call__(self):
        self.manager.request_lists_members_create_all()

class CommandListsMembersDestroyAll(AbstractTwitterCommand):
    """Remove multiple members from a list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_MEMBERS_DESTROY_ALL[0],
            aliases=COMMAND_LISTS_MEMBERS_DESTROY_ALL[1:],
            parents=[parser_listspec(), parser_users_batch()],
            help='remove multiple members from a list')
        return parser

    def __call__(self):
        self.manager.request_lists_members_destroy_all()

class CommandListsMembers(AbstractTwitterCommand):
    """List the members of the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_MEMBERS[0],
            aliases=COMMAND_LISTS_MEMBERS[1:],
            parents=[parser_listspec(), parser_users()],
            help='list members of the specified list')
        return parser

    def __call__(self):
        self.manager.request_lists_members()

class CommandListsSubscribersCreate(AbstractTwitterCommand):
    """Subscribe the authenticated user to the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_SUBSCRIBERS_CREATE[0],
            aliases=COMMAND_LISTS_SUBSCRIBERS_CREATE[1:],
            parents=[parser_listspec()],
            help='subscribe you to the specified list')
        return parser

    def __call__(self):
        self.manager.request_lists_subscribers_create()

class CommandListsSubscribersDestroy(AbstractTwitterCommand):
    """Unsubscribe the authenticated user to the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_SUBSCRIBERS_DESTROY[0],
            aliases=COMMAND_LISTS_SUBSCRIBERS_DESTROY[1:],
            parents=[parser_listspec()],
            help='unsubscribe you to the specified list')
        return parser

    def __call__(self):
        self.manager.request_lists_subscribers_destroy()

class CommandListsSubscribers(AbstractTwitterCommand):
    """List the subscribers of the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_SUBSCRIBERS[0],
            aliases=COMMAND_LISTS_SUBSCRIBERS[1:],
            parents=[parser_listspec(), parser_users()],
            help='list subscribers of the specified list')
        return parser

    def __call__(self):
        self.manager.request_lists_subscribers()

class CommandListsMemberships(AbstractTwitterCommand):
    """List lists the specified user has been added to."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_MEMBERSHIPS[0],
            aliases=COMMAND_LISTS_MEMBERSHIPS[1:],
            parents=[parser_user_single(), parser_ls()],
            help='list lists the specified user has been added to')
        return parser

    def __call__(self):
        self.manager.request_lists_memberships()

class CommandListsOwnerships(AbstractTwitterCommand):
    """List lists owned by the specified user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_OWNERSHIPS[0],
            aliases=COMMAND_LISTS_OWNERSHIPS[1:],
            parents=[parser_user_single(), parser_ls()],
            help='list lists owned by the specified user')
        return parser

    def __call__(self):
        self.manager.request_lists_ownerships()

class CommandListsSubscriptions(AbstractTwitterCommand):
    """List lists the specified user is subscribed to."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_SUBSCRIPTIONS[0],
            aliases=COMMAND_LISTS_SUBSCRIPTIONS[1:],
            parents=[parser_user_single(), parser_ls()],
            help='list lists the specified user is subscribed to')
        return parser

    def __call__(self):
        self.manager.request_lists_subscriptions()

class CommandListsCreate(AbstractTwitterCommand):
    """Create a new list for the authenticated user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_CREATE[0],
            aliases=COMMAND_LISTS_CREATE[1:],
            parents=[parser_prop()],
            help='create a new list')
        parser.add_argument(
            'name',
            help='the name for the list')
        return parser

    def __call__(self):
        self.manager.request_lists_create()

class CommandListsShow(AbstractTwitterCommand):
    """Show the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_SHOW[0],
            aliases=COMMAND_LISTS_SHOW[1:],
            parents=[parser_listspec()],
            help='show the specified list')
        return parser

    def __call__(self):
        self.manager.request_lists_show()

class CommandListsUpdate(AbstractTwitterCommand):
    """Update the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_UPDATE[0],
            aliases=COMMAND_LISTS_UPDATE[1:],
            parents=[parser_listspec(), parser_prop()],
            help='update the specified list')
        parser.add_argument(
            '--name',
            nargs='?',
            help='the name for the list')
        return parser

    def __call__(self):
        self.manager.request_lists_update(self)

class CommandListsDestroy(AbstractTwitterCommand):
    """Delete the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LISTS_DESTROY[0],
            aliases=COMMAND_LISTS_DESTROY[1:],
            parents=[parser_listspec()],
            help='delete the specified list')
        return parser

    def __call__(self):
        self.manager.request_lists_destroy(self)

_command_classes = tuple(v for k, v in locals().items() if k.startswith('CommandList'))

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in _command_classes]

def _parser_listspec():
    """(list_id | (slug (owner_id | owner_screen_name)))

        return {k:v[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',)
                if (k in args) and (args[k] is not None)}
    """

    parser = None
    def inner():
        nonlocal parser
        if parser:
            return parser

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
            '-I', '--owner-id',
            metavar='<owner_id>',
            help='the user ID of the user who owns the list being requested by a slug')
        owner.add_argument(
            '-S', '--owner-screen-name',
            metavar='<owner_screen_name>',
            help='the screen name of the user who owns the list being requested by a slug')

        return parser
    return inner

parser_listspec = _parser_listspec()

def _parser_users_batch():
    """Return the parent parser object of the following subcommands:

    * add
    * remove
    """

    parser = None
    def inner():
        nonlocal parser
        if parser:
            return parser

        parser = ArgumentParser(add_help=False)
        parser.add_argument(
            'screen_name',
            nargs='*',
            help='a list of screen names, up to 100 are allowed in a single request')
        parser.add_argument(
            '-f', '--file',
            type=FileType('r'),
            default=None,
            help='a file which lists screen names to be added or removed')
        return parser
    return inner

parser_users_batch = _parser_users_batch()

def _parser_users():
    """Return the parent parser object of the following subcommands:

    * show
    * subscribers
    """

    parser = None
    def inner():
        nonlocal parser
        if parser:
            return parser

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
    return inner

parser_users = _parser_users()

def _parser_ls():
    """Return the parent parser object of the following subcommands:

    * ownerships
    * memberships
    * subscriptions
    """

    parser = None
    def inner():
        nonlocal parser
        if parser:
            return parser

        parser = ArgumentParser(add_help=False)
        parser.add_argument(
            '-c', '--count',
            type=int,
            nargs='?',
            default=20,
            choices=range(1, 1001),
            metavar='{1..1000}',
            help='the amount of results to return per page')
        return parser
    return inner

parser_ls = _parser_ls()

def _parser_list_prop():
    """Return the parent parser object of the following subcommands:

    * create
    * update
    """

    parser = None
    def inner():
        nonlocal parser
        if parser:
            return parser

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
    return inner

parser_prop = _parser_list_prop()
