#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mjscore.py: Demonstrate docutils.statemachine.

Usage:
  mjscore.py [--help] [--version]
  mjscore.py [--today] [--verbose] [--file FILE]
    [-l | --language <langspec>]
    [-T | --target <playerspec>]
"""

from argparse import (ArgumentParser, FileType)
from docutils.statemachine import StateMachine
from mjstat.model import players_default
from mjstat.states import (initial_state, state_classes)
from mjstat.stat import evaluate
from mjstat.translator import output
import sys

__version__ = '0.0.0'

mjscore_path_default = r'D:\Program Files\mattari09\mjscore.txt'

def configure():
    """Return a command line parser."""

    parser = ArgumentParser(
        description='Demonstrate docutils.statemachine.')
    parser.add_argument('--version', action='version', version=__version__)

    # This parameter should not be optional.
    parser.add_argument(
        '--file',
        default=mjscore_path_default,
        type=FileType(mode='r', encoding='sjis'),
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

    return parser

def main():
    """The main function."""

    args = configure().parse_args()

    state_machine = StateMachine(
        state_classes=state_classes,
        initial_state=initial_state,
        debug=args.debug and args.verbose)
    state_machine.config = args

    if args.debug:
        from mjstat.testdata import test_input
        input_lines = [i.strip() for i in test_input.split('\n')]
    else:
        input_lines = [i.strip() for i in args.file.readlines()]

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
