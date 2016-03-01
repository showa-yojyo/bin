#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""model.py: Define various data types used in Mahjong.

Set of Yaku
====================
TBW
"""

from collections import namedtuple
from enum import Enum
import datetime
import dateutil.parser

datetime_format = r'%Y/%m/%d %H:%M'

Yaku = namedtuple('Yaku', (
    'is_concealed_only', # Determine if this yaku is concealed only.
    'has_concealed_bonus', # Determine if the han raises when concealed.
    'han', # Han value based on OPEN hands. e.g. 清一色 -> 5 (not 6).
    'name', # Spelling used in mjscore.txt.
    ))

class YakuTable(Enum):
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
yaku_map = {yaku.value.name:yaku for yaku in YakuTable}

# possible yakuman grades in mjscore.txt
yakuman_scalar = {
    #'':1,         # 8000, 16000
    'ダブル':2,    # 16000, 32000
    'トリプル':3,  # 24000, 48000
    '四倍':4,      # 32000, 64000
    '五倍':5,      # 40000, 80000
    '六倍':6,      # 48000, 96000
    '超':7,}       # 56000, 112000

def create_score_records(settings):
    """Create new game data."""

    game_data = dict(
        description='Game score recorded in mjscore.txt',
        games=[],
        settings=settings,)

    set_reference_period(game_data, settings)
    return game_data

def create_game_record(context):
    """Create an empty game record."""

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
    """Create an empth hand and put into the current hands."""

    game = context['games'][-1]
    hands = game['hands']
    hand = dict(
        action_table=[],
        balance={},
        game=game, # parent
        riichi_table=[False] * 4,
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
    """Set reference period to the score records."""

    since_date = None
    until_date = None
    if settings.today:
        today_date = datetime.date.today()
        since_date = today_date.strftime(datetime_format)
        until_date = (today_date + datetime.timedelta(1)).strftime(datetime_format)
    else:
        if settings.since:
            since_date = dateutil.parser.parse(settings.since).strftime(datetime_format)

        if settings.until:
            until_date = dateutil.parser.parse(settings.until).strftime(datetime_format)

    game_data['since'] = since_date
    game_data['until'] = until_date

def examine_action_table(hand):
    """Examine the action history of a hand record."""

    assert 'game' in hand
    assert 'action_table' in hand
    assert 'riichi_table' in hand

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
            hand['winner'] = hand['game']['players'][index]
            #break

    hand['chows'] = chows
    hand['pungs'] = pungs
    hand['kongs'] = kongs
