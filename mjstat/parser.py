# -*- coding: utf-8 -*-
"""parser.py: Define class MJScoreParser.
"""
from docutils.statemachine import StateMachine
from .states import MJScoreState

#class MJScoreParser(docutils.parsers.Parser):
class MJScoreParser(object):
    """Parse the content of mjscore.txt."""

    def __init__(self):
        self.input_string = None
        self.game_data = None
        self.state_machine = None

    def parse(self, input_string, game_data):
        """Parse `input_string` and populate `game_data`,
        a list of game records.
        """

        settings = game_data['settings']
        assert 'debug' in settings
        assert 'verbose' in settings

        self.setup_parse(input_string, game_data)
        # pylint: disable=no-member
        self.state_machine = StateMachine(
            state_classes=MJScoreState.__subclasses__(),
            initial_state='GameOpening',
            debug=settings.debug and settings.verbose)
        self.state_machine.config = settings

        input_lines = tuple(i.strip() for i in input_string.split('\n'))

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
