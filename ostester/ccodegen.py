import logging

from jinja2 import Environment, PackageLoader

from . import utils

env = Environment(loader=PackageLoader('ostester', 'templates'),
                  trim_blocks=True,
                  lstrip_blocks=True)
env.filters['header_to_function_name'] = utils.header_to_function_name
env.filters['function_test_case_name'] = utils.function_test_case_name
env.globals['new_name'] = utils.new_name


def generate_files(ast, gen_dir):
    logger = logging.getLogger('tests')
    with (gen_dir / 'main.c').open('w') as main:
        main_text = render_main([ast['header']])
        logger.info(main)
        print(main_text, file=main)
    with (gen_dir / 'compare.c').open('w') as compare:
        compare_text = render_header_suite(
            ast['header'], ast['tests'])
        logger.info(compare_text)
        print(compare_text, file=compare)


def render_main(tested_headers):
    """
    Returns a string containing the entry point for the generated tests
    """
    template = env.get_template('main.jinja2.c')
    return template.render(test_headers=tested_headers)


def render_header_suite_header(header):
    template = env.get_template('header_suite_header.jinja2.c')
    template.render(function=header)


def render_header_suite(header, functions):
    """
    Returns a string containing the entry point for the generated tests
    """
    template = env.get_template('header_suite.jinja2.c')
    return template.render(test_header_name=header,functions=functions)
