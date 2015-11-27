#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""List friends or followers of a specified Twitter user.

Usage:
  followmanager.py [--version] [--help]
  followmanager.py <command> [-c | --count <n>] <screen-name>
  followmanager.py friendships-lookup
    [-f | --file <filepath>] <screen-name>...
"""

from common_twitter import AbstractTwitterManager
from common_twitter import format_user
from common_twitter import get_user_csv_format
from followercommands import make_commands
from argparse import ArgumentParser
from itertools import count
from itertools import islice
from pprint import pprint
import time

__version__ = '1.x.1'

class TwitterFollowerManager(AbstractTwitterManager):
    """This class handles commands about a Twitter followers."""

    def __init__(self):
        super().__init__('followmanager', make_commands(self))

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that stores the command line
            parameters.
        """

        parser = ArgumentParser(description='Twitter Followers Viewer')
        parser.add_argument('--version', action='version', version=__version__)
        return parser

    def request_friends_ids(self):
        """Request GET friends/ids for Twitter."""
        self._list_ids(self.tw.friends.ids)

    def request_friends_list(self):
        """Request GET friends/list for Twitter."""
        self._list_common(self.tw.friends.list)

    def request_followers_ids(self):
        """Request GET followers/ids for Twitter."""
        self._list_ids(self.tw.followers.ids)

    def request_followers_list(self):
        """Request GET followers/list for Twitter."""
        self._list_common(self.tw.followers.list)

    def request_friendships_create(self):
        """Request GET friendships/create for Twitter."""
        raise NotImplementedError()

    def request_friendships_destroy(self):
        """Request GET friendships/destroy for Twitter."""
        raise NotImplementedError()

    def request_friendships_incoming(self):
        """Request GET friendships/incoming for Twitter."""
        self._list_ids(self.tw.friendships.incoming)

    def request_friendships_lookup(self):
        """Request GET friendships/lookup for Twitter."""

        request = self.tw.friendships.lookup
        logger, args = self.logger, self.args

        # Obtain the target users.
        users = []
        users.extend(args.user_id)
        if args.file:
            users.extend(line.rstrip() for line in args.file)

        # You are limited to adding up to 100 members to a list at a time.
        up_to = 100
        for i in count(0, up_to):
            chunk = islice(users, i, i + up_to)
            csv = ','.join(chunk)
            if not csv:
                break

            logger.info("[{:04d}]-[{:04d}] Waiting...".format(i, i + up_to))
            response = request(user_id=csv)
            pprint(response)
            logger.info("[{:04d}]-[{:04d}] Processed: {}".format(i, i + up_to, csv))
            time.sleep(2)

    def request_friendships_no_retweets_ids(self):
        """Request GET friendships/no_retweets/ids for Twitter."""

        response = self.tw.friendships.no_retweets.ids(stringify_ids=True)
        print('\n'.join(response))
        self.logger.info("{} users returned".format(len(response)))

    def request_friendships_outgoing(self):
        """Request GET friendships/outgoing for Twitter."""
        self._list_ids(self.tw.friendships.outgoing)

    def request_friendships_show(self):
        """Request GET friendships/show for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'source_screen_name',
            'target_screen_name',)}
        response = self.tw.friendships.show(**kwargs)
        pprint(response['relationship'])

    def request_friendships_update(self):
        """Request GET friendships/update for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'screen_name',
            'device',
            'retweets',)}

        self.logger.info('update parameters {}'.format(kwargs))
        response = self.tw.friendships.update(**kwargs)
        pprint(response['relationship'])

    def _list_ids(self, request):
        """Print user IDs."""

        logger, args = self.logger, self.args

        kwargs = dict(stringify_ids=True)
        if 'screen_name' in args:
            kwargs['screen_name'] = args.screen_name
        if 'count' in args:
            kwargs['count'] = args.count

        next_cursor = -1
        while next_cursor != 0:
            response = request(
                cursor=next_cursor,
                **kwargs)

            print('\n'.join(response['ids']))

            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

    def _list_common(self, request):
        """The common procedure of friends/list and followers/list.

        Args:
            request: A PTT request method for Twitter API.
        """

        logger, args = self.logger, self.args

        # Print CSV header.
        print(get_user_csv_format())

        kwargs = dict(
            screen_name=args.screen_name,
            skip_status=True,
            include_user_entities=False,)
        if args.count:
            kwargs['count'] = args.count

        next_cursor = -1
        while next_cursor != 0:
            # Request.
            users = request(
                cursor=next_cursor,
                **kwargs)

            for user in users['users']:
                print(format_user(user))

            next_cursor = users['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterFollowerManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
