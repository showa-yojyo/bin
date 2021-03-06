"""account.py: Implementation of class AbstractTwitterAccountCommand
and its subclasses.
"""

from argparse import FileType
from . import AbstractTwitterCommand, call_decorator
from ..parsers import (filter_args,
                       parser_include_entities,
                       parser_skip_status)

# POST account/remove_profile_banner
# GET account/settings
# POST account/settings
# POST account/update_delivery_device
# POST account/update_profile
# POST account/update_profile_background_image
# POST account/update_profile_banner
# POST account/update_profile_image
# GET account/verify_credentials

ACCOUNT_REMOVE_PROFILE_BANNER = ('account/remove_profile_banner',
                                 'remove_profile_banner')
ACCOUNT_SETTINGS_G = ('account/settings_g', 'get')
ACCOUNT_SETTINGS_P = ('account/settings_p', 'set')
ACCOUNT_UPDATE_DELIVERY_DEVICE = ('account/update_delivery_device',
                                  'delivery_device')
ACCOUNT_UPDATE_PROFILE = ('account/update_profile',
                          'profile')
ACCOUNT_UPDATE_PROFILE_BACKGROUND_IMAGE = (
    'account/update_profile_background_image',
    'profile_background_image')
ACCOUNT_UPDATE_PROFILE_BANNER = ('account/update_profile_banner',
                                 'profile_banner')
ACCOUNT_UPDATE_PROFILE_IMAGE = ('account/update_profile_image',
                                'profile_image')
ACCOUNT_VERIFY_CREDENTIALS = ('account/verify_credentials',
                              'verify')

# pylint: disable=abstract-method
class AbstractTwitterAccountCommand(AbstractTwitterCommand):
    """n/a"""
    pass

class CommandRemoveProfileBanner(AbstractTwitterAccountCommand):
    """Remove the uploaded profile banner for the authenticating user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            ACCOUNT_REMOVE_PROFILE_BANNER[0],
            aliases=ACCOUNT_REMOVE_PROFILE_BANNER[1:],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request POST account/remove_profile_banner for Twitter."""

        return {}, self.twhandler.account.remove_profile_banner

class CommandSettingsG(AbstractTwitterAccountCommand):
    """Print settings (including current trend, geo and sleep time
    information) for the authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            ACCOUNT_SETTINGS_G[0],
            aliases=ACCOUNT_SETTINGS_G[1:],
            help=self.__doc__)
        return parser

    @call_decorator
    def __call__(self):
        """Request GET account/settings for Twitter."""

        kwargs = dict(_method='GET')
        return kwargs, self.twhandler.account.settings

class CommandSettingsP(AbstractTwitterAccountCommand):
    """Update the authenticating user's settings."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            ACCOUNT_SETTINGS_P[0],
            aliases=ACCOUNT_SETTINGS_P[1:],
            help=self.__doc__)
        parser.add_argument(
            '--sleep-time-enabled',
            dest='sleep_time_enabled',
            action='store_true',
            help='enable sleep time')
        parser.add_argument(
            '--start-sleep-time',
            dest='start_sleep_time',
            metavar='<HH>',
            help='the hour that sleep time should begin')
        parser.add_argument(
            '--end-sleep-time',
            dest='end_sleep_time',
            metavar='<HH>',
            help='the hour that sleep time should end')
        parser.add_argument(
            '--time-zone',
            dest='time_zone',
            metavar='<TZ>',
            help='the timezone dates and times should be displayed in')
        parser.add_argument(
            '--trend-location-woeid',
            dest='trend_location_woeid',
            metavar='<woeid>',
            help='default trend location')
        parser.add_argument(
            '--allow-contributor-request',
            dest='allow_contributor_request',
            choices=['none', 'all', 'following'],
            metavar='{none,all,following}',
            help='allow others to include user as contributor')
        parser.add_argument(
            '--lang',
            help='the language which Twitter should render in')
        return parser

    @call_decorator
    def __call__(self):
        """Request POST account/settings for Twitter."""

        args = vars(self.args)
        kwargs = filter_args(
            args,
            'sleep_time_enabled', 'start_sleep_time', 'end_sleep_time',
            'time_zone', 'trend_location_woeid',
            'allow_contributor_request', 'lang')

        return kwargs, self.twhandler.account.settings

class CommandUpdateDeliveryDevice(AbstractTwitterAccountCommand):
    """Set which device Twitter delivers updates to for the
    authenticating user.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            ACCOUNT_UPDATE_DELIVERY_DEVICE[0],
            aliases=ACCOUNT_UPDATE_DELIVERY_DEVICE[1:],
            parents=[parser_include_entities()],
            help=self.__doc__)
        parser.add_argument(
            'device',
            choices=['ms', 'none'],
            metavar='{ms,none}',
            help='the device to which to update')

        return parser

    @call_decorator
    def __call__(self):
        """Request POST account/update_delivery_device for Twitter."""

        args = vars(self.args)
        kwargs = filter_args(
            args,
            'device', 'include_entities')

        return kwargs, self.twhandler.account.update_delivery_device

class CommandUpdateProfile(AbstractTwitterAccountCommand):
    """Set some values that users are able to set under the Account
    tab of their settings page.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            ACCOUNT_UPDATE_PROFILE[0],
            aliases=ACCOUNT_UPDATE_PROFILE[1:],
            parents=[parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)
        parser.add_argument(
            '--name',
            help='full name associated with the profile')
        parser.add_argument(
            '--url',
            help='URL associated with the profile')
        parser.add_argument(
            '--location',
            help='the city or country describing where '
                 'the user of the account is located')
        parser.add_argument(
            '--description',
            help='a description of the user owning the account')
        parser.add_argument(
            '--profile-link-color',
            dest='profile_link_color',
            help='a hex value that controls the color scheme of '
                 'links on your profile page')
        return parser

    @call_decorator
    def __call__(self):
        """Request POST account/update_profile for Twitter."""

        args = vars(self.args)
        kwargs = filter_args(
            args,
            'name', 'url', 'location', 'description',
            'profile_link_color')

        return kwargs, self.twhandler.account.update_profile

class CommandUpdateProfileBackgroundImage(AbstractTwitterAccountCommand):
    """Update the authenticating user's profile background image."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            ACCOUNT_UPDATE_PROFILE_BACKGROUND_IMAGE[0],
            aliases=ACCOUNT_UPDATE_PROFILE_BACKGROUND_IMAGE[1:],
            parents=[parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)

        # required should be True
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument(
            '-I', '--image',
            type=FileType('rb'),
            help='the background image for the profile')
        group.add_argument(
            '-M', '--media-id',
            dest='media_id',
            metavar='<media_id>',
            help='the media to use as the background image')
        parser.add_argument(
            '--tile',
            action='store_true',
            help='the background image will be displayed tiled')
        return parser

    @call_decorator
    def __call__(self):
        """Request POST account/update_profile_background_image for Twitter."""

        args = vars(self.args)
        kwargs = filter_args(
            args,
            'image', # will be base64-encoded by PTT.
            'media_id', 'tile')

        return kwargs, self.twhandler.account.update_profile_background_image

class CommandUpdateProfileBanner(AbstractTwitterAccountCommand):
    """Upload a profile banner on behalf of the authenticating user."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            ACCOUNT_UPDATE_PROFILE_BANNER[0],
            aliases=ACCOUNT_UPDATE_PROFILE_BANNER[1:],
            help=self.__doc__)
        # banner:The Base64-encoded or raw image data
        parser.add_argument(
            'banner',
            type=FileType('rb'),
            help='image data')
        parser.add_argument(
            '-W', '--width',
            type=int,
            help='the width of the preferred section of the image')
        parser.add_argument(
            '-H', '--height',
            type=int,
            help='the height of the preferred section of the image')
        parser.add_argument(
            '-L', '--offset-left',
            dest='offset_left',
            type=int,
            help='the number of pixels by which to offset '
                 'the uploaded image from the left')
        parser.add_argument(
            '-T', '--offset-top',
            dest='offset_top',
            type=int,
            help='the number of pixels by which to offset '
                 'the uploaded image from the top')
        return parser

    @call_decorator
    def __call__(self):
        """Request POST account/update_profile_banner for Twitter."""

        args = vars(self.args)
        kwargs = filter_args(
            args,
            'banner', # will be base64-encoded by PTT.
            'width', 'height', 'offset_left', 'offset_top')

        return kwargs, self.twhandler.account.update_profile_banner

class CommandUpdateProfileImage(AbstractTwitterAccountCommand):
    """Update the authenticating user's profile image."""

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            ACCOUNT_UPDATE_PROFILE_IMAGE[0],
            aliases=ACCOUNT_UPDATE_PROFILE_IMAGE[1:],
            parents=[parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)
        parser.add_argument(
            'image',
            type=FileType('rb'),
            help='the avatar image for the profile')
        return parser

    @call_decorator
    def __call__(self):
        """Request POST account/update_profile_image for Twitter."""

        args = vars(self.args)
        kwargs = filter_args(
            args,
            'image', # will be base64-encoded by PTT.
            'include_entities', 'skip_status')

        return kwargs, self.twhandler.account.update_profile_image

class CommandVerifyCredentials(AbstractTwitterAccountCommand):
    """Return an HTTP 200 OK response code and a representation of
    the requesting user if authentication was successful.
    """

    def create_parser(self, subparsers):
        parser = subparsers.add_parser(
            ACCOUNT_VERIFY_CREDENTIALS[0],
            aliases=ACCOUNT_VERIFY_CREDENTIALS[1:],
            parents=[parser_include_entities(),
                     parser_skip_status()],
            help=self.__doc__)
        parser.add_argument(
            '--email',
            action='store_true',
            help='email will be returned in the user objects as a string')
        return parser

    @call_decorator
    def __call__(self):
        """Request GET account/verify_credentials for Twitter."""

        request = self.twhandler.account.verify_credentials
        kwargs = filter_args(
            vars(self.args),
            'include_entities', 'skip_status', 'email')

        return kwargs, request

def make_commands(manager):
    """Prototype"""

    # pylint: disable=no-member
    return (cmd_t(manager) for cmd_t in
            AbstractTwitterAccountCommand.__subclasses__())
