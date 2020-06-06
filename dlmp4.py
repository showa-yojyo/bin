#!/usr/bin/env python
"""
mp4 downloader prototype

Usage:
$ dlmp4.py [OPTION] YOUTUBE_WATCH_URL...
Example:
$ dlmp4.py https://www.youtube.com/watch?v=xxxxxxxxxx
"""

from argparse import ArgumentParser
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import sys
from pytube import YouTube
from pytube.__main__ import logger as pytube_logger

__version__ = '1.0.1'

def parse_args(args):
    """Parse the command line parameters.

    Most options are taken from GNU wget.

    :param args:
        Raw command line arguments.

    :rtype: argparse.Namespace
    """

    parser = ArgumentParser(
        description='mp4 downloader protptype',
        epilog='Mail bug reports and suggestions to <yojyo@hotmail.com>',
        add_help=False)

    parser.add_argument(
        'watch_urls',
        metavar='URL',
        nargs='*',
        help='URL from which to extract mp4 files')

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

    # Logging and input file
    source_group = parser.add_argument_group('Logging and input file')
    output_group = source_group.add_mutually_exclusive_group()
    output_group.add_argument(
        '-o', '--output-file',
        metavar='FILE',
        help='log messages to FILE')
    output_group.add_argument(
        '-a', '--append-output',
        metavar='FILE',
        help='append messages to FILE')
    verbose_group = source_group.add_mutually_exclusive_group()
    verbose_group.add_argument(
        '-d', '--debug',
        action='store_true',
        default=False,
        help='print lots of debug information')
    verbose_group.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help='be verbose')
    verbose_group.add_argument(
        '-q', '--quiet',
        action='store_true',
        default=False,
        help='quiet (no output)')
    source_group.add_argument(
        '-i', '--input-file',
        metavar='FILE',
        help='download URLs found in local or external FILE')

    download_group = parser.add_argument_group('Download')
    download_group.add_argument(
        '-M', '--max-workers',
        type=int,
        default=3,
        help='the upper bound of the number of pools')

    dir_group = parser.add_argument_group('Directories')
    dir_group.add_argument(
        '-P', '--directory-prefix',
        metavar='PREFIX',
        default='.',
        help='save files to PREFIX/..')

    return parser.parse_args(args or [])

def init_logger(args):
    """Initialize local logger (and reset pytube logger)

    Set message format, verbosity, and stream handler to the logger.

    :param args:
        Parsed command line options.
    """

    formatter = pytube_logger.handlers[0].formatter

    logger = logging.getLogger(__name__)

    if args.debug:
        verbosity = logging.DEBUG
    elif args.verbose:
        verbosity = logging.INFO
    elif args.quiet:
        verbosity = logging.FATAL + 1
    else:
        verbosity = logging.WARNING

    if args.output_file:
        handler = logging.FileHandler(
            args.output_file, mode='w', encoding='utf-8', delay=True)
    elif args.append_output:
        handler = logging.FileHandler(
            args.append_output, mode='a', encoding='utf-8', delay=True)
    else:
        # By default, stream is sys.stderr.
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    handler.setLevel(verbosity)
    logger.addHandler(handler)

    logger.setLevel(verbosity)
    pytube_logger.setLevel(verbosity)

    return logger

def get_watch_urls(args):
    """Return watch URLs

    Like GNU wget doing so, <if there are URLs both on the command line and in
    an input file, those on the command lines will be the first ones to be
    retrieved> (GNU wget manual).

    :param args:
        Command line parameters.
    """

    watch_urls = args.watch_urls
    input_file = args.input_file
    if not input_file:
        return watch_urls

    if input_file == '-':
        lines = sys.stdin.read()
    else:
        with open(input_file, 'r') as fin:
            lines = fin.read()

    watch_urls.extend(lines.splitlines())
    return watch_urls

def run(args):
    """main function

    :param args:
        Command line parameters.
    """

    logger = init_logger(args)
    watch_urls = get_watch_urls(args)
    if not watch_urls:
        logger.error('No watch URLs')
        return 1

    async def run_core(watch_urls, pool=None):
        """Concurrently execute `download_media`

        :param watch_urls:
            A list of YouTube watch URLs.
        :param pool:
            An instance of `ThreadPoolExecutor`.
        """

        loop = asyncio.get_running_loop()
        futures = [loop.run_in_executor(
            pool, download_media, watch_url) for watch_url in watch_urls]
        done, pending = await asyncio.wait(
            futures, return_when=asyncio.ALL_COMPLETED)
        logger.debug('done: %s', done)
        logger.debug('pending: %s', pending)

        # TODO: List exit status
        if pending:
            sys.exit(3)
        if [i for i in done if i.exception()]:
            sys.exit(4)

    def download_media(watch_url):
        tube = YouTube(watch_url)
        logger.info('on download: %s', watch_url)

        try:
            media = tube.streams.filter(
                only_audio=True, file_extension='mp4').first()
            title = tube.title
            logger.info(
                'download completed from %s to <%s>',
                watch_url, title)
        except Exception:
            logger.exception('cannot download %s', watch_url)
            raise

        try:
            logger.info('saving <%s>...', title)
            media.download(
                output_path=args.directory_prefix,
                filename=title)
            logger.info('successfully saved <%s>', title)
        except Exception:
            logger.exception(
                '%s is not downloaded', title)
            raise

    with ThreadPoolExecutor(max_workers=args.max_workers) as pool:
        asyncio.run(run_core(watch_urls, pool), debug=args.debug)


def main(args=sys.argv[1:]):
    """main function"""
    sys.exit(run(parse_args(args)))


if __name__ == "__main__":
    main()
