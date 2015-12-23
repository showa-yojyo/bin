#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to manage Twitter statuses."

usage = """
  twstatus.py [--version] [--help]
  twstatus.py statuses/mentions_timeline [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>] [--trim-user]
    [--contributor-details] [-E | --include-entities]
  twstatus.py statuses/user_timeline [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>] [--trim-user]
    [-X | --exclude-replies] [--contributor-details] [--include-rts]
    <userspec>
  twstatus.py statuses/home_timeline [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>] [--trim-user]
    [-X | --exclude-replies] [--contributor-details] [--include-rts]
  twstatus.py statuses/retweets_of_me [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>] [--trim-user]
    [-E | --include-entities] [--include-user-entities]
  twstatus.py statuses/retweets/:id [-c | --count <n>]
    [--trim-user] <status_id>
  twstatus.py statuses/show/:id [--trim-user] [--include-my-retweet]
    [-E | --include-entities] <status_id>
  twstatus.py statuses/destroy/:id [--trim-user] <status_id>
  twstatus.py statuses/update [--in-reply-to-status-id <status_id>]
    [--possibly-sensitive] [--lat <Y>] [--long <X>]
    [--place-id <place>] [--display-coordinates] [--trim-user]
    [--media-ids <media_id>] <text>
  twstatus.py statuses/retweet/:id  [--trim-user] <status_id>

  twstatus.py statuses/oembed [--max-width <n>] [--hide-media]
    [--hide-thread] [--omit-script] [--omit-script]
    [--align {none,center,left,right}] [--related <csv-of-screen-names>]
    [--lang <lang>] [--widget-type {video}] [--hide-tweet]
    <status_id | url>
  twstatus.py statuses/retweeters/ids [--cursor <n>] [--stringify-ids]
    <status_id>
  twstatus.py statuses/lookup [-E | --include-entities] [--trim-user]
    [--map] <csv_of_status_ids>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

from twmods import AbstractTwitterManager
from twmods import epilog
from twmods import output
from twmods.commands.statuses import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.2'

class TwitterStatusManager(AbstractTwitterManager):
    """This class handles commands about Twitter statuses."""

    def __init__(self):
        super().__init__('twstatus', make_commands(self))

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the command line
            parameters.
        """

        parser = ArgumentParser(
            description=description, epilog=epilog, usage=usage)
        parser.add_argument(
            '--version',
            action='version',
            version=__version__)
        return parser

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterStatusManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
