# -*- coding: utf-8 -*-
"""ja.py: Japanese language mappings for language-dependent features.
"""

tmpl_summary = \
'''集計期間 {started_at} - {finished_at}
プレイヤーデータ
  名前 {name}
  ゲーム数 {count_games} 試合
  局数 {count_hands} 局'''

tmpl_fundamental = \
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

tmpl_yaku_freq = '役分布'
tmpl_value_tiles = '  役牌'
