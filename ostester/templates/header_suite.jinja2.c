{% from 'test_case.jinja2.c' import test_case %}
#include <stdint.h>
#include "compare.h"

uint32_t {{ function_name }}()
{
    {% for test in tests %}
    {% test_case(test) %}
    {% endfor %}
    return 0;
}

uint32_t test_compare_h()
{
    uint32_t success = 0;
    {% for test_function_name in test_function_names %}
    success = {{ test_function_name }}();
    if (success != 0)
    {
        return success;
    }
    {% endfor %}
    return success;
}
