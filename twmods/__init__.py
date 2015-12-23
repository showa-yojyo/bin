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

epilog = "GitHub repository: https://github.com/showa-yojyo/bin"

__version__ = '1.11.1'

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
        if not 'func' in self.args:
            self.args.func = root_parser.print_help

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

def output(data, fp=sys.stdout):
    """Output statuses, users, etc. to fp as JSON formatted data."""
    dump(data, fp, ensure_ascii=False, indent=4, sort_keys=True)
    fp.write("\n")
