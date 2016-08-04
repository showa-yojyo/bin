#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser

from twmods import AbstractTwitterManager
from twmods import EPILOG
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
__version__ = '1.0.2'

class TwitterTrendManager(AbstractTwitterManager):
    """This class handles trends/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twtrend', make_commands(self))

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

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterTrendManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
