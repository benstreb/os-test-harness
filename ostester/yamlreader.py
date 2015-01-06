import collections.abc
from io import StringIO

import yaml

import ast


def parse(file):
    return yaml.safe_load(file)


def parse_from_string(string):
    return parse(StringIO(string))


class Zeros(collections.abc.Sequence):

    def __init__(self, count, *args, **kwargs):
        print(args, kwargs)
        self.len = count

    def __getitem__(self, i):
        return 0

    def __len__(self):
        return self.len

yaml.add_representer(Zeros, lambda dumper, data:
    dumper.represent_scalar('!zeros', "({})".format(data.len)))
yaml.add_constructor('!zeros', Zeros)


class Pointer(yaml.YAMLObject):
    yaml_tag = '!pointer'

    def __init__(self, data, offset):
        self.data = data
        self.offset = offset


def transform(yaml):
    pass

