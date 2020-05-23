from sdeutils.file.field.field import Field
from sdeutils.file.field.cast.cast import Cast, STRING


class ColumnField:
    def __init__(self, values):
        self.field_list = [Field(value) for value in values]
        self.column_cast = self.get_column_cast()
        self.best_type = self.column_cast[0]
        self.refined_values = [
            f.cast_dict[self.best_type].casted_value for f in self.field_list
        ]

    def get_column_cast(self):
        cast_type_list = Cast.get_ordered_cast_type()
        res = []
        for cast_tpe in cast_type_list:
            if all([f.cast_dict[cast_tpe].is_casted for f in self.field_list]):
                res.append(cast_tpe)

        return res

    def get_header_compatibility(self, header):
        header_type = Field(header).get_valid_casts()[0]
        if header_type == self.best_type and header_type != STRING:
            return False
        else:
            return True
