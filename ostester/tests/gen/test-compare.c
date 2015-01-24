#include <stdint.h>
#include "compare.h"

uint32_t test_compare()
{
    char array0[] = {'a', 'b'};
    int result0 = compare('a', array0);
    if (!(result0 < 0))
    {
        return 1;
    }
    char array1[] = {0, 0, 0};
    int result1 = compare(0, array1);
    if (!(result1 == 0))
    {
        return 2;
    }
    char array2[] = {'c', 'b', 'a'};
    int result2 = compare('b', array2+1);
    if (!(result2 > 0))
    {
        return 3;
    }
}

uint32_t test_compare_h()
{
    uint32_t success = 0;
    success = test_compare();
    if (success != 0)
    {
        return success;
    }
    return success;
}
