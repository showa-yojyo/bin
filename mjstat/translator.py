# -*- coding: utf-8 -*-
"""translator.py: Translate text to output in specified language.
"""

from .model import value_tiles

tmpl_summary_en = \
'''Reference period: {started_at} - {finished_at}
Player data
  Name: {name}
  Number of games: {count_games} games
  Number of hands: {count_hands} hands'''

tmpl_fundamental_en = \
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

tmpl_yaku_freq_en = 'Frequency of yaku'
tmpl_value_tiles_en = '  Value tiles'

tmpl_summary_ja = \
'''集計期間 {started_at} - {finished_at}
プレイヤーデータ
  名前 {name}
  ゲーム数 {count_games} 試合
  局数 {count_hands} 局'''

tmpl_fundamental_ja = \
'''着順データ
  [1st, 2nd, 3rd, 4th]: {placing_distr}
  トップ率 {first_placing_rate:.2%}
  ラス率 {last_placing_rate:.2%}
  平均着順 {mean_placing:.2f} 着
アガリデータ
  アガリ率 {winning_rate:.2%} ({winning_count}/{count_hands})
  平均得点 {winning_mean:.2f} 点
  平均アガリ飜 {winning_mean_han:.2f}
  平均アガリ巡目 {winning_mean_turns:.2f}
放銃データ
  放銃率 {lod_rate:.2%} ({lod_count}/{count_hands})
  平均失点 {lod_mean:.2f} 点
立直データ
  平均使用率 {riichi_rate:.2%} ({riichi_count}/{count_hands})
鳴きデータ
  平均鳴き回数 {melding_rate:.2%} ({melding_count}/{count_hands})'''

tmpl_yaku_freq_ja = '役分布'

tmpl_value_tiles_ja = '  役牌'

tmpl_map = dict(
    en=dict(
        summary=tmpl_summary_en,
        fundamental=tmpl_fundamental_en,
        yaku_freq=tmpl_yaku_freq_en,
        value_tiles=tmpl_value_tiles_en,),
    ja=dict(
        summary=tmpl_summary_ja,
        fundamental=tmpl_fundamental_ja,
        yaku_freq=tmpl_yaku_freq_ja,
        value_tiles=tmpl_value_tiles_ja,),)

def output(player_data, language='en'):
    """Show the statistics of the target player."""

    target_games = player_data['games']
    if not target_games:
        print('NO DATA')
        return

    tmpl = tmpl_map.get(language, 'en')

    print(tmpl['summary'].format(
        count_games=len(target_games),
        started_at=target_games[0]['started_at'],
        finished_at=target_games[-1]['finished_at'],
        **player_data))

    if 'winning_count' in player_data:
        print(tmpl['fundamental'].format(**player_data))

    if 'yaku_freq' in player_data:
        print(tmpl['yaku_freq'])
        yaku_freq = player_data['yaku_freq']

        # Merge value tiles into an item.
        han = sum(yaku_freq.get(i, 0) for i in value_tiles)
        if han:
            print(tmpl['value_tiles'], han)

        yaku_freq = {k:v for k, v in yaku_freq.items()
                     if (k not in value_tiles) and (v > 0)}

        for k in sorted(yaku_freq):
            freq = yaku_freq[k]
            print('  {} {}'.format(k.name, freq))
