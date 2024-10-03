"""reader.py: Define class MJScoreReader.
"""
from argparse import Namespace
from typing import Self

from docutils.readers import Reader
from .model import create_score_records

class MJScoreReader(Reader):
    """Read and parse the content of mjscore.txt."""

    def __init__(self: Self) -> None:
        super().__init__()
        self.document = None # type: ignore[assignment]

    def get_transforms(self: Self):
        pass

    def parse(self: Self):
        self.document = document = self.new_document()

        parser = self.parser
        assert parser
        assert isinstance(self.input, str)
        parser.parse(self.input, document)

    def new_document(self: Self):
        settings: Namespace = self.settings # type: ignore[attr-defined]
        return create_score_records(settings)
