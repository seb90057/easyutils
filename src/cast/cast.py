import re
import json

DATE = 'DATE'
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
BOOLEAN = 'BOOLEAN'
NONE = 'NONE'
STRING = 'STRING'


priority = {
    FLOAT: [INTEGER, NONE],
    INTEGER: [DATE, BOOLEAN, NONE],
    STRING: [INTEGER, FLOAT, INTEGER, BOOLEAN, NONE],
    DATE: [NONE],
    NONE: [NONE],
    BOOLEAN: [NONE]

}


class Cast:
    patterns = {DATE: {'pattern_list': None,
                       'path': r'C:\Users\sebde\PycharmProjects\easyfile\src\conf\date.json'},
                INTEGER: {'pattern_list': None,
                          'path': r'C:\Users\sebde\PycharmProjects\easyfile\src\conf\integer.json'},
                FLOAT: {'pattern_list': None,
                        'path': r'C:\Users\sebde\PycharmProjects\easyfile\src\conf\float.json'},
                BOOLEAN: {'pattern_list': None,
                          'path': r'C:\Users\sebde\PycharmProjects\easyfile\src\conf\boolean.json'},
                NONE: {'pattern_list': None,
                       'path': r'C:\Users\sebde\PycharmProjects\easyfile\src\conf\none.json'},
                STRING: {'pattern_list': None,
                       'path': r'C:\Users\sebde\PycharmProjects\easyfile\src\conf\string.json'},
                }

    cast_list_ordered = [DATE, INTEGER, FLOAT, BOOLEAN, NONE, STRING]

    def __init__(self, value):
        self.value = value
        self.type = None
        self.pattern = None
        self.comment = None
        for ct in Cast.patterns:
            path = Cast.patterns[ct]['path']
            Cast.patterns[ct]['pattern_list'] = Cast.load_pattern(path)
        self.cast()

    def cast(self):
        for t in Cast.cast_list_ordered:
            res = Cast.is_(self.value, t)
            if res:
                self.type = t
                self.pattern = res['pattern']
                self.comment = res['comment']
                break

    def __str__(self):
        res = []
        for k, v in self.__dict__.items():
            res.append('{}: {}'.format(k, v))
        return '\n'.join(res)


    @staticmethod
    def load_pattern(path):
        pattern_list = []
        with open(path, 'r') as conf:
            patterns_dict = json.load(conf)

        for p in patterns_dict:
            pattern_dict = {}
            pattern_dict['pattern'] = re.compile(patterns_dict[p]['pattern'])
            pattern_dict['comment'] = patterns_dict[p]['comment']
            pattern_list.append(pattern_dict)
        return pattern_list

    @staticmethod
    def clean_elt(elt):
        return elt.replace(' ', '')

    @staticmethod
    def is_(elt, tpe):
        elt = str(elt)
        pattern_list = Cast.patterns[tpe]['pattern_list']
        for pattern in pattern_list:
            if pattern['pattern'].match(elt) is not None:
                return pattern
        return None

    @staticmethod
    def overload_cast(cast_list):
        tmp = cast_list
        for c in cast_list:
            welts = priority[c]
            tmp = [c if e in welts else e for e in tmp]
            tmp = list(set(tmp))

        return tmp[0]

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


if __name__ == '__main__':
    # c = Cast('coucou')
    # print(c)

    elt_list = ['1', '1,1', 'test', '2']
    cl = [Cast(elt) for elt in elt_list]
    print(json.dumps(Cast.cast_list(cl)))
