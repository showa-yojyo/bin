#!/usr/bin/env python
"""mjscore.py: Parse mjstat.txt and produce some statistics.

Usage:
  mjscore.py [--help] [--version]
  mjscore.py [--today] [--verbose] [--input <FILE> ...]
    [-l | --language <langspec>]
    [-T | --target <playerspec>]
    [-c | --config <FILE>]
"""

from argparse import ArgumentParser, Namespace
from configparser import ConfigParser
from os.path import expandvars
import sys
from typing import Never, Sequence

from docutils.io import StringInput, FileInput, FileOutput, Input
from mjstat.reader import MJScoreReader
from mjstat.parser import MJScoreParser
from mjstat.writer import MJScoreWriter
from mjstat.model import apply_transforms, merge_games

__version__ = "1.0.1"

SEARCH_PATH = (
    "$XDG_CONFIG_HOME/mjscore/mjscore.conf",
    "$HOME/.config/mjscore/mjscore.conf",
    "$HOME/.mjscore/mjscore.conf",
    "$HOME/.mjscore.conf",
)


def read_settings(args: Namespace) -> ConfigParser:
    """Read settings from a dotfile"""

    config = ConfigParser()
    if args.config:
        config.read(args.config)
        return config

    # config.read([expandvars(p) for p in SEARCH_PATH])
    for p in SEARCH_PATH:
        config.read(expandvars(p))

    return config


def parse_args(args: Sequence[str]) -> Namespace:
    """Convert argument strings to objects."""

    parser = ArgumentParser(add_help=False)
    parser.add_argument("-c", "--config", metavar="FILE", help="path to config file")

    known_args, remaining_argv = parser.parse_known_args(args)

    config = read_settings(known_args)
    try:
        defaults = dict(config.items("General"))
    except Exception as ex:
        print(f"Warning: {ex}", file=sys.stderr)

    parser = ArgumentParser(
        parents=[parser], description="A simple parser for mjscore.txt."
    )

    parser.add_argument("--version", action="version", version=__version__)

    # This parameter should not be optional.
    parser.add_argument(
        "--input", nargs="+", metavar="FILE", help="path to mjscore.txt"
    )

    parser.add_argument("--verbose", action="store_true", help="enable verbose mode")

    parser.add_argument(
        "-l", "--language", default="en", help="set the language (ISO 639-1) for output"
    )

    group = parser.add_argument_group("reference period")
    group.add_argument(
        "--today", action="store_true", help="set reference period to today"
    )

    group.add_argument(
        "--since",
        "--after",
        dest="since",
        metavar="<date>",
        help="analyze statistics more recent than a specific date",
    )

    group.add_argument(
        "--until",
        "--before",
        dest="until",
        metavar="<date>",
        help="analyze statistics older than a specific date",
    )

    parser.add_argument(
        "-T",
        "--target-player",
        default="あなた",
        help="specify the target player of statistics",
    )

    parser.add_argument(
        "-F",
        "--fundamental",
        action="store_true",
        help="produce fundamental statistics",
    )

    parser.add_argument(
        "-Y", "--yaku", action="store_true", help="produce frequency of yaku"
    )

    parser.add_argument(
        "-D", "--debug", action="store_true", help="for developer's use only"
    )

    parser.set_defaults(**defaults)

    return parser.parse_args(args=remaining_argv or ("--help",))


def run(args: Namespace) -> int:
    """The main function."""

    sources: list[Input] = []
    if args.debug:
        from mjstat.testdata import TEST_INPUT

        sources.append(StringInput(source=TEST_INPUT))
    else:
        # XXX
        if isinstance(args.input, (list, tuple)):
            sources.extend(
                FileInput(source_path=i, encoding="sjis", mode="r") for i in args.input
            )
        else:
            sources.append(FileInput(source_path=args.input, encoding="sjis", mode="r"))

    parser = MJScoreParser()
    reader = MJScoreReader()

    game_data_list = tuple(reader.read(src, parser, args) for src in sources)  # type: ignore[arg-type]
    game_data = merge_games(game_data_list)
    apply_transforms(game_data)

    writer = MJScoreWriter()
    writer.write(game_data, FileOutput(None))  # type: ignore[arg-type]
    return 0


def main(args: Sequence[str] = sys.argv[1:]) -> Never:
    sys.exit(run(parse_args(args=args)))


if __name__ == "__main__":
    main()
