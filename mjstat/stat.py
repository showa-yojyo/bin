# -*- coding: utf-8 -*-
"""stat.py: The module for mahjong statistics.
"""

from . import count_han
import re

def evaluate(game_data, target_player):
    """Evaluate possibly numerous statistical values.

    The structure of `game_data` is like as follows::

        game_data ::= description, date, games, player_stats
            description ::= str
            date ::= datetime
            games ::= list-of-game (*)
                game ::= result, hands, players, started_at, finished_at,
                    result ::= list-of-dict (4)
                         player->points
                    hands ::= list-of-hand (1..*)
                        hand ::= action_table, balance, chows, pungs,
                          kongs, riichi_table,
                          ending, winner?, winning_value, winning_yaku_list
                            action_table ::= list-of-str
                            balance ::= player->points
                            chows ::= list-of-str (4)
                            pongs ::= list-of-str (4)
                            kongs ::= list-of-str (4)
                            riichi_table ::= list-of-bool (4)
                            ending ::= (ロン|ツモ|流局|四風連打|...)
                            winner ::= str
                            winning_value ::= str
                            winning_yaku_list ::= str
                    players ::= list-of-str (4)
                    started_at ::= datetime
                    finished_at ::= datetime
            player_stats ::= (name)->player_data

    The structure of `player_data` is like as follows::

        player_data ::= name, count_hands, games, placing_data,
          winning_data, lod_data, riich_data, melding_data
        name ::= str
        count_hands ::= (int)
        games ::= list-of-game (*)
        placing_data ::= placing_distr, mean_placing,
          first_placing_rate, last_placing_rate
            placing_distr ::= int (4)
        winning_data ::= winning_count, winning_rate, winning_mean,
          winning_mean_turns
        lod_data ::= lod_count, lod_rate, lod_mean
        riich_data ::= riichi_count, riichi_rate
        melding_data ::= melding_count, melding_rate
    """

    target_games = [g for g in game_data['games'] if target_player in g['players']]

    player_data = dict(
        count_hands=sum(len(game['hands']) for game in target_games),
        games=target_games,
        name=target_player,)

    game_data['player_stats'].update({target_player:player_data})

    evaluate_placing(player_data)
    evaluate_winning(player_data)
    evaluate_losing(player_data)
    evaluate_riichi(player_data)
    evaluate_melding(player_data)

    # TODO: (challenge) 平均獲得チップ枚数

def evaluate_placing(player_data):
    """Evaluate distribution of target player's placing, or 着順表.
    """

    player_data['placing_distr'] = []
    player_data['mean_placing'] = 0
    player_data['first_placing_rate'] = 0
    player_data['last_placing_rate'] = 0

    name = player_data['name']
    placing_distr = [0] * 4

    target_games = player_data['games']
    for game in target_games:
        ranking = game['result']
        for i in range(4):
            if ranking[i]['player'] == name:
                placing_distr[i] += 1
                break

    player_data['placing_distr'] = placing_distr

    num_games = len(target_games)
    if num_games:
        player_data['mean_placing'] = sum(
            (v*i) for i, v in enumerate(placing_distr, 1)) / num_games
        player_data['first_placing_rate'] = placing_distr[0] / num_games
        player_data['last_placing_rate'] = placing_distr[-1] / num_games

# XXX
winning_value_re = re.compile(r'''
(?P<hu>\d+)符
\s*
(?P<han>.+)飜
''', re.VERBOSE)

han_char_table = {k:v for v, k in enumerate('一二三四', 1)}

def evaluate_winning(player_data):
    """Evaluate target player's winning data.

    :winning_count: the total numbers of the player's winning.

    :winning_rate: the probability that the player wins in a hand.

    :winning_mean: the mean how much points did the winner obtain
    par a hand.

    :winning_mean_turn: the mean how many times did the winner tsumo,
    or pick tiles from the wall par a hand.
    """

    player_data['winning_count'] = 0
    player_data['winning_rate'] = 0
    player_data['winning_mean'] = 0
    player_data['winning_mean_han'] = 0
    player_data['winning_mean_turns'] = 0

    num_hands = player_data['count_hands']
    if not num_hands:
        return

    name = player_data['name']

    num_winning = 0
    total_points = 0
    total_turns = 0
    total_han = 0
    name = player_data['name']
    for g in player_data['games']:
        # pattern must be 1G, 2G, 3G or 4G.
        pattern = '{:d}G'.format(g['players'].index(name) + 1)

        for hand in g['hands']:
            winner_name = hand.get('winner', None)
            if name == winner_name:
                assert hand['balance']
                points = hand['balance'][name]
                total_points += points
                num_winning += 1

                action_table = hand['action_table']
                total_turns += sum(1 for i in action_table
                    if i.startswith(pattern))

                value = hand['winning_value']
                m = winning_value_re.match(value)
                if m:
                    han = han_char_table[m.group('han')]
                else:
                    # Pattern 満貫 covers 満貫 itself as well as
                    # 跳満, 倍満 and 三倍満.
                    if value.find('満貫'):
                        # Manually compute how many han are.
                        yaku = hand['winning_yaku_list']
                        han = count_han(yaku.split(), False)
                    elif value.find('役満'):
                        han = 13
                        if value.startswith('ダブル'):
                            han *= 2
                        elif value.startswith('トリプル'):
                            han *= 3
                    else:
                        raise ValueError('unknown winning: {}'.format(value))

                total_han += han

    if num_winning:
        player_data['winning_count'] = num_winning
        player_data['winning_rate'] = num_winning / num_hands
        player_data['winning_mean'] = total_points / num_winning
        player_data['winning_mean_han'] = total_han / num_winning
        player_data['winning_mean_turns'] = total_turns / num_winning

def evaluate_losing(player_data):
    """Evaluate target player's losing-on-discarding (LOD) rate and
    mean LOD, or 放銃率 and 平均放銃率.
    """

    player_data['lod_count'] = 0
    player_data['lod_rate'] = 0
    player_data['lod_mean'] = 0

    num_hands = player_data['count_hands']
    if not num_hands:
        return

    num_lod = 0
    total_losing_points = 0
    name = player_data['name']
    for g in player_data['games']:
        index = g['players'].index(name)
        for hand in g['hands']:
            if hand['ending'] == 'ロン':
                # For instance, if the action table ends with
                # '... 1d3p 4A', player #4 wins from player #1.
                if index == int(hand['action_table'][-2][0]) - 1:
                    assert hand['balance']
                    num_lod += 1
                    # sum of negative values
                    total_losing_points += hand['balance'][name]

    if num_lod:
        player_data['lod_count'] = num_lod
        player_data['lod_rate'] = num_lod / num_hands
        player_data['lod_mean'] = total_losing_points / num_lod

def evaluate_riichi(player_data):
    """Evaluate riichi rate."""

    player_data['riichi_count'] = 0
    player_data['riichi_rate'] = 0
    num_hands = player_data['count_hands']
    if not num_hands:
        return

    num_riichi = 0
    name = player_data['name']
    for g in player_data['games']:
        index = g['players'].index(name)
        for hand in g['hands']:
            riichi_table = hand['riichi_table']
            if riichi_table[index]:
                num_riichi += 1

    if num_riichi:
        player_data['riichi_count'] = num_riichi
        player_data['riichi_rate'] = num_riichi / num_hands

def evaluate_melding(player_data):
    """Evaluate target player's melding rate.

    N.B. Unlike できすぎくん criteria, this function evaluates how
    OFTEN the player makes use of melding in a hand.
    """

    player_data['melding_count'] = 0
    player_data['melding_rate'] = 0
    num_hands = player_data['count_hands']
    if not num_hands:
        return

    num_melding = 0
    name = player_data['name']
    for g in player_data['games']:
        index = g['players'].index(name)
        for hand in g['hands']:
            # If できすぎくん's style is preferred,
            # just increment num_melding one only if rhs > 1.
            num_melding += sum(len(hand[i][index])
                               for i in ('chows', 'pungs', 'kongs'))

    if num_melding:
        player_data['melding_count'] = num_melding
        player_data['melding_rate'] = num_melding / num_hands
