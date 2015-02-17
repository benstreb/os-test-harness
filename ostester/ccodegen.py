from jinja2 import Environment, PackageLoader

import utils

env = Environment(loader=PackageLoader('ostester', 'templates'),
                  trim_blocks=True,
                  lstrip_blocks=True)
env.filters['header_to_function_name'] = utils.header_to_function_name
env.globals['new_name'] = utils.new_name


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
    return template.render(test_headers=tested_headers)


def render_header_suite(header, functions):
    """
    Returns a string containing the entry point for the generated tests
    >>> import os
    >>> from ostester.yamlreader import Signature
    >>> header = 'compare.h'
    >>> functions = [{
    ...     'name': 'compare',
    ...     'type': Signature(inputs=['char', 'char*'], output='int'),
    ...     'tests': [
    ...         {'args': ['a', ['a', 'b']],
    ...          'less_than': 0}],
    ...     }]
    >>> suite = render_header_suite(header, functions)
    >>> assert(suite)
    >>> with open(os.devnull, 'w') as suite_file:
    ...     print(suite, file=suite_file)
    """
    template = env.get_template('header_suite.jinja2.c')
    return template.render(test_header_name=header,functions=functions)
