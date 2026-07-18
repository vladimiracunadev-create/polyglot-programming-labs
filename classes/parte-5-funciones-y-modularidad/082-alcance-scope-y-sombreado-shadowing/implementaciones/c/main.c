#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long x = n;
    {
        long x = n + 10; /* sombrea a la externa dentro del bloque */
        printf("interno=%ld externo=%ld\n", x, n);
    }
    return 0;
}
