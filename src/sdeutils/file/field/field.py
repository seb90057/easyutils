from sdeutils.file.field.cast.cast import Cast, NONE


class Field:
    def __init__(self, value_list):
        self.values = value_list
        self.cast_estimation_dict = {}
        self.estimate_cast()
        self.discrepancy = self.discrepancy()
        self.estimated_cast = self.get_cast()

    def estimate_cast(self):
        for value in self.values:
            tp = Cast(value).type
            if tp in self.cast_estimation_dict.keys():
                self.cast_estimation_dict[tp]["count"] += 1
                self.cast_estimation_dict[tp]["values"].append(value)
            else:
                self.cast_estimation_dict[tp] = {"count": 1, "values": [value]}

    def discrepancy(self):
        cast_list = [c for c in self.cast_estimation_dict.keys() if c != NONE]
        if len(cast_list) > 1:
            return True
        return False

    def get_cast(self):
        cast_list = list(set(self.cast_estimation_dict.keys()))
        if self.discrepancy:
            return Cast.overload_cast(cast_list)
        else:
            if self.cast_estimation_dict.keys():
                return list(self.cast_estimation_dict.keys())[0]
            else:
                return None

    def __str__(self):
        res = []
        for k, v in self.cast_estimation_dict.items():
            res.append("{}: {}".format(k, v["count"]))
        return "\n".join(res)
