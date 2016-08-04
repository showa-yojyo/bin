# -*- coding: utf-8 -*-
"""blocks.py: Implementation of class AbstractTwitterBlockCommand
and its subclasses.
"""

from . import AbstractTwitterCommand, call_decorator
from ..parsers import (filter_args,
                       parser_user_single,
                       parser_cursor,
                       parser_include_entities,
                       parser_skip_status)

# POST blocks/create
# POST blocks/destroy
# GET blocks/ids
# GET blocks/list

BLOCK_CREATE = ('blocks/create', 'create')
BLOCK_DESTROY = ('blocks/destroy', 'destroy')
BLOCK_IDS = ('blocks/ids', 'ids')
BLOCK_LIST = ('blocks/list', 'list')

# pylint: disable=abstract-method
class AbstractTwitterBlockCommand(AbstractTwitterCommand):
    """n/a"""
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

    @call_decorator
    def __call__(self):
        """Request POST blocks/create for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'user_id', 'screen_name',
            'include_entities', 'skip_status')

        return kwargs, self.twhandler.blocks.create

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

    @call_decorator
    def __call__(self):
        """Request POST blocks/destroy for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'user_id', 'screen_name',
            'include_entities', 'skip_status')

        return kwargs, self.twhandler.blocks.destroy

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

    @call_decorator
    def __call__(self):
        """Request GET blocks/ids for Twitter."""

        kwargs = filter_args(vars(self.args), 'cursor')

        return kwargs, self.twhandler.blocks.ids

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

    @call_decorator
    def __call__(self):
        """Request GET blocks/list for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'cursor', 'include_entities', 'skip_status')

        return kwargs, self.twhandler.blocks.list

def make_commands(manager):
    """Prototype"""
    # pylint: disable=no-member
    return (cmd_t(manager) for cmd_t in
            AbstractTwitterBlockCommand.__subclasses__())
