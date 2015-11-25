# -*- coding: utf-8 -*-
"""followercommands.py
"""
__version__ = '1.5.0'

from common_twitter import AbstractTwitterCommand
from argparse import ArgumentParser
from argparse import FileType

# Available subcommands.
# names[0] and names[1:] are the official name and aliases, respectively.
COMMAND_FOLLOWERS_IDS = ('followers-ids', 'foi')
COMMAND_FOLLOWERS_LIST = ('followers-list', 'fol')

COMMAND_FRIENDS_IDS = ('friends-ids', 'fri')
COMMAND_FRIENDS_LIST = ('friends-list', 'frl')

COMMAND_FRIENDSHIPS_LOOKUP = ('friendships-lookup', 'lookup')

# GET followers/ids - COMMAND_FOLLOWERS_IDS
# GET followers/list - COMMAND_FOLLOWERS_LIST

# GET friends/ids - COMMAND_FRIENDS_IDS
# GET friends/list - COMMAND_FRIENDS_LIST

# POST friendships/create - Allows the authenticating users to follow the user specified in the ID parameter. - screen_name, user_id, follow?
# POST friendships/destroy - Allows the authenticating user to unfollow the user specified in the ID parameter. - screen_name, user_id
# GET friendships/incoming - Returns a collection of numeric IDs for every user who has a pending request to follow the authenticating user. - noargs
# GET friendships/lookup - COMMAND_FRIENDSHIPS_LOOKUP
# GET friendships/no_retweets/ids - Returns a collection of user_ids that the currently authenticated user does not want to receive retweets from. - noargs
# GET friendships/outgoing - Returns a collection of numeric IDs for every user who has a pending request to follow the authenticating user. - noargs
# GET friendships/show - Returns detailed information about the relationship between two arbitrary users. - special
# POST friendships/update - Allows one to enable or disable retweets and device notifications from the specified user - screen_name, user_id, device, ...

class CommandFollowersIds(AbstractTwitterCommand):
    """Print user IDs for every user following the specified user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FOLLOWERS_IDS[0],
            aliases=COMMAND_FOLLOWERS_IDS[1:],
            parents=[common_parser()],
            help='print user IDs for every user following the specified user')
        return parser

    def __call__(self):
        self.manager.request_followers_ids()

class CommandFollowersList(AbstractTwitterCommand):
    """List all of the users following the specified user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FOLLOWERS_LIST[0],
            aliases=COMMAND_FOLLOWERS_LIST[1:],
            parents=[common_parser()],
            help='list all of the users following the specified user')
        return parser

    def __call__(self):
        self.manager.request_followers_list()

class CommandFriendsIds(AbstractTwitterCommand):
    """Print user IDs for every user the specified user is following."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDS_IDS[0],
            aliases=COMMAND_FRIENDS_IDS[1:],
            parents=[common_parser()],
            help='print user IDs for every user the specified user is following')
        return parser

    def __call__(self):
        self.manager.request_friends_ids()

class CommandFriendsList(AbstractTwitterCommand):
    """List all of the users the specified user is following."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDS_LIST[0],
            aliases=COMMAND_FRIENDS_LIST[1:],
            parents=[common_parser()],
            help='list all of the users the specified user is following')
        return parser

    def __call__(self):
        self.manager.request_friends_list()

class CommandFriendshipsLookup(AbstractTwitterCommand):
    """Print the relationships of you to specified users."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_FRIENDSHIPS_LOOKUP[0],
            aliases=COMMAND_FRIENDSHIPS_LOOKUP[1:],
            parents=[parser_users_batch()],
            help='print the relationships of you to specified users')
        return parser

    def __call__(self):
        self.manager.request_friendships_lookup()

def make_commands(manager):
    """Prototype"""

    command_classes = (
        CommandFollowersIds,
        CommandFollowersList,
        CommandFriendsIds,
        CommandFriendsList,
        CommandFriendshipsLookup,)

    return [cmd_t(manager) for cmd_t in command_classes]

def _common_parser():
    """Return the parent parser object of the following subcommands:

    * friends
    * followers
    """

    parser = None
    def inner():
        nonlocal parser
        if parser:
            return parser

        parser = ArgumentParser(add_help=False)
        parser.add_argument(
            'screen_name',
            help='the screen name of the target user')
        parser.add_argument(
            '-c', '--count',
            type=int,
            nargs='?',
            #default=20,
            choices=range(1, 201),
            metavar='{1..200}',
            help='number of users to return per page')
        return parser
    return inner

common_parser = _common_parser()

def _parser_users_batch():
    """user_id version."""

    parser = None
    def inner():
        nonlocal parser
        if parser:
            return parser

        parser = ArgumentParser(add_help=False)
        parser.add_argument(
            'user_id',
            nargs='*',
            help='a list of user IDs')
        parser.add_argument(
            '-f', '--file',
            type=FileType('r'),
            default=None,
            help='a file which lists user IDs')
        return parser
    return inner

parser_users_batch = _parser_users_batch()
