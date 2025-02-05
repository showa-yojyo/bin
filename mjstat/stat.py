"""stat.py: The module for mahjong statistics.

This module contains function `create_player_data` and several
functions in order to evaluate player's statistical information.

Player Data Elements
======================================================================
The structure of `player_data` is like as follows::

  player_data ::= name, count_hands, game*, (placing_data,
                  winning_data, lod_data, riich_data,
                  melding_data)?, yaku_freq?;
    name ::= text;
    count_hands ::= integer;
    placing_data ::= placing_distr, mean_placing,
                     first_placing_rate, last_placing_rate;
      placing_distr ::= integer{4};
      mean_placing ::= value;
      first_placing_rate ::= value;
      last_placing_rate ::= value;
    winning_data ::= winning_count, winning_rate, winning_mean,
                     winning_mean_turns;
      winning_count ::= integer;
      winning_rate ::= value;
      winning_mean ::= value;
      winning_mean_turns ::= value;
    lod_data ::= lod_count, lod_rate, lod_mean;
      lod_count ::= integer;
      lod_rate ::= value;
      lod_mean ::= value;
    riich_data ::= riichi_count, riichi_rate;
      riichi_count ::= integer;
      riichi_rate ::= value;
    melding_data ::= melding_count, melding_rate;
      melding_count ::= integer;
      melding_rate ::= value;
    yaku_freq ::= (Yaku -> integer)*

Also see class `Yaku` and class `YakuTable` in module `mjstat.model`.
"""

from __future__ import annotations
from collections import Counter
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing import Iterable

from .model import YakuTable, YAKUMAN_SCALAR

type GameData = dict[str, Any]
type PlayerData = dict[str, Any]

# Mapping from special player names to key values.
DEFAULT_PLAYERS = {
    "あなた": 1,
    "下家": 2,
    "対面": 3,
    "上家": 4,
}


def get_key(player_name: str) -> int:
    """Return key value for sorting a list of `player_data`."""
    return DEFAULT_PLAYERS.get(player_name, hash(player_name))


def create_player_data(game_data: GameData, *players: str) -> list[PlayerData]:
    """Create new (fresh) player data objects.

    Args:
        game_data (dict): See `mjstat.model.create_score_records`.
        players (vararg): A list of target players' names.

    Returns:
        A list which contains dict objects which contain
        'count_hands', 'games', and 'name' as keys.
    """

    games = game_data["games"]
    data_list = []
    for i in sorted(players, key=get_key):
        target_games = [g for g in games if i in g["players"]]
        data = dict(
            count_hands=sum(len(g["hands"]) for g in target_games),
            games=target_games,
            name=i,
        )
        data_list.append(data)
    return data_list


def evaluate_placing(player_data: PlayerData) -> None:
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
        player_data (dict): See `mjstat.stat.create_player_data`.
    """

    player_data.update(
        placing_distr=[],
        mean_placing=0,
        first_placing_rate=0,
        last_placing_rate=0,
    )

    name = player_data["name"]
    placing_distr = [0] * 4

    target_games = player_data["games"]
    for game in target_games:
        ranking = game["result"]
        for i in range(4):
            if ranking[i]["player"] == name:
                placing_distr[i] += 1
                break

    player_data["placing_distr"] = placing_distr

    num_games = len(target_games)
    if num_games:
        player_data.update(
            mean_placing=sum((v * i) for i, v in enumerate(placing_distr, 1))
            / num_games,
            first_placing_rate=placing_distr[0] / num_games,
            last_placing_rate=placing_distr[-1] / num_games,
        )


DORA_RE = re.compile(r"[裏赤]?ドラ(\d)+")


def count_han(yakulist: Iterable[YakuTable], concealed: bool = False) -> int:
    """Count the total number of han (doubles)."""

    total_han = 0
    for yaku in yakulist:
        han = yaku.value.han
        if yaku.value.has_concealed_bonus and concealed:
            han += 1
        total_han += han

    return total_han


WINNING_VALUE_RE = re.compile(
    r"""
(?P<hu>\d+)符
\s*
(?P<han>.+)飜
""",
    re.VERBOSE,
)

HAN_CHAR_TABLE = {k: v for v, k in enumerate("一二三四", 1)}


def evaluate_winning(player_data: PlayerData) -> None:
    """Evaluate target player's winning data.

    This function stores the following items to `player_data`:

    :winning_count: the total numbers of the player's winning.
    :winning_rate: the probability the player wins in a hand.
    :winning_mean: the mean point the winner won par a hand.
    :winning_mean_turn: the mean turn the winner tsumo,
    or pick tiles from the wall par a hand.

    Args:
        player_data (dict): See `mjstat.stat.create_player_data`.
    """

    player_data.update(
        winning_count=0,
        winning_rate=0,
        winning_mean=0,
        winning_mean_han=0,
        winning_mean_turns=0,
    )

    num_hands = player_data["count_hands"]
    if not num_hands:
        return

    num_winning = 0
    total_points = 0
    total_turns = 0
    total_han = 0
    name = player_data["name"]
    for i in player_data["games"]:
        # pattern must be 1G, 2G, 3G or 4G.
        index = i["players"].index(name)
        pattern = f"{index + 1:d}G"

        for hand in i["hands"]:
            if name != hand.get("winner", None):
                continue

            assert hand["balance"]
            total_points += hand["balance"][name]
            num_winning += 1

            total_turns += sum(1 for j in hand["action_table"] if j.startswith(pattern))

            value = hand["winning_value"]
            hu_han = WINNING_VALUE_RE.match(value)
            if hu_han:
                han = HAN_CHAR_TABLE[hu_han.group("han")]
            else:
                # Pattern 満貫 covers 満貫 itself as well as
                # 跳満, 倍満 and 三倍満.
                if value.find("満貫") != -1:
                    # Manually count how many han are.
                    is_concealed = (
                        not hand["chows"][index]
                        and not hand["pungs"][index]  # including 加槓
                        and not hand["kongs"][index]
                    )  # only 大明槓
                    han = count_han(hand["winning_yaku_list"], is_concealed)

                    han += hand["winning_dora"]
                else:
                    index = value.find("役満")
                    if index > 0:
                        han = 13 * YAKUMAN_SCALAR[value[:index]]
                    elif index == 0:
                        han = 13
                    else:
                        raise ValueError(f"unknown winning: {value}")

            total_han += han

    if num_winning:
        player_data.update(
            winning_count=num_winning,
            winning_rate=num_winning / num_hands,
            winning_mean=total_points / num_winning,
            winning_mean_han=total_han / num_winning,
            winning_mean_turns=total_turns / num_winning,
        )


def evaluate_losing(player_data: PlayerData) -> None:
    """Evaluate target player's losses when he deals in an opponent
    player.

    This function stores the following items to `player_data`:

    :lod_count: the number the player dealt in.
    :lod_rate: the probability the player deals in par a hand.
    :lod_mean: the mean point the player paid by dealing in.

    Args:
        player_data (dict): See `mjstat.stat.create_player_data`.
    """

    player_data.update(
        lod_count=0,
        lod_rate=0,
        lod_mean=0,
    )

    num_hands = player_data["count_hands"]
    if not num_hands:
        return

    num_lod = 0
    total_losing_points = 0
    name = player_data["name"]
    for i in player_data["games"]:
        index = i["players"].index(name)
        for hand in i["hands"]:
            if hand["ending"] == "ロン":
                # For instance, if the action table ends with
                # '... 1d3p 4A', player #4 wins from player #1.
                if index == int(hand["action_table"][-2][0]) - 1:
                    assert hand["balance"]
                    num_lod += 1
                    # sum of negative values
                    total_losing_points += hand["balance"][name]

    if num_lod:
        player_data.update(
            lod_count=num_lod,
            lod_rate=num_lod / num_hands,
            lod_mean=total_losing_points / num_lod,
        )


def evaluate_riichi(player_data: PlayerData) -> None:
    """Evaluate target player's riichi rate.

    This function stores the following items to `player_data`:

    :riichi_count: the number the player successfully declared
    riichi.
    :riichi_rate: the probability the player declares riichi par
    a hand.

    Args:
        player_data (dict): See `mjstat.stat.create_player_data`.
    """

    player_data.update(
        riichi_count=0,
        riichi_rate=0,
    )
    num_hands = player_data["count_hands"]
    if not num_hands:
        return

    num_riichi = 0
    name = player_data["name"]
    for i in player_data["games"]:
        player_index = i["players"].index(name) + 1
        riichi_mark = f"{player_index}R"
        for hand in i["hands"]:
            actions = hand["action_table"]

            try:
                i = actions.index(riichi_mark)
            except ValueError:
                continue

            rest_actions = actions[i + 1 :]
            if len(rest_actions) == 1 or len(rest_actions) > 2:
                # the 4th riichi in a 四家立直
                # or rest_actions[0] does not deal in another
                # player.
                num_riichi += 1
                # otherwise, a deal-in.

    if num_riichi:
        player_data.update(
            riichi_count=num_riichi,
            riichi_rate=num_riichi / num_hands,
        )


def evaluate_melding(player_data: PlayerData) -> None:
    """Evaluate target player's melding rate.

    N.B. Unlike できすぎくん criteria, this function evaluates how
    OFTEN the player makes use of melding in a hand.

    This function stores the following items to `player_data`:

    :melding_count: the number the player called pung, chow, or
    (open) kong.
    :melding_rate: the expectation the player will call pung, chow,
    or (open) kong in a hand.

    Args:
        player_data (dict): See `mjstat.stat.create_player_data`.
    """

    player_data.update(
        melding_count=0,
        melding_rate=0,
    )
    num_hands = player_data["count_hands"]
    if not num_hands:
        return

    num_melding = 0
    name = player_data["name"]
    for i in player_data["games"]:
        index = i["players"].index(name)
        for hand in i["hands"]:
            # If できすぎくん's style is preferred,
            # just increment num_melding one only if rhs > 1.
            num_melding += sum(len(hand[j][index]) for j in ("chows", "pungs", "kongs"))

    if num_melding:
        player_data.update(
            melding_count=num_melding,
            melding_rate=num_melding / num_hands,
        )


def evaluate_yaku_frequency(player_data: PlayerData) -> None:
    """Count all yaku occurrences that the player wins.

    Args:
        player_data (dict): See `mjstat.stat.create_player_data`.
    """

    name = player_data["name"]
    yaku_lists = (
        hand["winning_yaku_list"]
        for i in player_data["games"]
        for hand in i["hands"]
        if hand.get("winner", None) == name
    )

    # Class collections.Counter is useful here.
    yaku_counter = Counter[list[Any]]()
    for i in yaku_lists:
        yaku_counter.update(i)

    player_data["yaku_freq"] = yaku_counter
