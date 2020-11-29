#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
from twmods.commands.lists import make_commands

DESCRIPTION = "A utility script to manage a Twitter list."

USAGE = """
  twlist.py [--version] [--help]
  twlist.py lists/statuses [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>]
    [-E | --include-entities] [--include-rts] <listspec>
  twlist.py lists/members/create_all [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
    <listspec>
  twlist.py lists/members/destroy_all [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
    <listspec>
  twlist.py lists/members [-c | --count <n>] [--cursor <n>]
    [-E | --include-entities] [--skip-status] <listspec>
  twlist.py lists/subscribers [-c | --count <n>] [--cursor <n>]
    [-E | --include-entities] [--skip-status] <listspec>
  twlist.py lists/subscribers/create <listspec>
  twlist.py lists/subscribers/destroy <listspec>
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
    [-d | --description <DESC>] [--name <NAME>] <listspec>
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
__version__ = '1.10.0'

MANAGER = make_manager(make_commands, globals())(__file__)

if __name__ == '__main__':
    MANAGER.main()
