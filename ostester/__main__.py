import argparse
import logging
import sys
import unittest


parser = argparse.ArgumentParser(
    description="Generates C code to perform tests specified by a YAML file",
)
parser.add_argument('--test', '-t', action='store', nargs='?',
                    const=True, default=False,
                    help="Run the test suite")
parser.add_argument('--verbose', '-v', action='count', default=0)


args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig()

if args.test:
    from . import tests
    if args.test is not True:
        tests = unittest.defaultTestLoader.loadTestsFromName(args.test, tests)
    else:
        tests = unittest.defaultTestLoader.loadTestsFromModule(tests)

    unittest.TextTestRunner(verbosity=args.verbose+1).run(tests)
