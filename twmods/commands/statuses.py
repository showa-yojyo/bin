# -*- coding: utf-8 -*-
"""statuses.py: Implementation of class AbstractTwitterStatusesCommand
and its subclasses.
"""

from .. import AbstractTwitterCommand
from .. import cache
from .. import parser_user_single
from .. import parser_cursor
from .. import parser_include_entities
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

    def __call__(self):
        self.manager.request_statuses_mentions_timeline()

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

    def __call__(self):
        self.manager.request_statuses_user_timeline()

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

    def __call__(self):
        self.manager.request_statuses_home_timeline()

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
                     parser_include_entities()],
            help=self.__doc__)
        parser.add_argument(
            '--include-user-entities',
            dest='include_user_entities',
            action='store_true',
            help='include the user entities node')
        return parser

    def __call__(self):
        self.manager.request_statuses_retweets_of_me()

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
                     parser_status_id()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_statuses_retweets_id()

class ShowId(AbstractTwitterStatusesCommand):
    """Output a single tweet, specified by the id parameter."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_SHOW_ID[0],
            aliases=STATUSES_SHOW_ID[1:],
            parents=[parser_trim_user(),
                     parser_include_entities(),
                     parser_status_id()],
            help=self.__doc__)
        parser.add_argument(
            '--include-my-retweet',
            dest='include_my_retweet',
            action='store_true',
            help='cause an additional current_user_retweet node')
        return parser

    def __call__(self):
        self.manager.request_statuses_show_id()

class DestroyId(AbstractTwitterStatusesCommand):
    """Destroy the status specified by the required ID parameter."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_DESTROY_ID[0],
            aliases=STATUSES_DESTROY_ID[1:],
            parents=[parser_trim_user(),
                     parser_status_id()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_statuses_destroy_id()

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
            action='store_true',
            help='a list of media_ids to associate with the tweet')
        parser.add_argument(
            'text',
            help='the text of your status update, typically up to 140 characters')

        return parser

    def __call__(self):
        self.manager.request_statuses_update()

class RetweetId(AbstractTwitterStatusesCommand):
    """Retweet a tweet."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_RETWEET_ID[0],
            aliases=STATUSES_RETWEET_ID[1:],
            parents=[parser_trim_user(),
                     parser_status_id()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_statuses_retweet_id()

class Oembed(AbstractTwitterStatusesCommand):
    """Output a single tweet, specified by either a tweet web URL or
    the tweet ID.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_OEMBED[0],
            aliases=STATUSES_OEMBED[1:],
            parents=[],
            help=self.__doc__)

        # This command has many optional parameters to implement manually.
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--id',
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

    def __call__(self):
        self.manager.request_statuses_oembed()

class RetweetersIds(AbstractTwitterStatusesCommand):
    """Output a collection of up to 100 user IDs."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            STATUSES_RETWEETERS_IDS[0],
            aliases=STATUSES_RETWEETERS_IDS[1:],
            parents=[parser_cursor(),
                     parser_status_id()],
            help=self.__doc__)
        return parser

    def __call__(self):
        self.manager.request_statuses_retweeters_ids()

class Lookup(AbstractTwitterStatusesCommand):
    """Output fully-hydrated tweet objects for up to 100 tweets per request."""

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
            'id',
            metavar='<status_id>',
            help='a comma separated list of tweet IDs, up to 100 are allowed in a single request')

        return parser

    def __call__(self):
        self.manager.request_statuses_lookup()

def make_commands(manager):
    """Prototype"""
    return [cmd_t(manager) for cmd_t in AbstractTwitterStatusesCommand.__subclasses__()]

# parsers

@cache
def parser_count_statuses():
    """Return the parent parser object for --count option."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-c', '--count',
        type=int,
        nargs='?',
        choices=range(1, 201),
        metavar='{1..200}',
        help='the number of tweets to return per page')
    return parser

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
def parser_since_max_ids():
    """Return the parent parser object for --since-id and --max-id option."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--since-id',
        dest='since_id',
        type=int,
        nargs='?',
        metavar='<status_id>',
        help='return results with an ID greater than the specified ID')
    parser.add_argument(
        '--max-id',
        dest='max_id',
        type=int,
        nargs='?',
        metavar='<status_id>',
        help='return results with an ID less than or equal to the specified ID')

    return parser

@cache
def parser_trim_user():
    """Return the parent parser object for --trim-user option."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--trim-user',
        dest='trim_user',
        action='store_true',
        help='get only the status authors ID in user object')
    return parser

@cache
def parser_contributor_details():
    """Return the parent parser object for --contributor-details option."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--contributor-details',
        dest='contributor_details',
        action='store_true',
        help='enhance the contributors element of the status')
    return parser

@cache
def parser_exclude_replies():
    """Return the parent parser object for --exclude-replies option."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-X', '--exclude-replies',
        dest='exclude_replies',
        action='store_true',
        help='prevent replies from appearing in the timeline')
    return parser

@cache
def parser_include_rts():
    """Return the parent parser object for --include-rts option."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--include-rts',
        dest='include_rts',
        action='store_true',
        help='show native retweets in the timeline')
    return parser

@cache
def parser_status_id():
    """Return the parent parser object for id argument."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        'id',
        type=int,
        nargs='?',
        metavar='<status_id>',
        help='a status Id')
    return parser
