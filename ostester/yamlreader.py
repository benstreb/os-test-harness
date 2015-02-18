"""
Reads in a yaml file representing a set of tests
>>> with open("ostester/tests/test-compare.yaml", 'r') as f:
...     yml = parse(f)
"""

import collections.abc
from abc import ABCMeta
from io import StringIO
import re

import yaml

import ast


def parse(file):
    return yaml.safe_load(file)


class ABCYAMLMeta(ABCMeta, type(yaml.YAMLObject)): pass


class Zeroed(collections.abc.Sequence, yaml.YAMLObject, metaclass=ABCYAMLMeta):
    """
    Represents a zeroed region of memory in C
    >>> yaml.safe_load("!zeroed 5")
    Zeroed(5)
    >>> yaml.dump(Zeroed(3))
    "!zeroed '3'\\n"
    >>> list(Zeroed(7))
    [0, 0, 0, 0, 0, 0, 0]
    >>> Zeroed(3)[-3]
    0
    >>> Zeroed(3)[-2]
    0
    >>> Zeroed(4)[1:3]
    [0, 0]
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
    >>> yaml.safe_load('!ptr value')
    Pointer('value')
    >>> yaml.safe_load('!ptr array+3')
    Pointer('array', offset=3)
    >>> yaml.dump(Pointer("value"))
    "!ptr 'value'\\n"
    >>> yaml.dump(Pointer("array", 2))
    "!ptr 'array+2'\\n"
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
    """Represents the signature of the function under test.
    >>> yaml.safe_load('int -> int')
    Signature(inputs=[int], output=int)
    >>> yaml.safe_load('int, char* -> char*')
    Signature(inputs=[int, char*], output=char*)
    >>> yaml.dump(Signature(inputs=['int'], output='int'))
    "!signature 'int -> int'\\n"
    >>> yaml.dump(Signature(inputs=['int', 'char*'], output='char*'))
    "!signature 'int, char* -> char*'\\n"
    >>> sig = Signature(inputs=['int', 'char*'], output='char*')
    >>> all(type(t) == CType for t in sig.inputs)
    True
    >>> type(sig.output) == CType
    True
    """
    yaml_loader = yaml.SafeLoader
    yaml_tag='!signature'
    yaml_resolver = re.compile(r'.+->.+')

    def __init__(self, *, inputs, output):
        self.inputs = inputs
        self.output = output

    @classmethod
    def from_yaml(cls, loader, node):
        inputs, output = node.value.split('->')
        return Signature(
            inputs=[CType(t.strip()) for t in inputs.split(',')],
            output=CType(output.strip()),
        )

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(
            Signature.yaml_tag,
            '{} -> {}'.format(', '.join(data.inputs), data.output)
        )

    def __repr__(self):
        return 'Signature(inputs={}, output={})'.format(
            repr(self.inputs),
            repr(self.output),
        )

yaml.SafeLoader.add_implicit_resolver('!signature', Signature.yaml_resolver, None)


class CType:
    """
    Represents en expression type in C.
    >>> t = CType("int*[3]")
    >>> t
    int*[3]
    >>> t.declare("values")
    'int *values[3]'
    """
    type_spec = re.compile(r'(\w+)\s*(\**)\s*((\[\d+\])*)')

    def __init__(self, type_decl):
        self.base_type, self.stars, self.arrays, _ = self.type_spec.match(
            type_decl).groups()

    def declare(self, name):
        return '{} {}{}{}'.format(
            self.base_type,
            self.stars,
            name,
            self.arrays,
        )

    def __repr__(self):
        return '{}{}{}'.format(
            self.base_type,
            self.stars,
            self.arrays,
        )


def transform(yaml):
    pass

