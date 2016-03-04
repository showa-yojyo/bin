# -*- coding: utf-8 -*-
"""writer.py: Define class MJScoreWriter.
"""

#from docutils.writers import UnfilteredWriter
from .languages import get_language
from .model import YakuTable
from .stat import (create_player_data,
                   evaluate_placing,
                   evaluate_winning,
                   evaluate_losing,
                   evaluate_riichi,
                   evaluate_melding,
                   evaluate_yaku_frequency)
from itertools import product
from jinja2 import Environment

#class MJScoreWriter(UnfilteredWriter):
class MJScoreWriter(object):

    def __init__(self):
        self.language = None
        self.game_data = None
        self.output = None
        self.destination = None
        self.parts = {}

    def write(self, game_data, destination):
        """Output `game_data` into `destination`."""

        settings = game_data['settings']
        self.language = get_language(settings.language)
        self.game_data = game_data
        self.destination = destination

        self.translate()

        output = self.destination.write(self.output)
        return output

    def translate(self):
        """Translate `self.game_data` into `self.output`."""

        self.assemble_parts()
        self.output = fill_template(self.parts['player_data'],
                                    self.language,
                                    **self.parts['options'])

    def assemble_parts(self):
        """Assemble the `self.parts` dictionary."""

        game_data = self.game_data
        settings = game_data['settings']
        target_player = settings.target_player

        if target_player == 'all':
            # Detect all players from game data.
            player_names = set().union(
                *(g['players'] for g in game_data['games']))
        else:
            player_names = (target_player,)

        player_data_list = create_player_data(game_data, *player_names)

        evaluators = []
        if settings.fundamental:
            evaluators.extend((
                evaluate_placing,
                evaluate_winning,
                evaluate_losing,
                evaluate_riichi,
                evaluate_melding,))
        if settings.yaku:
            evaluators.append(evaluate_yaku_frequency)

        for f, p in product(evaluators, player_data_list):
            f(p)

        self.parts.update(
            player_data=player_data_list,
            options=dict(fundamental=settings.fundamental,
                         yaku=settings.yaku),)

        assert 'player_data' in self.parts
        assert 'options' in self.parts

def format_float(val):
    return '{:.2f}'.format(val)

def format_percentage(val):
    return '{:.2%}'.format(val)

def fill_template(player_data, lang, fundamental, yaku):
    """Build long text which shows the statistics of the target
    player(s).
    """

    target_games = player_data[0]['games']
    if not target_games:
        return 'NO DATA'

    env = Environment(autoescape=False)
    env.filters.update(
        format_float=format_float,
        format_percentage=format_percentage,)

    output_text = env.from_string(lang.tmpl_summary).render(
        count_games=len(target_games),
        started_at=target_games[0]['started_at'],
        finished_at=target_games[-1]['finished_at'],
        data=player_data)

    if fundamental:
        output_text += env.from_string(lang.tmpl_fundamental).render(
            data=player_data)

    if yaku:
        yaku_name_map = {y:lang.yaku_names[i]
                         for i, y in enumerate(YakuTable)}
        output_text += env.from_string(lang.tmpl_yaku_freq).render(
            data=player_data,
            YakuTable=YakuTable,
            yaku_name_map=yaku_name_map)

    return output_text
