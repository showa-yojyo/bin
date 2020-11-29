#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser
from functools import wraps
import sys
from secret import twitter_instance
from twmods import (EPILOG, output)

DESCRIPTION = "Demonstrate Twitter's GET help/xxx endpoints."

USAGE = """
  twhelp.py [--version] [--help]
  twhelp.py configuration | languages | privacy | tos
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

    commands = (
        dict(func=request_help_configuration,
             command='help/configuration',
             aliases=['configuration', 'config'],
             help='print the current configuration used by Twitter'),
        dict(func=request_help_languages,
             command='help/languages',
             aliases=['languages', 'lang'],
             help='print the list of languages supported by Twitter'),
        dict(func=request_help_privacy,
             command='help/privacy',
             aliases=['privacy'],
             help='print Twitter\'s Privacy Policy'),
        dict(func=request_help_tos,
             command='help/tos',
             aliases=['tos'],
             help='print Twitter Terms of Service'))

    subparsers = root_parser.add_subparsers(help='commands')
    for cmd in commands:
        parser = subparsers.add_parser(
            cmd['command'],
            aliases=cmd['aliases'],
            help=cmd['help'])
        parser.set_defaults(func=cmd['func'])

    return root_parser.parse_args(args=args or ('--help',))

def request_decorator(request):
    """Decorate a function that returns an endpoint."""

    @wraps(request)
    def request_wrapper(stdout, stderr):
        """Output the response received from Twitter."""
        output(request(twitter_instance())(), stdout)
    return request_wrapper

@request_decorator
def request_help_configuration(twhandler):
    """Return the handler for GET help/configuration."""
    return twhandler.help.configuration

@request_decorator
def request_help_languages(twhandler):
    """Return the handler for GET help/languages."""
    return twhandler.help.languages

@request_decorator
def request_help_privacy(twhandler):
    """Return the handler for GET help/privacy."""
    return twhandler.help.privacy

@request_decorator
def request_help_tos(twhandler):
    """Return the handler for GET help/tos."""
    return twhandler.help.tos

def run(args, stdout=sys.stdout, stderr=sys.stderr):
    args.func(stdout, stderr)

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args)))

if __name__ == '__main__':
    main()
