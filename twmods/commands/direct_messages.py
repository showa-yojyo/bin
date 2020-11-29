"""direct_messages.py: Implementation of class
AbstractTwitterDirectMessageCommand and its subclasses.
"""

from argparse import ArgumentParser

from . import AbstractTwitterCommand, call_decorator
from ..parsers import (
    filter_args,
    cache,
    parser_user_single,
    parser_count_statuses,
    parser_page,
    parser_since_max_ids,
    parser_include_entities,
    parser_skip_status,)

# GET direct_messages
# POST direct_messages/destroy
# POST direct_messages/new
# GET direct_messages/sent
# GET direct_messages/show

DM = ('direct_messages', 'list')
DM_DESTROY = ('direct_messages/destroy', 'destroy')
DM_NEW = ('direct_messages/new', 'new', 'create')
DM_SENT = ('direct_messages/sent', 'sent')
DM_SHOW = ('direct_messages/show', 'show')

# pylint: disable=abstract-method
class AbstractTwitterDirectMessageCommand(AbstractTwitterCommand):
    """n/a"""
    pass

class Command(AbstractTwitterDirectMessageCommand):
    """Print the 20 most recent direct messages sent to the
    authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            DM[0],
            aliases=DM[1:],
            parents=[parser_since_max_ids(),
                     parser_count_statuses(), # 20, 200
                     parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET direct_messages for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'since_id', 'max_id',
            'count', 'include_entities', 'skip_status')

        return kwargs, self.twhandler.direct_messages

class CommandDestroy(AbstractTwitterDirectMessageCommand):
    """Destroy the direct message specified in the required ID
    parameter.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            DM_DESTROY[0],
            aliases=DM_DESTROY[1:],
            parents=[parser_id(),
                     parser_include_entities()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request POST direct_messages/destroy for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            '_id', 'include_entities')

        return kwargs, self.twhandler.direct_messages.destroy

class CommandNew(AbstractTwitterDirectMessageCommand):
    """Send a new direct message to the specified user from the
    authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            DM_NEW[0],
            aliases=DM_NEW[1:],
            parents=[parser_user_single()],
            help=self.__doc__)
        parser.add_argument(
            'text',
            help='the text of your direct message')
        return parser

    @call_decorator
    def __call__(self):
        """Request POST direct_messages/new for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'user_id', 'screen_name', 'text')

        return kwargs, self.twhandler.direct_messages.new

class CommandSent(AbstractTwitterDirectMessageCommand):
    """Print the 20 most recent direct messages sent by the
    authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            DM_SENT[0],
            aliases=DM_SENT[1:],
            parents=[parser_since_max_ids(),
                     parser_count_statuses(),
                     parser_page(),
                     parser_include_entities()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET direct_messages/sent for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'since_id', 'max_id',
            'count', 'page', 'include_entities')

        return kwargs, self.twhandler.direct_messages.sent

class CommandShow(AbstractTwitterDirectMessageCommand):
    """Print a single direct message, specified by an id parameter."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            DM_SHOW[0],
            aliases=DM_SHOW[1:],
            parents=[parser_id()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET direct_messages/show for Twitter."""

        # pylint: disable=protected-access
        return dict(_id=self.args._id), self.twhandler.direct_messages.show

def make_commands(manager):
    """Prototype"""

    # pylint: disable=no-member
    return (cmd_t(manager) for cmd_t in
            AbstractTwitterDirectMessageCommand.__subclasses__())

@cache
def parser_id():
    """Return the parser for id argument."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '_id',
        metavar='<dm_id>',
        help='the ID of the direct message to delete')
    return parser
