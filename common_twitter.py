# -*- coding: utf-8 -*-
"""common_twitter.py: A modules commonly imported by Twitter-related scripts.
"""
import logging
import sys

__version__ = '1.3.0'

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
