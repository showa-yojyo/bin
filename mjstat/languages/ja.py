# -*- coding: utf-8 -*-
"""ja.py: Japanese language mappings for language-dependent features.
"""

tmpl_summary = \
'''集計期間           {{started_at}} - {{finished_at}}
プレイヤー         {% for p in data %}{{p.name}} {% endfor %}
ゲーム数           {{count_games}}
局数               {{data[0].count_hands}}'''

tmpl_fundamental = \
'''着順データ
  着順頻度         {% for p in data %}{{p.placing_distr|join('-')}}  {% endfor %}
  トップ率         {% for p in data %}{{p.first_placing_rate|format_percentage}}  {% endfor %}
  ラス率           {% for p in data %}{{p.last_placing_rate|format_percentage}}  {% endfor %}
  平均着順         {% for p in data %}{{p.mean_placing|format_float}}  {% endfor %}
アガリデータ
  アガリ率         {% for p in data %}{{p.winning_rate|format_percentage}}  {% endfor %}
  平均得点         {% for p in data %}{{p.winning_mean|format_float}}  {% endfor %}
  平均アガリ飜     {% for p in data %}{{p.winning_mean_han|format_float}}  {% endfor %}
  平均アガリ巡目   {% for p in data %}{{p.winning_mean_turns|format_float}}  {% endfor %}
放銃データ
  放銃率           {% for p in data %}{{p.lod_rate|format_percentage}}  {% endfor %}
  平均失点         {% for p in data %}{{p.lod_mean|format_float}}  {% endfor %}
立直データ
  平均使用率       {% for p in data %}{{p.riichi_rate|format_percentage}}  {% endfor %}
鳴きデータ
  平均鳴き回数     {% for p in data %}{{p.melding_rate|format_percentage}}  {% endfor %}
'''

tmpl_yaku_freq = \
'''役分布
{% for y in yaku_table -%}
{{y.name|indent(2, True)}}    {% for p in data %}{{ p.yaku_freq[y] }}  {% endfor %}
{% endfor %}
'''
