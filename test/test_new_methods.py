from pathlib import Path
from unittest import TestCase

import pandas as pd

from app.class_with_methods import ClassWithMethods


class TestAndTime(TestCase):

    def setUp(self) -> None:
        self.df = pd.read_pickle(Path(__file__).parent.resolve() / 'pkls/source.pkl').head(100)

    def test_new_one(self):
        df, file_scheme = ClassWithMethods.something_new(self.df, {})
        pass