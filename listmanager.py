#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manage a Twitter list.

Usage:
  listmanager.py [--version] [--help]
  listmanager.py statuses [-c | --count <n>]
    [-M | --max-id <status-id>] [-N | --max-count <n>]
    <owner-screen-name> <slug>
  listmanager.py add <owner-screen-name> <slug>
    [-f | --file <filepath>] <screen-name>...
  listmanager.py remove <owner-screen-name> <slug>
    [-f | --file <filepath>] <screen-name>...
  listmanager.py show [-c | --count <n>] <owner-screen-name> <slug>
  listmanager.py subscribe <owner-screen-name> <slug>
  listmanager.py unsubscribe <owner-screen-name> <slug>
  listmanager.py subscribers [-c | --count <n>] <owner-screen-name> <slug>
  listmanager.py memberships [-c | --count <n>] <screen-name>
  listmanager.py ownerships [-c | --count <n>] <screen-name>
  listmanager.py subscriptions [-c | --count <n>] <screen-name>
  listmanager.py create [-m | --mode <public | private>]
    [-d | --desc <DESC>] <name>
  listmanager.py describe <owner-screen-name> <slug>
  listmanager.py update [-m | --mode <public | private>]
    [-d | --desc <DESC>] [--name <NAME>] <owner_screen_name> <slug>
  listmanager.py destroy <owner_screen_name> <slug>
"""

from common_twitter import AbstractTwitterManager
from common_twitter import SEP
from common_twitter import format_list
from common_twitter import format_user
from common_twitter import get_list_csv_format
from common_twitter import get_user_csv_format
from listcommands import make_commands
from argparse import ArgumentParser
from itertools import count
from itertools import islice
import time

__version__ = '1.7.1'

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

    def request_statuses(self):
        """Show a timeline of tweets of the specified list."""

        request, logger, args = self.tw.lists.statuses, self.logger, self.args

        kwargs = dict(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug,
            count=args.count,
            include_rts=False,
            include_entities=False,)

        if args.max_id:
            kwargs['max_id'] = args.max_id

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

    def request_add(self):
        """Add multiple members to a list."""
        self._manage_members(self.tw.lists.members.create_all)

    def request_remove(self):
        """Remove multiple members from a list."""
        self._manage_members(self.tw.lists.members.destroy_all)

    def request_members(self):
        """List the members of the specified list."""
        self._show_users(self.tw.lists.members)

    def request_subscribers(self):
        """List the subscribers of the specified list."""
        self._show_users(self.tw.lists.subscribers)

    def request_subscribe(self):
        """Subscribe the authenticated user to the specified list."""

        args = self.args
        self.tw.lists.subscribe(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug)
        self.logger.info("Subscribed to {owner_screen_name}/{slug}.".format(**vars(args)))

    def request_unsubscribe(self):
        """Unsubscribe the authenticated user to the specified list."""

        args = self.args
        self.tw.lists.unsubscribe(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug)
        self.logger.info("Unsubscribed from {owner_screen_name}/{slug}.".format(**vars(args)))

    def request_memberships(self):
        """List lists the specified user has been added to."""
        self._show_lists(self.tw.lists.memberships)

    def request_ownerships(self):
        """List lists owned by the specified user."""
        self._show_lists(self.tw.lists.ownerships)

    def request_subscriptions(self):
        """List lists the specified user is subscribed to."""
        self._show_lists(self.tw.lists.subscriptions)

    def request_create(self):
        """Create a new list for the authenticated user."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'name',
            'mode',
            'description')
                if k in args}

        self.tw.lists.create(**kwargs)
        logger.info("List {} is created.".format(args.name))

    def request_describe(self):
        """Show the specified list."""

        args = self.args
        response = self.tw.lists.show(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug)

        print(get_list_csv_format())
        print(format_list(response))

    def request_update(self):
        """Update the specified list."""

        logger, args = self.logger, vars(self.args)

        kwargs = {k:args[k] for k in (
            'owner_screen_name',
            'slug',
            'name',
            'mode',
            'description')
                if k in args}

        self.tw.lists.update(**kwargs)
        logger.info("List {} is updated.".format(args.slug))

    def request_delete(self):
        """Delete the specified list."""

        logger, args = self.logger, self.args
        self.tw.lists.destroy(
            owner_screen_name=args.owner_screen_name,
            slug=args.slug)
        logger.info("List {} is deleted.".format(args.slug))

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
                owner_screen_name=args.owner_screen_name,
                slug=args.slug,
                screen_name=csv)

            logger.info("[{:04d}]-[{:04d}] Processed: {}".format(i, i + up_to, csv))
            time.sleep(15)

    def _show_users(self, request):
        """Show users related tp the specified list.

        Args:
            request: Select lists.members or lists.subscribers.
        """

        logger, args = self.logger, self.args

        print(get_user_csv_format())

        next_cursor = -1
        while next_cursor != 0:
            # Request.
            response = request(
                owner_screen_name=args.owner_screen_name,
                slug=args.slug,
                count=args.count,
                cursor=next_cursor)

            for user in response['users']:
                print(format_user(user))

            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

    def _show_lists(self, request):
        """Show lists related to the specified user.

        Args:
            request: Select lists.ownerships, lists.memberships, etc.
        """

        logger, args = self.logger, self.args

        print(get_list_csv_format())

        next_cursor = -1
        while next_cursor != 0:
            response = request(
                screen_name=args.screen_name,
                count=args.count,
                cursor=next_cursor)

            for i in response['lists']:
                print(format_list(i))

            next_cursor = response['next_cursor']
            logger.info('next_cursor: {}'.format(next_cursor))

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
