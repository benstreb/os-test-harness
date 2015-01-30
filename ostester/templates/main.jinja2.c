{% from 'suite.jinja2.c' import suite %}
#include <stdint.h>
{% for test_include in test_includes %}
#include "{{ test_include }}"
{% endfor %}

{{ suite('test_main', test_includes|map('header_to_function_name')) }}
