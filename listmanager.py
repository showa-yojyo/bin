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
import itertools

__version__ = '1.1.1'

# Available subcommands.
COMMAND_LIST_ADD = 'add'
COMMAND_LIST_REMOVE = 'remove'
COMMAND_LIST_LIST = 'list'

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='Twitter List Manager')
    parser.add_argument('--version', action='version', version=__version__)

    subparsers = parser.add_subparsers(help='commands')

    parser_add = subparsers.add_parser(
        COMMAND_LIST_ADD,
        help='add multiple members to a list')

    parser_remove = subparsers.add_parser(
        COMMAND_LIST_REMOVE,
        help='remove multiple members from a list')

    parser_list = subparsers.add_parser(
        COMMAND_LIST_LIST,
        help='list the members of the specified list')

    add_common_args(parser_add)
    add_screen_names_args(parser_add)
    add_common_args(parser_remove)
    add_screen_names_args(parser_remove)
    add_common_args(parser_list)

    parser_add.set_defaults(func=execute_add)
    parser_remove.set_defaults(func=execute_remove)
    parser_list.set_defaults(func=execute_list)

    return parser

def add_common_args(parser):
    """TBW"""
    parser.add_argument(
        'owner_screen_name',
        help='the screen name of the user who owns the list being requested by a slug')

    parser.add_argument(
        'slug',
        help='the slug of the list.')

def add_screen_names_args(parser):
    """TBW"""
    parser.add_argument(
        'screen_names',
        nargs='*',
        help='a list of screen names, up to 100 are allowed in a single request')

    parser.add_argument(
        '-f', '--file',
        type=FileType('r', encoding='utf-8'),
        default=None,
        help='a file which lists screen names to be added or removed')

def manage_members(args, action):
    """Add multiple members to a list or remove from a list.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

        action: Select lists.members.create_all or lists.members.destroy_all.

    Returns:
        None.
    """

    # Obtain the target users.
    users = itertools.chain(args.screen_names, (line.rstrip() for line in args.file))

    # Note that lists can't have more than 5000 members
    # and you are limited to adding up to 100 members to a list at a time.
    up_to = 100
    for i in range(0, 5000, up_to):
        chunk = itertools.islice(users, i, i + up_to)
        csv = ','.join(chunk)
        if not csv:
            break

        action(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug,
            screen_name=csv)

def execute_add(args):
    """Add multiple members to a list.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """
    manage_members(args, args.tw.lists.members.create_all)

def execute_remove(args):
    """Remove multiple members from a list.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """
    manage_members(args, args.tw.lists.members.destroy_all)

def execute_list(args):
    """List the members of the specified list.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """

    tw = args.tw
    next_cursor = -1
    while next_cursor != 0:
        response = tw.lists.members(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug,
            cursor=next_cursor)

        for user in response['users']:
            print(format_user(user))

        next_cursor = response['next_cursor']

def format_user(user):
    """Return a string that shows user information.

    Args:
        user: An instance of the Twitter API users response object.

    Returns:
        A tab-separated value string.
    """
    return '{screen_name}\t{name}\t{description}\t{url}'.format(**user).replace('\n', ' ')

def main(args):
    """The main function.

    Args:
        args: An instance of argparse.ArgumentParser parsed in the configure
            function.

    Returns:
        None.
    """

    args.tw = twitter_instance()
    args.func(args)

if __name__ == '__main__':
    parser = configure()
    main(parser.parse_args())
