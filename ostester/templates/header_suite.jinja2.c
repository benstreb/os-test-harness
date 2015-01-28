{% from 'test_case.jinja2.c' import test_case %}
{% from 'suite.jinja2.c' import suite %}
#include <stdint.h>
#include "compare.h"

uint32_t {{ function_name }}()
{
    {% for test in tests %}
    {% test_case(test) %}
    {% endfor %}
    return 0;
}

{% suite(test_header_name, test_function_names %}
