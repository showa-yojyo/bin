# -*- coding: utf-8 -*-
"""listcommands.py
"""
__version__ = '1.7.0'

from common_twitter import AbstractTwitterCommand
from argparse import ArgumentParser
from argparse import FileType

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

class CommandListStatuses(AbstractTwitterCommand):
    """Show a timeline of tweets of the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_STATUSES[0],
            aliases=COMMAND_LIST_STATUSES[1:],
            parents=[parser_slug()],
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
        self.manager.request_statuses()

class CommandListAdd(AbstractTwitterCommand):
    """Add multiple members to a list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_ADD,
            parents=[parser_slug(), parser_users_batch()],
            help='add multiple members to a list')
        return parser

    def __call__(self):
        self.manager.request_add()

class CommandListRemove(AbstractTwitterCommand):
    """Remove multiple members from a list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_REMOVE,
            parents=[parser_slug(), parser_users_batch()],
            help='remove multiple members from a list')
        return parser

    def __call__(self):
        self.manager.request_remove()

class CommandListShow(AbstractTwitterCommand):
    """List the members of the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_SHOW,
            parents=[parser_slug(), parser_users()],
            help='list members of the specified list')
        return parser

    def __call__(self):
        self.manager.request_members()

class CommandListSubscribe(AbstractTwitterCommand):
    """Subscribe the authenticated user to the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_SUBSCRIBE[0],
            aliases=COMMAND_LIST_SUBSCRIBE[1:],
            parents=[parser_slug()],
            help='subscribe you to the specified list')
        return parser

    def __call__(self):
        self.manager.request_subscribe()

class CommandListUnsubscribe(AbstractTwitterCommand):
    """Unsubscribe the authenticated user to the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_UNSUBSCRIBE[0],
            aliases=COMMAND_LIST_UNSUBSCRIBE[1:],
            parents=[parser_slug()],
            help='unsubscribe you to the specified list')
        return parser

    def __call__(self):
        self.manager.request_unsubscribe()

class CommandListSubscribers(AbstractTwitterCommand):
    """List the subscribers of the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_SUBSCRIBERS[0],
            aliases=COMMAND_LIST_SUBSCRIBERS[1:],
            parents=[parser_slug(), parser_users()],
            help='list subscribers of the specified list')
        return parser

    def __call__(self):
        self.manager.request_subscribers()

class CommandListMemberships(AbstractTwitterCommand):
    """List lists the specified user has been added to."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_MEMBERSHIPS[0],
            aliases=COMMAND_LIST_MEMBERSHIPS[1:],
            parents=[parser_ls()],
            help='list lists the specified user has been added to')
        return parser

    def __call__(self):
        self.manager.request_memberships()

class CommandListOwnerships(AbstractTwitterCommand):
    """List lists owned by the specified user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_OWNERSHIPS[0],
            aliases=COMMAND_LIST_OWNERSHIPS[1:],
            parents=[parser_ls()],
            help='list lists owned by the specified user')
        return parser

    def __call__(self):
        self.manager.request_ownerships()

class CommandListSubscriptions(AbstractTwitterCommand):
    """List lists the specified user is subscribed to."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_SUBSCRIPTIONS[0],
            aliases=COMMAND_LIST_SUBSCRIPTIONS[1:],
            parents=[parser_ls()],
            help='list lists the specified user is subscribed to')
        return parser

    def __call__(self):
        self.manager.request_subscriptions()

class CommandListCreate(AbstractTwitterCommand):
    """Create a new list for the authenticated user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_CREATE,
            parents=[parser_prop()],
            help='create a new list')
        parser.add_argument(
            'name',
            help='the name for the list')
        return parser

    def __call__(self):
        self.manager.request_create()

class CommandListDescribe(AbstractTwitterCommand):
    """Show the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_DESCRIBE[0],
            aliases=COMMAND_LIST_DESCRIBE[1:],
            parents=[parser_slug()],
            help='show the specified list')
        return parser

    def __call__(self):
        self.manager.request_describe()

class CommandListUpdate(AbstractTwitterCommand):
    """Update the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_UPDATE[0],
            aliases=COMMAND_LIST_UPDATE[1:],
            parents=[parser_slug(), parser_prop()],
            help='update the specified list')
        parser.add_argument(
            '--name',
            nargs='?',
            help='the name for the list')
        return parser

    def __call__(self):
        self.manager.request_update(self)

class CommandListDelete(AbstractTwitterCommand):
    """Delete the specified list."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_LIST_DESTROY[0],
            aliases=COMMAND_LIST_DESTROY[1:],
            parents=[parser_slug()],
            help='delete the specified list')
        return parser

    def __call__(self):
        self.manager.request_delete(self)

def make_commands(manager):
    """Prototype"""

    command_classes = (
        CommandListStatuses,
        CommandListAdd,
        CommandListRemove,
        CommandListShow,
        CommandListSubscribers,
        CommandListSubscribe,
        CommandListUnsubscribe,
        CommandListMemberships,
        CommandListOwnerships,
        CommandListSubscriptions,
        CommandListCreate,
        CommandListDescribe,
        CommandListUpdate,
        CommandListDelete,)

    return [cmd_t(manager) for cmd_t in command_classes]

def _parser_slug():
    """Return a parser which parses arguments owner_screen_name and slug."""

    parser = None
    def inner():
        nonlocal parser
        if parser:
            return parser

        parser = ArgumentParser(add_help=False)
        parser.add_argument(
            'owner_screen_name',
            help='the screen name of the user who owns the list being requested by a slug')
        parser.add_argument(
            'slug',
            help='the slug of the list.')
        return parser
    return inner

parser_slug = _parser_slug()

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
