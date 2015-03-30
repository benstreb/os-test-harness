import abc

from .utils import new_name


class Value:
    """
    A type-inferred value.
    >>> unnamed = Value(1)
    >>> unnamed
    Value(1, name='...')
    >>> unnamed.name is not None
    True
    >>> Value(1, 'number')
    Value(1, name='number')
    >>> Value(1, 'number', 'int')
    Value(1, name='number', type='int')
    """
    def __init__(self, value, name=None, type=None):
        self.value = value
        self.name = name if name is not None else new_name()
        self.type = type

    def __repr__(self):
        if self.type is None:
            format_str = "Value({}, name='{}')"
        else:
            format_str = "Value({}, name='{}', type='{}')"
        return format_str.format(repr(self.value), self.name, self.type)


class TypeValue(metaclass=abc.ABCMeta):
    """
    A value and type combo needed for codegen.
    >>> from . import types
    >>> TypeValue(1, types.c_type('int'), name='test')
    TypeValue(value=1, type=int, name='test')
    >>> unnamed = TypeValue(1, types.c_type('int'))
    >>> unnamed
    TypeValue(value=1, type=int, name='...')
    >>> unnamed.name is not None
    True
    >>> unnamed.initialize()
    'int ... = 1'
    """
    def __init__(self, value, type, name=None):
        self.value = value
        self.type = type
        self.name = name if name is not None else new_name()

    def __repr__(self):
        return "TypeValue(value={}, type={}, name='{}')".format(
            self.value,
            self.type,
            self.name,
        )

    def initialize(self):
        return self.type.initialize(self.name, self.value)
