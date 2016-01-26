# -*- coding: utf-8 -*-
"""en.py: English language mappings for language-dependent features.
"""

tmpl_summary = \
'''Reference period:  {{started_at}} - {{finished_at}}
Players            {% for p in data %}{{p.name}} {% endfor %}
Number of games    {{count_games}}
Number of hands    {{data[0].count_hands}}'''

tmpl_fundamental = \
'''Placing data
  Place freq.      {% for p in data %}{{p.placing_distr|join('-')}}  {% endfor %}
  1st-place prob.  {% for p in data %}{{p.first_placing_rate|format_percentage}}  {% endfor %}
  4th-place prob.  {% for p in data %}{{p.last_placing_rate|format_percentage}}  {% endfor %}
  Mean place       {% for p in data %}{{p.mean_placing|format_float}}  {% endfor %}
Wins
  Winning rate     {% for p in data %}{{p.winning_rate|format_percentage}}  {% endfor %}
  Mean points      {% for p in data %}{{p.winning_mean|format_float}}  {% endfor %}
  Mean han         {% for p in data %}{{p.winning_mean_han|format_float}}  {% endfor %}
  Mean turns       {% for p in data %}{{p.winning_mean_turns|format_float}}  {% endfor %}
Losses on deal-in
  Deal-in rate     {% for p in data %}{{p.lod_rate|format_percentage}}  {% endfor %}
  Mean points      {% for p in data %}{{p.lod_mean|format_float}}  {% endfor %}
Riichi data
  Riichi prob.     {% for p in data %}{{p.riichi_rate|format_percentage}}  {% endfor %}
Melding data
  Melding prob.    {% for p in data %}{{p.melding_rate|format_percentage}}  {% endfor %}
'''

tmpl_yaku_freq = \
'''Frequency of yaku
{% for y in yaku_table -%}
{{y.name|indent(2, True)}}    {% for p in data %}{{ p.yaku_freq[y] }}  {% endfor %}
{% endfor %}
'''

tmpl_value_tiles = '  Value tiles'
