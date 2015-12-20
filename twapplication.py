#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = """A utility script to call GET application/rate_limit_status
of Twitter API."""

usage = """
  twapplication.py [--version] [--help]
  twapplication.py <cvs-of-resource-families>
"""

from secret import twitter_instance
from twmods import (epilog, output)
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.0'

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    root_parser = ArgumentParser(
        description=description,
        epilog=epilog,
        usage=usage)
    root_parser.add_argument(
        '--version',
        action='version',
        version=__version__)
    root_parser.add_argument(
        'resources',
        help='A comma-separated list of resource families')

    return root_parser

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    parser = configure()
    args = parser.parse_args(command_line)

    tw = twitter_instance()

    # Get the current rate limits for methods belonging to the
    # specified resource families.
    response = tw.application.rate_limit_status(
        resources=args.resources)
    output(response)

if __name__ == '__main__':
    main()
