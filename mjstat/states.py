# -*- coding: utf-8 -*-
"""states.py:
"""

from datetime import datetime
import re
from docutils.statemachine import State
from . import players_default

datetime_format = r'%Y/%m/%d %H:%M'

class MJScoreState(State):
    """Base class of state classes."""

    def bof(self, context):
        """Called at the beginning of data."""
        assert isinstance(context, dict)

        context['description'] = 'A demonstration of docutils.statemachine.'
        context['date'] = datetime.today().strftime(datetime_format)
        context['games'] = []
        context['player_stats'] = {}
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

        next_state = 'GameHeaderState'
        game = dict(
            result=[None] * 4,
            hands=[],
            players=[None] * 4)
        context['games'].append(game)

        game['started_at'] = started_at

        return context, next_state, []

# Regex for parsing players information, their names and ratings.
game_header_re = re.compile(r'''
持点\d+\s*      # 25000
\[1\](.+)\sR(?:\d+)\s*   # Player #1
\[2\](.+)\sR(?:\d+)\s*   # Player #2
\[3\](.+)\sR(?:\d+)\s*   # Player #3
\[4\](.+)\sR(?:\d+)\s*   # Player #4
''', re.VERBOSE)

class GameHeaderState(MJScoreState):
    """Parse the second line of a game."""

    patterns = dict(
        game_header=game_header_re,)

    initial_transitions = ['game_header',]

    def game_header(self, match, context, next_state):
        """Parse player names."""

        game = context['games'][-1]
        game['players'] = [i for i in match.groups()]

        return context, 'HandState', []

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

# Regex for a start hand, or a players' dealt tiles at the
# beginning of a hand.
start_hand_re = re.compile(r'''
\[
  (?P<id>[1-4])                 # player id
  (?P<seat>[東南西北])          # seat
\]
(?P<start_hand>
    (
        ([1-9]m)|           # character suit, or 萬子
        (5M)|
        ([1-9]p)|           # circle suit, or 筒子
        (5P)|
        ([1-9]s)|           # bamboo suit, or 索子
        (5S)|
        ([東南西北白発中])  # honor tiles, or 字牌
    ){13}
)                   # 13 tiles of a start hand, or 配牌
''', re.VERBOSE)

# Regex for the line that indicates all of dora tiles.
dora_list_re = re.compile(r'''
\[表ドラ\](?P<dora>[^\s]+)               # XXX: dot matches any of tiles
(\s*\[裏ドラ\](?P<uradora>.+))?      # XXX: dot matches any of tiles
''', re.VERBOSE)

# Regex for lines e.g. ``* 1G3s 1d1p 2G2s 2d9p ...``
# Do not make regex so complicated here.
actions_re = re.compile(r'''
\A
\*\s*
(?P<actions>.+)
\Z
''', re.VERBOSE)

end_of_game_re = re.compile(r'[-]+\s*試合結果\s*[-]+')

class HandState(MJScoreState):
    """Parse almost all of lines of hands."""

    patterns = dict(
        hand_header=hand_header_re,
        start_hand=start_hand_re,
        dora_list=dora_list_re,
        player_actions=actions_re,
        end_of_game=end_of_game_re,)

    initial_transitions = [
        'hand_header',
        'start_hand',
        'dora_list',
        'player_actions',
        'end_of_game']

    def hand_header(self, match, context, next_state):
        """Parse the header of a hand."""

        game = context['games'][-1]
        hands = game['hands']
        hand = dict(
            title=match.group('title'),
            action_table=[],
            riichi_table=[False] * 4,
            seat_table=[None] * 4,
            start_hand_table=[None] * 4,
            dora_table=[],
            chows=[],
            pungs=[],
            kongs=[],)

        hand['balance'] = {}
        player_and_balance = match.group('balance').strip().split()
        if player_and_balance:
            hand['balance'].update([(
                player_and_balance[i], int(player_and_balance[i + 1]),)
                    for i in range(0, len(player_and_balance), 2)])
        hands.append(hand)

        return context, 'HandEndingState', []

    def start_hand(self, match, context, next_state):
        """Handle lines of start hands."""

        # current hand
        game = context['games'][-1]
        hand = game['hands'][-1]

        player, seat, start_hand = match.group('id', 'seat', 'start_hand')
        index = int(player) - 1
        hand['seat_table'][index] = seat
        hand['start_hand_table'][index] = start_hand

        for i in range(3):
            m = start_hand_re.match(
                self.state_machine.next_line())
            player, seat, start_hand = m.group('id', 'seat', 'start_hand')
            index = int(player) - 1
            hand['seat_table'][index] = seat
            hand['start_hand_table'][index] = start_hand

        return context, next_state, []

    def dora_list(self, match, context, next_state):
        """Handle the line of dora tiles."""

        # current hand
        game = context['games'][-1]
        hand = game['hands'][-1]
        dora_table = hand['dora_table']

        dora_table.extend(match.group('dora', 'uradora'))

        return context, next_state, []

    def player_actions(self, match, context, next_state):
        """Handle a line which describes a part of all players' actions."""

        # current hand
        game = context['games'][-1]
        hand = game['hands'][-1]
        action_table = hand['action_table']

        actions = match.group('actions').split()
        action_table.extend(actions)

        while True:
            line = self.state_machine.next_line()
            match = actions_re.match(line)
            if not match:
                self.end_of_actions(context)
                break
            actions = match.group('actions').split()
            action_table.extend(actions)

        return context, next_state, []

    def end_of_actions(self, context):
        """The empty line immediately after action lines."""

        # current hand
        game = context['games'][-1]
        hand = game['hands'][-1]
        riichi_table = hand['riichi_table']

        actions = hand['action_table']
        chows = [[] for i in range(4)]
        pungs = [[] for i in range(4)]
        kongs = [[] for i in range(4)]

        for i, action in enumerate(actions):
            assert len(action) > 1
            index, action_type = action[0], action[1]
            assert index in '1234'
            assert action_type in 'ACDGKNRd'
            index = int(index) - 1

            prev_action = actions[i - 1] if i > 0 else None

            # Test if the action is riichi.
            if action_type == 'R':
                riichi_table[index] = True
                continue
            elif action_type == 'C':
                assert prev_action
                chows[index].append(prev_action[2:] + action[2:])
                continue
            elif action_type == 'N':
                assert prev_action
                pungs[index].append(prev_action[2:])
                continue
            elif action_type == 'K':
                # Test if this is extending a melded pung to a kong, or 加槓.
                tile = action[2:]
                if tile in pungs[index]:
                    continue
                # Test if this is a concealed kong, or 暗槓.
                if prev_action and prev_action[1] == 'G':
                    continue
                # Otherwise, this is a melded kong, or 大明槓.
                assert (not prev_action) or (prev_action[1] in 'dD')
                kongs[index].append(tile)
                continue
            elif action_type == 'A':
                # Someone wins.
                players = game['players']
                hand['winner'] = players[index]
                #break

        hand['chows'] = chows
        hand['pungs'] = pungs
        hand['kongs'] = kongs

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

        for i in range(4):
            rank = int(match.group('rank'))
            player = match.group('player')
            points = int(match.group('points'))
            ranking[rank - 1] = dict(player=player, points=points)
            if i < 3:
                line = self.state_machine.next_line()
                match = result_of_game_re.match(line)

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
