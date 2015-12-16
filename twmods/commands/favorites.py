# -*- coding: utf-8 -*-
"""favorites.py: Implementation of class AbstractTwitterFavoriteCommand
and its subclasses.
"""

from .. import AbstractTwitterCommand
from .. import cache
from .. import (parser_user_single,
                parser_count_statuses,
                parser_since_max_ids,
                parser_include_entities,)
from argparse import ArgumentParser

# POST favorites/create
# POST favorites/destroy
# GET favorites/list

FAV_CREATE = ('favorites/create', 'create')
FAV_DESTROY = ('favorites/destroy', 'destroy')
FAV_LIST = ('favorites/list', 'list')

class AbstractTwitterFavoriteCommand(AbstractTwitterCommand):
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

    def __call__(self):
        self.manager.request_favorites_create()

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

    def __call__(self):
        self.manager.request_favorites_destroy()

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

    def __call__(self):
        self.manager.request_favorites_list()

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterFavoriteCommand.__subclasses__()]

@cache
def parser_id():
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '_id',
        metavar='<id>',
        help='the numerical ID of the desired status')
    return parser
