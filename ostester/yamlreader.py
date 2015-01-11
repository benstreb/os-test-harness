import collections.abc
from io import StringIO

import yaml

import ast


def parse(file):
    return yaml.safe_load(file)


def parse_from_string(string):
    return parse(StringIO(string))


class Zeros(collections.abc.Sequence):
    """
    Represents a zeroed region of memory in C
    >>> yaml.load("!zeros 5")
    Zeros(5)
    >>> yaml.dump(Zeros(3))
    "!zeros '3'\\n"
    >>> list(Zeros(7))
    [0, 0, 0, 0, 0, 0, 0]
    >>> Zeros(3)[-3]
    0
    >>> Zeros(3)[-2]
    0
    >>> Zeros(4)[1:3]
    [0, 0]
    """

    yaml_tag='!zeros'

    def __init__(self, len):
        self.len = len

    @staticmethod
    def from_yaml_loader(loader, node):
        return Zeros(int(node.value))

    @staticmethod
    def yaml_representer(dumper, data):
        return dumper.represent_scalar(Zeros.yaml_tag, str(data.len))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [0 for key in range(*key.indices(self.len))]
        elif key > self.len-1 or key < -self.len:
            raise IndexError('Zeros index out of range')
        return 0

    def __len__(self):
        return self.len

    def __repr__(self):
        return 'Zeros({})'.format(repr(self.len))

yaml.add_representer(Zeros, Zeros.yaml_representer)
yaml.add_constructor(Zeros.yaml_tag, Zeros.from_yaml_loader)



class Pointer():
    """
    Represents a pointer into an array.
    >>> yaml.load('!ptr value')
    Pointer('value')
    >>> yaml.dump(Pointer("value"))
    "!ptr 'value'\\n"
    """
    yaml_tag = '!ptr'

    def __init__(self, data, offset=0):
        self.data = data
        self.offset = offset

    @staticmethod
    def from_yaml_loader(loader, node):
        return Pointer(node.value)

    @staticmethod
    def yaml_representer(dumper, data):
        return dumper.represent_scalar(Pointer.yaml_tag, data.data)

    def __repr__(self):
        return 'Pointer({})'.format(repr(self.data))

yaml.add_representer(Pointer, Pointer.yaml_representer)
yaml.add_constructor(Pointer.yaml_tag, Pointer.from_yaml_loader)


def transform(yaml):
    pass

