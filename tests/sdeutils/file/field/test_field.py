import unittest
from sdeutils.file.field.cast.cast import DATE, INTEGER, FLOAT
from sdeutils.file.field.field import Field


class TestField(unittest.TestCase):
    def setUp(self) -> None:
        self.float_value_list = ["20200518", "0000.05", "10. 30", "4", "37"]
        self.float_field = Field(self.float_value_list)

    def test_field(self):

        expect_cst = {
            DATE: {"count": 1, "values": ["20200518"]},
            FLOAT: {"count": 2, "values": ["0000.05", "10. 30"]},
            INTEGER: {"count": 2, "values": ["4", "37"]},
        }

        self.assertDictEqual(self.float_field.cast_estimation_dict, expect_cst)
        self.assertTrue(self.float_field.estimated_cast == FLOAT)
        self.assertTrue(self.float_field.discrepancy)

    def test_get_cast(self):
        self.assertTrue(self.float_field.get_cast() == FLOAT)
