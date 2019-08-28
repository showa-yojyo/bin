#!/usr/bin/env python
"""mjscore.py: Parse mjstat.txt and produce some statistics.

Usage:
  mjscore.py [--help] [--version]
  mjscore.py [--today] [--verbose] [--input <FILE> ...]
    [-l | --language <langspec>]
    [-T | --target <playerspec>]
    [-c | --config <FILE>]
"""

from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path
import sys
from docutils.io import (StringInput, FileInput, FileOutput)
from mjstat.reader import MJScoreReader
from mjstat.parser import MJScoreParser
from mjstat.writer import MJScoreWriter
from mjstat.model import (apply_transforms, merge_games)

__version__ = '0.0.0'

def parse_args(args):
    """Convert argument strings to objects."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-c', '--config',
        metavar='FILE',
        help='path to config file')

    args, remaining_argv = parser.parse_known_args()

    defaults = {}
    config = ConfigParser()
    config.read(args.config if args.config else Path.home() / '.mjscore')

    try:
        defaults = dict(config.items("General"))
    except Exception as ex:
        print(f'Warning: {ex}', file=sys.stderr)

    parser = ArgumentParser(
        parents=[parser],
        description='A simple parser for mjscore.txt.')

    parser.add_argument('--version', action='version', version=__version__)

    # This parameter should not be optional.
    parser.add_argument(
        '--input',
        nargs='+',
        metavar='FILE',
        help='path to mjscore.txt')

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='enable verbose mode')

    parser.add_argument(
        '-l', '--language',
        default='en',
        help='set the language (ISO 639-1) for output')

    group = parser.add_argument_group('reference period')
    group.add_argument(
        '--today',
        action='store_true',
        help='set reference period to today')

    group.add_argument(
        '--since', '--after',
        dest='since',
        metavar='<date>',
        help='analyze statistics more recent than a specific date')

    group.add_argument(
        '--until', '--before',
        dest='until',
        metavar='<date>',
        help='analyze statistics older than a specific date')

    parser.add_argument(
        '-T', '--target-player',
        default='あなた',
        help='specify the target player of statistics')

    parser.add_argument(
        '-F', '--fundamental',
        action='store_true',
        help='produce fundamental statistics')

    parser.add_argument(
        '-Y', '--yaku',
        action='store_true',
        help='produce frequency of yaku')

    parser.add_argument(
        '-D', '--debug',
        action='store_true',
        help='for developer\'s use only')

    parser.set_defaults(**defaults)

    return parser.parse_args(args=remaining_argv or ('--help',))

def run(args):
    """The main function."""

    sources = []
    if args.debug:
        from mjstat.testdata import TEST_INPUT
        sources.append(StringInput(source=TEST_INPUT))
    else:
        # XXX
        if isinstance(args.input, (list, tuple)):
            sources.extend(FileInput(
                source_path=i,
                encoding='sjis',
                mode='r') for i in args.input)
        else:
            sources.append(FileInput(
                source_path=args.input,
                encoding='sjis',
                mode='r'))

    parser = MJScoreParser()
    reader = MJScoreReader()

    game_data_list = tuple(reader.read(i, parser, args) for i in sources)
    game_data = merge_games(game_data_list)
    apply_transforms(game_data)

    writer = MJScoreWriter()
    writer.write(game_data, FileOutput(None))

def main(args=sys.argv[1:]):
    sys.exit(run(parse_args(args=args)))

if __name__ == '__main__':
    main()
