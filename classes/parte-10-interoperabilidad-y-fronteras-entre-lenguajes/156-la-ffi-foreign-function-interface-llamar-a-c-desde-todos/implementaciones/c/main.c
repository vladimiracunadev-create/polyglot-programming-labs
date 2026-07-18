#include <stdio.h>

long doble(long x) { return x * 2; } /* la funcion nativa en C */

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(n));
    return 0;
}
