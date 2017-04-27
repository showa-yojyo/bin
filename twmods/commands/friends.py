"""friends.py: Implementation of class AbstractTwitterFriendCommand
and its subclasses.
"""

from . import AbstractTwitterCommand
from ..parsers import (
    parser_user_single,
    parser_count_users,
    parser_count_users_many,
    parser_cursor,
    parser_skip_status,
    parser_include_user_entities)

# GET friends/ids
# GET friends/list

FRIENDS_IDS = ('friends/ids', 'fri')
FRIENDS_LIST = ('friends/list', 'frl')

# pylint: disable=abstract-method
class AbstractTwitterFriendCommand(AbstractTwitterCommand):
    """n/a"""
    pass

class CommandIds(AbstractTwitterFriendCommand):
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
        """Request GET friends/ids for Twitter."""
        self.list_ids(self.twhandler.friends.ids)

class CommandList(AbstractTwitterFriendCommand):
    """List all of the users the specified user is following."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FRIENDS_LIST[0],
            aliases=FRIENDS_LIST[1:],
            parents=[parser_user_single(),
                     parser_count_users(), # 20, 200
                     parser_cursor(),
                     parser_skip_status(),
                     parser_include_user_entities()],
            help=self.__doc__)
        return parser

    def __call__(self):
        """Request GET friends/list for Twitter."""
        self._list_common(self.twhandler.friends.list)

def make_commands(manager):
    """Prototype"""

    # pylint: disable=no-member
    return (cmd_t(manager) for cmd_t in
            AbstractTwitterFriendCommand.__subclasses__())
