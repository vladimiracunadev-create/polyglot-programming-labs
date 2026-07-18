#include <stdio.h>
#include <string.h>

int main(void) {
    char n[64];
    if (scanf("%63s", n) != 1) return 1;
    printf("digitos=%d\n", (int) strlen(n));
    return 0;
}
