#include <stdio.h>

long cuadrado(long n) {
    return n * n;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("puro=%ld\n", cuadrado(n));
    return 0;
}
