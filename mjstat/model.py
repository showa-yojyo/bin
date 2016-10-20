# -*- coding: utf-8 -*-
"""model.py: Define various data types used in Riichi Mahjong.

This module contains: class `Yaku`, the structure for Mahjong yaku;
class `YakuTable`, the set of all applicable Mahjong yaku;
a dictionary `yaku_map`, the mapping from yaku names to yaku objects
described above; a dictionary `yakuman_scalar`, the mapping from
yakuman grades to the multiplicand numbers; and a handful of
functions for construction of score data.
"""

from collections import namedtuple
from enum import Enum
import datetime
from itertools import (chain, product)

import dateutil.parser

DATETIME_FORMAT = r'%Y/%m/%d %H:%M'

Yaku = namedtuple('Yaku', (
    'is_concealed_only', # Determine if this yaku is concealed only.
    'has_concealed_bonus', # Determine if the han raises when concealed.
    'han', # Han value based on OPEN hands. e.g. 清一色 -> 5 (not 6).
    'name', # Spelling used in mjscore.txt.
    ))

class YakuTable(Enum):
    """A table that contains all of Mahjong yaku."""

    Yaku01 = Yaku(True, False, 1, 'リーチ')
    Yaku02 = Yaku(True, False, 1, '一発')
    Yaku03 = Yaku(True, False, 1, '門前清模和')
    Yaku04 = Yaku(False, False, 1, '断ヤオ')
    Yaku05 = Yaku(True, False, 1, '平和')
    Yaku06 = Yaku(True, False, 1, '一盃口')
    Yaku07 = Yaku(False, False, 1, '自風')
    Yaku08 = Yaku(False, False, 1, '場風')
    Yaku09 = Yaku(False, False, 1, '白')
    Yaku10 = Yaku(False, False, 1, '発')
    Yaku11 = Yaku(False, False, 1, '中')
    Yaku12 = Yaku(False, False, 1, '嶺上開花')
    Yaku13 = Yaku(False, False, 1, '槍槓')
    Yaku14 = Yaku(False, False, 1, '海底撈月')
    Yaku15 = Yaku(False, False, 1, '河底撈魚')
    Yaku16 = Yaku(False, True, 1, '三色同順')
    Yaku17 = Yaku(False, True, 1, '一気通貫')
    Yaku18 = Yaku(False, True, 1, '全帯')
    Yaku19 = Yaku(True, False, 2, '七対子')
    Yaku20 = Yaku(False, False, 2, '対々和')
    Yaku21 = Yaku(False, False, 2, '三暗刻')
    Yaku22 = Yaku(False, False, 2, '混老頭')
    Yaku23 = Yaku(False, False, 2, '三色同刻')
    Yaku24 = Yaku(False, False, 2, '三槓子')
    Yaku25 = Yaku(False, False, 2, '小三元')
    Yaku26 = Yaku(True, False, 2, 'ダブルリーチ')
    Yaku27 = Yaku(False, True, 2, '混一色')
    Yaku28 = Yaku(False, True, 2, '純全帯')
    Yaku29 = Yaku(True, False, 3, '二盃口')
    Yaku30 = Yaku(False, True, 5, '清一色')
    Yaku31 = Yaku(True, False, 13, '国士無双')
    Yaku32 = Yaku(True, False, 26, '国士無双１３面待')
    Yaku33 = Yaku(True, False, 13, '九連宝燈')
    Yaku34 = Yaku(True, False, 26, '九連宝燈９面待')
    Yaku35 = Yaku(True, False, 13, '天和')
    Yaku36 = Yaku(True, False, 13, '地和')
    Yaku37 = Yaku(True, False, 13, '四暗刻')
    Yaku38 = Yaku(True, False, 26, '四暗刻単騎待')
    Yaku39 = Yaku(False, False, 13, '四槓子')
    Yaku40 = Yaku(False, False, 13, '緑一色')
    Yaku41 = Yaku(False, False, 13, '清老頭')
    Yaku42 = Yaku(False, False, 13, '字一色')
    Yaku43 = Yaku(False, False, 13, '大三元')
    Yaku44 = Yaku(False, False, 13, '小四喜和')
    Yaku45 = Yaku(False, False, 26, '大四喜和')

# mapping from mjscore_name to yaku instance
YAKU_MAP = {yaku.value.name:yaku for yaku in YakuTable}

# possible yakuman grades in mjscore.txt
YAKUMAN_SCALAR = {
    #'':1,         # 8000, 16000
    'ダブル':2,    # 16000, 32000
    'トリプル':3,  # 24000, 48000
    '四倍':4,      # 32000, 64000
    '五倍':5,      # 40000, 80000
    '六倍':6,      # 48000, 96000
    '超':7,}       # 56000, 112000

def create_score_records(settings):
    """Create new game data.

    The structure of `game_data` is like as follows::

        game_data ::= settings, game*, since?, until?;
          settings ::= APPLICATION-DEPENDENT;
          game ::= result, hand+, player+, started_at, finished_at;
            result ::= (player->points){4};
              points ::= integer;
            hand ::= game, action_table, balance, dora_table, seat_table,
                     start_hand_table, chow*, pung*, kong*,
                     ending, winner?, winning_dora,
                     winning_value, winning_yaku_list;
              action_table ::= action+;
                action ::= [1-4], [ACdDKNR], tile;
              balance ::= player->points;
              dora_table ::= text+, text+;
              seat_table ::= seat{4};
                seat ::= (東|南|西|北);
              start_hand_table ::= start_hand{4};
                start_hand ::= tile{13};
                  tile ::= TODO;
              chow ::= (tile{3})*;
              pung ::= tile*;
              kong ::= tile*;
              ending ::= (ロン|ツモ|流局|四風連打|...);
              winner ::= player;
              winning_dora ::= integer;
              winning_value ::= text;
              winning_yaku_list ::= yaku+;
                yaku ::= TODO;
            player ::= text;
            started_at ::= datetime;
            finished_at ::= datetime;
          since ::= date;
          until ::= date;
    """

    game_data = dict(
        games=[],
        settings=settings,)

    set_reference_period(game_data, settings)
    return game_data

def create_game_record(context):
    """Create an empty game record.

    Args:
        context (dict): See function `create_score_records` above.

    Returns:
        A new dict object.
    """

    assert isinstance(context, dict)
    assert 'games' in context

    game = dict(
        result=[None] * 4,
        hands=[],
        players=[None] * 4,)
    context['games'].append(game)

    assert context['games'][-1] == game
    return game

def create_hand_record(context):
    """Create an empty hand and store it to the current hands.

    Args:
        context (dict): See function `create_score_records` above.

    Returns:
        A new dict object.
    """

    game = context['games'][-1]
    hands = game['hands']
    hand = dict(
        action_table=[],
        balance={},
        game=game, # parent
        seat_table=[None] * 4,
        start_hand_table=[None] * 4,
        dora_table=[],
        chows=[],
        pungs=[],
        kongs=[],)
    hands.append(hand)

    assert context['games'][-1]['hands'][-1] == hand
    return hand

def set_reference_period(game_data, settings):
    """Set reference period to the score records.

    Args:
        game_data (dict): See function `create_score_records` above.
        settings (argparse.Namespace): Command line arguments, etc.

    Returns:
        A new dict object.
    """

    since_date = None
    until_date = None
    if settings.today:
        today_date = datetime.date.today()
        since_date = today_date.strftime(DATETIME_FORMAT)
        until_date = (today_date + datetime.timedelta(1)).strftime(
            DATETIME_FORMAT)
    else:
        if settings.since:
            since_date = dateutil.parser.parse(settings.since).strftime(
                DATETIME_FORMAT)

        if settings.until:
            until_date = dateutil.parser.parse(settings.until).strftime(
                DATETIME_FORMAT)

    game_data.update(
        since=since_date,
        until=until_date,)

def find_winner(hand):
    """Find the winner of all hands.

    Args:
        hand (dict): See function `create_hand_record`.
    """

    assert 'game' in hand
    assert 'action_table' in hand

    # first_or_default
    winner = next((x for x in hand['action_table']
                   if x.endswith('A')), None)
    if not winner:
        return

    index = int(winner[0]) - 1
    assert index in range(4)
    hand['winner'] = hand['game']['players'][index]

def find_meldings(hand):
    """Find meldings (tile-calls) happened in a hand.

    Args:
        hand (dict): See function `create_hand_record`.
    """

    assert 'game' in hand
    assert 'action_table' in hand

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

        if action_type == 'C':
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

    hand.update(
        chows=chows,
        pungs=pungs,
        kongs=kongs)

def apply_transforms(game_data):
    """Apply a sort of transforms to elements in `game_data`.

    Args:
        game_data (dict): See function `create_score_records` above.
    """

    assert 'games' in game_data
    assert 'settings' in game_data

    settings = game_data['settings']
    transforms = []
    if settings.fundamental or settings.yaku:
        transforms.append(find_winner)
    if settings.fundamental:
        transforms.append(find_meldings)

    for i in game_data['games']:
        for transform, hand in product(transforms, i['hands']):
            transform(hand)

def merge_games(game_data_list):
    """Merge games of a collection of `game_data` to an instance of
    `game_data`.

    Args:
        game_data_list: A non-empty list or tuple of `game_data`.
    """

    assert game_data_list

    if not game_data_list[0]['games']:
        return game_data_list[0]

    game_data_sorted = sorted(
        game_data_list,
        key=lambda game_data: game_data['games'][0]['started_at'])

    game_data = game_data_sorted[0].copy()
    game_data['games'] = tuple(chain.from_iterable(
        i['games'] for i in game_data_sorted))

    return game_data
