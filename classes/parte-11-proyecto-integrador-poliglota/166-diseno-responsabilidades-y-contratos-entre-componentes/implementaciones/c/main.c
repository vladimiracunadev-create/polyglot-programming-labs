#include <stdio.h>
#include <string.h>

int main(void) {
    char a[64], b[64];
    if (scanf("%63s %63s", a, b) != 2) return 1;
    printf("contrato=%s\n", strcmp(a, b) == 0 ? "compatible" : "incompatible");
    return 0;
}
