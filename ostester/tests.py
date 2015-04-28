import logging
import unittest
from doctest import DocTestSuite, REPORT_ONLY_FIRST_FAILURE, ELLIPSIS

import yaml

from . import ast, ccodegen, types, values, yamlreader


class YAMLParseTestCase(unittest.TestCase):
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
    @unittest.skip('Currently non-functional while arrays are worked on')
    def test_transform(self):
        with open('ostester/tests/test-compare.yaml') as fixture:
            parsetree = yamlreader.parse(fixture)
        ast.root(parsetree)

    def test_new_declarations(self):
        int = types.Int()
        decls = ast.new_declarations({}, [3], [int])
        self.assertEqual(len(decls), 1)
        self.assertEqual(decls[0].value, 3)
        self.assertEqual(decls[0].type, int)
        int_ptr = types.Pointer(int)
        decls = ast.new_declarations(
            {'value': 3},
            [yamlreader.Pointer('value')],
            [int_ptr])
        self.assertEqual(len(decls), 2)
        self.assertEqual(decls[0].value, 3)
        self.assertEqual(decls[0].type, int)
        self.assertEqual(decls[1].value, 'value')
        self.assertEqual(decls[1].type, int_ptr)
        int_ptr_ptr = types.Pointer(int_ptr)
        decls = ast.new_declarations(
            {'value': 3, 'inner_ptr': yamlreader.Pointer('value')},
            [yamlreader.Pointer('inner_ptr')],
            [int_ptr_ptr])
        self.assertEqual(len(decls), 3)
        self.assertEqual(decls[0].value, 3)
        self.assertEqual(decls[1].value, 'value')
        self.assertEqual(decls[2].value, 'inner_ptr')
        self.assertEqual(decls[2].type, int_ptr_ptr)


class TypeTestCase(unittest.TestCase):
    def test_functional(self):
        int = types.c_type('int')
        self.assertEqual(int.initialize('value', '1'),
                         'int value = 1')
        char = types.c_type('char')
        self.assertEqual(char.initialize('value', 'c'),
                         "char value = 'c'")

    def test_c_type(self):
        self.assertEqual(types.c_type('int').base_type, 'int')

    def test_simple_types(self):
        int = types.Int()
        int.base_type = 'int'
        self.assertEqual(int.declare('value'), 'int value')
        self.assertEqual(int.initialize('value', '1'),
                         'int value = 1')
        self.assertEqual(int.coerce('1'), 1)
        char = types.Char()
        self.assertEqual(char.initialize('value', 'a'),
                         "char value = 'a'")
        self.assertEqual(char.coerce('1'), '1')

    def test_pointer_type(self):
        ptr = types.Pointer(types.Int())
        self.assertEqual(ptr.declare('ptr'), 'int*ptr')
        nested_ptr = types.Pointer(ptr)
        self.assertEqual(nested_ptr.declare('np'), 'int**np')
        self.assertEqual(ptr.initialize('ptr', 0), 'int*ptr = 0')
        self.assertEqual(nested_ptr.coerce(3), 3)


class ValueTestCase(unittest.TestCase):
    def test_value(self):
        unnamed = values.Value(1)
        self.assertEqual(unnamed.value, 1)
        self.assertIsNot(unnamed.name, None)
        self.assertEqual(values.Value(1, 'number').name, 'number')
        typed = values.Value(1, 'number', 'int')
        self.assertEqual(typed.type, 'int')
        self.assertEqual(repr(typed), "Value(1, name='number', type='int')")

    def test_declaration(self):
        from . import types
        int = types.Int()
        test = values.Declaration(1, int, name='test')
        self.assertEqual(test.value, 1)
        self.assertEqual(test.type, int)
        self.assertEqual(test.name, 'test')
        self.assertEqual(repr(test),
                         "Declaration(value=1, type=int, name='test')")
        self.assertEqual(test.initialize(), 'int test = 1')
        unnamed = values.Declaration(1, int)
        self.assertIsNot(unnamed.name, None)


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


class IntegrationTestCase(unittest.TestCase):
    def test_front_to_back(self):
        with open("ostester/tests/test-compare.yaml", 'r') as f:
            yml = yamlreader.parse(f)
        ast_ = ast.transform(yml)
        ccodegen.render_main([ast_['header']])
        ccodegen.render_header_suite(ast_['header'], ast_['tests'])


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
