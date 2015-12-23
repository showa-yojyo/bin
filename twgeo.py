#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "Demonstrate Twitter's GET geo/xxx endpoints."

usage = """
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

from twmods import AbstractTwitterManager
from twmods import epilog
from twmods.commands.geo import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.2'

class TwitterGeoManager(AbstractTwitterManager):
    "Demonstrate Twitter's GET geo/xxx endpoints."

    def __init__(self):
        super().__init__('twgeo', make_commands(self))

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the command line
            parameters.
        """

        parser = ArgumentParser(
            description=description,
            epilog=epilog,
            usage=usage)
        parser.add_argument(
            '--version',
            action='version',
            version=__version__)

        return parser

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterGeoManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
