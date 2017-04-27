"""saved_searches.py: Implementation of class AbstractTwitterSavedSearchCommand
and its subclasses.
"""

from argparse import ArgumentParser

from . import AbstractTwitterCommand, call_decorator
from ..parsers import cache

# POST saved_searches/create
# POST saved_searches/destroy/:id
# GET saved_searches/list
# GET saved_searches/show/:id

SS_CREATE = ('saved_searches/create', 'create')
SS_DESTROY_ID = ('saved_searches/destroy/:id', 'destroy')
SS_LIST = ('saved_searches/list', 'list')
SS_SHOW_ID = ('saved_searches/show/:id', 'show')

# pylint: disable=abstract-method
class AbstractTwitterSavedSearchCommand(AbstractTwitterCommand):
    """n/a"""
    pass

class CommandCreate(AbstractTwitterSavedSearchCommand):
    """Create a new saved search for the authenticated user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            SS_CREATE[0],
            aliases=SS_CREATE[1:],
            help=self.__doc__)
        parser.add_argument(
            'query',
            help='the query of the search the user would like to save')
        return parser

    @call_decorator
    def __call__(self):
        """Request POST saved_searches/create for Twitter."""

        return dict(query=self.args.query), self.twhandler.saved_searches.create

class CommandDestroyId(AbstractTwitterSavedSearchCommand):
    """Destroy a saved search for the authenticating user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            SS_DESTROY_ID[0],
            aliases=SS_DESTROY_ID[1:],
            parents=[parser_id()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request POST saved_searches/destroy/:id for Twitter."""

        # pylint: disable=protected-access
        return dict(_id=self.args.id), self.twhandler.saved_searches.destroy._id

class CommandList(AbstractTwitterSavedSearchCommand):
    """Print the authenticated user's saved search queries."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            SS_LIST[0],
            aliases=SS_LIST[1:],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET saved_searches/list for Twitter."""

        return {}, self.twhandler.saved_searches.list

class CommandShowId(AbstractTwitterSavedSearchCommand):
    """Print the information for the saved search represented by the
    given id.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            SS_SHOW_ID[0],
            aliases=SS_SHOW_ID[1:],
            parents=[parser_id()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET saved_searches/show/:id for Twitter."""

        # pylint: disable=protected-access
        return dict(_id=self.args.id), self.twhandler.saved_searches.show._id

def make_commands(manager):
    """Prototype"""

    # pylint: disable=no-member
    return (cmd_t(manager) for cmd_t in
            AbstractTwitterSavedSearchCommand.__subclasses__())

@cache
def parser_id():
    """Return the parser for id argument."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        'id',
        metavar='<id>',
        help='the ID of the saved search')
    return parser
