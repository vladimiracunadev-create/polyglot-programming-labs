#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("suma=%ld texto=%ld%ld\n", n + n, n, n);
    return 0;
}
