# -*- coding: utf-8 -*-
"""parser.py: Define class MJScoreParser.
"""
from .states import MJScoreState
from docutils.statemachine import StateMachine

#class MJScoreParser(docutils.parsers.Parser):
class MJScoreParser(object):

    def __init__(self, settings):
        self.input_string = None
        self.game_data = None
        self.state_machine = None
        self.settings = settings
        assert 'debug' in self.settings
        assert 'verbose' in self.settings

    def parse(self, input_string, game_data):
        """Parse `input_string` and populate `game_data`,
        a list of game records.
        """

        self.setup_parse(input_string, game_data)
        self.state_machine = StateMachine(
            state_classes=MJScoreState.__subclasses__(),
            initial_state='GameOpening',
            debug=self.settings.debug and self.settings.verbose)
        self.state_machine.config = self.settings

        input_lines = [i.strip() for i in input_string.split('\n')]

        self.state_machine.run(input_lines, context=game_data)
        self.state_machine.unlink()
        self.finish_parse()

    def setup_parse(self, input_string, game_data):
        """Initial parse setup."""

        self.input_string = input_string
        self.game_data = game_data

    def finish_parse(self):
        """Finalize parse details."""
        pass
