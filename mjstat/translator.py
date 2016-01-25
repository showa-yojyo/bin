# -*- coding: utf-8 -*-
"""translator.py: Translate text to output in specified language.
"""

from .languages import get_language
from .model import value_tiles

def output(player_data, lang_code='en'):
    """Show the statistics of the target player."""

    target_games = player_data['games']
    if not target_games:
        print('NO DATA')
        return

    lang = get_language(lang_code)

    print(lang.tmpl_summary.format(
        count_games=len(target_games),
        started_at=target_games[0]['started_at'],
        finished_at=target_games[-1]['finished_at'],
        **player_data))

    if 'winning_count' in player_data:
        print(lang.tmpl_fundamental.format(**player_data))

    if 'yaku_freq' in player_data:
        print(lang.tmpl_yaku_freq)
        yaku_freq = player_data['yaku_freq']

        # Merge value tiles into an item.
        han = sum(yaku_freq.get(i, 0) for i in value_tiles)
        if han:
            print(lang.tmpl_value_tiles, han)

        yaku_freq = {k:v for k, v in yaku_freq.items()
                     if (k not in value_tiles) and (v > 0)}

        for k in sorted(yaku_freq):
            freq = yaku_freq[k]
            print('  {} {}'.format(k.name, freq))
