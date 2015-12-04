#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manage a Twitter list.

Usage:
  twlist.py [--version] [--help]
  twlist.py statuses [-c | --count <n>]
    [-M | --max-id <status-id>] [-N | --max-count <n>]
    <listspec>
  twlist.py add <listspec>
    [-f | --file <filepath>] <screen-name>...
  twlist.py remove <listspec>
    [-f | --file <filepath>] <screen-name>...
  twlist.py show [-c | --count <n>] <listspec>
  twlist.py subscribe <listspec>
  twlist.py unsubscribe <listspec>
  twlist.py subscribers [-c | --count <n>] <listspec>
  twlist.py memberships [-c | --count <n>] <userspec>
  twlist.py ownerships [-c | --count <n>] <userspec>
  twlist.py subscriptions [-c | --count <n>] <userspec>
  twlist.py create [-m | --mode <public | private>]
    [-d | --description <DESC>] <name>
  twlist.py describe <listspec>
  twlist.py update [-m | --mode <public | private>]
    [-d | --desccription <DESC>] [--name <NAME>] <listspec>
  twlist.py destroy <listspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
  <listspec> ::= (-l | --list-id <list_id>)
               | (-s | --slug <slug>)
                 ((-I | --owner-id <owner_id>) 
                | (-S | --owner-screen-name <owner_screen_name>))
"""

from twmods import AbstractTwitterManager
from twmods import output
from twmods.commands.lists import make_commands
from argparse import ArgumentParser
from itertools import count
from itertools import islice
import sys
import time

__version__ = '1.9.0'

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

        parser = ArgumentParser(description='Twitter List Manager')
        parser.add_argument('--version', action='version', version=__version__)
        return parser

    def request_lists_statuses(self):
        """Show a timeline of tweets of the specified list."""

        request, logger, args = self.tw.lists.statuses, self.logger, vars(self.args)

        kwargs = dict(
            include_rts=False,
            include_entities=False,)
        kwargs.update({k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',
            'count', 'max_id')
                if (k in args) and (args[k] is not None)})

        total_statuses = 0

        # XXX
        pcount = args.get('count', 20)
        max_count = args.get('max_count', 20)
        if max_count < pcount:
            max_count = pcount

        results = []
        for i in count():
            logger.info("[{:03d}] Waiting...".format(i))

            # Request.
            response = request(**kwargs)
            if response:
                max_id = response[0]['id']
                min_id = response[-1]['id']
                mcount = len(response)
                total_statuses += mcount
            else:
                break

            results.extend(response)
            logger.info("[{:03d}] min_id={} Fetched.".format(i, min_id))

            if max_count <= total_statuses:
                logger.info("mcount={} max_count={} total_statuses={}".format(
                    mcount, max_count, total_statuses))
                break

            kwargs['max_id'] = min_id - 1

        output(results)

    def request_lists_members_create_alladd(self):
        """Add multiple members to a list."""
        self._manage_members(self.tw.lists.members.create_all)

    def request_lists_members_destroy_all(self):
        """Remove multiple members from a list."""
        self._manage_members(self.tw.lists.members.destroy_all)

    def request_lists_members(self):
        """List the members of the specified list."""
        self._show_users(self.tw.lists.members)

    def request_lists_subscribers(self):
        """List the subscribers of the specified list."""
        self._show_users(self.tw.lists.subscribers)

    def request_lists_subscribers_create(self):
        """Subscribe the authenticated user to the specified list."""
        self._manage_subscription(self.tw.lists.subscribers.create)

    def request_lists_unsubscribe(self):
        """Unsubscribe the authenticated user to the specified list."""
        self._manage_subscription(self.tw.lists.subscribers.destroy)

    def request_lists_memberships(self):
        """List lists the specified user has been added to."""
        self._show_lists(self.tw.lists.memberships)

    def request_lists_ownerships(self):
        """List lists owned by the specified user."""
        self._show_lists(self.tw.lists.ownerships)

    def request_lists_subscriptions(self):
        """List lists the specified user is subscribed to."""
        self._show_lists(self.tw.lists.subscriptions)

    def request_lists_create(self):
        """Create a new list for the authenticated user."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'name',
            'mode',
            'description')
                if k in args}

        self.tw.lists.create(**kwargs)
        logger.info("List is created.")

    def request_lists_show(self):
        """Show the specified list."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',)
                if (k in args) and (args[k] is not None)}

        output(self.tw.lists.show(**kwargs))

    def request_lists_update(self):
        """Update the specified list."""

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
        """Delete the specified list."""

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
        logger, args = self.logger, self.args

        # Obtain the target users.
        users = []
        users.extend(args.screen_name)
        if args.file:
            users.extend(line.rstrip() for line in args.file)

        args = var(args)
        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',)
                if (k in args) and (args[k] is not None)}

        # Note that lists can't have more than 5000 members
        # and you are limited to adding up to 100 members to a list at a time.
        up_to = 15
        for i in range(0, 5000, up_to):
            chunk = islice(users, i, i + up_to)
            csv = ','.join(chunk)
            if not csv:
                break

            logger.info("[{:04d}]-[{:04d}] Waiting...".format(i, i + up_to))

            # Request.
            request(
                screen_name=csv,
                **kwargs,)

            logger.info("[{:04d}]-[{:04d}] Processed: {}".format(i, i + up_to, csv))
            time.sleep(10)

    def _show_users(self, request):
        """Show users related tp the specified list.

        Args:
            request: Select lists.members or lists.subscribers.
        """

        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',
            'count',)
                if (k in args) and (args[k] is not None)}

        results = []
        next_cursor = -1
        while next_cursor != 0:
            # Request.
            response = request(
                skip_status=False,
                cursor=next_cursor,
                **kwargs)

            results.extend(response['users'])

            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

        output(results)

    def _show_lists(self, request):
        """Show lists related to the specified user.

        Args:
            request: Select lists.ownerships, lists.memberships, etc.
        """

        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',
            'count',)
                if (k in args) and (args[k] is not None)}

        results = []
        next_cursor = -1
        while next_cursor != 0:
            response = request(
                cursor=next_cursor,
                **kwargs)

            results.extend(response['lists'])

            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

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
