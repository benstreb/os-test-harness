#include <stdint.h>
#include "test-compare.c"


uint32_t test_main(void)
{
    uint32_t success = 0;
    success = test_compare();
    if (success != 0)
    {
        return success;
    }
    return success;
}
