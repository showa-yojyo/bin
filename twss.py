#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to call saved_searches/xxx of Twitter API."

usage = """
  twss.py [--version] [--help]
  twss.py saved_searches/create <query>
  twss.py saved_searches/destroy/:id <id>
  twss.py saved_searches/list
  twss.py saved_searches/show/:id <id>
"""

from twmods import AbstractTwitterManager
from twmods import (epilog, output, request_decorator)
from twmods.commands.saved_searches import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.0'

class TwitterSavedSearchManager(AbstractTwitterManager):
    """This class handles saved_searches/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twss', make_commands(self))

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
    def request_saved_searches_create(self):
        """Request POST saved_searches/create for Twitter."""

        return dict(query=self.args.query), self.tw.saved_searches.create

    @request_decorator
    def request_saved_searches_destroy_id(self):
        """Request POST saved_searches/destroy/:id for Twitter."""

        return dict(_id=self.args.id), self.tw.saved_searches.destroy._id

    @request_decorator
    def request_saved_searches_list(self):
        """Request GET saved_searches/list for Twitter."""

        return {}, self.tw.saved_searches.list

    @request_decorator
    def request_saved_searches_show_id(self):
        """Request GET saved_searches/show/:id for Twitter."""

        return dict(_id=self.args.id), self.tw.saved_searches.show._id

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterSavedSearchManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
