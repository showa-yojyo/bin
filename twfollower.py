#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser

from twmods import (AbstractTwitterManager, EPILOG)
from twmods.commands.followers import make_commands

DESCRIPTION = "A utility script to call followers/xxx of Twitter API."

USAGE = """
  twfollower.py [--version] [--help]
  twfollower.py followers/ids [-c | --count <n>] [--cursor <n>]
    <userspec>
  twfollower.py followers/list [--cursor <n>] [--skip-status]
    [--include-user-entities] <userspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.10.4'

class TwitterFollowerManager(AbstractTwitterManager):
    """This class handles followers/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twfollower', make_commands(self))

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

mgr = TwitterFollowerManager()

if __name__ == '__main__':
    mgr.main()
