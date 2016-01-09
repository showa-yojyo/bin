#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mjscore.py: Demonstrate docutils.statemachine.

Usage:
  mjscore.py [--help] [--version]
  mjscore.py [--today] [--verbose] [--file FILE]
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
\s?
(?P<balance>
 (
  (あなた|下家|対面|上家)\s?
  ([+-]?\d+)\s?
 ){,4}
)?
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
        if player_and_balance:
            rotation['balance'] = [
                dict(player=player_and_balance[i],
                     balance=int(player_and_balance[i + 1]),)
                for i in range(0, len(player_and_balance), 2)]
        else:
            rotation['balance'] = []

        rotations.append(rotation)

        return context, 'RotationEndingState', []

    def end_of_rotations(self, match, context, next_state):
        """---- game result ----"""

        return context, 'GameEndingState', []

# provisional
winning_re = re.compile(r'''
\A
(?P<winning_value>.+)
(?P<winning_decl>(ロン|ツモ))
(?P<winning_yaku_list>.+)
\Z
''', re.VERBOSE)

# TODO: canonical representation of 四槓開
draw_re = re.compile(r'(流局|四風連打|九種公九牌倒牌|四家リーチ|(四槓.+)|三家和)')

class RotationEndingState(MJScoreState):
    """Parse the line that tells the winner's hand or
    exhaustive/abortive draw.
    """

    patterns = dict(
        winning = winning_re,
        draw = draw_re,)

    initial_transitions = [
        'winning',
        'draw',]

    def winning(self, match, context, next_state):
        """Parse the line that includes ロン or ツモ."""

        # Get the current rotation from context.
        game = context['games'][-1]
        rotation = game['rotations'][-1]

        rotation['ending'] = match.group('winning_decl')

        # provisional
        rotation['winning_value'] = match.group('winning_value')
        rotation['winning_yaku_list'] = match.group('winning_yaku_list')#split()

        return context, 'RotationState', []

    def draw(self, match, context, next_state):
        """Parse the line that includes 流局, etc."""

        # Get the current rotation from context.
        game = context['games'][-1]
        rotation = game['rotations'][-1]

        rotation['ending'] = match.group()

        return context, 'RotationState', []

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
                       RotationEndingState,
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

def enumerate_rotations(game_data):
    for game in game_data['games']:
        for rot in game['rotations']:
            yield rot

def stat(game_data):
    """under construction"""

    all_games = game_data['games']

    num_rotations = sum(len(game['rotations']) for game in all_games)
    game_data['count_rotations'] = num_rotations

    # Calculate distribution of your placing, or 着順表.
    placing_distr = [0, 0, 0, 0]
    for game in all_games:
        ranking = game['result']
        for i in range(4):
            if ranking[i]['player'] ==  'あなた':
                placing_distr[i] += 1
                break

    game_data['your_placing_distr'] = placing_distr

    # Calculate statistical values about your placing.
    num_games = len(all_games)
    game_data['your_mean_placing'] = None
    game_data['your_first_placing_rate'] = None
    game_data['your_last_placing_rate'] = None
    if num_games:
        game_data['your_mean_placing'] = sum(
            (v*i) for i, v in enumerate(placing_distr, 1)) / num_games

        game_data['your_first_placing_rate'] = placing_distr[0] / num_games
        game_data['your_last_placing_rate'] = placing_distr[-1] / num_games

    # Calculate your winning rate, or 和了率.
    num_your_winning = 0
    for rot in enumerate_rotations(game_data):
        if rot['ending'] in ('ツモ', 'ロン'):
            assert rot['balance']
            first = rot['balance'][0]
            if (first['player'] == 'あなた' and
                first['balance'] > 0):
                num_your_winning += 1

    game_data['count_your_winning'] = num_your_winning
    game_data['your_winning_rate'] = 0
    if num_rotations:
        game_data['your_winning_rate'] = num_your_winning / num_rotations

    # Calculate your losing-on-discarding (LOD) rate and mean LOD,
    # or 放銃率 and 平均放銃率.
    num_your_lod = 0
    total_losing_points = 0
    for rot in enumerate_rotations(game_data):
        if rot['ending'] == 'ロン':
            assert rot['balance']
            last = rot['balance'][-1]
            if last['player'] == 'あなた':
                num_your_lod += 1
                total_losing_points += last['balance'] # negative value

    game_data['count_your_lod'] = num_your_lod
    game_data['your_lod_rate'] = None
    game_data['your_lod_mean'] = None
    if num_rotations:
        game_data['your_lod_rate'] = num_your_lod / num_rotations
        if num_your_lod:
            game_data['your_lod_mean'] = total_losing_points / num_your_lod

    # TODO: Implement more statistical values, thus:
    # * your riichi rate, or 立直率
    # * your melding rate, or 副露率
    # * mean of your winning points, or 平均和了点
    # * (challenge) 平均獲得チップ枚数

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
    print('Number of rotations:', game_data['count_rotations'])

    print('Your placings')
    print('  Histogram [1st, 2nd, 3rd, 4th]:', game_data['your_placing_distr'])
    print('  First placing rate: {:.2f}%'.format(game_data['your_first_placing_rate'] * 100))
    print('  Last placing rate:  {:.2f}%'.format(game_data['your_last_placing_rate'] * 100))
    print('  Mean placing:       {:.2f}th'.format(game_data['your_mean_placing']))

    print('Your winnings')
    print('  Number of winning:', game_data['count_your_winning'])
    print('  Winning rate: {:.2f}%'.format(game_data['your_winning_rate'] * 100))

    print('Your losings on discard')
    print('  Number of LOD:', game_data['count_your_lod'])
    print('  LOD rate: {:.2f}%'.format(game_data['your_lod_rate'] * 100))
    print('  LOD mean: {:.2f}pts.'.format(game_data['your_lod_mean']))

if __name__ == '__main__':
    main()
