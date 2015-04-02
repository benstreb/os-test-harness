from collections import namedtuple
from functools import partial

from .values import TypeValue


def transform(parsetree):
    """
    Takes in a parse tree and processes it to return an AST
    """
    return root(parsetree)


def root(test_list):
    metadata, *tests = test_list
    return {'header': metadata['header'],
            'tests': list(map(function_test, tests))}


def function_test(test):
    function_type = test['type']
    return {'name': test['function'],
            'type': function_type,
            'test_cases': [test_case(test, function_type)
                for test in test['tests']]}


def test_case(test_case, function_type):
    declarations = []
    args = [TypeValue(t, v) for t, v in
            zip(test_case['args'], function_type.inputs)]
    comparison, = test_case.keys() & comparisons
    return {'declarations': declarations,
            'arguments': args,
            'comparison': comparisons[comparison](test_case[comparison])}


class BinOp(namedtuple('BinOp', ('f', 'arg'))):
    __slots__ = ()
    def compare_with(self, arg):
        return '{} {} {}'.format(arg, self.f, self.arg)


comparisons = {"equals": partial(BinOp, '=='),
               "less_than": partial(BinOp, '<'),
               "greater_than": partial(BinOp, '>'),
              }
