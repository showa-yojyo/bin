# -*- coding: utf-8 -*-
"""__init__.py
"""

from secret import twitter_instance
from abc import ABCMeta
from abc import abstractmethod
from argparse import ArgumentParser
from json import dump
from twitter import TwitterHTTPError
import logging
import sys

__version__ = '1.5.0'

def make_logger(name=None):
    """Set up a logger with the specified name.

    Args:
        name: The logger object's name.

    Returns:
        A logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

class AbstractTwitterCommand(metaclass=ABCMeta):
    """Prototype"""

    def __init__(self, manager):
        """Prototype"""
        self.manager = manager

    @abstractmethod
    def create_parser(self, subparsers): pass

    @abstractmethod
    def __call__(self): pass

class AbstractTwitterManager(metaclass=ABCMeta):
    """This class is the base class of managers of requests for Twitter.

    The AbstractTwitterManager class is the abstract base class of
    managers that are used in utility scripts.
    """

    def __init__(self, name, commands=list()):
        """Create a new manager with the given name.

        Args:
            name: The name of manager, e.g. `listmanager`.
            commands: A list which contains command objects.
        """

        self.tw = None
        self.logger = make_logger(name)
        self.args = None
        self.commands = commands

    def setup(self, command_line=None):
        """Setup this instance.

        Args:
            command_line: Raw command line arguments.
        """

        root_parser = self.make_parser()

        # Subcommands
        subparsers = root_parser.add_subparsers(help='commands')

        for cmd in self.commands:
            cmd_parser = cmd.create_parser(subparsers)
            cmd_parser.set_defaults(func=cmd)

        self.args = root_parser.parse_args(command_line)

    @abstractmethod
    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that stores the command line
            parameters.
        """
        pass

    def execute(self):
        """Execute the specified command."""

        if not self.tw:
            self.tw = twitter_instance()

        try:
            self.args.func()
        except TwitterHTTPError as e:
            self.logger.error('{}'.format(e))
            raise

# parsers

def _parser_single_user():
    """An argument for user_id or screen_name."""

    parser = None
    def inner():
        nonlocal parser
        if parser:
            return parser

        parser = ArgumentParser(add_help=False)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '-U', '--user-id',
            nargs='?',
            dest='user_id',
            help='the ID of the user for whom to return results')
        group.add_argument(
            '-S', '--screen-name',
            nargs='?',
            dest='screen_name',
            help='the screen name of the user for whom to return results')
        return parser
    return inner

parser_user_single = _parser_single_user()

def output(data, fp=sys.stdout):
    """Output statuses, users, etc. to fp as JSON formatted data."""
    dump(data, fp, ensure_ascii=False, indent=4)
    fp.write("\n")
