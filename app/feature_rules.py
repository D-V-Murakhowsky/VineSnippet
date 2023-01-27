from typing import List

from .feature_class import Feature


class FeatureRules:

    @staticmethod
    def get(list_of_features: List[str]) -> List[Feature]:
        return [Feature(feature_name) for feature_name in list_of_features]