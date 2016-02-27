# -*- coding: utf-8 -*-
"""reader.py: Define class MJScoreReader.
"""
from .model import create_score_records
from docutils.readers import Reader

class MJScoreReader(Reader):

    def get_transforms(self):
        pass

    def parse(self):
        self.document = document = self.new_document()
        self.parser.parse(self.input, document)

    def new_document(self):
        # TODO: (priority: low) Design score model.
        return create_score_records(self.settings)
