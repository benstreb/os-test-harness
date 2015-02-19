import unittest
from doctest import DocTestSuite

def load_tests(loader, tests, ignore):
    from . import yamlreader
    from . import ccodegen
    tests.addTests(DocTestSuite(yamlreader))
    tests.addTests(DocTestSuite(ccodegen))
    return tests


if __name__ == "__main__":
    unittest.main(package='ostester')
