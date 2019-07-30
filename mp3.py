#!/usr/bin/env python
"""
mp3 downloader prototype

Usage:
$ mp3.py [OPTION] YOUTUBE_WATCH_URL...
Example:
$ mp3.py --save https://www.youtube.com/watch?v=xxxxxxxxxx
"""

from argparse import ArgumentParser
import asyncio
import sys
import time
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
        '-M', '--max-workers',
        type=int,
        default=3,
        help='the upper bound of the number of pools')
    parser.add_argument(
        '-s', '--save',
        action='store_true',
        help='write downloaded media to disk')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='explain what is being done')
    parser.add_argument(
        'watch_urls',
        metavar='URL',
        nargs='*',
        help='URL from which to extract mp3 files')

    parser.add_argument('--version', action='version', version=__version__)
    return parser.parse_args(args or [])

def timing_val(func):
    """DEBUG"""

    def wrapper(*arg, **kw):
        '''source: http://www.daniweb.com/code/snippet368.html'''
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        return (t2 - t1), res, func.__name__
    return wrapper

@timing_val
def run(args):
    """main function

    :param args:
        Command line parameters.
    """

    save = args.save
    if save:
        dest_dir = args.dest_dir
    verbose = args.verbose

    semaphore = asyncio.Semaphore(args.max_workers)

    async def run_core(args):
        tasks = [asyncio.create_task(
            download_media(watch_url)) for watch_url in args.watch_urls]
        await asyncio.gather(*tasks, return_exceptions=True)

    async def download_media(watch_url):
        async with semaphore:
            tube = YouTube(watch_url)

        media = tube.streams.filter(
            only_audio=True, file_extension='mp4').first()

        if verbose:
            print(media.default_filename)
        if save:
            try:
                media.download(output_path=dest_dir)
            except Exception:
                print(f'Error: {media.default_filename} is not downloaded')
                raise

    asyncio.run(run_core(args))

def main(args=sys.argv[1:]):
    """main function"""
    sys.exit(run(parse_args(args)))

if __name__ == "__main__":
    main()
