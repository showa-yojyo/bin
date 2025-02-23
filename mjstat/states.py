"""states.py: Define state classes for parsing mjscore.txt.

Summary of the transitions::

    (1) GameOpening
    -> (2) GameInitialCondition
    -> (3) RoundState
    -> (4) RoundClosing or (9) GamePlayerPlace
    (4) RoundClosing
    -> (5) RoundStartHands
    -> (6) RoundDoraSet
    -> (7) RoundActionHistory
    -> return to (3)
    (8) GamePlayerPlace
    -> (9) GameClosing
    -> return to (1)

"""

from __future__ import annotations

import re
from typing import Final, cast

from docutils.statemachine import State  # type: ignore[import-untyped]

from .model import YAKU_MAP, ScoreSheet, create_game_record, create_round_record

type TransitionResult = tuple[object, str, list[object]]

# pylint: disable=unused-argument, no-self-use


class MJScoreState(State):  # type: ignore[misc]
    """Base class of state classes."""


class GameOpening(MJScoreState):
    """(1) Parse the first line of a match."""

    game_opening_re: Final = re.compile(
        r"""
        =*\s
        東風戦：ランキング卓\s64卓\s開始\s
        (?P<timestamp>
        \d{4}/\d{2}/\d{2}\s\d{2}:\d{2}
        )\s
        =*
        """,
        re.VERBOSE,
    )

    patterns: Final = dict(
        handle_game_opening=game_opening_re,
    )
    initial_transitions: Final = [
        "handle_game_opening",
    ]

    def handle_game_opening(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """Parse a match header."""

        # Determine whether to parse this match or not.
        started_at: Final[str] = match.group("timestamp")
        since_date: Final[str] = context["since"]
        if since_date and started_at < since_date:
            return context, next_state, []

        until_date: Final[str] = context["until"]
        if until_date and until_date <= started_at:
            return context, next_state, []

        game = create_game_record(context)
        game["started_at"] = started_at

        return context, "GameInitialCondition", []


class GameInitialCondition(MJScoreState):
    """(2) Parse amount of point a player have before the start of the match, and the
    four players."""

    # Regex for parsing players information, their names and ratings.
    initial_condition_re: Final = re.compile(
        r"""
        持点\d+\s*      # e.g. 25000
        \[1\](.+)\sR(?:\d+)\s*   # Player #1
        \[2\](.+)\sR(?:\d+)\s*   # Player #2
        \[3\](.+)\sR(?:\d+)\s*   # Player #3
        \[4\](.+)\sR(?:\d+)\s*   # Player #4
        """,
        re.VERBOSE,
    )

    patterns: Final = dict(handle_initial_condition=initial_condition_re)
    initial_transitions: Final = ["handle_initial_condition"]

    def handle_initial_condition(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """Parse initial points and players."""

        game = context["games"][-1]
        game["players"] = cast(tuple[str, str, str, str], match.groups())

        return context, "RoundState", []


class RoundState(MJScoreState):
    """(3) State for a round of the opening or closing of the final round."""

    # 場 = east/south round
    # 局 = a round
    # 本場 = counter(s)
    # E.g. 東一局三本場 is translated to East, 1st round [with 0 counters].
    hand_header_re: Final = re.compile(
        r"""
        (?P<title>[東南][1-4]局\s\d本場)
        \(リーチ\d\)
        \s?
        (?P<balance>
         (
          (あなた|下家|対面|上家)\s?
          ([+-]?\d+)\s?
         ){,4}
        )?
    """,
        re.VERBOSE,
    )

    game_result_re: Final = re.compile(r"[-]+\s*試合結果\s*[-]+")

    patterns: Final = dict(
        handle_summary=hand_header_re,
        handle_game_result=game_result_re,
    )
    initial_transitions: Final = [
        "handle_summary",
        "handle_game_result",
    ]

    def handle_summary(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """Parse the header of a round."""

        round = create_round_record(context)
        round["title"] = match.group("title")
        if player_balance := match.group("balance").strip().split():
            round["balance"].update([
                (
                    player_balance[i],
                    int(player_balance[i + 1]),
                )
                for i in range(0, len(player_balance), 2)
            ])

        return context, "RoundClosing", []

    def handle_game_result(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """---- game result ----"""

        return context, "GamePlayerPlace", []


class RoundClosing(MJScoreState):
    """(4) Parse the line that contains the winner's hand or exhaustive/abortive
    draw.
    """

    winning_re: Final = re.compile(
        r"""
        (?P<winning_value>.+)
        (?P<winning_decl>(ロン|ツモ))
        \s
        (
          ((?P<winning_yaku_with_dora>.+)
            \s
            ドラ(?P<winning_dora>\d+)
          )|
          (?P<winning_yaku_without_dora>.+)
        )
    """,
        re.VERBOSE,
    )

    draw_re: Final = re.compile(
        r"(流局|九種公九牌倒牌|三家和|四風連打|四槓開|四家リーチ)"
    )

    patterns: Final = dict(
        handle_winning=winning_re,
        handle_draw=draw_re,
    )

    initial_transitions: Final = [
        "handle_winning",
        "handle_draw",
    ]

    def handle_winning(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """Parse the line that includes ロン or ツモ."""

        # Get the current hand from context.
        game = context["games"][-1]
        round = game["rounds"][-1]

        round["ending"] = match.group("winning_decl")
        round["winning_value"] = match.group("winning_value")

        if dora := match.group("winning_dora"):
            yaku_list = match.group("winning_yaku_with_dora")
            round["winning_dora"] = int(dora)
        else:
            yaku_list = match.group("winning_yaku_without_dora")
            round["winning_dora"] = 0
        round["winning_yaku_list"] = [YAKU_MAP[i] for i in yaku_list.split()]

        return context, "RoundStartHands", []

    def handle_draw(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """Parse the line that contains 流局, etc."""

        # Get the current hand from context.
        game = context["games"][-1]
        round = game["rounds"][-1]

        round["ending"] = match.group()

        return context, "RoundStartHands", []


class RoundStartHands(MJScoreState):
    """(5) State for parsing start hands (dealt tiles to players) of a round."""

    # Regex for a start hand, or a players' dealt tiles at the beginning of a hand.
    start_hand_re: Final = re.compile(
        r"""
        \[
          (?P<id>[1-4])                 # player id
          (?P<seat>[東南西北])          # seat
        \]
        (?P<start_hand>
            (
                ([1-9]m)|           # character suit, or 萬子
                (5M)|
                ([1-9]p)|           # circle suit, or 筒子
                (5P)|
                ([1-9]s)|           # bamboo suit, or 索子
                (5S)|
                ([東南西北白発中])  # honor tiles, or 字牌
            ){13}
        )                   # 13 tiles of a start hand, or 配牌
    """,
        re.VERBOSE,
    )

    patterns: Final = dict(handle_start_hands=start_hand_re)
    initial_transitions: Final = ["handle_start_hands"]

    def handle_start_hands(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """Handle lines of start hands."""

        # current hand
        game = context["games"][-1]
        round = game["rounds"][-1]

        player, seat, start_hand = match.group("id", "seat", "start_hand")
        index = int(player) - 1
        round["seat_table"][index] = seat
        round["start_hand_table"][index] = start_hand

        for _ in range(3):
            id_seat = self.start_hand_re.match(self.state_machine.next_line())
            assert id_seat
            player, seat, start_hand = id_seat.group("id", "seat", "start_hand")
            index = int(player) - 1
            round["seat_table"][index] = seat
            round["start_hand_table"][index] = start_hand

        return context, "RoundDoraSet", []


class RoundDoraSet(MJScoreState):
    """(6) State for parsing dora set of a hand."""

    # Regex for the line that indicates all of dora tiles.
    dora_set_re: Final = re.compile(
        r"""
        \[表ドラ\](?P<dora>[^\s]+)
        (\s*\[裏ドラ\](?P<uradora>.+))?      # XXX: dot matches any of tiles
    """,
        re.VERBOSE,
    )

    patterns: Final = dict(handle_dora_set=dora_set_re)
    initial_transitions: Final = ["handle_dora_set"]

    def handle_dora_set(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """Handle the line of dora tiles."""

        # current hand
        game = context["games"][-1]
        round = game["rounds"][-1]
        dora_table = round["dora_table"]

        dora_table.extend(match.group("dora", "uradora"))

        return context, "RoundActionHistory", []


class RoundActionHistory(MJScoreState):
    """(7) State for parsing the action history of a hand."""

    # Regex for lines e.g. ``* 1G3s 1d1p 2G2s 2d9p ...``
    # Do not make regex so complicated here.
    actions_re: Final = re.compile(
        r"""
        \A
        \*\s*
        (?P<actions>.+)
        \Z
    """,
        re.VERBOSE,
    )

    patterns: Final = dict(handle_actions=actions_re)
    initial_transitions: Final = ["handle_actions"]

    def handle_actions(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """Handle all the lines that describe actions."""

        # current hand
        game = context["games"][-1]
        round = game["rounds"][-1]
        action_table = round["action_table"]

        actions = match.group("actions").split()
        action_table.extend(actions)

        while True:
            line = self.state_machine.next_line()
            next_match = self.actions_re.match(line)
            if not next_match:
                break
            match = next_match
            actions = match.group("actions").split()
            action_table.extend(actions)

        return context, "RoundState", []


class GamePlayerPlace(MJScoreState):
    """(8) State for parsing player's place after a match."""

    player_place_re: Final = re.compile(
        r"""
        (?P<rank>[1-4])位
        \s+
        (?P<player>(あなた|下家|対面|上家))
        \s+
        (?P<points>[+-]?\d+)
    """,
        re.VERBOSE,
    )

    patterns: Final = dict(handle_player_place=player_place_re)
    initial_transitions: Final = ["handle_player_place"]

    def handle_player_place(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """Parse a rank line of the ranking list in a game."""

        game = context["games"][-1]
        ranking = game["result"]

        for i in range(4):
            pos = int(match.group("rank")) - 1
            ranking[pos]["player"] = match.group("player")
            ranking[pos]["points"] = int(match.group("points"))
            if i < 3:
                line = self.state_machine.next_line()
                next_match = self.player_place_re.match(line)
                assert next_match
                match = next_match

        return context, "GameClosing", []


class GameClosing(MJScoreState):
    """(9) Parse the last line of a match."""

    game_closing_re: Final = re.compile(
        r"""
        [-]*\s64卓\s終了\s
        (?P<timestamp>
        \d{4}/\d{2}/\d{2}\s\d{2}:\d{2}
        )
        \s
        [-]*
    """,
        re.VERBOSE,
    )

    patterns: Final = dict(handle_game_closing=game_closing_re)
    initial_transitions: Final = [
        "handle_game_closing",
    ]

    def handle_game_closing(
        self,
        match: re.Match[str],
        context: ScoreSheet,
        next_state: str,
    ) -> TransitionResult:
        """Parse the ending of a match."""

        game = context["games"][-1]
        game["finished_at"] = match.group("timestamp")

        return context, "GameOpening", []
