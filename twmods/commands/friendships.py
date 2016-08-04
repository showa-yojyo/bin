# -*- coding: utf-8 -*-
"""friendships.py: Implementation of class AbstractTwitterFriendshipCommand
and its subclasses.
"""

from . import AbstractTwitterCommand, call_decorator
from ..parsers import (
    filter_args,
    parser_cursor,
    parser_user_single,
    parser_user_multiple,)

# POST friendships/create - FRIENDSHIP_CREATE
# POST friendships/destroy - FRIENDSHIP_DESTROY
# GET friendships/incoming - FRIENDSHIPS_INCOMING
# GET friendships/lookup - FRIENDSHIPS_LOOKUP
# GET friendships/no_retweets/ids - FRIENDSHIPS_NO_RETWEETS_IDS
# GET friendships/outgoing - FRIENDSHIPS_OUTGOING
# GET friendships/show - FRIENDSHIPS_SHOW
# POST friendships/update - FRIENDSHIPS_UPDATE

FRIENDSHIP_CREATE = ('friendships/create', 'create', 'follow')
FRIENDSHIP_DESTROY = ('friendships/destroy', 'destroy', 'unfollow')
FRIENDSHIPS_INCOMING = ('friendships/incoming', 'in')
FRIENDSHIPS_LOOKUP = ('friendships/lookup', 'lookup')
FRIENDSHIPS_NO_RETWEETS_IDS = ('friendships/no_retweets/ids', 'nor')
FRIENDSHIPS_OUTGOING = ('friendships/outgoing', 'out')
FRIENDSHIPS_SHOW = ('friendships/show', 'relation')
FRIENDSHIPS_UPDATE = ('friendships/update', 'update')

# pylint: disable=abstract-method
class AbstractTwitterFriendshipCommand(AbstractTwitterCommand):
    """n/a"""
    pass

class CommandCreate(AbstractTwitterFriendshipCommand):
    """Allows the authenticating users to follow the user specified
    in the ID parameter.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIP_CREATE[0],
            aliases=FRIENDSHIP_CREATE[1:],
            parents=[parser_user_single()],
            help=self.__doc__)
        parser.add_argument(
            '--follow',
            action='store_true',
            help='enable notifications for the target user')
        return parser

    @call_decorator
    def __call__(self):
        """Request POST friendships/create for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'user_id', 'screen_name', 'follow')

        return kwargs, self.twhandler.friendships.create

class CommandDestroy(AbstractTwitterFriendshipCommand):
    """Allows the authenticating user to unfollow the user specified
    in the ID parameter.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIP_DESTROY[0],
            aliases=FRIENDSHIP_DESTROY[1:],
            parents=[parser_user_single()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request POST friendships/destroy for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'user_id', 'screen_name')

        return kwargs, self.twhandler.friendships.destroy

class CommandIncoming(AbstractTwitterFriendshipCommand):
    """Print IDs for every user who has a pending request to follow
    you.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIPS_INCOMING[0],
            aliases=FRIENDSHIPS_INCOMING[1:],
            parents=[parser_cursor()],
            help=self.__doc__)
        return parser

    def __call__(self):
        """Request GET friendships/incoming for Twitter."""
        self.manager.list_ids(self.twhandler.friendships.incoming)

class CommandLookup(AbstractTwitterFriendshipCommand):
    """Print the relationships of you to specified users."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIPS_LOOKUP[0],
            aliases=FRIENDSHIPS_LOOKUP[1:],
            parents=[parser_user_multiple()],
            help=self.__doc__)
        return parser

    def __call__(self):
        """Request GET friendships/lookup for Twitter."""
        self._request_users_csv(self.twhandler.friendships.lookup)

class CommandNoRetweetsIds(AbstractTwitterFriendshipCommand):
    """Print IDs that you do not want to receive retweets from."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIPS_NO_RETWEETS_IDS[0],
            aliases=FRIENDSHIPS_NO_RETWEETS_IDS[1:],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET friendships/no_retweets/ids for Twitter."""

        return {}, self.twhandler.friendships.no_retweets.ids

class CommandOutgoing(AbstractTwitterFriendshipCommand):
    """Print IDs for protected user for whom you have a pending
    follow request.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIPS_OUTGOING[0],
            aliases=FRIENDSHIPS_OUTGOING[1:],
            parents=[parser_cursor()],
            help=self.__doc__)
        return parser

    def __call__(self):
        """Request GET friendships/outgoing for Twitter."""
        self.manager.list_ids(self.twhandler.friendships.outgoing)

class CommandShow(AbstractTwitterFriendshipCommand):
    """Describe detailed information about the relationship between
    two arbitrary users.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIPS_SHOW[0],
            aliases=FRIENDSHIPS_SHOW[1:],
            help=self.__doc__)

        # required should be True
        source = parser.add_mutually_exclusive_group(required=False)
        source.add_argument(
            '-U', '--source-user-id',
            nargs='?',
            dest='source_user_id',
            help='the user_id of the subject user')
        source.add_argument(
            '-S', '--source-screen-name',
            nargs='?',
            dest='source_screen_name',
            help='the screen_name of the subject user')

        # required should be True
        target = parser.add_mutually_exclusive_group(required=False)
        target.add_argument(
            '-V', '--target-user-id',
            nargs='?',
            dest='target_user_id',
            help='the user_id of the target user')
        target.add_argument(
            '-T', '--target_screen_name',
            nargs='?',
            dest='target_screen_name',
            help='the screen_name of the target user')

        return parser

    @call_decorator
    def __call__(self):
        """Request GET friendships/show for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'source_user_id', 'source_screen_name',
            'target_user_id', 'target_screen_name')
        return kwargs, self.twhandler.friendships.show

class CommandUpdate(AbstractTwitterFriendshipCommand):
    """Allows one to enable or disable retweets and device
    notifications from the specified user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIPS_UPDATE[0],
            aliases=FRIENDSHIPS_UPDATE[1:],
            parents=[parser_user_single()],
            help=self.__doc__)

        device = parser.add_mutually_exclusive_group()
        device.add_argument(
            '--device',
            action='store_true',
            dest='device',
            help='enable device notifications from the target user')
        device.add_argument(
            '--no-device',
            action='store_false',
            dest='device',
            help='disable device notifications from the target user')
        rts = parser.add_mutually_exclusive_group()
        rts.add_argument(
            '--retweets',
            action='store_true',
            dest='retweets',
            help='enable retweets from the target user')
        rts.add_argument(
            '--no-retweets',
            action='store_false',
            dest='retweets',
            help='disable retweets from the target user')

        return parser

    @call_decorator
    def __call__(self):
        """Request GET friendships/update for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'user_id',
            'screen_name',
            'device',
            'retweets')

        return kwargs, self.twhandler.friendships.update

def make_commands(manager):
    """Prototype"""

    # pylint: disable=no-member
    return (cmd_t(manager) for cmd_t in
            AbstractTwitterFriendshipCommand.__subclasses__())
