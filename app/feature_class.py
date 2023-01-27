import re
from typing import Tuple, Union


class Feature:

    _regex = {'Year': r'\d{4}',
              'Capacity': r'\d{1,3} ml'}

    @property
    def name(self):
        return self._name

    def __init__(self, feature_name: str):
        self._re = self._regex[feature_name]
        self._name = feature_name

    def extract_mf_from_cell(self, cell_value: str) -> Tuple[Union[str, None], str, str, str]:
        if value := re.search(self._re, cell_value):
            cell = cell_value.replace(value.group(0), '')
            return value.group(0), cell, '', ''
        else:
            return None, cell_value, '', ''
