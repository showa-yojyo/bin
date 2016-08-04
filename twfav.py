#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser

from twmods import AbstractTwitterManager
from twmods import EPILOG
from twmods.commands.favorites import make_commands

DESCRIPTION = "A utility script to call favorites/xxx of Twitter API."

USAGE = """
  twfav.py [--version] [--help]
  twfav.py favorites/create [-E | --include-entities] <status_id>
  twfav.py favorites/destroy [-E | --include-entities] <status_id>
  twfav.py favorites/list [-c | --count <n>] [--since-id <status_id>]
    [--max-id <status_id>] [-E | --include-entities] <userspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.0.2'

class TwitterFavoriteManager(AbstractTwitterManager):
    """This class handles favorites/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twfav', make_commands(self))

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

    mgr = TwitterFavoriteManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
