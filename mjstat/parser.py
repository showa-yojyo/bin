"""parser.py: Define class MJScoreParser."""

from __future__ import annotations

from docutils.statemachine import StateMachine  # type: ignore[import-untyped]

from .model import ScoreSheet
from .states import MJScoreState


class MJScoreParser:
    """Parse the content of mjscore.txt."""

    def __init__(self) -> None:
        self.input_string: str
        self.score_sheet: ScoreSheet
        self.state_machine: StateMachine

    def parse(self, input_string: str, sheet: ScoreSheet) -> None:
        """Parse `input_string` and populate `score_sheet`, a list of game records."""

        settings = sheet["settings"]
        assert "debug" in settings
        assert "verbose" in settings

        self.setup_parse(input_string, sheet)
        # pylint: disable=no-member
        self.state_machine = StateMachine(
            state_classes=MJScoreState.__subclasses__(),
            initial_state="GameOpening",
            debug=settings.debug and settings.verbose,
        )
        # self.state_machine.config = settings

        input_lines = tuple(line.strip() for line in input_string.split("\n"))

        self.state_machine.run(input_lines, context=sheet)
        self.state_machine.unlink()
        self.finish_parse()

    def setup_parse(self, input_string: str, sheet: ScoreSheet) -> None:
        """Initial parse setup."""

        self.input_string = input_string
        self.score_sheet = sheet

    def finish_parse(self) -> None:
        """Finalize parse details."""
        pass
