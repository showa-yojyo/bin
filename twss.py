#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser

from twmods import (AbstractTwitterManager, EPILOG)
from twmods.commands.saved_searches import make_commands

DESCRIPTION = "A utility script to call saved_searches/xxx of Twitter API."

USAGE = """
  twss.py [--version] [--help]
  twss.py saved_searches/create <query>
  twss.py saved_searches/destroy/:id <id>
  twss.py saved_searches/list
  twss.py saved_searches/show/:id <id>
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.0.3'

class TwitterSavedSearchManager(AbstractTwitterManager):
    """This class handles saved_searches/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twss', make_commands(self))

    def make_parser(self, pre_parser):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the
            command line parameters.
        """

        parser = ArgumentParser(
            parents=[pre_parser],
            description=DESCRIPTION, epilog=EPILOG, usage=USAGE)
        parser.add_argument(
            '--version',
            action='version',
            version=__version__)
        return parser

mgr = TwitterSavedSearchManager()

if __name__ == '__main__':
    mgr.main()
