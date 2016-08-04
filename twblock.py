#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser

from twmods import AbstractTwitterManager
from twmods import EPILOG
from twmods.commands.blocks import make_commands

DESCRIPTION = "A utility script to call blocks/xxx of Twitter API."

USAGE = """
  twblock.py [--version] [--help]
  twblock.py blocks/create [-E | --include-entities]
    [--skip-status] <userspec>
  twblock.py blocks/destroy [-E | --include-entities]
    [--skip-status] <userspec>
  twblock.py blocks/ids [--cursor <n>] [-E | --include-entities]
    [--skip-status]
  twblock.py blocks/list [--cursor <n>] [-E | --include-entities]
    [--skip-status]

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.0.3'

class TwitterBlockManager(AbstractTwitterManager):
    """This class handles blocks/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twblock', make_commands(self))

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

    mgr = TwitterBlockManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
