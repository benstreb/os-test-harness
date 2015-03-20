import abc

from .utils import new_name


class TypeValue(metaclass=abc.ABCMeta):
    """
    A value and type combo needed for codegen.
    >>> from . import types
    >>> unnamed = TypeValue(1, types.c_type('int'))
    >>> unnamed
    TypeValue(value=1, type=int, name='...')
    >>> unnamed.name is not None
    True
    >>> TypeValue(1, types.c_type('int'), name='test')
    TypeValue(value=1, type=int, name='test')
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
