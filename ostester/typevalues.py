import abc


class TypeValue(metaclass=abc.ABCMeta):
    """
    A value and type combo needed for codegen.
    >>> from . import types
    >>> TypeValue(1, types.c_type('int'))
    TypeValue(value=1, type=int, name='...')
    """
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __repr__(self):
        return "TypeValue(value={}, type={}, name='{}')".format(
            self.value,
            self.type,
            None
        )
