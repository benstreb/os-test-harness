import logging
import unittest
from doctest import DocTestSuite, REPORT_ONLY_FIRST_FAILURE, ELLIPSIS

import yaml

from . import ast, ccodegen, types, values, yamlreader


class YAMLParseTestCase(unittest.TestCase):
    @unittest.skip('Pointers are temporarily out of commision')
    def test_integration_parse(self):
        with open("ostester/tests/test-compare.yaml", 'r') as f:
            yml = yamlreader.parse(f)

    def test_zeroed(self):
        Zeroed = yamlreader.Zeroed
        self.assertEqual(yaml.safe_load("!zeroed 5"), Zeroed(5))
        self.assertEqual(yaml.dump(Zeroed(3)), "!zeroed '3'\n")
        self.assertEqual(list(Zeroed(7)), [0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(Zeroed(3)[-3], 0)
        self.assertEqual(Zeroed(3)[-2], 0)
        self.assertEqual(Zeroed(4)[1:3], [0, 0])

    def test_pointer(self):
        Pointer = yamlreader.Pointer
        ptr = yaml.safe_load('!ptr value')
        self.assertEqual(ptr, Pointer('value'))
        offset_ptr = yaml.safe_load('!ptr array+3')
        self.assertEqual(offset_ptr, Pointer('array', offset=3))
        self.assertEqual(yaml.dump(ptr), "!ptr 'value'\n")
        self.assertEqual(yaml.dump(offset_ptr), "!ptr 'array+3'\n")

    @unittest.skip('Pointers are temporarily out of commision')
    def test_signature(self):
        Signature = yamlreader.Signature
        sig = yaml.safe_load('int -> int')
        self.assertEqual(sig, Signature(inputs=['int'], output='int'))
        hard_sig = yaml.safe_load('int, char* -> char*')
        self.assertEqual(hard_sig,
                         Signature(inputs=['int', 'char*'], output='char*'))
        self.assertEqual(yaml.dump(sig), "!signature 'int -> int'\n")
        self.assertEqual(yaml.dump(hard_sig),
                         "!signature 'int, char* -> char*'\n")
        from .types import _CType
        self.assertTrue(all(isinstance(t, types._CType) for t in sig.inputs))
        self.assertTrue(isinstance(sig.output, types._CType))


class ASTTestCase(unittest.TestCase):
    @unittest.skip('Pointers are temporarily out of commision')
    def test_transform(self):
        with open('ostester/tests/test-compare.yaml') as fixture:
            parsetree = yamlreader.parse(fixture)
        ast.root(parsetree)


class ValueTestCase(unittest.TestCase):
    def test_value(self):
        unnamed = values.Value(1)
        self.assertEqual(unnamed.value, 1)
        self.assertIsNot(unnamed.name, None)
        self.assertEqual(values.Value(1, 'number').name, 'number')
        typed = values.Value(1, 'number', 'int')
        self.assertEqual(typed.type, 'int')
        self.assertEqual(repr(typed), "Value(1, name='number', type='int')")

    def test_type_value(self):
        from . import types
        int = types.c_type('int')
        test = values.TypeValue(1, int, name='test')
        self.assertEqual(test.value, 1)
        self.assertEqual(test.type, int)
        self.assertEqual(test.name, 'test')
        self.assertEqual(repr(test),
                         "TypeValue(value=1, type=int, name='test')")
        self.assertEqual(test.initialize(), 'int test = 1')
        unnamed = values.TypeValue(1, int)
        self.assertIsNot(unnamed.name, None)


@unittest.skip('Pointers are temporarily out of commision')
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
