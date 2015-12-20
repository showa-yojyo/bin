# -*- coding: utf-8 -*-
"""trends.py: Implementation of class AbstractTwitterTrendCommand
and its subclasses.
"""

from .. import AbstractTwitterCommand
from argparse import ArgumentParser

# GET trends/available
# GET trends/closest
# GET trends/place

TREND_AVAILABLE = ('trends/available', 'available')
TREND_CLOSEST = ('trends/closest', 'closest')
TREND_PLACE = ('trends/place', 'place')

class AbstractTwitterTrendCommand(AbstractTwitterCommand):
    pass

class CommandAvailable(AbstractTwitterTrendCommand):
    """Print the locations that Twitter has trending topic
    information for.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            TREND_AVAILABLE[0],
            aliases=TREND_AVAILABLE[1:],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_trends_available()

class CommandClosest(AbstractTwitterTrendCommand):
    """Print the locations that Twitter has trending topic
    information for, closest to a specified location.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            TREND_CLOSEST[0],
            aliases=TREND_CLOSEST[1:],
            help=self.__doc__)
        parser.add_argument(
            'long',
            metavar='{-180.0..180.0}',
            help='the longitude that specifies trend locations')
        parser.add_argument(
            'lat',
            metavar='{-90.0..90.0}',
            help='the latitude that specifies trend locations')
        return parser

    def __call__(self):
        self.manager.request_trends_closest()

class CommandPlace(AbstractTwitterTrendCommand):
    """Print the top 50 trending topics for a specific WOEID, if
    trending information is available for it.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            TREND_PLACE[0],
            aliases=TREND_PLACE[1:],
            help=self.__doc__)
        parser.add_argument(
            '_id',
            metavar='<woeid>',
            help='the Yahoo! Where On Earth ID of the location')
        parser.add_argument(
            '--exclude',
            metavar='{hashtags}',
            help='remove all hashtags from the trends list')
        return parser

    def __call__(self):
        self.manager.request_trends_place()

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterTrendCommand.__subclasses__()]