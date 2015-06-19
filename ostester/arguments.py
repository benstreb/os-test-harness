import argparse


def parser():
    parser = argparse.ArgumentParser(
        description="Generates C code to perform tests specified by a YAML"
            "file",
    )
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--test', '-t', action='store', nargs='?',
                        const=True, default=False,
                        help="Run the test suite")
    return parser
