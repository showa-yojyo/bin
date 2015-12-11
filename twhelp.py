#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "Demonstrate Twitter's GET help/xxx endpoints."

usage = """
  twhelp.py [--version] [--help]
  twhelp.py configuration | languages | privacy | tos
"""

from argparse import ArgumentParser
from secret import twitter_instance
from twmods import epilog
from twmods import output

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

    COMMANDS = (
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
    for cmd in COMMANDS:
        parser = subparsers.add_parser(
            cmd['command'],
            aliases=cmd['aliases'],
            help=cmd['help'])
        parser.set_defaults(func=cmd['func'])

    return root_parser

def request_decorator(request):
    def request_wrapper():
        output(request(twitter_instance())())
    return request_wrapper

@request_decorator
def request_help_configuration(tw):
    return tw.help.configuration

@request_decorator
def request_help_languages(tw):
    return tw.help.languages

@request_decorator
def request_help_privacy(tw):
    return tw.help.privacy

@request_decorator
def request_help_tos(tw):
    return tw.help.tos

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
