import re


def c_type(type_decl):
    return _CType(type_decl)


class _CType:
    """
    Represents en expression type in C.
    >>> t = _CType("int*[3]")
    >>> t
    int*[3]
    >>> t.declare("values")
    'int *values[3]'
    """
    type_spec = re.compile(r'(\w+)\s*(\**)\s*((\[\d+\])*)')

    def __init__(self, type_decl):
        self.base_type, self.stars, self.arrays, _ = self.type_spec.match(
            type_decl).groups()

    def declare(self, name):
        return '{} {}{}{}'.format(
            self.base_type,
            self.stars,
            name,
            self.arrays,
        )

    def __repr__(self):
        return '{}{}{}'.format(
            self.base_type,
            self.stars,
            self.arrays,
        )


