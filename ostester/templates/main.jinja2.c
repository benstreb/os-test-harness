#include <stdint.h>
{% for test_header in test_headers %}
#include "test-compare.c"
{% endfor %}


uint32_t test_main(void)
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
