#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
from twmods.commands.friendships import make_commands

DESCRIPTION = "A utility script to call friendships/xxx of Twitter API."

USAGE = """
  twfriendship.py [--version] [--help]
  twfriendship.py friendships/create [--follow] <userspec>
  twfriendship.py friendships/destroy <userspec>
  twfriendship.py friendships/incoming [--cursor <n>]
  twfriendship.py friendships/lookup [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
  twfriendship.py friendships/no_retweets/ids
  twfriendship.py friendships/outgoing [--cursor <n>]
  twfriendship.py friendships/show (-U <source_user_id> | -S <source_screen_name>)
    (-V <target_user_id> | -T <target_screen_name>)
  twfriendship.py friendships/update [--[no-]device] [--[no-]retweets]
    <userspec>

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
