# -*- coding: utf-8 -*-
"""followers.py: Implementation of class AbstractTwitterFollowersCommand
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
FOLLOWERS_IDS = ('followers/ids', 'foi')
FOLLOWERS_LIST = ('followers/list', 'fol')

FRIENDS_IDS = ('friends/ids', 'fri')
FRIENDS_LIST = ('friends/list', 'frl')

FRIENDSHIPS_INCOMING = ('friendships/incoming', 'in')
FRIENDSHIPS_LOOKUP = ('friendships/lookup', 'lookup')
FRIENDSHIPS_NO_RETWEETS_IDS = ('friendships/no_retweets/ids', 'nor')
FRIENDSHIPS_OUTGOING = ('friendships/outgoing', 'out')
FRIENDSHIPS_SHOW = ('friendships/show', 'relation')
FRIENDSHIPS_UPDATE = ('friendships/update', 'update')

# GET followers/ids - FOLLOWERS_IDS
# GET followers/list - FOLLOWERS_LIST

# GET friends/ids - FRIENDS_IDS
# GET friends/list - FRIENDS_LIST

# POST friendships/create - Allows the authenticating users to follow the user specified in the ID parameter. - screen_name, user_id, follow?
# POST friendships/destroy - Allows the authenticating user to unfollow the user specified in the ID parameter. - screen_name, user_id
# GET friendships/incoming - FRIENDSHIPS_INCOMING
# GET friendships/lookup - FRIENDSHIPS_LOOKUP
# GET friendships/no_retweets/ids - FRIENDSHIPS_NO_RETWEETS_IDS
# GET friendships/outgoing - FRIENDSHIPS_OUTGOING
# GET friendships/show - FRIENDSHIPS_SHOW
# POST friendships/update - FRIENDSHIPS_UPDATE

class AbstractTwitterFollowersCommand(AbstractTwitterCommand):
    pass

class FollowersIds(AbstractTwitterFollowersCommand):
    """Print user IDs for every user following the specified
    user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FOLLOWERS_IDS[0],
            aliases=FOLLOWERS_IDS[1:],
            parents=[parser_user_single(),
                     parser_count_users_many(), # 20, 5000
                     parser_cursor()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_followers_ids()

class FollowersList(AbstractTwitterFollowersCommand):
    """List all of the users following the specified user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FOLLOWERS_LIST[0],
            aliases=FOLLOWERS_LIST[1:],
            parents=[parser_user_single(),
                     parser_count_users(), # 20, 200
                     parser_cursor()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_followers_list()

class FriendsIds(AbstractTwitterFollowersCommand):
    """Print user IDs for every user the specified user is
    following.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDS_IDS[0],
            aliases=FRIENDS_IDS[1:],
            parents=[parser_user_single(),
                     parser_count_users_many(), # 20, 5000
                     parser_cursor()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_friends_ids()

class FriendsList(AbstractTwitterFollowersCommand):
    """List all of the users the specified user is following."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDS_LIST[0],
            aliases=FRIENDS_LIST[1:],
            parents=[parser_user_single(),
                     parser_count_users(), # 20, 200
                     parser_cursor()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_friends_list()

class FriendshipsIncoming(AbstractTwitterFollowersCommand):
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
        self.manager.request_friendships_incoming()

class FriendshipsLookup(AbstractTwitterFollowersCommand):
    """Print the relationships of you to specified users."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIPS_LOOKUP[0],
            aliases=FRIENDSHIPS_LOOKUP[1:],
            parents=[parser_user_multiple()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_friendships_lookup()

class FriendshipsNoRetweetsIds(AbstractTwitterFollowersCommand):
    """Print IDs that you do not want to receive retweets from."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIPS_NO_RETWEETS_IDS[0],
            aliases=FRIENDSHIPS_NO_RETWEETS_IDS[1:],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_friendships_no_retweets_ids()

class FriendshipsOutgoing(AbstractTwitterFollowersCommand):
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
        self.manager.request_friendships_outgoing()

class FriendshipsShow(AbstractTwitterFollowersCommand):
    """Describe detailed information about the relationship between
    two arbitrary users.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDSHIPS_SHOW[0],
            aliases=FRIENDSHIPS_SHOW[1:],
            help=self.__doc__)

        parser.add_argument(
            'source_screen_name',
            help='the screen_name of the subject user')
        parser.add_argument(
            'target_screen_name',
            help='the screen_name of the target user')

        return parser

    def __call__(self):
        self.manager.request_friendships_show()

class FriendshipsUpdate(AbstractTwitterFollowersCommand):
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
