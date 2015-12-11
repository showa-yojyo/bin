#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to manage a Twitter list."

usage = """
  twlist.py [--version] [--help]
  twlist.py lists-statuses [-c | --count <n>]
    [--since-id <status_id>] [--max-id <status_id>]
    [-E | --include-entities] [--include-rts] <listspec>
  twlist.py lists-members-create_all [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
    <listspec>
  twlist.py lists-members-destroy_all [<userspec>...]
    [-UF | --file-user-id <path>] [-SF | --file-screen-name <path>]
    <listspec>
  twlist.py lists-members [-c | --count <n>] [--cursor <n>]
    [-E | --include-entities] [--skip-status] <listspec>
  twlist.py lists-subscribers [-c | --count <n>] [--cursor <n>]
    [-E | --include-entities] [--skip-status] <listspec>
  twlist.py lists-subscribers-create <listspec>
  twlist.py lists-subscribers-destroy <listspec>
  twlist.py lists-memberships [-c | --count <n>] [--cursor <n>]
    [--filter-to-owned-lists] <userspec>
  twlist.py lists-ownerships [-c | --count <n>] [--cursor <n>]
    <userspec>
  twlist.py lists-subscriptions [-c | --count <n>] [--cursor <n>]
    <userspec>
  twlist.py lists-create [-m | --mode <public | private>]
    [-d | --description <DESC>] <name>
  twlist.py lists-show <listspec>
  twlist.py lists-update [-m | --mode <public | private>]
    [-d | --desccription <DESC>] [--name <NAME>] <listspec>
  twlist.py lists-destroy <listspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
  <listspec> ::= (-l | --list-id <list_id>)
               | (-s | --slug <slug>)
                 ((-OI | --owner-id <owner_id>) 
                | (-OS | --owner-screen-name <owner_screen_name>))
"""

from twmods import AbstractTwitterManager
from twmods import epilog
from twmods import output
from twmods.commands.lists import make_commands
from twitter import TwitterHTTPError
from argparse import ArgumentParser
from itertools import count
import time

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.9.6'

class TwitterListManager(AbstractTwitterManager):
    """This class handles commands about a Twitter list."""

    def __init__(self):
        super().__init__('twlist', make_commands(self))

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

    def request_lists_statuses(self):
        """Request GET lists/statuses for Twitter."""

        request, logger, args = self.tw.lists.statuses, self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',
            'since_id', 'max_id', 'count',
            'include_rts', 'include_entities',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        output(response)

    def request_lists_members_create_all(self):
        """Request POST lists/members/create_all for Twitter."""
        self._manage_members(self.tw.lists.members.create_all)

    def request_lists_members_destroy_all(self):
        """Request POST lists/members/destroy_all for Twitter."""
        self._manage_members(self.tw.lists.members.destroy_all)

    def request_lists_members(self):
        """Request GET lists/members for Twitter."""
        self._show_users(self.tw.lists.members)

    def request_lists_subscribers(self):
        """Request GET lists/subscribers for Twitter."""
        self._show_users(self.tw.lists.subscribers)

    def request_lists_subscribers_create(self):
        """Request POST lists/subscribers_create for Twitter."""
        self._manage_subscription(self.tw.lists.subscribers.create)

    def request_lists_subscribers_destroy(self):
        """Request POST lists/subscribers/destroy for Twitter."""
        self._manage_subscription(self.tw.lists.subscribers.destroy)

    def request_lists_memberships(self):
        """Request GET lists/memberships for Twitter."""
        self._show_lists(self.tw.lists.memberships)

    def request_lists_ownerships(self):
        """Request GET lists/ownerships for Twitter."""
        self._show_lists(self.tw.lists.ownerships)

    def request_lists_subscriptions(self):
        """Request GET lists/subscriptions for Twitter."""
        self._show_lists(self.tw.lists.subscriptions)

    def request_lists_create(self):
        """Request POST lists/create for Twitter."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'name',
            'mode',
            'description')
                if k in args}

        self.tw.lists.create(**kwargs)
        logger.info("List is created.")

    def request_lists_show(self):
        """Request GET lists/show for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',)
                if (k in args) and (args[k] is not None)}

        output(self.tw.lists.show(**kwargs))

    def request_lists_update(self):
        """Request POST lists/update for Twitter."""

        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',
            'name',
            'mode',
            'description')
                if (k in args) and (args[k] is not None)}

        output(self.tw.lists.update(**kwargs))
        logger.info("List is updated.")

    def request_lists_destroy(self):
        """Request POST lists/destroy for Twitter."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',)
                if (k in args) and (args[k] is not None)}

        output(self.tw.lists.destroy(**kwargs))
        logger.info("List is deleted.")

    def _manage_members(self, request):
        """Add multiple members to a list or remove from a list.

        Args:
            request: Select lists.members.create_all or lists.members.destroy_all.
        """

        args = vars(args)
        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',)
                if (k in args) and (args[k] is not None)}

        self._request_users_csv(self, request, up_to=15, **kwargs)

    def _show_users(self, request):
        """Show users related tp the specified list.

        Args:
            request: Select lists.members or lists.subscribers.
        """

        logger, args = self.logger, vars(self.args)

        kwargs = dict(cursor=-1)
        kwargs.update({k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',
            'count', 'include_entities', 'skip_status',
            'cursor',) if (k in args) and (args[k] is not None)})

        results = []
        try:
            while kwargs['cursor']:
                response = request(**kwargs)
                results.extend(response['users'])
                next_cursor = response['next_cursor']
                logger.info('next_cursor: {}'.format(next_cursor))
                kwargs['cursor'] = next_cursor
        except TwitterHTTPError as e:
            logger.info('{}'.format(e))
            #raise

        output(results)

    def _show_lists(self, request):
        """Show lists related to the specified user.

        Args:
            request: Select lists.ownerships, lists.memberships, etc.
        """

        logger, args = self.logger, vars(self.args)

        kwargs = dict(cursor=-1)
        kwargs.update({k:args[k] for k in (
            'user_id', 'screen_name',
            'count', 'cursor',
            'filter_to_owned_lists')
                if (k in args) and (args[k] is not None)})

        results = []
        try:
            while kwargs['cursor']:
                response = request(**kwargs)
                results.extend(response['lists'])
                next_cursor = response['next_cursor']
                logger.info('next_cursor: {}'.format(next_cursor))
                kwargs['cursor'] = next_cursor
        except TwitterHTTPError as e:
            logger.info('{}'.format(e))
            #raise

        output(results)

    def _manage_subscription(self, request):
        """Subscribe or unsubscribe."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)

        output(response)
        self.logger.info("Finished to {request}".format(request=request))

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterListManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
