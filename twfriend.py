#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to call friends/xxx of Twitter API."

usage = """
  twfriend.py [--version] [--help]
  twfriend.py friends/ids [-c | --count <n>] [--cursor <n>]
    <userspec>
  twfriend.py friends/list [--cursor <n>] [--skip-status]
    [--include-user-entities] <userspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

from twmods import AbstractTwitterManager
from twmods import epilog
from twmods.commands.friends import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.10.1'

class TwitterFriendManager(AbstractTwitterManager):
    """This class handles friends/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twfriend', make_commands(self))

    def make_parser(self, pre_parser):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the command line
            parameters.
        """

        parser = ArgumentParser(
            parents=[pre_parser],
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

    mgr = TwitterFriendManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
