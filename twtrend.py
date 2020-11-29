#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
from twmods.commands.trends import make_commands

DESCRIPTION = "A utility script to call trends/xxx of Twitter API."

USAGE = """
  twtrend.py [--version] [--help]
  twtrend.py trends/available
  twtrend.py trends/closest <longitude> <latitude>
  twtrend.py trends/place [--exclude {hashtags}] <woeid>
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.1.0'

MANAGER = make_manager(make_commands, globals())(__file__)

if __name__ == '__main__':
    MANAGER.main()
