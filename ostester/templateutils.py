import re


def header_to_function_name(header):
    """
    Returns the name of the entry point of a test suite given the header
    containing the suite
    >>> header_to_function_name('compare.h')
    'test_compare_h'
    >>> header_to_function_name('include/header.h')
    'test_include_header_h'
    >>> header_to_function_name('compare')
    Traceback (most recent call last):
        ...
    ValueError: invalid header name: 'compare'
    >>> header_to_function_name('include.h/header.h')
    Traceback (most recent call last):
        ...
    ValueError: invalid header name: 'include.h/header.h'
    """
    word = '[a-zA-Z0-9_]+'
    header_regex = '({word}(/{word})*).h'.format(word=word)
    match = re.fullmatch(header_regex, header)
    if match is None:
        raise ValueError("invalid header name: '{}'".format(header))
    return 'test_{}_h'.format(match.group(1).replace('/', '_'))
