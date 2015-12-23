# -*- coding: utf-8 -*-
"""statuses.py: Implementation of class AbstractTwitterStatusesCommand
and its subclasses.
"""

from . import AbstractTwitterCommand, call_decorator
from ..parsers import (
    cache,
    parser_user_single,
    parser_count_statuses,
    parser_cursor,
    parser_since_max_ids,
    parser_include_entities,
    parser_include_rts,
    parser_include_user_entities)
from argparse import ArgumentParser

# commands

STATUSES_MENTIONS_TIMELINE = ('statuses/mentions_timeline', 'mentions_timeline', 'mt',)
STATUSES_USER_TIMELINE = ('statuses/user_timeline', 'user_timeline', 'ut',)
STATUSES_HOME_TIMELINE = ('statuses/home_timeline', 'home_timeline', 'ht',)
STATUSES_RETWEETS_OF_ME = ('statuses/retweets_of_me', 'retweets_of_me', 'rom',)
STATUSES_RETWEETS_ID = ('statuses/retweets/:id', 'retweets',)
STATUSES_SHOW_ID = ('statuses/show/:id', 'show',)
STATUSES_DESTROY_ID = ('statuses/destroy/:id', 'destroy',)
STATUSES_UPDATE = ('statuses/update', 'update',)
STATUSES_RETWEET_ID = ('statuses/retweet/:id', 'retweet',)
STATUSES_OEMBED = ('statuses/oembed', 'oembed',)
STATUSES_RETWEETERS_IDS = ('statuses/retweeters/ids', 'retweeters',)
STATUSES_LOOKUP = ('statuses/lookup', 'lookup',)

class AbstractTwitterStatusesCommand(AbstractTwitterCommand):
    pass

class MentionsTimeline(AbstractTwitterStatusesCommand):
    """Output the 20 most recent mentions (tweets containing a user's
    @screen_name) for the authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_MENTIONS_TIMELINE[0],
            aliases=STATUSES_MENTIONS_TIMELINE[1:],
            parents=[parser_count_statuses(), # 200
                     parser_since_max_ids(),
                     parser_trim_user(),
                     parser_contributor_details(),
                     parser_include_entities()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET statuses/mentions_timeline for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'count', 'since_id', 'max_id',
            'trim_user', 'contributor_details', 'include_entities',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.statuses.mentions_timeline

class UserTimeline(AbstractTwitterStatusesCommand):
    """Output a collection of the most recent tweets posted by the
    user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_USER_TIMELINE[0],
            aliases=STATUSES_USER_TIMELINE[1:],
            parents=[parser_count_statuses(), # 200
                     parser_since_max_ids(),
                     parser_trim_user(),
                     parser_exclude_replies(),
                     parser_contributor_details(),
                     parser_include_rts(),
                     parser_user_single(),],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET statuses/user_timeline for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'user_id', 'screen_name',
            'count', 'since_id', 'max_id',
            'trim_user', 'exclude_replies', 'contributor_details',
            'include_rts',)
                if (k in args) and (args[k] is not None)}

        return kwargs, self.tw.statuses.user_timeline

class HomeTimeline(AbstractTwitterStatusesCommand):
    """Output a collection of the most recent tweets and retweets
    posted by the authenticating user and the users they follow.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_HOME_TIMELINE[0],
            aliases=STATUSES_HOME_TIMELINE[1:],
            parents=[parser_count_statuses(), # 20, 200
                     parser_since_max_ids(),
                     parser_trim_user(),
                     parser_exclude_replies(),
                     parser_contributor_details(),
                     parser_include_rts()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET statuses/home_timeline for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'count', 'since_id', 'max_id',
            'trim_user', 'exclude_replies', 'contributor_details',
            'include_rts',)
                if (k in args) and (args[k] is not None)}

        return kwargs, self.tw.statuses.home_timeline

class RetweetsOfMe(AbstractTwitterStatusesCommand):
    """Output the most recent tweets authored by the authenticating
    user that have been retweeted by others.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_RETWEETS_OF_ME[0],
            aliases=STATUSES_RETWEETS_OF_ME[1:],
            parents=[parser_count_retweets(), # 20, 100
                     parser_since_max_ids(),
                     parser_trim_user(),
                     parser_include_entities(),
                     parser_include_user_entities()],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET statuses/retweets_of_me for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'count', 'since_id', 'max_id',
            'trim_user', 'include_entities', 'include_user_entities',)
                if (k in args) and (args[k] is not None)}

        return kwargs, self.tw.statuses.retweets_of_me

class RetweetsId(AbstractTwitterStatusesCommand):
    """Output a collection of the 100 most recent retweets of the
    tweet specified by the id parameter.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_RETWEETS_ID[0],
            aliases=STATUSES_RETWEETS_ID[1:],
            parents=[parser_count_retweets(), # 100
                     parser_trim_user(),
                     parser_status_id()], # 'id'
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET statuses/retweets/:id for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            '_id', 'count', 'trim_user',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.statuses.retweets._id

class ShowId(AbstractTwitterStatusesCommand):
    """Output a single tweet, specified by the id parameter."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_SHOW_ID[0],
            aliases=STATUSES_SHOW_ID[1:],
            parents=[parser_trim_user(),
                     parser_include_entities(),
                     parser_status_id()], # 'id'
            help=self.__doc__)
        parser.add_argument(
            '--include-my-retweet',
            dest='include_my_retweet',
            action='store_true',
            help='cause an additional current_user_retweet node')
        return parser

    @call_decorator
    def __call__(self):
        """Request GET statuses/show/:id for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            '_id', 'trim_user', 'include_my_retweet', 'include_entities',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.statuses.show._id

class DestroyId(AbstractTwitterStatusesCommand):
    """Destroy the status specified by the required ID parameter."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_DESTROY_ID[0],
            aliases=STATUSES_DESTROY_ID[1:],
            parents=[parser_trim_user(),
                     parser_status_id()], # ?
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request POST statuses/destroy/:id for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            '_id', 'trim_user',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.statuses.destroy._id

class Update(AbstractTwitterStatusesCommand):
    """Update the authenticating user's current status, also known
    as tweeting.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_UPDATE[0],
            aliases=STATUSES_UPDATE[1:],
            parents=[parser_trim_user()],
            help=self.__doc__)

        # This command has many optional parameters to implement manually.
        parser.add_argument(
            '--in-reply-to-status-id',
            dest='in_reply_to_status_id',
            type=int,
            nargs='?',
            help='the ID of an existing status that the update is in reply to')
        parser.add_argument(
            '--possibly-sensitive',
            dest='possibly_sensitive',
            action='store_true',
            help='be considered sensitive content e.g. nudity, violence, etc.')
        parser.add_argument(
            '--lat',
            metavar='{-90.0..90.0}',
            help='the latitude of the location this tweet refers to')
        parser.add_argument(
            '--long',
            metavar='{-180.0..180.0}',
            help='the longitude of the location this tweet refers to')
        parser.add_argument(
            '--place-id',
            dest='place_id',
            metavar='<place>',
            help='a place in the world')
        parser.add_argument(
            '--display-coordinates',
            dest='display_coordinates',
            action='store_true',
            help='put a pin on the exact coordinates a tweet has been sent from')
        parser.add_argument(
            '--media-ids',
            dest='media_ids',
            help='a list of media ids to associate with the tweet')
        parser.add_argument(
            'status',
            help='the text of your status update, typically up to 140 characters')

        return parser

    def __call__(self):
        """Request POST statuses/update for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'status', 'in_reply_to_status_id',
            'possibly_sensitive', 'lat', 'long',
            'place_id', 'display_coordinates',
            'trim_user', 'media_ids',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.statuses.update

class RetweetId(AbstractTwitterStatusesCommand):
    """Retweet a tweet."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_RETWEET_ID[0],
            aliases=STATUSES_RETWEET_ID[1:],
            parents=[parser_trim_user(),
                     parser_status_id()], # ?'id'
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request POST statuses/retweet/:id for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            '_id', 'trim_user',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.statuses.retweet._id

class Oembed(AbstractTwitterStatusesCommand):
    """Output a single tweet, specified by either a tweet web URL or
    the tweet ID.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_OEMBED[0],
            aliases=STATUSES_OEMBED[1:],
            #parents=[],
            help=self.__doc__)

        # This command has many optional parameters to implement manually.
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--id',
            dest='_id',
            help='the ID of the desired tweet')
        group.add_argument(
            '--url',
            help='the URL of the Tweet to be embedded')

        parser.add_argument(
            '--maxwidth',
            type=int,
            metavar='{220..250}',
            help='the maximum width of a rendered tweet in whole pixels')
        parser.add_argument(
            '--hide-media',
            dest='hide_media',
            action='store_true',
            help='hide photo, video, or link previews')
        parser.add_argument(
            '--hide-thread',
            dest='hide_thread',
            action='store_true',
            help='hide conversation thread')
        parser.add_argument(
            '--omit-script',
            dest='omit_script',
            action='store_true',
            help='cut the <script> tag for loading widgets.js')
        parser.add_argument(
            '--align',
            choices=['none', 'center', 'left', 'right'],
            help='Specify how the embedded tweet is floated')
        parser.add_argument(
            '--related',
            metavar='<csv-of-screen-names>',
            help='a comma-separated list of Twitter usernames related to your content')
        parser.add_argument(
            '--lang',
            help='the language of returned HTML')
        parser.add_argument(
            '--widget-type',
            dest='widget_type',
            choices=['video'],
            help='set to video to return a Twitter Video embed for the given tweet')
        parser.add_argument(
            '--hide-tweet',
            dest='hide_tweet',
            action='store_true',
            help='link directly to the tweet url instead of displaying a tweet overlay')

        return parser

    @call_decorator
    def __call__(self):
        """Request GET statuses/oembed for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            '_id', 'url',
            'maxwidth', 'hide_media', 'hide_thread', 'omit_script',
            'align', 'related', 'lang', 'widget_type', 'hide_tweet',)
                if (k in args) and (args[k] is not None)}

        return kwargs, self.tw.statuses.oembed

class RetweetersIds(AbstractTwitterStatusesCommand):
    """Output a collection of up to 100 user IDs."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_RETWEETERS_IDS[0],
            aliases=STATUSES_RETWEETERS_IDS[1:],
            parents=[parser_cursor(),
                     parser_status_id()], # '_id'
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET statuses/retweeters/ids for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            '_id', 'cursor', 'stringify_ids',)
                if (k in args) and (args[k] is not None)}

        return kwargs, self.tw.statuses.retweeters_ids

class Lookup(AbstractTwitterStatusesCommand):
    """Output fully-hydrated tweet objects for up to 100 tweets per
    request.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_LOOKUP[0],
            aliases=STATUSES_LOOKUP[1:],
            parents=[parser_include_entities(),
                     parser_trim_user()],
            help=self.__doc__)
        parser.add_argument(
            '--map',
            action='store_true',
            help='show invisible tweets for you by an explicitly null values')
        parser.add_argument(
            '_id',
            metavar='<status_id>',
            help='a comma separated list of tweet IDs, up to 100 are allowed in a single request')

        return parser

    @call_decorator
    def __call__(self):
        """Request GET statuses/lookup for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            '_id', 'trim_user', 'include_entities', 'map',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.statuses.lookup

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterStatusesCommand.__subclasses__()]

# parsers

@cache
def parser_count_retweets():
    """Return the parent parser object for --count option."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        choices=range(1, 101),
        metavar='{1..100}',
        help='the number of tweets to return per page')
    return parser

@cache
def parser_trim_user():
    """Return the parent parser object for --trim-user optional
    argument.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--trim-user',
        dest='trim_user',
        action='store_true',
        help='get only the status authors ID in user object')
    return parser

@cache
def parser_contributor_details():
    """Return the parent parser object for --contributor-details
    optional argument.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--contributor-details',
        dest='contributor_details',
        action='store_true',
        help='enhance the contributors element of the status')
    return parser

@cache
def parser_exclude_replies():
    """Return the parent parser object for --exclude-replies optional
    argument.
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-X', '--exclude-replies',
        dest='exclude_replies',
        action='store_true',
        help='prevent replies from appearing in the timeline')
    return parser

@cache
def parser_status_id():
    """Return the parent parser object for id argument."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '_id',
        type=int,
        nargs='?',
        metavar='<status_id>',
        help='a status Id')
    return parser
