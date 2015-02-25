import unittest
from doctest import DocTestSuite, REPORT_ONLY_FIRST_FAILURE

def load_tests(loader, tests, ignore):
    from . import yamlreader
    from . import ccodegen
    tests.addTests(DocTestSuite(yamlreader))
    tests.addTests(DocTestSuite(
        ccodegen, optionflags=REPORT_ONLY_FIRST_FAILURE))
    return tests
