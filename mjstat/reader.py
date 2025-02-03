"""reader.py: Define class MJScoreReader."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import Namespace
    from typing import Any, Self

from docutils.readers import Reader  # type: ignore[import-untyped]
from .model import create_score_records


class MJScoreReader(Reader):  # type: ignore[misc]
    """Read and parse the content of mjscore.txt."""

    def __init__(self: Self) -> None:
        super().__init__()
        self.document = None

    def get_transforms(self: Self) -> None:
        pass

    def parse(self: Self) -> None:
        self.document = document = self.new_document()  # type: ignore[assignment]

        parser = self.parser
        assert parser
        assert isinstance(self.input, str)
        parser.parse(self.input, document)

    def new_document(self: Self) -> dict[str, Any]:
        settings: Namespace = self.settings
        return create_score_records(settings)
