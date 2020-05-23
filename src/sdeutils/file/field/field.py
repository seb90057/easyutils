from sdeutils.file.field.cast.cast import Cast


class Field:
    def __init__(self, value):
        self.value = value
        ordered_type = Cast.get_ordered_cast_type()
        self.cast_dict = {k: Cast(self.value, k) for k in ordered_type}

    def is_(self, cast_type):
        try:
            return self.cast_dict[cast_type].is_casted
        except KeyError:
            raise KeyError

    def get_valid_casts(self):
        valid_cast_list = [
            cst.cast_type for cst in self.cast_dict.values() if cst.is_casted
        ]
        return valid_cast_list

    def __str__(self):
        s = "is {}: {}"
        res = [s.format(k, v.is_casted) for k, v in self.cast_dict.items()]
        return "\n".join(res)


if __name__ == "__main__":
    f = Field("-2.80821394920349083")

    print(f.get_valid_casts())
