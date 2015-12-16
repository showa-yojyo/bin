# -*- coding: utf-8 -*-
"""mutes.py: Implementation of class AbstractTwitterMuteCommand
and its subclasses.
"""

from .. import AbstractTwitterCommand
from .. import (parser_user_single,
                parser_cursor,
                parser_include_entities,
                parser_skip_status)
from argparse import ArgumentParser

# POST mutes/users/create
# POST mutes/users/destroy
# GET mutes/users/ids
# GET mutes/users/list

MUTE_USERS_CREATE = ('mutes/users/create', 'create')
MUTE_USERS_DESTROY = ('mutes/users/destroy', 'destroy')
MUTE_USERS_IDS = ('mutes/users/ids', 'ids')
MUTE_USERS_LIST = ('mutes/users/list', 'list')

class AbstractTwitterMuteCommand(AbstractTwitterCommand):
    pass

class CommandUsersCreate(AbstractTwitterMuteCommand):
    """Mute the user specified in the ID parameter for the
    authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            MUTE_USERS_CREATE[0],
            aliases=MUTE_USERS_CREATE[1:],
            parents=[parser_user_single()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_mutes_users_create()

class CommandUsersDestroy(AbstractTwitterMuteCommand):
    """Un-mute the user specified in the ID parameter for the
    authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            MUTE_USERS_DESTROY[0],
            aliases=MUTE_USERS_DESTROY[1:],
            parents=[parser_user_single()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_mutes_users_destroy()

class CommandUsersIds(AbstractTwitterMuteCommand):
    """Print an array of numeric user ids the authenticating user
    has muted.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            MUTE_USERS_IDS[0],
            aliases=MUTE_USERS_IDS[1:],
            parents=[parser_cursor()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_mutes_users_ids()

class CommandUsersList(AbstractTwitterMuteCommand):
    """Print an array of user objects the authenticating user has
    muted.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            MUTE_USERS_LIST[0],
            aliases=MUTE_USERS_LIST[1:],
            parents=[parser_cursor(),
                     parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_mutes_users_list()

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterMuteCommand.__subclasses__()]
