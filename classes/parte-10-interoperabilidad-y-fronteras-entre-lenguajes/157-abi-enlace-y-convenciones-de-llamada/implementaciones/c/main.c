#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("abi=%s\n", a == b ? "compatible" : "incompatible");
    return 0;
}
