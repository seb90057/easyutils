import re
import json
import pkg_resources

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
        for ct in Cast.patterns:
            path = Cast.patterns[ct]["path"]
            Cast.patterns[ct]["pattern_list"] = Cast.load_pattern(path)
        self.cast()

    def cast(self):
        for t in Cast.cast_list_ordered:
            res = Cast.is_(self.value, t)
            if res:
                self.type = t
                self.pattern = res["pattern"]
                self.comment = res["comment"]
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


if __name__ == "__main__":
    cast_list = [
        Cast("20200518"),
        Cast("0000.05"),
        Cast("10. 30"),
        Cast("4"),
        Cast("37"),
    ]
    cast_type_list = [cast.type for cast in cast_list]
    res_cast = Cast.overload_cast(cast_type_list)
    print(res_cast)
