#!/usr/bin/env python
"""
SKELETON
"""

from argparse import ArgumentParser
import logging
import sys

__version__ = '1.0.0'

def parse_args(args):
    """Parse the command line parameters.

    Most options are taken from GNU wget.

    :param args:
        Raw command line arguments.

    :rtype: argparse.Namespace
    """

    parser = ArgumentParser(
        description='SKELETON',
        epilog='Mail bug reports and suggestions to <yojyo@hotmail.com>',
        add_help=False)

    parser.add_argument(
        'main_args',
        metavar='SKELETON',
        nargs='*',
        help='SKELETON')

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

    return parser.parse_args(args or [])

def init_logger(args):
    """Initialize local logger (and reset pytube logger)

    Set message format, verbosity, and stream handler to the logger.

    :param args:
        Parsed command line options.
    """

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

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(verbosity)
    logger.addHandler(handler)
    logger.setLevel(verbosity)

    return logger

def get_main_args(args):
    """Return main arguments

    :param args:
        Command line parameters.
    """

    main_args = args.main_args
    input_file = args.input_file
    if not input_file:
        return main_args

    if input_file == '-':
        lines = sys.stdin.read()
    else:
        with open(input_file, 'r') as fin:
            lines = fin.read()

    main_args.extend(lines.splitlines())
    return main_args

def run(args):
    """main function

    :param args:
        Command line parameters.
    """

    logger = init_logger(args)
    main_args = get_main_args(args)
    if not main_args:
        logger.error('No arguments provided')
        return 1

    # SKELETON
    print(' '.join(main_args))

    return 0

def main(args=sys.argv[1:]):
    """main function"""
    sys.exit(run(parse_args(args)))

if __name__ == "__main__":
    main()
