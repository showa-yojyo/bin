#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to call mutes/xxx of Twitter API."

usage = """
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

from twmods import AbstractTwitterManager
from twmods import (epilog, output, request_decorator)
from twmods.commands.mutes import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.0'

class TwitterMuteManager(AbstractTwitterManager):
    """This class handles mutes/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twmute', make_commands(self))

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the command line
            parameters.
        """

        parser = ArgumentParser(
            description=description, epilog=epilog, usage=usage)
        parser.add_argument(
            '--version',
            action='version',
            version=__version__)
        return parser

    @request_decorator
    def request_mutes_users_create(self):
        """Request POST mutes/users/create for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.mutes.users.create

    @request_decorator
    def request_mutes_users_destroy(self):
        """Request POST mutes/users/destroy for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.mutes.users.destroy

    @request_decorator
    def request_mutes_users_ids(self):
        """Request GET mutes/users/ids for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in ('cursor')
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.mutes.users.ids

    @request_decorator
    def request_mutes_users_list(self):
        """Request GET mutes/users/list for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'cursor', 'include_entities', 'skip_status',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.mutes.users.list

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterMuteManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
