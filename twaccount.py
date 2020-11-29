#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from twmods import (make_manager, EPILOG)
from twmods.commands.account import make_commands

DESCRIPTION = "A utility script to call accounts/xxx of Twitter API."

USAGE = """
  twaccount.py [--version] [--help]
  twaccount.py account/remove_profile_banner
  twaccount.py account/settings_g
  twaccount.py account/settings_p [--sleep-time-enabled]
    [--start-sleep-time <HH>] [--end-sleep-time <HH>]
    [--time-zone <TZ>] [--trend-location-woeid <woeid>]
    [--allow-contributor-request {none,all,following}]
    [--lang <language>]
  twaccount.py account/update_delivery_device
    [-E | --include-entities] {ms,none}
  twaccount.py account/update_profile [--name <text>]
    [--url <URL>] [--location <text>] [--description <text>]
    [--profile-link-color <hex>] [-E | --include-entities]
    [--skip-status]
  twaccount.py account/update_profile_background_image [--tile]
    [-E | --include-entities] [--skip-status] <imagespec>
  twaccount.py account/update_profile_banner [-w | --width <n>]
    [-H | --height <n>] [-L | --offset-left <n>]
    [-T | --offset-top <n>] [-E | --include-entities]
    [--skip-status] <path>
  twaccount.py account/update_profile_image
    [-E | --include-entities] [--skip-status] <path>
  twaccount.py account/verify_credentials

where
  <imagespec> ::= (-I | --image <path>)
                | (-M | --media-id <media_id>)
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.1.0'

MANAGER = make_manager(make_commands, globals())(__file__)

if __name__ == '__main__':
    MANAGER.main()
