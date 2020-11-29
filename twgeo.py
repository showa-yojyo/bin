#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
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
__version__ = '1.1.0'

MANAGER = make_manager(make_commands, globals())(__file__)

if __name__ == '__main__':
    MANAGER.main()
