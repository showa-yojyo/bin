#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser

from twmods import (AbstractTwitterManager, EPILOG)
from twmods.commands.geo import make_commands

DESCRIPTION = "Demonstrate Twitter's GET geo/xxx endpoints."

USAGE = """
  twgeo.py [--version] [--help]
  twgeo.py geo/id/:place_id <place_id>
  twgeo.py geo/reverse_geocode [--lat <angle>] [--long <angle>]
    [-a | --accuracy <distance>] [-g | --granularity <G>]
    [-m | --max-results <n>]
  twgeo.py geo/search [--lat <angle>] [--long <angle>]
    [-q | --query <text>] [-i | --ip-address <IP>]
    [-a | --accuracy <distance>] [-g | --granularity <G>]
    [-m | --max-results <n>] [-c | --contained-with <place_id>]
    [-s | --street-address <addr>]
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.0.4'

class TwitterGeoManager(AbstractTwitterManager):
    "Demonstrate Twitter's GET geo/xxx endpoints."

    def __init__(self):
        super().__init__('twgeo', make_commands(self))

    def make_parser(self, pre_parser):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the
            command line parameters.
        """

        parser = ArgumentParser(
            parents=[pre_parser],
            description=DESCRIPTION,
            epilog=EPILOG,
            usage=USAGE)
        parser.add_argument(
            '--version',
            action='version',
            version=__version__)

        return parser

mgr = TwitterGeoManager()

if __name__ == '__main__':
    mgr.main()
