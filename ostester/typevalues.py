import abc


class TypeValue(metaclass=abc.ABCMeta):
    """
    A value and type combo needed for codegen.
    >>> from . import types
    >>> TypeValue(1, types.c_type('int'))
    TypeValue(value=1, type=int, name='...')
    """
    pass
