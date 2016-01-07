#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mjscore.py: Demonstrate docutils.statemachine.

Usage:
  mjscore.py [--help] [--version]
  mjscore.py [--verbose] [--file FILE]
"""

from argparse import (ArgumentParser, FileType)
from datetime import datetime
from json import dump
from docutils.statemachine import (State, StateMachine)
import re
import sys

__version__ = '0.0.0'

mjscore_path_default = r'D:\Program Files\mattari09\mjscore.txt'

datetime_format = r'%Y/%m/%d %H:%M'

# TODO: rotation_end
# TODO: (priority: low) rotation_starting_hand(s)
# TODO: (priority: low) rotation_dora
# TODO: (priority: low) rotation_discards

class MJScoreState(State):
    """Base class of state classes."""

    def bof(self, context):
        """Called at the beginning of data."""
        assert isinstance(context, dict)

        context['description'] = 'A demonstration of docutils.statemachine.'
        context['date'] = datetime.today().strftime(datetime_format)
        context['games'] = []
        return context, []

    @property
    def config(self):
        """Return the configuration."""
        return self.state_machine.config

beginning_of_game_re = re.compile(r'''
=*\s
東風戦：ランキング卓\s64卓\s開始\s
(?P<timestamp>
\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}
)\s
=*''', re.VERBOSE)

class GameBeginningState(MJScoreState):
    """Parse the first line of a game."""

    patterns = dict(
        beginning_of_game=beginning_of_game_re,)

    initial_transitions = ['beginning_of_game',]

    def beginning_of_game(self, match, context, next_state):
        """Parse the beginning of a game."""

        started_at = match.group('timestamp')
        if self.config.today:
            # Determine whether to parse this game or not.
            today = context['date']

            # Compare two 'YYYY/MM/DD's.
            if started_at.split()[0] != today.split()[0]:
                return context, next_state, []

        next_state = 'RotationState'
        game = dict(
            result=[None] * 4,
            rotations=[],)
        context['games'].append(game)

        game['started_at'] = started_at

        return context, next_state, []

# 場 = round
# 局 = rotation
# 本場 = counter(s)
# E.g. 東一局三本場 is translated to
#   East round, 1st rotation [with 0 counters]
rotation_header_re = re.compile(r'''
(?P<title>[東南][1-4]局\s\d本場)
\(リーチ\d\)
\s
(?P<balance>
 (
  (あなた|下家|対面|上家)\s?
  ([+-]?\d+)\s?
 ){,4}
)
''', re.VERBOSE)

end_of_rotations_re = re.compile(r'[-]+\s*試合結果\s*[-]+')

class RotationState(MJScoreState):
    """Parse almost all of lines of rotations."""

    patterns = dict(
        rotation_header=rotation_header_re,
        end_of_rotations=end_of_rotations_re,)

    initial_transitions = [
        'rotation_header',
        'end_of_rotations']

    def rotation_header(self, match, context, next_state):
        """Parse the header of a rotation."""

        game = context['games'][-1]
        rotations = game['rotations']
        rotation = dict(
            title=match.group('title'))

        player_and_balance = match.group('balance').strip().split()
        rotation['balance'] = [
            dict(player=player_and_balance[i],
                 balance=player_and_balance[i + 1],)
            for i in range(0, len(player_and_balance), 2)]

        rotations.append(rotation)

        return context, next_state, []

    def end_of_rotations(self, match, context, next_state):
        """---- game result ----"""

        return context, 'GameEndingState', []

ending_of_game_re = re.compile(r'''
[-]*\s64卓\s終了\s
(?P<timestamp>
\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}
)
\s
[-]*
''', re.VERBOSE)

result_of_game_re = re.compile(r'''
(?P<rank>[1-4])位
\s+
(?P<player>(あなた|下家|対面|上家))
\s+
(?P<points>[+-]?\d+)
''', re.VERBOSE)

class GameEndingState(MJScoreState):
    """Parse the last lines of a game"""

    patterns = dict(
        ending_of_game=ending_of_game_re,
        result_of_game=result_of_game_re,)

    initial_transitions = [
        'ending_of_game',
        'result_of_game',]

    def result_of_game(self, match, context, next_state):
        """Parse a rank line of the ranking list in a game."""

        game = context['games'][-1]
        ranking = game['result']

        rank = int(match.group('rank'))
        player = match.group('player')
        points = int(match.group('points'))
        ranking[rank - 1] = dict(player=player, points=points)

        return context, next_state, []

    def ending_of_game(self, match, context, next_state):
        """Parse the ending of a game."""

        game = context['games'][-1]
        game['finished_at'] = match.group('timestamp')

        next_state = 'GameBeginningState'
        return context, next_state, []

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

    return parser

def main():
    """The main function."""

    args = configure().parse_args()

    state_machine = StateMachine(
        state_classes=[GameBeginningState,
                       RotationState,
                       GameEndingState,],
        initial_state='GameBeginningState')
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

    stat(context)
    output(context)

def stat(game_data):
    """under construction"""

    placing_distr = [0, 0, 0, 0]

    all_games = game_data['games']
    for game in all_games:
        ranking = game['result']
        for i in range(4):
            if ranking[i]['player'] ==  'あなた':
                placing_distr[i] += 1
                break

    game_data['your_placing_distr'] = placing_distr

    # Calculate mean placing.
    num_games = len(all_games)
    if num_games:
        game_data['your_mean_placing'] = sum(
            (v*i) for i, v in enumerate(placing_distr, 1)) / num_games
    else:
        game_data['your_mean_placing'] = None

    # TODO: Implement more features.

def output(game_data):
    """under construction"""

    print('Date:', game_data['date'])

    all_games = game_data['games']
    if not all_games:
        print('No data.')
        return

    print('Reference period: <{}> - <{}>'.format(
        all_games[0]['started_at'],
        all_games[-1]['finished_at']))

    print('Number of games:', len(all_games))
    print('Your placing distribution [1st, 2nd, 3rd, 4th]:',
          game_data['your_placing_distr'])
    print('Mean placing: {:.2f}'.format(game_data['your_mean_placing']))

if __name__ == '__main__':
    main()
