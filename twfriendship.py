#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to call friendships/xxx of Twitter API."

usage = """
  twfriendship.py [--version] [--help]
  twfriendship.py friendships/create [--follow] <userspec>
  twfriendship.py friendships/destroy <userspec>
  twfriendship.py friendships/incoming [--cursor <n>]
  twfriendship.py friendships/lookup [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
  twfriendship.py friendships/no_retweets/ids
  twfriendship.py friendships/outgoing [--cursor <n>]
  twfriendship.py friendships/show (-U <source_user_id> | -S <source_screen_name>)
    (-V <target_user_id> | -T <target_screen_name>)
  twfriendship.py friendships/update [--[no-]device] [--[no-]retweets]
    <userspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

from twmods import AbstractTwitterManager
from twmods import (epilog, output, request_decorator)
from twmods.commands.friendships import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.10.0'

class TwitterFriendshipManager(AbstractTwitterManager):
    """This class handles friendships/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twfriendship', make_commands(self))

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

    @request_decorator
    def request_friendships_create(self):
        """Request POST friendships/create for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name', 'follow')
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.friendships.create

    @request_decorator
    def request_friendships_destroy(self):
        """Request POST friendships/destroy for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name')
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.friendships.destroy

    def request_friendships_incoming(self):
        """Request GET friendships/incoming for Twitter."""
        self._list_ids(self.tw.friendships.incoming)

    def request_friendships_lookup(self):
        """Request GET friendships/lookup for Twitter."""
        self._request_users_csv(self.tw.friendships.lookup)

    @request_decorator
    def request_friendships_no_retweets_ids(self):
        """Request GET friendships/no_retweets/ids for Twitter."""

        return {}, self.tw.friendships.no_retweets.ids

    def request_friendships_outgoing(self):
        """Request GET friendships/outgoing for Twitter."""
        self._list_ids(self.tw.friendships.outgoing)

    @request_decorator
    def request_friendships_show(self):
        """Request GET friendships/show for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'source_user_id', 'source_screen_name',
            'target_user_id', 'target_screen_name',)}
        return kwargs, self.tw.friendships.show

    @request_decorator
    def request_friendships_update(self):
        """Request GET friendships/update for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id',
            'screen_name',
            'device',
            'retweets',) if (k in args) and (args[k] is not None)}

        return kwargs, self.tw.friendships.update

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterFriendshipManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
