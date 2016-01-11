# -*- coding: utf-8 -*-
"""stat.py: The module for mahjong statistics.
"""

def enumerate_hands(game_data):
    for game in game_data['games']:
        for hand in game['hands']:
            yield hand

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
