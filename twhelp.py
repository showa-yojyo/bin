#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import ArgumentParser
from secret import twitter_instance
from twmods import EPILOG
from twmods import output

DESCRIPTION = "Demonstrate Twitter's GET help/xxx endpoints."

USAGE = """
  twhelp.py [--version] [--help]
  twhelp.py configuration | languages | privacy | tos
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

    return root_parser

def request_decorator(request):
    """Decorate a function that returns an endpoint."""
    def request_wrapper():
        """Output the response received from Twitter."""
        output(request(twitter_instance())())
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

def main(args=None):
    """The main function."""

    parser = configure()
    args = parser.parse_args(args)

    if not 'func' in args:
        parser.print_help()
        return

    args.func()

if __name__ == '__main__':
    main()
