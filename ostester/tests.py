import logging
import unittest
from doctest import DocTestSuite, REPORT_ONLY_FIRST_FAILURE, ELLIPSIS

from . import ccodegen, yamlreader, ast


class CodegenTestCase(unittest.TestCase):
    def setUp(self):
        self.parse_tree = [
            {'header': 'compare.h'},
            [{'name': 'compare',
             'type': yamlreader.Signature(inputs=['char', 'char*'],
                                          output='int'),
             'tests': [
                 {'args': ['a', ['a', 'b']],
                  'comparison': ast.comparisons['less_than'](0),
                  'number': 1}],
            }]]

    def test_main_codegen(self):
        main = ccodegen.render_main((self.parse_tree[0]['header'],))
        assert main
        logging.getLogger('tests').info(main)

    def test_header_suite_codegen(self):
        suite = ccodegen.render_header_suite(
            self.parse_tree[0]['header'],
            self.parse_tree[1],
        )
        assert suite
        logging.getLogger('tests').info(suite)


def load_tests(loader, tests, ignore):
    from . import yamlreader, ccodegen, types, values, ast
    tests.addTests(DocTestSuite(yamlreader))
    tests.addTests(DocTestSuite(types))
    tests.addTests(DocTestSuite(ast))
    tests.addTests(DocTestSuite(
        ccodegen, optionflags=REPORT_ONLY_FIRST_FAILURE))
    tests.addTests(DocTestSuite(
        values, optionflags=ELLIPSIS))
    return tests
