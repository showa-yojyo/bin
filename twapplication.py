#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser
import sys
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
__version__ = '1.0.2'

def parse_args(args):
    """Parse the command line parameters."""

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

    return root_parser.parse_args(args=args or ('--help',))

def run(args, stdout=sys.stdout, stderr=sys.stderr):
    """The main function."""

    twhandler = twitter_instance()

    # Get the current rate limits for methods belonging to the
    # specified resource families.
    response = twhandler.application.rate_limit_status(
        resources=args.resources)
    output(response, stdout)

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args)))

if __name__ == '__main__':
    main()
