#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
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
__version__ = '1.2.0'

MANAGER = make_manager(make_commands, globals())(__file__)

if __name__ == '__main__':
    MANAGER.main()
