import abc
import re


def c_type(type_decl):
    return _LiteralCType(type_decl)


class _CType(metaclass=abc.ABCMeta):
    """
    An ABC representing a type in C. Subclasses need to be able to
    declare and instantiate variables.
    """
    @abc.abstractmethod
    def declare(self, name):
        pass

    @abc.abstractmethod
    def initialize(self, name, value):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass


type_formatters = {
    'int': str,
    'char': "'{}'".format,
}


class _LiteralCType(_CType):
    """
    Represents a type in C that can be expressed with a literal
    anywhere. (As opposed to arrays and structs, which can only have
    literals at instantiation time).
    >>> t = _LiteralCType("int")
    >>> t
    int
    >>> t.declare("value")
    'int value'
    >>> t.initialize("value", '1')
    'int value = 1'
    >>> _LiteralCType('char').initialize("value", 'a')
    "char value = 'a'"
    """
    type_spec = re.compile(r'(\w+)\s*(\**)\s*((\[\d+\])*)')

    def __init__(self, type_decl):
        self.base_type, self.stars, self.arrays, _ = self.type_spec.match(
            type_decl).groups()

    def declare(self, name):
        return '{} {}'.format(
            self.base_type,
            name,
        )

    def initialize(self, name, value):
        return '{} {}{}{} = {}'.format(
            self.base_type,
            self.stars,
            name,
            self.arrays,
            type_formatters[self.base_type](value),
        )

    def __repr__(self):
        return '{}{}{}'.format(
            self.base_type,
            self.stars,
            self.arrays,
        )


