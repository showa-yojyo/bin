"""model.py: Define various data types used in Riichi Mahjong.

This module contains: class `Yaku`, the structure for Mahjong yaku; class `YakuTable`,
the set of all applicable Mahjong yaku; a dictionary `yaku_map`, the mapping from yaku
names to yaku objects described above; a dictionary `yakuman_scalar`, the mapping from
yakuman grades to the multiplicand numbers; and a handful of functions for construction
of score data.
"""

from __future__ import annotations

import datetime
from enum import Enum
from itertools import chain, product
from typing import TYPE_CHECKING, NamedTuple, TypedDict

if TYPE_CHECKING:
    from argparse import Namespace
    from collections import Counter
    from typing import Final, Required, Sequence

import dateutil.parser  # type: ignore[import-untyped]

DATETIME_FORMAT = r"%Y/%m/%d %H:%M"


class Yaku(NamedTuple):
    """Properties of Mahjong yaku.

    Attributes:
      :is_concealed_only:    Determine if this yaku is concealed only.
      :has_concealed_bonus:  Determine if the han raises when concealed.
      :han:                  Han value based on OPEN hands. e.g. 清一色 -> 5 (not 6).
      :name:                 Spelling used in ``mjscore.txt``.
    """

    is_concealed_only: bool
    has_concealed_bonus: bool
    han: int
    name: str


class YakuTable(Enum):
    """A table that contains all of Mahjong yaku."""

    Yaku01 = Yaku(True, False, 1, "リーチ")
    Yaku02 = Yaku(True, False, 1, "一発")
    Yaku03 = Yaku(True, False, 1, "門前清模和")
    Yaku04 = Yaku(False, False, 1, "断ヤオ")
    Yaku05 = Yaku(True, False, 1, "平和")
    Yaku06 = Yaku(True, False, 1, "一盃口")
    Yaku07 = Yaku(False, False, 1, "自風")
    Yaku08 = Yaku(False, False, 1, "場風")
    Yaku09 = Yaku(False, False, 1, "白")
    Yaku10 = Yaku(False, False, 1, "発")
    Yaku11 = Yaku(False, False, 1, "中")
    Yaku12 = Yaku(False, False, 1, "嶺上開花")
    Yaku13 = Yaku(False, False, 1, "槍槓")
    Yaku14 = Yaku(False, False, 1, "海底撈月")
    Yaku15 = Yaku(False, False, 1, "河底撈魚")
    Yaku16 = Yaku(False, True, 1, "三色同順")
    Yaku17 = Yaku(False, True, 1, "一気通貫")
    Yaku18 = Yaku(False, True, 1, "全帯")
    Yaku19 = Yaku(True, False, 2, "七対子")
    Yaku20 = Yaku(False, False, 2, "対々和")
    Yaku21 = Yaku(False, False, 2, "三暗刻")
    Yaku22 = Yaku(False, False, 2, "混老頭")
    Yaku23 = Yaku(False, False, 2, "三色同刻")
    Yaku24 = Yaku(False, False, 2, "三槓子")
    Yaku25 = Yaku(False, False, 2, "小三元")
    Yaku26 = Yaku(True, False, 2, "ダブルリーチ")
    Yaku27 = Yaku(False, True, 2, "混一色")
    Yaku28 = Yaku(False, True, 2, "純全帯")
    Yaku29 = Yaku(True, False, 3, "二盃口")
    Yaku30 = Yaku(False, True, 5, "清一色")
    Yaku31 = Yaku(True, False, 13, "国士無双")
    Yaku32 = Yaku(True, False, 26, "国士無双１３面待")
    Yaku33 = Yaku(True, False, 13, "九連宝燈")
    Yaku34 = Yaku(True, False, 26, "九連宝燈９面待")
    Yaku35 = Yaku(True, False, 13, "天和")
    Yaku36 = Yaku(True, False, 13, "地和")
    Yaku37 = Yaku(True, False, 13, "四暗刻")
    Yaku38 = Yaku(True, False, 26, "四暗刻単騎待")
    Yaku39 = Yaku(False, False, 13, "四槓子")
    Yaku40 = Yaku(False, False, 13, "緑一色")
    Yaku41 = Yaku(False, False, 13, "清老頭")
    Yaku42 = Yaku(False, False, 13, "字一色")
    Yaku43 = Yaku(False, False, 13, "大三元")
    Yaku44 = Yaku(False, False, 13, "小四喜和")
    Yaku45 = Yaku(False, False, 26, "大四喜和")


# mapping from mjscore_name to yaku instance
YAKU_MAP: Final = {yaku.value.name: yaku for yaku in YakuTable}

# possible yakuman grades in mjscore.txt
YAKUMAN_SCALAR: Final = {
    #'':1,         # 8000, 16000
    "ダブル": 2,  # 16000, 32000
    "トリプル": 3,  # 24000, 48000
    "四倍": 4,  # 32000, 64000
    "五倍": 5,  # 40000, 80000
    "六倍": 6,  # 48000, 96000
    "超": 7,
}  # 56000, 112000


class RoundStats(TypedDict, total=False):
    """Stats for a round.

    Attributes:
      :action_table:       The sequence of all actions by players.
      :balance:            Balance of players.
      :chows:              All the chows in this round.
      :dora_table:         The collection of dora tiles.
      :ending:             (ロン|ツモ|流局|四風連打|...)
      :game:               The game that this round occurred.
      :kongs:              All the kongs in this round.
      :pungs:              All the pungs in this round.
      :seat_table:         An four-element array of the cardinal directions.
      :start_hand_table:   All starting hands of the players.
      :title:              The wind, round and repeat count (if presents).
      :winner:             The winner's name.
      :winning_dora:       The number of dora the winner of this round has won.
      :winning_value:      A pair of Fu and Han, "満貫", or more than "満貫".
      :winning_yaku_list:  The yaku that the winner has completed.
    """

    action_table: list[str]
    balance: dict[str, int]
    chows: list[list[str]]
    dora_table: list[str]
    ending: str
    game: GameStats
    kongs: list[list[str]]
    pungs: list[list[str]]
    seat_table: Required[list[str]]
    start_hand_table: Required[list[str]]
    title: Required[str]
    winner: str
    winning_dora: int
    winning_value: str
    winning_yaku_list: list[YakuTable]


class Place(TypedDict):
    """Place information.

    Attributes:
       :player: One of "あなた","下家", "対面", or "上家".
       :points: Final points
    """

    player: str
    points: int


class GameStats(TypedDict):
    """Game data.

    Attributes:
      :finished_at:  The time this match finished.
      :rounds:        The sequence of all rounds of this match.
      :players:      The array of "あなた", "下家," "対面", "上家".
      :result:       The ranking order (places) of the players of this match.
      :started_at:   The time this match started.
    """

    finished_at: str
    rounds: list[RoundStats]
    players: tuple[str, str, str, str]
    result: list[Place]
    started_at: str


class ScoreSheet(TypedDict):
    """Document model.

    Attributes:
      :games:     See GameStats.
      :settings:  Application-dependent options.
      :since:     from which date this program parses.
      :until:     to which date this program parses.
    """

    games: list[GameStats]
    settings: Namespace
    since: str
    until: str


class PlayerStats(TypedDict, total=False):
    """Stats for a player.

    Attributes:
      :count_rounds:        The number of rounds the player has played.
      :games:               The matches the player has played.
      :name:                One of "あなた","下家", "対面", or "上家".
      :first_placing_rate:  The rate of the top place
      :last_placing_rate:   The rate of the bottom place
      :placing_distr:       The numbers of times in 1st, ..., 4th place.
      :mean_placing:        The mean value of places.
      :lod_count:           The number the player has dealt in.
      :lod_mean:            Mean value of points that the player has lost by dealing in.
      :lod_rate:            Dealing-in rate.
      :melding_count:       The number of times the player has melded.
      :melding_rate:        Melding rate.
      :riichi_count:        The number of times the player has called riich.
      :riichi_rate:         Riich rate of the player.
      :winning_count:       The number of wins.
      :winning_rate:        Win rate of the player.
      :winning_mean:        Mean value of wins
      :winning_mean_han:    Mean value of numbers of han.
      :winning_mean_turns:  Mean value of turns.
      :yaku_freq:           Table of occurrences of yaku.
    """

    count_rounds: Required[int]
    games: Required[list[GameStats]]
    name: Required[str]

    first_placing_rate: float
    last_placing_rate: float
    placing_distr: list[int]
    mean_placing: float

    lod_count: int
    lod_mean: float
    lod_rate: float
    melding_count: int
    melding_rate: float
    riichi_count: int
    riichi_rate: float
    winning_count: int
    winning_rate: float
    winning_mean: float
    winning_mean_han: float
    winning_mean_turns: float
    yaku_freq: Counter[YakuTable]


def create_score_records(settings: Namespace) -> ScoreSheet:
    """Create new game data."""

    sheet = ScoreSheet(
        games=[],
        settings=settings,
        since="",
        until="",
    )
    set_reference_period(sheet)
    return sheet


def create_game_record(context: ScoreSheet) -> GameStats:
    """Create an empty game record.

    Args:
      :context: See function `create_score_records` above.

    Returns:
      A new dict object.
    """

    games = context["games"]
    game = GameStats(
        finished_at="",
        rounds=[],
        players=("",) * 4,
        result=[Place(player="", points=0)] * 4,
        started_at="",
    )
    games.append(game)
    return game


def create_round_record(context: ScoreSheet) -> RoundStats:
    """Create an empty round and store it to the current round list.

    Args:
      :context: See function `create_score_records` above.

    Returns:
      A new object of type RoundStats.
    """

    game = context["games"][-1]
    round_list = game["rounds"]
    round_stats = RoundStats(
        action_table=[],
        balance={},
        game=game,
        seat_table=[""] * 4,
        start_hand_table=[""] * 4,
        title="unknown",
        dora_table=[],
        chows=[],
        pungs=[],
        kongs=[],
    )
    round_list.append(round_stats)

    assert context["games"][-1]["rounds"][-1] == round_stats
    return round_stats


def set_reference_period(sheet: ScoreSheet) -> None:
    """Set reference period to the score records.

    Args:
      :sheet: See function `create_score_records` above.
      :settings: (argparse.Namespace): Command line arguments, etc.

    Returns:
      A new dict object.
    """

    since_date = ""
    until_date = ""
    settings = sheet["settings"]
    if settings.today:
        today_date = datetime.date.today()
        since_date = today_date.strftime(DATETIME_FORMAT)
        until_date = (today_date + datetime.timedelta(1)).strftime(DATETIME_FORMAT)
    else:
        if settings.since:
            since_date = dateutil.parser.parse(settings.since).strftime(DATETIME_FORMAT)

        if settings.until:
            until_date = dateutil.parser.parse(settings.until).strftime(DATETIME_FORMAT)

    sheet["since"] = since_date
    sheet["until"] = until_date


def find_winner(round: RoundStats) -> None:
    """Find the winner of this round.

    Args:
      :round: See function `create_round_record`.
    """

    # first_or_default
    if not (
        winner := next((x for x in round["action_table"] if x.endswith("A")), None)
    ):
        return

    index = int(winner[0]) - 1
    assert index in range(4)
    round["winner"] = round["game"]["players"][index]


def find_meldings(round: RoundStats) -> None:
    """Find meldings (tile-calls) happened in a round.

    Args:
      :round: See function `create_round_record`.
    """

    actions = round["action_table"]

    chows: list[list[str]] = [[] for i in range(4)]
    pungs: list[list[str]] = [[] for i in range(4)]
    kongs: list[list[str]] = [[] for i in range(4)]

    for i, action in enumerate(actions):
        assert len(action) > 1
        action_type = action[1]
        assert action_type in "ACDGKNRd"

        assert action[0] in "1234"
        index = int(action[0]) - 1

        prev_action = actions[i - 1] if i > 0 else None

        match action_type:
            case "C":
                assert prev_action
                chows[index].append(prev_action[2:] + action[2:])
            case "N":
                assert prev_action
                pungs[index].append(prev_action[2:])
            case "K":
                # Test if this is extending a melded pung to a kong, or 加槓.
                tile = action[2:]
                if tile in pungs[index]:
                    continue
                # Test if this is a concealed kong, or 暗槓.
                if prev_action and prev_action[1] == "G":
                    continue
                # Otherwise, this is a melded kong, or 大明槓.
                assert (not prev_action) or (prev_action[1] in "dD")
                kongs[index].append(tile)

    round["chows"] = chows
    round["pungs"] = pungs
    round["kongs"] = kongs


def apply_transforms(sheet: ScoreSheet) -> None:
    """Apply a sort of transforms to elements in `sheet`.

    Args:
      :sheet: See function `create_score_records` above.
    """

    settings = sheet["settings"]
    transforms = []
    if settings.fundamental or settings.yaku:
        transforms.append(find_winner)
    if settings.fundamental:
        transforms.append(find_meldings)

    for i in sheet["games"]:
        for transform, round in product(transforms, i["rounds"]):
            transform(round)


def merge_games(sheet_list: Sequence[ScoreSheet]) -> ScoreSheet:
    """Merge games of a collection of `sheet`s to an instance of `sheet`.

    Args:
      :sheet_list: A sequence of objects of ScoreSheet.
    """

    assert sheet_list

    if not sheet_list[0]["games"]:
        return sheet_list[0]

    sheets_sorted = sorted(
        sheet_list, key=lambda sheet: sheet["games"][0]["started_at"]
    )

    sheet = sheets_sorted[0].copy()
    sheet["games"] = list(chain.from_iterable(i["games"] for i in sheets_sorted))

    return sheet
