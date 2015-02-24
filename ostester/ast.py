from collections import namedtuple
from functools import partial
from operator import eq, lt, gt


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
        return '{} {} {}'.format(arg, f, self.arg)


comparisons = {"equals": partial(BinOp, eq),
               "less_than": partial(BinOp, lt),
               "greater_than": partial(BinOp, gt),
              }
