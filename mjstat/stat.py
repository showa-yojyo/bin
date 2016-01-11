# -*- coding: utf-8 -*-
"""stat.py: The module for mahjong statistics.
"""

def enumerate_hands(game_data):
    for game in game_data['games']:
        for hand in game['hands']:
            yield hand

def evaluate(game_data, target_player):
    """Evaluate possibly numerous statistical values."""

    player_index = game_data['player_stats']['names'].index(target_player)
    player_data = dict(
        index=player_index,
        name=target_player)

    game_data['player_stats'].update({target_player:player_data})

    all_games = game_data['games']
    game_data['count_hands'] = sum(len(game['hands']) for game in all_games)

    evaluate_placing(game_data, player_data)
    evaluate_winning(game_data, player_data)
    evaluate_losing(game_data, player_data)
    evaluate_riichi(game_data, player_data)
    evaluate_melding(game_data, player_data)

    # TODO: (challenge) 平均獲得チップ枚数

def evaluate_placing(game_data, player_data):
    """Evaluate distribution of target player's placing, or 着順表.
    """

    player_data['placing_distr'] = []
    player_data['mean_placing'] = 0
    player_data['first_placing_rate'] = 0
    player_data['last_placing_rate'] = 0

    name = player_data['name']
    placing_distr = [0, 0, 0, 0]

    all_games = game_data['games']
    for game in all_games:
        ranking = game['result']
        for i in range(4):
            if ranking[i]['player'] == name:
                placing_distr[i] += 1
                break

    player_data['placing_distr'] = placing_distr

    num_games = len(all_games)
    if num_games:
        player_data['mean_placing'] = sum(
            (v*i) for i, v in enumerate(placing_distr, 1)) / num_games
        player_data['first_placing_rate'] = placing_distr[0] / num_games
        player_data['last_placing_rate'] = placing_distr[-1] / num_games

def evaluate_winning(game_data, player_data):
    """Evaluate target player's winning rate, or 和了率."""

    player_data['count_winning'] = 0
    player_data['winning_rate'] = 0
    player_data['winning_mean'] = 0

    num_hands = game_data['count_hands']
    if not num_hands:
        return

    name = player_data['name']

    num_winning = 0
    total_points = 0
    for hand in enumerate_hands(game_data):
        if hand['ending'] in ('ツモ', 'ロン'):
            assert hand['balance']
            first = hand['balance'][0]
            points = first['balance']
            if (first['player'] == name and
                points > 0):
                total_points += points
                num_winning += 1

    if num_winning:
        player_data['winning_rate'] = num_winning / num_hands
        player_data['winning_mean'] = total_points / num_winning

def evaluate_losing(game_data, player_data):
    """Evaluate target player's losing-on-discarding (LOD) rate and
    mean LOD, or 放銃率 and 平均放銃率.
    """

    player_data['count_lod'] = 0
    player_data['lod_rate'] = 0
    player_data['lod_mean'] = 0

    num_hands = game_data['count_hands']
    if not num_hands:
        return

    name = player_data['name']

    num_lod = 0
    total_losing_points = 0
    for hand in enumerate_hands(game_data):
        if hand['ending'] == 'ロン':
            assert hand['balance']
            last = hand['balance'][-1]
            if last['player'] == name:
                num_lod += 1
                total_losing_points += last['balance'] # sum of negative values

    if num_lod:
        player_data['lod_rate'] = num_lod / num_hands
        player_data['lod_mean'] = total_losing_points / num_lod

def evaluate_riichi(game_data, player_data):
    """Evaluate riichi rate."""

    player_data['riichi_rate'] = 0
    num_hands = game_data['count_hands']
    if not num_hands:
        return

    player_index = player_data['index']
    num_riichi = 0
    for hand in enumerate_hands(game_data):
        riichi_table = hand['riichi_table']
        if riichi_table[player_index]:
            num_riichi += 1

    player_data['riichi_rate'] = num_riichi / num_hands

def evaluate_melding(game_data, player_data):
    """Evaluate target player's melding rate.

    N.B. Unlike できすぎくん criteria, this function evaluates how
    OFTEN the player makes use of melding in a hand.
    """

    player_data['melding_count'] = 0
    player_data['melding_rate'] = 0
    num_hands = game_data['count_hands']
    if not num_hands:
        return

    num_melding = 0
    index = player_data['index']
    for hand in enumerate_hands(game_data):
        c = hand['melding_counter_table'][index]

        # If できすぎくん's style is preferred,
        # just increment num_melding one only if c > 1.
        num_melding += c

    if num_melding:
        player_data['melding_count'] = num_melding
        player_data['melding_rate'] = num_melding / num_hands
