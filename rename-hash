#!/usr/bin/env python

from hashlib import md5
from os import rename
from pathlib import Path
from typing import Iterable

import click


def newname(data: bytes, path: Path) -> Path:
    """Rename a file based on its hash value."""
    return path.parent / f"{md5(data).hexdigest()}{path.suffix}"


@click.command()
@click.argument("paths", nargs=-1, type=click.Path())
@click.help_option(help="Print this message and exit.")
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    help="Don't actually rename; just print them.",
)
def main(paths: Iterable[click.Path], dry_run: bool) -> None:
    """Rename files to their hash values."""

    for oldname in paths:
        with open(oldname, "rb") as input:
            data = input.read()
        try:
            old_path = Path(oldname)
            if dry_run:
                click.echo(f"{old_path} => {newname(data, old_path)}")
            else:
                rename(old_path, newname(data, old_path))
        except FileExistsError:
            if dry_run:
                click.echo(f"remove({oldname})")
            else:
                remove(oldname)


if __name__ == "__main__":
    main()
