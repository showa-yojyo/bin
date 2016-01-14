# -*- coding: utf-8 -*-
"""__init__.py
"""

import re

players_default = ['あなた', '下家', '対面', '上家']

# The mapping of yaku-han (without yakuman yaku).
# x: closed hand
# y: open
yaku_han_table = {
    'リーチ':(1, 0), # 立直
    '一発':(1, 0),
    '門前清模和':(1, 0), # 門前清自摸和
    '断ヤオ':(1, 1), # 断么九
    '平和':(1, 0),
    '一盃口':(1, 0),
    '自風':(1, 1),
    '場風':(1, 1),
    '白':(1, 1),
    '発':(1, 1),
    '中':(1, 1),
    '嶺上開花':(1, 1),
    # TODO: Make sure if this matches mjscore.txt's expression.
    '槍槓':(1, 1),
    '海底撈月':(1, 1),
    '河底撈魚':(1, 1),

    '三色同順':(2, 1),
    '一気通貫':(2, 1),
    '全帯':(2, 1), # 混全帯么九
    '七対子':(2, 2),
    '対々和':(2, 2),
    '三暗刻':(2, 2),
    '混老頭':(2, 2),
    '三色同刻':(2, 2),
    '三槓子':(2, 2),
    '小三元':(2, 2),
    'ダブルリーチ':(2, 0), # ダブル立直

    '混一色':(3, 2),
    '純全帯':(3, 2), # 純全帯么九
    '二盃口':(3, 0),

    '清一色':(6, 5),}

dora_re = re.compile(r'[裏赤]?ドラ(\d)+')

def count_han(yakulist, closed=False):
    """Count the total number of han (doubles)."""

    total_han = 0
    i = 0 if closed else 1
    for yaku in yakulist:
        # First search for the table.
        han = yaku_han_table.get(yaku, None)
        if han:
            total_han += han[i]
            continue

        # Next try to count dora.
        m = dora_re.match(yaku)
        if m:
            total_han += int(m.group(1))
            continue

    return total_han
