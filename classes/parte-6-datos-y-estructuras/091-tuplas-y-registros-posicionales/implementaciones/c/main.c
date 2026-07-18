#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene tuplas: se usa una struct. */
    struct Par { long a, b; } t = { b, a };
    printf("tupla=(%ld, %ld)\n", t.a, t.b);
    return 0;
}
