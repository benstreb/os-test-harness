import abc
import re


def c_type(type_decl):
    """
    Returns a type for the given type declaration.
    >>> c_type('int').base_type
    'int'
    """
    type_spec = re.compile(r'(\w+)\s*(\**)\s*((\[\d+\])*)')
    base_type, stars, arrays, _ = type_spec.match(
        type_decl).groups()
    if stars != '' or arrays != '':
        raise NotImplementedError()
    return _SimpleCType(type_decl)


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


class _SimpleCType(_CType):
    """
    Represents a non-composite type in C.
    >>> t = _SimpleCType("int")
    >>> t
    int
    >>> t.declare("value")
    'int value'
    >>> t.initialize("value", '1')
    'int value = 1'
    >>> _SimpleCType('char').initialize("value", 'a')
    "char value = 'a'"
    """

    def __init__(self, base_type):
        self.base_type = base_type

    def declare(self, name):
        return '{} {}'.format(
            self.base_type,
            name,
        )

    def initialize(self, name, value):
        return '{} {} = {}'.format(
            self.base_type,
            name,
            type_formatters[self.base_type](value),
        )

    def __repr__(self):
        return '{}'.format(self.base_type)

    def __eq__(self, other):
        return (isinstance(other, _SimpleCType) and
                self.base_type == other.base_type)


class _ArrayCType(_CType):
    """
    Represents an array in C.
    >>> t = _ArrayCType("int", 3)
    >>> t.declare('array')
    'int array[3]'
    """

    def __init__(self, base_type, length):
        self.base_type = c_type(base_type)
        self.length = length

    def declare(self, name):
        return '{}[{}]'.format(self.base_type.declare(name), self.length)

    def initialize(self, name, value):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()
