# -*- coding: utf-8 -*-
"""geo.py: Implementation of class AbstractTwitterGeoCommand
and its subclasses.
"""

from .. import AbstractTwitterCommand
from .. import cache
from argparse import ArgumentParser

# GET geo/id/:place_id
# POST geo/place DEPRECATED
# GET geo/reverse_geocode
# GET geo/search

GEO_ID_PLACE_ID = ('geo/id/:place_id', 'id')
GEO_REVERSE_GEOCODE = ('geo/reverse_geocode', 'reverse')
GEO_SEARCH = ('geo/search', 'search')

class AbstractTwitterGeoCommand(AbstractTwitterCommand):
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
            help='a place in the world where can be retrieved from geo/reverse_geocode')
        return parser

    def __call__(self):
        self.manager.request_id_place_id()

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

    def __call__(self):
        self.manager.request_reverse_geocode()

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
            help='free-form text to match against while executing a geo-based query')
        parser.add_argument(
            '-i', '--ip-address',
            dest='ip',
            metavar='<ip-address>',
            help='an IP address')
        parser.add_argument(
            '-c', '--contained-within',
            dest='contained_within',
            metavar='<place_id>',
            help='the place_id which you would like to restrict the search results to')
        parser.add_argument(
            '-s', '--street-address',
            dest='street_address',
            metavar='<text>',
            help='search for places which have this given street address')
        return parser

    def __call__(self):
        self.manager.request_search()

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterGeoCommand.__subclasses__()]

choices = ['poi', 'neighborhood', 'city', 'admin', 'country']

@cache
def parser_geo_common():
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-a', '--accuracy',
        help='a hint on the region in which to search')
    parser.add_argument(
        '-g', '--granularity',
        choices=choices,
        metavar='|'.join(choices),
        help='the minimal granularity of place types to return')
    parser.add_argument(
        '-m', '--max-results',
        type=int,
        dest='max_results',
        help='a hint as to the number of results to return')
    return parser
