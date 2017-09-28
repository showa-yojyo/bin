#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
from twmods.commands.blocks import make_commands

DESCRIPTION = "A utility script to call blocks/xxx of Twitter API."

USAGE = """
  twblock.py [--version] [--help]
  twblock.py blocks/create [-E | --include-entities]
    [--skip-status] <userspec>
  twblock.py blocks/destroy [-E | --include-entities]
    [--skip-status] <userspec>
  twblock.py blocks/ids [--cursor <n>] [-E | --include-entities]
    [--skip-status]
  twblock.py blocks/list [--cursor <n>] [-E | --include-entities]
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
