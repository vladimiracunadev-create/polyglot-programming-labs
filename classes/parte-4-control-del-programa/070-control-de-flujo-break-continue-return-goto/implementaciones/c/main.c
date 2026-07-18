#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long d = 2;
    for (; d <= n; d++) {
        if (n % d == 0) break;
    }
    printf("primer_divisor=%ld\n", d);
    return 0;
}
