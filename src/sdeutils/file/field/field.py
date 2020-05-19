from sdeutils.file.field.cast.cast import Cast


class Field:
    def __init__(self, value):
        cst = Cast(value)
        self.value = value
        self.type = cst.type
        self.refined_value = cst.refined_value
