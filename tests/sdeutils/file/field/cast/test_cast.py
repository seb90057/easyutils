import unittest
from sdeutils.file.field.cast.cast import (
    Cast,
    DATE,
    INTEGER,
    FLOAT,
    BOOLEAN,
    NONE,
    STRING,
)


class TestCast(unittest.TestCase):
    def setUp(self) -> None:
        for cast_type, cast_object in Cast.patterns.items():
            patterns = Cast.load_pattern(cast_object["path"])
            cast_object["pattern_list"] = patterns

    def test_is_date(self):

        value_list = ["27/01/1983", "27/1/1983", "31/01/1961", "19830127"]
        for value in value_list:
            self.assertTrue(Cast.is_(value, DATE), msg="{}".format(value))

    def test_is_integer(self):
        value_list = ["10", "10,0", "10.0", "10 0.0", " 10 0.0", "1 0 . 00 0"]
        for value in value_list:
            self.assertTrue(Cast.is_(value, INTEGER), msg="{}".format(value))

    def test_is_float(self):
        value_list = [
            "10.3",
            "10,3",
            "10. 3",
            "10 000.3",
            " 10 000.345 00",
            "10 000 . 3",
        ]
        for value in value_list:
            self.assertTrue(Cast.is_(value, FLOAT), msg="{}".format(value))

    def test_is_boolean(self):
        value_list = ["true", "FALse", "faux", "vrai", "1", "0"]
        for value in value_list:
            self.assertTrue(Cast.is_(value, BOOLEAN), msg="{}".format(value))

    def test_is_none(self):
        value_list = [""]
        for value in value_list:
            self.assertTrue(Cast.is_(value, NONE), msg="{}".format(value))

    def test_cast(self):
        value = "19830127"
        c_type = Cast(value).type
        self.assertTrue(c_type == DATE, msg="{}".format(value))

        value = "1"
        c_type = Cast(value).type
        self.assertTrue(c_type == INTEGER, msg="{}".format(value))

        value = "19834699"
        c_type = Cast(value).type
        self.assertTrue(c_type == INTEGER, msg="{}".format(value))

        value = "19834699-3"
        c_type = Cast(value).type
        self.assertTrue(c_type == STRING, msg="{}".format(value))

        value = "19834699.3"
        c_type = Cast(value).type
        self.assertTrue(c_type == FLOAT, msg="{}".format(value))

    def test_cast_list(self):
        cast_list = [
            Cast("19"),
            Cast("04/10/2008"),
            Cast("vrai"),
            Cast("ok dac"),
            Cast("37"),
        ]
        expected = {"INTEGER": 2, "DATE": 1, "BOOLEAN": 1, "STRING": 1}
        res = Cast.cast_list(cast_list)
        self.assertDictEqual(res, expected)

    def test_overload_cast(self):
        cast_list = [
            Cast("19"),
            Cast("04/10/2008"),
            Cast("vrai"),
            Cast("ok dac"),
            Cast("37"),
        ]
        cast_type_list = [cast.type for cast in cast_list]
        res_cast = Cast.overload_cast(cast_type_list)
        self.assertTrue(res_cast == STRING, msg=res_cast)

        cast_list = [
            Cast("20200518"),
            Cast("0000.05"),
            Cast("10. 30"),
            Cast("4"),
            Cast("37"),
        ]
        cast_type_list = [cast.type for cast in cast_list]
        res_cast = Cast.overload_cast(cast_type_list)
        self.assertTrue(res_cast == FLOAT, msg=res_cast)

        cast_list = [Cast("20200518"), Cast("5"), Cast("10"), Cast("37")]
        cast_type_list = [cast.type for cast in cast_list]
        res_cast = Cast.overload_cast(cast_type_list)
        self.assertTrue(res_cast == INTEGER, msg=res_cast)
