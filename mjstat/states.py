# -*- coding: utf-8 -*-
"""states.py:
"""

from datetime import datetime
import re
from docutils.statemachine import State
from . import players_default

# TODO: (priority: low) hand_starting_hand(s)
# TODO: (priority: low) hand_dora

datetime_format = r'%Y/%m/%d %H:%M'

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
            melding_counter_table=[0] * 4,
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
        melding_counter_table = hand['melding_counter_table']

        for action in actions:
            assert len(action) > 1
            assert action[0] in '1234'
            assert action[1] in 'ACDGKNRd'

            # Test if the action is riichi.
            if action[1] == 'R':
                riichi_table[int(action[0]) - 1] = True
            elif action[1] in 'CKN':
                index = int(action[0]) - 1
                melding_counter_table[index] += 1

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

# The following values are to be passed to the constructor of
# class StateMachine as its keyword arguments.
initial_state = 'GameBeginningState'
state_classes = MJScoreState.__subclasses__()
