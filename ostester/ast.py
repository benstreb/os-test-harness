from collections import namedtuple

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
    def compare(self, arg):
        return '{} {} {}'.format(arg, f, self.arg)
