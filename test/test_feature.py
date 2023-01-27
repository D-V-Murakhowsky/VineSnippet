from unittest import TestCase

from app.feature_class import Feature


class TestFeatureClass(TestCase):

    string_for_test = 'angelus 2006 750 ml'

    def test_apply(self):
        feature_1 = Feature('Year')
        feature_2 = Feature('Capacity')

        actual, _, _ = feature_1.extract_mf_from_cell(self.string_for_test)
        self.assertEqual('2006', actual)

        actual, _, _= feature_2.extract_mf_from_cell(self.string_for_test)
        self.assertEqual('750 ml', actual)
