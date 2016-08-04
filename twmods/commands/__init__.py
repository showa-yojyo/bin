# -*- coding: utf-8 -*-
"""__init__.py
"""

from abc import (ABCMeta, abstractmethod)
from itertools import (count, islice)
import time

from twitter import TwitterHTTPError

from .. import output
from ..parsers import filter_args

__version__ = '1.8.6'

class AbstractTwitterCommand(metaclass=ABCMeta):
    """Prototype"""

    def __init__(self, manager):
        """Prototype"""
        self.manager = manager

    @property
    def args(self):
        """Return the arguments."""
        return self.manager.args

    @property
    def logger(self):
        """Return the logger."""
        return self.manager.logger

    @property
    def twhandler(self):
        """Return the Twitter handler."""
        return self.manager.twhandler

    @abstractmethod
    def create_parser(self, subparsers):
        """Create an argument parser including subparsers."""
        pass

    @abstractmethod
    def __call__(self):
        """Invoke the command."""
        pass

    # Helper methods

    def list_ids(self, request):
        """Print user IDs.

        Args:
            request: A PTT request method for Twitter API.
        """

        logger, args = self.logger, vars(self.args)

        kwargs = dict(
            cursor=-1,
            stringify_ids=True,)
        kwargs.update(filter_args(args,
                                  'user_id',
                                  'screen_name',
                                  'count',
                                  'cursor'))
        logger.info('args={}'.format(kwargs))

        results = []
        try:
            while kwargs['cursor']:
                response = request(**kwargs)
                results.extend(response['ids'])
                next_cursor = response['next_cursor']
                logger.info('next_cursor: {}'.format(next_cursor))
                kwargs['cursor'] = next_cursor
        except TwitterHTTPError as ex:
            logger.info('{}'.format(ex))
            #raise

        print('\n'.join(results))
        logger.info('finished')

    def _list_common(self, request):
        """The common procedure of friends/list and followers/list.

        Args:
            request: A PTT request method for Twitter API.
        """

        logger = self.logger

        kwargs = dict(cursor=-1)
        kwargs.update(filter_args(
            'user_id', 'screen_name',
            'count', 'cursor', 'include_user_entities'))
        logger.info('args={}'.format(kwargs))

        results = []
        try:
            while kwargs['cursor']:
                response = request(**kwargs)
                results.extend(response['users'])
                next_cursor = response['next_cursor']
                logger.info('next_cursor: {}'.format(next_cursor))
                kwargs['cursor'] = next_cursor
        except TwitterHTTPError as ex:
            logger.info('{}'.format(ex))
            #raise

        output(results)
        logger.info('finished')

    def _request_users_csv(self, request, up_to=100, **kwargs):
        """Common method to the following requests:

        * GET users/lookup
        * GET friendships/lookup
        * POST lists/members/create_all
        * POST lists/members/destroy_all
        """

        logger, args = self.logger, self.args
        logger.info('{} args: {}'.format(request.__name__, args))

        # Obtain the target users.
        # user_id
        user_ids = []
        if args.user_id:
            user_ids.extend(args.user_id)
        if args.file_user_id:
            user_ids.extend(line.rstrip() for line in args.file_user_id)

        # TODO: lists/xxx never get results.
        results = []

        if user_ids:
            for i in count(0, up_to):
                csv = ','.join(islice(user_ids, i, i + up_to))
                if not csv:
                    break

                logger.info("[{:04d}]-[{:04d}] Waiting...".format(
                    i, i + up_to))
                response = request(user_id=csv, **kwargs)
                results.extend(response)
                logger.info("[{:04d}]-[{:04d}] Processed: {}".format(
                    i, i + up_to, csv))
                time.sleep(2)

        # screen_name
        screen_names = []
        if args.screen_name:
            screen_names.extend(args.screen_name)
        if args.file_screen_name:
            screen_names.extend(line.rstrip() for line in args.file_screen_name)

        if screen_names:
            for i in count(0, up_to):
                csv = ','.join(islice(screen_names, i, i + up_to))
                if not csv:
                    break

                logger.info("[{:04d}]-[{:04d}] Waiting...".format(
                    i, i + up_to))
                response = request(screen_name=csv, **kwargs)
                results.extend(response)

                logger.info("[{:04d}]-[{:04d}] Processed: {}".format(
                    i, i + up_to, csv))
                time.sleep(2)

        output(results)
        logger.info('finished')

def call_decorator(operation):
    """Decorate a request operation."""
    def inner(cmd):
        """Invoke cmd.operation and execute it."""
        kwargs, request = operation(cmd)
        logger = cmd.manager.logger
        logger.info('args={}'.format(kwargs))
        output(request(**kwargs))
        logger.info('finished')

    return inner
