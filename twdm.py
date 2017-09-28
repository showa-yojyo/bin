#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
from twmods.commands.direct_messages import make_commands

DESCRIPTION = "A utility script to call direct_messages/xxx of Twitter API."

USAGE = """
  twdm.py [--version] [--help]
  twdm.py direct_messages [--since-id <status_id>]
    [--max-id <status_id>] [-c | --count <n>]
    [-E | --include-entities] [--skip-status]
  twdm.py direct_messages/destroy [-E | --include-entities] <dm_id>
  twdm.py direct_messages/new <userspec> <text>
  twdm.py direct_messages/sent [--since-id <status_id>]
    [--max-id <status_id>] [-c | --count <n>] [-p | --page <n>]
    [-E | --include-entities]
  twdm.py direct_messages/show <dm_id>

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
