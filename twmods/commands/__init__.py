# -*- coding: utf-8 -*-
"""__init__.py
"""

from abc import ABCMeta
from abc import abstractmethod
from .. import output
from itertools import (count, islice)
from twitter import TwitterHTTPError
import time

__version__ = '1.8.5'

class AbstractTwitterCommand(metaclass=ABCMeta):
    """Prototype"""

    def __init__(self, manager):
        """Prototype"""
        self.manager = manager

    @property
    def args(self):
        return self.manager.args

    @property
    def logger(self):
        return self.manager.logger

    @property
    def tw(self):
        return self.manager.tw

    @abstractmethod
    def create_parser(self, subparsers): pass

    @abstractmethod
    def __call__(self): pass

    # Helper methods

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
        logger.info('args={}'.format(kwargs))

        results = []
        try:
            while kwargs['cursor']:
                response = request(**kwargs)
                results.extend(response['ids'])
                next_cursor = response['next_cursor']
                logger.info('next_cursor: {}'.format(next_cursor))
                kwargs['cursor'] = next_cursor
        except TwitterHTTPError as e:
            logger.info('{}'.format(e))
            #raise

        print('\n'.join(results))
        logger.info('finished')

    def _list_common(self, request):
        """The common procedure of friends/list and followers/list.

        Args:
            request: A PTT request method for Twitter API.
        """

        logger, args = self.logger, vars(self.args)

        kwargs = dict(cursor=-1)
        kwargs.update(
            {k:args[k] for k in (
                'user_id', 'screen_name',
                'count', 'cursor', 'include_user_entities')
             if (k in args) and (args[k] is not None)})
        logger.info('args={}'.format(kwargs))

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

                logger.info("[{:04d}]-[{:04d}] Waiting...".format(i, i + up_to))
                response = request(user_id=csv, **kwargs)
                results.extend(response)
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
                csv = ','.join(islice(screen_names, i, i + up_to))
                if not csv:
                    break

                logger.info("[{:04d}]-[{:04d}] Waiting...".format(i, i + up_to))
                response = request(screen_name=csv, **kwargs)
                results.extend(response)

                logger.info("[{:04d}]-[{:04d}] Processed: {}".format(i, i + up_to, csv))
                time.sleep(2)

        output(results)
        logger.info('finished')

def call_decorator(op):
    def inner(cmd):
        kwargs, request = op(cmd)
        logger = cmd.manager.logger
        logger.info('args={}'.format(kwargs))
        output(request(**kwargs))
        logger.info('finished')

    return inner
