"""geo.py: Implementation of class AbstractTwitterGeoCommand
and its subclasses.
"""

from argparse import ArgumentParser

from . import (AbstractTwitterCommand, call_decorator)
from ..parsers import (filter_args, cache)

# GET geo/id/:place_id
# POST geo/place DEPRECATED
# GET geo/reverse_geocode
# GET geo/search

GEO_ID_PLACE_ID = ('geo/id/:place_id', 'id')
GEO_REVERSE_GEOCODE = ('geo/reverse_geocode', 'reverse')
GEO_SEARCH = ('geo/search', 'search')

# pylint: disable=abstract-method
class AbstractTwitterGeoCommand(AbstractTwitterCommand):
    """n/a"""
    pass

class IdPlaceId(AbstractTwitterGeoCommand):
    """Output all the information about a known place."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            GEO_ID_PLACE_ID[0],
            aliases=GEO_ID_PLACE_ID[1:],
            help=self.__doc__)
        parser.add_argument(
            'place_id',
            help='a place in the world where can be retrieved '
                 'from geo/reverse_geocode')
        return parser

    @call_decorator
    def __call__(self):
        """Request GET geo/id/:place_id for Twitter."""

        # pylint: disable=protected-access
        kwargs = dict(_id=self.args.place_id)
        return kwargs, self.twhandler.geo.id._id # hack?

class ReverseGeocode(AbstractTwitterGeoCommand):
    """Search for up to 20 places that can be used as a place_id."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            GEO_REVERSE_GEOCODE[0],
            aliases=GEO_REVERSE_GEOCODE[1:],
            parents=[parser_geo_common()],
            help=self.__doc__)
        parser.add_argument(
            'long',
            metavar='{-180.0..180.0}',
            help='the longitude to search around')
        parser.add_argument(
            'lat',
            metavar='{-90.0..90.0}',
            help='the latitude to search around')

        return parser

    @call_decorator
    def __call__(self):
        """Request GET geo/reverse_geocode for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'lat', 'long', 'accuracy', 'granularity', 'max_results')

        return kwargs, self.twhandler.geo.reverse_geocode

class Search(AbstractTwitterGeoCommand):
    """Search for places that can be attached to a statuses/update."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            GEO_SEARCH[0],
            aliases=GEO_SEARCH[1:],
            parents=[parser_geo_common()],
            help=self.__doc__)
        parser.add_argument(
            '--long',
            metavar='{-180.0..180.0}',
            help='the longitude to search around')
        parser.add_argument(
            '--lat',
            metavar='{-90.0..90.0}',
            help='the latitude to search around')
        parser.add_argument(
            '-q', '--query',
            metavar='<text>',
            help='free-form text to match against '
                 'while executing a geo-based query')
        parser.add_argument(
            '-i', '--ip-address',
            dest='ip',
            metavar='<ip-address>',
            help='an IP address')
        parser.add_argument(
            '-c', '--contained-within',
            dest='contained_within',
            metavar='<place_id>',
            help='the place_id which you would like '
                 'to restrict the search results to')
        parser.add_argument(
            '-s', '--street-address',
            dest='street_address',
            metavar='<text>',
            help='search for places which have this given street address')
        return parser

    @call_decorator
    def __call__(self):
        """Request GET geo/search for Twitter."""

        kwargs = filter_args(
            vars(self.args),
            'lat', 'long', 'accuracy', 'granularity', 'max_results',
            'query', 'ip', 'contained_within', 'street_address')

        return kwargs, self.twhandler.geo.search

def make_commands(manager):
    """Prototype"""

    # pylint: disable=no-member
    return (cmd_t(manager) for cmd_t in
            AbstractTwitterGeoCommand.__subclasses__())

CHOICES = ('poi', 'neighborhood', 'city', 'admin', 'country')

@cache
def parser_geo_common():
    """Return the parser for common arguments."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-a', '--accuracy',
        help='a hint on the region in which to search')
    parser.add_argument(
        '-g', '--granularity',
        choices=CHOICES,
        metavar='|'.join(CHOICES),
        help='the minimal granularity of place types to return')
    parser.add_argument(
        '-m', '--max-results',
        type=int,
        dest='max_results',
        help='a hint as to the number of results to return')
    return parser
