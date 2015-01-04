from io import StringIO

import yaml

import ast


def parse(file):
    return yaml.safe_load(file)


def parse_from_string(string):
    return parse(StringIO(string))


def transform(yaml):
    pass


