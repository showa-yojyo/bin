#!/usr/bin/env python
"""mjscore.py: Parse mjstat.txt and produce some statistics.

Usage:
  mjscore.py [--help] [--version]
  mjscore.py [--today] [--verbose] [--input <FILE> ...]
    [-l | --language <langspec>]
    [-T | --target <playerspec>]
    [-c | --config <FILE>]
"""

from __future__ import annotations
from argparse import Namespace
from configparser import ConfigParser
import pathlib

import click

from docutils.io import StringInput, FileInput, FileOutput, Input  # type: ignore
from mjstat.reader import MJScoreReader
from mjstat.parser import MJScoreParser
from mjstat.writer import MJScoreWriter
from mjstat.model import apply_transforms, merge_games

__version__ = "1.1"

APP_NAME = "mjscore"

def get_default_config_path() -> pathlib.Path:
    """Return the path of default configuration file."""
    return pathlib.Path(click.get_app_dir(APP_NAME, force_posix=False)) / "mjscore.conf"


def read_settings(
    ctx: click.Context,
    param: click.Option,
    conf_path: None | pathlib.Path) -> pathlib.Path:
    """Read mjscore.conf to configure."""

    conf_parser = ConfigParser()
    if not conf_path:
        conf_path = get_default_config_path()

    conf_parser.read(conf_path)
    defaults = dict(conf_parser.items("General"))

    ctx.default_map = defaults

    return conf_path


@click.command()
@click.argument(
    "input",
    nargs=-1,
    metavar="/path/to/mjscore.txt",
)
@click.help_option(help="show this message and exit")
@click.version_option(__version__, help="show the version and exit")
@click.option("-v", "--verbose", is_flag=True, help="enable verbose mode")
@click.option(
    "-l",
    "--language",
    metavar="LANG",
    type=str,
    default="en",
    help="set the language (ISO 639-1) for output",
)
@click.option(
    "--today",
    is_flag=True,
    help="set reference period to today",
)
@click.option(
    "--since",
    "--after",
    type=str,  # click.DateTime(),
    metavar="DATE",
    help="analyze statistics more recent than a specific date",
)
@click.option(
    "--until",
    "--before",
    type=str,  # click.DateTime(),
    metavar="DATE",
    help="analyze statistics older than a specific date",
)
@click.option(
    "-T",
    "--target-player",
    type=str,
    default="あなた",
    metavar="NAME",
    help="specify the target player of statistics",
)
@click.option(
    "-F",
    "--fundamental",
    is_flag=True,
    help="produce fundamental statistics",
)
@click.option("-Y", "--yaku", is_flag=True, help="produce frequency of yaku")
@click.option("-D", "--debug", is_flag=True, help="for developer's use only")
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, path_type=pathlib.Path),
    default=None,
    metavar="FILE",
    callback=read_settings,
    is_eager=True,
    expose_value=False,
    help="path to config file",
)
@click.pass_context
def main(ctx: click.Context, *args, **kwargs) -> int:
    """A simple parser for mjscore.txt.

    \b
    Examples:
    mjscore -F --today /path/to/mjscore.txt
    \b
    Debug Examples:
    mjscore -D
    mjscore -D -T all
    mjscore -D -F
    mjscore -D -F -T all
    """

    if ctx.default_map:
        kwargs.update(ctx.default_map)

    mjscore = args or kwargs.get("input", "")
    nskwargs = Namespace(**kwargs)

    sources: list[Input] = []

    if nskwargs.debug:
        from mjstat.testdata import TEST_INPUT
        sources.append(StringInput(source=TEST_INPUT))
    else:
        # XXX
        if isinstance(mjscore, (list, tuple)):
            sources.extend(
                FileInput(
                    source_path=i,
                    encoding="sjis",
                    mode="r",
                )
                for i in mjscore
            )
        else:
            sources.append(
                FileInput(
                    source_path=mjscore,
                    encoding="sjis",
                    mode="r",
                )
            )

    parser = MJScoreParser()
    reader = MJScoreReader()

    game_data_list = tuple(reader.read(src, parser, nskwargs) for src in sources)  # type: ignore[arg-type]
    game_data = merge_games(game_data_list)
    apply_transforms(game_data)

    writer = MJScoreWriter()
    writer.write(game_data, FileOutput(None))  # type: ignore[arg-type]
    return 0


if __name__ == "__main__":
    main()
