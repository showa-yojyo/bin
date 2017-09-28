#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser

from twmods import (AbstractTwitterManager, EPILOG)
from twmods.commands.friends import make_commands

DESCRIPTION = "A utility script to call friends/xxx of Twitter API."

USAGE = """
  twfriend.py [--version] [--help]
  twfriend.py friends/ids [-c | --count <n>] [--cursor <n>]
    <userspec>
  twfriend.py friends/list [--cursor <n>] [--skip-status]
    [--include-user-entities] <userspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.10.3'

class TwitterFriendManager(AbstractTwitterManager):
    """This class handles friends/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twfriend', make_commands(self))

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

mgr = TwitterFriendManager()

if __name__ == '__main__':
    mgr.main()
