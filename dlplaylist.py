#!/usr/bin/env python
"""
mp4 downloader prototype

Usage:
$ dlplaylist.py [OPTION] YOUTUBE_PLAYLIST_URL
Example:
$ dlplaylist.py https://www.youtube.com/playlist?list=xxxxxxxxxxxxxxxxxxxxxxxxxx
"""

from argparse import ArgumentParser
import re
import sys
from pytube import Playlist

__version__ = '1.0.0'

def parse_args(args):
    """Parse the command line parameters.

    Most options are taken from GNU wget.

    :param args:
        Raw command line arguments.

    :rtype: argparse.Namespace
    """

    parser = ArgumentParser(
        description='YouTube play list downloader',
        epilog='Mail bug reports and suggestions to <yojyo@hotmail.com>',
        add_help=False)

    parser.add_argument(
        'playlist_url',
        metavar='URL',
        nargs='*',
        help='URL of a play list')

    # Startup:
    startup_group = parser.add_argument_group('Startup')
    startup_group.add_argument(
        '-V', '--version',
        action='version',
        version=__version__)
    startup_group.add_argument(
        '-h', '--help',
        action='help',
        help='print this help')

    dir_group = parser.add_argument_group('Directories')
    dir_group.add_argument(
        '-P', '--directory-prefix',
        metavar='PREFIX',
        default='.',
        help='directory in which MP4 files will be saved')

    return parser.parse_args(args or [])


def run(args):
    """main function

    :param args:
        Command line parameters.
    """

    playlist = Playlist(args.url)
    # A work-around suggested by https://stackoverflow.com/questions/62661930/pytube3-playlist-returns-empty-list
    playlist._video_regex = re.compile(r'\"url\":\"(/watch\?v=[\w-]*)')

    output_path = args.directory_prefix
    for i, video in enumerate(playlist.videos):
        media = video.streams.filter(only_audio=True, file_extension='mp4').first()
        filename = f'{i:03d}-{video.title}'
        print(f'Saving {filename}...', file=sys.stderr)
        media.download(
            output_path=output_path,
            filename=filename)


def main(args=sys.argv[1:]):
    """main function"""
    sys.exit(run(parse_args(args)))


if __name__ == "__main__":
    main()
