#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to manage a Twitter list."

usage = """
  twlist.py [--version] [--help]
  twlist.py lists-statuses [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>]
    [-E | --include-entities] [--include-rts] <listspec>
  twlist.py lists-members-create_all [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
    <listspec>
  twlist.py lists-members-destroy_all [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
    <listspec>
  twlist.py lists-members [-c | --count <n>] [--cursor <n>]
    [-E | --include-entities] [--skip-status] <listspec>
  twlist.py lists-subscribers [-c | --count <n>] [--cursor <n>]
    [-E | --include-entities] [--skip-status] <listspec>
  twlist.py lists-subscribers-create <listspec>
  twlist.py lists-subscribers-destroy <listspec>
  twlist.py lists-memberships [-c | --count <n>] [--cursor <n>]
    [--filter-to-owned-lists] <userspec>
  twlist.py lists-ownerships [-c | --count <n>] [--cursor <n>]
    <userspec>
  twlist.py lists-subscriptions [-c | --count <n>] [--cursor <n>]
    <userspec>
  twlist.py lists-create [-m | --mode <public | private>]
    [-d | --description <DESC>] <name>
  twlist.py lists-show <listspec>
  twlist.py lists-update [-m | --mode <public | private>]
    [-d | --desccription <DESC>] [--name <NAME>] <listspec>
  twlist.py lists-destroy <listspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
  <listspec> ::= (-l | --list-id <list_id>)
               | (-s | --slug <slug>)
                 ((-OI | --owner-id <owner_id>) 
                | (-OS | --owner-screen-name <owner_screen_name>))
"""

from twmods import AbstractTwitterManager
from twmods import epilog
from twmods.commands.lists import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.9.8'

class TwitterListManager(AbstractTwitterManager):
    """This class handles commands about a Twitter list."""

    def __init__(self):
        super().__init__('twlist', make_commands(self))

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

    mgr = TwitterListManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
