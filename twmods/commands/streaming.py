# -*- coding: utf-8 -*-
"""streaming.py: Implementation of class AbstractTwitterStreamingCommand
and its subclasses.
"""

from .. import AbstractTwitterCommand
from .. import cache
from argparse import ArgumentParser

# Public API
# GET statuses/sample
STREAMING_STATUSES_SAMPLE = ('statuses/sample', 'sample')

# POST statuses/filter
STREAMING_STATUSES_FILTER = ('statuses/filter', 'filter')

# User Streams (domain='userstream.twitter.com')
# GET user
STREAMING_USER = ('user',)

# Site Streams (domain='sitestream.twitter.com')
# GET site
STREAMING_SITE = ('site',)

# GET c/:stream_id/info
# ?

# Firehose
# GET statuses/firehose
STREAMING_STATUSES_FIREHOSE = ('statuses/firehose', 'firehose', 'fire')

class AbstractTwitterStreamingCommand(AbstractTwitterCommand):
    pass

class StatusesSample(AbstractTwitterStreamingCommand):
    """Print a small random sample of all public statuses."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STREAMING_STATUSES_SAMPLE[0],
            aliases=STREAMING_STATUSES_SAMPLE[1:],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_statuses_sample()

class StatusesFilter(AbstractTwitterStreamingCommand):
    """Print public statuses that match one or more filter predicates."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STREAMING_STATUSES_FILTER[0],
            aliases=STREAMING_STATUSES_FILTER[1:],
            parents=[parser_follow(),
                     parser_track_and_locations(),],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_statuses_filter()

class User(AbstractTwitterStreamingCommand):
    """Stream messages for a single user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STREAMING_USER[0],
            #aliases=STREAMING_USER[1:],
            parents=[parser_track_and_locations(),
                     parser_with_and_replies()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_user()

class Site(AbstractTwitterStreamingCommand):
    """Stream messages for a set of users."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STREAMING_SITE[0],
            #aliases=STREAMING_SITE[1:],
            parents=[parser_follow(),
                     parser_with_and_replies()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_site()

class StatusesFirehose(AbstractTwitterStreamingCommand):
    """Print all public statuses."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STREAMING_STATUSES_FIREHOSE[0],
            aliases=STREAMING_STATUSES_FIREHOSE[1:],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_statuses_firehose()

@cache
def parser_track_and_locations():
    """Return the parent parser object for --track and --locations
    optional arguments.
    """

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
    """Return the parent parser object for --follow optional
    argument.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--follow',
        metavar='CSV',
        help='A comma-separated list of user IDs to filter tweets')

    return parser

@cache
def parser_with_and_replies():
    """Return the parent parser object for --with and --replies
    optional arguments.
    """

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
