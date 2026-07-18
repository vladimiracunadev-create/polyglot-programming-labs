#include <stdio.h>

/* En C la modularidad se hace por archivos .h/.c; aquí una función local. */
long doble(long n) {
    return 2 * n;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(n));
    return 0;
}
