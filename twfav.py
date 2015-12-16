#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to call favorites/xxx of Twitter API."

usage = """
  twfav.py [--version] [--help]
  twfav.py favorites/create [-E | --include-entities] <status_id>
  twfav.py favorites/destroy [-E | --include-entities] <status_id>
  twfav.py favorites/list [-c | --count <n>] [--since-id <status_id>]
    [--max-id <status_id>] [-E | --include-entities] <userspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

from twmods import AbstractTwitterManager
from twmods import (epilog, output, request_decorator)
from twmods.commands.favorites import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.0'

class TwitterFavoriteManager(AbstractTwitterManager):
    """This class handles favorites/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twfav', make_commands(self))

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
    def request_favorites_create(self):
        """Request POST favorites/create for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            '_id', 'include_entities',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.favorites.create

    @request_decorator
    def request_favorites_destroy(self):
        """Request POST favorites/destroy for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            '_id', 'include_entities',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.favorites.destroy

    @request_decorator
    def request_favorites_list(self):
        """Request GET favorites/list for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',
            'count', 'since_id', 'max_id', 'include_entities',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.favorites.list

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterFavoriteManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
