"""writer.py: Define class MJScoreWriter."""

from __future__ import annotations

from itertools import product
from types import ModuleType
from typing import TYPE_CHECKING, TypedDict, cast

if TYPE_CHECKING:
    from collections.abc import Callable, Collection, MutableSequence
    from typing import Final

from docutils.io import Output  # type: ignore[import-untyped]
from jinja2 import Environment

from .languages import get_language
from .model import PlayerStats, ScoreSheet, YakuTable
from .stat import (
    create_player_stats,
    evaluate_losing,
    evaluate_melding,
    evaluate_placing,
    evaluate_riichi,
    evaluate_winning,
    evaluate_yaku_frequency,
)

type EvaluatorType = Callable[[PlayerStats], None]


class Parts(TypedDict):
    player_data: list[PlayerStats]
    options: dict[str, bool]


# class MJScoreWriter(UnfilteredWriter):
class MJScoreWriter:
    """Write score sheet to e.g. stdout."""

    def __init__(self) -> None:
        self.language: ModuleType
        self.score_sheet: ScoreSheet
        self.output: str
        self.destination: Output
        self.parts: Parts

    def write(self, sheet: ScoreSheet, destination: Output) -> str:
        """Output `sheet` into `destination`."""

        settings: Final = sheet["settings"]
        self.language = get_language(settings.language)
        self.score_sheet = sheet
        self.destination = destination

        self.translate()
        return cast(str, self.destination.write(self.output))

    def translate(self) -> None:
        """Translate `self.score_sheet` into `self.output`."""

        self.assemble_parts()
        self.output = fill_template(
            self.parts["player_data"],
            self.language,
            **self.parts["options"],
        )

    def assemble_parts(self) -> None:
        """Assemble the `self.parts` dictionary."""

        sheet = self.score_sheet
        settings = sheet["settings"]
        target_player = settings.target_player

        player_names: Collection[str]
        if target_player == "all":
            # Detect all players from game data.
            # Note: g['players'] is a tuple of str
            player_names = set()
            for g in sheet["games"]:
                player_names.update(g["players"])
        else:
            player_names = (target_player,)

        player_stats_list: Final = create_player_stats(sheet, *player_names)

        evaluators: list[EvaluatorType] = []
        if settings.fundamental:
            evaluators.extend((
                evaluate_placing,
                evaluate_winning,
                evaluate_losing,
                evaluate_riichi,
                evaluate_melding,
            ))
        if settings.yaku:
            evaluators.append(evaluate_yaku_frequency)

        for func, player in product(evaluators, player_stats_list):
            func(player)

        self.parts = Parts(
            player_data=player_stats_list,
            options=dict(fundamental=settings.fundamental, yaku=settings.yaku),
        )


def format_float(val: float) -> str:
    """Set a floating point number into a specific format."""
    return f"{val:.2f}"


def format_percentage(val: float) -> str:
    """Set a percentile into a specific format."""
    return f"{val:.2%}"


def fill_template(
    player_stats: MutableSequence[PlayerStats],
    lang: ModuleType,
    fundamental: bool,
    yaku: bool,
) -> str:
    """Build long text which shows the statistics of the target player(s)."""

    target_games: Final = player_stats[0]["games"] if player_stats else None
    if not target_games:
        return "NO DATA\n"

    env = Environment(autoescape=False)
    env.filters.update(
        format_float=format_float,
        format_percentage=format_percentage,
    )

    output_text = env.from_string(lang.tmpl_summary).render(
        count_games=len(target_games),
        started_at=target_games[0]["started_at"],
        finished_at=target_games[-1]["finished_at"],
        data=player_stats,
    )

    if fundamental:
        output_text += env.from_string(lang.tmpl_fundamental).render(data=player_stats)

    if yaku:
        yaku_name_map = {y: lang.yaku_names[i] for i, y in enumerate(YakuTable)}
        output_text += env.from_string(lang.tmpl_yaku_freq).render(
            data=player_stats,
            YakuTable=YakuTable,
            yaku_name_map=yaku_name_map,
        )

    return output_text
