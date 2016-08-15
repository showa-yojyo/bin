#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mjscore.py: Parse mjstat.txt and produce some statistics.

Usage:
  mjscore.py [--help] [--version]
  mjscore.py [--today] [--verbose] [--input <FILE> ...]
    [-l | --language <langspec>]
    [-T | --target <playerspec>]
    [-c | --config <FILE>]
"""

from argparse import (ArgumentParser, FileType)
from configparser import (ConfigParser, Error)
from os.path import expanduser
import sys
from docutils.io import (StringInput, FileInput, FileOutput)
from mjstat.reader import MJScoreReader
from mjstat.parser import MJScoreParser
from mjstat.writer import MJScoreWriter
from mjstat.model import (apply_transforms, merge_games)

__version__ = '0.0.0'

def configure():
    """Configuration of this application."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '-c', '--config',
        type=FileType(mode='r', encoding='utf-8'),
        metavar='FILE',
        help='path to config file')

    args, remaining_argv = parser.parse_known_args()

    defaults = {}
    config = ConfigParser()
    if args.config:
        config.read_file(args.config)
    else:
        default_config_path = expanduser('~/.mjscore')
        config.read(default_config_path)

    try:
        defaults = dict(config.items("General"))
    except Error as ex:
        print('Warning: {}'.format(ex), file=sys.stderr)

    parser = ArgumentParser(
        parents=[parser],
        description='A simple parser for mjscore.txt.')

    parser.add_argument('--version', action='version', version=__version__)

    # This parameter should not be optional.
    parser.add_argument(
        '--input',
        nargs='+',
        type=FileType(mode='r', encoding='sjis'),
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

    return parser.parse_args(remaining_argv)

def main():
    """The main function."""

    settings = configure()
    sources = []

    if settings.debug:
        from mjstat.testdata import TEST_INPUT
        sources.append(StringInput(source=TEST_INPUT))
    else:
        # XXX
        if isinstance(settings.input, (list, tuple)):
            sources.extend(FileInput(source=i) for i in settings.input)
        else:
            sources.append(FileInput(source=settings.input))

    parser = MJScoreParser()
    reader = MJScoreReader()

    game_data_list = tuple(reader.read(i, parser, settings) for i in sources)
    game_data = merge_games(game_data_list)
    apply_transforms(game_data)

    writer = MJScoreWriter()
    writer.write(game_data, FileOutput(None))

if __name__ == '__main__':
    main()
