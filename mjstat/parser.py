"""parser.py: Define class MJScoreParser."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Self

from docutils.statemachine import StateMachine  # type: ignore
from .states import MJScoreState

type GameData = dict[str, Any]


class MJScoreParser(object):
    """Parse the content of mjscore.txt."""

    def __init__(self: Self) -> None:
        self.input_string: str
        self.game_data: GameData
        self.state_machine: StateMachine

    def parse(self: Self, input_string: str, game_data: GameData) -> None:
        """Parse `input_string` and populate `game_data`,
        a list of game records.
        """

        settings = game_data["settings"]
        assert "debug" in settings
        assert "verbose" in settings

        self.setup_parse(input_string, game_data)
        # pylint: disable=no-member
        self.state_machine = StateMachine(
            state_classes=MJScoreState.__subclasses__(),
            initial_state="GameOpening",
            debug=settings.debug and settings.verbose,
        )
        # self.state_machine.config = settings

        input_lines = tuple(line.strip() for line in input_string.split("\n"))

        self.state_machine.run(input_lines, context=game_data)
        self.state_machine.unlink()
        self.finish_parse()

    def setup_parse(self: Self, input_string: str, game_data: GameData) -> None:
        """Initial parse setup."""

        self.input_string = input_string
        self.game_data = game_data

    def finish_parse(self: Self) -> None:
        """Finalize parse details."""
        pass
