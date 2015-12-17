# -*- coding: utf-8 -*-
"""blocks.py: Implementation of class AbstractTwitterBlockCommand
and its subclasses.
"""

from .. import AbstractTwitterCommand
from .. import (parser_user_single,
                parser_cursor,
                parser_include_entities,
                parser_skip_status)
from argparse import ArgumentParser

# POST blocks/create
# POST blocks/destroy
# GET blocks/ids
# GET blocks/list

BLOCK_CREATE = ('blocks/create', 'create')
BLOCK_DESTROY = ('blocks/destroy', 'destroy')
BLOCK_IDS = ('blocks/ids', 'ids')
BLOCK_LIST = ('blocks/list', 'list')

class AbstractTwitterBlockCommand(AbstractTwitterCommand):
    pass

class CommandCreate(AbstractTwitterBlockCommand):
    """Block the specified user from following the authenticating
    user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            BLOCK_CREATE[0],
            aliases=BLOCK_CREATE[1:],
            parents=[parser_user_single(),
                     parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_blocks_create()

class CommandDestroy(AbstractTwitterBlockCommand):
    """Un-blocks the user specified in the ID parameter for the
    authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            BLOCK_DESTROY[0],
            aliases=BLOCK_DESTROY[1:],
            parents=[parser_user_single(),
                     parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_blocks_destroy()

class CommandIds(AbstractTwitterBlockCommand):
    """Print a collection of user objects that the authenticating
    user is blocking.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            BLOCK_IDS[0],
            aliases=BLOCK_IDS[1:],
            parents=[parser_cursor()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_blocks_ids()

class CommandList(AbstractTwitterBlockCommand):
    """Print a collection of user objects that the authenticating
    user is blocking.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            BLOCK_LIST[0],
            aliases=BLOCK_LIST[1:],
            parents=[parser_cursor(),
                     parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_blocks_list()

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterBlockCommand.__subclasses__()]
