"""favorites.py: Implementation of class AbstractTwitterFavoriteCommand
and its subclasses.
"""

from argparse import ArgumentParser

from . import AbstractTwitterCommand, call_decorator
from ..parsers import (
    filter_args,
    cache,
    parser_user_single,
    parser_count_statuses,
    parser_since_max_ids,
    parser_include_entities,)

# POST favorites/create
# POST favorites/destroy
# GET favorites/list

FAV_CREATE = ('favorites/create', 'create')
FAV_DESTROY = ('favorites/destroy', 'destroy')
FAV_LIST = ('favorites/list', 'list')

# pylint: disable=abstract-method
class AbstractTwitterFavoriteCommand(AbstractTwitterCommand):
    """n/a"""
    pass

class CommandCreate(AbstractTwitterFavoriteCommand):
    """Like the status specified in the ID parameter as the
    authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FAV_CREATE[0],
            aliases=FAV_CREATE[1:],
            parents=[parser_id(),
                     parser_include_entities()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request POST favorites/create for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            '_id', 'include_entities')

        return kwargs, self.twhandler.favorites.create

class CommandDestroy(AbstractTwitterFavoriteCommand):
    """Un-like the status specified in the ID parameter as the
    authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FAV_DESTROY[0],
            aliases=FAV_DESTROY[1:],
            parents=[parser_id(),
                     parser_include_entities()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request POST favorites/destroy for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            '_id', 'include_entities')

        return kwargs, self.twhandler.favorites.destroy

class CommandList(AbstractTwitterFavoriteCommand):
    """Print the 20 most recent Tweets liked by the authenticating
    or specified user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            FAV_LIST[0],
            aliases=FAV_LIST[1:],
            parents=[parser_user_single(),
                     parser_count_statuses(), # 20, 200
                     parser_since_max_ids(),
                     parser_include_entities()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET favorites/list for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'user_id', 'screen_name',
            'count', 'since_id', 'max_id', 'include_entities')

        return kwargs, self.twhandler.favorites.list

def make_commands(manager):
    """Prototype"""

    # pylint: disable=no-member
    return (cmd_t(manager) for cmd_t in
            AbstractTwitterFavoriteCommand.__subclasses__())

@cache
def parser_id():
    """Return the parser for id argument."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '_id',
        metavar='<id>',
        help='the numerical ID of the desired status')
    return parser
