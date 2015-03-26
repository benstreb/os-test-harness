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


class _ArrayCType(_CType):
    """
    Represents an array in C.
    >>> t = _ArrayCType("int", 3)
    >>> t.declare('array')
    'int array[3]'
    >>> t.initialize('array', [1, 2, 3])
    'int array[3] = {1, 2, 3}'
    """

    def __init__(self, base_type, length):
        self.base_type = c_type(base_type)
        self.length = length

    def declare(self, name):
        return '{}[{}]'.format(self.base_type.declare(name), self.length)

    def initialize(self, name, value):
        return '{}[{}] = {{{}}}'.format(
            self.base_type.declare(name),
            self.length,
            ', '.join(
                self.base_type.literal(v) for v in value
            )
        )

    def __repr__(self):
        raise NotImplementedError()
