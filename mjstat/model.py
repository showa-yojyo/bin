#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""model.py: Define various data types used in Mahjong.

Set of Yaku
====================
TBW
"""

from collections import namedtuple

Yaku = namedtuple('Yaku', (
    'id',              # ID for sorting.
    'name',            # My favorite spelling.
    'name_mjscore',    # Spelling used in mjscore.txt.
    'is_concealed_only',  # Determine if this yaku is concealed only.
    'has_concealed_bonus', # Determine if the han raises when concealed.
    'han',   # Han value based on OPEN hands. e.g. 清一色 -> 5 (not 6).
    ))

yaku_table = (
    Yaku(1, '立直', 'リーチ', True, False, 1), # Riichi, Ready Hand.
    Yaku(2, '一発', '一発', True, False, 1), # One Shot
    Yaku(3, '門前清自摸和', '門前清模和', True, False, 1), # Self draw, Fully Concealed Hand
    Yaku(4, '断么九', '断ヤオ', False, False, 1), # All Simples
    Yaku(5, '平和', '平和', True, False, 1), # All Sequences, Pinfu
    Yaku(6, '一盃口', '一盃口', True, False, 1), # Pure Double Chow/Sequences.
    Yaku(7, '自風', '自風', False, False, 1), # Seat Wind (Value Tiles)
    Yaku(8, '場風', '場風', False, False, 1), # Prevalent Wind (Value Tiles)
    Yaku(9, '白', '白', False, False, 1), # Dragon Pung (Value Tiles)
    Yaku(10, '発', '発', False, False, 1), # Dragon Pung (Value Tiles)
    Yaku(11, '中', '中', False, False, 1), # Dragon Pung (Value Tiles)
    Yaku(12, '嶺上開花', '嶺上開花', False, False, 1), # After a Kong; Dead wall draw.
    Yaku(13, '搶槓', '槍槓', False, False, 1), # Robbing the Kong
    Yaku(14, '海底撈月', '海底撈月', False, False, 1), # Under the Sea; Win by last draw.
    Yaku(15, '河底撈魚', '河底撈魚', False, False, 1), # Under the River; Win by last discard.
    Yaku(16, '三色同順', '三色同順', False, True, 1), # Mixed Triple Chow, Three Colored Straight
    Yaku(17, '一気通貫', '一気通貫', False, True, 1), # Pure Straight
    Yaku(18, '混全帯么九', '全帯', False, True, 1), # Outside Hand; Terminal or honor in each group.
    Yaku(19, '七対子', '七対子', True, False, 2), # Seven Pairs
    Yaku(20, '対々和', '対々和', False, False, 2), # All Pungs/Triplets
    Yaku(21, '三暗刻', '三暗刻', False, False, 2),  # Three Concealed Pungs/Triplets
    Yaku(22, '混老頭', '混老頭', False, False, 2), # All Terminals and Honors
    Yaku(23, '三色同刻', '三色同刻', False, False, 2), # Triple Pung, Three Colored Triplets
    Yaku(24, '三槓子', '三槓子', False, False, 2), # Three Kongs
    Yaku(25, '小三元', '小三元', False, False, 2), # Little Three Dragons
    Yaku(26, 'ダブル立直', 'ダブルリーチ', True, False, 2), # Double Riichi
    Yaku(27, '混一色', '混一色', False, True, 2), # Half Flush
    Yaku(28, '純全帯么九', '純全帯', False, True, 2), # Terminals in All Sets; Terminal in each meld.
    Yaku(29, '二盃口', '二盃口', True, False, 3), # Twice Pure Double Chows; Two sets of identical sequences.
    Yaku(30, '清一色', '清一色', False, True, 5), # Full Flush

    Yaku(101, '国士無双', '国士無双', True, False, 13), # Thirteen Orphans
    Yaku(102, '国士無双十三面待ち', '国士無双１３面待', True, False, 26), # Thirteen Orphans
    Yaku(103, '九蓮宝燈', '九連宝燈', True, False, 13), # Nine Gates
    Yaku(104, '純正九蓮宝燈', '九連宝燈９面待', True, False, 26), # Pure Nine Gates
    Yaku(105, '天和', '天和', True, False, 13), # Blessing of Heaven, Heavenly Hand
    Yaku(106, '地和', '地和', True, False, 13), # Blessing of Earth, Earthly Hand
    Yaku(107, '四暗刻', '四暗刻', True, False, 13), # Four Concealed Pungs/Triplets
    Yaku(108, '四暗刻単騎待ち', '四暗刻単騎待', True, False, 26), # Four Concealed Pungs/Triplets
    Yaku(109, '四槓子', '四槓子', False, False, 13), # Four kongs
    Yaku(110, '緑一色', '緑一色', False, False, 13), # All Green
    Yaku(111, '清老頭', '清老頭', False, False, 13), # All Terminals
    Yaku(112, '字一色', '字一色', False, False, 13), # All Honors
    Yaku(113, '大三元', '大三元', False, False, 13), # Big Three Dragons
    Yaku(114, '小四喜', '小四喜和', False, False, 13), # Little Four Winds
    Yaku(115, '大四喜', '大四喜和', False, False, 26), # Big Four Winds
    )

# mapping from mjscore_name to yaku instance
yaku_map = {yaku.name_mjscore:yaku for yaku in yaku_table}

# possible yakuman grades in mjscore.txt
yakuman_scalar = {
    #'':1,         # 8000, 16000
    'ダブル':2,    # 16000, 32000
    'トリプル':3,  # 24000, 48000
    '四倍':4,      # 32000, 64000
    '五倍':5,      # 40000, 80000
    '六倍':6,      # 48000, 96000
    '超':7,}       # 56000, 112000
