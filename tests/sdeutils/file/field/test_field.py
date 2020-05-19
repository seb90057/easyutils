import unittest
from sdeutils.file.field.cast.cast import DATE
from sdeutils.file.field.field import Field
import datetime


class TestField(unittest.TestCase):
    def setUp(self) -> None:
        self.date_value = "27/01/1983"
        self.date_field = Field(self.date_value)

    def test_field(self):
        self.assertTrue(self.date_field.type == DATE)
        exp_dt = datetime.datetime(1983, 1, 27)
        self.assertTrue(self.date_field.refined_value == exp_dt)
