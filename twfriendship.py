#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser

from twmods import AbstractTwitterManager
from twmods import EPILOG
from twmods.commands.friendships import make_commands

DESCRIPTION = "A utility script to call friendships/xxx of Twitter API."

USAGE = """
  twfriendship.py [--version] [--help]
  twfriendship.py friendships/create [--follow] <userspec>
  twfriendship.py friendships/destroy <userspec>
  twfriendship.py friendships/incoming [--cursor <n>]
  twfriendship.py friendships/lookup [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
  twfriendship.py friendships/no_retweets/ids
  twfriendship.py friendships/outgoing [--cursor <n>]
  twfriendship.py friendships/show (-U <source_user_id> | -S <source_screen_name>)
    (-V <target_user_id> | -T <target_screen_name>)
  twfriendship.py friendships/update [--[no-]device] [--[no-]retweets]
    <userspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.10.2'

class TwitterFriendshipManager(AbstractTwitterManager):
    """This class handles friendships/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twfriendship', make_commands(self))

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

    mgr = TwitterFriendshipManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
