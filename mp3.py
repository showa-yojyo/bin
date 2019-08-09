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
from concurrent.futures import ThreadPoolExecutor
import logging
import sys
import time
from pytube import YouTube
from pytube import logger as pytube_logger

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
        action='count',
        default=0,
        help='increase verbosity')
    parser.add_argument(
        'watch_urls',
        metavar='URL',
        nargs='+',
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

def init_logger(args):
    """Initialize local logger (and reset pytube logger)
    """

    verbose = args.verbose
    formatter = pytube_logger.handlers[0].formatter

    logger = logging.getLogger(__name__)
    verbosity = verbose * 10
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(verbosity)

    logger.setLevel(verbosity)
    pytube_logger.setLevel(verbosity)

    logger.addHandler(handler)

    return logger

@timing_val
def run(args):
    """main function

    :param args:
        Command line parameters.
    """

    logger = init_logger(args)
    save = args.save
    if save:
        dest_dir = args.dest_dir
        logger.info('destination directory: %s', dest_dir)

    async def run_core(args, pool=None):
        """Concurrently execute `download_media`
        """
        loop = asyncio.get_running_loop()
        futures = [loop.run_in_executor(
            pool, download_media, watch_url) for watch_url in args.watch_urls]
        done, pending = await asyncio.wait(futures, return_when=asyncio.ALL_COMPLETED)
        logger.debug('done: %s', done)
        logger.debug('pending: %s', pending)

    def download_media(watch_url):
        tube = YouTube(watch_url)
        logger.info('on download: %s', watch_url)

        try:
            media = tube.streams.filter(
                only_audio=True, file_extension='mp4').first()
            assert media.default_filename
            logger.info('download completed: from %s to %s', watch_url, media.default_filename)
        except Exception:
            logger.exception('cannot download %s', watch_url)
            raise

        if save:
            try:
                media.download(output_path=dest_dir)
            except Exception:
                logger.exception(
                    '%s is not downloaded', media.default_filename)
                raise

    with ThreadPoolExecutor(max_workers=args.max_workers) as pool:
        asyncio.run(run_core(args, pool), debug=True)

def main(args=sys.argv[1:]):
    """main function"""
    sys.exit(run(parse_args(args)))

if __name__ == "__main__":
    main()
