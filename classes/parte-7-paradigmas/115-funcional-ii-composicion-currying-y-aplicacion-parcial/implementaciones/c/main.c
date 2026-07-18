#include <stdio.h>

long doblar(long x) { return x * 2; }
long incrementar(long x) { return x + 1; }

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", incrementar(doblar(n)));
    return 0;
}
