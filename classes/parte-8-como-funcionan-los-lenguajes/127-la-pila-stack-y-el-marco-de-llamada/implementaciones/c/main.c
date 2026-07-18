#include <stdio.h>

long sumar(long n) {
    return n == 0 ? 0 : n + sumar(n - 1);
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("suma=%ld profundidad=%ld\n", sumar(n), n);
    return 0;
}
