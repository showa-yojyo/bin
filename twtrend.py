#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to call trends/xxx of Twitter API."

usage = """
  twtrend.py [--version] [--help]
  twtrend.py trends/available
  twtrend.py trends/closest <longitude> <latitude>
  twtrend.py trends/place [--exclude {hashtags}] <woeid>
"""

from twmods import AbstractTwitterManager
from twmods import (epilog, output, request_decorator)
from twmods.commands.trends import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.0'

class TwitterTrendManager(AbstractTwitterManager):
    """This class handles trends/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twtrend', make_commands(self))

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
    def request_trends_available(self):
        """Request GET trends/available for Twitter."""

        return {}, self.tw.trends.available

    @request_decorator
    def request_trends_closest(self):
        """Request GET trends/closest for Twitter."""

        request, args = self.tw.trends.closest, vars(self.args)
        kwargs = {k:args[k] for k in (
            'lat', 'long',)
                if (k in args) and (args[k] is not None)}
        return kwargs, request

    @request_decorator
    def request_trends_place(self):
        """Request GET trends/place for Twitter."""

        request, args = self.tw.trends.place, vars(self.args)
        kwargs = {k:args[k] for k in (
            '_id', 'exclude',)
                if (k in args) and (args[k] is not None)}
        return kwargs, request

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterTrendManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
