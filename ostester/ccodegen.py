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
        logger.info("main.c")
        logger.info(main_text)
        print(main_text, file=main)
    hsh_name = 'test_'+ast['header']
    with (gen_dir / hsh_name).open('w') as hsh:
        compare_text = render_header_suite_header(ast['header'])
        logger.info(hsh_name)
        logger.info(compare_text)
        print(compare_text, file=hsh)
    hs_name = hsh_name.replace('.h', '.c')
    with (gen_dir / hs_name).open('w') as header_suite:
        compare_text = render_header_suite(
            ast['header'], hsh_name, ast['tests'])
        logger.info(hs_name)
        logger.info(compare_text)
        print(compare_text, file=header_suite)


def render_main(tested_headers):
    """
    Returns a string containing the entry point for the generated tests
    """
    template = env.get_template('main.jinja2.c')
    return template.render(test_headers=tested_headers)


def render_header_suite_header(header):
    template = env.get_template('header_suite_header.jinja2.c')
    return template.render(function=header)


def render_header_suite(test_header, hs_header, functions):
    """
    Returns a string containing the entry point for the generated tests
    """
    template = env.get_template('header_suite.jinja2.c')
    return template.render(test_header_name=test_header,
                           header_suite_header_name=hs_header,
                           functions=functions)
