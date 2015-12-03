#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""usermanager.py: A utility script to manage Twitter users.

Usage:
  usermanager.py [--version] [--help]
  usermanager.py lookup
    [-f | --file <filepath>] <screen-name>...
  usermanager.py show [--include-entities]
  usermanager.py search [-p | --page <n>] <user-id | screen-name>
    [-c | --count <n>] [--include-entities] <query>
  usermanager.py banner <user-id | screen-name>
  usermanager.py suggestions [-l | --lang <LANG>]
  usermanager.py spam <user-id | screen-name>
"""

from twmods import AbstractTwitterManager
from twmods.commands.users import make_commands
from argparse import ArgumentParser
from itertools import count
from itertools import islice
from pprint import pprint
import time

__version__ = '1.0.1'

class TwitterUserManager(AbstractTwitterManager):
    """This class handles commands about a Twitter users."""

    def __init__(self):
        super().__init__('usermanager', make_commands(self))

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that stores the command line
            parameters.
        """

        parser = ArgumentParser(description='a utility script to manage Twitter users')
        parser.add_argument('--version', action='version', version=__version__)
        return parser

    def request_users_lookup(self):
        """Request GET users/lookup for Twitter."""

        request = self.tw.users.lookup
        logger, args = self.logger, self.args
        logger.info('tw.users.lookup args: {}'.format(args))

        # user_id
        user_ids = []
        if args.user_id:
            user_ids.extend(args.user_id)
        if args.file_user_id:
            user_ids.extend(line.rstrip() for line in args.file_user_id)

        # up to 100 users per request
        up_to = 100

        if user_ids:
            for i in count(0, up_to):
                chunk = islice(user_ids, i, i + up_to)
                csv = ','.join(chunk)
                if not csv:
                    break

                logger.info("[{:04d}]-[{:04d}] Waiting...".format(i, i + up_to))
                response = request(user_id=csv)
                pprint(response)
                logger.info("[{:04d}]-[{:04d}] Processed: {}".format(i, i + up_to, csv))
                time.sleep(2)

        # screen_name
        screen_names = []
        if args.screen_name:
            screen_names.extend(args.screen_name)
        if args.file_screen_name:
            screen_names.extend(line.rstrip() for line in args.file_screen_name)

        if screen_names:
            for i in count(0, up_to):
                chunk = islice(screen_names, i, i + up_to)
                csv = ','.join(chunk)
                if not csv:
                    break

                logger.info("[{:04d}]-[{:04d}] Waiting...".format(i, i + up_to))
                response = request(screen_name=csv)
                pprint(response)
                logger.info("[{:04d}]-[{:04d}] Processed: {}".format(i, i + up_to, csv))
                time.sleep(2)

    def request_users_show(self):
        """Request GET users/show for Twitter."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',
            'include_entities')
              if k in args}
        logger.info('tw.users.show args: {}'.format(kwargs))

        response = self.tw.users.show(**kwargs)
        pprint(response)

    def request_users_search(self):
        """Request GET users/search for Twitter."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'q',
            'pages',
            'count',
            'include_entities')
                if k in args}
        response = self.tw.users.search(**kwargs)
        pprint(response)

    def request_users_profile_banner(self):
        """Request GET users/profile_banner for Twitter."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',)
                if k in args}
        logger.info('tw.users.profile_banner args: {}'.format(kwargs))

        response = self.tw.users.profile_banner(**kwargs)
        pprint(response)

    def request_users_suggestions(self):
        """Request GET users/suggestions for Twitter."""

        logger, args = self.logger, self.args
        kwargs  = {}
        if 'lang' in args:
            kwargs['lang'] = args.lang

        response = self.tw.users.suggestions(**kwargs)
        pprint(response)

    def request_users_report_spam(self):
        """Request POST users/report_spam for Twitter."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',)
                if k in args}
        response = self.tw.users.report_spam(**kwargs)
        pprint(response)

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterUserManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
