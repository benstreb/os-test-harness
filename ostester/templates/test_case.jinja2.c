{% macro test_case(function, args, comparison, declarations=[]) -%}
{% for declaration in declarations %}
{{ declaration.c_code() }}
{% endfor %}
{% result = newname() %}
{{ function.return_type.c_code(result) }} = {{ function.c_code(args) }}
if (!({{ comparison.c_code(result) }}))
{
    return {{ number }};
}
{%- endmacro %}
