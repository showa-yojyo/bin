# -*- coding: utf-8 -*-
"""common_twitter.py: A modules commonly imported by Twitter-related scripts.
"""

from secret import twitter_instance
from abc import ABCMeta
from abc import abstractmethod
import logging
import sys

__version__ = '1.4.0'

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
    return USER_CSV_FORMAT.format(**user).replace('\r', '').replace('\n', ' ')

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
    return TWEET_CSV_FORMAT.format(**tweet).replace('\r', '').replace('\n', ' ')

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

    def __init__(self, name):
        """Create a new manager with the given name.

        Args:
            name: The name of manager, e.g. `listmanager`.
        """

        self.tw = None
        self.logger = make_logger(name)
        self.args = None

    def setup(self, params=None):
        """Setup this instance.

        Args:
            params: Raw command line arguments.
        """

        parser = self.make_parser()
        self.args = parser.parse_args(params)

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
        self.args.func()
