#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to manage Twitter users."

usage = """
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

from twmods import AbstractTwitterManager
from twmods import epilog
from twmods.commands.users import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.1.3'

class TwitterUserManager(AbstractTwitterManager):
    """This class handles commands about a Twitter users."""

    def __init__(self):
        super().__init__('twuser', make_commands(self))

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that stores the command line
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

    mgr = TwitterUserManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
