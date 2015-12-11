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
__version__ = '1.0.1'

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

    def request_statuses_mentions_timeline(self):
        """Request GET statuses/mentions_timeline for Twitter."""

        request = self.tw.statuses.mentions_timeline
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            'count', 'since_id', 'max_id',
            'trim_user', 'contributor_details', 'include_entities',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_user_timeline(self):
        """Request GET statuses/user_timeline for Twitter."""

        request = self.tw.statuses.user_timeline
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',
            'count', 'since_id', 'max_id',
            'trim_user', 'exclude_replies', 'contributor_details',
            'include_rts',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_home_timeline(self):
        """Request GET statuses/home_timeline for Twitter."""

        request = self.tw.statuses.home_timeline
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            'count', 'since_id', 'max_id',
            'trim_user', 'exclude_replies', 'contributor_details',
            'include_rts',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_retweets_of_me(self):
        """Request GET statuses/retweets_of_me for Twitter."""

        request = self.tw.statuses.retweets_of_me
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            'count', 'since_id', 'max_id',
            'trim_user', 'include_entities', 'include_user_entities',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_retweets_id(self):
        """Request GET statuses/retweets/:id for Twitter."""

        request = self.tw.statuses.retweets
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            '_id', 'count', 'trim_user',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_show_id(self):
        """Request GET statuses/show/:id for Twitter."""

        request = self.tw.statuses.show
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            '_id', 'trim_user', 'include_my_retweet', 'include_entities',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_destroy_id(self):
        """Request POST statuses/destroy/:id for Twitter."""

        request = self.tw.statuses.destroy # !?
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            '_id', 'trim_user',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_update(self):
        """Request POST statuses/update for Twitter."""

        request = self.tw.statuses.update
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            'status', 'in_reply_to_status_id',
            'possibly_sensitive', 'lat', 'long',
            'place_id', 'display_coordinates',
            'trim_user', 'media_ids',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_retweet_id(self):
        """Request POST statuses/retweet/:id for Twitter."""

        request = self.tw.statuses.retweet # !?
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            '_id', 'trim_user',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_update_with_media(self):
        """Request POST statuses/update_with_media for Twitter."""

        # deprecated
        raise NotImplementedError()

    def request_statuses_oembed(self):
        """Request GET statuses/oembed for Twitter."""

        request = self.tw.statuses.oembed
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            '_id', 'url',
            'maxwidth', 'hide_media', 'hide_thread', 'omit_script',
            'align', 'related', 'lang', 'widget_type', 'hide_tweet',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_retweeters_ids(self):
        """Request GET statuses/retweeters/ids for Twitter."""

        request = self.tw.statuses.retweeters_ids
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            '_id', 'cursor', 'stringify_ids',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_statuses_lookup(self):
        """Request GET statuses/lookup for Twitter."""

        request = self.tw.statuses.lookup
        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            '_id', 'trim_user', 'include_entities', 'map',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

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
