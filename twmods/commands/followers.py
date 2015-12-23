# -*- coding: utf-8 -*-
"""followers.py: Implementation of class AbstractTwitterFollowersCommand
and its subclasses.
"""

from . import AbstractTwitterCommand, call_decorator
from ..parsers import (
    parser_user_single,
    parser_user_multiple,
    parser_count_users,
    parser_count_users_many,
    parser_cursor,
    parser_skip_status,
    parser_include_user_entities)
from argparse import ArgumentParser

# Available subcommands.
# names[0] and names[1:] are the official name and aliases, respectively.
FOLLOWERS_IDS = ('followers/ids', 'foi')
FOLLOWERS_LIST = ('followers/list', 'fol')

# GET followers/ids - FOLLOWERS_IDS
# GET followers/list - FOLLOWERS_LIST

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
        """Request GET followers/ids for Twitter."""
        self._list_ids(self.tw.followers.ids)

class FollowersList(AbstractTwitterFollowersCommand):
    """List all of the users following the specified user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FOLLOWERS_LIST[0],
            aliases=FOLLOWERS_LIST[1:],
            parents=[parser_user_single(),
                     parser_count_users(), # 20, 200
                     parser_cursor(),
                     parser_skip_status(),
                     parser_include_user_entities()],
            help=self.__doc__)
        return parser

    def __call__(self):
        """Request GET followers/list for Twitter."""
        self._list_common(self.tw.followers.list)

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterFollowersCommand.__subclasses__()]
