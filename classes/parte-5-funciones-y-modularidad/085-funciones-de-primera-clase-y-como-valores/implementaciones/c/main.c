#include <stdio.h>

long suma(long a, long b) { return a + b; }
long producto(long a, long b) { return a * b; }

long aplicar(long (*f)(long, long), long a, long b) {
    return f(a, b);
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("suma=%ld producto=%ld\n", aplicar(suma, a, b), aplicar(producto, a, b));
    return 0;
}
