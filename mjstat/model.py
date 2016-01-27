#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""model.py: Define various data types used in Mahjong.

Set of Yaku
====================
TBW
"""

from collections import namedtuple
from enum import Enum

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
