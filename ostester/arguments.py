import argparse


def parser():
    parser = argparse.ArgumentParser(
        description="Generates C code to perform tests specified by a YAML"
            "file",
    )
    parser.add_argument('yaml_file', help='the yaml file containing the tests')
    parser.add_argument('--output-dir', '-o', metavar='DIR', help='create the '
                        'files in DIR')
    return parser


def test_parser():
    parser = argparse.ArgumentParser(
        description="Generates C code to perform tests specified by a YAML"
            "file",
    )
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--test', '-t', action='store', nargs='?',
                        const=True, default=False,
                        help="Run the test suite")
    return parser
