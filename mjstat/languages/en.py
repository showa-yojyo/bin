# -*- coding: utf-8 -*-
"""en.py: English language mappings for language-dependent features.
"""

tmpl_summary = \
'''Reference period: {started_at} - {finished_at}
Player data
  Name: {name}
  Number of games: {count_games} games
  Number of hands: {count_hands} hands'''

tmpl_fundamental = \
'''Placing data
  [1st, 2nd, 3rd, 4th]: {placing_distr}
  1st-place prob.: {first_placing_rate:.2%}
  4th-place prob.: {last_placing_rate:.2%}
  Mean place: {mean_placing:.2f}th
Wins
  Winning percentage: {winning_rate:.2%} ({winning_count}/{count_hands})
  Mean points: {winning_mean:.2f} pts.
  Mean han: {winning_mean_han:.2f} han
  Mean turns: {winning_mean_turns:.2f} turns
Losses on deal-in
  Deal-in percentage: {lod_rate:.2%} ({lod_count}/{count_hands})
  Mean points: {lod_mean:.2f} pts.
Riichi data
  Riichi prob.: {riichi_rate:.2%} ({riichi_count}/{count_hands})
Melding data
  Melding prob.: {melding_rate:.2%} ({melding_count}/{count_hands})'''

tmpl_yaku_freq = 'Frequency of yaku'
tmpl_value_tiles = '  Value tiles'
