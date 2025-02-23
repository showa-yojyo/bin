"""stat.py: The module for mahjong statistics.

This module contains function `create_player_data` and several
functions in order to evaluate player's statistical information.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final, Iterable

from .model import YAKUMAN_SCALAR, PlayerStats, ScoreSheet, YakuTable

# Mapping from special player names to key values.
DEFAULT_PLAYERS: Final = {
    "あなた": 1,
    "下家": 2,
    "対面": 3,
    "上家": 4,
}


def get_key(player_name: str) -> int:
    """Return key value for sorting a list of `player_stats`."""
    return DEFAULT_PLAYERS.get(player_name, hash(player_name))


def create_player_stats(sheet: ScoreSheet, *players: str) -> list[PlayerStats]:
    """Create new (fresh) player data objects.

    Args:
      :sheet: See `mjstat.model.create_score_records`.
      :players: A list of target players' names.

    Returns:
      A list which contains dict objects which contain 'count_rounds', 'games', and
      'name' as keys.
    """

    games: Final = sheet["games"]
    player_stats_list = list[PlayerStats]()
    for i in sorted(players, key=get_key):
        target_games = [g for g in games if i in g["players"]]
        stats = PlayerStats(
            count_rounds=sum(len(g["rounds"]) for g in target_games),
            games=target_games,
            name=i,
        )
        player_stats_list.append(stats)
    return player_stats_list


def evaluate_placing(player_stats: PlayerStats) -> None:
    """Evaluate frequency of target player's placing, or 着順表.

    This function stores the following items to `player_data`:

    :placing_disr: the numbers of 1st, 2nd, 3rd and 4th places the
    player took.
    :mean_placing: the mean place the player took.
    :first_placing_rate: the probability the player takes the
    first place in a game.
    :last_placing_rate: the probability the player takes the
    4th, or last place in a game.

    Args:
      :player_stats: See `mjstat.stat.create_player_stats`.
    """

    name: Final[str] = player_stats["name"]
    placing_distr = [0] * 4

    target_games = player_stats["games"]
    for game in target_games:
        ranking = game["result"]
        for i in range(4):
            if ranking[i]["player"] == name:
                placing_distr[i] += 1
                break

    player_stats["placing_distr"] = placing_distr

    if num_games := len(target_games):
        player_stats["mean_placing"] = (
            sum((v * i) for i, v in enumerate(placing_distr, 1)) / num_games
        )
        player_stats["first_placing_rate"] = placing_distr[0] / num_games
        player_stats["last_placing_rate"] = placing_distr[-1] / num_games
    else:
        player_stats["mean_placing"] = 0
        player_stats["first_placing_rate"] = 0
        player_stats["last_placing_rate"] = 0


DORA_RE: Final = re.compile(r"[裏赤]?ドラ(\d)+")


def count_han(yakulist: Iterable[YakuTable], concealed: bool = False) -> int:
    """Count the total number of han (doubles)."""

    total_han: int = 0
    for yaku in yakulist:
        han = yaku.value.han
        if yaku.value.has_concealed_bonus and concealed:
            han += 1
        total_han += han

    return total_han


WINNING_VALUE_RE: Final = re.compile(
    r"""
(?P<hu>\d+)符
\s*
(?P<han>.+)飜
""",
    re.VERBOSE,
)

HAN_CHAR_TABLE: Final = {k: v for v, k in enumerate("一二三四", 1)}


def evaluate_winning(player_stats: PlayerStats) -> None:
    """Evaluate target player's winning data.

    This function stores the following items to `player_stats`:

    :winning_count: the total numbers of the player's winning.
    :winning_rate:
    :winning_mean:
    :winning_mean_turn:

    Args:
      :player_stats: See `mjstat.stat.create_player_stats`.
    """

    player_stats["winning_count"] = 0
    player_stats["winning_rate"] = 0
    player_stats["winning_mean"] = 0
    player_stats["winning_mean_han"] = 0
    player_stats["winning_mean_turns"] = 0

    if not (num_rounds := player_stats["count_rounds"]):
        return

    num_winning: int = 0
    total_points: int = 0
    total_turns: int = 0
    total_han: int = 0
    name: Final[str] = player_stats["name"]
    for i in player_stats["games"]:
        # pattern must be 1G, 2G, 3G or 4G.
        index = i["players"].index(name)
        pattern = f"{index + 1:d}G"

        for round in i["rounds"]:
            if name != round.get("winner", None):
                continue

            assert round["balance"]
            total_points += round["balance"][name]
            num_winning += 1

            total_turns += sum(
                1 for j in round["action_table"] if j.startswith(pattern)
            )

            value = round["winning_value"]
            han: int
            if hu_han := WINNING_VALUE_RE.match(value):
                han = HAN_CHAR_TABLE[hu_han.group("han")]
            else:
                # Pattern 満貫 covers 満貫 itself as well as
                # 跳満, 倍満 and 三倍満.
                if value.find("満貫") != -1:
                    # Manually count how many han are.
                    is_concealed = (
                        not round["chows"][index]
                        and not round["pungs"][index]  # including 加槓
                        and not round["kongs"][index]
                    )  # only 大明槓
                    han = count_han(round["winning_yaku_list"], is_concealed)

                    han += round["winning_dora"]
                else:
                    index = value.find("役満")
                    if index > 0:
                        yakuman_prefix: str = value[:index]
                        han = 13 * YAKUMAN_SCALAR[yakuman_prefix]
                    elif index == 0:
                        han = 13
                    else:
                        raise ValueError(f"unknown winning: {value}")

            total_han += han

    if num_winning:
        player_stats["winning_count"] = num_winning
        player_stats["winning_rate"] = num_winning / num_rounds
        player_stats["winning_mean"] = total_points / num_winning
        player_stats["winning_mean_han"] = total_han / num_winning
        player_stats["winning_mean_turns"] = total_turns / num_winning


def evaluate_losing(player_stats: PlayerStats) -> None:
    """Evaluate target player's losses when he deals in an opponent player.

    This function stores the following items to `player_data`:

    :lod_count: the number the player dealt in.
    :lod_rate:
    :lod_mean:

    Args:
      :player_stats: See `mjstat.stat.create_player_data`.
    """

    player_stats["lod_count"] = 0
    player_stats["lod_rate"] = 0
    player_stats["lod_mean"] = 0
    if not (num_rounds := player_stats["count_rounds"]):
        return

    num_lod: int = 0
    total_losing_points: int = 0
    name: Final[str] = player_stats["name"]
    for i in player_stats["games"]:
        index = i["players"].index(name)
        for round in i["rounds"]:
            if (
                round["ending"] == "ロン"
                and
                # For instance, if the action table ends with
                # '... 1d3p 4A', player #4 wins from player #1.
                index == int(round["action_table"][-2][0]) - 1
            ):
                assert round["balance"]
                num_lod += 1
                # sum of negative values
                total_losing_points += round["balance"][name]

    if num_lod:
        player_stats["lod_count"] = num_lod
        player_stats["lod_rate"] = num_lod / num_rounds
        player_stats["lod_mean"] = total_losing_points / num_lod


def evaluate_riichi(player_stats: PlayerStats) -> None:
    """Evaluate target player's riichi rate.

    This function stores the following items to `player_stats`:

    :riichi_count:
    :riichi_rate:

    Args:
      :player_stats: See `mjstat.stat.create_player_data`.
    """

    player_stats["riichi_count"] = 0
    player_stats["riichi_rate"] = 0
    if not (num_rounds := player_stats["count_rounds"]):
        return

    num_riichi: int = 0
    name: Final[str] = player_stats["name"]
    for i in player_stats["games"]:
        player_index = i["players"].index(name) + 1
        riichi_mark = f"{player_index}R"
        for round in i["rounds"]:
            actions = round["action_table"]

            try:
                pos = actions.index(riichi_mark)
            except ValueError:
                continue

            rest_actions = actions[pos + 1 :]
            num_rest_actions = len(rest_actions)
            if num_rest_actions == 1 or num_rest_actions > 2:
                # the 4th riichi in a 四家立直
                # or rest_actions[0] does not deal in another
                # player.
                num_riichi += 1
                # otherwise, a deal-in.

    if num_riichi:
        player_stats["riichi_count"] = num_riichi
        player_stats["riichi_rate"] = num_riichi / num_rounds


def evaluate_melding(player_stats: PlayerStats) -> None:
    """Evaluate target player's melding rate.

    N.B. Unlike できすぎくん criteria, this function evaluates how OFTEN the player
    makes use of melding in a round.

    This function stores the following items to `player_stats`:

    :melding_count: the number the player called pung, chow, or (open) kong.
    :melding_rate:

    Args:
      :player_stats: See `mjstat.stat.create_player_data`.
    """

    player_stats["melding_count"] = 0
    player_stats["melding_rate"] = 0
    if not (num_rounds := player_stats["count_rounds"]):
        return

    num_melding: int = 0
    name: Final[str] = player_stats["name"]
    for game in player_stats["games"]:
        pos = game["players"].index(name)
        for round in game["rounds"]:
            # If できすぎくん's style is preferred,
            # just increment num_melding one only if rhs > 1.
            num_melding += len(round["chows"][pos])
            num_melding += len(round["pungs"][pos])
            num_melding += len(round["kongs"][pos])

    if num_melding:
        player_stats["melding_count"] = num_melding
        player_stats["melding_rate"] = num_melding / num_rounds


def evaluate_yaku_frequency(player_stats: PlayerStats) -> None:
    """Count all yaku occurrences that the player wins.

    Args:
      :player_stats: See `mjstat.stat.create_player_stats`.
    """

    name: Final[str] = player_stats["name"]
    yaku_counter = Counter[YakuTable]()
    for yaku_list in (
        round["winning_yaku_list"]
        for game in player_stats["games"]
        for round in game["rounds"]
        if round.get("winner", None) == name
    ):
        yaku_counter.update(yaku_list)
    player_stats["yaku_freq"] = yaku_counter
