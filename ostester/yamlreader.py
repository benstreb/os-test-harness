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

    def __eq__(self, other):
        return isinstance(other, Zeroed) and other.len == self.len


class Pointer(yaml.YAMLObject):
    """
    Represents a pointer into an array.
    """
    yaml_loader = yaml.SafeLoader
    yaml_tag = '!ptr'

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_yaml(cls, loader, node):
        return Pointer(node.value.strip())

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(Pointer.yaml_tag, data.data)

    def __repr__(self):
        return 'Pointer({})'.format(repr(self.data))

    def __eq__(self, other):
        return (isinstance(other, Pointer) and
                other.data == self.data)


class Offset(yaml.YAMLObject):
    """
    Represents an array offset
    That is, a pointer of the form array + n
    """
    yaml_loader = yaml.SafeLoader
    yaml_tag = '!offset'

    def __init__(self, data, offset):
        self.data = data
        self.offset = int(offset)

    @classmethod
    def from_yaml(cls, loader, node):
        data, offset = map(str.strip, node.value.split('+'))
        return Offset(data, offset)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(
            Offset.yaml_tag, '{}+{}'.format(data.data, data.offset))

    def __repr__(self):
        return 'Offset({}, {})'.format(repr(self.data), self.offset)

    def __eq__(self, other):
        return (isinstance(other, Offset) and
                other.data == self.data and
                other.offset == self.offset)


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

    def __eq__(self, other):
        return (isinstance(other, Signature) and
                self.inputs == other.inputs and
                self.output == other.output)

yaml.SafeLoader.add_implicit_resolver('!signature', Signature.yaml_resolver, None)
