#include <stdio.h>

long doblar(long x) {
    x = x * 2; /* modifica la copia local */
    return x;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long local = doblar(n);
    printf("original=%ld local=%ld\n", n, local);
    return 0;
}
