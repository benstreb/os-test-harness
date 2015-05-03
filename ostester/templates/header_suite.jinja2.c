{% from 'test_case.jinja2.c' import test_case %}
{% from 'suite.jinja2.c' import suite %}
#include <stdint.h>
#include "{{ test_header_name }}"

{% for function in functions %}
uint32_t {{ function.name }}()
{
    {% for test in function.test_cases %}
    {{ test_case(function, test) }}
    {% endfor %}
    return 0;
}
{% endfor %}

{{ suite(test_header_name, functions|map(attribute='name')) }}
