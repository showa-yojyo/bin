"""reader.py: Define class MJScoreReader."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import Namespace

from docutils.readers import Reader  # type: ignore[import-untyped]

from .model import ScoreSheet, create_score_records


class MJScoreReader(Reader):  # type: ignore[misc]
    """Read and parse the content of mjscore.txt."""

    def __init__(self) -> None:
        super().__init__()
        self.document: ScoreSheet | None = None

    def get_transforms(self) -> None:
        pass

    def parse(self) -> None:
        self.document = document = self.new_document()

        parser = self.parser
        assert parser
        assert isinstance(self.input, str)
        parser.parse(self.input, document)

    def new_document(self) -> ScoreSheet:
        settings: Namespace = self.settings
        return create_score_records(settings)
