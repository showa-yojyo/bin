# -*- coding: utf-8 -*-
"""followercommands.py: Implementation of class AbstractTwitterFollowersCommand
and its subclasses.
"""

from .. import AbstractTwitterCommand
from .. import cache
from .. import parser_user_single
from .. import parser_user_multiple
from .. import parser_count_users_many
from .. import parser_cursor
from argparse import ArgumentParser

# Available subcommands.
# names[0] and names[1:] are the official name and aliases, respectively.
COMMAND_FOLLOWERS_IDS = ('followers-ids', 'foi')
COMMAND_FOLLOWERS_LIST = ('followers-list', 'fol')

COMMAND_FRIENDS_IDS = ('friends-ids', 'fri')
COMMAND_FRIENDS_LIST = ('friends-list', 'frl')

COMMAND_FRIENDSHIPS_INCOMING = ('friendships-incoming', 'in')
COMMAND_FRIENDSHIPS_LOOKUP = ('friendships-lookup', 'lookup')
COMMAND_FRIENDSHIPS_NO_RETWEETS_IDS = ('friendships-no_retweets-ids', 'nor')
COMMAND_FRIENDSHIPS_OUTGOING = ('friendships-outgoing', 'out')
COMMAND_FRIENDSHIPS_SHOW = ('friendships-show', 'relation')
COMMAND_FRIENDSHIPS_UPDATE = ('friendships-update', 'update')

# GET followers/ids - COMMAND_FOLLOWERS_IDS
# GET followers/list - COMMAND_FOLLOWERS_LIST

# GET friends/ids - COMMAND_FRIENDS_IDS
# GET friends/list - COMMAND_FRIENDS_LIST

# POST friendships/create - Allows the authenticating users to follow the user specified in the ID parameter. - screen_name, user_id, follow?
# POST friendships/destroy - Allows the authenticating user to unfollow the user specified in the ID parameter. - screen_name, user_id
# GET friendships/incoming - COMMAND_FRIENDSHIPS_INCOMING
# GET friendships/lookup - COMMAND_FRIENDSHIPS_LOOKUP
# GET friendships/no_retweets/ids - COMMAND_FRIENDSHIPS_NO_RETWEETS_IDS
# GET friendships/outgoing - COMMAND_FRIENDSHIPS_OUTGOING
# GET friendships/show - COMMAND_FRIENDSHIPS_SHOW
# POST friendships/update - COMMAND_FRIENDSHIPS_UPDATE

class AbstractTwitterFollowersCommand(AbstractTwitterCommand):
    pass

class CommandFollowersIds(AbstractTwitterFollowersCommand):
    """Print user IDs for every user following the specified user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FOLLOWERS_IDS[0],
            aliases=COMMAND_FOLLOWERS_IDS[1:],
            parents=[parser_user_single(), parser_count_users_many(), parser_cursor()], # 20, 5000
            help='print user IDs for every user following the specified user')
        return parser

    def __call__(self):
        self.manager.request_followers_ids()

class CommandFollowersList(AbstractTwitterFollowersCommand):
    """List all of the users following the specified user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FOLLOWERS_LIST[0],
            aliases=COMMAND_FOLLOWERS_LIST[1:],
            parents=[parser_user_single(), parser_count_users(), parser_cursor()], # 20, 200
            help='list all of the users following the specified user')
        return parser

    def __call__(self):
        self.manager.request_followers_list()

class CommandFriendsIds(AbstractTwitterFollowersCommand):
    """Print user IDs for every user the specified user is following."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDS_IDS[0],
            aliases=COMMAND_FRIENDS_IDS[1:],
            parents=[parser_user_single(), parser_count_users_many(), parser_cursor()], # 20, 5000
            help='print user IDs for every user the specified user is following')
        return parser

    def __call__(self):
        self.manager.request_friends_ids()

class CommandFriendsList(AbstractTwitterFollowersCommand):
    """List all of the users the specified user is following."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDS_LIST[0],
            aliases=COMMAND_FRIENDS_LIST[1:],
            parents=[parser_user_single(), parser_count_users(), parser_cursor()], # 20, 200
            help='list all of the users the specified user is following')
        return parser

    def __call__(self):
        self.manager.request_friends_list()

class CommandFriendshipsIncoming(AbstractTwitterFollowersCommand):
    """Print IDs for every user who has a pending request to follow you."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDSHIPS_INCOMING[0],
            aliases=COMMAND_FRIENDSHIPS_INCOMING[1:],
            parents=[parser_cursor()],
            help='print IDs for every user who has a pending request to follow you')
        return parser

    def __call__(self):
        self.manager.request_friendships_incoming()

class CommandFriendshipsLookup(AbstractTwitterFollowersCommand):
    """Print the relationships of you to specified users."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDSHIPS_LOOKUP[0],
            aliases=COMMAND_FRIENDSHIPS_LOOKUP[1:],
            parents=[parser_user_multiple()],
            help='print the relationships of you to specified users')
        return parser

    def __call__(self):
        self.manager.request_friendships_lookup()

class CommandFriendshipsNoRetweetsIds(AbstractTwitterFollowersCommand):
    """Print IDs that you do not want to receive retweets from."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDSHIPS_NO_RETWEETS_IDS[0],
            aliases=COMMAND_FRIENDSHIPS_NO_RETWEETS_IDS[1:],
            help='print IDs that you do not want to receive retweets from')
        return parser

    def __call__(self):
        self.manager.request_friendships_no_retweets_ids()

class CommandFriendshipsOutgoing(AbstractTwitterFollowersCommand):
    """Print IDs for protected user for whom you have a pending follow request."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDSHIPS_OUTGOING[0],
            aliases=COMMAND_FRIENDSHIPS_OUTGOING[1:],
            parents=[parser_cursor()],
            help='print IDs for protected user for whom you have a pending follow request')
        return parser

    def __call__(self):
        self.manager.request_friendships_outgoing()

class CommandFriendshipsShow(AbstractTwitterFollowersCommand):
    """Describe detailed information about the relationship between two arbitrary users."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDSHIPS_SHOW[0],
            aliases=COMMAND_FRIENDSHIPS_SHOW[1:],
            help='print information about the relationship between two users')

        parser.add_argument(
            'source_screen_name',
            help='the screen_name of the subject user')
        parser.add_argument(
            'target_screen_name',
            help='the screen_name of the target user')

        return parser

    def __call__(self):
        self.manager.request_friendships_show()

class CommandFriendshipsUpdate(AbstractTwitterFollowersCommand):
    """Allows one to enable or disable retweets and device
    notifications from the specified user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDSHIPS_UPDATE[0],
            aliases=COMMAND_FRIENDSHIPS_UPDATE[1:],
            parents=[parser_user_single()],
            help='enable or disable retweets and device notifications from the specified user')

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

    def __call__(self):
        self.manager.request_friendships_update()

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterFollowersCommand.__subclasses__()]

@cache
def parser_count_users():
    """Return the parent parser object of the following subcommands:

    * friends/lists
    * followers/lists
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        choices=range(1, 201),
        metavar='{1..200}',
        help='number of users to return per page')
    return parser
