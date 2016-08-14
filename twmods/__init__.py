# -*- coding: utf-8 -*-
"""__init__.py
"""

from abc import (ABCMeta, abstractmethod)
from argparse import (ArgumentParser, FileType)
from configparser import (ConfigParser, Error)
from json import dump
import logging
from os.path import expanduser
import sys

from twitter import TwitterHTTPError

from secret import twitter_instance

EPILOG = "GitHub repository: https://github.com/showa-yojyo/bin"

__version__ = '1.13.0'

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
    formatter = logging.Formatter(
        '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

class AbstractTwitterManager(metaclass=ABCMeta):
    """This class is the base class of managers of requests for Twitter.

    The AbstractTwitterManager class is the abstract base class of
    managers that are used in utility scripts.
    """

    def __init__(self, name, commands=None):
        """Create a new manager with the given name.

        Args:
            name: The name of manager, e.g. `listmanager`.
            commands: A list which contains command objects.
        """

        self.twhandler = None
        self.logger = make_logger(name)
        self.args = None
        self.commands = commands or []
        self._dry_run = False

    @property
    def dry_run(self):
        """Global option dry_run."""
        return self._dry_run

    def setup(self, command_line=None):
        """Setup this instance.

        Args:
            command_line: Raw command line arguments.
        """

        pre_parser = ArgumentParser(add_help=False)
        pre_parser.add_argument(
            '--config',
            type=FileType(mode='r', encoding='utf-8'),
            metavar='FILE',
            help='path to config file')

        pre_parser.add_argument(
            '--dry_run',
            dest='dry_run',
            action='store_true',
            help='perform a trial run with no changes made')

        args, remaining_argv = pre_parser.parse_known_args(command_line)
        self._dry_run = args.dry_run

        defaults = {}
        config = ConfigParser()
        if args.config:
            config.read_file(args.config)
        else:
            default_config_path = expanduser('~/.twmanagerrc')
            config.read(default_config_path)

        try:
            defaults = dict(config.items("General"))
        except Error as ex:
            print('Warning: {}'.format(ex), file=sys.stderr)

        root_parser = self.make_parser(pre_parser)

        # Subcommands
        subparsers = root_parser.add_subparsers(help='commands')

        for cmd in self.commands:
            cmd_parser = cmd.create_parser(subparsers)
            cmd_parser.set_defaults(func=cmd, **defaults)

        #root_parser.set_defaults(**defaults)
        self.args = root_parser.parse_args(remaining_argv)

        if not 'func' in self.args:
            self.args.func = root_parser.print_help

    @abstractmethod
    def make_parser(self, pre_parser):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that stores the command line
            parameters.
        """
        pass

    def execute(self):
        """Execute the specified command."""

        if not self.twhandler:
            self.twhandler = twitter_instance()

        try:
            self.args.func()
        except TwitterHTTPError as ex:
            self.logger.error('{}'.format(ex))
            raise

def output(data, fp=sys.stdout):
    """Output statuses, users, etc. to fp as JSON formatted data."""
    dump(data, fp, ensure_ascii=False, indent=4, sort_keys=True)
    fp.write("\n")
