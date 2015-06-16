{% from 'suite.jinja2.c' import suite %}
#include <stdint.h>
{% for test_header in test_headers %}
#include "{{ 'test_' + test_header }}"
{% endfor %}

{{ suite('test_main', test_headers|map('header_to_function_name')) }}
