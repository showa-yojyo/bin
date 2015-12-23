#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to call trends/xxx of Twitter API."

usage = """
  twtrend.py [--version] [--help]
  twtrend.py trends/available
  twtrend.py trends/closest <longitude> <latitude>
  twtrend.py trends/place [--exclude {hashtags}] <woeid>
"""

from twmods import AbstractTwitterManager
from twmods import epilog
from twmods.commands.trends import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.1'

class TwitterTrendManager(AbstractTwitterManager):
    """This class handles trends/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twtrend', make_commands(self))

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the command line
            parameters.
        """

        parser = ArgumentParser(
            description=description, epilog=epilog, usage=usage)
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
