#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mjscore.py: Parse mjstat.txt and produce some statistics.

Usage:
  mjscore.py [--help] [--version]
  mjscore.py [--today] [--verbose] [--input <FILE>]
    [-l | --language <langspec>]
    [-T | --target <playerspec>]
    [-c | --config <FILE>]
"""

from argparse import (ArgumentParser, FileType)
from configparser import (ConfigParser, Error)
from os.path import expanduser
from mjstat.states import parse_mjscore
from mjstat.stat import evaluate
from mjstat.translator import output
import sys

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
    except Error as e:
        print('Warning: {}'.format(e), file=sys.stderr)

    parser = ArgumentParser(
        parents=[parser],
        description='A simple parser for mjscore.txt.')

    parser.add_argument('--version', action='version', version=__version__)

    # This parameter should not be optional.
    parser.add_argument(
        '--input',
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

    # TODO: (priority: high) reference period as a parameter
    parser.add_argument(
        '--today',
        action='store_true',
        help='set reference period to today')

    parser.add_argument(
        '-T', '--target-player',
        default='あなた',
        help='specify the target player of statistics')

    parser.add_argument(
        '--fundamental',
        action='store_true',
        help='produce fundamental statistics')

    parser.add_argument(
        '--yaku',
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

    args = configure()

    if args.debug:
        from mjstat.testdata import test_input
        input_lines = [i.strip() for i in test_input.split('\n')]
    else:
        input_lines = [i.strip() for i in args.input.readlines()]

    game_data = parse_mjscore(input_lines, args)

    if args.verbose:
        from json import dump
        dump(game_data, sys.stdout, ensure_ascii=False, indent=4, sort_keys=True)
        sys.stdout.write("\n")

    lang_code = args.language
    target_player = args.target_player

    stat_options = dict(fundamental=args.fundamental,
                        yaku=args.yaku)

    if target_player == 'all':
        # Detect all players from game data.
        player_names = set()
        for game in game_data['games']:
            player_names = player_names.union(game['players'])

        for target_player in player_names:
            output(evaluate(game_data, target_player, **stat_options), lang_code)
    else:
        output(evaluate(game_data, target_player, **stat_options), lang_code)

if __name__ == '__main__':
    main()
