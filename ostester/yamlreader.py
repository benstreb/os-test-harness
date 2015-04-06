"""
Reads in a yaml file representing a set of tests
"""

import collections.abc
from abc import ABCMeta
from io import StringIO
import re

import yaml

import ast
from .types import c_type


def parse(file):
    return yaml.safe_load(file)


class ABCYAMLMeta(ABCMeta, type(yaml.YAMLObject)): pass


class Zeroed(collections.abc.Sequence, yaml.YAMLObject, metaclass=ABCYAMLMeta):
    """
    Represents a zeroed region of memory in C
    """

    yaml_loader = yaml.SafeLoader
    yaml_tag='!zeroed'

    def __init__(self, len):
        self.len = len

    @classmethod
    def from_yaml(cls, loader, node):
        return Zeroed(int(node.value))

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(Zeroed.yaml_tag, str(data.len))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [0 for key in range(*key.indices(self.len))]
        elif key > self.len-1 or key < -self.len:
            raise IndexError('Zeroed index out of range')
        return 0

    def __len__(self):
        return self.len

    def __repr__(self):
        return 'Zeroed({})'.format(repr(self.len))


class Pointer(yaml.YAMLObject):
    """
    Represents a pointer into an array.
    """
    yaml_loader = yaml.SafeLoader
    yaml_tag = '!ptr'

    def __init__(self, data, offset=0):
        self.data = data
        self.offset = int(offset)

    @classmethod
    def from_yaml(cls, loader, node):
        args = map(str.strip, node.value.split('+'))
        return Pointer(*args)

    @classmethod
    def to_yaml(cls, dumper, data):
        if not data.offset:
            format_str = '{}'
        else:
            format_str = '{}+{}'
        return dumper.represent_scalar(
            Pointer.yaml_tag, format_str.format(data.data, data.offset))

    def __repr__(self):
        if not self.offset:
            format_str = 'Pointer({})'
        else:
            format_str = 'Pointer({}, offset={})'
        return format_str.format(repr(self.data), self.offset)


class Signature(yaml.YAMLObject):
    """
    Represents the signature of the function under test.
    """
    yaml_loader = yaml.SafeLoader
    yaml_tag='!signature'
    yaml_resolver = re.compile(r'.+->.+')

    def __init__(self, *, inputs, output):
        self.inputs = list(map(c_type, inputs))
        self.output = c_type(output)

    @classmethod
    def from_yaml(cls, loader, node):
        inputs, output = node.value.split('->')
        return Signature(
            inputs=[t.strip() for t in inputs.split(',')],
            output=output.strip(),
        )

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(
            Signature.yaml_tag,
            '{} -> {}'.format(
                ', '.join(map(str, data.inputs)),
                data.output,
            )
        )

    def __repr__(self):
        return 'Signature(inputs={}, output={})'.format(
            repr(self.inputs),
            repr(self.output),
        )

yaml.SafeLoader.add_implicit_resolver('!signature', Signature.yaml_resolver, None)


def transform(yaml):
    pass

