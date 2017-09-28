#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
from twmods.commands.favorites import make_commands

DESCRIPTION = "A utility script to call favorites/xxx of Twitter API."

USAGE = """
  twfav.py [--version] [--help]
  twfav.py favorites/create [-E | --include-entities] <status_id>
  twfav.py favorites/destroy [-E | --include-entities] <status_id>
  twfav.py favorites/list [-c | --count <n>] [--since-id <status_id>]
    [--max-id <status_id>] [-E | --include-entities] <userspec>

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
