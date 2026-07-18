#include <stdio.h>

/* C no tiene cierres: el estado (base) se pasa como parámetro. */
long sumar(long base, long x) {
    return base + x;
}

int main(void) {
    long base;
    if (scanf("%ld", &base) != 1) return 1;
    printf("r1=%ld r2=%ld\n", sumar(base, 1), sumar(base, 2));
    return 0;
}
