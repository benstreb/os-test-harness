{% macro test_case(fn, test) %}
{% for declaration in test.declarations %}
{{ declaration.c_code() }};
{% endfor %}
{% set result = new_name() %}
{{ fn.type.output.declare(result) }} = {{ fn.c_code(args) }};
if (!({{ test.comparison.c_code(result) }}))
{
    return {{ test.number }};
}
{% endmacro %}
