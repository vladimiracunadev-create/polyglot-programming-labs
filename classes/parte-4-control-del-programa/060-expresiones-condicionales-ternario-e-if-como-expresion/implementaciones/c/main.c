#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long mx = a > b ? a : b;
    printf("max=%ld\n", mx);
    return 0;
}
