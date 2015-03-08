import abc
import re


def c_type(type_decl):
    return _SimpleCType(type_decl)


class _CType(metaclass=abc.ABCMeta):
    """
    An ABC representing a type in C. Subclasses need to be able to
    declare and instantiate variables.
    """
    @abc.abstractmethod
    def initialize(self, name, value):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass


class _SimpleCType(_CType):
    """
    Represents a non-composite type in C.
    >>> t = _SimpleCType("int*[3]")
    >>> t
    int*[3]
    >>> t.initialize("values", '{1, 2, 3}')
    'int *values[3] = {1, 2, 3}'
    """
    type_spec = re.compile(r'(\w+)\s*(\**)\s*((\[\d+\])*)')

    def __init__(self, type_decl):
        self.base_type, self.stars, self.arrays, _ = self.type_spec.match(
            type_decl).groups()

    def initialize(self, name, value):
        return '{} {}{}{} = {}'.format(
            self.base_type,
            self.stars,
            name,
            self.arrays,
            value,
        )

    def __repr__(self):
        return '{}{}{}'.format(
            self.base_type,
            self.stars,
            self.arrays,
        )


