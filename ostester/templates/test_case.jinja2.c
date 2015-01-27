{% macro test_case(test) -%}
{% for declaration in test.declarations %}
{{ declaration.c_code() }}
{% endfor %}
{% result = newname() %}
{% fn = test.function %}
{{ fn.return_type.c_code(result) }} = {{ fn.c_code(args) }}
if (!({{ test.comparison.c_code(result) }}))
{
    return {{ test.number }};
}
{%- endmacro %}
