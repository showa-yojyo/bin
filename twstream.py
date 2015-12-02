#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""twstream.py: Twitter Streaming API Utility

Usage:
  twstream.py [common-options] <command> [command-options]
"""

from secret import twitter_stream
from twitter import TwitterHTTPError
from twitter.stream import Timeout, HeartbeatTimeout, Hangup
from common_twitter import AbstractTwitterManager
from twstreamcommands import make_commands
from argparse import ArgumentParser
from pprint import pprint

__version__ = '1.1.0'

class TwitterStreamManager(AbstractTwitterManager):
    """Twitter Streaming API Utility"""

    def __init__(self):
        super().__init__('twstream', make_commands(self))

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the command line
            parameters.
        """

        parser = ArgumentParser(description='Twitter Streaming API Utility')
        parser.add_argument('--version', action='version', version=__version__)

        parser.add_argument(
            '-o', '--timeout',
            default=60,
            help='timeout for the stream (seconds)')
        parser.add_argument(
            '-H', '--heartbeat',
            default=90,
            help='set heartbeat timeout (seconds)')
        parser.add_argument(
            '-b', '--block',
            action='store_true',
            default=True,
            help='set stream to blocking')

        group = parser.add_argument_group(title='Streaming API arguments')
        group.add_argument(
            '--delimited',
            metavar='length',
            help='do not use this option')
        group.add_argument(
            '--stall-warnings',
            action='store_true',
            default=False,
            dest='stall_warnings',
            help='enable periodic warning messages if the client is in danger of being disconnected')
        group.add_argument(
            '--filter-level',
            dest='filter_level',
            choices=('none', 'low', 'medium',),
            help='the minimum value of the filter level')
        group.add_argument(
            '--language',
            help='a comma-separated list of BCP 47 language identifiers')

        return parser

    def execute(self):
        """Execute the specified command."""

        try:
            self.args.func()
        except TwitterHTTPError as e:
            self.logger.error('{}'.format(e))
            raise

    def request_statuses_sample(self):
        """Request GET statuses/sample for Twitter."""

        tw = self._setup_stream()
        query_args = {k:args[k] for k in (
            'delimited', 'stall_warnings',)
                if k in args}

        g = tw.statuses.sample(**query_args)
        self._output_statuses(g)

    def request_statuses_filter(self):
        """Request POST statuses/filter for Twitter."""

        tw = self._setup_stream()
        query_args = {k:args[k] for k in (
            'follow', 'track', 'locations',
            'delimited', 'stall_warnings',)
                if k in args}

        g = tw.statuses.filter(**query_args)
        self._output_statuses(g)

    def request_user(self):
        """Request GET user for Twitter."""

        tw = self._setup_stream(domain='userstream.twitter.com')
        query_args = {k:args[k] for k in (
            'delimited', 'stall_warnings',
            'with', 'replies',
            'track', 'locations',)
                if k in args}

        for msg in tw.user(**query_args):
            if not tweet:
                continue

            if tweet in (Timeout, HeartbeatTimeout, Hangup):
                print("{}".format(tweet))
                break

            # Friends lists.
            if 'friends' in msg or 'friends_str' in msg:
                pprint(msg)
                continue

            # Direct messages.
            if 'recipient' in msg and 'sender' in msg:
                pprint(msg)
                continue

            # Events
            if 'event' in msg:
                pprint(msg)
                continue

            # Warnings
            if 'warning' in msg:
                pprint(msg)
                continue

            # Unknown
            print("Unknown {}".format(msg))

    def request_site(self):
        """Request GET site for Twitter."""

        tw = self._setup_stream(domain='sitestream.twitter.com')
        query_args = {k:args[k] for k in (
            'follow',
            'delimited', 'stall_warnings',
            'with', 'replies',)
                if k in args}

        for msg in tw.site(**query_args):
            pprint(msg)

    def request_statuses_firehose(self):
        """Request GET statuses/firehose for Twitter."""

        tw = self._setup_stream()
        query_args = {k:args[k] for k in (
            'count',
            'delimited', 'stall_warnings',)
                if k in args}

        g = tw.statuses.firehose(**query_args)
        self._output_statuses(g)

    def _setup_stream(self, **kwargs):
        """x"""

        args = vars(self.args)
        stream_args = {k:args[k] for k in (
            'timeout',
            'block',
            'heartbeat_timeout')
                if k in args}
        return twitter_stream(**kwargs, **stream_args)

    def _output_statuses(self, gen):
        """x"""

        csv_header = (
            'id',
            'created_at',
            'user[screen_name]',
            'user[name]',
            #'source',
            'text',)
        csv_format = '|'.join(('{' + i + '}' for i in csv_header))

        for tweet in gen:
            if not tweet:
                continue

            if tweet in (Timeout, HeartbeatTimeout, Hangup):
                print("{}".format(tweet))
                break

            if 'text' in tweet:
                #pprint(tweet)
                line = csv_format.format(**tweet)
                print(line.replace('\r', '').replace('\n', '\\n'))
                continue

            print("Unknown {}".format(tweet))

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterStreamManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
