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
    [0, 0, 0]
    """

    def __init__(self, len):
        self.len = len

    @staticmethod
    def from_loader(loader, node):
        return Zeros(int(node.value))

    def __getitem__(self, i):
        if i > self.len-1 or i < -self.len:
            raise IndexError('Zeros index out of range')
        return 0

    def __len__(self):
        return self.len

    def __repr__(self):
        return 'Zeros({})'.format(repr(self.len))

yaml.add_representer(Zeros, lambda dumper, data:
    dumper.represent_scalar('!zeros', str(data.len)))
yaml.add_constructor('!zeros', Zeros.from_loader)


class Pointer(yaml.YAMLObject):
    yaml_tag = '!pointer'

    def __init__(self, data, offset):
        self.data = data
        self.offset = offset


def transform(yaml):
    pass

