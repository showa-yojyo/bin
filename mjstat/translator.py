# -*- coding: utf-8 -*-
"""translator.py: Translate text to output in specified language.
"""

from .model import YakuTable
from jinja2 import Environment

def format_float(val):
    return '{:.2f}'.format(val)

def format_percentage(val):
    return '{:.2%}'.format(val)

# XXX
default_players = {
    'あなた':1,
    '下家':2,
    '対面':3,
    '上家':4,
    }

def get_key_for_special_names(player_data):
    """XXX"""
    return default_players.get(player_data['name'], hash(player_data['name']))

def fill_template(player_data, lang, fundamental, yaku):
    """Build long text which shows the statistics of the target
    player(s).
    """

    target_games = player_data[0]['games']
    if not target_games:
        return 'NO DATA'

    # XXX
    player_data = sorted(player_data, key=get_key_for_special_names)

    env = Environment(autoescape=False)
    env.filters['format_float'] = format_float
    env.filters['format_percentage'] = format_percentage

    output_text = env.from_string(lang.tmpl_summary).render(
        count_games=len(target_games),
        started_at=target_games[0]['started_at'],
        finished_at=target_games[-1]['finished_at'],
        data=player_data)

    if fundamental:
        output_text += env.from_string(lang.tmpl_fundamental).render(
            data=player_data)

    if yaku:
        yaku_name_map = {y:lang.yaku_names[i] for i, y in enumerate(YakuTable)}
        output_text += env.from_string(lang.tmpl_yaku_freq).render(
            data=player_data,
            YakuTable=YakuTable,
            yaku_name_map=yaku_name_map)

    return output_text
