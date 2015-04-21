import abc

from .utils import new_name


class Value:
    """
    A type-inferred value.
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


class Declaration(metaclass=abc.ABCMeta):
    """
    Represents a declaration - a type, a name, and a value
    """
    def __init__(self, value, type, name=None):
        self.value = value
        self.type = type
        self.name = name if name is not None else new_name()

    def __repr__(self):
        return "Declaration(value={}, type={}, name='{}')".format(
            self.value,
            self.type,
            self.name,
        )

    def initialize(self):
        return self.type.initialize(self.name, self.value)
