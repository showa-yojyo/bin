# -*- coding: utf-8 -*-
"""users.py: Implementation of class AbstractTwitterUsersCommand
and its subclasses.
"""

from .. import AbstractTwitterCommand
from .. import cache
from .. import (parser_full,
                parser_user_single,
                parser_user_multiple,
                parser_include_entities)
from argparse import ArgumentParser

# Available subcommands.
# names[0] and names[1:] are the official name and aliases, respectively.
USERS_LOOKUP = ('users/lookup', 'lookup')
USERS_SHOW = ('users/show', 'show')
USERS_SEARCH = ('users/search', 'search')
USERS_PROFILE_BANNER = ('users/profile_banner', 'banner')
USERS_SUGGESTIONS = ('users/suggestions', 'suggestions', 'sug')
USERS_REPORT_SPAM = ('users/report_spam', 'spam')

# GET users/lookup <- USERS_LOOKUP
# GET users/show <- USERS_SHOW
# GET users/search <- USERS_SEARCH
# GET users/profile_banner <- USERS_PROFILE_BANNER
# GET users/suggestions/:slug - n/a
# GET users/suggestions <- USERS_SUGGESTIONS
# GET users/suggestions/:slug/members - n/a
# POST users/report_spam <- USERS_REPORT_SPAM

class AbstractTwitterUsersCommand(AbstractTwitterCommand):
    pass

class Lookup():
    """Print fully-hydrated user objects."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            USERS_LOOKUP[0],
            aliases=USERS_LOOKUP[1:],
            parents=[parser_user_multiple()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_users_lookup()

class Show(AbstractTwitterUsersCommand):
    """Print information about the user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            USERS_SHOW[0],
            aliases=USERS_SHOW[1:],
            parents=[parser_user_single(),
                     parser_include_entities()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_users_show()

class Search(AbstractTwitterUsersCommand):
    """Search public user accounts."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            USERS_SEARCH[0],
            aliases=USERS_SEARCH[1:],
            parents=[parser_full(), parser_include_entities()],
            help=self.__doc__)
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
        return parser

    def __call__(self):
        self.manager.request_users_search()

class ProfileBanner(AbstractTwitterUsersCommand):
    """Print a map of the available size variations 
    of the specified user's profile banner.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            USERS_PROFILE_BANNER[0],
            aliases=USERS_PROFILE_BANNER[1:],
            parents=[parser_user_single()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_users_profile_banner()

class Suggestions(AbstractTwitterUsersCommand):
    """Print the list of suggested user categories."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            USERS_SUGGESTIONS[0],
            aliases=USERS_SUGGESTIONS[1:],
            help=self.__doc__)
        parser.add_argument(
            '-l', '--lang',
            help='the requested language (with ISO 639-1 representation)')
        return parser

    def __call__(self):
        self.manager.request_users_suggestions()

class ReportSpam(AbstractTwitterUsersCommand):
    """Report the specified user as a spam account to Twitter."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            USERS_REPORT_SPAM[0],
            aliases=USERS_REPORT_SPAM[1:],
            parents=[parser_user_single()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_users_report_spam()

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterUsersCommand.__subclasses__()]
