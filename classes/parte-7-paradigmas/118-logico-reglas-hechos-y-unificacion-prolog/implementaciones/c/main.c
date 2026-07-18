#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("divisor=%s\n", b % a == 0 ? "true" : "false");
    return 0;
}
