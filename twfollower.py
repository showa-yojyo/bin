#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
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
__version__ = '1.11.0'

MANAGER = make_manager(make_commands, globals())(__file__)

if __name__ == '__main__':
    MANAGER.main()
