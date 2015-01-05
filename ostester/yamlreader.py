from io import StringIO

import yaml

import ast


def parse(file):
    return yaml.safe_load(file)


def parse_from_string(string):
    return parse(StringIO(string))


def zeros(count):
    return [0]*count
yaml.add_constructor('!zeros', zeros)


class Pointer(yaml.YAMLObject):
    yaml_tag = '!pointer'

    def __init__(self, data, offset):
        self.data = data
        self.offset = offset


def transform(yaml):
    pass

