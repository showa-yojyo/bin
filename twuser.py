#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser

from twmods import (AbstractTwitterManager, EPILOG)
from twmods.commands.users import make_commands

DESCRIPTION = "A utility script to manage Twitter users."

USAGE = """
  twuser.py [--version] [--help]
  twuser.py users-lookup [<userspec>...]
    [-UF | --file-user-id <path>]
    [-SF | --file-screen-name <path>]
  twuser.py users-show [--include-entities] <userspec>
  twuser.py users-search [-F | --full] [-p | --page <n>]
    [-c | --count <n>] [-E | --include-entities] <query>
  twuser.py users-profile-banner <userspec>
  twuser.py users-suggestions [-l | --lang <LANG>]
  twuser.py users-report-spam <userspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.1.5'

class TwitterUserManager(AbstractTwitterManager):
    """This class handles commands about a Twitter users."""

    def __init__(self):
        super().__init__('twuser', make_commands(self))

    def make_parser(self, pre_parser):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that stores the command line
            parameters.
        """

        parser = ArgumentParser(
            parents=[pre_parser],
            description=DESCRIPTION, epilog=EPILOG, usage=USAGE)
        parser.add_argument(
            '--version',
            action='version',
            version=__version__)
        return parser

mgr = TwitterUserManager()

if __name__ == '__main__':
    mgr.main()
