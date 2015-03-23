from collections import namedtuple
from functools import partial


def transform(parsetree):
    """
    Takes in a parse tree and processes it to return an AST
    >>> from .yamlreader import parse
    >>> with open('ostester/tests/test-compare.yaml') as fixture:
    ...     parsetree = parse(fixture)
    """
    pass


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


class BinOp(namedtuple('BinOp', ('f', 'arg'))):
    __slots__ = ()
    def compare_with(self, arg):
        return '{} {} {}'.format(arg, self.f, self.arg)


comparisons = {"equals": partial(BinOp, '=='),
               "less_than": partial(BinOp, '<'),
               "greater_than": partial(BinOp, '>'),
              }
