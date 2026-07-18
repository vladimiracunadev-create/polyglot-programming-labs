#include <stdio.h>

/* C devuelve un valor; el segundo va por puntero. */
long divmod(long a, long b, long *resto) {
    *resto = a % b;
    return a / b;
}

int main(void) {
    long a, b, r;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long q = divmod(a, b, &r);
    printf("cociente=%ld resto=%ld\n", q, r);
    return 0;
}
