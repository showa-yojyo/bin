#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""twfollower.py: A utility script to manage friends and followers
of a specified Twitter user.

Usage:
  twfollower.py [--version] [--help]
  twfollower.py followers-ids [-c | --count <n>] [--cursor <n>]
    <userspec>
  twfollower.py followers-list [--cursor <n>] <userspec>
  twfollower.py friends-ids [-c | --count <n>] [--cursor <n>]
    <userspec>
  twfollower.py friends-list [--cursor <n>] <userspec>
  twfollower.py friendships-incoming [--cursor <n>]
  twfollower.py friendships-lookup [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
  twfollower.py friendships-no_retweets-ids
  twfollower.py friendships-outgoing [--cursor <n>]
  twfollower.py friendships-show <source_screen_name>
    <target_screen_name>
  twfollower.py friendships-update [--[no-]device] [--[no-]retweets]
    <userspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

from twitter import TwitterHTTPError
from twmods import AbstractTwitterManager
from twmods import output
from twmods.commands.followers import make_commands
from argparse import ArgumentParser
from itertools import count
import time

__version__ = '1.9.4'

class TwitterFollowerManager(AbstractTwitterManager):
    """This class handles commands about a Twitter followers."""

    def __init__(self):
        super().__init__('twfollower', make_commands(self))

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
        self._request_users_csv(self.tw.friendships.lookup)

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

        output(response['relationship'])

    def request_friendships_update(self):
        """Request GET friendships/update for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id',
            'screen_name',
            'device',
            'retweets',) if (k in args) and (args[k] is not None)}

        self.logger.info('update parameters {}'.format(kwargs))
        response = self.tw.friendships.update(**kwargs)
        output(response['relationship'])

    def _list_ids(self, request):
        """Print user IDs.

        Args:
            request: A PTT request method for Twitter API.
        """

        logger, args = self.logger, vars(self.args)

        kwargs = dict(
            cursor=-1,
            stringify_ids=True,)
        kwargs.update(
            {k:args[k] for k in (
                'user_id',
                'screen_name',
                'count',
                'cursor',) if (k in args) and (args[k] is not None)})
        logger.info('_list_ids arg: {}'.format(kwargs))

        while kwargs['cursor'] != 0:
            response = request(**kwargs)
            print('\n'.join(response['ids']))
            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))
            kwargs['cursor'] = next_cursor

    def _list_common(self, request):
        """The common procedure of friends/list and followers/list.

        Args:
            request: A PTT request method for Twitter API.
        """

        logger, args = self.logger, vars(self.args)

        kwargs = dict(
            cursor=-1,
            skip_status=True,
            include_user_entities=False,)
        kwargs.update(
            {k:args[k] for k in (
                'user_id',
                'screen_name',
                'count',
                'cursor',) if (k in args) and (args[k] is not None)})

        results = []
        try:
            while kwargs['cursor'] != 0:
                response = request(**kwargs)
                results.extend(response['users'])
                next_cursor = response['next_cursor']
                logger.info('next_cursor: {}'.format(next_cursor))
                kwargs['cursor'] = next_cursor
        except TwitterHTTPError as e:
            logger.info('{}'.format(e))
            #raise

        output(results)

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