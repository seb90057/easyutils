import unittest
import pandas as pd
from tests.sdeutils.file import csv_file, path


class TestCsvFile(unittest.TestCase):
    def setUp(self) -> None:
        self.path = path
        self.csv_file = csv_file
        self.values = {
            "header1": ["voiture", "camion", "moto", "avion"],
            "header2": [3, 2.5, 10, 8],
            "header3": [True, False, False, True],
            "header4": [3, 4, 5, 6],
        }
        self.df = pd.DataFrame(data=self.values)

    def test_CsvFile(self):
        self.assertTrue(self.csv_file.path == self.path)
        self.assertTrue(self.csv_file.delimiter == ";")
        self.assertTrue(self.csv_file.has_header)
        self.assertListEqual(
            self.csv_file.header, ["header1", "header2", "header3", "header4"]
        )

    def test_get_basic_info(self):
        expected_dict = {
            "has_header": True,
            "delimiter": ";",
            "quotechar": '"',
            "escapechar": None,
        }
        res_dict = self.csv_file.get_basic_info()
        self.assertDictEqual(res_dict, expected_dict)

    def test_get_fields_info(self):
        expected_dict = {
            "header1": {
                "field_name": "header1",
                "values": ["voiture", "camion", "moto", "avion"],
                "cast_repartition": {"STRING": 4},
            },
            "header2": {
                "field_name": "header2",
                "values": [3, 2.5, 10, 8],
                "cast_repartition": {"INTEGER": 3, "FLOAT": 1},
            },
            "header3": {
                "field_name": "header3",
                "values": [True, False, False, True],
                "cast_repartition": {"BOOLEAN": 4},
            },
            "header4": {
                "field_name": "header4",
                "values": [3, 4, 5, 6],
                "cast_repartition": {"INTEGER": 4},
            },
        }
        res_dict = self.csv_file.get_fields_info()

        self.assertDictEqual(res_dict, expected_dict)

    def test_get_df(self):
        df = self.csv_file.get_df()

        res = df.join(self.df, lsuffix="_l", rsuffix="_r", how="inner")

        self.assertTrue(len(res.index) == len(df.index))

    def test_get_row_nb(self):
        self.assertTrue(self.csv_file.get_row_nb() == 4)

    def test_get_df_sample(self):
        # test if row nb up to existing, return whole df
        df_sample = self.csv_file.get_df_sample(max_row_nb=10)
        res = df_sample.join(self.df, lsuffix="_l", rsuffix="_r", how="inner")

        self.assertTrue(len(res.index) == len(df_sample.index))

        # test if row nb less to existing, return only sample
        df_sample = self.csv_file.get_df_sample(max_row_nb=2)
        res = df_sample.join(self.df, lsuffix="_l", rsuffix="_r", how="inner")
        self.assertTrue(len(res.index) == 2)
