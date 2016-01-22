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
from docutils.statemachine import StateMachine
from os.path import expanduser
from mjstat.model import players_default
from mjstat.states import (initial_state, state_classes)
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
        choices=['all',] + players_default,
        default='あなた',
        help='specify the target player of statistics')

    parser.add_argument(
        '-D', '--debug',
        action='store_true',
        help='for developer\'s use only')

    parser.set_defaults(**defaults)

    return parser.parse_args(remaining_argv)

def main():
    """The main function."""

    args = configure()

    state_machine = StateMachine(
        state_classes=state_classes,
        initial_state=initial_state,
        debug=args.debug and args.verbose)
    state_machine.config = args

    if args.debug:
        from mjstat.testdata import test_input
        input_lines = [i.strip() for i in test_input.split('\n')]
    else:
        input_lines = [i.strip() for i in args.input.readlines()]

    # TODO: (priority: low) Define score model.
    context = {}
    state_machine.run(input_lines, context=context)

    if args.verbose:
        from json import dump
        dump(context, sys.stdout, ensure_ascii=False, indent=4, sort_keys=True)
        sys.stdout.write("\n")

    state_machine.unlink()

    lang = args.language
    target_player = args.target_player
    if target_player == 'all':
        # TODO: Detect all players from game data.
        for target_player in players_default:
            output(context, evaluate(context, target_player), lang)
    else:
        output(context, evaluate(context, target_player), lang)

if __name__ == '__main__':
    main()
