import time
from functools import wraps

import numpy as np
import pandas as pd
import swifter

from .feature_rules import FeatureRules

feature_rules = FeatureRules

NUMBER_OF_ITERATIONS = 5


def timeit(N):
    def timeit_outer(func):
        @wraps(func)
        def timeit_inner(*args, **kwargs):
            start_time = time.perf_counter()
            for _ in range(N):
                func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            print(f'Function {func.__name__} Took {total_time:.4f} seconds while launching {N} times')
        return timeit_inner
    return timeit_outer


class ClassWithMethods:

    @staticmethod
    @timeit(NUMBER_OF_ITERATIONS)
    def current_edition(df: pd.DataFrame, file_schema=None):
        _file_schema = file_schema if file_schema else {}

        for i, row in df.iterrows():
            for feature in feature_rules.get(['Year', 'Capacity']):
                feature_value = ""
                for k, v in row.items():

                    if not isinstance(v, str):
                        v = str(v)

                    if v.isnumeric() or v == '' or k in ['raw_data', 'Status']:
                        continue

                    value, cell, _, _ = feature.extract_mf_from_cell(v)

                    if value and (value not in feature_value):
                        feature_value = f"{feature_value} {value}"
                        df.at[i, k] = cell

                if feature_value:
                    df.at[i, feature.name] = feature_value.strip()
        if "Type" in df:
            df['Type'] = df['Type'].fillna('')
            _file_schema["Type"] = "Type"
        if 'Condition_comments' in df:
            df['Condition_comments'] = df['Condition_comments'].fillna('')
            _file_schema["Condition_comments"] = "Condition_comments"
        else:
            df["Condition_comments"] = ""
        df["Condition"] = df["Condition_comments"].str.len() > 0
        _file_schema["Condition"] = "Condition"
        return df, _file_schema

    @staticmethod
    def _extract(cell: str):
        resp = []
        for feature_iter in feature_rules.get(['Year', 'Capacity']):
            val, cell, _, _ = feature_iter.extract_mf_from_cell(cell)
            resp.append(val)
        resp.append(cell)
        return resp

    @classmethod
    @timeit(NUMBER_OF_ITERATIONS)
    def something_new(cls, df: pd.DataFrame, file_schema=None):
        _df = df[[c for c in df.columns if c not in file_schema]]
        _df = _df.applymap(cls._extract).dropna(how='all', axis=1)

        response = _df.applymap(lambda x: x[2])
        response['Year'] = _df.\
            applymap(lambda x: x[0]).\
            apply(lambda x: ''.join(list(filter(lambda x: x is not None, set(x)))))
        response['Capacity'] = _df.\
            applymap(lambda x: x[1]).\
            apply(lambda x: ''.join(list(filter(lambda x: x is not None, set(x)))))

        return response, file_schema

    @classmethod
    @timeit(NUMBER_OF_ITERATIONS)
    def something_new_swifter(cls, df: pd.DataFrame, file_schema=None):
        _df = df[[c for c in df.columns if c not in file_schema]]
        _df = _df.swifter.progress_bar(False).applymap(cls._extract).dropna(how='all', axis=1)

        response = _df.swifter.progress_bar(False).applymap(lambda x: x[2])
        response['Year'] = _df.swifter.progress_bar(False).\
            applymap(lambda x: x[0]).\
            apply(lambda x: ''.join(list(filter(lambda x: x is not None, set(x)))))
        response['Capacity'] = _df.swifter.progress_bar(False).\
            applymap(lambda x: x[1]).\
            apply(lambda x: ''.join(list(filter(lambda x: x is not None, set(x)))))

        return response, file_schema

    @classmethod
    @timeit(NUMBER_OF_ITERATIONS)
    def vectorized_new(cls, df: pd.DataFrame, file_schema=None):
        _df = df[[c for c in df.columns if c not in file_schema]]
        _df = _df.applymap(cls._extract).dropna(how='all', axis=1)

        response = _df.applymap(lambda x: x[2])
        response['Year'] = np.apply_along_axis(lambda y: ' '.join(list(filter(lambda y: y is not None, set(y)))),
                                               1, _df.applymap(lambda x: x[0]).values)
        response['Capacity'] = np.apply_along_axis(lambda y: ' '.join(list(filter(lambda y: y is not None, set(y)))),
                                                   1, _df.applymap(lambda x: x[1]).values)

        return response, file_schema

