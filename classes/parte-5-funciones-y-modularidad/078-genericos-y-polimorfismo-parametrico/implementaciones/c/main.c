#include <stdio.h>

/* C no tiene genéricos: se escribe una función por tipo (o macros). */
long mayor(long a, long b) {
    return a > b ? a : b;
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("max=%ld\n", mayor(a, b));
    return 0;
}
