# -*- coding: utf-8 -*-
"""common_twitter.py: A modules commonly imported by Twitter-related scripts.
"""

from secret import twitter_instance
from abc import ABCMeta
from abc import abstractmethod
from twitter import TwitterHTTPError
import logging
import sys

__version__ = '1.4.1'

SEP = '\t'

USER_COLUMN_HEADER = (
    'id',
    'screen_name',
    'name',
    'protected',
    'lang',
    'location',
    'created_at',
    'friends_count',
    'followers_count',
    'description',
    'url',)

def get_user_csv_format(delim=SEP):
    """Return the format string for user csv lines.

    Args:
        delim: A character for CSV delimiter. Default to TAB'.
        use_status: True if JSON data returned by Twitter have `status` attribute.

    Returns:
        A tab-separated value string.
    """
    return delim.join(USER_COLUMN_HEADER)

USER_CSV_FORMAT = SEP.join(('{' + i + '}' for i in USER_COLUMN_HEADER))

def format_user(user):
    """Return a string that shows user information.

    Args:
        user: An instance of the Twitter API user response object.

    Returns:
        A tab-separated value string.
    """
    return USER_CSV_FORMAT.format(**user).replace('\r', '').replace('\n', '\\n')

TWEET_COLUMN_HEADER = (
    'id',
    'created_at',
    'text',
    'favorite_count',
    'retweet_count',)

def get_tweet_csv_format(delim=SEP):
    """Return the format string for tweet csv lines.

    Args:
        delim: A character for CSV delimiter.

    Returns:
        A tab-separated value string.
    """
    return delim.join(TWEET_COLUMN_HEADER)

TWEET_CSV_FORMAT = SEP.join(('{' + i + '}' for i in TWEET_COLUMN_HEADER))

def format_tweet(tweet):
    """Return a string that shows tweet information.

    Args:
        tweet: An instance of the Twitter API twitter response object.

    Returns:
        A tab-separated value string.
    """
    return TWEET_CSV_FORMAT.format(**tweet).replace('\r', '').replace('\n', '\\n')

LIST_COLUMN_HEADER = (
    'id',
    'slug',
    'full_name',
    'created_at',
    'mode',
    'member_count',
    'subscriber_count',
    'description',)

def get_list_csv_format(delim=SEP):
    """Return the format string for tweet csv lines.

    Args:
        delim: A character for CSV delimiter.

    Returns:
        A tab-separated value string.
    """

    return delim.join(LIST_COLUMN_HEADER)

LIST_CSV_FORMAT = SEP.join(('{' + i + '}' for i in LIST_COLUMN_HEADER))

def format_list(list):
    return LIST_CSV_FORMAT.format(**list).replace('\r', '').replace('\n', '\\n')

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
