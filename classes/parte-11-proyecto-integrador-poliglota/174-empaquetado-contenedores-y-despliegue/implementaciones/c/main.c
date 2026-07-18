#include <stdio.h>

int main(void) {
    char version[64];
    if (scanf("%63s", version) != 1) return 1;
    printf("imagen=app:%s\n", version);
    return 0;
}
