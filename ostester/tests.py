import logging
import unittest
from doctest import DocTestSuite, REPORT_ONLY_FIRST_FAILURE, ELLIPSIS

from . import ccodegen, yamlreader, ast, values


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
        self.assertTrue(main)
        logging.getLogger('tests').info(main)

    def test_header_suite_codegen(self):
        suite = ccodegen.render_header_suite(
            self.parse_tree[0]['header'],
            self.parse_tree[1],
        )
        self.assertTrue(suite)
        logging.getLogger('tests').info(suite)


class ASTTestCase(unittest.TestCase):
    def test_transform(self):
        with open('ostester/tests/test-compare.yaml') as fixture:
            parsetree = yamlreader.parse(fixture)
        ast.root(parsetree)


class TypeTestCase(unittest.TestCase):
    def test_value(self):
        unnamed = values.Value(1)
        self.assertEqual(unnamed.value, 1)
        self.assertNotEqual(unnamed.name, None)
        self.assertEqual(values.Value(1, 'number').name, 'number')
        typed = values.Value(1, 'number', 'int')
        self.assertEqual(typed.type, 'int')
        self.assertEqual(repr(typed), "Value(1, name='number', type='int')")


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
