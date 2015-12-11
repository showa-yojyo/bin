#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""twuser.py: A utility script to manage Twitter users.

Usage:
  twuser.py [--version] [--help]
  twuser.py users-lookup [<userspec>...]
    [-UF | --file-user-id <path>]
    [-SF | --file-screen-name <path>]
  twuser.py users-show [--include-entities] <userspec>
  twuser.py users-search [-F | --full] [-p | --page <n>]
    [-c | --count <n>] [-E | --include-entities] <query>
  twuser.py users-profile-banner <userspec>
  twuser.py users-suggestions [-l | --lang <LANG>]
  twuser.py users-report-spam <userspec>

where
  <userspec> ::= (-U | --user-id <user_id>)
               | (-S | --screen-name <screen_name>)
"""

from twitter import TwitterHTTPError
from twmods import AbstractTwitterManager
from twmods import output
from twmods.commands.users import make_commands
from argparse import ArgumentParser
from itertools import count
import time

__version__ = '1.1.2'

class TwitterUserManager(AbstractTwitterManager):
    """This class handles commands about a Twitter users."""

    def __init__(self):
        super().__init__('twuser', make_commands(self))

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
        self._request_users_csv(self.tw.users.lookup)

    def request_users_show(self):
        """Request GET users/show for Twitter."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',
            'include_entities')
              if k in args}
        logger.info('tw.users.show args: {}'.format(kwargs))

        response = self.tw.users.show(**kwargs)

        output(response)

    def request_users_search(self):
        """Request GET users/search for Twitter."""

        logger, args = self.logger, vars(self.args)
        request = self.tw.users.search
        results = None
        if args['full']:
            UP_TO = 20
            MAX_PAGE = 1000 // UP_TO
            kwargs = {k:args[k] for k in (
                'q',
                'include_entities')
                    if (k in args) and (args[k] is not None)}

            results = []
            kwargs['count'] = UP_TO
            try:
                for i in range(MAX_PAGE):
                    kwargs['page'] = i + 1
                    logger.info('users.search params={}'.format(kwargs))
                    response = request(**kwargs)
                    if not response:
                        break

                    results.extend(response)
                    if len(response) < UP_TO:
                        break

                    time.sleep(2)
            except TwitterHTTPError as e:
                logger.error('{}'.format(e))
                #raise
        else:
            kwargs = {k:args[k] for k in (
                'q',
                'page',
                'count',
                'include_entities')
                    if (k in args) and (args[k] is not None)}

            logger.info('users.search params={}'.format(kwargs))
            results = request(**kwargs)
        output(results)

    def request_users_profile_banner(self):
        """Request GET users/profile_banner for Twitter."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',)
                if k in args}
        logger.info('tw.users.profile_banner args: {}'.format(kwargs))

        response = self.tw.users.profile_banner(**kwargs)
        output(response)

    def request_users_suggestions(self):
        """Request GET users/suggestions for Twitter."""

        logger, args = self.logger, self.args
        kwargs  = {}
        if 'lang' in args:
            kwargs['lang'] = args.lang

        response = self.tw.users.suggestions(**kwargs)
        output(response)

    def request_users_report_spam(self):
        """Request POST users/report_spam for Twitter."""

        logger, args = self.logger, vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',)
                if k in args}

        response = self.tw.users.report_spam(**kwargs)
        output(response)

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
