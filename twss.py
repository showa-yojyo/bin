#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
from twmods.commands.saved_searches import make_commands

DESCRIPTION = "A utility script to call saved_searches/xxx of Twitter API."

USAGE = """
  twss.py [--version] [--help]
  twss.py saved_searches/create <query>
  twss.py saved_searches/destroy/:id <id>
  twss.py saved_searches/list
  twss.py saved_searches/show/:id <id>
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.1.0'

MANAGER = make_manager(make_commands, globals())(__file__)

if __name__ == '__main__':
    MANAGER.main()
