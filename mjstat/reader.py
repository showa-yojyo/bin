# -*- coding: utf-8 -*-
"""reader.py: Define class MJScoreReader.
"""
from docutils.readers import Reader
from .model import create_score_records

class MJScoreReader(Reader):
    """Read and parse the content of mjscore.txt."""

    def __init__(self):
        super().__init__()
        self.document = None

    def get_transforms(self):
        pass

    def parse(self):
        self.document = document = self.new_document()
        self.parser.parse(self.input, document)

    def new_document(self):
        return create_score_records(self.settings)
