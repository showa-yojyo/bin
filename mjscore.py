#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mjscore.py: Demonstrate docutils.statemachine.

Usage:
  mjscore.py [--help] [--version]
  mjscore.py [--today] [--verbose] [--file FILE]
    [-T | --target <playerspec>]
"""

from argparse import (ArgumentParser, FileType)
from json import dump
from docutils.statemachine import StateMachine
from mjstat import players_default
from mjstat.states import (initial_state, state_classes)
from mjstat.stat import evaluate
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

    return parser

def main():
    """The main function."""

    args = configure().parse_args()

    state_machine = StateMachine(
        state_classes=state_classes,
        initial_state=initial_state)
    state_machine.config = args

    input = args.file
    input_lines = [i.strip() for i in input.readlines()]

    # TODO: (priority: low) Define score model.
    context = {}
    results = state_machine.run(input_lines, context=context)

    if args.verbose:
        print(results)
        dump(context, sys.stdout, ensure_ascii=False, indent=4, sort_keys=True)
        sys.stdout.write("\n")

    state_machine.unlink()

    target_player = args.target_player
    if target_player == 'all':
        for target_player in players_default:
            evaluate(context, target_player)
            output(context, target_player)
    else:
        evaluate(context, target_player)
        output(context, target_player)

def output(game_data, target_player):
    """Show the statistics of the target player."""

    print('Date:', game_data['date'])

    player_data = game_data['player_stats'][target_player]
    target_games = player_data['games']
    if not target_games:
        print('No data.')
        return

    print('Reference period: <{}> - <{}>'.format(
        target_games[0]['started_at'],
        target_games[-1]['finished_at']))

    print('Player data')
    print('  Name:', target_player)
    print('  Number of games:', len(target_games))
    print('  Number of hands:', player_data['count_hands'])

    print('Placings')
    print('  [1st, 2nd, 3rd, 4th]:', player_data['placing_distr'])
    print('  First placing rate: {:.2f}%'.format(player_data['first_placing_rate'] * 100))
    print('  Last placing rate: {:.2f}%'.format(player_data['last_placing_rate'] * 100))
    print('  Mean: {:.2f}th'.format(player_data['mean_placing']))

    print('Winnings')
    print('  Number of winning:', player_data['winning_count'])
    print('  Rate: {:.2f}%'.format(player_data['winning_rate'] * 100))
    print('  Mean: {:.2f}pts.'.format(player_data['winning_mean']))

    print('Losings on discard')
    print('  Number of LOD:', player_data['lod_count'])
    print('  Rate: {:.2f}%'.format(player_data['lod_rate'] * 100))
    print('  Mean: {:.2f}pts.'.format(player_data['lod_mean']))

    print('Riichi data')
    print('  Total:', player_data['riichi_count'])
    print('  Rate: {:.2f}%'.format(player_data['riichi_rate'] * 100))

    print('Melding data')
    print('  Total:', player_data['melding_count'])
    print('  Rate: {:.2f}%'.format(player_data['melding_rate'] * 100))

if __name__ == '__main__':
    main()
