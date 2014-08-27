#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script manages your own Twitter lists.

Examples:
  You can add users to a list by the "add" command::

    $ python listmanager.py add your_screen_name your_list_name [user ...]

  Likewise, you can also remove users by the "remove" command.
"""

from secret import twitter_instance
from argparse import ArgumentParser
from argparse import FileType

__version__ = '1.0.0'

COMMAND_LIST_ADD = 'add'
COMMAND_LIST_REMOVE = 'remove'

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='Twitter List Manager')
    parser.add_argument('--version', action='version', version=__version__)

    # Positional arguments.
    parser.add_argument(
        'command',
        choices=[COMMAND_LIST_ADD, COMMAND_LIST_REMOVE,],
        help='Either "{}" or "{}".'.format(COMMAND_LIST_ADD, COMMAND_LIST_REMOVE))

    parser.add_argument(
        'owner_screen_name',
        help='The screen name of the user who owns the list being requested by a slug.')

    parser.add_argument(
        'slug',
        help='The slug of the list.')

    parser.add_argument(
        'screen_names',
        nargs='*',
        help='A list of screen names, up to 100 are allowed in a single request.')

    # Optional arguments.
    parser.add_argument(
        '-f', '--file',
        type=FileType('r', encoding='utf-8'),
        default=None,
        help='A file which lists screen names to be added or removed.')

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
    cmd = None
    if args.command == COMMAND_LIST_ADD:
        cmd = tw.lists.members.create_all
    elif args.command == COMMAND_LIST_REMOVE:
        cmd = tw.lists.members.destroy_all

    # Obtain the target users.
    users = []
    users.extend(args.screen_names)
    if args.file:
        users.extend(line.strip() for line in args.file)

    cmd(
        owner_screen_name=args.owner_screen_name,
        slug=args.slug,
        screen_name=','.join(users))

if __name__ == '__main__':
    parser = configure()
    main(parser.parse_args())
