#include <stdint.h>
{% for test_include in test_includes %}
#include "{{ test_include }}"
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
