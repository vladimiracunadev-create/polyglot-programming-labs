#include <stdio.h>

long suma(long a, long b) {
    return a + b;
}

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("suma=%ld\n", suma(a, b));
    return 0;
}
