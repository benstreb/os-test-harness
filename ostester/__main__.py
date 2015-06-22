import argparse
import logging
import unittest
from . import arguments


parser = arguments.test_parser()
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
