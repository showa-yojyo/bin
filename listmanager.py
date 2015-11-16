#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manage multiple users in a specified Twitter list.

Usage:
  listmanager.py [--version] [--help]
  listmanager.py add <owner-screen-name> <slug>
    [-f | --file <filepath>] <screen-name>...
  listmanager.py remove <owner-screen-name> <slug>
    [-f | --file <filepath>] <screen-name>...
  listmanager.py show <owner-screen-name> <slug>
"""

from secret import twitter_instance
from common_twitter import format_user
from common_twitter import get_user_csv_format
from common_twitter import make_logger
from argparse import ArgumentParser
from argparse import FileType
import itertools
import sys
import time

__version__ = '1.2.0'

# Available subcommands.
COMMAND_LIST_ADD = 'add'
COMMAND_LIST_REMOVE = 'remove'
COMMAND_LIST_SHOW = 'show'

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
        COMMAND_LIST_SHOW,
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
    logger = make_logger('listmanager')

    # Obtain the target users.
    users = []
    users.extend(args.screen_names)
    if args.file:
        users.extend(line.rstrip() for line in args.file)

    # Note that lists can't have more than 5000 members
    # and you are limited to adding up to 100 members to a list at a time.
    up_to = 15
    for i in range(0, 5000, up_to):
        chunk = itertools.islice(users, i, i + up_to)
        csv = ','.join(chunk)
        if not csv:
            break

        if i != 0:
            time.sleep(15)

        logger.info("[{:05d}]-[{:05d}] Waiting...".format(i, i + up_to))

        action(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug,
            screen_name=csv)

        logger.info("[{:05d}]-[{:05d}] Fetched: {}".format(i, i + up_to, csv))

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

    logger = make_logger('listmanager')

    tw = args.tw
    next_cursor = -1

    print(get_user_csv_format())

    while next_cursor != 0:
        response = tw.lists.members(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug,
            cursor=next_cursor)

        for user in response['users']:
            print(format_user(user))

        next_cursor = response['next_cursor']
        logger.info('next_cursor: {}'.format(next_cursor))

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
