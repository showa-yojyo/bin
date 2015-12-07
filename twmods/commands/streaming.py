# -*- coding: utf-8 -*-
"""twstreamcommands.py:
"""

from .. import AbstractTwitterCommand
from .. import cache
from argparse import ArgumentParser

# Public API
# GET statuses/sample
COMMAND_STATUSES_SAMPLE = ('statuses-sample', 'sample')

# POST statuses/filter
COMMAND_STATUSES_FILTER = ('statuses-filter', 'filter')

# User Streams (domain='userstream.twitter.com')
# GET user
COMMAND_USER = ('user',)

# Site Streams (domain='sitestream.twitter.com')
# GET site
COMMAND_SITE = ('site',)

# GET c/:stream_id/info
# ?

# Firehose
# GET statuses/firehose
COMMAND_STATUSES_FIREHOSE = ('statuses-firehose', 'firehose', 'fire')

class AbstractTwitterStreamingCommand(AbstractTwitterCommand):
    pass

class CommandStatusesSample(AbstractTwitterStreamingCommand):
    """Print a small random sample of all public statuses."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_STATUSES_SAMPLE[0],
            aliases=COMMAND_STATUSES_SAMPLE[1:],
            help='print a small random sample of all public statuses')
        return parser

    def __call__(self):
        self.manager.request_statuses_sample()

class CommandStatusesFilter(AbstractTwitterStreamingCommand):
    """Print public statuses that match one or more filter predicates."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_STATUSES_FILTER[0],
            aliases=COMMAND_STATUSES_FILTER[1:],
            parents=[parser_follow(), parser_track_and_locations(),],
            help='print public statuses that match one or more filter predicates')
        return parser

    def __call__(self):
        self.manager.request_statuses_filter()

class CommandUser(AbstractTwitterStreamingCommand):
    """Stream messages for a single user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_USER[0],
            #aliases=COMMAND_USER[1:],
            parents=[parser_track_and_locations(), parser_with_and_replies()],
            help='stream messages for a single user')
        return parser

    def __call__(self):
        self.manager.request_user()

class CommandSite(AbstractTwitterStreamingCommand):
    """Stream messages for a set of users."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_SITE[0],
            #aliases=COMMAND_SITE[1:],
            parents=[parser_follow(), parser_with_and_replies()],
            help='stream messages for a set of users')
        return parser

    def __call__(self):
        self.manager.request_site()

class CommandStatusesFirehose(AbstractTwitterStreamingCommand):
    """Print all public statuses."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            COMMAND_STATUSES_FIREHOSE[0],
            aliases=COMMAND_STATUSES_FIREHOSE[1:],
            help='print all public statuses')
        return parser

    def __call__(self):
        self.manager.request_statuses_firehose()

@cache
def parser_track_and_locations():
    """TBW"""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--track',
        metavar='CSV',
        help='A comma-separated list of phrases to filter tweets')
    parser.add_argument(
        '--locations',
        metavar='CSV',
        help='A comma-separated list of coordinates specifying a set of bounding boxes to filter tweets')

    return parser

@cache
def parser_follow():
    """TBW"""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--follow',
        metavar='CSV',
        help='A comma-separated list of user IDs to filter tweets')

    return parser

@cache
def parser_with_and_replies():
    """TBW"""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--with',
        choices=('user', 'followings',),
        help='the types of messages')
    parser.add_argument(
        '--replies',
        choices=('all',),
        help='show all replies')

    return parser

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterStreamingCommand.__subclasses__()]
