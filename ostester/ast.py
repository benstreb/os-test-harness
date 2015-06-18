from collections import namedtuple
from functools import partial

from .values import Declaration
from . import yamlreader as yr
from . import types
from . import utils


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


test_number = 0
def test_case(test_case, function_type):
    global test_number
    # Pointer in args
    # Literals in args
    declarations, args = new_declarations(test_case.get('data', {}),
                                          test_case['args'],
                                          function_type.inputs)
    comparison, = test_case.keys() & comparisons
    test_number += 1
    return {'declarations': declarations,
            'arguments': args,
            'comparison': comparisons[comparison](test_case[comparison]),
            'number': test_number}


def new_declarations(explicit_declarations, args, function_inputs):
    new_declarations = []
    arg_values = []
    for arg, type in zip(args, function_inputs):
        if isinstance(arg, yr.Pointer) or isinstance(arg, yr.Declaration):
            d, a = recursive_declarations(explicit_declarations,
                                          arg, utils.new_name(), type)
            new_declarations.extend(d)
            arg_values.extend(a)
        else:
            d = Declaration(arg, type)
            new_declarations.append(d)
            arg_values.append(d)
    return (new_declarations, arg_values)


def recursive_declarations(declarations, arg, name, type):
    if isinstance(arg, yr.Pointer):
        inner_type = type.inner_type
        d, a = recursive_declarations(declarations,
                                      declarations[arg.data],
                                      arg.data,
                                      inner_type)
        return (d + [Declaration(arg.data, type, name)], a)
    elif isinstance(arg, yr.Declaration):
        d = Declaration(declarations[arg.name], type, arg.name)
    else:
        d = Declaration(declarations[name], type, name)
    return ([d], [d])


class BinOp(namedtuple('BinOp', ('f', 'arg'))):
    __slots__ = ()
    def compare_with(self, arg):
        return '{} {} {}'.format(arg, self.f, self.arg)


comparisons = {"equals": partial(BinOp, '=='),
               "less_than": partial(BinOp, '<'),
               "greater_than": partial(BinOp, '>'),
              }
