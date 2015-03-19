import unittest
from doctest import DocTestSuite, REPORT_ONLY_FIRST_FAILURE, ELLIPSIS

def load_tests(loader, tests, ignore):
    from . import yamlreader
    from . import ccodegen
    from . import types
    from . import typevalues
    tests.addTests(DocTestSuite(yamlreader))
    tests.addTests(DocTestSuite(types))
    tests.addTests(DocTestSuite(
        ccodegen, optionflags=REPORT_ONLY_FIRST_FAILURE))
    tests.addTests(DocTestSuite(
        typevalues, optionflags=ELLIPSIS))
    return tests
