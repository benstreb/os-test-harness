import yaml
from io import StringIO
from collections import namedtuple


def parse(file):
    yaml = yaml.safe_load(file)


def parse_from_string(string):
    return parse(StringIO(string))


def FileMetadata(header, **kwargs):
    return {"header": header}


def FunctionTests(function_name, tests, metadata={}):
    return {"function": function_name,
            "tests": tests,
            "metadata": metadata}


def TestCase(declarations, test_arguments, comparison):
    return {"declarations": declarations,
            "arguments": arguments,
            "comparison": comparison}
