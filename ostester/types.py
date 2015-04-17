import abc
import re


def c_type(type_decl):
    """
    Returns a type for the given type declaration.
    """
    type_spec = re.compile(r'(\w+)\s*(\**)\s*((\[\d+\])*)')
    base_type, stars, arrays, _ = type_spec.match(
        type_decl).groups()
    if arrays != '':
        raise NotImplementedError()
    elif stars != '':
        return Pointer(c_type(base_type + stars[1:]))
    elif base_type not in type_map:
        raise ValueError('Unsupported base type: {}'.format(base_type))
    else:
        return type_map[base_type]


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


class _SimpleCType(_CType):
    """
    Represents a non-composite type in C.
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
            self._rhs_format(value),
        )

    def __repr__(self):
        return '{}'.format(self.base_type)

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                self.base_type == other.base_type)


class Int(_SimpleCType):
    def __init__(self):
        self.base_type = 'int'

    def coerce(self, value):
        return int(value)

    def _rhs_format(self, value):
        return str(self.coerce(value))


class Char(_SimpleCType):
    def __init__(self):
        self.base_type = 'char'

    def coerce(self, value):
        s = str(value)
        if len(s) != 1:
            raise ValueError("Characters need to have length 1")
        return s

    def _rhs_format(self, value):
        return "'{}'".format(self.coerce(value))


type_map = {
    'int': Int(),
    'char': Char(),
}


class Pointer(_CType):
    """
    Represents a pointer in C.
    """

    def __init__(self, inner_type):
        self.inner_type = inner_type

    def declare(self, name):
        return '{}*{}'.format(self.inner_type, name)

    def initialize(self, name, value):
        return '{}*{} = {}'.format(self.inner_type, name, value)

    def __repr__(self):
        return '{}*'.format(self.inner_type)

    def __eq__(self, other):
        return (isinstance(other, Pointer) and
                self.inner_type == other.inner_type)
