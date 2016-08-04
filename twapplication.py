#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser
from twmods import (EPILOG, output)
from secret import twitter_instance

DESCRIPTION = """A utility script to call GET application/rate_limit_status
of Twitter API."""

USAGE = """
  twapplication.py [--version] [--help]
  twapplication.py <cvs-of-resource-families>
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.0.1'

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    root_parser = ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
        usage=USAGE)
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

    twhandler = twitter_instance()

    # Get the current rate limits for methods belonging to the
    # specified resource families.
    response = twhandler.application.rate_limit_status(
        resources=args.resources)
    output(response)

if __name__ == '__main__':
    main()
