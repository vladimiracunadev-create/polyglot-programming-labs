#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long f = 1;
    for (long i = 1; i <= n; i++) {
        f *= i;
    }
    printf("factorial=%ld\n", f);
    return 0;
}
