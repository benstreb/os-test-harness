import collections.abc
from io import StringIO

import yaml

import ast


def parse(file):
    return yaml.safe_load(file)


def parse_from_string(string):
    return parse(StringIO(string))


class Zeros(collections.abc.Sequence):

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

