#!/usr/bin/env python
"""MODULE DOCSTRING WILL BE DYNAMICALLY OVERRIDED."""

from argparse import (ArgumentParser, FileType)
from secret import twitter_instance
from twmods import (EPILOG, output)

DESCRIPTION = "Demonstrate Twitter's POST media/upload endpoint."

USAGE = """
  twmedia.py [--version] [--help]
  twmedia.py [--additional-owners <csv-of-user-ids>] FILE
"""

# pylint: disable=redefined-builtin
__doc__ = '\n'.join((DESCRIPTION, USAGE, EPILOG))
__version__ = '1.0.2'

def configure():
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    root_parser = ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
        usage=USAGE)
    root_parser.add_argument(
        '--version',
        action='version',
        version=__version__)
    root_parser.add_argument(
        '-o', '--additional-owners',
        dest='additional_owners',
        help='a comma-separated string of user IDs')
    root_parser.add_argument(
        'file',
        metavar='FILE',
        type=FileType('rb'),
        help='a PNG, JPEG, BMP, WEBP, or GIF file')

    return root_parser

def main(args=None):
    """The main function."""

    parser = configure()
    args = parser.parse_args(args)

    raw_data = args.file.read()
    print('file size = {} MB'.format(len(raw_data) >> 20))

    # Media uploads for images are limited to 5MB in file size,
    # and for videos are limited to 15MB. For chunked uploads,
    # the maximum chunk size is 5MB.
    #
    # MIME-types supported by this endpoint: PNG, JPEG, BMP, WEBP,
    # GIF, Animated GIF.

    kwargs = dict(media=raw_data)

    # A maximum of 100 additional owners may be specified.
    if args.additional_owners:
        kwargs['additional_owners'] = args.additional_owners

    # Uploaded media files will be available for use for 60 minutes
    # before they are flushed from the servers (if not associated
    # with a Tweet or Card).

    twhandler = twitter_instance(domain='upload.twitter.com')
    response = twhandler.media.upload(**kwargs)
    output(response)

if __name__ == '__main__':
    main()
