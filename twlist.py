#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser

from twmods import AbstractTwitterManager
from twmods import EPILOG
from twmods.commands.lists import make_commands

DESCRIPTION = "A utility script to manage a Twitter list."

USAGE = """
  twlist.py [--version] [--help]
  twlist.py lists/statuses [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>]
    [-E | --include-entities] [--include-rts] <listspec>
  twlist.py lists/members-create_all [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
    <listspec>
  twlist.py lists/members-destroy_all [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
    <listspec>
  twlist.py lists/members [-c | --count <n>] [--cursor <n>]
    [-E | --include-entities] [--skip-status] <listspec>
  twlist.py lists/subscribers [-c | --count <n>] [--cursor <n>]
    [-E | --include-entities] [--skip-status] <listspec>
  twlist.py lists/subscribers-create <listspec>
  twlist.py lists/subscribers-destroy <listspec>
  twlist.py lists/memberships [-c | --count <n>] [--cursor <n>]
    [--filter-to-owned-lists] <userspec>
  twlist.py lists/ownerships [-c | --count <n>] [--cursor <n>]
    <userspec>
  twlist.py lists/subscriptions [-c | --count <n>] [--cursor <n>]
    <userspec>
  twlist.py lists/create [-m | --mode <public | private>]
    [-d | --description <DESC>] <name>
  twlist.py lists/show <listspec>
  twlist.py lists/update [-m | --mode <public | private>]
    [-d | --desccription <DESC>] [--name <NAME>] <listspec>
  twlist.py lists/destroy <listspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
  <listspec> ::= (-l | --list-id <list_id>)
               | (-s | --slug <slug>)
                 ((-OI | --owner-id <owner_id>) 
                | (-OS | --owner-screen-name <owner_screen_name>))
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.9.10'

class TwitterListManager(AbstractTwitterManager):
    """This class handles commands about a Twitter list."""

    def __init__(self):
        super().__init__('twlist', make_commands(self))

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

    mgr = TwitterListManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
