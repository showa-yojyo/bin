#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manage a Twitter list.

Usage:
  listmanager.py [--version] [--help]
  listmanager.py statuses [-c | --count <n>]
    [-M | --max-id <status-id>] [-N | --max-count <n>]
    <listspec>
  listmanager.py add <listspec>
    [-f | --file <filepath>] <screen-name>...
  listmanager.py remove <listspec>
    [-f | --file <filepath>] <screen-name>...
  listmanager.py show [-c | --count <n>] <listspec>
  listmanager.py subscribe <listspec>
  listmanager.py unsubscribe <listspec>
  listmanager.py subscribers [-c | --count <n>] <listspec>
  listmanager.py memberships [-c | --count <n>] <userspec>
  listmanager.py ownerships [-c | --count <n>] <userspec>
  listmanager.py subscriptions [-c | --count <n>] <userspec>
  listmanager.py create [-m | --mode <public | private>]
    [-d | --description <DESC>] <name>
  listmanager.py describe <listspec>
  listmanager.py update [-m | --mode <public | private>]
    [-d | --desccription <DESC>] [--name <NAME>] <listspec>
  listmanager.py destroy <listspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
  <listspec> ::= (-l | --list-id <list_id>)
               | (-s | --slug <slug>)
                 ((-I | --owner-id <owner_id>) 
                | (-S | --owner-screen-name <owner_screen_name>))
"""

from common_twitter import AbstractTwitterManager
from common_twitter import SEP
from common_twitter import USER_COLUMN_HEADER
from common_twitter import format_list
from common_twitter import format_user
from common_twitter import get_list_csv_format
from common_twitter import get_user_csv_format
from listcommands import make_commands
from argparse import ArgumentParser
from itertools import count
from itertools import islice
from pprint import pprint
import time

__version__ = '1.8.1'

class TwitterListManager(AbstractTwitterManager):
    """This class handles commands about a Twitter list."""

    def __init__(self):
        super().__init__('listmanager', make_commands(self))

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

        csv_header = (
            'created_at',
            'user[screen_name]',
            'user[name]',
            #'source',
            'favorited',
            'retweet_count',
            'text',)
        csv_format = SEP.join(('{' + i + '}' for i in csv_header))

        # Print CSV header.
        print(SEP.join(csv_header))

        total_statuses = 0

        pcount = args.count
        max_count = args.max_count
        if max_count < pcount:
            max_count = pcount

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

            for j in response:
                line = csv_format.format(**j)
                print(line.replace('\r', '').replace('\n', '\\n'))

            logger.info("[{:03d}] min_id={} Fetched.".format(i, min_id))

            if max_count <= total_statuses:
                logger.info("mcount={} max_count={} total_statuses={}".format(
                    mcount, max_count, total_statuses))
                break

            kwargs['max_id'] = min_id - 1

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

        print(get_list_csv_format())
        print(format_list(self.tw.lists.show(**kwargs)))

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

        pprint(self.tw.lists.update(**kwargs))
        logger.info("List is updated.")

    def request_lists_destroy(self):
        """Delete the specified list."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',)
                if (k in args) and (args[k] is not None)}
        pprint(self.tw.lists.destroy(**kwargs))
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

        csv_header = USER_COLUMN_HEADER + ('status[text]', 'status[source]',)
        csv_format = SEP.join(('{' + i + '}' for i in csv_header))
        print(SEP.join(csv_header))

        next_cursor = -1
        while next_cursor != 0:
            # Request.
            response = request(
                skip_status=False,
                cursor=next_cursor,
                **kwargs)

            for user in response['users']:
                if 'status' in user:
                    line = csv_format.format(**user)
                    print(line.replace('\r', '').replace('\n', '\\n'))

            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

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

        print(get_list_csv_format())

        next_cursor = -1
        while next_cursor != 0:
            response = request(
                cursor=next_cursor,
                **kwargs)

            for i in response['lists']:
                print(format_list(i))

            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

    def _manage_subscription(self, request):
        """Subscribe or unsubscribe."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'list_id', 'slug',
            'owner_id', 'owner_screen_name',)
                if (k in args) and (args[k] is not None)}

        response = request(**kwargs)
        pprint(response)
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
