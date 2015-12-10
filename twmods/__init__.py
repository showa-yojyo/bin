# -*- coding: utf-8 -*-
"""__init__.py
"""

from secret import twitter_instance
from abc import ABCMeta
from abc import abstractmethod
from argparse import ArgumentParser
from argparse import FileType
from json import dump
from twitter import TwitterHTTPError
import logging
import sys

__version__ = '1.7.2'

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

    # Helper methods

    def _request_users_csv(self, request, up_to=100, **kwargs):
        """Common method to the following requests:

        * GET users/lookup
        * GET friendships/lookup
        * POST lists/members/create_all
        * POST lists/members/destroy_all
        """

        logger, args = self.logger, self.args
        logger.info('{} args: {}'.format(request.__name__, args))

        # Obtain the target users.
        # user_id
        user_ids = []
        if args.user_id:
            user_ids.extend(args.user_id)
        if args.file_user_id:
            user_ids.extend(line.rstrip() for line in args.file_user_id)

        # TODO: lists/xxx never get results.
        results = []

        if user_ids:
            for i in count(0, up_to):
                csv = ','.join(islice(user_ids, i, i + up_to))
                if not csv:
                    break

                logger.info("[{:04d}]-[{:04d}] Waiting...".format(i, i + up_to))
                response = request(user_id=csv, **kwargs)
                results.extend(response)
                logger.info("[{:04d}]-[{:04d}] Processed: {}".format(i, i + up_to, csv))
                time.sleep(2)

        # screen_name
        screen_names = []
        if args.screen_name:
            screen_names.extend(args.screen_name)
        if args.file_screen_name:
            screen_names.extend(line.rstrip() for line in args.file_screen_name)

        if screen_names:
            for i in count(0, up_to):
                csv = ','.join(islice(screen_names, i, i + up_to))
                if not csv:
                    break

                logger.info("[{:04d}]-[{:04d}] Waiting...".format(i, i + up_to))
                response = request(screen_name=csv, **kwargs)
                results.extend(response)

                logger.info("[{:04d}]-[{:04d}] Processed: {}".format(i, i + up_to, csv))
                time.sleep(2)

        output(results)

def cache(func):
    instance = None
    def inner():
        nonlocal instance
        if instance:
            return instance

        instance = func()
        return instance
    return inner

# parsers

@cache
def parser_user_single():
    """Return the parent parser object for --user-id and
    --screen_name arguments.
    """

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

@cache
def parser_user_multiple():
    """Return the parent parser object for --user-id and
    --screen_name arguments.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-U', '--user-id',
        nargs='*',
        dest='user_id',
        help='the ID of the user for whom to return results')
    parser.add_argument(
        '-S', '--screen-name',
        nargs='*',
        dest='screen_name',
        help='the screen name of the user for whom to return results')
    parser.add_argument(
        '-UF', '--file-user-id',
        type=FileType('r'),
        default=None,
        dest='file_user_id',
        help='a file which lists user IDs')
    parser.add_argument(
        '-SF', '--file-screen-name',
        type=FileType('r'),
        default=None,
        dest='file_screen_name',
        help='a file which lists screen names')
    return parser

@cache
def parser_count_users_many():
    """Return the parent parser object for --count optional argument.

    The following subcommands use this parser:

    * friends/ids
    * followers/ids
    * lists/members
    * lists/subscribers
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        choices=range(1, 5001),
        metavar='{1..5000}',
        help='the number of users to return per page')
    return parser

@cache
def parser_cursor():
    """Return the parent parser object for --cursor optional
    argument.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--cursor',
        type=int,
        nargs='?',
        help='break the results into pages')
    return parser

@cache
def parser_include_entities():
    """Return the parent parser object for --include-entities
    optional argument.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-E', '--include-entities',
        action='store_true',
        dest='include_entities',
        help='include entity nodes in tweet objects')
    return parser

def output(data, fp=sys.stdout):
    """Output statuses, users, etc. to fp as JSON formatted data."""
    dump(data, fp, ensure_ascii=False, indent=4)
    fp.write("\n")
