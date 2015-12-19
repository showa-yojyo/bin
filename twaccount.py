#!/usr/bin/env python
# -*- coding: utf-8 -*-

description = "A utility script to call accounts/xxx of Twitter API."

usage = """
  twaccount.py [--version] [--help]
  twaccount.py account/remove_profile_banner
  twaccount.py account/settings_g
  twaccount.py account/settings_p [--sleep-time-enabled]
    [--start-sleep-time <HH>] [--end-sleep-time <HH>]
    [--time-zone <TZ>] [--trend-location-woeid <woeid>]
    [--allow-contributor-request {none,all,following}]
    [--lang <language>]
  twaccount.py account/update_delivery_device
    [-E | --include-entities] {ms,none}
  twaccount.py account/update_profile [--name <text>]
    [--url <URL>] [--location <text>] [--description <text>]
    [--profile-link-color <hex>] [-E | --include-entities]
    [--skip-status]
  twaccount.py account/update_profile_background_image [--tile]
    [-E | --include-entities] [--skip-status] <imagespec>
  twaccount.py account/update_profile_banner [-w | --width <n>]
    [-H | --height <n>] [-L | --offset-left <n>]
    [-T | --offset-top <n>] [-E | --include-entities]
    [--skip-status] <path>
  twaccount.py account/update_profile_image
    [-E | --include-entities] [--skip-status] <path>
  twaccount.py account/verify_credentials

where
  <imagespec> ::= (-I | --image <path>)
                | (-M | --media-id <media_id>)
"""

from twmods import AbstractTwitterManager
from twmods import (epilog, output, request_decorator)
from twmods.commands.account import make_commands
from argparse import ArgumentParser

__doc__ = '\n'.join((description, usage, epilog))
__version__ = '1.0.0'

class TwitterAccountManager(AbstractTwitterManager):
    """This class handles accounts/xxx endpoints of Twitter API."""

    def __init__(self):
        super().__init__('twaccount', make_commands(self))

    def make_parser(self):
        """Create the command line parser.

        Returns:
            An instance of argparse.ArgumentParser that will store the command line
            parameters.
        """

        parser = ArgumentParser(
            description=description, epilog=epilog, usage=usage)
        parser.add_argument(
            '--version',
            action='version',
            version=__version__)
        return parser

    @request_decorator
    def request_account_remove_profile_banner(self):
        """Request POST account/remove_profile_banner for Twitter."""

        return {}, self.tw.account.remove_profile_banner

    @request_decorator
    def request_account_settings_g(self):
        """Request GET account/settings for Twitter."""

        args = vars(self.args)
        kwargs = dict(_method='GET')
        return kwargs, self.tw.account.settings

    @request_decorator
    def request_account_settings_p(self):
        """Request POST account/settings for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'sleep_time_enabled', 'start_sleep_time', 'end_sleep_time',
            'time_zone', 'trend_location_woeid',
            'allow_contributor_request', 'lang',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.account.settings

    @request_decorator
    def request_account_update_delivery_device(self):
        """Request POST account/update_delivery_device for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'device', 'include_entities',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.account.update_delivery_device

    @request_decorator
    def request_account_update_profile(self):
        """Request POST account/update_profile for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'name', 'url', 'location', 'description',
            'profile_link_color',)
                if (k in args) and (args[k] is not None)}
        return kwargs, self.tw.account.update_profile

    @request_decorator
    def request_account_update_profile_background_image(self):
        """Request POST account/update_profile_background_image for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'image', # will be base64-encoded by PTT.
            'media_id', 'tile',)
                if (k in args) and (args[k] is not None)}

        return kwargs, self.tw.account.update_profile_background_image

    @request_decorator
    def request_account_update_profile_banner(self):
        """Request POST account/update_profile_banner for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'banner', # will be base64-encoded by PTT.
            'width', 'height', 'offset_left', 'offset_top',)
                if (k in args) and (args[k] is not None)}

        return kwargs, self.tw.account.update_profile_banner

    @request_decorator
    def request_account_update_profile_image(self):
        """Request POST account/update_profile_image for Twitter."""

        args = vars(self.args)
        kwargs = {k:args[k] for k in (
            'image', # will be base64-encoded by PTT.
            'include_entities', 'skip_status',)
                if (k in args) and (args[k] is not None)}

        return kwargs, self.tw.account.update_profile_image

    @request_decorator
    def request_account_verify_credentials(self):
        """Request GET account/verify_credentials for Twitter."""

        request, args = self.tw.account.verify_credentials, vars(self.args)
        kwargs = {k:args[k] for k in (
            'include_entities', 'skip_status', 'email',)
                if (k in args) and (args[k] is not None)}
        return kwargs, request

def main(command_line=None):
    """The main function.

    Args:
        command_line: Raw command line arguments.
    """

    mgr = TwitterAccountManager()
    mgr.setup(command_line)
    mgr.execute()

if __name__ == '__main__':
    main()
