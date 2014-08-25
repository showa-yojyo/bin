#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script manages your own Twitter lists.

Examples:
  You can add users to a list by the "add" command::

    $ python listmanager.py add your_screen_name your_list_name user1 [user2 ...]

  Likewise, you can also remove users by the "remove" command.
"""

from secret import twitter_instance
from argparse import ArgumentParser

__version__ = '1.0.0'

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='Twitter List Manager')
    parser.add_argument('--version', action='version', version=__version__)

    # Positional arguments
    parser.add_argument(
        'command',
        choices=['add', 'remove',],
        help='Either "add" or "remove".')

    parser.add_argument(
        'owner_screen_name',
        help='The screen name of the user who owns the list being requested by a slug.')

    parser.add_argument(
        'slug',
        help='The slug of the list.')

    parser.add_argument(
        'screen_names',
        nargs='+',
        help='A comma separated list of screen names, up to 100 are allowed in a single request.')

    return parser

def main(args):
    """The main function.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """

    tw = twitter_instance()

    # Few commands are available so far.
    if args.command == 'add':
        tw.lists.members.create_all(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug,
            screen_name=','.join(args.screen_names))
    elif args.command == 'remove':
        tw.lists.members.destroy_all(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug,
            screen_name=','.join(args.screen_names))

if __name__ == '__main__':
    parser = configure()
    main(parser.parse_args())
