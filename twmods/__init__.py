"""__init__.py
"""

from abc import (ABCMeta, abstractmethod)
from argparse import (ArgumentParser, FileType)
from configparser import (ConfigParser, Error)
from json import dump
import logging
from pathlib import Path
import sys

from twitter import TwitterHTTPError

from secret import twitter_instance

EPILOG = "GitHub repository: https://github.com/showa-yojyo/bin"

__version__ = '1.15.0'

def make_logger(name=None, stdlog=sys.stderr):
    """Set up a logger with the specified name.

    Args:
        name: The logger object's name.
        stdlog: stream for logging output.

    Returns:
        A logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(stdlog)
    handler.setFormatter(logging.Formatter(
        '{asctime}:{name}:{levelname}:{message}', style='{'))
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
        self.logger = None
        self.name = name
        self.args = None
        self.commands = commands or []
        self._dry_run = False

    @property
    def dry_run(self):
        """Global option dry_run."""
        return self._dry_run

    def parse_args(self, args):
        """Parse the command line parameters."""

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

        args, remaining_argv = pre_parser.parse_known_args(args)
        self._dry_run = args.dry_run

        defaults = {}
        config = ConfigParser()
        config.read(args.config if args.config else Path.home() / '.twmanagerrc')

        try:
            defaults = dict(config.items("General"))
        except Exception as ex:
            print(f'Warning: {ex}', file=sys.stderr)

        root_parser = self.make_parser(pre_parser)

        # Subcommands
        subparsers = root_parser.add_subparsers(help='commands')

        for cmd in self.commands:
            cmd_parser = cmd.create_parser(subparsers)
            cmd_parser.set_defaults(func=cmd, **defaults)

        #root_parser.set_defaults(**defaults)
        self.args = root_parser.parse_args(args=remaining_argv or ('--help',))
        return self.args

    @abstractmethod
    def make_parser(self, pre_parser):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that stores the command line
            parameters.
        """
        pass

    def execute(self, args, stdout=sys.stdout, stderr=sys.stderr):
        """Execute the specified command."""

        self.logger = make_logger(self.name, stderr)

        if not self.twhandler:
            self.twhandler = twitter_instance()

        try:
            self.args.func()
        except TwitterHTTPError as ex:
            self.logger.error('exception', exc_info=ex)
            raise

    def main(self, args=sys.argv[1:]):
        sys.exit(self.execute(self.parse_args(args)))

def make_manager(make_commands, params):
    """Return a subclass of class AbstractTwitterManager."""

    class BasicTwitterManager(AbstractTwitterManager):
        """This class handles commands about a Twitter list."""

        DESCRIPTION = params['DESCRIPTION']
        EPILOG = params['EPILOG']
        USAGE = params['USAGE']
        VERSION = params['__version__']

        def __init__(self, name):
            super().__init__(name, make_commands(self))

        def make_parser(self, pre_parser):
            """Create the command line parser."""

            parser = ArgumentParser(
                parents=[pre_parser],
                description=self.DESCRIPTION,
                epilog=self.EPILOG,
                usage=self.USAGE)
            parser.add_argument(
                '--version',
                action='version',
                version=self.VERSION)
            return parser

    return BasicTwitterManager

def output(data, fp=sys.stdout):
    """Output statuses, users, etc. to fp as JSON formatted data."""
    dump(data, fp, ensure_ascii=False, indent=4, sort_keys=True)
    fp.write("\n")
