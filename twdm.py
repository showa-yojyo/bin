#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to call direct_messages/xxx of Twitter API."

usage = """
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

from twmods import AbstractTwitterManager
from twmods import epilog
from twmods.commands.direct_messages import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.0'

class TwitterDirectMessageManager(AbstractTwitterManager):
    """This class handles direct_messages/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twdm', make_commands(self))

    def make_parser(self, pre_parser):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the command line
            parameters.
        """

        parser = ArgumentParser(
            parents=[pre_parser],
            description=description, epilog=epilog, usage=usage)
        parser.add_argument(
            '--version',
            action='version',
            version=__version__)
        return parser

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterDirectMessageManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
