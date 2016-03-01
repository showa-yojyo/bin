# -*- coding: utf-8 -*-
"""writer.py: Define class MJScoreWriter.
"""

#from docutils.writers import UnfilteredWriter
from .languages import get_language
from .stat import evaluate
from .translator import fill_template

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

        stat_options = dict(fundamental=settings.fundamental,
                            yaku=settings.yaku)
        self.parts['options'] = stat_options

        target_player = settings.target_player
        if target_player == 'all':
            # Detect all players from game data.
            player_names = set().union(*(g['players'] for g in game_data['games']))
        else:
            player_names = (target_player,)

        self.parts['player_data'] = [
            evaluate(game_data, target_player, **stat_options)
            for target_player in player_names]

        assert 'player_data' in self.parts
        assert 'options' in self.parts
