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


priority = {
    FLOAT: [INTEGER, NONE],
    INTEGER: [DATE, BOOLEAN, NONE],
    STRING: [INTEGER, FLOAT, INTEGER, BOOLEAN, NONE],
    DATE: [NONE],
    NONE: [NONE],
    BOOLEAN: [NONE],
}


class Cast:
    patterns = {
        DATE: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, DATE_PATH),
        },
        INTEGER: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, INTEGER_PATH),
        },
        FLOAT: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, FLOAT_PATH),
        },
        BOOLEAN: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, BOOLEAN_PATH),
        },
        NONE: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, NONE_PATH),
        },
        STRING: {
            "pattern_list": None,
            "path": pkg_resources.resource_filename(__name__, STRING_PATH),
        },
    }

    cast_list_ordered = [DATE, INTEGER, FLOAT, BOOLEAN, NONE, STRING]

    def __init__(self, value):
        self.value = value
        self.type = None
        self.pattern = None
        self.comment = None
        self.method = None
        self.arg = None
        for ct in Cast.patterns:
            path = Cast.patterns[ct]["path"]
            Cast.patterns[ct]["pattern_list"] = Cast.load_pattern(path)
        self.cast()
        self.refined_value = getattr(Cast, self.method)(self.value, self.arg)

    def cast(self):
        for t in Cast.cast_list_ordered:
            res = Cast.is_(self.value, t)
            if res:
                self.type = t
                self.pattern = res["pattern"]
                self.comment = res["comment"]
                self.method = res["method"]
                self.arg = res.get("arg")
                break

    def __str__(self):
        res = []
        for k, v in self.__dict__.items():
            res.append("{}: {}".format(k, v))
        return "\n".join(res)

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
    def is_(elt, tpe):
        elt = str(elt)
        if tpe in [INTEGER, FLOAT]:
            elt = elt.replace(" ", "")

        if tpe in [BOOLEAN]:
            elt = elt.lower()

        pattern_list = Cast.patterns[tpe]["pattern_list"]
        for pattern in pattern_list:
            if pattern["pattern"].match(elt) is not None:
                return pattern
        return None

    @staticmethod
    def overload_cast(cast_list):
        res = list(set(cast_list))

        for c in res:
            weak_elts = priority[c]
            res = [elt if elt not in weak_elts else c for elt in res]

        res = list(set(res))
        return res[0]

    @staticmethod
    def cast_list(casts):
        res = {}
        for cst in casts:
            ct = cst.type
            if ct in res:
                res[ct] += 1
            else:
                res[ct] = 1
        return res

    @staticmethod
    def to_date(value, tr):
        return datetime.datetime.strptime(value, tr)

    @staticmethod
    def to_integer(value, tr):
        clean_value = float(str(value).replace(" ", ""))
        return int(clean_value)

    @staticmethod
    def to_float(value, tr):
        clean_value = str(value).replace(" ", "")
        return float(clean_value)

    @staticmethod
    def to_boolean(value, tr):
        if str(value).lower() in ["true", "vrai", "1"]:
            return True
        elif str(value).lower() in ["false", "faux", "0"]:
            return False
        else:
            raise Exception

    @staticmethod
    def to_string(value, tr):
        return str(value)


if __name__ == "__main__":

    c = Cast("1")

    print(c)
