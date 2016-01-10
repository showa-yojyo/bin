#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mjscore.py: Demonstrate docutils.statemachine.

Usage:
  mjscore.py [--help] [--version]
  mjscore.py [--today] [--verbose] [--file FILE]
    [-T | --target <playerspec>]
"""

from argparse import (ArgumentParser, FileType)
from datetime import datetime
from json import dump
from docutils.statemachine import (State, StateMachine)
import re
import sys

__version__ = '0.0.0'

mjscore_path_default = r'D:\Program Files\mattari09\mjscore.txt'
players_default = ['あなた', '下家', '対面', '上家']
datetime_format = r'%Y/%m/%d %H:%M'

# TODO: (priority: low) hand_starting_hand(s)
# TODO: (priority: low) hand_dora

class MJScoreState(State):
    """Base class of state classes."""

    def bof(self, context):
        """Called at the beginning of data."""
        assert isinstance(context, dict)

        context['description'] = 'A demonstration of docutils.statemachine.'
        context['date'] = datetime.today().strftime(datetime_format)
        context['games'] = []
        context['player_stats'] = dict(names=players_default)
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

        next_state = 'HandState'
        game = dict(
            result=[None] * 4,
            hands=[],)
        context['games'].append(game)

        game['started_at'] = started_at

        return context, next_state, []

# 場 = a round
# 局 = a hand
# 本場 = counter(s)
# E.g. 東一局三本場 is translated to
#   East round, 1st hand (or rotation) [with 0 counters]
hand_header_re = re.compile(r'''
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

# Regex for lines e.g. ``* 1G3s 1d1p 2G2s 2d9p ...``
# Do not make regex so complicated here.
actions_re = re.compile(r'''
\A
\*\s*
(?P<actions>.+)
\Z
''', re.VERBOSE)

empty_re = re.compile(r'\Z')

end_of_game_re = re.compile(r'[-]+\s*試合結果\s*[-]+')

class HandState(MJScoreState):
    """Parse almost all of lines of hands."""

    patterns = dict(
        hand_header=hand_header_re,
        player_actions=actions_re,
        end_of_actions=empty_re,
        end_of_game=end_of_game_re,)

    initial_transitions = [
        'hand_header',
        'player_actions',
        'end_of_game']

    def hand_header(self, match, context, next_state):
        """Parse the header of a hand."""

        game = context['games'][-1]
        hands = game['hands']
        hand = dict(
            title=match.group('title'),
            riichi_table=[False] * 4,)

        player_and_balance = match.group('balance').strip().split()
        if player_and_balance:
            hand['balance'] = [
                dict(player=player_and_balance[i],
                     balance=int(player_and_balance[i + 1]),)
                for i in range(0, len(player_and_balance), 2)]
        else:
            hand['balance'] = []

        hands.append(hand)

        return context, 'HandEndingState', []

    def player_actions(self, match, context, next_state):
        """Handle a line which describes a part of all players' actions."""

        # current hand
        hand = context['games'][-1]['hands'][-1]
        riichi_table = hand['riichi_table']

        actions = match.group('actions').split()
        for action in actions:
            assert len(action) > 1
            assert action[0] in '1234'
            assert action[1] in 'ACDGKNRd'

            # Test if the action is riichi.
            if action[1] == 'R':
                riichi_table[int(action[0]) - 1] = True

        return context, next_state, []

    def end_of_actions(self, match, context, next_state):
        """The empty line immediately after action lines."""

        return context, next_state, []

    def end_of_game(self, match, context, next_state):
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

class HandEndingState(MJScoreState):
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

        # Get the current hand from context.
        game = context['games'][-1]
        hand = game['hands'][-1]

        hand['ending'] = match.group('winning_decl')

        # provisional
        hand['winning_value'] = match.group('winning_value')
        hand['winning_yaku_list'] = match.group('winning_yaku_list')#split()

        return context, 'HandState', []

    def draw(self, match, context, next_state):
        """Parse the line that includes 流局, etc."""

        # Get the current hand from context.
        game = context['games'][-1]
        hand = game['hands'][-1]

        hand['ending'] = match.group()

        return context, 'HandState', []

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
        state_classes=[GameBeginningState,
                       HandState,
                       HandEndingState,
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

    target_player = args.target_player
    if target_player == 'all':
        for target_player in players_default:
            stat(context, target_player)
            output(context, target_player)
    else:
        stat(context, target_player)
        output(context, target_player)

def enumerate_hands(game_data):
    for game in game_data['games']:
        for rot in game['hands']:
            yield rot

def stat(game_data, target_player):
    """Calculate possibly numerous statistical values."""

    all_games = game_data['games']
    player_index = game_data['player_stats']['names'].index(target_player)

    num_hands = sum(len(game['hands']) for game in all_games)
    game_data['count_hands'] = num_hands

    # Calculate distribution of target player's placing, or 着順表.
    placing_distr = [0, 0, 0, 0]
    for game in all_games:
        ranking = game['result']
        for i in range(4):
            if ranking[i]['player'] == target_player:
                placing_distr[i] += 1
                break

    player_data = {}
    game_data['player_stats'].update({target_player:player_data})

    player_data['placing_distr'] = placing_distr

    # Calculate statistical values about target player's placing.
    num_games = len(all_games)
    player_data['mean_placing'] = 0
    player_data['first_placing_rate'] = 0
    player_data['last_placing_rate'] = 0
    if num_games:
        player_data['mean_placing'] = sum(
            (v*i) for i, v in enumerate(placing_distr, 1)) / num_games

        player_data['first_placing_rate'] = placing_distr[0] / num_games
        player_data['last_placing_rate'] = placing_distr[-1] / num_games

    # Calculate target player's winning rate, or 和了率.
    num_winning = 0
    total_points = 0
    for hand in enumerate_hands(game_data):
        if hand['ending'] in ('ツモ', 'ロン'):
            assert hand['balance']
            first = hand['balance'][0]
            points = first['balance']
            if (first['player'] == target_player and
                points > 0):
                total_points += points
                num_winning += 1

    player_data['count_winning'] = num_winning
    player_data['winning_rate'] = 0
    player_data['winning_mean'] = 0
    if num_hands and num_winning:
        player_data['winning_rate'] = num_winning / num_hands
        player_data['winning_mean'] = total_points / num_winning

    # Calculate target player's losing-on-discarding (LOD) rate and mean LOD,
    # or 放銃率 and 平均放銃率.
    num_lod = 0
    total_losing_points = 0
    for hand in enumerate_hands(game_data):
        if hand['ending'] == 'ロン':
            assert hand['balance']
            last = hand['balance'][-1]
            if last['player'] == target_player:
                num_lod += 1
                total_losing_points += last['balance'] # sum of negative values

    player_data['count_lod'] = num_lod
    player_data['lod_rate'] = 0
    player_data['lod_mean'] = 0
    if num_hands and num_lod:
        player_data['lod_rate'] = num_lod / num_hands
        player_data['lod_mean'] = total_losing_points / num_lod

    # TODO: Implement more statistical values, thus:
    # * your melding rate, or 副露率
    # * (challenge) 平均獲得チップ枚数

    # Calculate riichi rate.
    player_data['riichi_rate'] = 0
    if num_hands:
        num_riichi = 0
        for hand in enumerate_hands(game_data):
            riichi_table = hand['riichi_table']
            if riichi_table[player_index]:
                num_riichi += 1

        player_data['riichi_rate'] = num_riichi / num_hands

def output(game_data, target_player):
    """Show the statistics of the target player."""

    print('Date:', game_data['date'])

    all_games = game_data['games']
    if not all_games:
        print('No data.')
        return

    print('Reference period: <{}> - <{}>'.format(
        all_games[0]['started_at'],
        all_games[-1]['finished_at']))

    print('Number of games:', len(all_games))
    print('Number of hands:', game_data['count_hands'])

    player_data = game_data['player_stats'][target_player]

    print('Player {} data: '.format(target_player))

    print('Placings')
    print('  Histogram [1st, 2nd, 3rd, 4th]:', player_data['placing_distr'])
    print('  First placing rate: {:.2f}%'.format(player_data['first_placing_rate'] * 100))
    print('  Last placing rate: {:.2f}%'.format(player_data['last_placing_rate'] * 100))
    print('  Mean: {:.2f}th'.format(player_data['mean_placing']))

    print('Winnings')
    print('  Number of winning:', player_data['count_winning'])
    print('  Rate: {:.2f}%'.format(player_data['winning_rate'] * 100))
    print('  Mean: {:.2f}pts.'.format(player_data['winning_mean']))

    print('Losings on discard')
    print('  Number of LOD:', player_data['count_lod'])
    print('  Rate: {:.2f}%'.format(player_data['lod_rate'] * 100))
    print('  Mean: {:.2f}pts.'.format(player_data['lod_mean']))

    print('Riichi rate: {:.2f}%'.format(player_data['riichi_rate'] * 100))

if __name__ == '__main__':
    main()
