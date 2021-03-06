"""trends.py: Implementation of class AbstractTwitterTrendCommand
and its subclasses.
"""

from . import AbstractTwitterCommand, call_decorator
from ..parsers import filter_args

# GET trends/available
# GET trends/closest
# GET trends/place

TREND_AVAILABLE = ('trends/available', 'available')
TREND_CLOSEST = ('trends/closest', 'closest')
TREND_PLACE = ('trends/place', 'place')

# pylint: disable=abstract-method
class AbstractTwitterTrendCommand(AbstractTwitterCommand):
    """n/a"""
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

    @call_decorator
    def __call__(self):
        """Request GET trends/available for Twitter."""

        return {}, self.twhandler.trends.available

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

    @call_decorator
    def __call__(self):
        """Request GET trends/closest for Twitter."""

        request, args = self.twhandler.trends.closest, vars(self.args)
        kwargs = filter_args(
            args,
            'lat', 'long')

        return kwargs, request

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

    @call_decorator
    def __call__(self):
        """Request GET trends/place for Twitter."""

        request, args = self.twhandler.trends.place, vars(self.args)
        kwargs = filter_args(
            args,
            '_id', 'exclude')

        return kwargs, request

def make_commands(manager):
    """Prototype"""

    # pylint: disable=no-member
    return (cmd_t(manager) for cmd_t in
            AbstractTwitterTrendCommand.__subclasses__())
