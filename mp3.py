#!/usr/bin/env python
"""
mp3 downloader prototype

Usage:
$ mp3.py [OPTION] YOUTUBE_WATCH_URL...
Example:
$ mp3.py --save https://www.youtube.com/watch?v=xxxxxxxxxx
"""

from argparse import ArgumentParser
import sys
from pytube import YouTube

__version__ = '1.0.0'

def parse_args(args):
    """Parse the command line parameters.

    Returns:
        An instance of argparse.ArgumentParser that stores the command line
        parameters.
    """

    parser = ArgumentParser(description='mp3 downloader protptype')
    parser.add_argument(
        '-d', '--destination',
        dest='dest_dir',
        metavar='DEST',
        default='.',
        help='dirctory in which files are saved')
    parser.add_argument(
        '-s', '--save',
        action='store_true',
        help='write downloaded media to disk')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='explain what is being done')
    parser.add_argument(
        'url',
        nargs='*',
        help='URL from which to extract mp3 files')

    parser.add_argument('--version', action='version', version=__version__)
    return parser.parse_args(args or [])

def download(url):
    """Download a video file from YouTube

    Without writing any media to disk.

    :param str url:
        A YouTube watch URL.
    :returns:
        A stream of mp4?
    """
    tube = YouTube(url)
    return tube.streams.filter(only_audio=True, file_extension='mp4').first()

def save(media, dest_dir):
    """Save media to disk

    :param Stream media:
        Media stream to be saved.
    :param str dest_dir:
        Output path for writing media file.
    :rtype str:
    :returns:
        Output file path.
    """

    return media.download(output_path=dest_dir)

def run(args):
    """main function"""

    for i in args.url:
        media = download(i)
        if args.verbose:
            print(media.default_filename)
        if args.save:
            save(media, args.dest_dir)

def main(args=sys.argv[1:]):
    """main function"""
    sys.exit(run(parse_args(args)))

if __name__ == "__main__":
    main()
