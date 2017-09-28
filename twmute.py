#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
from twmods.commands.mutes import make_commands

DESCRIPTION = "A utility script to call mutes/xxx of Twitter API."

USAGE = """
  twmute.py [--version] [--help]
  twmute.py mutes/users/create <userspec>
  twmute.py mutes/users/destroy <userspec>
  twmute.py mutes/users/ids [--cursor <n>]
  twmute.py mutes/users/list [--cursor <n>] [-E | --include-entities]
    [--skip-status]

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.1.0'

MANAGER = make_manager(make_commands, globals())(__file__)

if __name__ == '__main__':
    MANAGER.main()
