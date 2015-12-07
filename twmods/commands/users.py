# -*- coding: utf-8 -*-
"""usercommands.py
"""
__version__ = '1.0.3'

from .. import AbstractTwitterCommand
from .. import cache
from .. import parser_user_single
from argparse import ArgumentParser
from argparse import FileType

# Available subcommands.
# names[0] and names[1:] are the official name and aliases, respectively.
COMMAND_USERS_LOOKUP = ('users-lookup', 'lookup')
COMMAND_USERS_SHOW = ('users-show', 'show')
COMMAND_USERS_SEARCH = ('users-search', 'search')
COMMAND_USERS_PROFILE_BANNER = ('users-profile-banner', 'banner')
COMMAND_USERS_SUGGESTIONS = ('users-suggestions', 'suggestions', 'sug')
COMMAND_USERS_REPORT_SPAM = ('users-report-spam', 'spam')

# GET users/lookup <- COMMAND_USERS_LOOKUP
# GET users/show <- COMMAND_USERS_SHOW
# GET users/search <- COMMAND_USERS_SEARCH
# GET users/profile_banner <- COMMAND_USERS_PROFILE_BANNER
# GET users/suggestions/:slug - n/a
# GET users/suggestions <- COMMAND_USERS_SUGGESTIONS
# GET users/suggestions/:slug/members - n/a
# POST users/report_spam <- COMMAND_USERS_REPORT_SPAM

class CommandUsersLookup(AbstractTwitterCommand):
    """Print fully-hydrated user objects."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_USERS_LOOKUP[0],
            aliases=COMMAND_USERS_LOOKUP[1:],
            parents=[parser_user_multiple()],
            help='print fully-hydrated user objects')
        return parser

    def __call__(self):
        self.manager.request_users_lookup()

class CommandUsersShow(AbstractTwitterCommand):
    """Print information about the user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_USERS_SHOW[0],
            aliases=COMMAND_USERS_SHOW[1:],
            parents=[parser_user_single(), parser_include_entities()],
            help='print information about the user')
        return parser

    def __call__(self):
        self.manager.request_users_show()

class CommandUsersSearch(AbstractTwitterCommand):
    """Search public user accounts."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_USERS_SEARCH[0],
            aliases=COMMAND_USERS_SEARCH[1:],
            parents=[parser_include_entities()],
            help='search public user accounts')
        parser.add_argument(
            'q',
            help='the search query to run against people search')
        parser.add_argument(
            '-p', '--page',
            type=int,
            help='the page ranges of results to retrieve')
        parser.add_argument(
            '-c', '--count',
            type=int,
            choices=range(1, 21),
            metavar='{1..20}',
            help='the number of potential user results to retrieve per page')
        parser.add_argument(
            '--full',
            action='store_true',
            help='retrieve data as much as possible')
        return parser

    def __call__(self):
        self.manager.request_users_search()

class CommandUsersProfileBanner(AbstractTwitterCommand):
    """Print a map of the available size variations 
    of the specified user's profile banner.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_USERS_PROFILE_BANNER[0],
            aliases=COMMAND_USERS_PROFILE_BANNER[1:],
            parents=[parser_user_single()],
            help='print multiple URLs of profile banner available')
        return parser

    def __call__(self):
        self.manager.request_users_profile_banner()

class CommandUsersSuggestions(AbstractTwitterCommand):
    """Print the list of suggested user categories."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_USERS_SUGGESTIONS[0],
            aliases=COMMAND_USERS_SUGGESTIONS[1:],
            help='print the list of suggested user categories')
        parser.add_argument(
            '-l', '--lang',
            help='the requested language (with ISO 639-1 representation)')
        return parser

    def __call__(self):
        self.manager.request_users_suggestions()

class CommandUsersReportSpam(AbstractTwitterCommand):
    """Report the specified user as a spam account to Twitter."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_USERS_REPORT_SPAM[0],
            aliases=COMMAND_USERS_REPORT_SPAM[1:],
            parents=[parser_user_single()],
            help='report the specified user as a spam account to Twitter')
        return parser

    def __call__(self):
        self.manager.request_users_report_spam()

_command_classes = tuple(v for k, v in locals().items() if k.startswith('CommandUsers'))

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in _command_classes]

@cache
def parser_user_multiple():
    """Multiple arguments for user_id or screen_name."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-U', '--user-id',
        nargs='*',
        dest='user_id',
        help='the ID of the user for whom to return results')
    parser.add_argument(
        '-S', '--screen-name',
        nargs='*',
        dest='screen_name',
        help='the screen name of the user for whom to return results')
    parser.add_argument(
        '-UF', '--file-user-id',
        type=FileType('r'),
        default=None,
        dest='file_user_id',
        help='a file which lists user IDs')
    parser.add_argument(
        '-SF', '--file-screen-name',
        type=FileType('r'),
        default=None,
        dest='file_screen_name',
        help='a file which lists screen names')
    return parser

@cache
def parser_include_entities():
    """An argument for include_entities."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-E', '--include-entities',
        action='store_true',
        dest='include_entities',
        help='include entity nodes in tweet objects')
    return parser
