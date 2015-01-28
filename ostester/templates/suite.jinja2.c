{% macro suite(function, sub_functions) %}
uint32_t {{ function }}(void)
{
    uint32_t success = 0;
    {% for f in sub_functions %}
    success = {{ f }}();
    if (success != 0)
    {
        return success;
    }
    {% endfor %}
    return success;
}
{% endmacro %}
