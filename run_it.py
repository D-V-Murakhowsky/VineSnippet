import logging
from pathlib import Path

import pandas as pd

from app.class_with_methods import ClassWithMethods

logging.basicConfig(level=logging.ERROR)


class RunIt:

    def __init__(self) -> None:
        df = pd.read_pickle(Path(__file__).parent.resolve() / 'pkls/source.pkl')
        self.df = pd.concat([df] * 30, axis=0).reset_index(drop=True)

    def current_one(self):
        ClassWithMethods.current_edition(self.df.copy(), {})

    def new_one(self):
        ClassWithMethods.something_new(self.df.copy(), {})

    def new_one_swifter(self):
        ClassWithMethods.something_new_swifter(self.df.copy(), {})

    def vectorized_one(self):
        ClassWithMethods.vectorized_new(self.df.copy(), {})


if __name__ == '__main__':
    runit_instance = RunIt()
    runit_instance.current_one()
    runit_instance.new_one()
    runit_instance.new_one_swifter()
    runit_instance.vectorized_one()
