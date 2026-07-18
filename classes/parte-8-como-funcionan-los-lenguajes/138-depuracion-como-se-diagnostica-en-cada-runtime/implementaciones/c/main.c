#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("valor=%ld cuadrado=%ld cubo=%ld\n", n, n * n, n * n * n);
    return 0;
}
