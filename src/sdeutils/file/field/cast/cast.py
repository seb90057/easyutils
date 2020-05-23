import re
import json
import pkg_resources
import datetime

DATE = "DATE"
INTEGER = "INTEGER"
FLOAT = "FLOAT"
BOOLEAN = "BOOLEAN"
NONE = "NONE"
STRING = "STRING"

DATE_PATH = "/conf/date.json"
INTEGER_PATH = "/conf/integer.json"
FLOAT_PATH = "/conf/float.json"
BOOLEAN_PATH = "/conf/boolean.json"
NONE_PATH = "/conf/none.json"
STRING_PATH = "/conf/string.json"


class Cast:
    loaded = False

    def __init__(self, value, cast_type):
        if not Cast.loaded:
            Cast.load_patterns()

        self.cast_type = cast_type
        self.value = value
        self.arg = None
        self.casted_value = None
        self.pattern = None
        self.pattern_id = None
        self.comment = None
        self.is_casted = False
        self.cast()

    def is_(self, tpe):
        elt = str(self.value)
        if tpe in [INTEGER, FLOAT]:
            elt = elt.replace(" ", "")

        if tpe in [BOOLEAN]:
            elt = elt.lower()

        pattern_list = Cast.cast_details[tpe]["pattern_list"]
        for pattern in pattern_list:
            if pattern["pattern"].match(elt) is not None:
                return pattern
        return None

    def to_date(self):
        return datetime.datetime.strptime(self.value, self.arg)

    def to_integer(self):
        clean_value = float(str(self.value).replace(" ", ""))
        return int(clean_value)

    def to_float(self):
        if self.pattern == 2:
            m = self.pattern.search(self.value)
            clean_value = float(m.group("num")) ** float(-m.group("exp"))
        else:
            clean_value = str(self.value).replace(" ", "").replace(",", ".")
        return float(clean_value)

    def to_boolean(self):
        if str(self.value).lower() in ["true", "vrai", "1"]:
            return True
        elif str(self.value).lower() in ["false", "faux", "0"]:
            return False
        else:
            raise Exception

    def to_string(self):
        return str(self.value)

    def cast(self):
        res = self.is_(self.cast_type)
        if res:
            self.is_casted = True
            self.pattern = res["pattern"]
            self.comment = res["comment"]
            self.pattern_id = res.get("pattern_id")
            self.arg = res.get("arg")
            self.casted_value = Cast.to_(self.cast_type, self)

    cast_details = {
        DATE: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, DATE_PATH),
            "method": to_date,
            "priority": 1,
        },
        INTEGER: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, INTEGER_PATH),
            "method": to_integer,
            "priority": 3,
        },
        FLOAT: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, FLOAT_PATH),
            "method": to_float,
            "priority": 4,
        },
        BOOLEAN: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, BOOLEAN_PATH),
            "method": to_boolean,
            "priority": 2,
        },
        STRING: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, STRING_PATH),
            "method": to_string,
            "priority": 5,
        },
    }

    @staticmethod
    def to_(cast_type, cst):
        cast_method = Cast.cast_details[cast_type]["method"]
        try:
            return cast_method(cst)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def load_patterns():
        for ct in Cast.cast_details:
            path = Cast.cast_details[ct]["path"]
            Cast.cast_details[ct]["pattern_list"] = Cast.load_pattern(path)
        Cast.loaded = True

    @staticmethod
    def load_pattern(path):
        pattern_list = []
        with open(path, "r") as conf:
            patterns_dict = json.load(conf)

        for p in patterns_dict:
            pattern_dict = {}
            pattern_dict["pattern"] = re.compile(patterns_dict[p]["pattern"])
            pattern_dict["comment"] = patterns_dict[p]["comment"]
            pattern_dict["method"] = patterns_dict[p]["method"]
            try:
                pattern_dict["arg"] = patterns_dict[p]["arg"]
            except KeyError:
                pattern_dict["arg"] = ""
            pattern_list.append(pattern_dict)
        return pattern_list

    @staticmethod
    def get_ordered_cast_type():
        res = [
            k
            for k, v in sorted(
                Cast.cast_details.items(), key=lambda item: item[1]["priority"]
            )
        ]
        return res


if __name__ == "__main__":
    Cast.load_patterns()
    c = Cast("1.3", FLOAT)

    print(c.casted_value)
