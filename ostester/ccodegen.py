import re

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('ostester', 'templates'),
                  trim_blocks=True,
                  lstrip_blocks=True)


def header_to_function_name(header):
    """
    Returns the name of the entry point of a test suite given the header
    containing the suite
    >>> header_to_function_name('compare.h')
    'test_compare'
    >>> header_to_function_name('include/header.h')
    'test_include_header'
    >>> header_to_function_name('compare')
    Traceback (most recent call last):
        ...
    ValueError: invalid header name: 'compare'
    """
    word = '[a-zA-Z0-9_]+'
    header_regex = '({word}(/{word})*).h'.format(word=word)
    match = re.fullmatch(header_regex, header)
    return 'test_' + match.group(1).replace('/', '_')


def render_main(tested_headers):
    """
    Returns a string containing the entry point for the generated tests
    >>> import os
    >>> metadata = {'header': 'compare.h'}
    >>> main = render_main((metadata['header'],))
    >>> assert(main)
    >>> with open(os.devnull, 'w') as main_file:
    ...     print(main, file=main_file)
    """
    template = env.get_template('main.jinja2.c')
    tests = (header_to_function_name(h) for h in tested_headers)
    return template.render(test_includes=tested_headers,
                           test_function_names=tests)
