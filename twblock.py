#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to call blocks/xxx of Twitter API."

usage = """
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

from twmods import AbstractTwitterManager
from twmods import (epilog, output)
from twmods.commands.blocks import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.2'

class TwitterBlockManager(AbstractTwitterManager):
    """This class handles blocks/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twblock', make_commands(self))

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

    mgr = TwitterBlockManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
