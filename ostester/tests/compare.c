#include <stdio.h>
#include "test_main.h"

int main(void) {
    return test_main();
}

int compare(char chr, char* str) {
    for (int i = 0; str[i] != 0; i++) {
        if (str[i] < chr) {
            return 1;
        } else if (str[i] > chr) {
            return -1;
        }
    }
    return 0;
}