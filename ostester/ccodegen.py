from jinja2 import Environment, PackageLoader

from templateutils import header_to_function_name

env = Environment(loader=PackageLoader('ostester', 'templates'),
                  trim_blocks=True,
                  lstrip_blocks=True)
env.filters['header_to_function_name'] = header_to_function_name


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
    return template.render(test_includes=tested_headers)
