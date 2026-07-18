#include <stdio.h>

int main(void) {
    char version[64];
    if (scanf("%63s", version) != 1) return 1;
    printf("desplegado=v%s\n", version);
    return 0;
}
