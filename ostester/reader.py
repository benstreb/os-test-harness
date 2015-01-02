import yaml
from io import StringIO
from collections import namedtuple


def parse(file):
    yaml = yaml.safe_load(file)


def parse_from_string(string):
    return parse(StringIO(string))


def Metadata(header, **kwargs):
    return {"header": header}
