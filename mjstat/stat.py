# -*- coding: utf-8 -*-
"""stat.py: The module for mahjong statistics.
"""

def evaluate(game_data, target_player):
    """Evaluate possibly numerous statistical values."""

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
    placing_distr = [0, 0, 0, 0]

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

def evaluate_winning(player_data):
    """Evaluate target player's winning rate, or 和了率."""

    player_data['winning_count'] = 0
    player_data['winning_rate'] = 0
    player_data['winning_mean'] = 0

    num_hands = player_data['count_hands']
    if not num_hands:
        return

    name = player_data['name']

    num_winning = 0
    total_points = 0
    name = player_data['name']
    for g in player_data['games']:
        for hand in g['hands']:
            if hand['ending'] in ('ツモ', 'ロン'):
                assert hand['balance']
                first = hand['balance'][0]
                points = first['balance']
                if (first['player'] == name and
                    points > 0):
                    total_points += points
                    num_winning += 1

    if num_winning:
        player_data['winning_count'] = num_winning
        player_data['winning_rate'] = num_winning / num_hands
        player_data['winning_mean'] = total_points / num_winning

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
        for hand in g['hands']:
            if hand['ending'] == 'ロン':
                assert hand['balance']
                last = hand['balance'][-1]
                if last['player'] == name:
                    num_lod += 1
                    total_losing_points += last['balance'] # sum of negative values

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
            c = hand['melding_counter_table'][index]

            # If できすぎくん's style is preferred,
            # just increment num_melding one only if c > 1.
            num_melding += c

    if num_melding:
        player_data['melding_count'] = num_melding
        player_data['melding_rate'] = num_melding / num_hands
